# KaliGhost Development Guidelines

This document outlines the coding standards, development practices, and contribution guidelines for the KaliGhost project. These guidelines ensure code quality, maintainability, and consistency across the codebase.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Coding Standards](#coding-standards)
   - [Python Style Guide](#python-style-guide)
   - [JavaScript/TypeScript Style Guide](#javascripttypescript-style-guide)
   - [Documentation Standards](#documentation-standards)
3. [Project Structure](#project-structure)
4. [Branching Strategy](#branching-strategy)
5. [Testing](#testing)
   - [Unit Tests](#unit-tests)
   - [Integration Tests](#integration-tests)
   - [End-to-End Tests](#end-to-end-tests)
6. [Continuous Integration](#continuous-integration)
7. [Security Considerations](#security-considerations)
8. [Performance Guidelines](#performance-guidelines)
9. [Contributing](#contributing)

## Getting Started

To set up your development environment:

1. Fork the KaliGhost repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/KaliGhost.git
   cd KaliGhost
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install  # for frontend components
   ```
4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some additional conventions:

#### Naming Conventions
- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private members: prefixed with `_`

#### Imports
- Group imports in order: standard library, third-party, local
- Use explicit imports rather than wildcards
- Alphabetize imports within each group

#### Example
```python
import os
import sys
from typing import List, Dict, Optional

import requests
from pydantic import BaseModel

from .utils import format_output
from .models import ScanResult


class NetworkScanner(BaseModel):
    """Handles network scanning operations."""
    
    def __init__(self, target: str, ports: List[int]):
        self.target = target
        self.ports = ports
        self._results: List[ScanResult] = []
    
    def scan_target(self) -> List[ScanResult]:
        """
        Scan target for open ports.
        
        Returns:
            List of scan results
            
        Raises:
            ConnectionError: If unable to reach target
            ValueError: If invalid port range provided
        """
        if not self._validate_target():
            raise ValueError("Invalid target format")
            
        results = []
        for port in self.ports:
            if self._check_port(port):
                results.append(ScanResult(host=self.target, port=port))
                
        return results
```

#### Type Hints
Always use type hints for function parameters and return values:

```python
def calculate_risk_score(vulnerability: Dict[str, Any]) -> float:
    """Calculate risk score based on vulnerability data."""
    cvss_base = vulnerability.get('cvss_base_score', 0.0)
    exploitability = vulnerability.get('exploitability', 0.0)
    return cvss_base * (1 + exploitability * 0.3)
```

### JavaScript/TypeScript Style Guide

Follow Airbnb JavaScript Style Guide with TypeScript extensions:

#### File Structure
```typescript
// Import statements
import { useEffect, useState } from 'react';
import axios from 'axios';

// Constants
const API_BASE_URL = '/api/v1';

// Interfaces
interface ScanResult {
  id: string;
  target: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  findings: number;
}

// Component definition
const ScannerDashboard: React.FC = () => {
  // State declarations
  const [results, setResults] = useState<ScanResult[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  
  // Effects
  useEffect(() => {
    fetchScanResults();
  }, []);
  
  // Functions
  const fetchScanResults = async (): Promise<void> => {
    try {
      setLoading(true);
      const response = await axios.get<ScanResult[]>(`${API_BASE_URL}/scans`);
      setResults(response.data);
    } catch (error) {
      console.error('Failed to fetch scan results:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Render
  return (
    <div className="scanner-dashboard">
      {/* Component JSX */}
    </div>
  );
};

export default ScannerDashboard;
```

### Documentation Standards

All public functions, classes, and modules must include docstrings or comments:

#### Python Docstrings (Sphinx format)
```python
def execute_scan(targets: List[str], ports: List[int]) -> Dict[str, Any]:
    """
    Execute network scan on specified targets and ports.
    
    This function orchestrates scanning operations using multiple tools
    and aggregates the results into a standardized format.
    
    Args:
        targets: List of IP addresses or hostnames to scan
        ports: List of port numbers to check
        
    Returns:
        Dictionary containing scan results with the following structure:
        {
            'scan_id': 'unique identifier',
            'timestamp': 'ISO 8601 timestamp',
            'results': [
                {
                    'target': 'scanned host',
                    'port': 'port number',
                    'status': 'open/closed/filtered'
                }
            ]
        }
        
    Raises:
        ValueError: If targets or ports lists are empty
        ConnectionError: If unable to initiate scan process
        
    Example:
        >>> execute_scan(['192.168.1.1'], [22, 80, 443])
        {'scan_id': 'scan-123', 'timestamp': '2026-05-15T14:30:00Z', ...}
    """
```

#### JavaScript Comments
```typescript
/**
 * Fetch security findings from the API
 * 
 * This function retrieves security findings for a specific project,
 * applying filtering and sorting based on provided parameters.
 * 
 * @param projectId - Unique identifier for the project
 * @param filters - Optional filter criteria for findings
 * @param sortBy - Field to sort results by
 * @returns Promise resolving to array of finding objects
 * 
 * @throws {Error} If API request fails
 * @throws {ValidationError} If projectId is invalid
 */
async function fetchFindings(
  projectId: string, 
  filters?: FindingFilters, 
  sortBy: SortField = 'severity'
): Promise<Finding[]> {
  // Implementation
}
```

## Project Structure

```
KaliGhost/
├── src/
│   ├── agent/              # AI agent core functionality
│   │   ├── core/           # Core agent components
│   │   ├── tools/          # Tool integrations
│   │   ├── models/         # Data models
│   │   └── utils/          # Utility functions
│   ├── gui/                # Desktop application
│   │   ├── components/     # React components
│   │   ├── styles/         # CSS/SCSS files
│   │   └── assets/         # Static assets
│   └── cli/                # Command-line interface
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── docs/                   # Documentation
├── scripts/                # Build and utility scripts
├── examples/               # Example configurations and usage
└── vendor/                 # Third-party dependencies
```

## Branching Strategy

We follow GitFlow branching model:

- `main`: Production-ready code
- `develop`: Latest development changes
- `feature/*`: New features
- `hotfix/*`: Urgent production fixes
- `release/*`: Preparation for new releases

### Creating a Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/new-scanner-module
```

### Submitting Changes
1. Ensure your branch is up to date with `develop`
2. Write and run tests
3. Update documentation as needed
4. Submit a pull request with clear description

## Testing

### Unit Tests

Unit tests should cover individual functions and methods with isolated test cases.

```python
import pytest
from unittest.mock import Mock, patch

from src.agent.core.scanner import NetworkScanner


def test_network_scanner_initialization():
    """Test NetworkScanner initializes correctly."""
    scanner = NetworkScanner("192.168.1.1", [22, 80, 443])
    assert scanner.target == "192.168.1.1"
    assert scanner.ports == [22, 80, 443]


@patch('src.agent.core.scanner.requests.get')
def test_scan_host_success(mock_get):
    """Test successful host scanning."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'open_ports': [22, 80]
    }
    
    scanner = NetworkScanner("192.168.1.1", [22, 80, 443])
    results = scanner.scan_target()
    
    assert len(results) == 2
    assert results[0].port == 22
    assert results[1].port == 80


def test_scan_invalid_target():
    """Test scanning with invalid target raises exception."""
    with pytest.raises(ValueError):
        NetworkScanner("invalid-target", [80])
```

### Integration Tests

Integration tests verify interactions between components.

```python
import pytest

from src.agent.core.scanner import NetworkScanner
from src.agent.tools.nmap_wrapper import NmapWrapper


@pytest.mark.integration
def test_scanner_with_real_nmap():
    """Test scanner integration with actual Nmap."""
    # Skip if Nmap not available
    if not NmapWrapper.is_available():
        pytest.skip("Nmap not available")
        
    scanner = NetworkScanner("127.0.0.1", [22, 80])
    results = scanner.scan_target()
    
    # Verify we got valid results
    assert isinstance(results, list)
    # Don't assert specific results as they depend on local environment
```

### End-to-End Tests

E2E tests validate complete workflows.

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.mark.e2e
def test_complete_scan_workflow():
    """Test complete scan workflow through GUI."""
    driver = webdriver.Chrome()
    
    try:
        # Navigate to app
        driver.get("http://localhost:3000")
        
        # Enter target
        target_input = driver.find_element(By.ID, "target-input")
        target_input.send_keys("192.168.1.1")
        
        # Click scan button
        scan_button = driver.find_element(By.ID, "scan-button")
        scan_button.click()
        
        # Wait for results
        results_div = driver.find_element(By.ID, "scan-results")
        assert results_div.is_displayed()
        
        # Verify results
        result_items = driver.find_elements(By.CLASS_NAME, "result-item")
        assert len(result_items) > 0
        
    finally:
        driver.quit()
```

## Continuous Integration

All pull requests must pass our CI pipeline:

1. **Code Quality Checks**
   - Linting with flake8, black, and mypy
   - Security scanning with bandit
   - Dependency checks with safety

2. **Testing Pipeline**
   - Unit tests (coverage > 80%)
   - Integration tests
   - E2E tests (when applicable)

3. **Documentation**
   - Docstring validation
   - Build documentation

## Security Considerations

### Input Validation

Always validate and sanitize inputs:

```python
import re
from urllib.parse import urlparse


def validate_target_input(target: str) -> bool:
    """
    Validate target input to prevent command injection.
    
    Args:
        target: Target hostname or IP address
        
    Returns:
        True if valid, False otherwise
    """
    # Check if it's a valid IP address
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if ip_pattern.match(target):
        parts = target.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    # Check if it's a valid hostname
    hostname_pattern = re.compile(
        r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    )
    if hostname_pattern.match(target):
        return len(target) <= 253
    
    return False
```

### Secure Coding Practices

1. Never log sensitive information
2. Encrypt data at rest and in transit
3. Use secure random number generators
4. Implement proper error handling without information leakage
5. Apply principle of least privilege

### Dependency Management

Regularly update dependencies and scan for vulnerabilities:

```bash
# Check for outdated dependencies
pip list --outdated

# Security scan
safety check

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Performance Guidelines

### Asynchronous Operations

Use async/await for I/O-bound operations:

```python
import asyncio
import aiohttp


async def fetch_multiple_targets(targets: List[str]) -> List[Dict]:
    """
    Fetch data from multiple targets concurrently.
    
    Args:
        targets: List of URLs to fetch
        
    Returns:
        List of response dictionaries
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_target_data(session, target) 
            for target in targets
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]


async def fetch_target_data(session: aiohttp.ClientSession, url: str) -> Dict:
    """
    Fetch data from a single target.
    
    Args:
        session: HTTP session to use
        url: URL to fetch
        
    Returns:
        Dictionary with response data
    """
    async with session.get(url, timeout=30) as response:
        data = await response.json()
        return {
            'url': url,
            'status': response.status,
            'data': data
        }
```

### Memory Management

Clean up resources properly:

```python
import gc
from contextlib import contextmanager


@contextmanager
def temporary_file_cleanup(file_path: str):
    """Context manager to ensure file cleanup."""
    try:
        yield file_path
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def process_large_dataset(dataset_path: str) -> List[Dict]:
    """
    Process large dataset efficiently.
    
    Args:
        dataset_path: Path to dataset file
        
    Returns:
        Processed results
    """
    results = []
    
    with temporary_file_cleanup(dataset_path) as temp_path:
        with open(temp_path, 'r') as f:
            # Process in chunks to avoid memory issues
            chunk_size = 1000
            while True:
                chunk = f.readlines(chunk_size)
                if not chunk:
                    break
                    
                # Process chunk
                processed_chunk = [
                    process_record(line) 
                    for line in chunk
                ]
                results.extend(processed_chunk)
                
                # Force garbage collection periodically
                if len(results) % 10000 == 0:
                    gc.collect()
                    
    return results
```

### Caching

Implement caching for expensive operations:

```python
from functools import lru_cache
import hashlib
import pickle


@lru_cache(maxsize=128)
def cached_vulnerability_lookup(cve_id: str) -> Dict:
    """
    Look up vulnerability information with caching.
    
    Args:
        cve_id: CVE identifier
        
    Returns:
        Vulnerability information
    """
    # Simulate API call
    return fetch_vulnerability_data(cve_id)


def get_cached_scan_results(scan_params: Dict) -> Optional[List]:
    """
    Retrieve cached scan results if available.
    
    Args:
        scan_params: Parameters used for scan
        
    Returns:
        Cached results or None if not found
    """
    # Create cache key from params
    cache_key = hashlib.md5(
        pickle.dumps(scan_params, protocol=pickle.HIGHEST_PROTOCOL)
    ).hexdigest()
    
    # Check cache (implementation depends on cache backend)
    return cache_backend.get(cache_key)
```

## Contributing

We welcome contributions to the KaliGhost project! Here's how to get started:

### Reporting Issues

Before submitting an issue:
1. Check existing issues to avoid duplicates
2. Provide detailed reproduction steps
3. Include environment information (OS, Python version, etc.)
4. Add relevant logs or screenshots

### Code Contributions

1. **Fork and Branch**: Create a feature branch from `develop`
2. **Code Quality**: Follow all style guidelines
3. **Tests**: Include appropriate tests for new functionality
4. **Documentation**: Update relevant documentation
5. **Commit Messages**: Use clear, descriptive commit messages
6. **Pull Request**: Submit PR with detailed description

### Commit Message Format

Follow conventional commits format:

```
feat(scanner): add UDP scanning capability

- Implement UDP port scanning using nmap
- Add new UDP_SCAN mode to scanner configuration
- Update documentation with UDP scanning examples

Resolves #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactorings
- `perf`: Performance improvements
- `test`: Test-related changes
- `chore`: Maintenance tasks

By following these guidelines, you'll help maintain the quality and consistency of the KaliGhost codebase while ensuring your contributions can be smoothly integrated.

---
© 2026 KaliGhost Project. All rights reserved.