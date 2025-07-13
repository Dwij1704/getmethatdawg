#!/bin/bash

# Local installation script for getmethatdawg
# This script installs getmethatdawg on your local machine for testing

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Installing getmethatdawg locally...${NC}"

# Configuration
GETMETHATDAWG_HOME="$HOME/.getmethatdawg"
GETMETHATDAWG_BIN="$HOME/.local/bin"

# Create directories
mkdir -p "$GETMETHATDAWG_HOME/lib/python"
mkdir -p "$GETMETHATDAWG_HOME/libexec"
mkdir -p "$GETMETHATDAWG_BIN"

echo -e "${BLUE}Installing getmethatdawg SDK...${NC}"
# Install getmethatdawg-sdk
python3.11 -m pip install --target "$GETMETHATDAWG_HOME/lib/python" ./getmethatdawg-sdk/
python3.11 -m pip install --target "$GETMETHATDAWG_HOME/lib/python" flask gunicorn

echo -e "${BLUE}Installing getmethatdawg CLI...${NC}"
# Create the getmethatdawg executable
cat > "$GETMETHATDAWG_BIN/getmethatdawg" << EOF
#!/bin/bash

# getmethatdawg - Zero-config deploy for Python agents
# Local installation version

set -euo pipefail

# Set up Python path
export PYTHONPATH="$GETMETHATDAWG_HOME/lib/python:\$PYTHONPATH"
export GETMETHATDAWG_HOME="$GETMETHATDAWG_HOME"
export GETMETHATDAWG_LIBEXEC="$GETMETHATDAWG_HOME/libexec"

# Source the main script
exec "\$GETMETHATDAWG_HOME/libexec/getmethatdawg-main.sh" "\$@"
EOF

chmod +x "$GETMETHATDAWG_BIN/getmethatdawg"

# Copy the main script
cp bin/getmethatdawg "$GETMETHATDAWG_HOME/libexec/getmethatdawg-main.sh"
chmod +x "$GETMETHATDAWG_HOME/libexec/getmethatdawg-main.sh"

# Copy libexec
cp -r libexec/* "$GETMETHATDAWG_HOME/libexec/" 2>/dev/null || true

echo -e "${GREEN}✅ getmethatdawg installed successfully!${NC}"
echo ""
echo -e "${YELLOW}Important:${NC} Add $GETMETHATDAWG_BIN to your PATH:"
echo "echo 'export PATH=\"$GETMETHATDAWG_BIN:\$PATH\"' >> ~/.zshrc"
echo "source ~/.zshrc"
echo ""
echo "Or for this session only:"
echo "export PATH=\"$GETMETHATDAWG_BIN:\$PATH\""
echo ""
echo "Test with: getmethatdawg --version" 