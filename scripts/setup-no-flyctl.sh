#!/bin/bash

# GetMeThatDawg - Setup No-flyctl Version
# This script helps you set up the pre-authenticated container approach

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local deps_ok=true
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is required but not installed"
        deps_ok=false
    fi
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        deps_ok=false
    fi
    
    if ! python3 -c "import cryptography" 2>/dev/null; then
        log_warning "cryptography package not found, attempting to install..."
        pip3 install cryptography || {
            log_error "Failed to install cryptography package"
            deps_ok=false
        }
    fi
    
    if [[ "$deps_ok" == false ]]; then
        log_error "Please install missing prerequisites and try again"
        exit 1
    fi
    
    log_success "All prerequisites met"
}

# Get Fly.io token
get_flyio_token() {
    echo
    log_info "Setting up Fly.io authentication..."
    
    if command -v flyctl &> /dev/null; then
        log_info "flyctl found, you can get your token with: flyctl auth token"
        echo
    else
        log_warning "flyctl not found. You'll need to get your Fly.io API token from:"
        echo "  1. Install flyctl: curl -L https://fly.io/install.sh | sh"
        echo "  2. Login: flyctl auth login"
        echo "  3. Get token: flyctl auth token"
        echo
    fi
    
    echo -n "Enter your Fly.io API token (starts with fly_): "
    read -rs FLY_TOKEN
    echo
    
    if [[ ! "$FLY_TOKEN" =~ ^fly_ ]]; then
        log_error "Token should start with 'fly_'"
        exit 1
    fi
    
    log_success "Fly.io token received"
}

# Encrypt token
encrypt_token() {
    log_info "Encrypting Fly.io token..."
    
    ENCRYPTED_TOKEN=$(python3 scripts/encrypt-flyio-token.py "$FLY_TOKEN" | grep -A1 "ENCRYPTED TOKEN" | tail -1)
    
    if [[ -z "$ENCRYPTED_TOKEN" ]]; then
        log_error "Failed to encrypt token"
        exit 1
    fi
    
    log_success "Token encrypted successfully"
}

# Build container
build_container() {
    log_info "Building authenticated container..."
    
    docker build -f Dockerfile.authenticated-builder \
        --build-arg FLY_API_TOKEN_ENCRYPTED="$ENCRYPTED_TOKEN" \
        -t getmethatdawg/builder:authenticated .
    
    log_success "Container built successfully"
}

# Push to registry
push_container() {
    echo
    log_info "Container registry options:"
    echo "1. GitHub Container Registry (ghcr.io) - Recommended"
    echo "2. Docker Hub"
    echo "3. Skip pushing (test locally only)"
    
    echo -n "Choose option (1-3): "
    read -r choice
    
    case "$choice" in
        1)
            push_to_ghcr
            ;;
        2)
            push_to_dockerhub
            ;;
        3)
            log_info "Skipping container push"
            ;;
        *)
            log_error "Invalid choice"
            exit 1
            ;;
    esac
}

push_to_ghcr() {
    log_info "Pushing to GitHub Container Registry..."
    
    # Tag for GHCR
    docker tag getmethatdawg/builder:authenticated ghcr.io/dwij1704/getmethatdawg-builder:authenticated
    
    # Check if logged in
    if ! docker info | grep -q "Username"; then
        log_warning "Not logged in to GitHub Container Registry"
        echo "Please login with: echo \$GITHUB_TOKEN | docker login ghcr.io -u dwij1704 --password-stdin"
        echo "Or: docker login ghcr.io"
        return 1
    fi
    
    # Push
    docker push ghcr.io/dwij1704/getmethatdawg-builder:authenticated
    log_success "Pushed to GitHub Container Registry"
}

push_to_dockerhub() {
    log_info "Pushing to Docker Hub..."
    
    # Check if logged in
    if ! docker info | grep -q "Username"; then
        log_warning "Not logged in to Docker Hub"
        echo "Please login with: docker login"
        return 1
    fi
    
    # Push
    docker push getmethatdawg/builder:authenticated
    log_success "Pushed to Docker Hub"
}

# Test deployment
test_deployment() {
    echo
    log_info "Testing the authenticated container..."
    
    if [[ -f "examples/simple_ai_crew.py" ]]; then
        log_info "Testing with simple_ai_crew.py..."
        
        docker run --rm \
            -v "$(pwd)/examples/simple_ai_crew.py:/tmp/source.py:ro" \
            getmethatdawg/builder:authenticated \
            /tmp/source.py simple-ai-crew --test-mode
        
        log_success "Test completed"
    else
        log_warning "No test file found, skipping test"
    fi
}

# Main setup flow
main() {
    echo "🚀 GetMeThatDawg - No-flyctl Setup"
    echo "=================================="
    echo
    echo "This script will help you set up getmethatdawg to work without requiring"
    echo "users to install flyctl or set up Fly.io accounts."
    echo
    echo "All deployments will go to YOUR Fly.io account automatically."
    echo
    
    check_prerequisites
    get_flyio_token
    encrypt_token
    build_container
    push_container
    
    echo
    log_success "Setup completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Replace bin/getmethatdawg with bin/getmethatdawg-no-flyctl"
    echo "2. Update homebrew formula"
    echo "3. Test with: ./bin/getmethatdawg-no-flyctl deploy examples/simple_ai_crew.py --auto-detect"
    echo
    echo "Users will now only need Docker to deploy!"
}

main "$@" 