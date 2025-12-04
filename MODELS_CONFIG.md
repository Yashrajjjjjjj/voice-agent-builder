MODELS_CONFIG.md# Voice Agent Builder - Comprehensive Model Configuration

## Architecture: FREE + PAID Models
User selects from comprehensive model options across LLM, STT, TTS, and ASR categories.

---

## 1. LARGE LANGUAGE MODELS (LLM) - FREE & PAID

### FREE & OPEN-SOURCE LLMs (Replicate/Ollama)
```
**Mistral Series**
  - mistral-7b          (Fast, lightweight, free)
  - mistral-7b-instruct (Instruction-tuned)
  - mistral-medium      (Better reasoning)
  - mixtral-8x7b        (Top FREE choice)
  - mixtral-8x22b       (Ultra-powerful FREE)

**Llama Series**
  - llama-2-7b          (Meta's open source)
  - llama-2-13b         (Balanced)
  - llama-2-70b         (Most powerful)
  - llama-3-8b          (Latest, faster)
  - llama-3-70b         (Latest, best)

**DeepSeek Series**
  - deepseek-7b         (Cost-effective)
  - deepseek-33b        (Advanced reasoning)
  - deepseek-coder-33b  (Code generation)

**Other Open-Source**
  - Qwen-7b/14b/72b     (Alibaba's models)
  - Falcon-7b/40b/180b  (TII's models)
  - Phi-2               (Small but powerful)
  - Neural-Chat-7b      (Conversation optimized)
```

### PAID Commercial LLMs
```
**OpenAI**
  - gpt-4-turbo         ($0.01/$0.03 per 1K tokens)
  - gpt-4               ($0.03/$0.06)
  - gpt-3.5-turbo       ($0.0005/$0.0015)

**Anthropic Claude**
  - claude-3-opus       ($0.015/$0.075 per 1K)
  - claude-3-sonnet     ($0.003/$0.015)
  - claude-3-haiku      ($0.00025/$0.00125)

**Google**
  - gemini-pro          (Free tier available)
  - palm-2              (Older, cheaper)

**XAI**
  - Grok-1              (Latest, experimental)
```

---

## 2. SPEECH-TO-TEXT (STT) - FREE & PAID

### FREE & OPEN-SOURCE STT
```
**Silero (100% FREE, Offline)**
  - silero-stt-en       (English, super fast)
  - silero-stt-multi    (95+ languages including all Indian languages)
  - Model size: 48MB    (Can run locally!)

**OpenAI Whisper (FREE via Replicate)**
  - whisper-tiny        (39M params, fastest)
  - whisper-base        (74M params, balanced)
  - whisper-small       (244M params, accurate)
  - whisper-medium      (769M params, very accurate)
  - whisper-large       (1550M params, best)
  - Supports: 97+ languages

**Google Cloud Speech-to-Text (FREE tier)**
  - Free: 60 minutes/month
  - Accurate multi-language support

**Mozilla DeepSpeech (Offline)**
  - English only, but 100% open-source
  - Can run completely locally
```

### PAID STT Services
```
**OpenAI Whisper API**
  - $0.02 per minute

**Google Cloud STT**
  - $0.024 per 15 seconds after free tier

**Azure Speech-to-Text**
  - $1.00 per hour after free tier

**AWS Transcribe**
  - $0.0001 per second
```

---

## 3. TEXT-TO-SPEECH (TTS) - FREE & PAID + VOICE CLONING

### FREE & OPEN-SOURCE TTS with VOICE CLONING
```
**XTTS-v2 by Coqui (RECOMMENDED FOR VOICE CLONING)**
  - FREE, open-source
  - Supports: 20+ languages (including all Indian languages)
  - Voice cloning: Upload 2-5 min audio sample → Clone voice
  - Latency: ~2-3 seconds per response
  - Quality: Near human-like with user's cloned voice
  - Provider: Replicate (free tier available)

  **Indian Language Support in XTTS-v2:**
    - Hindi, Tamil, Telugu, Kannada, Malayalam
    - Bengali, Gujarati, Marathi, English (Indian accent)

**Silero TTS (100% FREE, Offline)**
  - 100+ language voices
  - Can run completely locally
  - Fast inference
  - No voice cloning (use as alternative)

**Glow-TTS (Offline, 100% FREE)**
  - Fast, natural speech
  - Can run locally
  - Multi-language support
  - Open-source

**MeloTTS (100% FREE)**
  - Supports 13+ languages
  - Can run locally
  - Indian language support
```

### PAID TTS with Premium Voice Cloning
```
**ElevenLabs (PREMIUM - BEST VOICE CLONING)**
  - Pricing: $5-99/month (11K-1M characters)
  - Voice cloning: Upload sample → Clone instantly
  - Premium voices: 30+ languages
  - Latency: <200ms
  - Quality: Indistinguishable from real voice

**Microsoft Azure TTS**
  - $4/month (free tier: 5M characters/month)
  - Voice cloning available
  - 450+ voices in 140+ languages

**Google Cloud TTS**
  - Free tier: 1M characters/month
  - Paid: $16 per 1M characters
  - 220+ voices in 40+ languages
  - Neural voices available

**Cartesia**
  - Real-time voice cloning
  - Sub-100ms latency
  - Custom voice training

**Vapi TTS Integration**
  - Uses multiple TTS providers
  - Automatic fallback
  - Premium voice quality
```

---

## 4. AUTOMATIC SPEECH RECOGNITION (ASR) - FREE & PAID

### FREE & OPEN-SOURCE ASR
```
**Silero VAD (Voice Activity Detection)**
  - 100% FREE, offline
  - Detect speech vs silence
  - Multiple language support

**Wav2Letter++**
  - 100% open-source
  - Can run offline
  - High accuracy
```

### PAID ASR Services
```
**Google Cloud Speech-to-Text**
  - $0.024 per 15 seconds (after free tier)

**Azure Speech Services**
  - $1.00 per hour

**AWS Transcribe**
  - $0.0001 per second
```

---

## 5. PHONE INTEGRATION PROVIDERS

### Supported Phone APIs
```
**Vapi (RECOMMENDED FOR VOICE AGENTS)**
  - Automatic phone calls
  - Call handling
  - Voicemail detection
  - Pricing: $0.13-0.25/minute
  - Best for: Outbound voice agent calls

**Twilio**
  - Make & receive calls
  - Pricing: $0.0085/minute inbound, $0.02/minute outbound
  - SMS integration
  - Flexible webhooks

**Exotel (INDIA-FOCUSED)**
  - Indian phone numbers
  - Pricing: ₹0.30-1.50/minute
  - IVR support
  - SMS integration
  - Best for: India-based users

**Vonage/Nexmo**
  - Global coverage
  - Advanced call control
  - Recording capabilities
```

---

## 6. VOICE CLONING PIPELINE (USER'S OWN VOICE)

### Step 1: Upload Voice Sample
```
User uploads 2-5 minute audio sample of their voice
- Supported formats: WAV, MP3, OGG
- Quality: 16kHz or higher
- Content: Natural speech, clear pronunciation
```

### Step 2: Train on XTTS-v2
```
1. Backend processes audio sample
2. Creates voice embeddings using XTTS-v2
3. Stores voice profile in Cloud Storage
4. Associates with user account
```

### Step 3: Use Cloned Voice for TTS
```
1. When agent responds, use user's cloned voice
2. Text → User's Cloned Voice (via XTTS-v2)
3. Audio played in real-time conversation
4. Voice quality: Near-identical to user's actual voice
```

### Step 4: Voice Library Management
```
- Store all cloned voices in "Voice Library"
- Team members can access team voices
- Delete/archive old voices
- Create new clones anytime
- Export voice profiles
```

---

## 7. DASHBOARD STRUCTURE (Like Vapi)

### Agent Builder Workflow
```
1. **Create Agent**
   - Agent Name
   - Job Role (e.g., "Sales Rep", "Customer Support")
   - System Instruction (with AI Prompt Enhancer)

2. **Select Models**
   - LLM: Choose from 15+ FREE or PAID options
   - STT: Choose from 5+ FREE or PAID options
   - TTS: Choose from 8+ FREE or PAID options (with cloning)
   - ASR: Choose from 3+ options

3. **Configure Voice**
   - Use default voice
   - OR upload your voice sample (2-5 min)
   - OR select from voice library
   - Preview voice with test phrase

4. **Test & Deploy**
   - Test conversation via web/phone
   - Configure phone (Vapi/Twilio/Exotel)
   - Deploy agent
   - Make test call

5. **Monitor & Manage**
   - View call logs
   - Monitor costs
   - Analytics dashboard
   - Voice library management
```

---

## 8. COST STRUCTURE

### 100% FREE Setup (Using Open-Source)
```
LLM:  Groq API (completely FREE)
STT:  Silero or Whisper free tier
TTS:  XTTS-v2 (free) + user's cloned voice
ASR:  Silero VAD (free)
Phone: Twilio free trial (limited)
Total: $0/month for core functionality
```

### Minimal Cost Setup ($1-5/month)
```
LLM:  Groq (free)
STT:  Google Cloud free tier
TTS:  XTTS-v2 + voice cloning
Phone: Twilio ($0.0085-0.02/min)
Estimate: $1-5/month for light usage
```

### Premium Setup ($20-100/month)
```
LLM:  GPT-4 Turbo
STT:  OpenAI Whisper API
TTS:  ElevenLabs + voice cloning
Phone: Vapi or Twilio pro
Estimate: $50-100/month for heavy usage
```

---

## 9. DEPLOYMENT STATUS

✅ **COMPLETED:**
- Backend with FastAPI
- WebSocket real-time conversations
- Firebase Firestore database
- Voice cloning pipeline (XTTS-v2)
- All Indian language support
- Groq LLM integration
- Replicate STT/TTS integration

🔄 **IN PROGRESS:**
- React dashboard with model selection
- Voice cloning UI
- Phone integration setup

📋 **TODO:**
- Add paid model integrations (ElevenLabs, OpenAI, etc.)
- Vapi/Twilio/Exotel phone call system
- Production testing
- Voice cloning quality improvements

---

## 10. QUICK START FOR VOICE CLONING

1. Prepare your voice sample (2-5 minutes)
2. Upload via dashboard
3. System trains voice profile
4. Select "Your Voice" when creating agent
5. Conversations use your cloned voice
6. Share voice with team
7. Make test calls with your voice

---

## Next: Phone Call Testing

Once deployment is complete, we will:
1. Set up Vapi/Twilio credentials
2. Train on your voice sample
3. Make test call to your phone number
4. Verify agent responds in your voice
5. Test with Exotel (India)
6. Full production deployment
