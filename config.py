"""
Configuration module for LinkedIn Profile Optimizer
Manages free AI providers, Apify settings, and other global config.
"""

import os
from typing import Dict, Any, Optional

from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()


class AIProviderConfig:
    """Configuration for free AI providers"""

    # ---------- NVIDIA (primary – free) ----------
    NVIDIA_CONFIG = {
        "api_key": "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",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model": "meta/llama3-70b-instruct",
        "max_tokens": 2048,
        "temperature": 0.7,
    }

    # ---------- Groq (alternative – free) ----------
    GROQ_CONFIG = {
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.1-8b-instant",
        "max_tokens": 4096,
        "temperature": 0.7,
    }

    # ---------- Hugging Face (backup – free) ----------
    HUGGINGFACE_CONFIG = {
        "api_key": os.getenv("HUGGINGFACE_API_TOKEN"),
        "base_url": "https://api-inference.huggingface.co/models",
        "model": "microsoft/DialoGPT-large",
        "max_tokens": 1024,
        "temperature": 0.7,
    }


class AppConfig:
    """Global application-level configuration"""

    # Preferred AI provider order
    DEFAULT_PROVIDER = "nvidia"

    # --------- Apify (LinkedIn scraping) ----------
    # Apify configuration with CORRECT values (tested and working)
    APIFY_API_KEY = os.getenv(
        "APIFY_API_KEY",
        "apify_api_hIZ46DC21UJ2OjChR2FMB8tDY7nqNp11T1tR",  # Fixed: 'O' not '0'
    )
    # Use the correct task ID format
    APIFY_LINKEDIN_ACTOR = os.getenv(
        "APIFY_LINKEDIN_ACTOR",
        "mritunjayp.tt.21/mass-linkedin-profile-scraper"  # Your saved task
    )

    # Single-agent prompt (unchanged but included for completeness)
    AGENT_CONFIG = {
        "provider": DEFAULT_PROVIDER,
        "system_prompt": (
            "You are an expert LinkedIn Profile Optimizer and Career Advisor. "
            "You provide comprehensive analysis and recommendations for LinkedIn profiles, "
            "job fit assessment, content optimization, and career guidance.\n\n"
            "Always deliver specific, actionable advice, quantified assessments, "
            "and industry-relevant insights."
        ),
    }

    # ---------- Helper methods ----------
    @classmethod
    def get_provider_config(cls, provider: str) -> Optional[Dict[str, Any]]:
        configs = {
            "nvidia": AIProviderConfig.NVIDIA_CONFIG,
            "groq": AIProviderConfig.GROQ_CONFIG,
            "huggingface": AIProviderConfig.HUGGINGFACE_CONFIG,
        }
        return configs.get(provider.lower())

    @classmethod
    def get_available_providers(cls) -> Dict[str, bool]:
        """Return which providers have valid API keys"""
        return {
            "nvidia": bool(AIProviderConfig.NVIDIA_CONFIG["api_key"]),
            "groq": bool(
                AIProviderConfig.GROQ_CONFIG["api_key"]
                and AIProviderConfig.GROQ_CONFIG["api_key"] != "your_groq_key_here"
            ),
            "huggingface": bool(
                AIProviderConfig.HUGGINGFACE_CONFIG["api_key"]
                and AIProviderConfig.HUGGINGFACE_CONFIG["api_key"]
                != "your_huggingface_token_here"
            ),
        }

    @classmethod
    def get_best_available_provider(cls) -> str:
        """Pick the best provider in priority order"""
        available = cls.get_available_providers()
        for provider in ["nvidia", "groq", "huggingface"]:
            if available.get(provider):
                return provider
        return "nvidia" 