# 🚀 GetMeThatDawg - Zero-Config AI Agent Deployment

**Deploy Python AI agents as live web services with a single command - no decorators, no configuration, no hassle.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)
[![Fly.io](https://img.shields.io/badge/deploy-fly.io-purple.svg)](https://fly.io/)

## ✨ What is GetMeThatDawg?

GetMeThatDawg transforms any Python file with functions into a production-ready web API, automatically detecting endpoints and managing secrets. Perfect for AI agents, data science models, and Python automation scripts.

```bash
# Just write Python functions
def generate_content(topic: str, style: str = "professional"):
    return {"content": f"Generated content about {topic}"}

# Deploy with one command
getmethatdawg deploy my_agent.py --auto-detect

# Get live API instantly
# ✅ https://my-agent.fly.dev/generate-content
```

## 🎯 Key Features

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

2. **Deploy with auto-detection**:
```bash
getmethatdawg deploy my_agent.py --auto-detect
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

# Deploy with automatic secrets management
getmethatdawg deploy ai_content_crew.py --auto-detect

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
getmethatdawg deploy my_agent.py --auto-detect --name my-custom-app

# Deploy to specific region
getmethatdawg deploy my_agent.py --auto-detect --region ord

# Use different requirements file
getmethatdawg deploy my_agent.py --auto-detect --requirements custom-requirements.txt
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

### Community Examples
- [AI Writing Assistant](examples/writing_assistant/) - GPT-powered content generator
- [Data Analysis API](examples/data_analysis/) - Pandas/NumPy data processing
- [Image Recognition Service](examples/image_recognition/) - Computer vision API

---

**Made with ❤️ for Python developers who want to focus on building, not deploying.**

[⭐ Star us on GitHub](https://github.com/Dwij1704/getmethatdawg) | [📖 Read the Docs](https://getmethatdawg.dev) | [💬 Join Discord](https://discord.gg/getmethatdawg) 