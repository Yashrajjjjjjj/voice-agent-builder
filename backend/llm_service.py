import os
import logging
import httpx
from typing import Optional, Dict
from enum import Enum

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    GROQ = "groq"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    MISTRAL = "mistral"
    GROK = "grok"
    DEEPSEEK = "deepseek"
    SARVAM = "sarvam"
    TOGETHER = "together"
    HUGGINGFACE = "huggingface"

class LLMService:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.grok_key = os.getenv("XAI_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.sarvam_key = os.getenv("SARVAM_API_KEY")
        self.together_key = os.getenv("TOGETHER_API_KEY")
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")
    
    async def generate(self, prompt: str, model: str = "groq-mixtral", language: str = "hi") -> Optional[str]:
        """Generate text with fallback logic"""
        try:
            if model.startswith("groq"):
                return await self._call_groq(prompt, language)
            elif model.startswith("openai"):
                return await self._call_openai(prompt, language)
            elif model.startswith("anthropic"):
                return await self._call_anthropic(prompt, language)
            elif model.startswith("gemini"):
                return await self._call_gemini(prompt, language)
            elif model.startswith("mistral"):
                return await self._call_mistral(prompt, language)
            elif model.startswith("grok"):
                return await self._call_grok(prompt, language)
            elif model.startswith("deepseek"):
                return await self._call_deepseek(prompt, language)
            elif model.startswith("sarvam"):
                return await self._call_sarvam(prompt, language)
            else:
                return await self._call_groq(prompt, language)
        except Exception as e:
            logger.error(f"Error with {model}: {e}, falling back to Groq")
            return await self._call_groq(prompt, language)
    
    async def _call_groq(self, prompt: str, language: str) -> Optional[str]:
        try:
            from groq import Groq
            client = Groq(api_key=self.groq_key)
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": f"Respond in {language}. Keep response concise."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return None
    
    async def _call_openai(self, prompt: str, language: str) -> Optional[str]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": f"Respond in {language}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return await self._call_groq(prompt, language)
    
    async def _call_anthropic(self, prompt: str, language: str) -> Optional[str]:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": f"Respond in {language}. {prompt}"}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            return await self._call_groq(prompt, language)
    
    async def _call_gemini(self, prompt: str, language: str) -> Optional[str]:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(f"Respond in {language}. {prompt}")
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return await self._call_groq(prompt, language)
    
    async def _call_mistral(self, prompt: str, language: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.mistral_key}"},
                    json={
                        "model": "mistral-large",
                        "messages": [{"role": "user", "content": f"Respond in {language}. {prompt}"}],
                        "max_tokens": 500
                    }
                )
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Mistral error: {e}")
            return await self._call_groq(prompt, language)
    
    async def _call_grok(self, prompt: str, language: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.grok_key}"},
                    json={
                        "model": "grok-4",
                        "messages": [{"role": "user", "content": f"Respond in {language}. {prompt}"}],
                        "max_tokens": 500
                    }
                )
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Grok error: {e}")
            return await self._call_groq(prompt, language)
    
    async def _call_deepseek(self, prompt: str, language: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.deepseek_key}"},
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": f"Respond in {language}. {prompt}"}],
                        "max_tokens": 500
                    }
                )
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Deepseek error: {e}")
            return await self._call_groq(prompt, language)
    
    async def _call_sarvam(self, prompt: str, language: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.sarvam.ai/chat",
                    headers={"Authorization": f"Bearer {self.sarvam_key}"},
                    json={
                        "model": "sarvam-1",
                        "messages": [{"role": "user", "content": f"Respond in {language}. {prompt}"}],
                        "max_tokens": 500
                    }
                )
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Sarvam error: {e}")
            return await self._call_groq(prompt, language)
    
    def get_available_models(self) -> list:
        return [
            "groq-mixtral",
            "groq-llama2",
            "openai-gpt4",
            "anthropic-claude3",
            "gemini-3",
            "mistral-large",
            "grok-4",
            "deepseek-v3",
            "sarvam-1"
        ]
