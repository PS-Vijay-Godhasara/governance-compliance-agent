#!/usr/bin/env python3
"""Simple test script to verify the governance agent works"""

import asyncio
import httpx
import json


async def test_agent():
    """Test the governance agent with simple examples"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        
        # 1. Health check
        print("🔍 Testing health check...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"✅ Health: {response.json()}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # 2. Register a simple policy
        print("\n📝 Registering policy...")
        policy_data = {
            "name": "simple_validation",
            "content": "User must have valid email and age between 18-65"
        }
        
        try:
            response = await client.post(f"{base_url}/policies", json=policy_data)
            result = response.json()
            policy_id = result["policy_id"]
            print(f"✅ Policy registered: {policy_id}")
        except Exception as e:
            print(f"❌ Policy registration failed: {e}")
            return
        
        # 3. Test valid data
        print("\n✅ Testing valid data...")
        valid_data = {
            "policy_id": policy_id,
            "data": {
                "email": "user@example.com",
                "age": 25
            }
        }
        
        try:
            response = await client.post(f"{base_url}/validate", json=valid_data)
            result = response.json()
            print(f"Valid data result: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"❌ Valid data test failed: {e}")
        
        # 4. Test invalid data
        print("\n❌ Testing invalid data...")
        invalid_data = {
            "policy_id": policy_id,
            "data": {
                "email": "invalid-email",
                "age": 150
            }
        }
        
        try:
            response = await client.post(f"{base_url}/validate", json=invalid_data)
            result = response.json()
            print(f"Invalid data result: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"❌ Invalid data test failed: {e}")
        
        # 5. Get policy details
        print(f"\n📋 Getting policy details...")
        try:
            response = await client.get(f"{base_url}/policies/{policy_id}")
            result = response.json()
            print(f"Policy details: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"❌ Get policy failed: {e}")


if __name__ == "__main__":
    print("🧪 Testing Governance & Compliance Agent")
    print("=" * 50)
    print("Make sure the agent is running: python run.py")
    print("=" * 50)
    
    asyncio.run(test_agent())