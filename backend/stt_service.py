import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        self.google_key = os.getenv("GOOGLE_CLOUD_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.azure_key = os.getenv("AZURE_STT_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.deepgram_key = os.getenv("DEEPGRAM_API_KEY")
    
    async def transcribe(self, audio_path: str, language: str = "hi", model: str = "google-stt") -> Optional[str]:
        """Transcribe audio to text with fallback"""
        try:
            if model.startswith("google"):
                return await self._call_google_stt(audio_path, language)
            elif model.startswith("openai"):
                return await self._call_openai_whisper(audio_path, language)
            elif model.startswith("azure"):
                return await self._call_azure_stt(audio_path, language)
            elif model.startswith("groq"):
                return await self._call_groq_whisper(audio_path, language)
            elif model.startswith("assemblyai"):
                return await self._call_assemblyai(audio_path, language)
            elif model.startswith("deepgram"):
                return await self._call_deepgram(audio_path, language)
            else:
                return await self._call_google_stt(audio_path, language)
        except Exception as e:
            logger.error(f"Error with {model}: {e}, falling back to Google")
            return await self._call_google_stt(audio_path, language)
    
    async def _call_google_stt(self, audio_path: str, language: str) -> Optional[str]:
        """Call Google Cloud STT"""
        try:
            from google.cloud import speech_v1
            client = speech_v1.SpeechClient()
            with open(audio_path, "rb") as audio_file:
                content = audio_file.read()
            audio = speech_v1.RecognitionAudio(content=content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=16000,
                language_code=language
            )
            response = client.recognize(config=config, audio=audio)
            return response.results[0].alternatives[0].transcript if response.results else ""
        except Exception as e:
            logger.error(f"Google STT error: {e}")
            return None
    
    async def _call_openai_whisper(self, audio_path: str, language: str) -> Optional[str]:
        """Call OpenAI Whisper API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language.split("-")[0]
                )
            return transcript.text
        except Exception as e:
            logger.error(f"OpenAI Whisper error: {e}")
            return await self._call_google_stt(audio_path, language)
    
    async def _call_azure_stt(self, audio_path: str, language: str) -> Optional[str]:
        """Call Microsoft Azure Speech-to-Text"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_key,
                region=os.getenv("AZURE_REGION")
            )
            speech_config.speech_recognition_language = language
            audio_input = speechsdk.AudioConfig(filename=audio_path)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_input
            )
            result = recognizer.recognize_once()
            return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else ""
        except Exception as e:
            logger.error(f"Azure STT error: {e}")
            return await self._call_google_stt(audio_path, language)
    
    async def _call_groq_whisper(self, audio_path: str, language: str) -> Optional[str]:
        """Call Groq Whisper API"""
        try:
            from groq import Groq
            client = Groq(api_key=self.groq_key)
            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3",
                    language=language.split("-")[0]
                )
            return transcript.text
        except Exception as e:
            logger.error(f"Groq Whisper error: {e}")
            return await self._call_google_stt(audio_path, language)
    
    async def _call_assemblyai(self, audio_path: str, language: str) -> Optional[str]:
        """Call AssemblyAI for speech recognition"""
        try:
            async with httpx.AsyncClient() as client:
                with open(audio_path, "rb") as audio_file:
                    response = await client.post(
                        "https://api.assemblyai.com/v2/upload",
                        headers={"Authorization": self.assemblyai_key},
                        content=audio_file.read()
                    )
                    upload_url = response.json()["upload_url"]
                response = await client.post(
                    "https://api.assemblyai.com/v2/transcript",
                    headers={"Authorization": self.assemblyai_key},
                    json={
                        "audio_url": upload_url,
                        "language_code": language.split("-")[0]
                    }
                )
                transcript_id = response.json()["id"]
                # Poll for result
                while True:
                    result = await client.get(
                        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                        headers={"Authorization": self.assemblyai_key}
                    )
                    result_data = result.json()
                    if result_data["status"] == "completed":
                        return result_data["text"]
                    elif result_data["status"] == "error":
                        raise Exception("Transcription failed")
        except Exception as e:
            logger.error(f"AssemblyAI error: {e}")
            return await self._call_google_stt(audio_path, language)
    
    async def _call_deepgram(self, audio_path: str, language: str) -> Optional[str]:
        """Call Deepgram for speech recognition"""
        try:
            async with httpx.AsyncClient() as client:
                with open(audio_path, "rb") as audio_file:
                    response = await client.post(
                        "https://api.deepgram.com/v1/listen",
                        headers={"Authorization": f"Token {self.deepgram_key}"},
                        content=audio_file.read(),
                        params={
                            "model": "nova-2",
                            "language": language.split("-")[0]
                        }
                    )
                    return response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
        except Exception as e:
            logger.error(f"Deepgram error: {e}")
            return await self._call_google_stt(audio_path, language)
    
    def get_available_models(self) -> list:
        return [
            "google-stt",
            "openai-whisper",
            "azure-stt",
            "groq-whisper",
            "assemblyai-stt",
            "deepgram-stt"
        ]
