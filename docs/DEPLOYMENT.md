# Deployment Guide for getmethatdawg

This guide covers how to deploy the getmethatdawg package to various environments.

## Development Setup

### 1. Quick Start

```bash
# Clone the repository
git clone https://github.com/getmethatdawg-deploy/getmethatdawg.git
cd getmethatdawg

# Set up development environment
./scripts/setup-dev.sh
```

### 2. Manual Setup

```bash
# Install dependencies
brew install python@3.11 docker flyctl

# Install getmethatdawg-sdk in development mode
cd getmethatdawg-sdk
pip install -e .
cd ..

# Build the builder Docker image
docker build -t getmethatdawg/builder:latest -f Dockerfile.builder .

# Test the setup
./scripts/test-local.sh
```

## Package Building

### 1. Build Python Package

```bash
# Build getmethatdawg-sdk package
make build

# This creates:
# - getmethatdawg-sdk/dist/getmethatdawg-sdk-0.1.0.tar.gz
# - getmethatdawg-sdk/dist/getmethatdawg_sdk-0.1.0-py3-none-any.whl
```

### 2. Build Docker Image

```bash
# Build the builder image
make builder-image

# Or manually:
docker build -t getmethatdawg/builder:latest -f Dockerfile.builder .
```

## Homebrew Formula Deployment

### 1. Create GitHub Release

```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Create release archive
git archive --format=tar.gz --prefix=getmethatdawg-0.1.0/ v0.1.0 > getmethatdawg-0.1.0.tar.gz

# Calculate SHA256
sha256sum getmethatdawg-0.1.0.tar.gz
```

### 2. Update Homebrew Formula

Update the `getmethatdawg.rb` file with the correct URL and SHA256:

```ruby
class GetMeThatDawg < Formula
  desc "Zero-config deploy & MCP for Python agents"
  homepage "https://github.com/getmethatdawg-deploy/getmethatdawg"
  url "https://github.com/getmethatdawg-deploy/getmethatdawg/archive/v0.1.0.tar.gz"
  sha256 "actual_sha256_hash_here"
  license "MIT"
  # ... rest of formula
end
```

### 3. Submit to Homebrew

```bash
# Fork homebrew-core
# Create a new branch
# Add getmethatdawg.rb to Formula/
# Submit a pull request
```

## Docker Image Deployment

### 1. Build Multi-Architecture Image

```bash
# Build and push to Docker Hub
docker buildx build --platform linux/amd64,linux/arm64 \
  -t getmethatdawg/builder:latest \
  -f Dockerfile.builder \
  --push .
```

### 2. Alternative: GitHub Container Registry

```bash
# Tag for GitHub Container Registry
docker tag getmethatdawg/builder:latest ghcr.io/getmethatdawg-deploy/builder:latest

# Push to GitHub Container Registry
docker push ghcr.io/getmethatdawg-deploy/builder:latest
```

## PyPI Deployment

### 1. Build and Upload getmethatdawg-sdk

```bash
cd getmethatdawg-sdk

# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI (requires credentials)
python -m twine upload dist/*
```

### 2. Test Installation

```bash
# Test installation from PyPI
pip install getmethatdawg-sdk

# Test import
python -c "import getmethatdawg; print('Success!')"
```

## Local Installation (Development)

### 1. Install CLI Tool

```bash
# Install locally
make install

# Or manually:
sudo cp bin/getmethatdawg /usr/local/bin/
sudo cp bin/getmethatdawg-builder /usr/local/bin/
sudo mkdir -p /usr/local/lib/getmethatdawg
sudo cp -r libexec /usr/local/lib/getmethatdawg/
```

### 2. Test Installation

```bash
# Test CLI
getmethatdawg --help

# Test deployment
getmethatdawg deploy examples/my_agent.py
```

## Production Deployment

### 1. Prerequisites

- Docker Hub or GitHub Container Registry account
- PyPI account (for getmethatdawg-sdk)
- GitHub repository with releases
- Homebrew tap (optional, for private formula)

### 2. Release Process

1. Update version numbers in:
   - `getmethatdawg-sdk/setup.py`
   - `bin/getmethatdawg` (version command)
   - `getmethatdawg.rb`

2. Create and push git tag:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

3. Build and push Docker image:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 \
     -t getmethatdawg/builder:v0.1.0 \
     -t getmethatdawg/builder:latest \
     -f Dockerfile.builder \
     --push .
   ```

4. Upload to PyPI:
   ```bash
   cd getmethatdawg-sdk
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

5. Create GitHub release with tarball

6. Update and submit Homebrew formula

## Testing Deployments

### 1. Test with Example Agent

```bash
# Test the example agent
getmethatdawg deploy examples/my_agent.py
```

### 2. Test with Custom Agent

```bash
# Create a test agent
cat > test_agent.py << 'EOF'
import getmethatdawg

@getmethatdawg.expose(method="GET", path="/test")
def test():
    return {"status": "ok", "message": "Hello from getmethatdawg!"}
EOF

# Deploy it
getmethatdawg deploy test_agent.py
```

### 3. Verify Deployment

```bash
# Check the deployed endpoint
curl https://your-app.fly.dev/test
```

## Troubleshooting

### Common Issues

1. **Docker permission errors**: Add user to docker group or use `sudo`
2. **flyctl authentication**: Run `flyctl auth login`
3. **Python import errors**: Check `sys.path` and virtual environment
4. **Missing dependencies**: Install via Homebrew or package manager

### Debug Commands

```bash
# Check Docker
docker info

# Check flyctl
flyctl auth whoami

# Check Python
python3 -c "import getmethatdawg; print(getmethatdawg.__version__)"

# Test builder
./scripts/test-local.sh
```

## Rollback

### 1. Rollback Homebrew Formula

```bash
# Revert to previous version in formula
# Submit new PR with reverted changes
```

### 2. Rollback Docker Image

```bash
# Tag previous version as latest
docker tag getmethatdawg/builder:v0.0.9 getmethatdawg/builder:latest
docker push getmethatdawg/builder:latest
```

### 3. Rollback PyPI Package

```bash
# You cannot delete PyPI packages
# Upload a new version with fixes
``` 