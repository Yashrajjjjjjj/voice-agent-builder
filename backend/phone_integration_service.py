# Phone Integration Service
# Integrate Vapi, Twilio, and Exotel for outbound calling capabilities

import asyncio
import logging
import os
from typing import Optional, Dict
import httpx

logger = logging.getLogger(__name__)

class PhoneIntegrationService:
    """Phone calling service supporting Vapi, Twilio, and Exotel"""
    
    def __init__(self):
        self.vapi_key = os.getenv("VAPI_API_KEY")
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
        self.exotel_api_key = os.getenv("EXOTEL_API_KEY")
        self.exotel_api_token = os.getenv("EXOTEL_API_TOKEN")

    async def make_call(
        self,
        phone_number: str,
        agent_id: str,
        provider: str = "vapi",
        message: Optional[str] = None
    ) -> dict:
        """Make outbound call using specified provider"""
        try:
            providers_to_try = [provider, "vapi", "twilio", "exotel"]
            
            for prov in providers_to_try:
                if prov == "vapi":
                    result = await self._call_vapi(phone_number, agent_id, message)
                elif prov == "twilio":
                    result = await self._call_twilio(phone_number, agent_id, message)
                elif prov == "exotel":
                    result = await self._call_exotel(phone_number, agent_id, message)
                else:
                    continue
                    
                if result and result.get("success"):
                    return result
            
            return {"success": False, "error": "All calling providers failed"}
        except Exception as e:
            logger.error(f"Phone call error: {e}")
            return {"success": False, "error": str(e)}

    async def _call_vapi(
        self,
        phone_number: str,
        agent_id: str,
        message: Optional[str]
    ) -> Optional[dict]:
        """Make call using Vapi (AI-native calling platform)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.vapi.ai/call/phone",
                    headers={"Authorization": f"Bearer {self.vapi_key}"},
                    json={
                        "phoneNumber": phone_number,
                        "assistantId": agent_id,
                        "messages": [
                            {
                                "role": "system",
                                "content": message or "You are a helpful voice agent"
                            }
                        ]
                    }
                )
                
                if response.status_code == 200:
                    call_data = response.json()
                    return {
                        "success": True,
                        "call_id": call_data.get("callId"),
                        "provider": "vapi",
                        "phone_number": phone_number,
                        "status": "initiated"
                    }
        except Exception as e:
            logger.error(f"Vapi call error: {e}")
        return None

    async def _call_twilio(
        self,
        phone_number: str,
        agent_id: str,
        message: Optional[str]
    ) -> Optional[dict]:
        """Make call using Twilio (widely supported, requires payment)"""
        try:
            async with httpx.AsyncClient() as client:
                auth = (self.twilio_account_sid, self.twilio_auth_token)
                response = await client.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Calls.json",
                    auth=auth,
                    data={
                        "From": self.twilio_phone,
                        "To": phone_number,
                        "Url": "https://handler.twilio.com/twiml/callback"
                    }
                )
                
                if response.status_code in [200, 201]:
                    call_data = response.json()
                    return {
                        "success": True,
                        "call_id": call_data.get("sid"),
                        "provider": "twilio",
                        "phone_number": phone_number,
                        "status": call_data.get("status")
                    }
        except Exception as e:
            logger.error(f"Twilio call error: {e}")
        return None

    async def _call_exotel(
        self,
        phone_number: str,
        agent_id: str,
        message: Optional[str]
    ) -> Optional[dict]:
        """Make call using Exotel (India-focused communication platform)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.exotel.com/v1/Accounts/{account_sid}/Calls/connect.json",
                    auth=(self.exotel_api_key, self.exotel_api_token),
                    data={
                        "From": os.getenv("EXOTEL_CALLER_ID"),
                        "To": phone_number,
                        "CallerId": os.getenv("EXOTEL_CALLER_ID")
                    }
                )
                
                if response.status_code in [200, 201]:
                    call_data = response.json()
                    return {
                        "success": True,
                        "call_id": call_data.get("Call", {}).get("Sid"),
                        "provider": "exotel",
                        "phone_number": phone_number,
                        "status": "initiated"
                    }
        except Exception as e:
            logger.error(f"Exotel call error: {e}")
        return None

    async def get_call_status(self, call_id: str, provider: str) -> dict:
        """Get status of ongoing call"""
        try:
            if provider == "vapi":
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"https://api.vapi.ai/call/{call_id}",
                        headers={"Authorization": f"Bearer {self.vapi_key}"}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "call_id": call_id,
                            "status": data.get("status"),
                            "duration": data.get("duration"),
                            "provider": "vapi"
                        }
            elif provider == "twilio":
                async with httpx.AsyncClient() as client:
                    auth = (self.twilio_account_sid, self.twilio_auth_token)
                    response = await client.get(
                        f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Calls/{call_id}.json",
                        auth=auth
                    )
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "call_id": call_id,
                            "status": data.get("status"),
                            "duration": data.get("duration"),
                            "provider": "twilio"
                        }
        except Exception as e:
            logger.error(f"Get call status error: {e}")
        
        return {"error": "Could not fetch call status"}

    async def hang_up_call(self, call_id: str, provider: str) -> dict:
        """Hang up / end call"""
        try:
            if provider == "vapi":
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"https://api.vapi.ai/call/{call_id}/end",
                        headers={"Authorization": f"Bearer {self.vapi_key}"}
                    )
                    return {
                        "success": response.status_code in [200, 204],
                        "call_id": call_id,
                        "provider": "vapi"
                    }
            elif provider == "twilio":
                async with httpx.AsyncClient() as client:
                    auth = (self.twilio_account_sid, self.twilio_auth_token)
                    response = await client.post(
                        f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Calls/{call_id}.json",
                        auth=auth,
                        data={"Status": "completed"}
                    )
                    return {
                        "success": response.status_code in [200, 204],
                        "call_id": call_id,
                        "provider": "twilio"
                    }
        except Exception as e:
            logger.error(f"Hang up error: {e}")
            return {"success": False, "error": str(e)}

    async def record_call(
        self,
        call_id: str,
        provider: str,
        enable_recording: bool = True
    ) -> dict:
        """Enable/disable call recording"""
        try:
            if provider == "twilio":
                async with httpx.AsyncClient() as client:
                    auth = (self.twilio_account_sid, self.twilio_auth_token)
                    response = await client.post(
                        f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Calls/{call_id}/Recordings.json",
                        auth=auth,
                        data={"RecordingStatusCallbackEvent": "completed"}
                    )
                    if response.status_code in [200, 201]:
                        return {
                            "success": True,
                            "call_id": call_id,
                            "recording_enabled": enable_recording
                        }
        except Exception as e:
            logger.error(f"Recording error: {e}")
        
        return {"success": False, "error": "Recording not available for this provider"}

    def get_supported_providers(self) -> list:
        """Get list of supported calling providers"""
        return ["vapi", "twilio", "exotel"]
