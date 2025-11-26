# Dependency Evaluator Script Usage

This document describes how to use the `dependency_evaluator.py` script for automated package data gathering.

## Overview

The dependency evaluator script automates the tedious parts of dependency evaluation:
- Running ecosystem-specific commands (npm, pip, cargo, go)
- Fetching data from package registries and GitHub
- Parsing and structuring the results
- Handling errors and edge cases gracefully

**Recommended approach**: Use the script as your default data gathering method for npm, PyPI, Cargo, and Go packages. It saves time, ensures consistency, and reduces the chance of missing important data points.

**Manual fallback**: The skill works perfectly fine without the script using the manual workflow described in [WORKFLOW.md](./WORKFLOW.md) - use this for unsupported ecosystems or if the script fails.

## Prerequisites

### Required
- Python 3.7 or higher (uses only standard library)

### Optional (for enhanced functionality)
- **npm** - For evaluating Node.js packages
- **pip** - For evaluating Python packages
- **cargo** - For evaluating Rust crates
- **go** - For evaluating Go modules
- **gh CLI** - For richer GitHub data (falls back to API if not available)

## Installation

No installation required! The script uses only Python standard library.

Location: `learnfrompast/skills/dependency-evaluator/scripts/dependency_evaluator.py`

## Basic Usage

```bash
python3 dependency_evaluator.py <package-name> <ecosystem>
```

### Examples

**Evaluate an npm package**:
```bash
python3 dependency_evaluator.py lodash npm
```

**Evaluate a Python package**:
```bash
python3 dependency_evaluator.py requests pypi
```

**Evaluate a Rust crate**:
```bash
python3 dependency_evaluator.py serde cargo
```

**Evaluate a Go module**:
```bash
python3 dependency_evaluator.py github.com/gorilla/mux go
```

## Supported Ecosystems

| Ecosystem | Value | Data Sources |
|-----------|-------|--------------|
| npm (Node.js) | `npm` | npm registry, npm view, GitHub |
| PyPI (Python) | `pypi` | PyPI JSON API, pip, GitHub |
| Cargo (Rust) | `cargo` | crates.io API, GitHub |
| Go | `go` | go list, pkg.go.dev, GitHub |

## Output Format

The script outputs structured JSON to stdout:

```json
{
  "package": "lodash",
  "ecosystem": "npm",
  "timestamp": "2025-01-26T10:30:00Z",
  "registry_data": {
    "latest_version": "4.17.21",
    "license": "MIT",
    "description": "Lodash modular utilities",
    "repository_url": "https://github.com/lodash/lodash",
    "versions_count": 115,
    "publish_history": {...},
    "all_versions": [...]
  },
  "github_data": {
    "repository_url": "https://github.com/lodash/lodash",
    "pushed_at": "2024-12-15T10:30:00Z",
    "open_issues_count": 42,
    "stargazers_count": 58000,
    "contributors_count": 123,
    "community_health": {...}
  },
  "security_data": {},
  "dependency_footprint": {
    "direct_dependencies": 0,
    "total_dependencies": 0,
    "tree_depth": 1
  },
  "errors": [],
  "warnings": [
    "npm audit requires package.json context - skipping"
  ]
}
```

## Saving Output to File

```bash
python3 dependency_evaluator.py lodash npm > lodash-data.json
```

Then analyze the data file separately.

## Exit Codes

- **0**: Success (no errors, warnings are OK)
- **1**: Errors encountered (check `errors` array in output)

## What the Script Does

### For npm Packages
1. Runs `npm view <package> --json` for metadata
2. Runs `npm view <package> time --json` for version history
3. Runs `npm view <package> versions --json` for all versions
4. Extracts GitHub repository URL
5. Fetches GitHub API data (stars, issues, contributors, etc.)
6. Notes limitations (npm audit, npm ls require additional context)

### For PyPI Packages
1. Fetches `https://pypi.org/pypi/<package>/json` API
2. Parses package metadata and release history
3. Extracts GitHub repository URL if present
4. Fetches GitHub API data

### For Cargo Packages
1. Fetches `https://crates.io/api/v1/crates/<package>` API
2. Fetches `https://crates.io/api/v1/crates/<package>/versions` API
3. Parses crate metadata and downloads stats
4. Fetches GitHub API data

### For Go Modules
1. Runs `go list -m -json <module>`
2. Parses module metadata
3. Fetches GitHub API data if module is hosted on GitHub

### GitHub Data Gathering
- **Preferred**: Uses `gh` CLI if available (faster, authenticated)
- **Fallback**: Direct GitHub API calls via urllib (rate-limited to 60/hour)
- **Data collected**: Stars, forks, issues, last push, contributors, community health

## Limitations

### Commands Requiring Context
Some operations require additional context that the script cannot provide in isolation:

**npm audit**: Requires `package.json` and installed dependencies
```
Warning: "npm audit requires package.json context - skipping"
```

**npm ls**: Requires package to be installed locally
```
Warning: "npm ls requires package installation - skipping"
```

**Workaround**: Run these commands manually in your project directory after installing the package.

### GitHub API Rate Limiting
- **Unauthenticated**: 60 requests/hour
- **With gh CLI** (authenticated): 5000 requests/hour

If you hit rate limits:
```
Warning: "Access forbidden (rate limit?): https://api.github.com/..."
```

**Workaround**: Install and authenticate `gh` CLI, or wait for rate limit reset.

### Network Dependence
The script requires network access for:
- Package registry APIs (PyPI, crates.io)
- GitHub API

If offline or network issues occur, you'll see:
```
Warning: "Network error fetching https://...: ..."
```

## Error Handling

The script is designed to be resilient:

### Command Not Found
```
Warning: "Command not found: npm"
```
**Action**: Install the missing tool or use a different ecosystem

### Package Not Found
```
Error: "Resource not found: https://pypi.org/pypi/nonexistent-package/json"
```
**Action**: Check package name spelling

### Malformed Data
```
Warning: "Failed to parse npm view output"
```
**Action**: Check command output manually, may indicate tool version incompatibility

## Tips for Best Results

### 1. Install Ecosystem Tools
Install the tools for ecosystems you frequently evaluate:
```bash
# npm (comes with Node.js)
brew install node

# pip (comes with Python)
brew install python

# cargo (Rust)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# go
brew install go

# GitHub CLI (optional but recommended)
brew install gh
gh auth login
```

### 2. Use with Claude Code Workflow
The script integrates seamlessly with the dependency-evaluator skill:

```bash
# Gather data first
python3 scripts/dependency_evaluator.py lodash npm > data.json

# Then ask Claude to analyze it
# "Please analyze the dependency data in data.json and provide an evaluation report"
```

### 3. Batch Evaluations
Evaluate multiple packages:
```bash
for pkg in lodash react vue; do
  python3 dependency_evaluator.py $pkg npm > "$pkg-data.json"
done
```

### 4. Integrate with Scripts
Use in shell scripts or automation:
```bash
#!/bin/bash
OUTPUT=$(python3 dependency_evaluator.py "$1" npm 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "Evaluation failed for $1"
  echo "$OUTPUT" | jq '.errors'
else
  echo "Package: $(echo "$OUTPUT" | jq -r '.registry_data.latest_version')"
fi
```

## Interpreting Output

### Registry Data
- **latest_version**: Current stable version
- **license**: Package license (check compatibility)
- **versions_count**: Total number of releases (many = active, few = early/abandoned)
- **publish_history**: Dates of each version (check release cadence)

### GitHub Data
- **pushed_at**: Last commit date (recent = active maintenance)
- **open_issues_count**: Number of open issues (high = potential problems or popularity)
- **stargazers_count**: GitHub stars (popularity indicator)
- **contributors_count**: Number of contributors (bus factor assessment)
- **community_health.health_percentage**: 0-100 score (>70 is good)

### Warnings vs Errors
- **Warnings**: Non-critical issues, evaluation continues (e.g., "npm audit skipped")
- **Errors**: Critical failures, data may be incomplete (e.g., "package not found")

## Troubleshooting

### "Command not found: npm"
**Problem**: npm is not installed or not in PATH
**Solution**: Install Node.js or add npm to PATH

### "Access forbidden (rate limit?)"
**Problem**: GitHub API rate limit exceeded
**Solution**: Install and authenticate gh CLI, or wait 1 hour

### "Failed to parse npm view output"
**Problem**: npm output format changed or npm version incompatible
**Solution**: Update npm (`npm install -g npm@latest`) or report issue

### Output shows empty registry_data
**Problem**: Package doesn't exist or command failed
**Solution**: Check package name, review warnings/errors array

### Script hangs/times out
**Problem**: Network issue or slow API response
**Solution**: Check internet connection, script timeout is 30s per command

## Next Steps

After gathering data with the script:
1. Review the JSON output for completeness
2. Use the [SIGNAL_DETAILS.md](./SIGNAL_DETAILS.md) guide to interpret each signal
3. Apply the scoring framework from [SKILL.md](./SKILL.md)
4. Generate your evaluation report following [WORKFLOW.md](./WORKFLOW.md)

## Reporting Issues

If you encounter bugs or have suggestions:
1. Check the `errors` and `warnings` arrays in the output
2. Verify the issue isn't covered in Troubleshooting above
3. Report with: package name, ecosystem, full output, Python version, OS

## See Also

- [SKILL.md](./SKILL.md) - Main evaluation framework
- [WORKFLOW.md](./WORKFLOW.md) - Step-by-step evaluation process
- [COMMANDS.md](./COMMANDS.md) - Manual command reference
- [ERROR_HANDLING.md](./ERROR_HANDLING.md) - Fallback strategies
