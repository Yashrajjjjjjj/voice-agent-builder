import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.replicate_key = os.getenv("REPLICATE_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.google_key = os.getenv("GOOGLE_CLOUD_KEY")
        self.azure_key = os.getenv("AZURE_TTS_KEY")
        self.cartesia_key = os.getenv("CARTESIA_API_KEY")
    
    async def synthesize(self, text: str, language: str = "hi", model: str = "replicate-xtts") -> Optional[str]:
        """Synthesize speech from text with fallback"""
        try:
            if model.startswith("replicate"):
                return await self._call_replicate(text, language)
            elif model.startswith("elevenlabs"):
                return await self._call_elevenlabs(text, language)
            elif model.startswith("google"):
                return await self._call_google_tts(text, language)
            elif model.startswith("azure"):
                return await self._call_azure_tts(text, language)
            elif model.startswith("cartesia"):
                return await self._call_cartesia(text, language)
            else:
                return await self._call_replicate(text, language)
        except Exception as e:
            logger.error(f"Error with {model}: {e}, falling back to Replicate")
            return await self._call_replicate(text, language)
    
    async def _call_replicate(self, text: str, language: str) -> Optional[str]:
        """Call Replicate XTTS-v2 for voice cloning"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.replicate.com/v1/predictions",
                    headers={"Authorization": f"Bearer {self.replicate_key}"},
                    json={
                        "version": "cjwbw/xtts_v2",
                        "input": {
                            "text": text,
                            "language": language.split("-")[0]
                        }
                    }
                )
                data = response.json()
                prediction_id = data["id"]
                # Poll for result
                while True:
                    result = await client.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers={"Authorization": f"Bearer {self.replicate_key}"}
                    )
                    result_data = result.json()
                    if result_data["status"] == "succeeded":
                        return result_data["output"]
                    elif result_data["status"] == "failed":
                        raise Exception("Prediction failed")
        except Exception as e:
            logger.error(f"Replicate error: {e}")
            return None
    
    async def _call_elevenlabs(self, text: str, language: str) -> Optional[str]:
        """Call ElevenLabs for premium TTS"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
                    headers={"xi-api-key": self.elevenlabs_key},
                    json={
                        "text": text,
                        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
                    }
                )
                return response.content.decode("base64")
        except Exception as e:
            logger.error(f"ElevenLabs error: {e}")
            return await self._call_replicate(text, language)
    
    async def _call_google_tts(self, text: str, language: str) -> Optional[str]:
        """Call Google Cloud TTS"""
        try:
            from google.cloud import texttospeech
            client = texttospeech.TextToSpeechClient()
            input_text = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                name=f"{language}-Neural2-C"
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = client.synthesize_speech(
                input=input_text, voice=voice, audio_config=audio_config
            )
            return response.audio_content
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return await self._call_replicate(text, language)
    
    async def _call_azure_tts(self, text: str, language: str) -> Optional[str]:
        """Call Microsoft Azure TTS"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{os.getenv('AZURE_REGION')}.tts.speech.microsoft.com/cognitiveservices/v1",
                    headers={
                        "Ocp-Apim-Subscription-Key": self.azure_key,
                        "Content-Type": "application/ssml+xml"
                    },
                    content=f'<speak version="1.0" xml:lang="{language}"><voice>{text}</voice></speak>'
                )
                return response.content
        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            return await self._call_replicate(text, language)
    
    async def _call_cartesia(self, text: str, language: str) -> Optional[str]:
        """Call Cartesia AI TTS"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.cartesia.ai/v1/text-to-speech/transform",
                    headers={"Authorization": f"Bearer {self.cartesia_key}"},
                    json={
                        "text": text,
                        "language": language,
                        "voice_id": "presets_speaking"
                    }
                )
                return response.content
        except Exception as e:
            logger.error(f"Cartesia error: {e}")
            return await self._call_replicate(text, language)
    
    def get_available_models(self) -> list:
        return [
            "replicate-xtts",
            "elevenlabs-premium",
            "google-tts",
            "azure-tts",
            "cartesia-tts"
        ]
