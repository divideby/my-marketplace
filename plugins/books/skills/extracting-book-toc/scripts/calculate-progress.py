#!/usr/bin/env python3
"""
Скрипт для расчёта прогресса чтения книги.

Поддерживает три метода расчёта:
1. По весам [w:N] — относительный объём глав из ЛитРес
2. По страницам [N-M] — диапазоны страниц
3. По главам (fallback) — простой подсчёт отмеченных пунктов

Использование:
    python calculate-progress.py path/to/book.md
    python calculate-progress.py --format json path/to/book.md
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass


@dataclass
class ProgressItem:
    """Элемент прогресса (глава)."""
    title: str
    completed: bool
    weight: int | None = None
    pages_start: int | None = None
    pages_end: int | None = None
    indent: int = 0


def parse_progress_section(content: str) -> list[ProgressItem]:
    """Извлечь чеклист из секции ## Прогресс."""
    items = []

    # Найти секцию Прогресс
    progress_match = re.search(r'## Прогресс\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not progress_match:
        return items

    progress_text = progress_match.group(1)

    # Парсить каждую строку чеклиста
    for line in progress_text.split('\n'):
        # Формат: "- [x] Название [w:123]" или "- [ ] Название [1-89]"
        match = re.match(r'^(\s*)-\s*\[([ xX])\]\s*(.+)$', line)
        if not match:
            continue

        indent = len(match.group(1))
        completed = match.group(2).lower() == 'x'
        title_part = match.group(3).strip()

        # Извлечь вес [w:N]
        weight = None
        weight_match = re.search(r'\[w:(\d+)\]', title_part)
        if weight_match:
            weight = int(weight_match.group(1))
            title_part = re.sub(r'\s*\[w:\d+\]', '', title_part)

        # Извлечь диапазон страниц [N-M]
        pages_start = None
        pages_end = None
        pages_match = re.search(r'\[(\d+)-(\d+)\]', title_part)
        if pages_match:
            pages_start = int(pages_match.group(1))
            pages_end = int(pages_match.group(2))
            title_part = re.sub(r'\s*\[\d+-\d+\]', '', title_part)

        items.append(ProgressItem(
            title=title_part.strip(),
            completed=completed,
            weight=weight,
            pages_start=pages_start,
            pages_end=pages_end,
            indent=indent,
        ))

    return items


def get_total_pages(content: str) -> int | None:
    """Извлечь общее количество страниц из frontmatter."""
    match = re.search(r'^total:\s*(\d+)', content, re.MULTILINE)
    if match:
        return int(match.group(1))
    return None


def calculate_progress(items: list[ProgressItem], total_pages: int | None = None) -> dict:
    """Рассчитать прогресс по книге.

    Возвращает словарь с полями:
    - total_items: общее количество пунктов
    - completed_items: количество выполненных
    - progress_by_items: процент по количеству пунктов
    - progress_by_weight: процент по весам (если есть)
    - progress_by_pages: процент по страницам (если есть)
    - progress: итоговый прогресс (лучший из доступных методов)
    - method: использованный метод (weight/pages/items)
    """
    if not items:
        return {
            "total_items": 0,
            "completed_items": 0,
            "progress_by_items": 0,
            "progress": 0,
            "method": "items",
        }

    total_items = len(items)
    completed_items = sum(1 for item in items if item.completed)
    progress_by_items = round(completed_items / total_items * 100, 1)

    result = {
        "total_items": total_items,
        "completed_items": completed_items,
        "progress_by_items": progress_by_items,
        "progress": progress_by_items,
        "method": "items",
    }

    # Расчёт по весам
    items_with_weight = [item for item in items if item.weight is not None]
    if items_with_weight:
        total_weight = sum(item.weight for item in items_with_weight)
        completed_weight = sum(item.weight for item in items_with_weight if item.completed)
        if total_weight > 0:
            progress_by_weight = round(completed_weight / total_weight * 100, 1)
            result["total_weight"] = total_weight
            result["completed_weight"] = completed_weight
            result["progress_by_weight"] = progress_by_weight
            result["progress"] = progress_by_weight
            result["method"] = "weight"

    # Расчёт по страницам
    items_with_pages = [item for item in items if item.pages_start is not None]
    if items_with_pages:
        completed_pages = sum(
            item.pages_end - item.pages_start + 1
            for item in items_with_pages
            if item.completed
        )
        # Используем total из frontmatter или последнюю страницу
        if total_pages:
            progress_by_pages = round(completed_pages / total_pages * 100, 1)
        else:
            max_page = max(item.pages_end for item in items_with_pages)
            progress_by_pages = round(completed_pages / max_page * 100, 1)

        result["completed_pages"] = completed_pages
        result["total_pages"] = total_pages or max(item.pages_end for item in items_with_pages)
        result["progress_by_pages"] = progress_by_pages
        # Страницы приоритетнее весов
        result["progress"] = progress_by_pages
        result["method"] = "pages"

    return result


def format_progress_human(result: dict) -> str:
    """Форматировать результат для человека."""
    lines = []

    progress = result["progress"]
    method = result["method"]

    if method == "weight":
        lines.append(f"Прогресс: {progress}% (по объёму)")
        lines.append(f"  Глав: {result['completed_items']}/{result['total_items']}")
        lines.append(f"  Вес: {result['completed_weight']}/{result['total_weight']}")
    elif method == "pages":
        lines.append(f"Прогресс: {progress}% (по страницам)")
        lines.append(f"  Глав: {result['completed_items']}/{result['total_items']}")
        lines.append(f"  Страниц: {result['completed_pages']}/{result['total_pages']}")
    else:
        lines.append(f"Прогресс: {progress}% (по главам)")
        lines.append(f"  Глав: {result['completed_items']}/{result['total_items']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Рассчитать прогресс чтения книги из markdown-файла"
    )
    parser.add_argument("file", help="Путь к файлу заметки книги (.md)")
    parser.add_argument("--format", choices=["json", "human"], default="human",
                        help="Формат вывода (default: human)")

    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {args.file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}", file=sys.stderr)
        sys.exit(1)

    items = parse_progress_section(content)
    if not items:
        print("Секция ## Прогресс не найдена или пуста", file=sys.stderr)
        sys.exit(1)

    total_pages = get_total_pages(content)
    result = calculate_progress(items, total_pages)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_progress_human(result))


if __name__ == "__main__":
    main()
