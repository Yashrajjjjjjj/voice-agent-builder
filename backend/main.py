from fastapi import FastAPI, WebSocket, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import firestore, storage as fb_storage, credentials
from groq import Groq
import httpx
import json
import os
import asyncio
from datetime import datetime, timedelta
import base64
from typing import Dict, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Init Firebase
try:
    if not firebase_admin.get_app():
        firebase_admin.initialize_app()
except ValueError:
    pass

db = firestore.client()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="Indian Voice Agent Builder")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
REPLICATE_API = "https://api.replicate.com/v1"

INDIAN_LANGUAGES = {
    "hi": {"name": "Hindi", "code": "hi-IN"},
    "ta": {"name": "Tamil", "code": "ta-IN"},
    "te": {"name": "Telugu", "code": "te-IN"},
    "kn": {"name": "Kannada", "code": "kn-IN"},
    "ml": {"name": "Malayalam", "code": "ml-IN"},
    "bn": {"name": "Bengali", "code": "bn-IN"},
    "gu": {"name": "Gujarati", "code": "gu-IN"},
    "mr": {"name": "Marathi", "code": "mr-IN"},
    "en": {"name": "English (Indian)", "code": "en-IN"},
}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported Indian languages"""
    return {
        "languages": list(INDIAN_LANGUAGES.values()),
        "count": len(INDIAN_LANGUAGES)
    }


@app.post("/api/agents")
async def create_agent(
    name: str = Form(...),
    job_role: str = Form(...),
    system_instruction: str = Form(...),
    primary_language: str = Form(default="hi"),
    supported_languages: List[str] = Form(default=["hi", "en"]),
    user_id: str = Form(...),
):
    """Create a new voice agent"""
    try:
        agent_id = f"agent_{int(datetime.utcnow().timestamp())}_{os.urandom(4).hex()}"
        
        agent_data = {
            "id": agent_id,
            "name": name,
            "job_role": job_role,
            "system_instruction": system_instruction,
            "primary_language": primary_language,
            "supported_languages": supported_languages,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "status": "active"
        }
        
        db.collection("agents").document(agent_id).set(agent_data)
        
        logger.info(f"Agent created: {agent_id}")
        return {
            "success": True,
            "agent_id": agent_id,
            "message": f"Agent '{name}' created successfully",
            "agent": agent_data
        }
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    try:
        agent_doc = db.collection("agents").document(agent_id).get()
        if not agent_doc.exists:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"success": True, "agent": agent_doc.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/agents")
async def list_agents(user_id: str):
    """List all agents for a user"""
    try:
        agents_ref = db.collection("agents").where("user_id", "==", user_id).stream()
        agents = [doc.to_dict() for doc in agents_ref]
        return {"success": True, "agents": agents, "count": len(agents)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/clone-voice")
async def clone_voice(user_id: str = Form(...), file: UploadFile = File(...)):
    """Upload and store voice clone"""
    try:
        contents = await file.read()
        
        # Store in Cloud Storage
        bucket = fb_storage.bucket()
        blob = bucket.blob(f"voice_clones/{user_id}/{file.filename}")
        blob.upload_from_string(contents, content_type=file.content_type)
        
        # Store metadata
        voice_id = f"voice_{int(datetime.utcnow().timestamp())}_{os.urandom(4).hex()}"
        db.collection("voice_library").document(voice_id).set({
            "voice_id": voice_id,
            "user_id": user_id,
            "voice_file": f"voice_clones/{user_id}/{file.filename}",
            "filename": file.filename,
            "created_at": datetime.utcnow().isoformat(),
            "status": "ready"
        })
        
        logger.info(f"Voice cloned for user: {user_id}")
        return {"success": True, "voice_id": voice_id, "message": "Voice cloned successfully"}
    except Exception as e:
        logger.error(f"Error cloning voice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/voice-library/{user_id}")
async def get_voice_library(user_id: str):
    """Get user's voice library"""
    try:
        voices_ref = db.collection("voice_library").where("user_id", "==", user_id).stream()
        voices = [doc.to_dict() for doc in voices_ref]
        return {"success": True, "voices": voices, "count": len(voices)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.websocket("/ws/voice-agent/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for real-time voice conversations"""
    await websocket.accept()
    
    try:
        # Get agent details
        agent_doc = db.collection("agents").document(agent_id).get()
        if not agent_doc.exists:
            await websocket.send_json({"error": "Agent not found"})
            await websocket.close()
            return
        
        agent = agent_doc.to_dict()
        lang = agent.get("primary_language", "hi")
        
        await websocket.send_json({"type": "ready", "message": "Agent ready for conversation"})
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "audio":
                audio_b64 = data.get("audio")
                
                try:
                    # STT via Replicate Whisper
                    stt_response = await call_replicate_async(
                        model="openai/whisper",
                        input={"audio": f"data:audio/wav;base64,{audio_b64}", "language": lang}
                    )
                    user_text = stt_response.get("transcription", "")
                    
                    if user_text:
                        await websocket.send_json({"type": "transcription", "text": user_text})
                        
                        # LLM via Groq
                        llm_response = groq_client.chat.completions.create(
                            model="mixtral-8x7b-32768",
                            messages=[
                                {
                                    "role": "system",
                                    "content": f"{agent.get('system_instruction')} (Respond in {INDIAN_LANGUAGES[lang]['name']}, keep response under 50 words)"
                                },
                                {"role": "user", "content": user_text}
                            ],
                            max_tokens=100,
                        )
                        ai_response = llm_response.choices[0].message.content
                        
                        await websocket.send_json({"type": "ai_response", "text": ai_response})
                        
                        # TTS via Replicate XTTS-v2
                        tts_response = await call_replicate_async(
                            model="cjwbw/xtts_v2",
                            input={
                                "text": ai_response,
                                "language": lang.split("-")[0]  # Use language code only
                            }
                        )
                        
                        audio_url = tts_response.get("audio", tts_response.get("audio_url"))
                        if audio_url:
                            async with httpx.AsyncClient(timeout=60) as client:
                                try:
                                    audio_data = (await client.get(audio_url)).content
                                    audio_b64_response = base64.b64encode(audio_data).decode()
                                    await websocket.send_json({"type": "audio", "audio": audio_b64_response})
                                except Exception as e:
                                    logger.error(f"Error fetching audio: {str(e)}")
                                    await websocket.send_json({"type": "error", "message": "Audio generation failed"})
                except Exception as e:
                    logger.error(f"Error in conversation: {str(e)}")
                    await websocket.send_json({"type": "error", "message": str(e)})
    
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()


async def call_replicate_async(model: str, input: dict):
    """Call Replicate API asynchronously"""
    try:
        headers = {"Authorization": f"Token {REPLICATE_API_KEY}"}
        async with httpx.AsyncClient(timeout=180) as client:
            # Create prediction
            response = await client.post(
                f"{REPLICATE_API}/predictions",
                json={"version": model, "input": input},
                headers=headers
            )
            
            if response.status_code != 201:
                logger.error(f"Replicate API error: {response.text}")
                return {"error": "API call failed"}
            
            pred_id = response.json().get("id")
            
            # Poll for result
            for attempt in range(120):  # 2 minutes timeout
                result = (await client.get(
                    f"{REPLICATE_API}/predictions/{pred_id}",
                    headers=headers
                )).json()
                
                if result.get("status") == "succeeded":
                    return result.get("output", {})
                elif result.get("status") == "failed":
                    error_msg = result.get("error", "Unknown error")
                    logger.error(f"Replicate prediction failed: {error_msg}")
                    return {"error": error_msg}
                
                await asyncio.sleep(1)
            
            return {"error": "Request timeout"}
    except Exception as e:
        logger.error(f"Error calling Replicate: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
