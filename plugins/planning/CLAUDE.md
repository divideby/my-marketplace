# planning

Плагин для стратегического планирования на разных временных горизонтах.

## Назначение

Структурированное планирование с использованием лучших методологий:
- **GTD** — обработка входящих, weekly review
- **Джедайские техники** — фокус, энергия, приоритизация
- **OKRs** — квартальные цели с измеримыми результатами
- **12 Week Year** — квартал как "год" для создания срочности
- **Harada Method** — 64 шага к годовой цели

## Требования

Запускай Claude Code из корня Obsidian vault'а.

## Структура

```
planning/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── week.md       # /planning:week
│   ├── month.md      # /planning:month
│   ├── quarter.md    # /planning:quarter
│   ├── half-year.md  # /planning:half-year
│   └── year.md       # /planning:year
├── skills/
│   └── planning-methods/
│       ├── SKILL.md
│       └── references/
│           ├── week-template.md
│           ├── month-template.md
│           ├── quarter-template.md
│           └── year-template.md
└── settings/
```

## Команды

| Команда | Горизонт | Методология | Актуализирует |
|---------|----------|-------------|---------------|
| `/planning:week` | Неделя | GTD + Jedi | Месяц |
| `/planning:month` | Месяц | Jedi | Квартал |
| `/planning:quarter` | Квартал | OKRs + 12WY | Полугодие |
| `/planning:half-year` | Полугодие | OKRs | Год |
| `/planning:year` | Год | Harada (64) | — |

## Файлы в Obsidian

Хранятся в `Base/`:
- `Week-2026-W03.md`
- `Month-2026-01.md`
- `Quarter-2026-Q1.md`
- `HalfYear-2026-H1.md`
- `Year-2026.md`

## Каскадная актуализация

Каждая команда проверяет актуальность плана следующего уровня:

```
week → month → quarter → half-year → year
```

## Workflow каждой команды

1. **Ретро** — анализ прошлого периода
2. **План** — цели и фокусы нового периода
3. **Актуализация** — проверка плана следующего уровня
