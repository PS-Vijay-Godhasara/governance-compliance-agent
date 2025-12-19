"""Ollama provider for free LLM models"""

import httpx
import json
from typing import Optional, Dict, Any


class OllamaProvider:
    """Minimal Ollama client for free models"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral:7b"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Ollama"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.1),
                        "top_p": kwargs.get("top_p", 0.9),
                        "num_predict": kwargs.get("max_tokens", 512)
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            print(f"Ollama error: {e}")
            return ""
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def health_check(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False