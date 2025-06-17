# AI Interactive CMS

A powerful AI-powered interactive Content Management System that provides intelligent code assistance through a web interface.

## Features

- 🤖 **AI-Powered Code Assistance**: Get help with coding questions and concepts
- 💬 **Interactive Chat Interface**: Communicate with AI through a modern chat interface  
- 🔄 **WebSocket Communication**: Real-time bidirectional communication between frontend and backend
- 🎨 **Modern UI**: Beautiful, responsive interface with animated backgrounds
- 📁 **Conversation Management**: Maintain context across chat sessions

## Prerequisites

Before running this application, make sure you have:

1. **Python 3.11+** installed
2. **uv** - Modern Python package manager (recommended)
   ```bash
   # Install uv (cross-platform)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or using pip
   pip install uv
   ```
3. **Git** (optional, for version control)

## Installation

1. Clone or download this project:
   ```bash
   git clone <repository-url>
   cd interactive-cms
   ```

2. Install Python dependencies using uv:
   ```bash
   # Create a virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   
   # Alternative: Install directly without virtual environment
   uv pip install -r requirements.txt
   ```

3. Verify Codex CLI is working:
   ```bash
   codex --help
   ```

## Usage

### Quick Start with uv (Recommended)

For the fastest setup using uv:

```bash
# Clone and setup in one go
git clone <repository-url>
cd interactive-cms

# Initialize and run the project
uv run python main.py
```

This automatically:
- Creates a virtual environment
- Installs all dependencies
- Starts the FastAPI server

### Manual Setup with uv

1. Initialize the project with uv:
   ```bash
   # Sync dependencies with virtual environment
   uv sync
   
   # Activate the virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Start the server:
   ```bash
   # Using uv run (no activation needed)
   uv run python main.py
   
   # Or if environment is activated
   python main.py
   
   # Or using the project script
   uv run start
   ```

### Development Commands with uv

```bash
# Run with auto-reload for development
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Install additional packages
uv add <package-name>

# Install development dependencies
uv sync --dev

# Run tests (if available)
uv run pytest

# Format code
uv run black .
uv run isort .

# Check code quality
uv run flake8
```

### Traditional Python (Alternative)

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python main.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

3. Start interacting with the AI CMS:
   - Use the **AI Chat Interface** to ask questions or request code generation
   - Use the **Terminal Panel** to execute Codex commands or shell commands
   - Monitor real-time output and responses

### Using Makefile (Easiest)

The project includes a Makefile for convenient commands:

```bash
# Complete setup for new users
make setup

# Or step by step
make install  # Install dependencies
make run      # Start the server

# Development commands
make dev      # Install with dev dependencies
make dev-run  # Run with auto-reload
make format   # Format code
make lint     # Check code quality
make clean    # Clean up virtual environment

# See all available commands
make help
```

## API Endpoints

- `GET /` - Serves the main web interface
- `WebSocket /ws` - Real-time communication endpoint
- `GET /health` - Health check endpoint

## WebSocket Message Types

### Sending to Server:
- `ai_chat` - Send prompts to AI for code assistance

### Receiving from Server:
- `ai_response` - AI-generated responses

## Example Usage

### AI Chat Examples:
- "Explain how to create a Python function to calculate fibonacci numbers"
- "What are best practices for error handling in JavaScript?"
- "How does this sorting algorithm work?"
- "What are the benefits of using REST APIs?"
- `git status`
- `npm install`
- `python test.py`

## Project Structure

```
interactive-cms/
├── main.py              # FastAPI backend server
├── requirements.txt     # Python dependencies
├── static/
│   └── index.html      # Frontend interface
└── README.md           # This file
```

## Configuration

The application uses the following default settings:
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 8000
- **Workspace**: Current directory
- **WebSocket**: Real-time communication enabled

## Troubleshooting

## Troubleshooting

### Common Issues:

1. **Connection issues**:
   - Check if port 8000 is available
   - Verify firewall settings

2. **WebSocket connection failed**:
   - Ensure the server is running
   - Check browser console for errors

### Debug Mode:
Run the server with debug logging:
```bash
python main.py --reload --log-level debug
```

## Security Considerations

- This application provides an AI chat interface for coding assistance
- Use only in trusted environments
- Consider implementing authentication for production use
- Always validate AI suggestions before implementing them

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the OpenAI Codex CLI documentation
3. Create an issue in the repository

---

**Note**: This application requires a valid OpenAI API key and Codex CLI setup. Make sure you have appropriate API credits and understand OpenAI's usage policies.
