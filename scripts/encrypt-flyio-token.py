#!/usr/bin/env python3
"""
Encrypt Fly.io token for secure embedding in getmethatdawg authenticated builder.
This script is used privately to generate encrypted tokens.

Usage:
    python3 encrypt-flyio-token.py YOUR_FLY_API_TOKEN
"""

import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt_token(token):
    """Encrypt a Fly.io token using the same key derivation as the auth script."""
    
    # Same key derivation as in auth-setup.sh
    decrypt_key = "getmethatdawg-deploy-key-v1"
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'getmethatdawg-salt',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(decrypt_key.encode()))
    fernet = Fernet(key)
    
    # Encrypt the token
    encrypted_token = fernet.encrypt(token.encode())
    return encrypted_token.decode()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 encrypt-flyio-token.py YOUR_FLY_API_TOKEN")
        print("\nThis script encrypts your Fly.io token for secure embedding in the Docker container.")
        print("Keep this script private and never commit the output to public repos.")
        sys.exit(1)
    
    token = sys.argv[1]
    
    if not token.startswith('fly_'):
        print("Warning: Token doesn't look like a Fly.io token (should start with 'fly_')")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    encrypted_token = encrypt_token(token)
    
    print("✅ Token encrypted successfully!")
    print("\n" + "="*60)
    print("ENCRYPTED TOKEN (use this in Docker build):")
    print("="*60)
    print(encrypted_token)
    print("="*60)
    print("\nTo build the authenticated container:")
    print(f"docker build -f Dockerfile.authenticated-builder --build-arg FLY_API_TOKEN_ENCRYPTED='{encrypted_token}' -t getmethatdawg/builder:authenticated .")
    print("\nTo push to GitHub Container Registry:")
    print("docker tag getmethatdawg/builder:authenticated ghcr.io/dwij1704/getmethatdawg-builder:authenticated")
    print("docker push ghcr.io/dwij1704/getmethatdawg-builder:authenticated")

if __name__ == "__main__":
    main() 