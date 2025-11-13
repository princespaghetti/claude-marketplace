# learnfrompast

Analyzes your shell command history to identify usage patterns, productivity improvements, automation opportunities, and skill development areas based on your actual shell workflows.

## Overview

This Claude Code plugin provides personalized insights into your command-line habits by analyzing your zsh or bash history to reveal patterns, inefficiencies, and opportunities for improvement.

## Installation

First, add the marketplace to Claude Code:

```bash
/plugin marketplace add princespaghetti/claude-marketplace
```

Then install this plugin:

```bash
/plugin install learnfrompast@princespaghetti-marketplace
```

## Usage

Once installed, use the command to analyze your shell command history:

```bash
/review_history
```

**Note on command invocation**: If there are no naming conflicts with other plugins or built-in commands, you can use the short form `/review_history`. However, if Claude Code detects a namespace collision, you may need to use the fully-qualified form:

```bash
/learnfrompast:review_history
```

The namespaced format (`plugin-name:command-name`) will always work regardless of conflicts.

## What It Analyzes

### Command Patterns
- Top 10-15 most frequent commands with usage counts
- Command categorization (version control, package management, file operations, development tools, etc.)
- Repeated command sequences that could be automated

### Productivity Opportunities
- Long or repetitive commands suitable for aliasing (prioritized by frequency × length)
- Command chains executed together frequently
- Excessive directory navigation patterns that could be optimized

### Deliverables

The plugin generates a concise, actionable report including:
- **Summary**: Brief overview of your command patterns and workflow (2-3 sentences)
- **Top Commands**: Your 10-15 most frequent commands with counts
- **Improvement Opportunities**: 3-4 specific recommendations with Impact/Effort ratings
- **Suggested Aliases & Functions**: Ready-to-use, copy-pasteable code for your ~/.zshrc or ~/.bashrc
- **Quick Wins**: 2-3 improvements that take less than 5 minutes to implement

## Features

- Analyzes both zsh and bash history files
- Provides concrete, actionable recommendations
- Prioritizes suggestions by impact (frequency × time saved)
- Generates working code, not templates
- Encouraging tone that highlights existing strengths

## Example Output

The report will help you:
- Discover commands you use most often
- Find opportunities to create time-saving aliases
- Identify command chains that could be automated
- Improve your shell workflow efficiency

## Requirements

- Access to `~/.zsh_history` or `~/.bash_history`
- Claude Code installation

## License

MIT License - see [LICENSE](../LICENSE) for details.
