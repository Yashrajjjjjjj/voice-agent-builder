# Complete Deployment Guide - Indian Voice Agent Builder

## Prerequisites
- Google Cloud account with billing enabled
- GitHub account
- Node.js 18+ installed locally
- Python 3.9+ installed locally
- gcloud CLI installed
- Git installed

## Step 1: Prepare API Keys

### Get Groq API Key (FREE)
1. Visit https://console.groq.com/keys
2. Click "Create API Key"
3. Copy and save the key
4. Store as environment variable: `GROQ_API_KEY`

### Get Replicate API Key (FREE tier)
1. Visit https://replicate.com/account/api-tokens
2. Copy your token
3. Store as environment variable: `REPLICATE_API_KEY`

### Set Up Firebase Project
1. Go to https://firebase.google.com/console
2. Create new project: "voice-agent-builder"
3. Enable Firestore Database
4. Enable Cloud Storage
5. Download service account JSON
6. Set `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`

## Step 2: Deploy Backend to Google Cloud Run

### Option A: Using gcloud CLI (Recommended)

```bash
# Clone repository
git clone https://github.com/Yashrajjjjjjj/voice-agent-builder
cd voice-agent-builder/backend

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy Docker image
gcloud run deploy voice-agent-backend \
  --source . \
  --platform managed \
  --region asia-south1 \
  --memory 2Gi \
  --timeout 3600 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=YOUR_GROQ_KEY,REPLICATE_API_KEY=YOUR_REPLICATE_KEY,GOOGLE_APPLICATION_CREDENTIALS=/workspace/creds.json

# After deployment, note the SERVICE_URL
# This will be used in frontend
```

### Option B: Using Docker locally first (for testing)

```bash
cd backend

# Build Docker image
docker build -t voice-agent-builder:latest .

# Run locally
docker run -p 8080:8080 \
  -e GROQ_API_KEY=YOUR_KEY \
  -e REPLICATE_API_KEY=YOUR_KEY \
  voice-agent-builder:latest

# Test health endpoint
curl http://localhost:8080/health
```

## Step 3: Deploy Frontend to Vercel

### Option A: Using Vercel CLI

```bash
# Navigate to frontend directory
cd frontend

# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel deploy --prod

# Add environment variable
# In Vercel dashboard: REACT_APP_BACKEND_URL=YOUR_CLOUD_RUN_URL
```

### Option B: Using GitHub Integration

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure root directory: `frontend`
5. Add environment variable: `REACT_APP_BACKEND_URL=YOUR_CLOUD_RUN_URL`
6. Deploy

## Step 4: Test Backend Endpoints

### Test Health Check
```bash
curl https://YOUR_CLOUD_RUN_URL/health
```

### Get Supported Languages
```bash
curl https://YOUR_CLOUD_RUN_URL/api/languages
```

### Create Agent
```bash
curl -X POST https://YOUR_CLOUD_RUN_URL/api/agents \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=TestAgent&job_role=Sales&system_instruction=You are a sales agent&primary_language=hi&user_id=user123"
```

### Upload Voice Sample
```bash
curl -X POST https://YOUR_CLOUD_RUN_URL/api/clone-voice \
  -F "user_id=user123" \
  -F "file=@voice_sample.wav"
```

## Step 5: Voice Cloning Setup

### Upload Your Voice Sample

1. Prepare 2-5 minute audio file of yourself speaking clearly
2. Format: WAV, MP3, or OGG
3. Quality: 16kHz or higher
4. Content: Natural speech in desired language

### Upload via Dashboard

1. Open frontend URL
2. Go to "Voice Library"
3. Click "Upload Voice Sample"
4. Select your audio file
5. System trains XTTS-v2 model on your voice
6. Voice available for all future agents

## Step 6: Create Your First Agent

### Via Dashboard

1. Click "Create New Agent"
2. Fill Agent Details:
   - Name: e.g., "Yash's Sales Agent"
   - Job Role: "Sales Representative"
   - System Instruction: "You are a friendly sales agent helping customers"
3. Select Models:
   - LLM: Groq (Mixtral-8x7b) - FREE
   - STT: Replicate Whisper - FREE
   - TTS: XTTS-v2 with voice cloning - FREE
   - Language: Hindi
4. Configure Voice:
   - Select "Your Voice" from voice library
5. Save Agent

## Step 7: Test Conversation

### Web Conversation Test

1. Click on agent in dashboard
2. Click "Test Chat"
3. Speak into microphone
4. Agent responds in your cloned voice
5. Verify accuracy and voice quality

## Step 8: Phone Integration Setup (Optional)

### Option A: Vapi Integration

1. Sign up at https://vapi.ai
2. Get Vapi API key
3. In backend, add Vapi integration for phone calls
4. Configure agent for phone calls
5. Make test call to your number

### Option B: Twilio Integration

1. Sign up at https://www.twilio.com
2. Get Twilio credentials (Account SID, Auth Token)
3. Configure webhook to backend
4. Test phone calls

### Option C: Exotel Integration (India)

1. Sign up at https://exotel.com
2. Get API credentials
3. Configure for India-specific phone numbers
4. Test calls with Exotel

## Step 9: First Test Call

### Make Test Call with Your Voice

```bash
# If using Vapi
curl -X POST https://YOUR_BACKEND/api/phone/call \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "YOUR_NUMBER", "agent_id": "YOUR_AGENT_ID", "provider": "vapi"}'
```

1. Agent calls your phone number
2. Listens to your message
3. Responds in your cloned voice
4. Performs configured tasks
5. Logs call data

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
gcloud run logs voice-agent-backend --limit 100

# Verify environment variables
echo $GROQ_API_KEY
echo $REPLICATE_API_KEY
```

### Voice Cloning Not Working
- Check Replicate API key is valid
- Verify audio file format (WAV, MP3, OGG)
- Check file duration (2-5 minutes)
- Ensure clear audio quality

### Frontend Not Connecting
- Verify REACT_APP_BACKEND_URL is correct
- Check CORS is enabled on backend
- Verify API endpoints are accessible

### Phone Calls Failing
- Check API credentials for provider (Vapi/Twilio/Exotel)
- Verify phone number format
- Check billing/credits
- Review provider logs

## Cost Tracking

### Expected Monthly Costs (Free Setup)
```
Backend (Cloud Run): FREE (900k CPU-seconds/month free tier)
Database (Firestore): FREE (50k reads/day free tier)
Storage (Cloud Storage): FREE (5GB free tier)
LLM (Groq): FREE
STT/TTS (Replicate): FREE tier available
Frontend (Vercel): FREE (hobby tier)
Total: $0/month for basic usage
```

### If Using Paid Models
```
OpenAI GPT-4: $0.03-0.06 per 1K tokens
ElevenLabs TTS: $5-99/month
Azure STT: $1.00/hour after free tier
Vapi Phone: $0.13-0.25/minute
Estimated: $20-100/month depending on usage
```

## Next Steps

1. ✅ Deploy backend to Cloud Run
2. ✅ Deploy frontend to Vercel
3. ✅ Upload your voice sample
4. ✅ Create first agent
5. ✅ Test conversation via web
6. ✅ Set up phone integration
7. ✅ Make first test call
8. ✅ Monitor costs and performance
9. ✅ Scale agents and team management
10. ✅ Add paid model integrations as needed

## Support

For issues:
1. Check logs: `gcloud run logs`
2. Review error messages in browser console
3. Test endpoints with curl/Postman
4. Check Firebase console for data
5. Contact support with error details
