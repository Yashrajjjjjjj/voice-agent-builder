# Agent Management Service
# Manage voice agents with configurations, system prompts, and Indian language support

import logging
import json
import os
from typing import Optional, List, Dict
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class AgentManagementService:
    """Service for creating and managing voice agents"""
    
    def __init__(self):
        self.agents_dir = "/tmp/agents_db"
        os.makedirs(self.agents_dir, exist_ok=True)

    def create_agent(
        self,
        name: str,
        job_role: str,
        system_instruction: str,
        language: str,
        llm_provider: str = "groq",
        tts_provider: str = "replicate_xtts",
        stt_provider: str = "google_stt",
        voice_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> dict:
        """Create a new voice agent"""
        try:
            agent_id = str(uuid.uuid4())
            
            agent_config = {
                "id": agent_id,
                "name": name,
                "job_role": job_role,
                "system_instruction": system_instruction,
                "language": language,
                "llm_provider": llm_provider,
                "tts_provider": tts_provider,
                "stt_provider": stt_provider,
                "voice_id": voice_id,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "status": "active"
            }
            
            # Save agent configuration
            agent_path = os.path.join(self.agents_dir, f"{agent_id}.json")
            with open(agent_path, "w") as f:
                json.dump(agent_config, f, indent=2)
            
            logger.info(f"Created agent: {agent_id}")
            return {
                "success": True,
                "agent_id": agent_id,
                "message": f"Agent '{name}' created successfully",
                "config": agent_config
            }
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return {"success": False, "error": str(e)}

    def get_agent(self, agent_id: str) -> dict:
        """Retrieve agent configuration"""
        try:
            agent_path = os.path.join(self.agents_dir, f"{agent_id}.json")
            if os.path.exists(agent_path):
                with open(agent_path, "r") as f:
                    agent_config = json.load(f)
                return {"success": True, "agent": agent_config}
            else:
                return {"success": False, "error": "Agent not found"}
        except Exception as e:
            logger.error(f"Error retrieving agent: {e}")
            return {"success": False, "error": str(e)}

    def update_agent(
        self,
        agent_id: str,
        updates: Dict
    ) -> dict:
        """Update agent configuration"""
        try:
            agent_path = os.path.join(self.agents_dir, f"{agent_id}.json")
            if not os.path.exists(agent_path):
                return {"success": False, "error": "Agent not found"}
            
            with open(agent_path, "r") as f:
                agent_config = json.load(f)
            
            # Update only allowed fields
            allowed_fields = [
                "name", "job_role", "system_instruction",
                "language", "llm_provider", "tts_provider",
                "stt_provider", "voice_id", "temperature",
                "max_tokens", "status"
            ]
            
            for key, value in updates.items():
                if key in allowed_fields:
                    agent_config[key] = value
            
            agent_config["updated_at"] = datetime.utcnow().isoformat()
            
            with open(agent_path, "w") as f:
                json.dump(agent_config, f, indent=2)
            
            return {"success": True, "agent": agent_config}
        except Exception as e:
            logger.error(f"Error updating agent: {e}")
            return {"success": False, "error": str(e)}

    def list_agents(self, language: Optional[str] = None) -> dict:
        """List all agents, optionally filtered by language"""
        try:
            agents = []
            for agent_file in os.listdir(self.agents_dir):
                if agent_file.endswith(".json"):
                    with open(os.path.join(self.agents_dir, agent_file), "r") as f:
                        agent_config = json.load(f)
                        if language is None or agent_config.get("language") == language:
                            agents.append(agent_config)
            
            return {"success": True, "agents": agents, "count": len(agents)}
        except Exception as e:
            logger.error(f"Error listing agents: {e}")
            return {"success": False, "error": str(e)}

    def delete_agent(self, agent_id: str) -> dict:
        """Delete an agent"""
        try:
            agent_path = os.path.join(self.agents_dir, f"{agent_id}.json")
            if os.path.exists(agent_path):
                os.remove(agent_path)
                return {"success": True, "message": f"Agent {agent_id} deleted"}
            else:
                return {"success": False, "error": "Agent not found"}
        except Exception as e:
            logger.error(f"Error deleting agent: {e}")
            return {"success": False, "error": str(e)}

    def enhance_prompt(
        self,
        system_instruction: str,
        language: str
    ) -> str:
        """Enhance system prompt with language-specific context"""
        language_context = {
            "hi": "You are speaking in Hindi. Use appropriate Hindi grammar and phrases.",
            "ta": "You are speaking in Tamil. Use appropriate Tamil grammar and phrases.",
            "te": "You are speaking in Telugu. Use appropriate Telugu grammar and phrases.",
            "kn": "You are speaking in Kannada. Use appropriate Kannada grammar and phrases.",
            "ml": "You are speaking in Malayalam. Use appropriate Malayalam grammar and phrases.",
            "bn": "You are speaking in Bengali. Use appropriate Bengali grammar and phrases.",
            "gu": "You are speaking in Gujarati. Use appropriate Gujarati grammar and phrases.",
            "mr": "You are speaking in Marathi. Use appropriate Marathi grammar and phrases.",
            "en-IN": "You are speaking in Indian English. Use Indian English vocabulary and expressions."
        }
        
        enhanced_prompt = f"{system_instruction}\n\n{language_context.get(language, '')}\n\nAlways be respectful, helpful, and culturally sensitive."
        return enhanced_prompt

    def clone_agent(
        self,
        source_agent_id: str,
        new_name: str
    ) -> dict:
        """Clone an existing agent with a new name"""
        try:
            source_path = os.path.join(self.agents_dir, f"{source_agent_id}.json")
            if not os.path.exists(source_path):
                return {"success": False, "error": "Source agent not found"}
            
            with open(source_path, "r") as f:
                source_config = json.load(f)
            
            new_agent_id = str(uuid.uuid4())
            source_config["id"] = new_agent_id
            source_config["name"] = new_name
            source_config["created_at"] = datetime.utcnow().isoformat()
            source_config["updated_at"] = datetime.utcnow().isoformat()
            
            agent_path = os.path.join(self.agents_dir, f"{new_agent_id}.json")
            with open(agent_path, "w") as f:
                json.dump(source_config, f, indent=2)
            
            return {"success": True, "agent_id": new_agent_id, "agent": source_config}
        except Exception as e:
            logger.error(f"Error cloning agent: {e}")
            return {"success": False, "error": str(e)}

    def get_indian_language_support(self) -> dict:
        """Get supported Indian languages"""
        return {
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
