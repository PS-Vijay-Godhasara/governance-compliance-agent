#!/usr/bin/env python3
"""Simple run script for the Governance Agent"""

import asyncio
import subprocess
import sys
import time
import httpx
from pathlib import Path


async def check_ollama():
    """Check if Ollama is running and has required models"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                
                required_models = ["mistral:7b", "llama3.2:3b", "llama3.2:1b"]
                available = [m for m in required_models if m in model_names]
                
                if available:
                    print(f"✅ Ollama running with models: {available}")
                    return True
                else:
                    print("❌ No required models found. Run: ollama pull mistral:7b")
                    return False
            return False
    except:
        print("❌ Ollama not running. Start with: ollama serve")
        return False


def install_requirements():
    """Install Python requirements"""
    print("📦 Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                  check=True)


async def main():
    """Main execution function"""
    print("🚀 Starting Governance & Compliance Agent")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return
    
    # Install requirements
    try:
        install_requirements()
        print("✅ Requirements installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return
    
    # Check Ollama
    if not await check_ollama():
        print("\n🔧 To setup Ollama:")
        print("1. Install: curl -fsSL https://ollama.com/install.sh | sh")
        print("2. Start: ollama serve")
        print("3. Pull model: ollama pull mistral:7b")
        return
    
    # Start the application
    print("\n🎯 Starting FastAPI application...")
    print("📍 API: http://localhost:8000")
    print("📍 Health: http://localhost:8000/health")
    print("📍 Docs: http://localhost:8000/docs")
    print("\n⏹️  Press Ctrl+C to stop")
    
    try:
        import uvicorn
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except ImportError:
        print("❌ uvicorn not installed. Run: pip install uvicorn")


if __name__ == "__main__":
    asyncio.run(main())