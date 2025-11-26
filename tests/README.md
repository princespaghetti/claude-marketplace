# Tests

This directory contains test suites for the claude-marketplace repository.

## Structure

Tests are organized by component:

- **workflow-analyzer/** - Tests for the Claude Code workflow analyzer script
  - See [workflow-analyzer/TESTING.md](workflow-analyzer/TESTING.md) for details
- **dependency-evaluator/** - Tests for the dependency evaluator script
  - See [dependency-evaluator/TESTING.md](dependency-evaluator/TESTING.md) for details

## Why Tests are Here

Tests are kept outside of the plugin installation directories (like `learnfrompast/`) to avoid including test files in the distributed plugins. This keeps the installed plugins clean and minimal.

## Running Tests

Each test directory contains its own:
- `requirements-test.txt` - Test-specific dependencies
- `TESTING.md` - Detailed instructions for running tests
- `pytest.ini` - Pytest configuration

Navigate to the specific test directory and follow the instructions in its TESTING.md file.
