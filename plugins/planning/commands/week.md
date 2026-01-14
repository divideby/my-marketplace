---
description: Недельное планирование — ретро + план + актуализация месяца
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Weekly Planning

Execute weekly planning session using GTD and Jedi Techniques.

**Assumes**: Running from Obsidian vault root.

## Workflow

1. Determine current week (ISO format)
2. Load previous week file (if exists) for retro
3. Conduct retrospective
4. Create new week plan
5. Actualize monthly plan

---

## Step 1: Determine Week

```bash
date +%Y-W%V
```

File will be: `Base/Week-{YEAR}-W{WEEK}.md`

---

## Step 2: Load Context

1. Read previous week file: `Base/Week-{PREV}.md`
2. Read current month file: `Base/Month-{YEAR}-{MM}.md` (if exists)
3. Check what tasks are due this week

---

## Step 3: Retrospective (GTD Weekly Review)

Ask user:

```
Question: "Ретро прошлой недели. Что получилось?"
```

```
Question: "Что не получилось? Какие уроки?"
```

Summarize in Ретро section.

---

## Step 4: Weekly Focuses

Ask user:

```
Question: "Какие 3-5 главных фокусов на эту неделю?"
```

Consider:
- Tasks due this week
- Monthly goals (if month file exists)
- Ongoing projects

---

## Step 5: Daily Distribution

For each weekday (Пн-Пт):
- Show date
- Ask if there are specific tasks for that day
- Add tasks query block

Use Jedi Techniques:
- Deep work in morning slots
- Meetings in afternoon
- Buffer time for unexpected

---

## Step 6: Habits

Ask:
```
Question: "Какие привычки поддерживаем на этой неделе?"
```

---

## Step 7: Actualize Month

If month file exists (`Base/Month-{YEAR}-{MM}.md`):

1. Read month goals
2. Ask user:
```
Question: "Месячный план актуален? Нужны корректировки?"
Options:
- "Всё актуально"
- "Нужно скорректировать"
- "Посмотреть план"
```

If corrections needed → edit month file.

---

## Step 8: Write Week File

Create `Base/Week-{YEAR}-W{WEEK}.md` using template from skill.

Include:
- Ретро section
- Фокусы недели
- Привычки
- План по дням with dataview queries
- Link to month plan

---

## Output

```
Неделя {WEEK} спланирована!

Фокусы:
- Focus 1
- Focus 2
- Focus 3

Файл: Base/Week-{YEAR}-W{WEEK}.md
```
