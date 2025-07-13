# Dockerfile for yoo/builder:latest
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/yoo

# Copy and install yoo-sdk
COPY yoo-sdk/ ./yoo-sdk/
RUN cd yoo-sdk && pip install -e .

# Copy the builder script
COPY bin/yoo-builder ./bin/
RUN chmod +x ./bin/yoo-builder

# Set up PATH
ENV PATH="/opt/yoo/bin:$PATH"

# Set up the entry point
ENTRYPOINT ["/opt/yoo/bin/yoo-builder"] 