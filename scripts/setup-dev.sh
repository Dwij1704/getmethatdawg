#!/bin/bash

# Development setup script for getmethatdawg
set -euo pipefail

echo "🏗️  Setting up getmethatdawg development environment..."

# Check dependencies
echo "📋 Checking dependencies..."
missing_deps=()

if ! command -v python3 &> /dev/null; then
    missing_deps+=("python3")
fi

if ! command -v docker &> /dev/null; then
    missing_deps+=("docker")
fi

if ! command -v flyctl &> /dev/null; then
    missing_deps+=("flyctl")
fi

if [ ${#missing_deps[@]} -ne 0 ]; then
    echo "❌ Missing dependencies: ${missing_deps[*]}"
    echo "Please install them and run this script again"
    echo ""
    echo "On macOS with Homebrew:"
    echo "  brew install python@3.11 docker flyctl"
    echo ""
    echo "Docker Desktop: https://www.docker.com/products/docker-desktop/"
    echo "Fly.io CLI: https://fly.io/docs/hands-on/install-flyctl/"
    exit 1
fi

echo "✅ All dependencies found"

# Install getmethatdawg-sdk in development mode
echo "📦 Installing getmethatdawg-sdk..."
cd getmethatdawg-sdk
pip install -e .
cd ..

# Build the builder Docker image
echo "🐳 Building Docker builder image..."
docker build -t getmethatdawg/builder:latest -f Dockerfile.builder .

# Test the setup
echo "🧪 Testing setup..."
./scripts/test-local.sh

echo "✅ Development environment setup complete!"
echo ""
echo "You can now:"
echo "  - Test locally: ./scripts/test-local.sh"
echo "  - Deploy example: ./bin/getmethatdawg deploy examples/my_agent.py"
echo "  - Build package: make build"
echo "  - Install locally: make install" 