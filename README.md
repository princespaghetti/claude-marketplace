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

Analyzes your development workflows to identify productivity improvements and automation opportunities based on your actual shell, git, and Claude usage patterns.

**Capabilities:**
- **Claude Workflow Analysis** (workflow-analyzer skill): Detects repeated multi-step workflows in your Claude sessions and generates custom commands to automate them. Shows time savings estimates and creates ready-to-use command definitions. Simply ask Claude to "analyze my workflows" to activate.
- **Shell History Analysis** (`/review_history` command): Analyzes zsh/bash history for command patterns, suggests aliases and automation opportunities
- **Git Workflow Patterns** (git-workflow-patterns skill): Identifies git habits, analyzes commit/branch/collaboration patterns, and suggests workflow improvements. Activates automatically when discussing git workflows.

**[Full documentation →](learnfrompast/README.md)**

**Quick install:**
```bash
/plugin install learnfrompast@princespaghetti-marketplace
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
