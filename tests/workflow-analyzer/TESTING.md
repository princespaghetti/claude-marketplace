# Testing workflow_analyzer.py

This document describes how to run the test suite for the workflow analyzer script.

## Location

Tests are located in `/tests/workflow-analyzer/` at the repository root, outside of the plugin installation directory.

## Setup

Install test dependencies from the tests directory:

```bash
cd tests/workflow-analyzer
pip install -r requirements-test.txt
```

## Running Tests

### Run all tests

```bash
pytest test_workflow_analyzer.py
```

### Run with verbose output

```bash
pytest test_workflow_analyzer.py -v
```

### Run with coverage report

```bash
pytest test_workflow_analyzer.py --cov=workflow_analyzer --cov-report=html
```

### Run specific test categories

The tests are organized into categories using pytest markers (though not explicitly marked in the code, you can filter by test name patterns):

**Unit tests** (test individual functions):
```bash
pytest test_workflow_analyzer.py -k "analyze_sessions or generate_report"
```

**Integration tests** (test the main() function):
```bash
pytest test_workflow_analyzer.py -k "main_function"
```

**Edge case tests**:
```bash
pytest test_workflow_analyzer.py -k "edge_case or error or handling"
```

### Run a specific test

```bash
pytest test_workflow_analyzer.py::test_analyze_sessions_empty_list
```

## Test Coverage

The test suite covers:

### analyze_sessions() function
- Empty file lists
- Single and multiple user prompts
- Filtering of meta messages
- Filtering of command messages
- Filtering of short messages
- Ignoring assistant messages
- Ignoring file snapshots
- Handling malformed JSON
- Pattern detection (git, version, docs, test/fix, implementation)
- Multiple sessions from different projects
- Prompt metadata storage

### generate_report() function
- Basic report structure
- Including examples from patterns
- Project activity sorting
- Time savings calculations
- Handling zero patterns

### main() function
- Processing stdin input
- Handling empty stdin
- Processing multiple files

### Edge cases
- Nonexistent files
- Empty files
- Unicode content
- Very long messages
- Message content as list (non-string)
- Missing required fields

## Test Structure

Tests use pytest fixtures to create temporary JSONL session files that mimic the structure of actual Claude Code conversation logs. The main fixture is `create_test_session_file`, which creates realistic test data without requiring actual log files.

## Sample Test Data Format

The tests use JSONL entries that match the Claude Code conversation log format:

```json
{
  "type": "user",
  "message": {
    "role": "user",
    "content": "User's message here"
  },
  "sessionId": "test-session-123",
  "uuid": "test-uuid-456"
}
```

Other entry types like `"type": "assistant"` and `"type": "file-history-snapshot"` are also tested to ensure they're properly filtered.
