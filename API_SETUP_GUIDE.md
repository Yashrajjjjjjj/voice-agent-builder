# 🔐 SECURE API SETUP GUIDE - Step-by-Step for Your Account

## ⚠️ SECURITY FIRST - YOU Control Your Keys

You will log in to each service directly. I am providing step-by-step instructions ONLY.
**Your credentials NEVER pass through any intermediary - they stay 100% secure with you.**

---

## 1️⃣ GROQ API KEY (Completely FREE LLM)

### Step 1: Visit Groq Console
- Open: https://console.groq.com/keys
- You'll need to create/login to your account

### Step 2: Create API Key
1. Click **"Create API Key"** button
2. Give it a name like: "voice-agent-builder"
3. Click **Create**
4. **IMPORTANT: Copy the key immediately** (it won't show again)

### Step 3: Save Your Key
```
Your GROQ_API_KEY = [paste your key here]
```

### Step 4: Add to Your System
```bash
# Linux/Mac - Add to ~/.bashrc or ~/.zshrc
export GROQ_API_KEY="your_key_here"

# Windows - Set environment variable
set GROQ_API_KEY=your_key_here

# Or create .env file in your project
GROQ_API_KEY=your_key_here
```

---

## 2️⃣ REPLICATE API TOKEN (FREE Tier STT/TTS)

### Step 1: Visit Replicate
- Open: https://replicate.com/signin
- Sign up with Gmail (your yashrajemailme@gmail.com)
- Verify email

### Step 2: Get API Token
1. Once logged in, go to: https://replicate.com/account/api-tokens
2. You'll see your API token listed
3. **Copy it** (looks like: `r8_...`)

### Step 3: Save Your Token
```
Your REPLICATE_API_KEY = [paste your token here]
```

### Step 4: Add to Your System
```bash
# Linux/Mac
export REPLICATE_API_KEY="your_token_here"

# Windows
set REPLICATE_API_KEY=your_token_here

# .env file
REPLICATE_API_KEY=your_token_here
```

---

## 3️⃣ FIREBASE PROJECT SETUP (FREE Firestore & Cloud Storage)

### Step 1: Create Firebase Project
- Open: https://firebase.google.com/console
- Click **"Create project"** (or use existing: yash-first-project-in-data)
- If creating new: Name it "voice-agent-builder"
- Accept terms, click **"Create project"**

### Step 2: Enable Firestore Database
1. In Firebase console, click **"Firestore Database"**
2. Click **"Create database"**
3. Select: **"Start in production mode"**
4. Region: **"asia-south1"** (closest to India)
5. Click **"Create"**

### Step 3: Enable Cloud Storage
1. In Firebase console, click **"Storage"**
2. Click **"Get Started"**
3. Accept default settings
4. Click **"Done"**

### Step 4: Get Service Account Credentials
1. Go to **"Project Settings"** (gear icon, top-left)
2. Click **"Service Accounts"** tab
3. Select **"Python"** from dropdown
4. Click **"Generate new private key"**
5. This downloads a JSON file
6. **KEEP THIS FILE SAFE** - it contains credentials

### Step 5: Set Environment Variable
```bash
# Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/downloaded-credentials.json"

# Windows
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\downloaded-credentials.json

# In .env file
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## 4️⃣ VAPI API KEY (Phone Integration - Optional)

### Step 1: Sign Up for Vapi
- Open: https://vapi.ai
- Click **"Sign Up"** or **"Get Started"**
- Use your Gmail: yashrajemailme@gmail.com

### Step 2: Get API Key
1. Once logged in, go to **"API Keys"** or **"Settings"**
2. Click **"Create API Key"**
3. Copy the key

### Step 3: Save Your Key
```
Your VAPI_API_KEY = [paste your key here]
```

---

## 5️⃣ TWILIO API KEYS (Phone Integration - Alternative)

### Step 1: Sign Up for Twilio
- Open: https://www.twilio.com/try-twilio
- Click **"Start Free"**
- Use your Gmail

### Step 2: Get Credentials
1. In Twilio console, find: **Account SID** and **Auth Token**
2. Copy both

### Step 3: Save Your Keys
```
TWILIO_ACCOUNT_SID = [paste here]
TWILIO_AUTH_TOKEN = [paste here]
```

---

## 6️⃣ EXOTEL API KEYS (India-Specific Phone)

### Step 1: Sign Up for Exotel
- Open: https://exotel.com
- Click **"Start Free"** or **"Sign Up"**
- Fill in details for India

### Step 2: Get API Keys
1. Go to **"Settings"** → **"API"**
2. Find your: **API Key** and **API Token**
3. Also get your **SID** (Exotel SID)

### Step 3: Save Your Keys
```
EXOTEL_API_KEY = [paste here]
EXOTEL_API_TOKEN = [paste here]
EXOTEL_SID = [paste here]
```

---

## 7️⃣ OPTIONAL: ELEVENLABS TTS (Premium Voice)

### Step 1: Sign Up
- Open: https://elevenlabs.io
- Click **"Sign Up"**
- Use your Gmail

### Step 2: Get API Key
1. Go to **"API"** or **"Account"**
2. Find your **API Key**
3. Copy it

### Step 3: Save Your Key
```
ELEVENLABS_API_KEY = [paste here]
```

---

## 8️⃣ CREATE .env FILE

Create a `.env` file in your project root with ALL keys:

```bash
# .env file (NEVER commit this to GitHub!)

# FREE APIs
GROQ_API_KEY=your_groq_key_here
REPLICATE_API_KEY=your_replicate_token_here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/firebase-credentials.json

# Phone APIs (Choose one or all)
VAPI_API_KEY=your_vapi_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid_here
TWILIO_AUTH_TOKEN=your_twilio_token_here
EXOTEL_API_KEY=your_exotel_key_here
EXOTEL_API_TOKEN=your_exotel_token_here
EXOTEL_SID=your_exotel_sid_here

# Premium TTS (Optional)
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

---

## 9️⃣ VERIFY YOUR SETUP

Test each API key:

```bash
# Test Groq
python -c "from groq import Groq; print('Groq OK' if Groq().chat.completions.create(model='mixtral-8x7b-32768', messages=[{'role':'user', 'content':'hi'}]) else 'Failed')"

# Test Replicate
curl -H "Authorization: Token $REPLICATE_API_KEY" https://api.replicate.com/v1/predictions

# Test Firebase
python -c "import firebase_admin; firebase_admin.initialize_app(); print('Firebase OK')"
```

---

## 🔒 SECURITY BEST PRACTICES

✅ **DO:**
- Keep .env file in .gitignore (never commit to GitHub)
- Rotate keys regularly (once per month)
- Use different keys for dev/prod
- Enable 2FA on all accounts
- Keep credentials file safe

❌ **DON'T:**
- Share API keys with anyone
- Post keys in code comments
- Commit .env to GitHub
- Use the same key for different projects
- Hardcode keys in source code

---

## ✅ ALL SET!

Once you have all keys and created the .env file, you're ready to:
1. Deploy backend to Google Cloud Run
2. Deploy frontend to Vercel
3. Upload your voice sample
4. Make your first test call

Follow DEPLOYMENT_GUIDE.md for next steps!
