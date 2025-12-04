# API Key Setup Guide for Indian Voice Agent Builder

## Overview
This guide provides step-by-step instructions to obtain FREE API keys for all services used in the Indian Voice Agent Builder. **NO credit card is required** for any of these services.

---

## 1. LLM Providers (Language Models)

### Groq - FREE (Recommended for Getting Started)
- **URL**: https://console.groq.com/keys
- **Steps**:
  1. Go to https://console.groq.com/
  2. Click "Sign Up" or "Log In"
  3. Create account (no credit card needed)
  4. Navigate to "API Keys" section
  5. Click "Create New API Key"
  6. Copy the key and add to `.env` as `GROQ_API_KEY`
- **Rate Limit**: 30 requests/minute (FREE)
- **Model**: `mixtral-8x7b-32768`

### Google Gemini - FREE
- **URL**: https://makersuite.google.com/app/apikey
- **Steps**:
  1. Go to Google AI Studio
  2. Click "Create API Key"
  3. Copy and save in `.env` as `GOOGLE_GEMINI_API_KEY`
- **Rate Limit**: 60 requests/minute
- **No credit card required**

### Together AI - FREE Tier
- **URL**: https://api.together.xyz/
- **Steps**:
  1. Sign up at Together AI
  2. Go to API keys section
  3. Generate new API key
- **Includes many open-source models**

---

## 2. Text-to-Speech (TTS) Providers

### Google Cloud Text-to-Speech - FREE
- **URL**: https://console.cloud.google.com/
- **Steps**:
  1. Create a Google Cloud Project
  2. Enable "Text-to-Speech API"
  3. Create a service account
  4. Download JSON credentials
  5. Save as `google-credentials.json`
- **Free Tier**: 1 million characters/month

### ElevenLabs - FREE Tier
- **URL**: https://elevenlabs.io/
- **Steps**:
  1. Sign up (no credit card)
  2. Go to "API Keys"
  3. Copy your API key
  4. Add to `.env` as `ELEVENLABS_API_KEY`
- **Free Tier**: 10,000 characters/month
- **Includes Indian language support**

### Replicate - FREE Credits
- **URL**: https://replicate.com/account/api-tokens
- **Steps**:
  1. Create account
  2. Go to API Tokens
  3. Create new token
- **Excellent for voice cloning**
- **Free credits included**

---

## 3. Speech-to-Text (STT) Providers

### Google Cloud Speech-to-Text - FREE
- Uses same credentials as Google TTS above
- **Free Tier**: 60 minutes/month
- **Setup**: Already configured if you set up Google TTS

### AssemblyAI - FREE Trial
- **URL**: https://www.assemblyai.com/
- **Steps**:
  1. Sign up (no credit card)
  2. Copy API key from dashboard
  3. Add to `.env` as `ASSEMBLYAI_API_KEY`
- **Free**: 100 concurrent requests

### Deepgram - FREE Tier
- **URL**: https://console.deepgram.com/
- **Steps**:
  1. Create free account
  2. Generate API key
  3. Add to `.env` as `DEEPGRAM_API_KEY`

---

## 4. Phone Integration

### Twilio - Free Trial
- **URL**: https://console.twilio.com/
- **Steps**:
  1. Sign up (trial credits provided)
  2. Get trial phone number
  3. Copy Account SID and Auth Token
  4. Add all to `.env`
- **Cost**: $0.01-0.05 per minute for calls

### Exotel - Indian Alternative
- **URL**: https://exotel.com/
- **Steps**:
  1. Sign up with Indian phone number
  2. Complete verification
  3. Get API credentials
  4. Add to `.env`
- **Recommended for India-based deployments**

---

## 5. Authentication (Google OAuth)

### Google OAuth - FREE
- **URL**: https://console.cloud.google.com/
- **Steps**:
  1. Go to Google Cloud Console
  2. Create OAuth 2.0 credentials
  3. Set redirect URI: `http://localhost:8000/auth/google/callback`
  4. Copy Client ID and Secret
  5. Add to `.env`

---

## Setup Checklist

### Minimum Required (to get started immediately):
- [ ] Groq API Key (LLM)
- [ ] Google Gemini API Key (Alternative LLM)
- [ ] Google Cloud Text-to-Speech credentials (TTS)
- [ ] Google Cloud Speech-to-Text (STT - uses same credentials)
- [ ] Replicate API Token (Voice Cloning)

### Optional (for extended functionality):
- [ ] ElevenLabs API Key (Premium TTS)
- [ ] Twilio Credentials (Phone calling)
- [ ] Exotel Credentials (Indian phone integration)
- [ ] AssemblyAI API Key (Advanced STT)
- [ ] Deepgram API Key (Advanced STT)

---

## How to Add Keys to .env

1. Copy `.env.example` to `.env`
2. Open `.env` in your text editor
3. Replace `your_*_api_key_here` with actual keys
4. Never commit `.env` to git

### Example .env content:
```
GROQ_API_KEY=gsk_your_actual_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
```

---

## Common Issues

### "API Key not found"
- Check if key is in `.env` file
- Verify .env file is in the backend directory
- Ensure no extra spaces or quotes around key

### "Rate limit exceeded"
- Switch to a different provider from fallback list
- Wait for rate limit reset (usually 1 hour)
- Upgrade to paid tier if needed

### "Credit card required"
- This should NOT happen
- Use providers listed as FREE
- Check alternative providers

---

## Production Deployment

For Railway/Vercel deployment:
1. Add all `.env` variables to platform's "Environment Variables" section
2. Do NOT commit `.env` file
3. Use strong JWT_SECRET_KEY in production
4. Enable HTTPS for all API calls

---

## Support

For issues:
1. Check official API documentation
2. Verify API key is correct
3. Check rate limits
4. Review application logs
5. Create GitHub issue with details

**Remember**: Start with Groq and Google services (both FREE, no credit card needed)!
