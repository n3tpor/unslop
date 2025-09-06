# Start from Ubuntu
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    nano \
    python3 \
    python3-pip \
    sudo \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install solace-agent-mesh and verify installation
RUN pip3 install solace-agent-mesh && sam -v

# Set working directory
WORKDIR /root

# Default to bash shell
CMD ["/bin/bash"]
