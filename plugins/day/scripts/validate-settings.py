#!/usr/bin/env python3
"""
Validate Day plugin settings and vault structure.

Usage:
    python validate-settings.py [--path PATH]

Output: JSON with validation status and issues.
"""

import argparse
import json
import re
from pathlib import Path

VAULT_PATH = Path.cwd()
SETTINGS_FILE = '.claude/day-patterns.md'

REQUIRED_SECTIONS = [
    '## Утренняя рутина',
    '## Фиксированные регулярные события',
    '## Временные слоты',
]

REQUIRED_DIRS = ['Dailies', 'Base', 'Base/Meetings']
REQUIRED_FILES = ['Inbox.md']


def validate_settings(vault: Path) -> dict:
    """Validate settings file exists and has required sections."""
    settings_path = vault / SETTINGS_FILE
    result = {
        'file': str(settings_path),
        'exists': False,
        'sections_found': [],
        'sections_missing': [],
        'valid': False
    }

    if not settings_path.exists():
        result['sections_missing'] = [s.replace('## ', '') for s in REQUIRED_SECTIONS]
        result['error'] = f'Settings file not found: {SETTINGS_FILE}'
        return result

    result['exists'] = True
    content = settings_path.read_text(encoding='utf-8')

    for section in REQUIRED_SECTIONS:
        if section in content:
            result['sections_found'].append(section.replace('## ', ''))
        else:
            result['sections_missing'].append(section.replace('## ', ''))

    result['valid'] = len(result['sections_missing']) == 0
    return result


def validate_vault_structure(vault: Path) -> dict:
    """Validate vault has required directories and files."""
    result = {
        'dirs_found': [],
        'dirs_missing': [],
        'files_found': [],
        'files_missing': [],
        'valid': False
    }

    for dir_name in REQUIRED_DIRS:
        dir_path = vault / dir_name
        if dir_path.is_dir():
            result['dirs_found'].append(dir_name)
        else:
            result['dirs_missing'].append(dir_name)

    for file_name in REQUIRED_FILES:
        file_path = vault / file_name
        if file_path.is_file():
            result['files_found'].append(file_name)
        else:
            result['files_missing'].append(file_name)

    result['valid'] = (
        len(result['dirs_missing']) == 0 and
        len(result['files_missing']) == 0
    )
    return result


def main():
    parser = argparse.ArgumentParser(description='Validate Day plugin settings')
    parser.add_argument('--path', type=str, help='Custom vault path')
    parser.add_argument('--quiet', action='store_true', help='Only show errors')

    args = parser.parse_args()
    vault = Path(args.path) if args.path else VAULT_PATH

    settings = validate_settings(vault)
    vault_struct = validate_vault_structure(vault)

    result = {
        'vault': str(vault),
        'settings': settings,
        'structure': vault_struct,
        'valid': settings['valid'] and vault_struct['valid']
    }

    if args.quiet and result['valid']:
        print(json.dumps({'valid': True}, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    exit(0 if result['valid'] else 1)


if __name__ == '__main__':
    main()
