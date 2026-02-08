#!/bin/bash
# invoke.sh - Build and run AgenticSeek Docker container

set -e

# Configuration
CONTAINER_NAME="agentic-seek-backend"
HOST_PORT=11420
CONTAINER_PORT=7777
IMAGE_NAME="agentic-seek:latest"

echo "========================================"
echo "  AgenticSeek Docker Container Builder"
echo "========================================"

# Build the Docker image
echo ""
echo "Step 1: Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo ""
echo "Step 2: Stopping and removing existing container..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

echo ""
echo "Step 3: Starting new container..."
echo "  Host port: $HOST_PORT"
echo "  Container port: $CONTAINER_PORT"
echo ""

docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    -v "$(pwd)"/sources:/app/sources:ro \
    -v "$(pwd)"/prompts:/app/prompts:ro \
    -v "$(pwd)"/llm_router:/app/llm_router:ro \
    -v "$(pwd)"/config.ini:/app/config.ini:ro \
    -e "BACKEND_PORT=$CONTAINER_PORT" \
    --add-host="host.docker.internal:host-gateway" \
    --restart=unless-stopped \
    "$IMAGE_NAME"

echo ""
echo "========================================"
echo "  AgenticSeek is now running!"
echo "========================================"
echo ""
echo "  API Address: http://localhost:$HOST_PORT"
echo "  Health Check: http://localhost:$HOST_PORT/health"
echo "  Query Endpoint: http://localhost:$HOST_PORT/query"
echo ""
echo "  To view logs: docker logs -f $CONTAINER_NAME"
echo "  To stop: docker stop $CONTAINER_NAME"
echo "  To remove: docker rm $CONTAINER_NAME"
echo ""
