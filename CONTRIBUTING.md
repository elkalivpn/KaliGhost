# Contributing to KaliGhost 3.0

First off, thank you for your interest in contributing to KaliGhost! We appreciate your support.

## Code of Conduct

Be respectful, inclusive, and professional. We're building elite engineering tools.

---

## How to Contribute

### 🐛 Bug Reports

Found a bug? Report it on [GitHub Issues](https://github.com/elkalivpn/KaliGhost/issues).

**Include:**
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

### 💡 Feature Requests

Have an idea? Open an issue with the label `enhancement`.

**Include:**
- Use case description
- Why this feature matters
- Implementation suggestions (optional)

### 🔒 Security Disclosures

**Do NOT open a public issue for security vulnerabilities.**

Email: `security@kalighost.io`

---

## Development Setup

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Git

### Local Development

```bash
# Clone
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start services
./start.sh
```

### Running Tests

```bash
# Run E2E tests
python test_e2e.py

# Run specific test
python test_e2e.py --test-name "test_orchestrator"
```

### Code Style

- **Format**: Black (4-space indentation)
- **Linting**: Pylint, Flake8
- **Type Hints**: Required for all public functions
- **Docstrings**: Google-style for all modules/classes

```bash
# Format code
black backend/ cli.py webchat.py

# Lint
pylint backend/
flake8 backend/
```

---

## Pull Request Process

### Before Submitting

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/description`
3. **Commit** with clear messages: `git commit -m "Add feature X"`
4. **Test** thoroughly: `python test_e2e.py`
5. **Push** to your fork: `git push origin feature/description`
6. **Open** a Pull Request

### PR Requirements

- ✅ All tests passing (11/12 minimum)
- ✅ No breaking changes without discussion
- ✅ Updated documentation if needed
- ✅ Clear commit messages
- ✅ No security vulnerabilities
- ✅ Code follows style guide

### PR Template

```markdown
## Description
Brief description of changes

## Type
- [ ] Bug fix
- [ ] Feature
- [ ] Documentation
- [ ] Performance

## Changes
- Change 1
- Change 2

## Testing
How was this tested?

## Breaking Changes
None / Describe breaking changes
```

---

## Module Development

### Adding a New Module

1. **Create** `backend/my_module.py`
2. **Implement** core functions
3. **Add tests** in `test_e2e.py`
4. **Document** in docstrings
5. **Update** `__init__.py` exports

### Module Template

```python
"""
my_module.py - Brief description

This module provides functionality for X.
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class MyModule:
    """Main class for my module."""
    
    def __init__(self):
        """Initialize the module."""
        self.initialized = True
    
    async def my_function(self, param: str) -> Dict[str, Any]:
        """
        Do something.
        
        Args:
            param: Input parameter
        
        Returns:
            Result dictionary
        
        Raises:
            ValueError: If param is invalid
        """
        if not param:
            raise ValueError("param cannot be empty")
        
        result = await self._internal_function(param)
        return result
    
    async def _internal_function(self, param: str) -> Dict[str, Any]:
        """Internal helper function."""
        # Implementation
        return {"status": "success", "param": param}


def get_my_module() -> MyModule:
    """Factory function for MyModule."""
    return MyModule()
```

---

## Documentation

### Update These When Needed

- **ARCHITECTURE_3_0.md** - For architectural changes
- **COMPLETE_SUITE_3_0.md** - For new workflows
- **QUICKSTART.md** - For setup changes
- **README.md** - For major feature additions

### Documentation Style

- Clear, concise language
- Code examples where helpful
- Links to related docs
- Updated table of contents

---

## Testing Guidelines

### Unit Tests
Test individual functions in isolation.

### Integration Tests
Test module interactions.

### E2E Tests
Test complete workflows end-to-end.

### Coverage
Aim for > 85% code coverage.

```python
# Example test
@suite.test("Module X - Functionality")
async def test_module_x():
    from backend.my_module import get_my_module
    
    module = get_my_module()
    result = await module.my_function("test")
    
    assert result["status"] == "success"
```

---

## Release Process

### Version Numbering
- Major.Minor.Patch (e.g., 3.0.1)
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Release Checklist

- [ ] Update version in code
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Build Docker images
- [ ] Tag release: `git tag v3.0.1`
- [ ] Push tag: `git push origin v3.0.1`

---

## Code Review Process

### We Look For

✅ **Functionality**
- Does it work as intended?
- Are there edge cases?

✅ **Quality**
- Is code clean and readable?
- Are there type hints?
- Are docstrings present?

✅ **Testing**
- Are tests comprehensive?
- Do they pass?

✅ **Security**
- No SQL injection risks?
- No secrets in code?
- Proper authentication?

✅ **Performance**
- No N+1 queries?
- Efficient algorithms?
- Async where needed?

---

## Getting Help

- **Documentation**: See `/` directory for guides
- **Issues**: Check existing issues first
- **Discussions**: GitHub Discussions for questions
- **Email**: support@kalighost.io

---

## Acknowledgments

Contributors who improve KaliGhost help make elite development accessible to everyone. Thank you!

---

<div align="center">

**🐉 Together, we're building the future of development.**

</div>
