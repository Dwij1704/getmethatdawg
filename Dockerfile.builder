# Dockerfile for getmethatdawg/builder:latest
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/getmethatdawg

# Copy and install getmethatdawg-sdk
COPY getmethatdawg-sdk/ ./getmethatdawg-sdk/
RUN cd getmethatdawg-sdk && pip install -e .

# Copy the builder script
COPY bin/getmethatdawg-builder ./bin/
RUN chmod +x ./bin/getmethatdawg-builder

# Set up PATH
ENV PATH="/opt/getmethatdawg/bin:$PATH"

# Set up the entry point
ENTRYPOINT ["/opt/getmethatdawg/bin/getmethatdawg-builder"] 