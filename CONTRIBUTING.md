# Contributing to GetMeThatDawg

Thank you for your interest in contributing to GetMeThatDawg! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/Dwij1704/getmethatdawg.git
   cd getmethatdawg
   ```
3. **Set up development environment**:
   ```bash
   make dev-setup
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make your changes** and test them
6. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- Docker
- Git

### Setting Up
```bash
# Clone the repository
git clone https://github.com/Dwij1704/getmethatdawg.git
cd getmethatdawg

# Set up development environment
make dev-setup

# Verify setup
make test
```

### Development Workflow
```bash
# Run tests
make test

# Run linting
make lint

# Format code
make format

# Test with examples
make examples

# Clean up
make clean
```

## 📋 What Can You Contribute?

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide system information (OS, Python version, Docker version)
- Include error messages and logs

### ✨ Feature Requests
- Use GitHub Issues to suggest features
- Describe the use case and benefits
- Provide examples of how it would work
- Consider creating a proof of concept

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

### 📚 Documentation
- Improve README and documentation
- Add examples and tutorials
- Fix typos and clarify explanations
- Add API documentation

### 🧪 Testing
- Add test cases for new features
- Improve test coverage
- Test on different platforms
- Performance testing

## 🎯 Areas That Need Help

### High Priority
- [ ] **AWS Lambda support** - Add serverless deployment option
- [ ] **Kubernetes support** - Add K8s deployment templates
- [ ] **More AI framework examples** - LangChain, Hugging Face, etc.
- [ ] **Authentication/Authorization** - Add auth middleware
- [ ] **Rate limiting** - Add built-in rate limiting

### Medium Priority
- [ ] **Database integration** - PostgreSQL, Redis, etc.
- [ ] **Monitoring/Logging** - Better observability tools
- [ ] **Custom domains** - Support for custom domain names
- [ ] **Multi-region deployment** - Deploy to multiple regions
- [ ] **CI/CD templates** - GitHub Actions, GitLab CI, etc.

### Nice to Have
- [ ] **GUI dashboard** - Web interface for managing deployments
- [ ] **VS Code extension** - Deploy directly from VS Code
- [ ] **More deployment targets** - Vercel, Netlify, Railway, etc.
- [ ] **Auto-scaling policies** - Smart scaling based on usage
- [ ] **Cost optimization** - Monitor and optimize deployment costs

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8
- Use Black for formatting: `make format`
- Use type hints where possible
- Write docstrings for functions and classes

### Git Commit Messages
Use conventional commit format:
```
type(scope): description

feat(auto-detect): add support for async functions
fix(secrets): handle special characters in environment variables
docs(readme): update installation instructions
test(builder): add tests for endpoint detection
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

### Code Organization
```
getmethatdawg/
├── bin/getmethatdawg                 # Main CLI entry point
├── getmethatdawg-sdk/               # Python SDK
│   ├── getmethatdawg/
│   │   ├── __init__.py
│   │   ├── builder.py     # Core builder logic
│   │   └── decorators.py  # @getmethatdawg.expose decorators
│   ├── tests/             # Test suite
│   └── setup.py
├── examples/              # Example applications
├── docs/                  # Documentation
├── scripts/               # Installation and helper scripts
└── homebrew/              # Homebrew formula
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
cd getmethatdawg-sdk && python -m pytest tests/test_builder.py -v

# Run with coverage
cd getmethatdawg-sdk && python -m pytest tests/ --cov=getmethatdawg --cov-report=html
```

### Writing Tests
- Write tests for all new features
- Use pytest framework
- Follow the AAA pattern (Arrange, Act, Assert)
- Mock external dependencies (Docker, Fly.io API)

Example test:
```python
def test_auto_detect_get_endpoint():
    """Test that GET endpoints are detected correctly"""
    # Arrange
    builder = GetMeThatDawgBuilder("test.py", auto_detect=True)
    
    # Act
    endpoints = builder.analyze_function("def get_user(id: str): return {'user': id}")
    
    # Assert
    assert len(endpoints) == 1
    assert endpoints[0].method == "GET"
    assert endpoints[0].path == "/get-user"
```

### Integration Tests
- Test actual deployments with Docker
- Test end-to-end workflows
- Use temporary environments
- Clean up after tests

## 📚 Documentation Guidelines

### README Updates
- Keep examples current and working
- Update feature lists when adding functionality
- Include screenshots for visual features
- Test all code examples

### API Documentation
- Document all public functions and classes
- Include parameter types and return values
- Provide usage examples
- Document error conditions

### Tutorials and Guides
- Step-by-step instructions
- Real-world examples
- Troubleshooting sections
- Links to related resources

## 🚢 Release Process

### Version Numbering
We use [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release in Git
- [ ] Publish to PyPI
- [ ] Update Homebrew formula

## 🤝 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass: `make test`
- [ ] Linting passes: `make lint`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for user-facing changes)

### PR Description Template
```markdown
## Summary
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Documentation
- [ ] README updated
- [ ] API docs updated
- [ ] Examples updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated
```

### Review Process
1. **Automated checks** run (tests, linting)
2. **Code review** by maintainers
3. **Feedback** and iterations
4. **Approval** and merge

## 🎖️ Recognition

Contributors are recognized in:
- README.md contributors section
- GitHub releases
- Project documentation

## 📞 Getting Help

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and community discussion
- **Discord** - Real-time chat (coming soon)
- **Email** - maintainers@getmethatdawg.dev (for private matters)

## 📜 Code of Conduct

### Our Pledge
We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at conduct@getmethatdawg.dev.

## 🙏 Thank You

Thank you for contributing to GetMeThatDawg! Your contributions help make Python deployment easier for developers worldwide.

---

**Questions?** Open an issue or start a discussion. We're here to help! 🚀 