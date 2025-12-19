#!/usr/bin/env python3
"""
Quick demo runner for the Governance & Compliance Agent system
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from examples.agent_usage import main as run_demo


def check_requirements():
    """Check if basic requirements are met"""
    try:
        import httpx
        import chromadb
        print("✅ Core dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def check_ollama():
    """Check if Ollama is available"""
    try:
        import httpx
        response = httpx.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running")
            return True
        else:
            print("⚠️  Ollama server not responding")
            return False
    except Exception:
        print("⚠️  Ollama not available - will use fallback mode")
        return False


def main():
    """Main demo runner"""
    print("🤖 Governance & Compliance Agent Demo Runner")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check Ollama (optional)
    ollama_available = check_ollama()
    if not ollama_available:
        print("Note: Some features may be limited without Ollama")
        print("To install Ollama: curl -fsSL https://ollama.com/install.sh | sh")
        print("Then run: ollama serve && ollama pull mistral:7b")
    
    print("\nStarting demo...")
    print("-" * 30)
    
    # Run the demo
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()