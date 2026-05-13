# KaliGhost Dockerfile
# Base: Kali Linux con herramientas esenciales
# Con llama-cpp-python precompilado
# Mantenido por elKalivpn

# --- Fase 1: Construcción ---
FROM kalilinux/kali-rolling as builder

# Metadatos
LABEL maintainer="elkalivpn@kalighost.dev" \
        description="KaliGhost - Sistema de pentesting autónomo con IA" \
        version="1.1.8"

# Variables de entorno
ENV DEBIAN_FRONTEND=noninteractive \
    KALI_ROLLING=true \
    SHELL=/bin/bash

# Paquetes esenciales para construcción
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    wget \
    && rm -rf /var/lib/apt/lists/*


# Instalar herramientas de Kali
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    metasploit-framework \
    wireshark \
    burpsuite \
    sqlmap \
    john \
    hashcat \
    hydra \
    openvas \
    theharvester \
    dnsenum \
    && rm -rf /var/lib/apt/lists/*



# --- Fase 2: YrYs-Agent IA ---
FROM python:3.11-slim as agent

# Instalar dependencias de construcción para C/C++
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    git \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Crear usuario no privilegiado
RUN useradd -m -s /bin/bash kalighost

# Copiar herramientas esenciales
COPY --from=builder /usr/bin/nmap /usr/bin/nmap
COPY --from=builder /usr/bin/msfconsole /usr/bin/msfconsole
COPY --from=builder /usr/bin/wireshark /usr/bin/wireshark

# Directorios y permisos
WORKDIR /home/kalighost
RUN chown -R kalighost:kalighost /home/kalighost

# Cambiar a usuario kalighost para instalar dependencias
USER kalighost

# Crear requirements temporales sin llama-cpp-python
COPY requirements.txt .
RUN grep -v 'llama-cpp-python' requirements.txt > requirements-no-llama.txt

# Instalar todas las demás dependencias
RUN pip install --no-cache-dir -r requirements-no-llama.txt

# Copiar llama-cpp-python ya compilado localmente
COPY vendor/llama-cpp-python /home/kalighost/.local/lib/python3.11/site-packages/

# Volver a root para copiar el agente
USER root
COPY src/agent ./YrYs-Agent
RUN chown -R kalighost:kalighost ./YrYs-Agent && chmod +x ./YrYs-Agent/main.py

# --- Fase 3: Final ---
FROM python:3.11-slim

# Agregar repositorio de Kali para metasploit-framework
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    && curl -fsSL https://archive.kali.org/archive-key.asc | gpg --dearmor -o /usr/share/keyrings/kali-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/kali-archive-keyring.gpg] https://http.kali.org/kali kali-rolling main non-free contrib" > /etc/apt/sources.list.d/kali.list \
    && apt-get update

# Instalar herramientas base
RUN apt-get install -y --no-install-recommends \
    nmap \
    metasploit-framework \
    wireshark \
    && rm -rf /var/lib/apt/lists/*


# Crear usuario no privilegiado
RUN useradd -m -s /bin/bash kalighost

# Copiar solo lo esencial
COPY --from=agent /home/kalighost /home/kalighost

# Cambiar a usuario no privilegiado
USER kalighost
WORKDIR /home/kalighost

# Exponer puertos
EXPOSE 22 80 443 8080 9001

# Comando predeterminado
CMD ["python3", "./YrYs-Agent/main.py", "--autonomous", "--model", "claude-3-opus"]