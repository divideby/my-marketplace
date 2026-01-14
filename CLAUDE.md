# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin marketplace repository. It provides a local collection of plugins that can be loaded into Claude Code.

## Available Plugins

| Plugin | Description | Commands |
| ------ | ----------- | -------- |
| **specs** | Создание спецификаций проектов (L0/L1) | `/specs:new` |
| **books** | Чтение книг по методологии Поварнина | `/books:new`, `/books:session`, `/books:progress`, `/books:finish` |
| **day** | Протокол дня: планирование с Obsidian-задачами | `/day:today`, `/day:checkin` |

See `plugins/<name>/CLAUDE.md` for detailed plugin documentation.

## Architecture

### Marketplace Configuration

- `.claude-plugin/marketplace.json` - Root marketplace manifest listing all available plugins with their sources and descriptions

### Plugin Structure

Each plugin lives in `plugins/<plugin-name>/` with:

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (name, description, version, author)
├── commands/            # Slash commands (user-invoked)
│   └── <command>.md
└── skills/              # Agent skills (model-invoked, auto-triggered)
    └── <skill-name>/
        ├── SKILL.md
        └── scripts/     # Optional utility scripts
```

**Important:** `commands/`, `skills/`, `agents/`, `hooks/` must be at plugin root level, NOT inside `.claude-plugin/`.

### Command Format

Commands are user-invoked via `/plugin:command`. Defined as markdown with YAML frontmatter:

```markdown
---
description: Short description shown in command list
---

# Command Name

Instructions for Claude when this command is invoked.
```

### Skill Format

Skills are model-invoked — Claude decides when to use them based on task context. Each skill needs a `SKILL.md`:

```markdown
---
name: skill-name
description: What this skill does and when to use it. Claude uses this to decide when to activate the skill.
---

# Skill Name

Instructions Claude follows when skill is active.
```

**SKILL.md requirements:**
- `name`: max 64 chars, lowercase letters/numbers/hyphens only
- `description`: max 1024 chars, must include WHAT it does AND WHEN to use it

## Creating a New Plugin

1. Create directory `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with metadata
3. Add commands in `commands/<command-name>.md`
4. Add skills in `skills/<skill-name>/SKILL.md` (optional)
5. Register in `.claude-plugin/marketplace.json`

## Versioning

Marketplace подключается через GitHub — **обновляй версию** в `plugin.json` при значимых изменениях:

- `0.1.0` → `0.1.1` — фиксы, мелкие изменения
- `0.1.0` → `0.2.0` — новая функциональность
- `0.x.x` → `1.0.0` — стабильный релиз

Без обновления версии Claude Code может не подтянуть изменения из кеша.

---

## Plugin Development Reference

Reference documentation for creating high-quality plugins. Consult when improving existing plugins or creating new ones.

### Skills Best Practices

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

#### Core Principles

1. **Concise is key** — Context window is shared. Only add what Claude doesn't already know.
2. **Set appropriate degrees of freedom:**
   - High freedom (text instructions): multiple approaches valid
   - Medium freedom (pseudocode/templates): preferred pattern exists
   - Low freedom (exact scripts): operations are fragile
3. **Test with all models** — What works for Opus may need more detail for Haiku.

#### SKILL.md Structure

- Keep body under 500 lines
- Use progressive disclosure: main instructions in SKILL.md, details in separate files
- Keep references one level deep from SKILL.md
- For files >100 lines, add table of contents

#### Writing Effective Descriptions

- Write in third person ("Processes files..." not "I can help you...")
- Be specific, include key terms and triggers
- Example: `"Extracts table of contents from books using LitRes, Open Library APIs. Use when user asks for book chapters, TOC, or reading progress checklist."`

#### Workflow Pattern

For complex tasks, provide a checklist Claude can track:

```markdown
## Workflow

Copy this checklist:
- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: ...

**Step 1: ...**
[Instructions]
```

#### Feedback Loop Pattern

Run validator → fix errors → repeat:

```markdown
1. Make changes
2. Validate: `python scripts/validate.py`
3. If fails → fix and re-validate
4. Only proceed when validation passes
```

#### Scripts in Skills

Benefits of utility scripts over generated code:
- More reliable
- Save tokens (no code in context)
- Ensure consistency

Make clear whether to EXECUTE or READ the script:
- Execute: "Run `analyze.py` to extract fields"
- Read: "See `analyze.py` for the algorithm"

#### Anti-Patterns to Avoid

- Windows-style paths (`\` instead of `/`)
- Too many options without a default
- Time-sensitive information
- Inconsistent terminology
- Deeply nested file references

### Skills Architecture

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

#### Three Levels of Loading

| Level | When Loaded | Content |
|-------|-------------|---------|
| 1. Metadata | Always (startup) | `name` and `description` from frontmatter |
| 2. Instructions | When skill triggered | SKILL.md body |
| 3. Resources | As needed | Additional files, scripts |

#### Progressive Disclosure

- Metadata loaded at startup (~100 tokens per skill)
- SKILL.md body loaded only when relevant
- Scripts executed without loading code into context (only output)
- No context penalty for bundled files until accessed

### Plugin Directory Reference

Source: https://code.claude.com/docs/en/plugins

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # ONLY manifest here
├── commands/            # User-invoked slash commands
├── skills/              # Model-invoked capabilities
├── agents/              # Custom agents
└── hooks/               # Event hooks
```

**Common mistake:** Don't put `commands/`, `skills/`, etc. inside `.claude-plugin/`.
