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

Analyzes your shell command history to identify usage patterns, productivity improvements, automation opportunities, and skill development areas based on your actual shell workflows.

**Features:**
- Identifies most frequent commands and patterns
- Suggests high-impact aliases and automation opportunities
- Provides actionable productivity improvements
- Analyzes command patterns by category (git, file operations, development tools, etc.)
- Generates ready-to-use shell functions and aliases

**Usage:**
```bash
/review_history
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
