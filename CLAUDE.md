# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin marketplace repository. It provides a local collection of plugins that can be loaded into Claude Code.

## Architecture

### Marketplace Configuration
- `.claude-plugin/marketplace.json` - Root marketplace manifest listing all available plugins with their sources and descriptions

### Plugin Structure
Each plugin lives in `plugins/<plugin-name>/` with:
- `.claude-plugin/plugin.json` - Plugin metadata (name, description, version, author)
- `commands/` - Directory containing command definitions as markdown files

### Command Format
Commands are defined as markdown files with YAML frontmatter:
```markdown
---
description: Short description shown in command list
---

# Command Name

Instructions for Claude when this command is invoked.
```

## Creating a New Plugin

1. Create a directory under `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with plugin metadata
3. Add commands in `commands/<command-name>.md`
4. Register the plugin in `.claude-plugin/marketplace.json`
