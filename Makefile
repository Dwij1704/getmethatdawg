# Makefile for getmethatdawg - Zero-config deployment for Python AI agents

.PHONY: help install uninstall clean test build package homebrew docs examples dev-setup

# Default target
.DEFAULT_GOAL := help

# Configuration
PYTHON_CMD ?= python3.11
GETMETHATDAWG_HOME ?= /usr/local/lib/getmethatdawg
GETMETHATDAWG_BIN ?= /usr/local/bin
BUILD_DIR := build
DIST_DIR := dist

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

help: ## Show this help message
	@echo "🚀 getmethatdawg - Zero-config deployment for Python AI agents"
	@echo "================================================================"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Quick start:"
	@echo "  make install          # Install getmethatdawg system-wide"
	@echo "  make test             # Run tests"
	@echo "  make examples         # Try example deployments"

install: ## Install getmethatdawg system-wide
	@echo "$(GREEN)Installing getmethatdawg system-wide...$(NC)"
	@chmod +x scripts/install.sh
	@./scripts/install.sh

uninstall: ## Uninstall getmethatdawg from system
	@echo "$(YELLOW)Uninstalling getmethatdawg...$(NC)"
	@chmod +x scripts/install.sh
	@./scripts/install.sh uninstall

dev-setup: ## Set up development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@$(PYTHON_CMD) -m pip install -e getmethatdawg-sdk/
	@$(PYTHON_CMD) -m pip install pytest black flake8 mypy
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo "You can now use: ./bin/getmethatdawg deploy your_file.py --auto-detect"

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	@cd getmethatdawg-sdk && $(PYTHON_CMD) -m pytest tests/ -v
	@echo "$(GREEN)Tests completed!$(NC)"

test-simple: ## Test with a simple example
	@echo "$(BLUE)Testing simple deployment...$(NC)"
	@echo 'def hello(name: str = "World"): return {"message": f"Hello, {name}!"}' > test_simple.py
	@echo "Created test_simple.py"
	@echo "To test deployment, run: getmethatdawg deploy test_simple.py --auto-detect"

test-crewai: ## Test CrewAI example deployment
	@echo "$(BLUE)Testing CrewAI deployment...$(NC)"
	@cd examples/storytelling_agent && \
		if [ -f .env ]; then \
			echo "Found .env file, deploying with secrets..."; \
			../../bin/getmethatdawg deploy ai_contentgen_crew.py --auto-detect; \
		else \
			echo "No .env file found, deploying in demo mode..."; \
			../../bin/getmethatdawg deploy ai_contentgen_crew.py --auto-detect; \
		fi

lint: ## Run code linting
	@echo "$(BLUE)Linting code...$(NC)"
	@cd getmethatdawg-sdk && $(PYTHON_CMD) -m flake8 getmethatdawg/
	@cd getmethatdawg-sdk && $(PYTHON_CMD) -m black --check getmethatdawg/
	@cd getmethatdawg-sdk && $(PYTHON_CMD) -m mypy getmethatdawg/
	@echo "$(GREEN)Linting completed!$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	@cd getmethatdawg-sdk && $(PYTHON_CMD) -m black getmethatdawg/
	@echo "$(GREEN)Code formatted!$(NC)"

clean: ## Clean build artifacts and temporary files
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	@rm -rf $(BUILD_DIR)/ $(DIST_DIR)/
	@rm -rf getmethatdawg-sdk/build/ getmethatdawg-sdk/dist/ getmethatdawg-sdk/*.egg-info/
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -f test_simple.py my_agent.py
	@echo "$(GREEN)Cleanup completed!$(NC)"

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	@mkdir -p $(BUILD_DIR) $(DIST_DIR)
	@cd getmethatdawg-sdk && $(PYTHON_CMD) setup.py sdist bdist_wheel
	@cp getmethatdawg-sdk/dist/* $(DIST_DIR)/
	@echo "$(GREEN)Build completed! Check $(DIST_DIR)/$(NC)"

package: build ## Create release packages
	@echo "$(BLUE)Creating release packages...$(NC)"
	@tar -czf $(DIST_DIR)/getmethatdawg-source.tar.gz \
		--exclude='*.pyc' \
		--exclude='__pycache__' \
		--exclude='.git' \
		--exclude='getmethatdawg-env' \
		--exclude='build' \
		--exclude='dist' \
		bin/ getmethatdawg-sdk/ libexec/ examples/ docs/ scripts/ \
		README.md LICENSE Makefile
	@echo "$(GREEN)Release package created: $(DIST_DIR)/getmethatdawg-source.tar.gz$(NC)"

homebrew: ## Create homebrew formula (requires git repository)
	@echo "$(BLUE)Creating homebrew formula...$(NC)"
	@echo "Homebrew formula is ready at: homebrew/getmethatdawg.rb"
	@echo ""
	@echo "To publish to homebrew:"
	@echo "  1. Create a GitHub repository for your homebrew tap"
	@echo "  2. Copy homebrew/getmethatdawg.rb to your tap repository"
	@echo "  3. Update the URL and SHA256 in the formula"
	@echo "  4. Users can then install with:"
	@echo "     brew tap Dwij1704/getmethatdawg"
	@echo "     brew install getmethatdawg"

docs: ## Generate documentation
	@echo "$(BLUE)Documentation is available in docs/$(NC)"
	@echo "📚 Available documentation:"
	@echo "  - README.md                    Main project documentation"
	@echo "  - docs/DEPLOYMENT_GUIDE.md     Complete deployment guide"
	@echo "  - examples/storytelling_agent/API_USAGE_GUIDE.md    API usage examples"
	@echo "  - examples/storytelling_agent/ENVIRONMENT_SETUP.md  Environment setup"

examples: ## List and describe available examples
	@echo "$(BLUE)Available examples:$(NC)"
	@echo ""
	@echo "📝 Simple Agent (examples/storytelling_agent/simple_agent.py):"
	@echo "   Basic example with content generation functions"
	@echo "   Deploy: getmethatdawg deploy examples/storytelling_agent/simple_agent.py --auto-detect"
	@echo ""
	@echo "🤖 CrewAI Multi-Agent (examples/storytelling_agent/ai_contentgen_crew.py):"
	@echo "   Advanced 4-agent content creation system"
	@echo "   Deploy: getmethatdawg deploy examples/storytelling_agent/ai_contentgen_crew.py --auto-detect"
	@echo ""
	@echo "📊 API Testing:"
	@echo "   Run: examples/storytelling_agent/test_api_sequence.sh"
	@echo "   Demo: examples/storytelling_agent/demo_api_workflow.sh"
	@echo "   Postman: Import examples/storytelling_agent/CrewAI_Content_Agent_Postman_Collection.json"

check-deps: ## Check if all dependencies are installed
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@command -v $(PYTHON_CMD) >/dev/null 2>&1 || { echo "❌ Python 3.11+ not found"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "❌ Docker not found"; exit 1; }
	@command -v flyctl >/dev/null 2>&1 || { echo "⚠️  flyctl not found (will be installed automatically)"; }
	@docker info >/dev/null 2>&1 || { echo "⚠️  Docker not running"; }
	@echo "$(GREEN)✅ Dependencies check completed$(NC)"

install-deps: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@$(PYTHON_CMD) -m pip install --upgrade pip
	@$(PYTHON_CMD) -m pip install pytest black flake8 mypy wheel setuptools twine
	@echo "$(GREEN)Development dependencies installed!$(NC)"

version: ## Show version information
	@echo "getmethatdawg version 0.1.0"
	@echo "Zero-config deployment for Python AI agents"
	@echo ""
	@echo "Components:"
	@echo "  - getmethatdawg CLI: bin/getmethatdawg"
	@echo "  - getmethatdawg SDK: getmethatdawg-sdk/"
	@echo "  - Builder: getmethatdawg-sdk/getmethatdawg/builder.py"
	@echo "  - Examples: examples/"

release: build package ## Create a complete release
	@echo "$(GREEN)🎉 Release created!$(NC)"
	@echo ""
	@echo "Release artifacts:"
	@ls -la $(DIST_DIR)/
	@echo ""
	@echo "Next steps:"
	@echo "  1. Test the release: make test"
	@echo "  2. Update GitHub repository"
	@echo "  3. Create GitHub release with $(DIST_DIR)/getmethatdawg-source.tar.gz"
	@echo "  4. Update homebrew formula with new SHA256"
	@echo "  5. Publish to PyPI: cd getmethatdawg-sdk && twine upload dist/*"

demo: ## Run a complete demo
	@echo "$(BLUE)🎬 getmethatdawg Demo$(NC)"
	@echo "====================="
	@echo ""
	@echo "Creating a simple AI agent..."
	@echo 'def generate_idea(topic: str, style: str = "creative"): return {"idea": f"A {style} project about {topic}"}' > demo_agent.py
	@echo 'def analyze_sentiment(text: str): return {"sentiment": "positive", "confidence": 0.95}' >> demo_agent.py
	@echo ""
	@echo "Created demo_agent.py with 2 functions"
	@echo ""
	@echo "To deploy:"
	@echo "  getmethatdawg deploy demo_agent.py --auto-detect"
	@echo ""
	@echo "This will create:"
	@echo "  - GET  /generate-idea?topic=...&style=..."
	@echo "  - POST /analyze-sentiment (with JSON body)"
	@echo ""
	@echo "🚀 Try it now: getmethatdawg deploy demo_agent.py --auto-detect"

# Development targets
dev-test: dev-setup test ## Set up dev environment and run tests

dev-lint: dev-setup lint ## Set up dev environment and run linting

dev-all: dev-setup test lint examples ## Complete development setup

# CI/CD targets
ci-test: install-deps test lint ## CI testing pipeline

ci-build: install-deps build ## CI build pipeline

ci-release: ci-test ci-build release ## Complete CI release pipeline

# Docker targets
docker-build: ## Build getmethatdawg/builder Docker image
	@echo "$(BLUE)Building getmethatdawg/builder Docker image...$(NC)"
	@docker build -t getmethatdawg/builder:latest -f Dockerfile.builder .
	@echo "$(GREEN)Docker image built: getmethatdawg/builder:latest$(NC)"

docker-clean: ## Clean Docker images and containers
	@echo "$(YELLOW)Cleaning Docker images...$(NC)"
	@docker rmi getmethatdawg/builder:latest 2>/dev/null || true
	@docker system prune -f
	@echo "$(GREEN)Docker cleanup completed$(NC)"

# Help for specific components
help-install: ## Show installation help
	@echo "$(BLUE)Installation Options:$(NC)"
	@echo ""
	@echo "🍺 Homebrew (Recommended):"
	@echo "   brew tap Dwij1704/getmethatdawg"
	@echo "   brew install getmethatdawg"
	@echo ""
	@echo "📦 Manual Installation:"
	@echo "   git clone https://github.com/Dwij1704/getmethatdawg.git"
	@echo "   cd getmethatdawg"
	@echo "   make install"
	@echo ""
	@echo "👨‍💻 Development Setup:"
	@echo "   make dev-setup"

help-deploy: ## Show deployment help
	@echo "$(BLUE)Deployment Options:$(NC)"
	@echo ""
	@echo "🎯 Auto-Detection (Recommended):"
	@echo "   getmethatdawg deploy my_agent.py --auto-detect"
	@echo ""
	@echo "🏷️  Manual Decorators:"
	@echo "   Use @getmethatdawg.expose decorators in your Python file"
	@echo "   getmethatdawg deploy my_agent.py"
	@echo ""
	@echo "🔐 With Environment Variables:"
	@echo "   Create .env file in same directory"
	@echo "   getmethatdawg deploy my_agent.py --auto-detect" 