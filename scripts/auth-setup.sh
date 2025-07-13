#!/bin/bash

# Auth setup script for getmethatdawg authenticated builder
# This script decrypts the Fly.io token and authenticates flyctl

set -euo pipefail

# Decryption key (this could be derived from multiple sources for security)
DECRYPT_KEY="getmethatdawg-deploy-key-v1"

# Function to decrypt the Fly.io token
decrypt_token() {
    if [[ -n "${FLY_API_TOKEN_ENCRYPTED:-}" ]]; then
            # Use Python to decrypt the token
    python3 -c "
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Derive key from decrypt key
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'getmethatdawg-salt',
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(os.environ['DECRYPT_KEY'].encode()))
fernet = Fernet(key)

# Decrypt the token
encrypted_token = os.environ['FLY_API_TOKEN_ENCRYPTED']
token = fernet.decrypt(encrypted_token.encode()).decode()
print(token)
"
    else
        echo ""
    fi
}

# Authenticate with Fly.io if token is available
if [[ -n "${FLY_API_TOKEN_ENCRYPTED:-}" ]]; then
    echo "🔐 Authenticating with Fly.io..."
    
    # Decrypt the token
    FLY_API_TOKEN=$(decrypt_token)
    
    if [[ -n "$FLY_API_TOKEN" ]]; then
        # Set the token for flyctl
        export FLY_API_TOKEN
        
        # Verify authentication
        if flyctl auth whoami &>/dev/null; then
            echo "✅ Fly.io authentication successful"
        else
            echo "⚠️ Fly.io authentication failed, but continuing..."
        fi
    else
        echo "⚠️ Failed to decrypt Fly.io token"
    fi
else
    echo "⚠️ No Fly.io token provided, deployments may fail"
fi

# Execute the original command
exec "$@" 