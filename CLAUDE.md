# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace repository that distributes developer productivity plugins. The marketplace follows the official Claude Code plugin marketplace specification.

## Architecture

### Marketplace Structure
- **Root**: Contains marketplace configuration at `.claude-plugin/marketplace.json`
- **Plugin directories**: Each plugin is a subdirectory (e.g., `learnfrompast/`) containing:
  - `.claude-plugin/plugin.json` - Plugin manifest with metadata
  - `commands/` - Command definitions as markdown files with frontmatter
  - `README.md` - Plugin documentation

### Key Configuration Files

**/.claude-plugin/marketplace.json**
- Defines marketplace metadata (name, owner, description, version, repository)
- Lists all available plugins with their source paths and metadata
- Plugin entries include: name, source (relative path), description, version, license, repository, keywords, category

**learnfrompast/.claude-plugin/plugin.json**
- Plugin-specific manifest with name, description, version, author
- Includes homepage and repository URLs

### Plugin Command Structure

Commands are markdown files in `{plugin}/commands/` with:
- YAML frontmatter containing `description` field
- Markdown content with instructions for Claude Code to execute
- Commands should provide specific, actionable instructions for Claude's behavior

## Adding New Plugins

When adding a new plugin to this marketplace:

1. Create plugin directory at repository root: `{plugin-name}/`
2. Create plugin manifest: `{plugin-name}/.claude-plugin/plugin.json` with required fields (name, description, version, author)
3. Add commands in: `{plugin-name}/commands/{command-name}.md` with frontmatter
4. Add plugin entry to `.claude-plugin/marketplace.json` plugins array with metadata
5. Create plugin README: `{plugin-name}/README.md` documenting usage
6. Use kebab-case for plugin names, snake_case for command filenames

## Naming Conventions

- **Marketplace names**: kebab-case, no spaces (e.g., `princespaghetti-marketplace`)
- **Plugin names**: kebab-case, no spaces (e.g., `learnfrompast`)
- **Command files**: snake_case with `.md` extension (e.g., `review_history.md`)
- Use semantic versioning for all version fields

## Testing Plugins

To test plugin.json and marketplace.json files locally before publishing:
```bash
claude plugin validate .
```
This would be run at the level of the file
## Publishing Updates

This marketplace is published via GitHub at: https://github.com/princespaghetti/claude-marketplace

When making changes:
1. Update version numbers in both `marketplace.json` and affected `plugin.json` files
2. Update plugin metadata in marketplace.json if plugin details change
3. Ensure descriptions remain consistent between marketplace.json and plugin.json
4. Keep README files synchronized with plugin functionality
