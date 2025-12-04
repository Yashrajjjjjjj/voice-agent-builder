# Indian Voice Agent Builder

🇮🇳 Create AI voice agents in **any Indian language** with your own cloned voice. 100% free using Google Cloud, Groq AI, and Replicate APIs.

## Features

✅ **Multi-Language Support** - Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, English (Indian accent)

✅ **Your Voice** - Clone your voice from a 2-5 minute audio sample

✅ **100% Free** - No paid APIs. Uses Groq (free), Replicate (free tier), Google Cloud (free tier)

✅ **Dashboard** - Create agents, manage voice library, configure LLM settings

✅ **Real-time Voice** - WebSocket-based real-time conversations

✅ **Cloud-Native** - Runs entirely on Google Cloud, Vercel frontend

## Tech Stack

**Backend:** FastAPI + Python
- Google Cloud (Firestore, Cloud Storage)
- Groq API (LLM - FREE)
- Replicate API (STT: Whisper, TTS: XTTS-v2 - FREE tier)
- Deploy: Cloud Run (900k free CPU-sec/month)

**Frontend:** React + TypeScript
- Deploy: Vercel (free)
- Real-time voice streaming (WebRTC)
- Voice cloning UI

**Database:** Firebase Firestore
- Free tier: 50k reads/day
- Agent configurations
- Voice library metadata
- Conversation logs

## Architecture

```
Client (React)
    ↓
Cloud Run (FastAPI)
    ├─ Groq API (LLM)
    ├─ Replicate (STT/TTS)
    └─ Firestore + Cloud Storage
```

## Getting Started

### Prerequisites

- Google Cloud account (300 free trial credits)
- Groq API key (free at groq.com)
- Replicate API key (free at replicate.com)
- Node.js 18+ (frontend)
- Python 3.11+ (backend)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your-groq-api-key"
export REPLICATE_API_KEY="your-replicate-api-key"

# Run locally
uvicorn main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

### 3. Deploy to Google Cloud

```bash
# Backend: Cloud Run
gcloud run deploy voice-agent \
  --source backend \
  --platform managed \
  --memory 2Gi \
  --timeout 3600 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your-key,REPLICATE_API_KEY=your-key

# Frontend: Vercel
cd frontend
vercel deploy
```

## Project Structure

```
voice-agent-builder/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Docker for Cloud Run
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceAgent.jsx     # Main agent interface
│   │   │   ├── VoiceCloner.jsx    # Voice cloning UI
│   │   │   ├── AgentBuilder.jsx   # Agent creation
│   │   │   └── VoiceLibrary.jsx   # Voice library
│   │   └── App.jsx
│   ├── package.json
│   └── vercel.json
├── README.md
└── .gitignore
```

## API Endpoints

### WebSocket

**`/ws/voice-agent/{agent_id}`** - Real-time voice conversation

```json
// Send audio
{"type": "audio", "audio": "base64_audio_data"}

// Receive transcription
{"type": "transcription", "text": "user said..."}

// Receive audio response
// Binary WebSocket frame with audio
```

### REST API

**`POST /api/agents`** - Create agent
```json
{
  "name": "Sales Agent",
  "job_role": "Sales Representative",
  "system_instruction": "Help with sales inquiries",
  "primary_language": "hi",
  "supported_languages": ["hi", "en"],
  "voice_clone_id": "user_id",
  "user_id": "user_id"
}
```

**`GET /api/agents?user_id=xxx`** - List agents

**`POST /api/clone-voice?user_id=xxx`** - Clone voice (upload audio file)

**`GET /api/voice-library?user_id=xxx`** - Get voice library

## Usage

### 1. Clone Your Voice

1. Record 2-5 minutes of your voice
2. Upload via dashboard
3. Your voice is ready for agents

### 2. Create an Agent

1. Go to Dashboard → Create Agent
2. Fill in: Name, Job Role, System Instruction
3. Select Language(s)
4. Choose your cloned voice
5. Click Create

### 3. Talk to Your Agent

1. Open agent
2. Click "Start Recording"
3. Speak in your selected language
4. Agent responds in your voice

## Environment Variables

```bash
# Required
GROQ_API_KEY=your_groq_api_key
REPLICATE_API_KEY=your_replicate_api_key

# Optional
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
API_URL=https://your-cloud-run-url.run.app
```

## Supported Languages

| Code | Language | Status |
|------|----------|--------|
| hi | हिंदी (Hindi) | ✅ |
| ta | தமிழ் (Tamil) | ✅ |
| te | తెలుగు (Telugu) | ✅ |
| kn | ಕನ್ನಡ (Kannada) | ✅ |
| ml | മലയാളം (Malayalam) | ✅ |
| bn | বাংলা (Bengali) | ✅ |
| gu | ગુજરાતી (Gujarati) | ✅ |
| mr | मराठी (Marathi) | ✅ |
| en | English (Indian) | ✅ |

## Cost Breakdown (100% Free)

| Service | Free Limit | Usage |
|---------|-----------|-------|
| Groq API | Unlimited | LLM |
| Replicate | Free tier | STT/TTS |
| Cloud Run | 900k CPU-sec/month | Backend |
| Firestore | 50k reads/day | Database |
| Cloud Storage | 5GB | Voice files |
| Vercel | Unlimited | Frontend |

## Troubleshooting

### Audio not transcribing?
- Ensure audio format is WAV/MP3
- Check Replicate API key
- Verify language code is correct

### Voice sounds robotic?
- Use 3-5 min of clear voice sample
- Try natural speech patterns
- Use Replicate XTTS-v2 model for better quality

### Rate limiting?
- Groq: Generous free tier
- Replicate: Check free tier limits
- Cloud Run: 900k CPU-seconds free

## Contributing

Contributions welcome! Please submit PRs for:
- New language support
- UI improvements
- Performance optimizations
- Bug fixes

## License

MIT License - feel free to use for commercial projects

## Support

For issues, open a GitHub issue or check documentation.

## Built with ❤️ by Yashraj

Building AI agents for everyone. 🚀
