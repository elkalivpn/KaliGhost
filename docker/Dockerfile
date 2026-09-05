# KaliGhost IDE - Main Dockerfile
# Based on Kali Linux for security tools

FROM kalilinux/kali-rolling:latest

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    netcat-traditional \
    nmap \
    tcpdump \
    wireshark-common \
    tshark \
    radare2 \
    gdb \
    file \
    binutils \
    docker.io \
    docker-compose \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /root/.kalighost/workspaces /workspace/logs

# Set permissions
RUN chmod +x kalighost.py

# Expose ports
EXPOSE 8080 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health || exit 1

# Default command
CMD ["python3", "kalighost.py", "start", "--headless"]
