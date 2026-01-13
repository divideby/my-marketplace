#!/usr/bin/env python3
"""
Скрипт для извлечения оглавления книги.
Источники: ЛитРес, Open Library, Google Books.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
from html import unescape

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}


def fetch_url(url: str, timeout: int = 15) -> str | None:
    """Загрузить страницу по URL."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}", file=sys.stderr)
        return None


# ==================== ЛитРес ====================

# Поиск по названию на ЛитРес не работает (сайт использует JS-рендеринг)
# Используйте --litres-id с ID из URL книги


def fetch_litres_toc(book_id: str) -> list[dict] | None:
    """Получить оглавление с ЛитРес по ID книги."""
    # Определяем сервер по предпоследней цифре ID
    server_num = book_id[-2] if len(book_id) >= 2 else "0"
    toc_url = f"https://cv{server_num}.litres.ru/pub/c/cover/{book_id}.xml"

    xml = fetch_url(toc_url)
    if not xml or "<toc>" not in xml:
        return None

    chapters = []
    # Парсим XML: <toc-item n="0" deep="1" id="59">Введение</toc-item>
    for match in re.finditer(r'<toc-item[^>]*deep="(\d+)"[^>]*>([^<]+)</toc-item>', xml):
        deep = int(match.group(1))
        title = unescape(match.group(2).strip())
        if title and deep > 0:  # Пропускаем deep=0 (название книги)
            chapters.append({"title": title, "deep": deep})

    return chapters if chapters else None


def format_litres_toc(chapters: list[dict]) -> list[str]:
    """Форматировать оглавление ЛитРес с отступами."""
    result = []
    for ch in chapters:
        # Добавляем отступы для вложенных пунктов
        indent = "  " * (ch["deep"] - 1)
        result.append(f"{indent}{ch['title']}")
    return result


# ==================== Open Library ====================

def fetch_open_library(isbn: str = None, title: str = None) -> dict | None:
    """Поиск книги в Open Library API."""
    if isbn:
        url = f"https://openlibrary.org/isbn/{isbn}.json"
    elif title:
        search_url = f"https://openlibrary.org/search.json?title={urllib.parse.quote(title)}&limit=1"
        html = fetch_url(search_url)
        if not html:
            return None
        try:
            data = json.loads(html)
            if data.get("docs"):
                key = data["docs"][0].get("key")
                if key:
                    url = f"https://openlibrary.org{key}.json"
                else:
                    return None
            else:
                return None
        except Exception:
            return None
    else:
        return None

    html = fetch_url(url)
    if html:
        try:
            return json.loads(html)
        except Exception:
            pass
    return None


def extract_toc_from_open_library(data: dict) -> list[str] | None:
    """Извлечь оглавление из данных Open Library."""
    toc = data.get("table_of_contents")
    if toc:
        chapters = []
        for item in toc:
            if isinstance(item, dict):
                title = item.get("title", "")
                if title:
                    chapters.append(title)
            elif isinstance(item, str):
                chapters.append(item)
        if chapters:
            return chapters
    return None


# ==================== Google Books ====================

def fetch_google_books(isbn: str = None, title: str = None) -> dict | None:
    """Поиск книги в Google Books API."""
    if isbn:
        query = f"isbn:{isbn}"
    elif title:
        query = urllib.parse.quote(title)
    else:
        return None

    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    html = fetch_url(url)
    if html:
        try:
            data = json.loads(html)
            if data.get("totalItems", 0) > 0:
                return data["items"][0]["volumeInfo"]
        except Exception:
            pass
    return None


# ==================== Форматирование ====================

def format_as_checklist(chapters: list[str]) -> str:
    """Преобразовать список глав в markdown чеклист."""
    lines = ["## Прогресс", ""]
    for chapter in chapters:
        chapter = " ".join(chapter.split())
        if chapter:
            lines.append(f"- [ ] {chapter}")
    return "\n".join(lines)


# ==================== Main ====================

def main():
    parser = argparse.ArgumentParser(
        description="Извлечь оглавление книги (ЛитРес, Open Library)"
    )
    parser.add_argument("--isbn", help="ISBN книги (для Open Library)")
    parser.add_argument("--title", help="Название книги (для Open Library)")
    parser.add_argument("--litres-id", help="ID книги на ЛитРес (число из URL)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown",
                        help="Формат вывода (default: markdown)")

    args = parser.parse_args()

    if not args.isbn and not args.title and not args.litres_id:
        print("Укажи --litres-id (рекомендуется) или --isbn / --title", file=sys.stderr)
        sys.exit(1)

    chapters = None
    source = None
    book_url = None

    # 1. ЛитРес — основной источник для русскоязычных книг
    if args.litres_id:
        print(f"Загружаю с ЛитРес (ID: {args.litres_id})...", file=sys.stderr)
        litres_chapters = fetch_litres_toc(args.litres_id)
        if litres_chapters:
            chapters = format_litres_toc(litres_chapters)
            source = "ЛитРес"
            book_url = f"https://www.litres.ru/book/-{args.litres_id}/"

    # 2. Open Library — для англоязычных книг
    if not chapters and (args.isbn or args.title):
        print("Ищу в Open Library...", file=sys.stderr)
        ol_data = fetch_open_library(isbn=args.isbn, title=args.title)
        if ol_data:
            chapters = extract_toc_from_open_library(ol_data)
            if chapters:
                source = "Open Library"

    # 3. Google Books — только для ссылки на превью
    if not chapters and (args.isbn or args.title):
        print("Ищу в Google Books...", file=sys.stderr)
        gb_data = fetch_google_books(isbn=args.isbn, title=args.title)
        if gb_data:
            preview_link = gb_data.get("previewLink")
            if preview_link:
                print(f"Превью: {preview_link}", file=sys.stderr)

    # Вывод результата
    if chapters:
        print(f"Найдено в {source}: {len(chapters)} пунктов", file=sys.stderr)
        if book_url:
            print(f"Источник: {book_url}", file=sys.stderr)

        if args.format == "json":
            print(json.dumps(chapters, ensure_ascii=False, indent=2))
        else:
            print(format_as_checklist(chapters))
    else:
        print("\nОглавление не найдено автоматически.", file=sys.stderr)
        if book_url:
            print(f"Проверь страницу вручную: {book_url}", file=sys.stderr)
        print("Попробуй ввести вручную или найти на сайте издательства.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
