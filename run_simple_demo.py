#!/usr/bin/env python3
"""
Simple demo runner for the Governance & Compliance Agent
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from examples.simple_usage import test_direct_usage, demo_business_scenarios


def main():
    """Main demo runner"""
    print("🤖 Simple Governance & Compliance Agent Demo")
    print("=" * 50)
    
    print("✅ Running simplified version with file-based policies")
    print("✅ No database or complex dependencies required")
    print("✅ Policies stored in ./policies directory")
    
    print("\nStarting demo...")
    print("-" * 30)
    
    try:
        # Run direct usage test
        test_direct_usage()
        
        # Run business scenarios
        demo_business_scenarios()
        
        print("\n✅ All demos completed successfully!")
        print("\n🚀 To start the API server, run:")
        print("   python -m src.simple_main")
        print("\n📚 For more examples, see:")
        print("   python examples/simple_usage.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()