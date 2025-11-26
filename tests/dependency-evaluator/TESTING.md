# Testing dependency_evaluator.py

This document describes how to run the test suite for the dependency evaluator script.

## Location

Tests are located in `/tests/dependency-evaluator/` at the repository root, outside of the plugin installation directory.

## Setup

Install test dependencies from the tests directory:

```bash
cd tests/dependency-evaluator
pip install -r requirements-test.txt
```

## Running Tests

### Run all tests

```bash
pytest test_dependency_evaluator.py
```

### Run with verbose output

```bash
pytest test_dependency_evaluator.py -v
```

### Run with coverage report

```bash
pytest test_dependency_evaluator.py --cov=dependency_evaluator --cov-report=html
```

### Run specific test categories

The tests are organized into categories. You can filter by test name patterns:

**Core functionality tests**:
```bash
pytest test_dependency_evaluator.py -k "test_gather"
```

**Command execution tests**:
```bash
pytest test_dependency_evaluator.py -k "test_run_command"
```

**Error handling tests**:
```bash
pytest test_dependency_evaluator.py -k "error or failure"
```

**Integration tests** (end-to-end flows):
```bash
pytest test_dependency_evaluator.py -k "test_evaluate"
```

**GitHub integration tests**:
```bash
pytest test_dependency_evaluator.py -k "github"
```

### Run a specific test

```bash
pytest test_dependency_evaluator.py::test_npm_data_gathering
```

## Test Coverage

The test suite covers:

### DependencyEvaluator class
- Initialization and configuration
- Command execution (run_command method)
- URL fetching (fetch_url method)
- npm data gathering
- PyPI data gathering
- Cargo data gathering
- Go data gathering
- GitHub data extraction and API calls
- Security data collection
- Dependency footprint analysis
- Full evaluation workflow

### Command execution
- Successful command execution
- Command not found handling
- Command timeout handling
- Subprocess errors

### HTTP/Network operations
- Successful API calls
- HTTP error codes (404, 403, etc.)
- Network errors
- JSON parsing errors
- Rate limiting

### Data parsing
- npm JSON output parsing
- PyPI API response parsing
- Cargo/crates.io API response parsing
- Go module data parsing
- GitHub API response parsing

### Edge cases
- Missing package data
- Malformed URLs
- Empty responses
- Unicode in package names
- Very large responses
- Rate limiting scenarios

## Test Structure

Tests use pytest fixtures to mock external dependencies:
- `mock_subprocess_run`: Mocks subprocess.run for command execution
- `mock_urlopen`: Mocks urllib.request.urlopen for HTTP requests
- Sample JSON responses for each ecosystem

This allows tests to run without:
- Actual package installations
- Network access
- External API dependencies

## Sample Test Data Format

The tests use realistic sample data matching actual API responses:

**npm view output**:
```json
{
  "version": "4.17.21",
  "license": "MIT",
  "repository": {"type": "git", "url": "https://github.com/lodash/lodash"}
}
```

**GitHub API response**:
```json
{
  "pushed_at": "2024-12-15T10:30:00Z",
  "open_issues_count": 42,
  "stargazers_count": 58000
}
```

## Coverage Goals

Target: >85% code coverage for all core functions
- Command execution: 100%
- Data gathering methods: >90%
- Error handling: >90%
- Integration: >80%
