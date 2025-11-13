# learnfrompast

Analyzes your shell command history and git workflows to identify usage patterns, productivity improvements, automation opportunities, and skill development areas based on your actual development workflows.

## Overview

This Claude Code plugin provides personalized insights into your development habits by analyzing your zsh/bash history and git workflows to reveal patterns, inefficiencies, and opportunities for improvement.

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

### Shell History Analysis (Command)

Explicitly analyze your shell command history using the command:

```bash
/review_history
```

**Note on command invocation**: If there are no naming conflicts with other plugins or built-in commands, you can use the short form `/review_history`. However, if Claude Code detects a namespace collision, you may need to use the fully-qualified form:

```bash
/learnfrompast:review_history
```

The namespaced format (`plugin-name:command-name`) will always work regardless of conflicts.

### Git Workflow Analysis (Skill)

The plugin also includes a **git-workflow-patterns** skill that activates automatically when you:
- Mention git workflows, commits, branches, or rebasing
- Express frustration with git operations
- Work with merge conflicts, force pushes, or PRs
- Ask about git best practices or workflow optimization

The skill analyzes your git history and provides personalized recommendations based on your actual patterns. No explicit command needed—Claude activates it contextually when relevant.

## What It Analyzes

### Shell Command Patterns (via `/review_history` command)
- Top 10-15 most frequent commands with usage counts
- Command categorization (version control, package management, file operations, development tools, etc.)
- Repeated command sequences that could be automated
- Long or repetitive commands suitable for aliasing (prioritized by frequency × length)
- Command chains executed together frequently
- Excessive directory navigation patterns that could be optimized

**Deliverables**:
- **Summary**: Brief overview of your command patterns and workflow (2-3 sentences)
- **Top Commands**: Your 10-15 most frequent commands with counts
- **Improvement Opportunities**: 3-4 specific recommendations with Impact/Effort ratings
- **Suggested Aliases & Functions**: Ready-to-use, copy-pasteable code for your ~/.zshrc or ~/.bashrc
- **Quick Wins**: 2-3 improvements that take less than 5 minutes to implement

### Git Workflow Patterns (via `git-workflow-patterns` skill)

The skill analyzes your git history to identify:

**Commit Patterns**:
- Message consistency and format
- Commit size (lines changed per commit)
- Commit frequency and batching behavior
- WIP/fixup commits that should be squashed
- Test commit patterns

**Branch Patterns**:
- Naming conventions and consistency
- Branch lifespan (time from creation to merge)
- Abandoned branches
- Branch size and long-lived branches (20+ commits)

**Collaboration Patterns**:
- Solo vs. co-authored commits
- Merge vs. rebase preferences
- Force push frequency and safety
- PR size and review patterns

**Error Recovery Patterns**:
- Reflog usage (indicating mistakes/uncertainty)
- Reset/revert patterns
- Cherry-pick frequency
- Stash accumulation

**Workflow Efficiency**:
- Repeated command sequences (alias opportunities)
- Conflict patterns in specific files
- Context switching frequency

**Deliverables**:
- Personalized recommendations based on your actual git behavior
- Safety improvements (e.g., `--force-with-lease` instead of `--force`)
- Git aliases and config suggestions
- Workflow optimizations (branch strategy, commit strategy, etc.)
- Quick wins for immediate improvement

## Features

- **Dual analysis**: Shell command history (command) + Git workflow patterns (skill)
- **Autonomous activation**: Git skill activates contextually when relevant
- **Explicit control**: Shell analysis via explicit `/review_history` command
- **Concrete recommendations**: Actionable, specific suggestions with working code
- **Impact prioritization**: Suggestions ranked by frequency × time saved
- **Privacy-conscious**: Local analysis, no external data transmission
- **Copy-pasteable solutions**: Ready-to-use aliases, configs, and scripts
- **Encouraging feedback**: Highlights strengths while suggesting improvements

## Example Scenarios

### Shell History Analysis
Run `/review_history` to:
- Discover your most-used commands
- Find opportunities to create time-saving aliases
- Identify command chains that could be automated
- Improve overall shell workflow efficiency

### Git Workflow Analysis (Automatic)

**Scenario 1**: You mention "I always mess up rebasing"
- Skill activates, analyzes your reflog and reset patterns
- Suggests backup workflow before rebasing
- Provides safe rebase aliases based on your habits

**Scenario 2**: Working on a branch with 40+ commits
- Skill detects long-lived branch pattern
- Analyzes your historical PR sizes and review times
- Suggests breaking into smaller PRs with specific split points

**Scenario 3**: You ask "Why do I keep having merge conflicts?"
- Skill identifies files that conflict frequently
- Analyzes your conflict resolution patterns
- Suggests git config changes and workflow improvements

## Requirements

- Claude Code installation
- Access to `~/.zsh_history` or `~/.bash_history` for shell analysis
- Git repository for git workflow analysis

## License

MIT License - see [LICENSE](../LICENSE) for details.
