FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt


# --- Auto-Generated Entrypoint Configuration ---
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN mkdir -p /var/log && touch /var/log/app.log
EXPOSE 5000

FROM ubuntu:20.04

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# --- Auto-Generated Entrypoint Configuration ---
# Copy the entrypoint script to a standard location and ensure it has a proper shebang
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN echo "#!/usr/bin/env bash" | cat - /usr/local/bin/entrypoint.sh > /tmp/entrypoint.tmp && \
    mv /tmp/entrypoint.tmp /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

# Create log directory and file with proper permissions
RUN mkdir -p /var/log && touch /var/log/app.log && chmod 666 /var/log/app.log

EXPOSE 5000

# Use exec form to avoid shell parsing issues

FROM ubuntu:20.04

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Add entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# Ensure a proper shebang (if missing) and make it executable
RUN if ! head -n1 /usr/local/bin/entrypoint.sh | grep -q '^#!/usr/bin/env bash'; then \
        sed -i '1i#!/usr/bin/env bash' /usr/local/bin/entrypoint.sh; \
    fi && \
    chmod +x /usr/local/bin/entrypoint.sh

# Create log directory and file with appropriate permissions
RUN mkdir -p /var/log && touch /var/log/app.log && chmod 666 /var/log/app.log

EXPOSE 5000


FROM ubuntu:20.04

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy and prepare the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# Ensure a proper shebang (add if missing) and make it executable
RUN if ! head -n1 /usr/local/bin/entrypoint.sh | grep -q '^#!/usr/bin/env bash'; then \
        sed -i '1i#!/usr/bin/env bash' /usr/local/bin/entrypoint.sh; \
    fi && \
    chmod +x /usr/local/bin/entrypoint.sh

# Create log directory and file with appropriate permissions
RUN mkdir -p /var/log && \
    touch /var/log/app.log && \
    chmod 666 /var/log/app.log

EXPOSE 5000

# Use exec form to avoid shell parsing issues

FROM ubuntu:20.04

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy and prepare the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# Ensure a proper shebang (add if missing) and make it executable
RUN if ! head -n1 /usr/local/bin/entrypoint.sh | grep -q '^#!/usr/bin/env bash'; then \
        sed -i '1i#!/usr/bin/env bash' /usr/local/bin/entrypoint.sh; \
    fi && \
    chmod +x /usr/local/bin/entrypoint.sh

# Create log directory and file with appropriate permissions
RUN mkdir -p /var/log && \
    touch /var/log/app.log && \
    chmod 666 /var/log/app.log

EXPOSE 5000

# Use exec form to avoid shell parsing issues
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]
