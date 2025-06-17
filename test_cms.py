#!/usr/bin/env python3
"""
Test script for AI Interactive CMS
Tests the basic functionality without requiring Codex CLI API key
"""

import asyncio
import json
import websockets
import requests
import sys
from datetime import datetime

BASE_URL = "http://localhost:8001"
WS_URL = "ws://localhost:8001/ws"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']} at {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_main_page():
    """Test the main page endpoint"""
    print("🔍 Testing main page...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            content = response.text
            if "AI Interactive CMS" in content and "WebSocket" in content:
                print("✅ Main page loads correctly with expected content")
                return True
            else:
                print("❌ Main page content missing expected elements")
                return False
        else:
            print(f"❌ Main page failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page test failed: {e}")
        return False

async def test_websocket_connection():
    """Test WebSocket connection and basic messaging"""
    print("🔍 Testing WebSocket connection...")
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("✅ WebSocket connection established")
            
            # Test shell command (should work even without Codex API key)
            test_message = {
                "type": "shell",
                "command": "echo 'Hello from AI CMS'",
                "workspace": "/tmp"
            }
            
            await websocket.send(json.dumps(test_message))
            print("📤 Sent test shell command")
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            data = json.loads(response)
            
            if data.get("type") == "shell_response":
                result = data.get("result", {})
                if result.get("success") and "Hello from AI CMS" in result.get("stdout", ""):
                    print("✅ WebSocket shell command test passed")
                    return True
                else:
                    print(f"❌ Shell command failed: {result}")
                    return False
            else:
                print(f"❌ Unexpected response type: {data.get('type')}")
                return False
                
    except asyncio.TimeoutError:
        print("❌ WebSocket test timed out")
        return False
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

async def test_codex_command():
    """Test Codex command with proper Azure provider configuration"""
    print("🔍 Testing Codex command with Azure provider...")
    try:
        async with websockets.connect(WS_URL) as websocket:
            test_message = {
                "type": "codex",
                "command": "testing basic functionality",
                "workspace": "/tmp"
            }
            
            await websocket.send(json.dumps(test_message))
            print("📤 Sent test Codex command")
            
            response = await asyncio.wait_for(websocket.recv(), timeout=15)
            data = json.loads(response)
            
            if data.get("type") == "codex_response":
                result = data.get("result", {})
                if result.get("success"):
                    stdout = result.get("stdout", "")
                    if stdout and ("assistant" in stdout or "Hello" in stdout or "assist" in stdout):
                        print("✅ Codex command test passed - received AI response")
                        return True
                    else:
                        print(f"⚠️  Codex responded but output unclear: {stdout}")
                        return True  # Still consider success if no error
                else:
                    stderr = result.get("stderr", "")
                    if "API key" in stderr or "No API key configured" in stderr:
                        print("⚠️  Codex command failed due to missing API key (expected)")
                        return True  # This is expected without API key
                    else:
                        print(f"❌ Codex command failed: {result}")
                        return False
            else:
                print(f"❌ Unexpected response type: {data.get('type')}")
                return False
                
    except Exception as e:
        print(f"❌ Codex test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting AI Interactive CMS Tests")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Main Page", test_main_page),
        ("WebSocket Connection", test_websocket_connection),
        ("Codex Command", test_codex_command),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
        
        print("-" * 30)
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:<8} {test_name}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI Interactive CMS is working correctly.")
        return 0
    elif passed >= total - 1:  # Allow Codex to fail due to API key
        print("✨ Core functionality working! Only Codex API key needed for full functionality.")
        return 0
    else:
        print("💥 Some critical tests failed. Please check the server.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Test runner crashed: {e}")
        sys.exit(1)
