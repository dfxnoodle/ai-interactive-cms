#!/usr/bin/env python3
"""
Test script to verify Codex integration with the FastAPI WebSocket endpoint
"""
import asyncio
import websockets
import json
import sys

async def test_codex_integration():
    """Test the Codex integration via WebSocket"""
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Test AI chat with Codex
            test_message = {
                "type": "ai_chat",
                "prompt": "Write a simple Python function that adds two numbers",
                "workspace": "/tmp"
            }
            
            print(f"📤 Sending message: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            print(f"📥 Received response: {response_data}")
            
            if response_data.get("type") == "ai_response":
                result = response_data.get("result", {})
                if result.get("success"):
                    print("✅ Codex integration working successfully!")
                    print(f"📝 AI Response: {result.get('stdout', 'No output')}")
                else:
                    print("❌ Codex command failed")
                    print(f"🚨 Error: {result.get('error', 'Unknown error')}")
                    print(f"🚨 Stderr: {result.get('stderr', 'No stderr')}")
            else:
                print("❌ Unexpected response type")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Make sure the FastAPI server is running on localhost:8000")
        sys.exit(1)

if __name__ == "__main__":
    print("🧪 Testing Codex integration...")
    asyncio.run(test_codex_integration())
