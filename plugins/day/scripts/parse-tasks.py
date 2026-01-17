#!/usr/bin/env python3
"""
Parse tasks from Obsidian vault markdown files.

Usage:
    python parse-tasks.py [--due-today | --overdue | --no-date | --inbox] [--path PATH]

Output: JSON array of tasks with metadata.
"""

import argparse
import json
import os
import re
from datetime import datetime, date
from pathlib import Path

VAULT_PATH = Path.cwd()  # Use current directory as vault root
TODAY = date.today().isoformat()

# Task regex pattern
# Handles:
#   - [ ] text #task (regular markdown, kanban)
#   - > - [ ] text #task (callout blocks)
#   - - [ ] #task text (tag at start)
TASK_PATTERN = re.compile(
    r'^[>\s]*- \[([ xX])\]\s*(.+)',
    re.MULTILINE
)

def parse_tasks_from_file(filepath: Path) -> list:
    """Extract tasks from a markdown file."""
    tasks = []
    try:
        content = filepath.read_text(encoding='utf-8')
        for match in TASK_PATTERN.finditer(content):
            status, raw_text = match.groups()

            # Skip if not a #task
            if '#task' not in raw_text:
                continue

            # Extract priority emoji
            priority = ''
            for p in ['⏫', '🔼', '🔽', '⚡']:
                if p in raw_text:
                    priority = p
                    break

            # Extract due date
            due_match = re.search(r'📅\s*(\d{4}-\d{2}-\d{2})', raw_text)
            due_date = due_match.group(1) if due_match else ''

            # Clean text: remove tags, priority, dates
            text = raw_text
            text = re.sub(r'#\w+', '', text)  # remove tags
            text = re.sub(r'[⏫🔼🔽⚡]', '', text)  # remove priority
            text = re.sub(r'📅\s*\d{4}-\d{2}-\d{2}', '', text)  # remove due date
            text = re.sub(r'✅\s*\d{4}-\d{2}-\d{2}', '', text)  # remove done date
            text = text.strip()

            tasks.append({
                'file': str(filepath.relative_to(VAULT_PATH)),
                'text': text,
                'raw_text': raw_text,
                'done': status.lower() == 'x',
                'priority': priority,
                'due': due_date,
                'line': content[:match.start()].count('\n') + 1
            })
    except Exception as e:
        pass
    return tasks

def collect_tasks(path: Path = VAULT_PATH) -> list:
    """Collect all tasks from vault."""
    all_tasks = []

    # Scan markdown files
    for md_file in path.rglob('*.md'):
        # Skip templates and archives
        if '_templates' in str(md_file) or 'TG Channel' in str(md_file):
            continue
        all_tasks.extend(parse_tasks_from_file(md_file))

    return all_tasks

def filter_tasks(tasks: list, filter_type: str) -> list:
    """Filter tasks by criteria."""
    today = date.today()

    if filter_type == 'due-today':
        return [t for t in tasks if not t['done'] and t['due'] == TODAY]

    elif filter_type == 'overdue':
        return [t for t in tasks if not t['done'] and t['due'] and t['due'] < TODAY]

    elif filter_type == 'no-date':
        return [t for t in tasks if not t['done'] and not t['due']]

    elif filter_type == 'inbox':
        return [t for t in tasks if not t['done'] and '#inbox' in t.get('raw_text', '')]

    elif filter_type == 'undone':
        return [t for t in tasks if not t['done']]

    return tasks

def main():
    parser = argparse.ArgumentParser(description='Parse Obsidian tasks')
    parser.add_argument('--due-today', action='store_true', help='Tasks due today')
    parser.add_argument('--overdue', action='store_true', help='Overdue tasks')
    parser.add_argument('--no-date', action='store_true', help='Tasks without due date')
    parser.add_argument('--inbox', action='store_true', help='Tasks with #inbox tag')
    parser.add_argument('--undone', action='store_true', help='All undone tasks')
    parser.add_argument('--path', type=str, help='Custom vault path')

    args = parser.parse_args()

    vault = Path(args.path) if args.path else VAULT_PATH
    tasks = collect_tasks(vault)

    if args.due_today:
        tasks = filter_tasks(tasks, 'due-today')
    elif args.overdue:
        tasks = filter_tasks(tasks, 'overdue')
    elif args.no_date:
        tasks = filter_tasks(tasks, 'no-date')
    elif args.inbox:
        tasks = filter_tasks(tasks, 'inbox')
    elif args.undone:
        tasks = filter_tasks(tasks, 'undone')

    # Sort by priority
    priority_order = {'⏫': 0, '🔼': 1, '⚡': 1, '': 2, '🔽': 3}
    tasks.sort(key=lambda t: priority_order.get(t['priority'], 2))

    print(json.dumps(tasks, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
