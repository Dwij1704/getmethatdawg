#!/bin/bash

# GetMeThatDawg Installation Script
# Install getmethatdawg system-wide for zero-config Python agent deployment

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

log_step() {
    echo -e "${BLUE}🔄${NC} $1"
}

# Configuration
GETMETHATDAWG_HOME="${GETMETHATDAWG_HOME:-/usr/local/lib/getmethatdawg}"
GETMETHATDAWG_BIN="${GETMETHATDAWG_BIN:-/usr/local/bin}"
PYTHON_CMD="${PYTHON_CMD:-python3.11}"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Check dependencies
check_dependencies() {
    log_step "Checking dependencies..."
    local deps_ok=true
    
    # Check Python
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        log_error "Python 3.11+ is required but not found"
        log_info "Install Python 3.11+ from https://python.org or use your package manager"
        deps_ok=false
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is required but not installed"
        log_info "Install Docker from https://docker.com"
        deps_ok=false
    fi
    
    # Check flyctl
    if ! command -v flyctl &> /dev/null; then
        log_warning "flyctl is not installed (required for deployment)"
        log_info "Will attempt to install flyctl automatically"
    fi
    
    # Check if Docker is running
    if command -v docker &> /dev/null && ! docker info &> /dev/null 2>&1; then
        log_warning "Docker is installed but not running"
        log_info "Please start Docker before using getmethatdawg"
    fi
    
    if [[ "$deps_ok" == false ]]; then
        exit 1
    fi
    
    log_success "Dependencies check completed"
}

# Install flyctl if needed
install_flyctl() {
    if ! command -v flyctl &> /dev/null; then
        log_step "Installing flyctl..."
        
        local os=$(detect_os)
        case $os in
            macos)
                if command -v brew &> /dev/null; then
                    brew install flyctl
                else
                    curl -L https://fly.io/install.sh | sh
                fi
                ;;
            linux)
                curl -L https://fly.io/install.sh | sh
                ;;
            *)
                log_error "Automatic flyctl installation not supported on this OS"
                log_info "Please install flyctl manually from https://fly.io/docs/getting-started/installing-flyctl/"
                exit 1
                ;;
        esac
        
        log_success "flyctl installed"
    fi
}

# Create installation directories
create_directories() {
    log_step "Creating installation directories..."
    
    sudo mkdir -p "$GETMETHATDAWG_HOME"
    sudo mkdir -p "$GETMETHATDAWG_HOME/lib/python"
    sudo mkdir -p "$GETMETHATDAWG_HOME/libexec"
    sudo mkdir -p "$GETMETHATDAWG_HOME/docs"
    sudo mkdir -p "$GETMETHATDAWG_HOME/examples"
    
    log_success "Directories created"
}

# Install getmethatdawg-sdk
install_getmethatdawg_sdk() {
    log_step "Installing getmethatdawg Python SDK..."
    
    # Install getmethatdawg-sdk with dependencies
    sudo "$PYTHON_CMD" -m pip install --target "$GETMETHATDAWG_HOME/lib/python" ./getmethatdawg-sdk/
    
    # Install required dependencies
    sudo "$PYTHON_CMD" -m pip install --target "$GETMETHATDAWG_HOME/lib/python" flask gunicorn
    
    log_success "getmethatdawg SDK installed"
}

# Install getmethatdawg CLI
install_getmethatdawg_cli() {
    log_step "Installing getmethatdawg CLI..."
    
    # Create the main getmethatdawg executable
    sudo tee "$GETMETHATDAWG_BIN/getmethatdawg" > /dev/null << EOF
#!/bin/bash

# getmethatdawg - Zero-config deploy for Python agents
# System-wide installation version

set -euo pipefail

# Set up Python path to find getmethatdawg modules
export PYTHONPATH="$GETMETHATDAWG_HOME/lib/python:\$PYTHONPATH"
export GETMETHATDAWG_HOME="$GETMETHATDAWG_HOME"
export GETMETHATDAWG_LIBEXEC="$GETMETHATDAWG_HOME/libexec"

# Source the main deployment script
exec "\$GETMETHATDAWG_HOME/libexec/getmethatdawg-main.sh" "\$@"
EOF
    
    # Make executable
    sudo chmod +x "$GETMETHATDAWG_BIN/getmethatdawg"
    
    # Install the main deployment script
    sudo cp bin/getmethatdawg "$GETMETHATDAWG_HOME/libexec/getmethatdawg-main.sh"
    sudo chmod +x "$GETMETHATDAWG_HOME/libexec/getmethatdawg-main.sh"
    
    # Install supporting files
    sudo cp -r libexec/* "$GETMETHATDAWG_HOME/libexec/" 2>/dev/null || true
    
    log_success "getmethatdawg CLI installed"
}

# Install documentation and examples
install_docs() {
    log_step "Installing documentation and examples..."
    
    # Install documentation
    sudo cp -r docs/* "$GETMETHATDAWG_HOME/docs/" 2>/dev/null || true
    sudo cp README.md "$GETMETHATDAWG_HOME/" 2>/dev/null || true
    sudo cp LICENSE "$GETMETHATDAWG_HOME/" 2>/dev/null || true
    
    # Install examples
    sudo cp -r examples/* "$GETMETHATDAWG_HOME/examples/" 2>/dev/null || true
    
    log_success "Documentation and examples installed"
}

# Install shell completions
install_completions() {
    log_step "Installing shell completions..."
    
    local os=$(detect_os)
    
    # Bash completion
    if [[ -d "/usr/local/etc/bash_completion.d" ]]; then
        sudo cp scripts/completions/getmethatdawg.bash "/usr/local/etc/bash_completion.d/getmethatdawg"
        log_success "Bash completion installed"
    elif [[ -d "/etc/bash_completion.d" ]]; then
        sudo cp scripts/completions/getmethatdawg.bash "/etc/bash_completion.d/getmethatdawg"
        log_success "Bash completion installed"
    fi
    
    # Zsh completion
    if [[ -d "/usr/local/share/zsh/site-functions" ]]; then
        sudo cp scripts/completions/_getmethatdawg "/usr/local/share/zsh/site-functions/_getmethatdawg"
        log_success "Zsh completion installed"
    elif [[ -d "/usr/share/zsh/site-functions" ]]; then
        sudo cp scripts/completions/_getmethatdawg "/usr/share/zsh/site-functions/_getmethatdawg"
        log_success "Zsh completion installed"
    fi
}

# Test installation
test_installation() {
    log_step "Testing installation..."
    
    # Test getmethatdawg command
    if "$GETMETHATDAWG_BIN/getmethatdawg" --version &> /dev/null; then
        log_success "getmethatdawg command works"
    else
        log_error "getmethatdawg command failed"
        exit 1
    fi
    
    # Test Python import
    if PYTHONPATH="$GETMETHATDAWG_HOME/lib/python" "$PYTHON_CMD" -c "import getmethatdawg; print('getmethatdawg SDK imported successfully')" &> /dev/null; then
        log_success "getmethatdawg SDK import works"
    else
        log_warning "getmethatdawg SDK import failed (this may be OK for auto-detect mode)"
    fi
}

# Show post-install instructions
show_post_install() {
    echo ""
    echo -e "${GREEN}🎉 getmethatdawg installation completed successfully!${NC}"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
    echo "  2. Make sure Docker is running: docker info"
    echo "  3. Optionally sign up for Fly.io: flyctl auth signup"
    echo ""
    echo "🚀 Quick Start:"
    echo "  # Create a simple Python file"
    echo "  echo 'def hello(name: str = \"World\"): return {\"message\": f\"Hello, {name}!\"}' > my_agent.py"
    echo ""
    echo "  # Deploy it with auto-detection"
    echo "  getmethatdawg deploy my_agent.py --auto-detect"
    echo ""
    echo "📚 Resources:"
    echo "  - Documentation: $GETMETHATDAWG_HOME/docs/"
    echo "  - Examples: $GETMETHATDAWG_HOME/examples/"
    echo "  - GitHub: https://github.com/Dwij1704/getmethatdawg"
    echo ""
    echo "🆘 Need help? Run: getmethatdawg --help"
}

# Uninstall function
uninstall() {
    log_step "Uninstalling getmethatdawg..."
    
    # Remove files
    sudo rm -f "$GETMETHATDAWG_BIN/getmethatdawg"
    sudo rm -rf "$GETMETHATDAWG_HOME"
    
    # Remove completions
    sudo rm -f "/usr/local/etc/bash_completion.d/getmethatdawg" 2>/dev/null || true
    sudo rm -f "/etc/bash_completion.d/getmethatdawg" 2>/dev/null || true
    sudo rm -f "/usr/local/share/zsh/site-functions/_getmethatdawg" 2>/dev/null || true
    sudo rm -f "/usr/share/zsh/site-functions/_getmethatdawg" 2>/dev/null || true
    
    log_success "getmethatdawg uninstalled"
}

# Main installation function
main() {
    echo -e "${BLUE}🚀 getmethatdawg Installation Script${NC}"
    echo "=================================="
    echo ""
    
    # Check for uninstall
    if [[ "${1:-}" == "uninstall" ]]; then
        uninstall
        return 0
    fi
    
    # Check if running as root
    if [[ $EUID -eq 0 ]]; then
        log_error "Don't run this script as root. It will use sudo when needed."
        exit 1
    fi
    
    # Check if we're in the getmethatdawg directory
    if [[ ! -f "getmethatdawg-sdk/setup.py" ]]; then
        log_error "This script must be run from the getmethatdawg project directory"
        log_info "cd into the cloned getmethatdawg repository and run this script again"
        exit 1
    fi
    
    # Run installation steps
    check_dependencies
    install_flyctl
    create_directories
    install_getmethatdawg_sdk
    install_getmethatdawg_cli
    install_docs
    install_completions
    test_installation
    show_post_install
}

# Handle command line arguments
case "${1:-install}" in
    install|"")
        main "$@"
        ;;
    uninstall)
        uninstall
        ;;
    --help|-h)
        echo "getmethatdawg Installation Script"
        echo ""
        echo "Usage:"
        echo "  $0 [install]    Install getmethatdawg system-wide"
        echo "  $0 uninstall    Remove getmethatdawg installation"
        echo "  $0 --help       Show this help"
        echo ""
        echo "Environment Variables:"
        echo "  GETMETHATDAWG_HOME        Installation directory (default: /usr/local/lib/getmethatdawg)"
        echo "  GETMETHATDAWG_BIN         Binary directory (default: /usr/local/bin)"
        echo "  PYTHON_CMD      Python command (default: python3.11)"
        ;;
    *)
        log_error "Unknown command: $1"
        log_info "Run '$0 --help' for usage information"
        exit 1
        ;;
esac 