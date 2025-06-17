# AI CMS Systemd Service

This directory contains the systemd service configuration for running the AI Interactive CMS as a system service.

## Files

- `ai-cms.service` - The systemd service unit file
- `.env.example` - Environment variables template

## Quick Setup

1. **Install the service (user service - recommended):**
   ```bash
   mkdir -p ~/.config/systemd/user
   cp ai-cms.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable ai-cms
   ```

2. **Configure environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   nano .env
   ```

3. **Start the service:**
   ```bash
   systemctl --user start ai-cms
   ```

4. **Verify it's working:**
   ```bash
   systemctl --user status ai-cms
   curl http://localhost:8000/health
   ```

## Service Management

Use systemctl commands to control the service:

### User Service (recommended)
```bash
# Install
mkdir -p ~/.config/systemd/user
cp ai-cms.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable ai-cms

# Control
systemctl --user start ai-cms
systemctl --user stop ai-cms
systemctl --user restart ai-cms
systemctl --user status ai-cms

# Logs
journalctl --user -u ai-cms -f
```

### System Service (requires sudo)
```bash
# Install
sudo cp ai-cms.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ai-cms

# Control
sudo systemctl start ai-cms
sudo systemctl stop ai-cms
sudo systemctl restart ai-cms
systemctl status ai-cms

# Logs
journalctl -u ai-cms -f
```

## Service Configuration

The service is configured with the following features:

- **Auto-restart**: The service will automatically restart if it crashes
- **Environment isolation**: Runs with security restrictions
- **Logging**: All output is logged to the systemd journal
- **Resource limits**: Reasonable limits on file handles and processes
- **Environment variables**: Loads from `.env` file if present

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required for AI functionality
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Azure OpenAI alternative
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## Troubleshooting

1. **Check service status:**
   ```bash
   systemctl --user status ai-cms
   ```

2. **View logs:**
   ```bash
   journalctl --user -u ai-cms -f
   ```

3. **Check if uv is available:**
   ```bash
   which uv
   /snap/bin/uv --version
   ```

4. **Verify dependencies:**
   ```bash
   cd /home/dinochlai/interactive-cms
   uv pip list
   ```

5. **Test manual startup:**
   ```bash
   cd /home/dinochlai/interactive-cms
   uv run python main.py
   ```

## Service Features

- **Automatic startup**: Starts on system boot (when enabled)
- **Restart on failure**: Automatically restarts if the service crashes
- **Security hardening**: Runs with restricted permissions
- **Environment variable support**: Loads from `.env` file
- **Comprehensive logging**: All output captured in systemd journal
- **Resource management**: Proper limits on system resources

## Network Access

The service will be available at:
- Local: http://localhost:8000
- Network: http://your-server-ip:8000

Make sure port 8000 is open in your firewall if you need external access.

## Security Notes

The service runs with the following security restrictions:
- No new privileges can be acquired
- Private temporary directory
- Protected system directories
- Home directory protection (except for the app directory)

This ensures the service runs securely even if compromised.
