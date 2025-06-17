from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import subprocess
import asyncio
import json
import os
import uuid
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="AI Interactive CMS", description="AI-powered CMS using Codex CLI")

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

class CodexManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.conversation_history: Dict[str, List[dict]] = {}

    def get_or_create_session(self, session_id: str) -> dict:
        """Get or create a session for conversation management"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        # Update last activity
        self.sessions[session_id]["last_activity"] = datetime.now().isoformat()
        return self.sessions[session_id]
    
    def add_to_conversation(self, session_id: str, role: str, content: str):
        """Add a message to the conversation history"""
        self.get_or_create_session(session_id)
        self.conversation_history[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only the last 20 messages to prevent excessive context
        if len(self.conversation_history[session_id]) > 20:
            self.conversation_history[session_id] = self.conversation_history[session_id][-20:]
    
    def build_conversation_context(self, session_id: str, new_prompt: str) -> str:
        """Build a context-aware prompt including conversation history"""
        self.get_or_create_session(session_id)
        history = self.conversation_history[session_id]
        
        if not history:
            # First message, no context needed
            return new_prompt
        
        # Build context from recent conversation
        context_parts = ["Previous conversation context:"]
        for message in history[-10:]:  # Last 10 messages for context
            role = message["role"]
            content = message["content"][:200]  # Truncate long messages
            if len(message["content"]) > 200:
                content += "..."
            context_parts.append(f"{role.capitalize()}: {content}")
        
        context_parts.append("\nCurrent request:")
        context_parts.append(new_prompt)
        
        return "\n".join(context_parts)
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history for a session"""
        if session_id in self.conversation_history:
            self.conversation_history[session_id] = []

    def parse_codex_response(self, codex_output: str) -> str:
        """Parse Codex CLI JSON output to extract the actual AI response"""
        try:
            # Split by lines and try to parse each JSON line
            lines = codex_output.strip().split('\n')
            responses = []
            
            for line in lines:
                if not line.strip():
                    continue
                    
                try:
                    data = json.loads(line)
                    
                    # Look for assistant messages
                    if data.get('type') == 'message' and data.get('role') == 'assistant':
                        content = data.get('content', [])
                        if isinstance(content, list):
                            for item in content:
                                if item.get('type') == 'output_text':
                                    responses.append(item.get('text', ''))
                        elif isinstance(content, str):
                            responses.append(content)
                    
                    # Look for function call outputs that might contain responses
                    elif data.get('type') == 'function_call_output':
                        output_data = data.get('output', {})
                        if isinstance(output_data, str):
                            try:
                                parsed_output = json.loads(output_data)
                                if 'output' in parsed_output:
                                    responses.append(parsed_output['output'].strip())
                            except json.JSONDecodeError:
                                responses.append(output_data.strip())
                        elif isinstance(output_data, dict) and 'output' in output_data:
                            responses.append(output_data['output'].strip())
                    
                except json.JSONDecodeError:
                    # If it's not JSON, it might be plain text response
                    if line.strip() and not line.startswith('{'):
                        responses.append(line.strip())
            
            # Join all responses
            if responses:
                final_response = '\n'.join(responses).strip()
                # Clean up any escape characters
                final_response = final_response.replace('\\n', '\n').replace('\\"', '"')
                return final_response or "Response processed successfully"
            else:
                # Fallback: return the first non-empty line that looks like text
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('{') and len(line) > 10:
                        return line
                
                return "AI response received successfully"
                
        except Exception as e:
            print(f"Error parsing Codex response: {e}")
            # Return a cleaned version of the original output as fallback
            cleaned = codex_output.replace('\\n', '\n').replace('\\"', '"')
            return cleaned[:500] + "..." if len(cleaned) > 500 else cleaned

    async def execute_ai_chat(self, command: str, session_id: str, workspace_path: str = None, auto_save: bool = True) -> dict:
        """Execute an AI chat command using Codex CLI with conversation context"""
        # Build context-aware prompt
        context_command = self.build_conversation_context(session_id, command)
        
        # Add auto-save instruction if enabled
        if auto_save:
            context_command += "\n\n### Make sure to edit and save to the file ###"
        
        # Add user message to history
        self.add_to_conversation(session_id, "user", command)
        
        try:
            # Prepare Codex CLI command
            codex_cmd = ["codex", "-q"]  # -q for quiet/non-interactive mode
            
            # Add auto-approval flag if auto_save is enabled
            if auto_save:
                codex_cmd.append("--full-auto")
            
            # Add the prompt
            codex_cmd.append(context_command)
            
            # Set working directory
            cwd = workspace_path or os.getcwd()
            
            print(f"Executing Codex CLI in {cwd}: {' '.join(codex_cmd)}")
            
            # Execute Codex CLI command
            process = await asyncio.create_subprocess_exec(
                *codex_cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=dict(os.environ, OPENAI_API_KEY=os.getenv('OPENAI_API_KEY', ''))
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=120.0)
            except asyncio.TimeoutError:
                process.kill()
                raise Exception("Codex CLI execution timed out after 120 seconds")
            
            # Decode output
            stdout_text = stdout.decode('utf-8', errors='replace').strip()
            stderr_text = stderr.decode('utf-8', errors='replace').strip()
            
            print(f"Codex CLI exit code: {process.returncode}")
            print(f"Codex CLI stdout: {stdout_text[:500]}...")
            print(f"Codex CLI stderr: {stderr_text[:200]}...")
            
            if process.returncode == 0:
                # Parse Codex CLI response to extract the actual AI message
                ai_response = self.parse_codex_response(stdout_text)
                self.add_to_conversation(session_id, "assistant", ai_response)
                
                return {
                    "success": True,
                    "stdout": ai_response,
                    "stderr": stderr_text,
                    "exit_code": process.returncode,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Error occurred
                error_msg = stderr_text or stdout_text or f"Codex CLI failed with exit code {process.returncode}"
                
                # Check for common error patterns
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    error_msg = "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
                elif "not found" in error_msg.lower() and "codex" in error_msg.lower():
                    error_msg = "⚠️ Codex CLI not found. Please install with: npm install -g @openai/codex"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "stderr": stderr_text,
                    "stdout": stdout_text,
                    "exit_code": process.returncode,
                    "timestamp": datetime.now().isoformat()
                }
                
        except FileNotFoundError:
            error_msg = "⚠️ Codex CLI not found. Please install with: npm install -g @openai/codex"
            return {
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            error_msg = f"Error executing Codex CLI: {str(e)}"
            print(f"Exception in execute_ai_chat: {e}")
            return {
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }

codex_manager = CodexManager()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get_homepage():
    """Serve the main HTML page"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend not found</h1><p>Please ensure static/index.html exists</p>", status_code=404)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    session_id = str(uuid.uuid4())
    print(f"New WebSocket connection: {session_id}")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from {session_id}: {data}")
            
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON received: {e}")
                await manager.send_personal_message(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }), websocket)
                continue
            
            command_type = message_data.get("type")
            workspace = message_data.get("workspace", os.getcwd())
            auto_save = message_data.get("auto_save", True)  # Default to True for backward compatibility
            
            print(f"Processing command type: {command_type}")
            
            if command_type == "ai_chat":
                # Handle AI chat requests (using Codex for code generation/modification)
                ai_prompt = message_data.get("prompt", "")
                auto_save = message_data.get("auto_save", True)  # Default to True for backward compatibility
                print(f"AI chat prompt: {ai_prompt}")
                
                if not ai_prompt:
                    await manager.send_personal_message(json.dumps({
                        "type": "ai_response",
                        "session_id": session_id,
                        "prompt": "",
                        "result": {
                            "success": False,
                            "error": "Empty prompt provided",
                            "timestamp": datetime.now().isoformat()
                        }
                    }), websocket)
                    continue
                
                # Use context-aware command execution
                result = await codex_manager.execute_ai_chat(ai_prompt, session_id, workspace, auto_save)
                await manager.send_personal_message(json.dumps({
                    "type": "ai_response",
                    "session_id": session_id,
                    "prompt": ai_prompt,
                    "result": result
                }), websocket)
            
            elif command_type == "clear_conversation":
                # Clear conversation history for this session
                codex_manager.clear_conversation(session_id)
                await manager.send_personal_message(json.dumps({
                    "type": "conversation_cleared",
                    "session_id": session_id,
                    "message": "Conversation history cleared",
                    "timestamp": datetime.now().isoformat()
                }), websocket)
            
            elif command_type == "get_conversation_history":
                # Get conversation history for this session
                codex_manager.get_or_create_session(session_id)
                history = codex_manager.conversation_history.get(session_id, [])
                await manager.send_personal_message(json.dumps({
                    "type": "conversation_history",
                    "session_id": session_id,
                    "history": history,
                    "timestamp": datetime.now().isoformat()
                }), websocket)
            else:
                print(f"Unknown command type: {command_type}")
                await manager.send_personal_message(json.dumps({
                    "type": "error",
                    "message": f"Unknown command type: {command_type}"
                }), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Session {session_id} disconnected")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    
    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    print("🚀 Starting AI Interactive CMS...")
    print("📝 Make sure you have Codex CLI installed and configured")
    print("⚠️  Running with --dangerously-auto-approve-everything (auto-executes commands)")
    print("🌐 Server will be available at http://localhost:8000")
    print(f"🔑 Azure OpenAI API Key: {'SET' if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT SET'}")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=["test_*.py"])
