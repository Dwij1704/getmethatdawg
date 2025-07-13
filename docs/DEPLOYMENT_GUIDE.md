# GetMeThatDawg Deployment Guide - Seamless Environment Management

This guide explains how to deploy Python applications with automatic environment variable and secrets management using the enhanced getmethatdawg deployment system.

## What's New - Seamless Environment Management

The getmethatdawg deployment system now automatically handles environment variables and secrets with zero configuration:

- 🔍 **Auto-detect** `.env` files in your project
- 🔐 **Secure secrets** management using Fly.io's encrypted secrets
- 📝 **Smart categorization** of environment variables vs secrets
- 🚀 **One-command deployment** with full environment setup

## Quick Start

1. **Create your Python application** with functions you want to expose
2. **Add a `.env` file** with your environment variables
3. **Deploy with one command**: `getmethatdawg deploy your_app.py --auto-detect`

That's it! No decorators, no manual configuration, no secrets management headaches.

## Environment Variables Management

### How It Works

The getmethatdawg system automatically:

1. **Searches for `.env` files** in your project directory
2. **Categorizes variables** into secrets vs regular environment variables
3. **Generates deployment scripts** that securely set secrets
4. **Deploys with proper security** using Fly.io's secrets management

### Variable Categories

#### 🔐 Secrets (Encrypted & Secure)
Variables containing these patterns are automatically treated as secrets:
- `API_KEY` (e.g., `OPENAI_API_KEY`)
- `TOKEN` (e.g., `ACCESS_TOKEN`)
- `SECRET` (e.g., `CLIENT_SECRET`)
- `PASSWORD` (e.g., `DB_PASSWORD`)
- `PRIVATE_KEY`, `CREDENTIAL`, `AUTH_KEY`

#### 🌍 Environment Variables (Regular)
All other variables are set as regular environment variables:
- `MODEL_NAME` (e.g., `OPENAI_MODEL_NAME`)
- `API_BASE` (e.g., `OPENAI_API_BASE`)
- `TIMEOUT`, `REGION`, `DEBUG`, etc.

### Example .env File

```bash
# API Keys (automatically secured as secrets)
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GROQ_API_KEY=gsk_your-key-here

# Configuration (regular environment variables)
OPENAI_MODEL_NAME=gpt-4o-mini
ANTHROPIC_MODEL_NAME=claude-3-sonnet-20240229
CONTENT_GENERATION_TIMEOUT=120
DEFAULT_CONTENT_TYPE=blog_post
DEBUG=false
```

## Deployment Process

### Basic Deployment

```bash
# Auto-detect endpoints and manage environment seamlessly
getmethatdawg deploy my_app.py --auto-detect
```

### What Happens Behind the Scenes

1. **🔍 Analysis Phase**
   - Scans your Python file for functions to expose
   - Reads your `.env` file
   - Categorizes environment variables

2. **🔐 Security Phase**
   - Generates deployment script with secrets management
   - Creates secure configuration files
   - Prepares Fly.io deployment artifacts

3. **🚀 Deployment Phase**
   - Sets secrets securely using `flyctl secrets set`
   - Deploys your application
   - Provides live URL and endpoint information

### Example Output

```bash
$ getmethatdawg deploy ai_content_crew.py --auto-detect

🔍 Auto-detecting endpoints...
✅ Auto-detected: GET /get-crew-info -> get_crew_info
✅ Auto-detected: POST /generate-content -> generate_content
✅ Auto-detected: GET /get-environment-status -> get_environment_status
🎯 Found 10 potential endpoints

✅ Loaded 6 environment variables from .env
✅ Generated secrets file with 3 secrets
✅ Generated deployment script: deploy-with-secrets.sh

🔐 Setting up secrets for deployment...
✅ All secrets staged. Deploying with secrets...
✅ Pushed to Fly.io
🌐 https://ai-content-crew.fly.dev
```

## CrewAI Example - Complete Workflow

Here's how to deploy the advanced CrewAI content creation agent:

### 1. Setup Environment

```bash
cd examples/storytelling_agent
```

### 2. Create .env File

```bash
# Get API keys from:
# - OpenAI: https://platform.openai.com/
# - Anthropic: https://console.anthropic.com/
# - Groq: https://console.groq.com/

cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
ANTHROPIC_MODEL_NAME=claude-3-sonnet-20240229
GROQ_MODEL_NAME=mixtral-8x7b-32768
EOF
```

### 3. Deploy with One Command

```bash
getmethatdawg deploy ai_content_crew.py --auto-detect
```

### 4. Test the Deployment

```bash
# Run the comprehensive test suite
./test_api_sequence.sh

# Or test manually
curl https://your-app.fly.dev/get-environment-status
```

## API Usage Examples

### Check System Status

```bash
# Health check
curl https://your-app.fly.dev/

# Environment status
curl https://your-app.fly.dev/get-environment-status
```

### Generate Content

```bash
curl -X POST https://your-app.fly.dev/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI in Healthcare",
    "content_type": "blog_post",
    "target_audience": "healthcare professionals",
    "tone": "professional",
    "word_count": 1500,
    "keywords": ["AI", "healthcare", "machine learning"]
  }'
```

### SEO Optimization

```bash
curl -X POST https://your-app.fly.dev/optimize-content-seo \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your content here...",
    "target_keywords": ["keyword1", "keyword2"],
    "target_audience": "developers"
  }'
```

## Security Features

### ✅ What's Secure

- **Encrypted secrets**: API keys are stored using Fly.io's encrypted secrets
- **No logs**: Secrets don't appear in deployment logs or configuration files
- **Access control**: Only your deployed app can access its secrets
- **Environment isolation**: Each deployment has its own secure environment

### ❌ What's Not Exposed

- Secrets never appear in generated `fly.toml` files
- Environment variables are clearly separated from secrets
- No plaintext storage of sensitive data
- Secrets are not visible in Docker images

## Troubleshooting

### Missing .env File

```bash
# Check if .env exists
ls -la .env

# Example .env creation
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Secrets Not Set

```bash
# Check secrets status
flyctl secrets list -a your-app-name

# Manually set a secret if needed
flyctl secrets set OPENAI_API_KEY=your-key -a your-app-name
```

### Demo Mode vs Production

```bash
# Check if running in demo mode
curl https://your-app.fly.dev/get-environment-status

# Response shows API key availability
{
  "status": "success",
  "data": {
    "openai_available": true,
    "anthropic_available": false,
    "groq_available": true,
    "demo_mode": false
  }
}
```

### Deployment Issues

```bash
# Check app logs
flyctl logs -a your-app-name

# Check app status
flyctl status -a your-app-name

# Restart app
flyctl restart -a your-app-name
```

## Advanced Features

### Custom Deployment Scripts

The system generates `deploy-with-secrets.sh` scripts that you can customize:

```bash
# Generated script handles secrets automatically
./deploy-with-secrets.sh

# Or deploy manually
flyctl deploy --remote-only
```

### Multiple Environments

```bash
# Development environment
cp .env .env.dev
getmethatdawg deploy app.py --auto-detect

# Production environment
cp .env.prod .env
getmethatdawg deploy app.py --auto-detect
```

### Environment Validation

```bash
# Check which variables are detected
getmethatdawg deploy app.py --auto-detect --dry-run  # (future feature)
```

## Best Practices

### 1. Environment Variables Organization

```bash
# Group by service
OPENAI_API_KEY=...
OPENAI_MODEL_NAME=...
OPENAI_API_BASE=...

ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL_NAME=...

# Use consistent naming
SERVICE_API_KEY=...
SERVICE_MODEL_NAME=...
SERVICE_TIMEOUT=...
```

### 2. Security

- ✅ Use `.env` files for local development
- ✅ Add `.env` to `.gitignore`
- ✅ Use different API keys for different environments
- ✅ Rotate API keys regularly

### 3. Testing

```bash
# Test in demo mode first
getmethatdawg deploy app.py --auto-detect  # without .env

# Add API keys for production testing
echo "OPENAI_API_KEY=..." > .env
getmethatdawg deploy app.py --auto-detect
```

## Migration from Manual Setup

### Old Way (Manual Decorators)

```python
import getmethatdawg

@getmethatdawg.expose(method="POST", path="/generate")
def generate_content(topic: str):
    return {"content": f"Generated content about {topic}"}
```

### New Way (Auto-Detection)

```python
def generate_content(topic: str):
    """Generate content about a given topic"""
    return {"content": f"Generated content about {topic}"}
```

Deploy with: `getmethatdawg deploy app.py --auto-detect`

## Integration Examples

### Python SDK

```python
import requests
import os

# Use the deployed endpoint
response = requests.post(
    'https://your-app.fly.dev/generate-content',
    json={
        "topic": "Machine Learning",
        "content_type": "blog_post",
        "target_audience": "developers"
    }
)
content = response.json()
```

### JavaScript/Node.js

```javascript
const response = await fetch('https://your-app.fly.dev/generate-content', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        topic: 'AI Ethics',
        content_type: 'article',
        target_audience: 'general'
    })
});
const content = await response.json();
```

## Support

- **Documentation**: Check `API_USAGE_GUIDE.md` for detailed API usage
- **Environment Setup**: See `ENVIRONMENT_SETUP.md` for environment configuration
- **Testing**: Run `test_api_sequence.sh` for comprehensive testing
- **Issues**: Check deployment logs with `flyctl logs -a your-app-name`

## Conclusion

The enhanced getmethatdawg deployment system provides:

- 🚀 **Zero-configuration deployment** of Python applications
- 🔐 **Automatic secrets management** for API keys and sensitive data
- 🎯 **Smart endpoint detection** without manual decorators
- 📱 **Production-ready** applications with proper security
- 🔄 **Seamless workflow** from development to deployment

Deploy your AI agents, APIs, and Python applications with confidence - getmethatdawg handles the complexity while you focus on building amazing applications! 