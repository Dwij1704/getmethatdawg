# GetMeThatDawg - No flyctl Setup

This guide explains how to eliminate the flyctl dependency by using a pre-authenticated Docker container that deploys to your Fly.io account automatically.

## 🎯 Benefits

- **Users only need Docker** - no flyctl installation required
- **No Fly.io account setup** - deployments go to your account automatically  
- **Secure credentials** - encrypted and embedded in container
- **Same user experience** - `getmethatdawg deploy my_file.py` just works

## 🔧 Setup Process

### 1. Get Your Fly.io API Token

```bash
# If you don't have flyctl installed:
flyctl auth token

# The token will look like: fly_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Encrypt Your Token

```bash
# Install dependencies
pip install cryptography

# Encrypt your token (keep this private!)
python3 scripts/encrypt-flyio-token.py fly_your_actual_token_here
```

This outputs an encrypted token like:
```
gAAAAABhxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Build the Authenticated Container

```bash
# Build with your encrypted token
docker build -f Dockerfile.authenticated-builder \
  --build-arg FLY_API_TOKEN_ENCRYPTED='gAAAAABhxxxxxxxxxxxxxxxxxxxxx' \
  -t getmethatdawg/builder:authenticated .
```

### 4. Push to Container Registry

**Option A: GitHub Container Registry (Recommended)**
```bash
# Tag for GitHub Container Registry
docker tag getmethatdawg/builder:authenticated ghcr.io/dwij1704/getmethatdawg-builder:authenticated

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u dwij1704 --password-stdin

# Push
docker push ghcr.io/dwij1704/getmethatdawg-builder:authenticated
```

**Option B: Docker Hub**
```bash
# Tag for Docker Hub
docker tag getmethatdawg/builder:authenticated getmethatdawg/builder:authenticated

# Login and push
docker login
docker push getmethatdawg/builder:authenticated
```

### 5. Update getmethatdawg Binary

Replace the main `bin/getmethatdawg` with `bin/getmethatdawg-no-flyctl` and update the homebrew formula.

## 🔐 Security Model

### Encryption Details
- **Algorithm**: Fernet (AES 128 with HMAC)
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Salt**: Static salt for deterministic key generation
- **Key**: Derived from hardcoded string in both encrypt/decrypt scripts

### Security Considerations
- ✅ **Credentials not in public repo** - only encrypted token in container
- ✅ **Token rotation** - rebuild container with new token as needed
- ✅ **No plaintext storage** - token only decrypted at runtime
- ⚠️ **Container access** - anyone with container access could theoretically extract token
- ⚠️ **Key hardcoded** - encryption key is in public code (acceptable for this use case)

### Threat Model
- **Protects against**: Accidental exposure, casual browsing of public repos
- **Does not protect against**: Determined attackers with container access
- **Acceptable because**: Fly.io tokens can be scoped and rotated, deployments are to your account anyway

## 🚀 User Experience

Once set up, users can deploy without any Fly.io setup:

```bash
# Only requirement: Docker
brew install docker

# Install getmethatdawg (no flyctl needed!)
brew install dwij1704/getmethatdawg/getmethatdawg

# Deploy anything (goes to your Fly.io account)
getmethatdawg deploy my_agent.py --auto-detect
```

## 🔄 Token Rotation

To rotate your Fly.io token:

1. Generate new token: `flyctl auth token`
2. Encrypt new token: `python3 scripts/encrypt-flyio-token.py NEW_TOKEN`
3. Rebuild container with new encrypted token
4. Push updated container to registry
5. Users automatically get new token on next deployment

## 📝 Implementation Checklist

- [ ] Encrypt your Fly.io token using `scripts/encrypt-flyio-token.py`
- [ ] Build authenticated container with `Dockerfile.authenticated-builder`
- [ ] Push container to GitHub Container Registry or Docker Hub
- [ ] Test container works: `docker run --rm -v ./examples/simple_ai_crew.py:/tmp/source.py:ro getmethatdawg/builder:authenticated /tmp/source.py simple-ai-crew`
- [ ] Replace main binary with no-flyctl version
- [ ] Update homebrew formula to use new version
- [ ] Update documentation

## 🎯 Result

Users get the same amazing zero-config deployment experience, but with only Docker as a dependency. All deployments go to your Fly.io account seamlessly! 