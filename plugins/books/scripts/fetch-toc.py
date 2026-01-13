#!/usr/bin/env python3
"""
Скрипт для извлечения оглавления книги.
Источники: ЛитРес, Лабиринт, Open Library, Google Books.
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


# ==================== Лабиринт ====================

def search_labirint(title: str) -> tuple[str, str] | None:
    """Найти книгу на Лабиринте и вернуть (URL, название)."""
    search_url = f"https://www.labirint.ru/search/{urllib.parse.quote(title)}/?stype=0"
    html = fetch_url(search_url)
    if not html:
        return None

    match = re.search(r'href="(/books/\d+/)"', html)
    if match:
        book_url = f"https://www.labirint.ru{match.group(1)}"
        title_match = re.search(r'class="[^"]*product-title[^"]*"[^>]*>([^<]+)<', html)
        found_title = title_match.group(1).strip() if title_match else "Неизвестно"
        return (book_url, found_title)
    return None


def fetch_labirint_by_isbn(isbn: str) -> str | None:
    """Найти книгу на Лабиринте по ISBN."""
    search_url = f"https://www.labirint.ru/search/{isbn}/?stype=0"
    html = fetch_url(search_url)
    if not html:
        return None

    match = re.search(r'href="(/books/\d+/)"', html)
    if match:
        return f"https://www.labirint.ru{match.group(1)}"
    return None


def fetch_labirint_toc(url: str) -> list[str] | None:
    """Извлечь оглавление со страницы книги на Лабиринте."""
    html = fetch_url(url)
    if not html:
        return None

    chapters = []
    toc_match = re.search(
        r'\[\],"(Введение[^"]+|Предисловие[^"]+|Глава\s+1[^"]+)"',
        html
    )

    if toc_match:
        content = toc_match.group(1)
        content = content.replace('\\u003C', '<').replace('\\u003E', '>')
        content = re.sub(r'</?br\s*/?>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'<[^>]+>', '', content)
        content = unescape(content)

        for line in content.split('\n'):
            line = line.strip()
            if line and len(line) > 2:
                if re.match(r'^(Введение|Предисловие|Заключение|Послесловие|Эпилог|Приложени|Глава|Часть|Раздел|\d+\.)', line, re.IGNORECASE):
                    chapters.append(line)

    if chapters:
        seen = set()
        unique = []
        for ch in chapters:
            if ch not in seen:
                seen.add(ch)
                unique.append(ch)
        return unique[:100]

    return None


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
        description="Извлечь оглавление книги (ЛитРес, Лабиринт, Open Library)"
    )
    parser.add_argument("--isbn", help="ISBN книги")
    parser.add_argument("--title", help="Название книги")
    parser.add_argument("--url", help="Прямой URL страницы книги на Лабиринте")
    parser.add_argument("--litres-id", help="ID книги на ЛитРес (число)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown",
                        help="Формат вывода (default: markdown)")

    args = parser.parse_args()

    if not args.isbn and not args.title and not args.url and not args.litres_id:
        print("Укажи --isbn, --title, --url или --litres-id", file=sys.stderr)
        sys.exit(1)

    chapters = None
    source = None
    book_url = None

    # 1. Если указан ID ЛитРес напрямую
    if args.litres_id:
        print(f"Загружаю с ЛитРес (ID: {args.litres_id})...", file=sys.stderr)
        litres_chapters = fetch_litres_toc(args.litres_id)
        if litres_chapters:
            chapters = format_litres_toc(litres_chapters)
            source = "ЛитРес"
            book_url = f"https://www.litres.ru/book/-{args.litres_id}/"

    # 2. Если указан прямой URL Лабиринта
    if not chapters and args.url:
        print(f"Загружаю {args.url}...", file=sys.stderr)
        chapters = fetch_labirint_toc(args.url)
        if chapters:
            source = "Лабиринт"
            book_url = args.url

    # 3. Пробуем Лабиринт по ISBN или названию
    if not chapters:
        print("Ищу на Лабиринте...", file=sys.stderr)
        labirint_url = None

        if args.isbn:
            labirint_url = fetch_labirint_by_isbn(args.isbn)
        elif args.title:
            result = search_labirint(args.title)
            if result:
                labirint_url, found_title = result
                print(f"Найдена книга: \"{found_title}\"", file=sys.stderr)

        if labirint_url:
            print(f"URL: {labirint_url}", file=sys.stderr)
            book_url = labirint_url
            chapters = fetch_labirint_toc(labirint_url)
            if chapters:
                source = "Лабиринт"

    # 4. Пробуем Open Library (для англоязычных книг)
    if not chapters:
        print("Ищу в Open Library...", file=sys.stderr)
        ol_data = fetch_open_library(isbn=args.isbn, title=args.title)
        if ol_data:
            chapters = extract_toc_from_open_library(ol_data)
            if chapters:
                source = "Open Library"

    # 5. Пробуем Google Books (только для ссылки на превью)
    if not chapters:
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
