# princespaghetti-marketplace

A collection of developer productivity plugins for Claude Code.

## About

This marketplace provides curated plugins designed to enhance your development workflow with Claude Code. Each plugin is focused on improving productivity, providing insights, and automating common tasks.

## Installation

First, add this marketplace to Claude Code:

```bash
/plugin marketplace add princespaghetti/claude-marketplace
```

Then install individual plugins:

```bash
/plugin install learnfrompast@princespaghetti-marketplace
```

Or browse and install interactively:

```bash
/plugin
```

## Available Plugins

### learnfrompast

Analyzes your development workflows to identify productivity improvements and automation opportunities based on your actual shell and git usage patterns.

**Capabilities:**
- **Shell History Analysis** (`/review_history` command): Analyzes zsh/bash history for command patterns, suggests aliases and automation opportunities
- **Git Workflow Patterns** (autonomous skill): Identifies git habits, analyzes commit/branch/collaboration patterns, and suggests workflow improvements

**[Full documentation →](learnfrompast/README.md)**

**Quick install:**
```bash
/plugin install learnfrompast@princespaghetti-marketplace
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
