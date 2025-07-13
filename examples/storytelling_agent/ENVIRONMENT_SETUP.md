# Environment Variables Setup Guide

This guide shows you how to set up environment variables for the CrewAI Content Creation Agent.

## Quick Setup

1. **Create a .env file** in the `storytelling_agent` directory:
   ```bash
   cd examples/storytelling_agent
   touch .env
   ```

2. **Add your API keys** to the `.env` file:
   ```bash
   # Required: At least one API key for real AI responses
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   
   # Optional: Model preferences
   OPENAI_MODEL_NAME=gpt-4o-mini
   ANTHROPIC_MODEL_NAME=claude-3-sonnet-20240229
   GROQ_MODEL_NAME=mixtral-8x7b-32768
   
   # Optional: Additional configurations
   CONTENT_GENERATION_TIMEOUT=120
   DEFAULT_CONTENT_TYPE=blog_post
   MAX_CONTENT_LENGTH=2000
   ```

3. **Deploy with automatic secrets management**:
   ```bash
   getmethatdawg deploy ai_content_crew.py --auto-detect
   ```

## How It Works

The getmethatdawg deployment system will:
1. 🔍 **Auto-detect** your `.env` file
2. 🔐 **Categorize** environment variables (secrets vs regular config)
3. 📝 **Generate** a deployment script with proper secrets handling
4. 🚀 **Deploy** using Fly.io's secure secrets management

## Environment Variable Types

### Secrets (Handled Securely)
These are automatically detected and set as Fly.io secrets:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GROQ_API_KEY`
- Any variable containing: `API_KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`

### Regular Environment Variables
These are set as regular environment variables:
- `OPENAI_MODEL_NAME`
- `ANTHROPIC_MODEL_NAME`
- `GROQ_MODEL_NAME`
- `CONTENT_GENERATION_TIMEOUT`
- `DEFAULT_CONTENT_TYPE`
- `MAX_CONTENT_LENGTH`

## Getting API Keys

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Anthropic API Key
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account or sign in
3. Navigate to API keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Groq API Key
1. Go to [Groq Console](https://console.groq.com/)
2. Create an account or sign in
3. Navigate to API keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Demo Mode vs Production

### Without API Keys (Demo Mode)
- ✅ Deployment works immediately
- ✅ All endpoints respond with mock data
- ✅ Fast response times
- ❌ No real AI-generated content

### With API Keys (Production Mode)
- ✅ Real AI-powered content generation
- ✅ High-quality, relevant content
- ✅ All 4 CrewAI agents working together
- ⏱️ Longer response times (30-60 seconds)
- 💰 Uses API credits

## Security Notes

- ✅ **Secrets are secure**: API keys are stored as Fly.io secrets, not in environment variables
- ✅ **Not logged**: Secrets don't appear in deployment logs
- ✅ **Encrypted**: Secrets are encrypted at rest
- ✅ **Access controlled**: Only your app can access its secrets

## Troubleshooting

### No API Keys Available
```bash
# Check which API keys are set
curl https://your-app.fly.dev/get-environment-status
```

### Missing .env File
```bash
# Verify .env file exists
ls -la examples/storytelling_agent/.env

# Check .env file contents (be careful not to expose secrets!)
head -5 examples/storytelling_agent/.env
```

### Deployment Issues
```bash
# Check deployment logs
flyctl logs -a your-app-name

# Check app status
flyctl status -a your-app-name
```

## Example .env File

Create `examples/storytelling_agent/.env`:
```bash
# Minimal setup (choose one)
OPENAI_API_KEY=sk-proj-...your-key-here

# Or comprehensive setup
OPENAI_API_KEY=sk-proj-...your-openai-key
ANTHROPIC_API_KEY=sk-ant-...your-anthropic-key
GROQ_API_KEY=gsk_...your-groq-key
OPENAI_MODEL_NAME=gpt-4o-mini
ANTHROPIC_MODEL_NAME=claude-3-sonnet-20240229
GROQ_MODEL_NAME=mixtral-8x7b-32768
```

## Verification

After deployment, verify your setup:
```bash
# Check environment status
curl https://your-app.fly.dev/get-environment-status

# Test content generation
curl -X POST https://your-app.fly.dev/generate-content \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test content", "content_type": "blog_post"}'
```

This setup ensures your API keys are handled securely while providing a seamless deployment experience! 