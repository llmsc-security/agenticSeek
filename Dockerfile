# Dockerfile for AgenticSeek FastAPI backend
# Root-level Dockerfile for easy Docker deployment

FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    gnupg \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    gcc \
    g++ \
    gfortran \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (for browser automation)
RUN cd /tmp && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb && \
    apt-get install -y --no-install-recommends ./chrome.deb && \
    rm -rf /var/lib/apt/lists/* /tmp/chrome.deb

# Install ChromeDriver
RUN cd /tmp && \
    CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1) && \
    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O chromedriver.zip && \
    unzip -q chromedriver.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -f /tmp/chromedriver.zip

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/.logs /app/.screenshots /opt/workspace

# Copy application code
COPY api.py .
COPY sources/ ./sources/
COPY prompts/ ./prompts/
COPY llm_router/ ./llm_router/
COPY config.ini .

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose the default port (port 7777)
EXPOSE 7777

# Use entrypoint script to start the server
ENTRYPOINT ["/app/entrypoint.sh"]
