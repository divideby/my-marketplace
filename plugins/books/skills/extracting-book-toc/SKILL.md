---
name: extracting-book-toc
description: Extracts table of contents from books using LitRes, Open Library, or Google Books APIs. Use when the user asks to get a book's table of contents, chapters list, or wants to create a reading progress checklist for a book.
---

# Extracting Book Table of Contents

Extracts TOC from book sources and converts it to a markdown progress checklist.

## Workflow

```
Progress:
- [ ] Step 1: Get book identifier (LitRes ID, ISBN, or title)
- [ ] Step 2: Run fetch script
- [ ] Step 3: Handle result (success or fallback to manual)
- [ ] Step 4: Update book note with checklist
```

## Step 1: Get book identifier

Ask the user which book needs a TOC. Get one of:

- **LitRes ID** (recommended for Russian books): Number from URL `litres.ru/book/author/title-48514275/` → `48514275`
- **ISBN**: For international books
- **Title**: As fallback search

## Step 2: Run fetch script

```bash
# LitRes (recommended for Russian books)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --litres-id "48514275"

# Open Library / Google Books (for English books)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --isbn "9781455586691"
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --title "Deep Work"
```

Output format options:
- `--format markdown` (default): Progress checklist
- `--format json`: Raw chapter list

For metadata only (no TOC):
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/extracting-book-toc/scripts/fetch-toc.py" --litres-id "48514275" --info
```

## Step 3: Handle result

**If TOC found**: Script outputs markdown checklist ready to use.

**If TOC not found**: Ask user to paste TOC manually:

> Table of contents not found automatically. Please copy it from the book or publisher's website.

Example format:
```
Introduction
Chapter 1. Title
Chapter 2. Title
...
Conclusion
```

Then convert to checklist:
```markdown
## Progress

- [ ] Introduction
- [ ] Chapter 1. Title
- [ ] Chapter 2. Title
- [ ] Conclusion
```

## Step 4: Update book note

Replace the "Progress" section in the book's note file (`Base/Book Name.md`) with the new checklist.

## Tips

- For technical books: include subsections if available
- For fiction: chapters are usually sufficient
- Optionally add page ranges: `- [ ] Chapter 1 (pp. 1-30)`
