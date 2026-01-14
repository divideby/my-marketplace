#!/usr/bin/env python3
"""
Скрипт для извлечения информации о книге.
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
    """Загрузить страницу по URL (с редиректами)."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # Следуем редиректам вручную если нужно
            final_url = response.geturl()
            if final_url != url:
                req = urllib.request.Request(final_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=timeout) as response2:
                    return response2.read().decode("utf-8", errors="ignore")
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}", file=sys.stderr)
        return None


# ==================== ЛитРес ====================

def fetch_litres_xml(book_id: str) -> str | None:
    """Загрузить XML с ЛитРес."""
    server_num = book_id[-2] if len(book_id) >= 2 else "0"
    url = f"https://cv{server_num}.litres.ru/pub/c/cover/{book_id}.xml"
    return fetch_url(url)


def extract_litres_metadata(xml: str, book_id: str) -> dict | None:
    """Извлечь метаданные книги из XML ЛитРес."""
    if not xml:
        return None

    # Автор и название в первом toc-item с deep="0"
    # Формат: "Автор. Название книги"
    title_match = re.search(r'<toc-item[^>]*deep="0"[^>]*>([^<]+)</toc-item>', xml)
    if not title_match:
        return None

    full_title = unescape(title_match.group(1).strip())

    # Разделяем автора и название по первой точке с пробелом
    parts = full_title.split(". ", 1)
    if len(parts) == 2:
        author = parts[0].strip()
        title = parts[1].strip()
    else:
        author = None
        title = full_title

    # Обложка по стандартному URL
    cover = f"https://cdn.litres.ru/pub/c/cover/{book_id}.jpg"

    return {
        "title": title,
        "author": author,
        "cover": cover,
        "pages": None,
        "isbn": None,
        "publisher": None,
        "year": None,
        "litres_id": book_id,
        "litres_url": f"https://www.litres.ru/book/-{book_id}/",
    }


def extract_litres_toc(xml: str) -> list[dict] | None:
    """Извлечь оглавление из XML ЛитРес."""
    if not xml or "<toc>" not in xml:
        return None

    chapters = []
    for match in re.finditer(r'<toc-item[^>]*deep="(\d+)"[^>]*>([^<]+)</toc-item>', xml):
        deep = int(match.group(1))
        title = unescape(match.group(2).strip())
        if title and deep > 0:
            chapters.append({"title": title, "deep": deep})

    return chapters if chapters else None


def format_litres_toc(chapters: list[dict]) -> list[str]:
    """Форматировать оглавление ЛитРес с отступами."""
    result = []
    for ch in chapters:
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


def extract_google_metadata(data: dict) -> dict | None:
    """Извлечь метаданные из Google Books."""
    if not data:
        return None

    authors = data.get("authors", [])
    image_links = data.get("imageLinks", {})

    return {
        "title": data.get("title"),
        "author": authors[0] if authors else None,
        "cover": image_links.get("thumbnail"),
        "pages": data.get("pageCount"),
        "isbn": next((i.get("identifier") for i in data.get("industryIdentifiers", [])
                      if i.get("type") in ("ISBN_13", "ISBN_10")), None),
        "publisher": data.get("publisher"),
        "year": data.get("publishedDate", "")[:4] or None,
    }


# ==================== Форматирование ====================

def format_as_checklist(chapters: list[str]) -> str:
    """Преобразовать список глав в markdown чеклист."""
    lines = ["## Прогресс", ""]
    for chapter in chapters:
        chapter = " ".join(chapter.split())
        if chapter:
            lines.append(f"- [ ] {chapter}")
    return "\n".join(lines)


def format_metadata_json(meta: dict) -> str:
    """Форматировать метаданные как JSON."""
    return json.dumps(meta, ensure_ascii=False, indent=2)


def format_metadata_yaml(meta: dict) -> str:
    """Форматировать метаданные как YAML frontmatter."""
    lines = ["---"]
    if meta.get("title"):
        # Экранируем кавычки в названии
        title = meta["title"].replace('"', '\\"')
        lines.append(f'title: "{title}"')
    if meta.get("author"):
        lines.append(f'author: [{meta["author"]}]')
    if meta.get("publisher"):
        lines.append(f'publisher: {meta["publisher"]}')
    if meta.get("year"):
        lines.append(f'publish: {meta["year"]}')
    if meta.get("pages"):
        lines.append(f'total: {meta["pages"]}')
    if meta.get("isbn"):
        lines.append(f'isbn: {meta["isbn"]}')
    if meta.get("cover"):
        lines.append(f'coverUrl: {meta["cover"]}')
    if meta.get("litres_id"):
        lines.append(f'litresId: {meta["litres_id"]}')
    if meta.get("litres_url"):
        lines.append(f'litresUrl: {meta["litres_url"]}')
    lines.append("status: reading")
    lines.append("tags: [own]")
    lines.append("---")
    return "\n".join(lines)


# ==================== Main ====================

def main():
    parser = argparse.ArgumentParser(
        description="Извлечь информацию о книге (ЛитРес, Open Library, Google Books)"
    )
    parser.add_argument("--isbn", help="ISBN книги")
    parser.add_argument("--title", help="Название книги")
    parser.add_argument("--litres-id", help="ID книги на ЛитРес (число из URL)")
    parser.add_argument("--info", action="store_true",
                        help="Получить метаданные книги вместо оглавления")
    parser.add_argument("--format", choices=["json", "markdown", "yaml"], default="markdown",
                        help="Формат вывода (default: markdown)")

    args = parser.parse_args()

    if not args.isbn and not args.title and not args.litres_id:
        print("Укажи --litres-id (рекомендуется) или --isbn / --title", file=sys.stderr)
        sys.exit(1)

    # Режим получения метаданных
    if args.info:
        meta = None
        source = None

        # 1. ЛитРес
        if args.litres_id:
            print(f"Загружаю метаданные с ЛитРес (ID: {args.litres_id})...", file=sys.stderr)
            xml = fetch_litres_xml(args.litres_id)
            if xml:
                meta = extract_litres_metadata(xml, args.litres_id)
                if meta:
                    source = "ЛитРес"

        # 2. Google Books (fallback)
        if not meta and (args.isbn or args.title):
            print("Ищу в Google Books...", file=sys.stderr)
            gb_data = fetch_google_books(isbn=args.isbn, title=args.title)
            if gb_data:
                meta = extract_google_metadata(gb_data)
                if meta:
                    source = "Google Books"

        if meta:
            print(f"Найдено в {source}", file=sys.stderr)
            if args.format == "json":
                print(format_metadata_json(meta))
            elif args.format == "yaml":
                print(format_metadata_yaml(meta))
            else:
                print(format_metadata_yaml(meta))
        else:
            print("Метаданные не найдены.", file=sys.stderr)
            sys.exit(1)
        return

    # Режим получения оглавления
    chapters = None
    source = None
    book_url = None

    # 1. ЛитРес
    if args.litres_id:
        print(f"Загружаю с ЛитРес (ID: {args.litres_id})...", file=sys.stderr)
        xml = fetch_litres_xml(args.litres_id)
        if xml:
            litres_chapters = extract_litres_toc(xml)
            if litres_chapters:
                chapters = format_litres_toc(litres_chapters)
                source = "ЛитРес"
                book_url = f"https://www.litres.ru/book/-{args.litres_id}/"

    # 2. Open Library
    if not chapters and (args.isbn or args.title):
        print("Ищу в Open Library...", file=sys.stderr)
        ol_data = fetch_open_library(isbn=args.isbn, title=args.title)
        if ol_data:
            chapters = extract_toc_from_open_library(ol_data)
            if chapters:
                source = "Open Library"

    # 3. Google Books — только для превью
    if not chapters and (args.isbn or args.title):
        print("Ищу в Google Books...", file=sys.stderr)
        gb_data = fetch_google_books(isbn=args.isbn, title=args.title)
        if gb_data:
            preview_link = gb_data.get("previewLink")
            if preview_link:
                print(f"Превью: {preview_link}", file=sys.stderr)

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
