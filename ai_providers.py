"""
AI Provider Interface for LinkedIn Profile Optimizer
Unified interface for free AI services with NVIDIA as primary provider
"""
import logging
from typing import Dict, Any, Optional, List
from openai import OpenAI
from config import AppConfig, AIProviderConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProvider:
    """Unified interface for free AI providers"""
    
    def __init__(self, provider: Optional[str] = None):
        """Initialize AI provider with fallback to best available free option"""
        self.provider = provider or AppConfig.get_best_available_provider()
        self.config = AppConfig.get_provider_config(self.provider)
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate AI client"""
        try:
            if self.provider == "nvidia":
                if self.config is None:
                    logger.error("NVIDIA config is None - cannot initialize client")
                    return
                    
                self.client = OpenAI(
                    base_url=self.config["base_url"],
                    api_key=self.config["api_key"]
                )
                logger.info("NVIDIA AI client initialized successfully")
            elif self.provider == "groq":
                if self.config is None:
                    logger.error("Groq config is None - cannot initialize client")
                    return
                    
                self.client = OpenAI(
                    base_url=self.config["base_url"],
                    api_key=self.config["api_key"]
                )
                logger.info("Groq AI client initialized successfully")
            elif self.provider == "huggingface":
                # For HuggingFace, we'll use requests directly
                logger.info("HuggingFace AI client initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider} client: {e}")
            # Fallback to NVIDIA if initialization fails
            if self.provider != "nvidia":
                self.provider = "nvidia"
                self.config = AppConfig.get_provider_config("nvidia")
                self._initialize_client()
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate AI response using the configured provider"""
        try:
            if self.provider in ["nvidia", "groq"]:
                return self._generate_openai_compatible(prompt, system_prompt or "", **kwargs)
            elif self.provider == "huggingface":
                return self._generate_huggingface(prompt, system_prompt or "", **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"Error generating response with {self.provider}: {e}")
            # Try fallback to NVIDIA if not already using it
            if self.provider != "nvidia":
                logger.info("Falling back to NVIDIA...")
                self.provider = "nvidia"
                self.config = AppConfig.get_provider_config("nvidia")
                self._initialize_client()
                return self._generate_openai_compatible(prompt, system_prompt or "", **kwargs)
            else:
                return f"I apologize, but I'm currently unable to process your request due to technical issues. Please try again later."
    
    def _generate_openai_compatible(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        """Generate response using OpenAI-compatible API (NVIDIA, Groq)"""
        messages = []
        # For NVIDIA, do not use 'system' role, only 'user' for the first message
        # If you want to include a system prompt, prepend it to the user content
        if system_prompt:
            user_content = f"{system_prompt}\n\n{prompt}"
        else:
            user_content = prompt
        messages.append({"role": "user", "content": user_content})
        # Merge kwargs with default config
        generation_params = {
            "model": self.config["model"] if self.config else None,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config["max_tokens"] if self.config else None),
            "temperature": kwargs.get("temperature", self.config["temperature"] if self.config else None),
            "stream": False
        }
        try:
            if self.client is None:
                raise Exception("Client not initialized")
            response = self.client.chat.completions.create(**generation_params)
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"{self.provider.title()} API error: {e}")
            raise
    
    def _generate_huggingface(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        """Generate response using HuggingFace Inference API"""
        import requests
        
        # Combine system prompt and user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        if not self.config or 'api_key' not in self.config:
            raise ValueError("Missing API key configuration for HuggingFace")
            
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": kwargs.get("max_tokens", self.config["max_tokens"]),
                "temperature": kwargs.get("temperature", self.config["temperature"]),
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                f"{self.config['base_url']}/{self.config['model']}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                else:
                    return str(result).strip()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            raise
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider"""
        if not self.config:
            return {
                "provider": self.provider,
                "model": "unknown",
                "status": "inactive",
                "max_tokens": 0
            }
        
        return {
            "provider": self.provider,
            "model": self.config.get("model", "unknown"),
            "status": "active" if self.client else "inactive",
            "max_tokens": self.config.get("max_tokens", 0)
        }

# Global AI provider instance
ai_provider = AIProvider()

def get_ai_response(prompt: str, system_prompt: str | None = None, **kwargs) -> str:
    """Convenience function to get AI response"""
    return ai_provider.generate_response(prompt, system_prompt, **kwargs)

def get_provider_status() -> Dict[str, Any]:
    """Get current provider status"""
    return ai_provider.get_provider_info() 