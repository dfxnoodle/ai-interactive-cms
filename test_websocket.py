#!/usr/bin/env python3
"""
Simple WebSocket test to verify backend communication
"""

import asyncio
import json
import websockets

async def test_websocket():
    uri = "ws://localhost:8001/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Test shell command
            test_message = {
                "type": "shell",
                "command": "echo 'Hello from test'",
                "workspace": "/tmp"
            }
            
            print(f"📤 Sending: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            print(f"📥 Received: {response}")
            
            # Test Codex command
            codex_message = {
                "type": "codex",
                "command": "testing",
                "workspace": "/tmp"
            }
            
            print(f"📤 Sending: {codex_message}")
            await websocket.send(json.dumps(codex_message))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=15)
            print(f"📥 Received: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
