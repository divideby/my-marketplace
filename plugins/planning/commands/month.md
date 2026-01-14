---
description: Месячное планирование — ретро + план + актуализация квартала
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Monthly Planning

Execute monthly planning session.

**Assumes**: Running from Obsidian vault root.

## Workflow

1. Determine current month
2. Load previous month for retro
3. Conduct retrospective
4. Set monthly goals and themes
5. Plan weekly breakdown
6. Actualize quarterly plan

---

## Step 1: Determine Month

```bash
date +%Y-%m
```

File: `Base/Month-{YEAR}-{MM}.md`

---

## Step 2: Load Context

1. Previous month: `Base/Month-{PREV}.md`
2. Current quarter: `Base/Quarter-{YEAR}-Q{N}.md`
3. Year plan: `Base/Year-{YEAR}.md`

---

## Step 3: Retrospective

Ask user:

```
Question: "Главные достижения прошлого месяца?"
```

```
Question: "Что не получилось? Уроки?"
```

---

## Step 4: Monthly Theme & Goals

Ask:

```
Question: "Какая главная тема этого месяца?"
```

```
Question: "3-5 ключевых целей месяца?"
```

Cross-reference with quarterly OKRs if available.

---

## Step 5: Key Dates

Ask:

```
Question: "Ключевые даты и дедлайны в этом месяце?"
```

---

## Step 6: Weekly Breakdown

For each week of the month:
- Suggest focus based on goals
- Ask user for adjustments

---

## Step 7: Habits

```
Question: "Привычки на месяц?"
```

---

## Step 8: Actualize Quarter

If quarter file exists:

1. Show quarterly OKRs
2. Ask:
```
Question: "Как прогресс по квартальным OKRs? Актуальны ли они?"
Options:
- "На треке"
- "Нужна корректировка OKRs"
- "Посмотреть детали"
```

---

## Step 9: Write Month File

Create `Base/Month-{YEAR}-{MM}.md` with:
- Ретро
- Тема и цели
- Ключевые даты
- Понедельный план
- Привычки
- Link to quarter

---

## Output

```
Месяц {MONTH} спланирован!

Тема: {theme}
Цели:
- Goal 1
- Goal 2

Файл: Base/Month-{YEAR}-{MM}.md
```
