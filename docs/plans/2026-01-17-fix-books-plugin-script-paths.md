# Fix Books Plugin Script Paths Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix script paths in books plugin so scripts work when called from any project (not just from marketplace directory)

**Architecture:** Replace hardcoded relative paths `plugins/books/skills/...` with `${CLAUDE_PLUGIN_ROOT}` variable that resolves to the actual plugin installation directory at runtime

**Tech Stack:** Markdown commands, shell variable interpolation

---

## Problem Analysis

Current commands use relative paths:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py
```

This only works when CWD is the marketplace directory. When the plugin is installed globally via `~/.claude/plugins/cache/`, the scripts are at:
```
~/.claude/plugins/cache/<org>/<plugin>/<version>/skills/extracting-book-toc/scripts/
```

Solution: Use `${CLAUDE_PLUGIN_ROOT}` which Claude Code expands to the plugin's root directory.

---

## Task 1: Fix `/books:new` Command

**Files:**
- Modify: `plugins/books/commands/new.md:22-26,31-35`

**Step 1: Read current file state**

Run: `cat plugins/books/commands/new.md` (already done in exploration)

**Step 2: Replace first script path**

Replace line 23:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --litres-id "48514275" --info
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --litres-id "48514275" --info
```

**Step 3: Replace second script path**

Replace line 26:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --title "Deep Work" --info
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --title "Deep Work" --info
```

**Step 4: Replace third script path**

Replace line 35:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --litres-id "48514275"
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --litres-id "48514275"
```

**Step 5: Verify changes**

Run: `grep -n "CLAUDE_PLUGIN_ROOT" plugins/books/commands/new.md`
Expected: 3 lines with the updated paths

**Step 6: Commit**

```bash
git add plugins/books/commands/new.md
git commit -m "$(cat <<'EOF'
fix(books): use CLAUDE_PLUGIN_ROOT for fetch-toc.py paths in /books:new

Replace hardcoded relative paths with ${CLAUDE_PLUGIN_ROOT} variable
so scripts work when plugin is installed globally.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Fix `/books:progress` Command

**Files:**
- Modify: `plugins/books/commands/progress.md:22`

**Step 1: Replace script path**

Replace line 22:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/calculate-progress.py "Base/Название книги.md" --format json
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/calculate-progress.py" "Base/Название книги.md" --format json
```

**Step 2: Verify changes**

Run: `grep -n "CLAUDE_PLUGIN_ROOT" plugins/books/commands/progress.md`
Expected: 1 line with the updated path

**Step 3: Commit**

```bash
git add plugins/books/commands/progress.md
git commit -m "$(cat <<'EOF'
fix(books): use CLAUDE_PLUGIN_ROOT for calculate-progress.py path

Replace hardcoded relative path with ${CLAUDE_PLUGIN_ROOT} variable
so script works when plugin is installed globally.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Fix `extracting-book-toc` Skill

**Files:**
- Modify: `plugins/books/skills/extracting-book-toc/SKILL.md:32-36,45`

**Step 1: Replace first script path**

Replace line 32:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --litres-id "48514275"
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --litres-id "48514275"
```

**Step 2: Replace second script path**

Replace line 35:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --isbn "9781455586691"
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --isbn "9781455586691"
```

**Step 3: Replace third script path**

Replace line 36:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --title "Deep Work"
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --title "Deep Work"
```

**Step 4: Replace fourth script path**

Replace line 45:
```bash
python3 plugins/books/skills/extracting-book-toc/scripts/fetch-toc.py --litres-id "48514275" --info
```
With:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --litres-id "48514275" --info
```

**Step 5: Verify changes**

Run: `grep -n "CLAUDE_PLUGIN_ROOT" plugins/books/skills/extracting-book-toc/SKILL.md`
Expected: 4 lines with the updated paths

**Step 6: Commit**

```bash
git add plugins/books/skills/extracting-book-toc/SKILL.md
git commit -m "$(cat <<'EOF'
fix(books): use CLAUDE_PLUGIN_ROOT for fetch-toc.py paths in skill

Replace hardcoded relative paths with ${CLAUDE_PLUGIN_ROOT} variable
so skill works when plugin is installed globally.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Update Plugin Version

**Files:**
- Modify: `plugins/books/.claude-plugin/plugin.json`

**Step 1: Bump version**

Change version from `"1.1.0"` to `"1.1.1"` (patch version for bug fix).

**Step 2: Verify changes**

Run: `cat plugins/books/.claude-plugin/plugin.json`
Expected: `"version": "1.1.1"`

**Step 3: Commit**

```bash
git add plugins/books/.claude-plugin/plugin.json
git commit -m "$(cat <<'EOF'
chore(books): bump version to 1.1.1

Version bump for script path fixes.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Final Verification

After all tasks complete:

1. Search all files for old paths to ensure none remain:
   ```bash
   grep -r "plugins/books/skills" plugins/books/
   ```
   Expected: No matches (empty output)

2. Search for new paths to confirm updates:
   ```bash
   grep -r "CLAUDE_PLUGIN_ROOT" plugins/books/
   ```
   Expected: 8 matches (3 in new.md, 1 in progress.md, 4 in SKILL.md)
