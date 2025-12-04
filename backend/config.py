# Configuration module for Indian Voice Agent Builder
# Centralized configuration for all LLM, TTS, STT, and ASR providers

import os
from typing import Dict, List, Optional
from enum import Enum

# Supported Indian Languages
INDIAN_LANGUAGES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "gu": "Gujarati",
    "mr": "Marathi",
    "en-IN": "English (Indian)"
}

# LLM Provider Configuration
LLM_PROVIDERS = {
    "groq": {
        "name": "Groq",
        "tier": "free",
        "models": [
            "llama2-70b-4096",
            "mixtral-8x7b-32768",
            "llama2-13b-chat"
        ],
        "env_key": "GROQ_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "openai": {
        "name": "OpenAI",
        "tier": "premium",
        "models": ["gpt-4", "gpt-3.5-turbo"],
        "env_key": "OPENAI_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "anthropic": {
        "name": "Anthropic",
        "tier": "premium",
        "models": ["claude-3-opus", "claude-3-sonnet"],
        "env_key": "ANTHROPIC_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "gemini": {
        "name": "Google Gemini",
        "tier": "paid",
        "models": ["gemini-3", "gemini-3-pro"],
        "env_key": "GEMINI_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "mistral": {
        "name": "Mistral AI",
        "tier": "open-source",
        "models": ["mistral-7b", "mistral-13b", "mistral-nano"],
        "env_key": "MISTRAL_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "llama": {
        "name": "Llama",
        "tier": "open-source",
        "models": ["llama-2-7b", "llama-2-13b", "llama-2-70b"],
        "env_key": "LLAMA_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "deepseek": {
        "name": "DeepSeek",
        "tier": "open-source",
        "models": ["deepseek-7b", "deepseek-33b"],
        "env_key": "DEEPSEEK_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "sarvam": {
        "name": "Sarvam AI",
        "tier": "free",
        "models": ["sarvam-2b"],
        "env_key": "SARVAM_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "together": {
        "name": "Together AI",
        "tier": "free",
        "models": ["llama-2-70b-chat"],
        "env_key": "TOGETHER_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "grok": {
        "name": "Grok (XAI)",
        "tier": "premium",
        "models": ["grok-4", "grok-4.1"],
        "env_key": "GROK_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    }
}

# TTS Provider Configuration
TTS_PROVIDERS = {
    "replicate_xtts": {
        "name": "Replicate XTTS-v2",
        "tier": "free",
        "supports_voice_cloning": True,
        "env_key": "REPLICATE_API_TOKEN",
        "free_tier": True,
        "no_credit_card": True
    },
    "elevenlabs": {
        "name": "ElevenLabs",
        "tier": "premium",
        "supports_voice_cloning": True,
        "env_key": "ELEVENLABS_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "google_tts": {
        "name": "Google Cloud TTS",
        "tier": "free",
        "supports_voice_cloning": False,
        "env_key": "GOOGLE_APPLICATION_CREDENTIALS",
        "free_tier": True,
        "no_credit_card": True
    },
    "azure_tts": {
        "name": "Microsoft Azure TTS",
        "tier": "premium",
        "supports_voice_cloning": False,
        "env_key": "AZURE_TTS_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "cartesia": {
        "name": "Cartesia",
        "tier": "premium",
        "supports_voice_cloning": True,
        "env_key": "CARTESIA_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    }
}

# STT/ASR Provider Configuration
STT_PROVIDERS = {
    "google_stt": {
        "name": "Google Cloud Speech-to-Text",
        "tier": "free",
        "env_key": "GOOGLE_APPLICATION_CREDENTIALS",
        "free_tier": True,
        "no_credit_card": True
    },
    "openai_whisper": {
        "name": "OpenAI Whisper",
        "tier": "premium",
        "env_key": "OPENAI_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "azure_stt": {
        "name": "Microsoft Azure Speech",
        "tier": "premium",
        "env_key": "AZURE_SPEECH_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "groq_whisper": {
        "name": "Groq Whisper",
        "tier": "free",
        "env_key": "GROQ_API_KEY",
        "free_tier": True,
        "no_credit_card": True
    },
    "assemblyai": {
        "name": "AssemblyAI",
        "tier": "premium",
        "env_key": "ASSEMBLYAI_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    },
    "deepgram": {
        "name": "Deepgram Nova-2",
        "tier": "premium",
        "env_key": "DEEPGRAM_API_KEY",
        "free_tier": False,
        "no_credit_card": False
    }
}

# Fallback chains for providers
FALLBACK_CHAINS = {
    "llm": ["groq", "together", "mistral", "llama", "deepseek"],
    "tts": ["replicate_xtts", "google_tts", "elevenlabs", "cartesia", "azure_tts"],
    "stt": ["google_stt", "groq_whisper", "openai_whisper", "deepgram", "assemblyai", "azure_stt"]
}

# API Endpoints
API_ENDPOINTS = {
    "groq": "https://api.groq.com",
    "openai": "https://api.openai.com",
    "anthropic": "https://api.anthropic.com",
    "replicate": "https://api.replicate.com",
    "google": "https://www.googleapis.com",
    "elevenlabs": "https://api.elevenlabs.io"
}

# Language-specific model recommendations
LANGUAGE_MODEL_RECOMMENDATIONS = {
    "hi": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "ta": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "te": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "kn": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "ml": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "bn": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "gu": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "mr": {"llm": "groq", "tts": "google_tts", "stt": "google_stt"},
    "en-IN": {"llm": "groq", "tts": "replicate_xtts", "stt": "openai_whisper"}
}

def get_free_tier_providers():
    """Get all free tier providers without credit card requirement"""
    free_llms = [k for k, v in LLM_PROVIDERS.items() if v["free_tier"] and v["no_credit_card"]]
    free_tts = [k for k, v in TTS_PROVIDERS.items() if v["free_tier"] and v["no_credit_card"]]
    free_stt = [k for k, v in STT_PROVIDERS.items() if v["free_tier"] and v["no_credit_card"]]
    return {"llm": free_llms, "tts": free_tts, "stt": free_stt}

def validate_api_keys() -> Dict[str, bool]:
    """Validate that required API keys are available"""
    status = {}
    for provider, config in LLM_PROVIDERS.items():
        status[f"llm_{provider}"] = os.getenv(config["env_key"]) is not None
    for provider, config in TTS_PROVIDERS.items():
        status[f"tts_{provider}"] = os.getenv(config["env_key"]) is not None
    for provider, config in STT_PROVIDERS.items():
        status[f"stt_{provider}"] = os.getenv(config["env_key"]) is not None
    return status

if __name__ == "__main__":
    print("Free Tier Providers (No Credit Card):")
    free_providers = get_free_tier_providers()
    print(f"LLM: {free_providers['llm']}")
    print(f"TTS: {free_providers['tts']}")
    print(f"STT: {free_providers['stt']}")
