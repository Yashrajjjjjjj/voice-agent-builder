# Indian Voice Agent Builder - Main FastAPI Application
# Comprehensive API endpoint for all voice agent services

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional, List

# Import all service modules
from llm_service import LLMService
from tts_service import TTSService
from stt_service import STTService
from asr_service import ASRService
from voice_cloning_service import VoiceCloningService
from phone_integration_service import PhoneIntegrationService
from agent_management_service import AgentManagementService
from config import (
    INDIAN_LANGUAGES,
    LLM_PROVIDERS,
    TTS_PROVIDERS,
    STT_PROVIDERS,
    FALLBACK_CHAINS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Indian Voice Agent Builder API",
    description="Comprehensive API for creating and managing Indian voice agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize all services
llm_service = LLMService()
tts_service = TTSService()
stt_service = STTService()
asr_service = ASRService()
voice_cloning_service = VoiceCloningService()
phone_service = PhoneIntegrationService()
agent_service = AgentManagementService()

# Pydantic models
class AgentCreateRequest(BaseModel):
    name: str
    job_role: str
    system_instruction: str
    language: str
    llm_provider: Optional[str] = "groq"
    tts_provider: Optional[str] = "replicate_xtts"
    stt_provider: Optional[str] = "google_stt"
    voice_id: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class TextGenerationRequest(BaseModel):
    prompt: str
    language: str
    provider: Optional[str] = "groq"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class TextToSpeechRequest(BaseModel):
    text: str
    language: str
    voice_id: Optional[str] = None
    provider: Optional[str] = "replicate_xtts"
    speed: Optional[float] = 1.0

class PhoneCallRequest(BaseModel):
    phone_number: str
    agent_id: str
    provider: Optional[str] = "vapi"
    message: Optional[str] = None

# Health Check Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Indian Voice Agent Builder"}

@app.get("/status")
async def status():
    """Get service status"""
    return {
        "llm_service": "active",
        "tts_service": "active",
        "stt_service": "active",
        "asr_service": "active",
        "voice_cloning_service": "active",
        "phone_integration_service": "active",
        "agent_management_service": "active"
    }

# Configuration Endpoints
@app.get("/config/languages")
async def get_supported_languages():
    """Get all supported Indian languages"""
    return INDIAN_LANGUAGES

@app.get("/config/llm-providers")
async def get_llm_providers():
    """Get all LLM providers"""
    return {provider: config["name"] for provider, config in LLM_PROVIDERS.items()}

@app.get("/config/tts-providers")
async def get_tts_providers():
    """Get all TTS providers"""
    return {provider: config["name"] for provider, config in TTS_PROVIDERS.items()}

@app.get("/config/stt-providers")
async def get_stt_providers():
    """Get all STT providers"""
    return {provider: config["name"] for provider, config in STT_PROVIDERS.items()}

# Agent Management Endpoints
@app.post("/agents/create")
async def create_agent(request: AgentCreateRequest):
    """Create a new voice agent"""
    result = agent_service.create_agent(
        name=request.name,
        job_role=request.job_role,
        system_instruction=request.system_instruction,
        language=request.language,
        llm_provider=request.llm_provider,
        tts_provider=request.tts_provider,
        stt_provider=request.stt_provider,
        voice_id=request.voice_id,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent configuration"""
    result = agent_service.get_agent(agent_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/agents")
async def list_agents(language: Optional[str] = None):
    """List all agents, optionally filtered by language"""
    result = agent_service.list_agents(language)
    return result

# LLM Endpoints
@app.post("/llm/generate")
async def generate_text(request: TextGenerationRequest):
    """Generate text using LLM"""
    result = await llm_service.generate(
        prompt=request.prompt,
        language=request.language,
        provider=request.provider,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    if "error" in result and result["error"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# TTS Endpoints
@app.post("/tts/synthesize")
async def synthesize_speech(request: TextToSpeechRequest):
    """Synthesize speech from text"""
    result = await tts_service.synthesize(
        text=request.text,
        language=request.language,
        voice_id=request.voice_id,
        provider=request.tts_provider,
        speed=request.speed
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Voice Cloning Endpoints
@app.post("/voice-cloning/clone")
async def clone_voice(
    voice_name: str,
    language: str,
    provider: Optional[str] = "replicate_xtts",
    file: UploadFile = File(...)
):
    """Clone voice from audio sample"""
    # Save uploaded file temporarily
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    result = await voice_cloning_service.clone_voice(
        voice_samples=[tmp_path],
        voice_name=voice_name,
        provider=provider,
        language=language
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Voice cloning failed"))
    return result

@app.get("/voice-cloning/voices")
async def list_cloned_voices():
    """List all cloned voices"""
    voices = voice_cloning_service.list_cloned_voices()
    return {"voices": voices, "count": len(voices)}

# Phone Integration Endpoints
@app.post("/phone/call")
async def make_phone_call(request: PhoneCallRequest):
    """Make outbound call"""
    result = await phone_service.make_call(
        phone_number=request.phone_number,
        agent_id=request.agent_id,
        provider=request.provider,
        message=request.message
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Call initiation failed"))
    return result

@app.get("/phone/call/{call_id}/status")
async def get_call_status(call_id: str, provider: str):
    """Get call status"""
    result = await phone_service.get_call_status(call_id, provider)
    return result

@app.post("/phone/call/{call_id}/hang-up")
async def hang_up_call(call_id: str, provider: str):
    """Hang up call"""
    result = await phone_service.hang_up_call(call_id, provider)
    return result

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Indian Voice Agent Builder API",
        "version": "1.0.0",
        "description": "Complete API for building voice agents in Indian languages",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "config": "/config/*",
            "agents": "/agents/*",
            "llm": "/llm/*",
            "tts": "/tts/*",
            "voice_cloning": "/voice-cloning/*",
            "phone": "/phone/*"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
