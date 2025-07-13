# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

## [0.0.1] - 2024-12-07

### Added
- 🚀 **Zero-Config Python Agent Deployment**
  - Deploy Python functions as web APIs with a single command
  - Auto-detection of functions as endpoints (no decorators needed)
  - Dual deployment modes: Regular (flyctl) and Pre-authenticated (Docker only)
  - Interactive setup for requirements.txt and .env files
  - Comprehensive secrets management with automatic categorization

- 🔧 **Enhanced Pre-Auth Mode**
  - Pre-authenticated container deployment with encrypted credentials
  - End-to-end deployment logs just like regular mode
  - Real-time streaming of deployment progress and flyctl output
  - Live deployment status, app creation, secrets setup, and final URLs
  - Smart fallback to regular mode if pre-auth container unavailable

- 📊 **CrewAI and AI Framework Support**
  - Complete CrewAI multi-agent example with content creation workflow
  - Support for OpenAI, Anthropic, Groq, and other LLM providers
  - Automatic environment variable detection and setup
  - Production-ready AI agent deployment examples

- 🛠️ **Developer Experience**
  - Homebrew installation support
  - Comprehensive documentation and examples
  - Interactive prompts for missing dependencies
  - Deployment preview with endpoint listing
  - Error handling and debugging tools

### Changed
- Initial release

### Fixed
- Initial release

## [1.2.0] - 2024-12-07

### Added
- 🚀 **Dual Deployment Modes**
  - **Regular Mode** (default): Uses flyctl + your Fly.io account (existing behavior)
  - **Pre-authenticated Mode** (`--pre-auth`): Uses pre-authenticated container, no flyctl needed
  - Smart fallback: If pre-auth container unavailable, falls back to regular mode

- 🔧 **Enhanced Command Line Interface**
  - New flag: `--pre-auth` for pre-authenticated deployments
  - Environment variable: `GETMETHATDAWG_MODE=pre-auth` to default to pre-auth mode
  - Improved help text with clear mode explanations and examples
  - Better error messages with suggestions for missing dependencies

- 🐳 **Pre-authenticated Container Support**
  - Secure encrypted credential embedding using Fernet encryption
  - GitHub Container Registry and Docker Hub support
  - Automatic container pulling and fallback mechanisms
  - Zero user setup required for pre-auth mode

- 🛠️ **Setup Tools**
  - `scripts/encrypt-flyio-token.py` - Secure token encryption utility
  - `scripts/setup-no-flyctl.sh` - Automated setup for pre-auth mode
  - `Dockerfile.authenticated-builder` - Pre-authenticated container builder
  - `docs/NO_FLYCTL_SETUP.md` - Complete implementation guide

### Changed
- 📦 **Homebrew Formula**
  - flyctl dependency now optional (only needed for regular mode)
  - Updated help text and caveats to explain both modes
  - Separate deployment scripts for regular and pre-auth modes
  - Improved error messages for missing dependencies

- 🎯 **User Experience**
  - Same commands work in both modes: `getmethatdawg deploy my_file.py`
  - Clear mode indication in output logs
  - Environment detection for optimal experience
  - Backwards compatible - existing usage continues to work

### Technical Improvements
- **Argument Parsing**: Robust parsing for multiple flags and options
- **Container Management**: Smart image pulling with registry fallbacks  
- **Error Handling**: Graceful degradation and helpful error messages
- **Security**: Encrypted credentials with PBKDF2 key derivation
- **Documentation**: Comprehensive setup and usage guides

### Dependencies
- **Regular Mode**: Docker + flyctl (unchanged)
- **Pre-auth Mode**: Docker only (new option)
- **SDK**: No changes to existing SDK usage

## [1.1.2] - 2024-12-07

### Fixed
- 🐛 **Critical Bug Fixes**
  - Fixed unbound variable error in cleanup function during deployment
  - Fixed homebrew version argument parsing issue (circular sourcing bug)
  - Improved error handling in bash strict mode for better reliability

### Technical Improvements
- **Cleanup Handling**: Added proper variable checks in cleanup function
- **Homebrew Stability**: Fixed circular sourcing issue causing argument parsing failures
- **Error Resilience**: Better handling of edge cases in deployment cleanup

## [1.1.1] - 2024-12-07

### Fixed
- 🐛 **Critical Bug Fix**
  - Fixed PYTHONPATH unbound variable error in homebrew installation
  - Improved environment variable handling with proper bash parameter expansion
  - Ensures seamless installation for all users without manual fixes

### Technical Improvements
- **Homebrew Formula**: Fixed `${PYTHONPATH:-}` parameter expansion for unset variables
- **User Experience**: Eliminates need for manual post-installation fixes
- **Reliability**: Ensures consistent behavior across different shell environments

## [1.1.0] - 2024-12-07

### Added
- 🔧 **Enhanced Homebrew Support**
  - Improved homebrew formula with better error handling
  - Fixed PYTHONPATH environment variable initialization
  - Better dependency checking and validation

- 🚀 **Deployment Improvements** 
  - Enhanced auto-detection reliability
  - Better error messages for deployment failures
  - Improved Docker builder with latest dependencies

### Changed
- 📦 **Updated Dependencies**
  - Updated Python SDK to latest versions
  - Improved Flask and Gunicorn configurations
  - Better CrewAI integration and stability

### Fixed
- 🐛 **Bug Fixes**
  - Fixed homebrew installation PYTHONPATH issue
  - Resolved module import errors in builder
  - Fixed command parsing in CLI scripts
  - Improved error handling for missing dependencies

### Technical Improvements
- **Module System**: Fixed getmethatdawg module imports throughout codebase
- **Error Handling**: Better error messages and debugging information
- **Stability**: Improved reliability of auto-detection and deployment
- **Documentation**: Updated examples and troubleshooting guides

## [0.1.0] - 2024-07-12

### Added
- 🚀 **Core Features**
  - Zero-config deployment for Python applications
  - Auto-detection of functions as API endpoints
  - Seamless environment variable and secrets management
  - Fly.io integration for cloud deployment
  - Docker containerization with automatic builder

- 🔍 **Auto-Detection System**
  - Intelligent HTTP method detection (GET vs POST)
  - Automatic path generation from function names
  - Smart parameter handling and type conversion
  - AST-based function analysis

- 🔐 **Environment Management**
  - Automatic `.env` file detection and processing
  - Smart categorization of secrets vs environment variables
  - Fly.io secrets integration for secure API key storage
  - Generated deployment scripts with secrets management

- 🤖 **AI Framework Support**
  - Complete CrewAI multi-agent system example
  - OpenAI, Anthropic, and Groq LLM integration
  - Real-time content generation with 4 specialized agents
  - Production-ready AI content creation workflow

- 📦 **Installation Options**
  - Homebrew formula for system-wide installation
  - Manual installation script with dependency management
  - Development environment setup
  - Shell completions for bash and zsh

- 🛠️ **Developer Tools**
  - Comprehensive CLI with auto-detection mode
  - Postman collection for API testing
  - Automated test scripts and demo workflows
  - Complete documentation and examples

- 📚 **Documentation**
  - Comprehensive README with examples
  - Deployment guide with best practices
  - API usage guide with real-world scenarios
  - Environment setup instructions
  - Contributing guidelines

- 🧪 **Examples**
  - Simple agent example with basic functions
  - Advanced CrewAI multi-agent content creation system
  - API testing and demonstration scripts
  - Postman collection for endpoint testing

### Technical Details
- **Languages**: Python 3.11+, Bash
- **Dependencies**: Docker, Fly.io CLI
- **Frameworks**: Flask, CrewAI, LangChain
- **Deployment**: Fly.io with auto-scaling and health checks
- **Security**: Encrypted secrets, environment isolation

### Infrastructure
- **Builder System**: Docker-based containerization
- **Auto-Detection**: AST parsing for intelligent endpoint detection
- **Secrets Management**: Fly.io encrypted secrets with automatic categorization
- **Monitoring**: Built-in health checks and status endpoints

### Performance
- **Deployment Time**: 30-60 seconds for complete deployment
- **Auto-Scaling**: Scales to zero when idle, auto-starts on demand
- **Global Edge**: Deployed on Fly.io's global infrastructure
- **Container Size**: Optimized Docker images (400-500MB for AI workloads)

### Developer Experience
- **Zero Configuration**: No decorators or setup required with auto-detect
- **One Command Deploy**: `getmethatdawg deploy my_agent.py --auto-detect`
- **Smart Defaults**: Intelligent HTTP method and path detection
- **Rich Documentation**: Complete guides and examples

---

## Release Notes

### v0.1.0 Highlights

This is the initial release of GetMeThatDawg, introducing a revolutionary approach to Python deployment:

**🎯 Zero-Config Deployment**
- Deploy any Python file with functions as a live web API
- No decorators, configuration files, or infrastructure setup needed
- Automatic endpoint detection using intelligent AST analysis

**🔐 Seamless Secrets Management**
- Automatic detection and secure handling of API keys
- Smart categorization of secrets vs environment variables
- One-command deployment with encrypted secrets

**🤖 AI-Ready Architecture**
- Built-in support for popular AI frameworks
- Complete CrewAI example with 4 specialized agents
- Production-ready AI content generation system

**📦 Professional Installation**
- Homebrew package for system-wide installation
- Comprehensive CLI with shell completions
- Development environment setup

### Breaking Changes
- None (initial release)

### Migration Guide
- None (initial release)

### Known Issues
- Builder image download on first use (expected, ~2 minutes)
- Fly.io account required for deployment
- Docker must be running for builds

### Contributors
- @Dwij1704 - Project creator and maintainer

---

## Future Roadmap

### v0.2.0 (Planned)
- AWS Lambda deployment support
- Kubernetes deployment templates
- Enhanced authentication/authorization
- Performance monitoring dashboard

### v0.3.0 (Planned)
- Multiple cloud provider support
- Custom domain configuration
- Advanced scaling policies
- Cost optimization features

### Long-term Goals
- GUI dashboard for deployment management
- VS Code extension
- Multi-language support (Go, Node.js, etc.)
- Enterprise features (SSO, audit logs, etc.)

---

## Links
- [GitHub Repository](https://github.com/Dwij1704/getmethatdawg)
- [Documentation](https://github.com/Dwij1704/getmethatdawg/tree/main/docs)
- [Examples](https://github.com/Dwij1704/getmethatdawg/tree/main/examples)
- [Issues](https://github.com/Dwij1704/getmethatdawg/issues)
- [Discussions](https://github.com/Dwij1704/getmethatdawg/discussions) 