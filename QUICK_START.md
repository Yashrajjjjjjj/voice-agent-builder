# QUICK START - Deploy in 30 Minutes

## Step 1: Get API Keys (5 min)

### Groq API Key
1. Go to https://console.groq.com/keys
2. Login (use Google or GitHub)
3. Copy your API key
4. Save it somewhere safe

### Replicate API Key  
1. Go to https://replicate.com/signin
2. Login (use Google account)
3. Go to https://replicate.com/account/api-tokens
4. Copy your token

## Step 2: Clone & Setup Backend (10 min)

```bash
git clone https://github.com/Yashrajjjjjjj/voice-agent-builder
cd voice-agent-builder

# Create backend folder
mkdir -p backend
cd backend

# Create .env file
echo 'GROQ_API_KEY=your_groq_key_here' > .env
echo 'REPLICATE_API_KEY=your_replicate_key_here' >> .env

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==11.0.3
firebase-admin==6.2.0
groq==0.4.1
httpx==0.25.1
pydantic==2.5.0
python-multipart==0.0.6
EOF

# Install dependencies
pip install -r requirements.txt

# Create main.py with complete backend code
cat > main.py << 'EOF'
from fastapi import FastAPI, WebSocket, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import firestore, storage as fb_storage
from groq import Groq
import httpx
import json
import os
import asyncio
from datetime import datetime, timedelta

# Init Firebase
if not firebase_admin.get_app():
    firebase_admin.initialize_app()

db = firestore.client()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="Voice Agent Builder")

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
    "hi": {"name": "Hindi", "code": "hi"},
    "ta": {"name": "Tamil", "code": "ta"},
    "te": {"name": "Telugu", "code": "te"},
    "kn": {"name": "Kannada", "code": "kn"},
    "ml": {"name": "Malayalam", "code": "ml"},
    "bn": {"name": "Bengali", "code": "bn"},
    "gu": {"name": "Gujarati", "code": "gu"},
    "mr": {"name": "Marathi", "code": "mr"},
    "en": {"name": "English (Indian)", "code": "en"},
}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/agents")
async def create_agent(config: dict):
    try:
        agent_id = f"agent_{int(datetime.utcnow().timestamp())}_{os.urandom(4).hex()}"
        
        agent_data = {
            "id": agent_id,
            "name": config.get("name", "Untitled Agent"),
            "job_role": config.get("job_role", ""),
            "system_instruction": config.get("system_instruction", ""),
            "primary_language": config.get("primary_language", "hi"),
            "supported_languages": config.get("supported_languages", ["hi", "en"]),
            "voice_clone_id": config.get("voice_clone_id"),
            "created_at": datetime.utcnow().isoformat(),
            "user_id": config.get("user_id"),
        }
        
        db.collection("agents").document(agent_id).set(agent_data)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "message": f"Agent '{config.get('name')}' created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/clone-voice")
async def clone_voice(user_id: str, file: UploadFile):
    try:
        contents = await file.read()
        
        # Store in Cloud Storage
        bucket = fb_storage.bucket()
        blob = bucket.blob(f"voice_clones/{user_id}/{file.filename}")
        blob.upload_from_string(contents, content_type=file.content_type)
        
        # Store metadata
        db.collection("voice_library").document(user_id).set({
            "user_id": user_id,
            "voice_file": f"voice_clones/{user_id}/{file.filename}",
            "filename": file.filename,
            "created_at": datetime.utcnow().isoformat(),
            "status": "ready"
        })
        
        return {"success": True, "voice_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.websocket("/ws/voice-agent/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    await websocket.accept()
    
    try:
        agent_doc = db.collection("agents").document(agent_id).get()
        if not agent_doc.exists:
            await websocket.send_json({"error": "Agent not found"})
            await websocket.close()
            return
        
        agent = agent_doc.to_dict()
        lang = agent.get("primary_language", "hi")
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "audio":
                audio_b64 = data.get("audio")
                
                # STT via Replicate
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
                        messages=[{
                            "role": "system",
                            "content": f"{agent.get('system_instruction')} (Respond in {INDIAN_LANGUAGES[lang]['name']})"
                        }, {"role": "user", "content": user_text}],
                        max_tokens=150,
                    )
                    ai_response = llm_response.choices[0].message.content
                    
                    # TTS via Replicate
                    tts_response = await call_replicate_async(
                        model="cjwbw/xtts_v2",
                        input={"text": ai_response, "language": lang}
                    )
                    
                    audio_url = tts_response.get("audio_url")
                    if audio_url:
                        async with httpx.AsyncClient() as client:
                            audio_data = (await client.get(audio_url)).content
                        await websocket.send_bytes(audio_data)
    
    except Exception as e:
        print(f"Error: {e}")

async def call_replicate_async(model: str, input: dict):
    headers = {"Authorization": f"Token {REPLICATE_API_KEY}"}
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(f"{REPLICATE_API}/predictions", json={"version": model, "input": input}, headers=headers)
        pred_id = response.json().get("id")
        
        for _ in range(120):
            result = (await client.get(f"{REPLICATE_API}/predictions/{pred_id}", headers=headers)).json()
            if result.get("status") == "succeeded":
                return result.get("output", {})
            elif result.get("status") == "failed":
                return {"error": result.get("error")}
            await asyncio.sleep(0.5)
    return {"error": "Timeout"}
EOF

# Test locally
uvicorn main:app --reload
```

## Step 3: Deploy to Cloud Run (10 min)

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Deploy
gcloud run deploy voice-agent \
  --source . \
  --platform managed \
  --region asia-south1 \
  --memory 2Gi \
  --timeout 3600 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=YOUR_KEY,REPLICATE_API_KEY=YOUR_KEY
```

## Step 4: Frontend (5 min)

```bash
# Create frontend folder
mkdir -p ../frontend
cd ../frontend

# Initialize React
npm init -y
npm install react react-dom axios

# Create index.html and main app (simplified for now)
# Will expand based on deployment feedback

# Deploy to Vercel
npm install -g vercel
vercel deploy --prod
```

## Testing

Once deployed, test at:
```
https://your-cloud-run-url.run.app/health
```

## Environment Variables Needed

```
GROQ_API_KEY=xxxxxxxxxxx
REPLICATE_API_KEY=xxxxxxxxxxx
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Next Steps

1. Test STT/TTS with curl
2. Build React dashboard  
3. Add voice cloning
4. Scale to production

## Support

If stuck, check:
- API keys are correct
- Cloud Run memory is 2Gi minimum
- Firebase is initialized
- All environment variables are set
