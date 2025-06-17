#!/usr/bin/env python3
"""
Test script to verify environment variable passing
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_env_vars():
    """Test if environment variables are being passed correctly"""
    print("Environment variables loaded:")
    print(f"AZURE_OPENAI_API_KEY: {'SET' if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT SET'}")
    
    # Test subprocess with environment
    env = os.environ.copy()
    print(f"Environment copy includes AZURE_OPENAI_API_KEY: {'AZURE_OPENAI_API_KEY' in env}")
    
    # Try to run codex command with explicit environment
    try:
        process = await asyncio.create_subprocess_shell(
            'echo "Environment test" && codex -p azure -q "say hello" --quiet',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)
        
        print(f"Return code: {process.returncode}")
        print(f"Stdout: {stdout.decode()}")
        print(f"Stderr: {stderr.decode()}")
        
    except asyncio.TimeoutError:
        print("Command timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_env_vars())
