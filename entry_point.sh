#!/bin/bash
# Entrypoint script for AgenticSeek FastAPI backend

set -e

# Check if config.ini exists, create default if not
if [ ! -f /app/config.ini ]; then
    echo "[MAIN]"
    echo "provider_name = together"
    echo "provider_model = deepseek-ai/DeepSeek-V3"
    echo "provider_server_address = https://api.together.xyz/v1"
    echo "is_local = false"
    echo "agent_name = JARVIS"
    echo "languages = en zh"
    echo "speak = false"
    echo "listen = false"
    echo "recover_last_session = false"
    echo "jarvis_personality = true"
    echo "save_session = true"
    echo ""
    echo "[BROWSER]"
    echo "headless_browser = true"
    echo "stealth_mode = true"
    echo "" > /app/config.ini
fi

# Set default port if not specified
if [ -z "$BACKEND_PORT" ]; then
    BACKEND_PORT=7777
fi

echo "[AgenticSeek] Starting FastAPI server on port $BACKEND_PORT..."

# Create necessary directories
mkdir -p /app/.logs
mkdir -p /app/.screenshots

# Start the FastAPI server with uvicorn
exec uvicorn api:api --host 0.0.0.0 --port $BACKEND_PORT
