<div align="center">
  <img src="assets/getmethatdawg-logo.png" alt="GetMeThatDawg Logo" width="300"/>
  
  # 🚀 GetMeThatDawg - Zero-Config AI Agent Deployment

  **Deploy Python AI agents as live web services with a single command - no decorators, no configuration, no hassle.**

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)
  [![Fly.io](https://img.shields.io/badge/deploy-fly.io-purple.svg)](https://fly.io/)
  
  🔥 **NEW: Pre-Authenticated Deployment Mode** - Deploy without installing flyctl!
</div>

## ✨ What is GetMeThatDawg?

GetMeThatDawg transforms any Python file with functions into a production-ready web API, automatically detecting endpoints and managing secrets. Perfect for AI agents, data science models, and Python automation scripts.

### 🔥 **NEW: Pre-Authenticated Deployment Mode**

Deploy with **zero setup** - no flyctl installation required! Perfect for enterprise environments, CI/CD pipelines, and simplified workflows.

```bash
# Just write Python functions
def generate_content(topic: str, style: str = "professional"):
    return {"content": f"Generated content about {topic}"}

# Deploy with pre-authenticated mode (RECOMMENDED)
getmethatdawg deploy my_agent.py --pre-auth

# Get live API instantly - no flyctl needed!
# ✅ https://my-agent.fly.dev/generate-content
```

### 🚀 **Two Deployment Modes**

| Mode | Command | Requirements | Best For |
|------|---------|-------------|----------|
| 🔥 **Pre-Auth** | `--pre-auth` | Docker only | Enterprise, CI/CD, Simplified workflows |
| 🛠️ **Regular** | (default) | Docker + flyctl | Local development, Full control |

## 🎯 Key Features

### 🔥 **Pre-Authenticated Mode (NEW)**
- **⚡ Zero Setup** - Deploy without installing flyctl or managing tokens
- **🏢 Enterprise Ready** - Perfect for restricted environments and CI/CD
- **🔐 Encrypted Credentials** - Secure token embedding with Fernet encryption
- **🤖 Smart Fallback** - Automatically falls back to regular mode if needed

### 🚀 **Core Features**
- **🔍 Auto-Detection** - No decorators needed, automatically detects functions as API endpoints
- **🔐 Seamless Secrets** - Automatic `.env` file handling with encrypted secrets management
- **🤖 AI-Ready** - Perfect for CrewAI, LangChain, and other AI frameworks
- **⚡ Zero Config** - From Python file to live API in one command
- **🛡️ Production Ready** - Secure, scalable deployments on Fly.io
- **📊 Built-in Monitoring** - Health checks and status endpoints included

## 🚀 Quick Start

### Installation

#### via Homebrew (Recommended)
```bash
brew tap Dwij1704/getmethatdawg
brew install getmethatdawg
```

#### Manual Installation
```bash
git clone https://github.com/Dwij1704/getmethatdawg.git
cd getmethatdawg
make install
```

### 🔥 **Pre-Authenticated Mode (Recommended)**

**Zero setup required** - just install and deploy!

```bash
# 1. Install getmethatdawg
brew install Dwij1704/getmethatdawg

# 2. Deploy with pre-auth mode
getmethatdawg deploy my_agent.py --pre-auth

# 3. That's it! Your API is live
# ✅ https://my-agent.fly.dev/
```

**Perfect for:**
- 🏢 Enterprise environments with restricted tooling
- 🔄 CI/CD pipelines and automated deployments  
- ⚡ Quick demos and prototypes
- 🛡️ Teams preferring containerized deployments

### 🛠️ **Regular Mode**

For users who prefer full control and have flyctl installed:

```bash
# Install flyctl first
curl -L https://fly.io/install.sh | sh

# Deploy with regular mode
getmethatdawg deploy my_agent.py
```

### Deploy Your First Agent

1. **Create a Python file** with functions:
```python
# my_agent.py
def hello_world(name: str = "World"):
    """Say hello to someone"""
    return {"message": f"Hello, {name}!"}

def analyze_data(data: list, method: str = "mean"):
    """Analyze data using specified method"""
    if method == "mean":
        return {"result": sum(data) / len(data)}
    return {"result": "Method not supported"}
```

2. **Deploy with pre-auth mode (recommended)**:
```bash
getmethatdawg deploy my_agent.py --pre-auth --auto-detect
```

3. **Get live API endpoints**:
```bash
✅ Deployed to: https://my-agent.fly.dev
📡 Available endpoints:
  GET  /hello-world
  POST /analyze-data
```

## 🤖 AI Agent Examples

### CrewAI Multi-Agent System
Deploy a complete 4-agent content creation system:

```python
# ai_content_crew.py
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

def create_content_request(topic: str, content_type: str = "blog_post"):
    """Create content using 4 AI agents: Research → Write → Edit → SEO"""
    # ... CrewAI implementation
    return {"content": "Generated content...", "seo_score": 95}

def get_environment_status():
    """Check which AI services are available"""
    return {
        "openai_available": bool(os.getenv('OPENAI_API_KEY')),
        "status": "production"
    }
```

```bash
# Add API keys to .env file
echo "OPENAI_API_KEY=sk-..." > .env
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env

# Deploy with pre-auth mode and automatic secrets management
getmethatdawg deploy ai_content_crew.py --pre-auth --auto-detect

# ✅ Live API with encrypted secrets
# ✅ 10 endpoints auto-detected
# ✅ Production-ready in 60 seconds
```

## 🔐 Environment Management

GetMeThatDawg automatically handles environment variables and secrets:

```bash
# .env file in your project
OPENAI_API_KEY=sk-proj-your-key-here     # → Encrypted secret
ANTHROPIC_API_KEY=sk-ant-your-key        # → Encrypted secret
MODEL_NAME=gpt-4o-mini                   # → Environment variable
DEBUG=false                              # → Environment variable
```

**Smart categorization:**
- 🔐 **Secrets**: `API_KEY`, `TOKEN`, `SECRET`, `PASSWORD` → Encrypted
- 🌍 **Environment**: Configuration values → Regular env vars

## 📊 Auto-Detection Intelligence

GetMeThatDawg automatically detects functions as API endpoints using intelligent analysis:

```python
# GET endpoints (data retrieval)
def get_user_profile(user_id: str):
    return {"user": "data"}

def list_items():
    return {"items": []}

# POST endpoints (actions/multiple params)  
def create_user(name: str, email: str, role: str = "user"):
    return {"user_id": "12345"}

def process_data(data: list, algorithm: str, threshold: float):
    return {"results": "processed"}
```

**Generates:**
- `GET /get-user-profile?user_id=123`
- `GET /list-items`
- `POST /create-user` with JSON body
- `POST /process-data` with JSON body

## 🛠️ Advanced Usage

### Custom Configuration
```bash
# Specify custom app name
getmethatdawg deploy my_agent.py --pre-auth --auto-detect --name my-custom-app

# Deploy to specific region
getmethatdawg deploy my_agent.py --pre-auth --auto-detect --region ord

# Use different requirements file
getmethatdawg deploy my_agent.py --pre-auth --auto-detect --requirements custom-requirements.txt
```

### API Testing
```bash
# Built-in API test suite
./examples/storytelling_agent/test_api_sequence.sh

# Demo workflow
./examples/storytelling_agent/demo_api_workflow.sh

# Import Postman collection
# Import: examples/storytelling_agent/CrewAI_Content_Agent_Postman_Collection.json
```

## 📁 Project Structure

```
getmethatdawg/
├── bin/getmethatdawg           # Main CLI command
├── getmethatdawg-sdk/          # Python SDK and builder
├── examples/                   # Example applications
│   ├── storytelling_agent/     # CrewAI multi-agent example
│   └── simple_agent/           # Basic example
├── docs/                       # Documentation
├── scripts/                    # Installation scripts
└── homebrew/                   # Homebrew formula
```

## 🧪 Examples

### 1. Simple API
```python
def calculate(operation: str, a: float, b: float):
    if operation == "add": return {"result": a + b}
    if operation == "multiply": return {"result": a * b}
    return {"error": "Unsupported operation"}
```

### 2. Data Science Model
```python
import pandas as pd
from sklearn.model_selection import train_test_split

def train_model(dataset: str, target_column: str):
    """Train ML model on provided dataset"""
    # Load and process data
    return {"model_id": "abc123", "accuracy": 0.95}

def predict(model_id: str, features: dict):
    """Make predictions using trained model"""
    return {"prediction": 42, "confidence": 0.89}
```

### 3. AI Content Generator
```python
from openai import OpenAI

def generate_content(prompt: str, style: str = "professional"):
    """Generate content using OpenAI"""
    client = OpenAI()  # Uses OPENAI_API_KEY from env
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"content": response.choices[0].message.content}
```

## 🚀 Deployment Targets

- **Fly.io** (default) - Global edge deployment
- **Docker** - Local and cloud deployment  
- **Kubernetes** - Enterprise deployment (coming soon)
- **AWS Lambda** - Serverless deployment (coming soon)

## 🔧 Requirements

### Pre-Auth Mode (Recommended)
- **Python 3.11+**
- **Docker** (for building)

### Regular Mode
- **Python 3.11+**
- **Docker** (for building)
- **Fly.io CLI** (for deployment)

## 📚 Documentation

- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Complete deployment documentation
- **[API Usage Guide](examples/storytelling_agent/API_USAGE_GUIDE.md)** - How to use deployed APIs
- **[Environment Setup](examples/storytelling_agent/ENVIRONMENT_SETUP.md)** - Environment configuration
- **[Examples](examples/)** - Real-world examples and tutorials

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Dwij1704/getmethatdawg&type=Date)](https://star-history.com/#Dwij1704/getmethatdawg&Date)

## 🎉 Showcase

### Success Stories
- **AI Content Agency** - Deployed 50+ CrewAI agents serving 10k+ requests/day
- **Data Science Team** - Turned Jupyter notebooks into production APIs in minutes
- **Startup MVP** - Launched AI-powered product in 24 hours

## 🔥 Pre-Authenticated Mode Deep Dive

### What is Pre-Authenticated Mode?

Pre-authenticated mode is a revolutionary deployment approach that eliminates the need for flyctl installation and token management. Instead of requiring users to install and authenticate with flyctl, getmethatdawg uses pre-built Docker containers with encrypted credentials embedded securely.

### 🚀 Key Benefits

| Feature | Pre-Auth Mode | Regular Mode |
|---------|---------------|--------------|
| **Setup Time** | 0 minutes | 5-10 minutes |
| **Dependencies** | Docker only | Docker + flyctl |
| **Enterprise Ready** | ✅ Perfect for restricted environments | ⚠️ Requires flyctl installation |
| **CI/CD Ready** | ✅ Zero configuration | ⚠️ Requires secret management |
| **Security** | ✅ Encrypted credentials in container | ✅ Local flyctl authentication |
| **Fallback** | ✅ Auto-falls back to regular mode | ❌ No fallback |

### 🛡️ Security Model

Pre-auth mode uses enterprise-grade security:

- **Fernet Encryption** - Industry-standard symmetric encryption
- **PBKDF2 Key Derivation** - 100,000 iterations for key strengthening
- **Container Isolation** - Credentials never stored in plaintext
- **Token Rotation** - Easy credential updates via container rebuilds

### 🏢 Perfect for Enterprise

- **Restricted Environments** - Deploy without installing additional tools
- **CI/CD Pipelines** - Zero-setup automated deployments
- **Security Compliance** - No plaintext credentials in repositories
- **Team Scalability** - One-time setup, unlimited deployments

### 🔄 Smart Fallback

If pre-authenticated container isn't available, getmethatdawg automatically falls back to regular mode:

```bash
getmethatdawg deploy my_agent.py --pre-auth
# ✅ Tries pre-auth first
# ✅ Falls back to regular mode if needed
# ✅ Zero disruption to workflow
```

### Environment Variables

For AI agents that require API keys, create a `.env` file in your project directory:

```bash
# Copy the template and fill in your values
cp examples/.env.template .env
```

Common environment variables:
- `OPENAI_API_KEY` - OpenAI API key for GPT models
- `CREWAI_API_KEY` - CrewAI API key (if using CrewAI)
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude models

**Security Note**: Never commit `.env` files to version control. They are automatically ignored by getmethatdawg.

### Community Examples
- [AI Writing Assistant](examples/writing_assistant/) - GPT-powered content generator
- [Data Analysis API](examples/data_analysis/) - Pandas/NumPy data processing
- [Image Recognition Service](examples/image_recognition/) - Computer vision API

---

## 🔥 Ready to Deploy? Try Pre-Auth Mode!

**Skip the setup, start deploying immediately:**

```bash
# 1. Install getmethatdawg
brew install Dwij1704/getmethatdawg

# 2. Deploy with zero configuration
getmethatdawg deploy your_agent.py --pre-auth

# 3. Your API is live! 🚀
```

**Perfect for:**
- 🏢 **Enterprise teams** - No flyctl installation required
- 🔄 **CI/CD pipelines** - Zero-setup automated deployments
- ⚡ **Quick prototypes** - From idea to API in minutes
- 🛡️ **Security-first** - Encrypted credentials, no plaintext storage

**Try it today and experience deployment without friction!**

---

**Made with ❤️ for Python developers who want to focus on building, not deploying.**

[⭐ Star us on GitHub](https://github.com/Dwij1704/getmethatdawg) | [📖 Read the Docs](https://getmethatdawg.dev)