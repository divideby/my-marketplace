---
description: Утреннее планирование дня с задачами из Obsidian
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "TodoWrite"]
---

# Daily Planning Protocol

Execute morning planning workflow for Obsidian vault at `/home/divideby/Yandex.Disk/Ocean/new-ocean/`.

## Workflow

1. **Check current time** with `date` command
2. **Collect all tasks** (show to user)
3. **Ask for day's focus**
4. **Generate schedule** and write to daily note

---

## Step 1: Get Current Date

Run `date +%Y-%m-%d` to determine today's date for the daily note filename.

---

## Step 2: Collect Tasks

Read and present ALL tasks from these sources:

### 2.1 Due Today
Search for tasks with today's date (`📅 YYYY-MM-DD`):
```
Grep pattern: "📅 {today's date}"
Path: /home/divideby/Yandex.Disk/Ocean/new-ocean/
```

### 2.2 Dailies Inbox (no due date)
Read recent daily notes and find tasks WITHOUT `📅` date:
```
Path: /home/divideby/Yandex.Disk/Ocean/new-ocean/Dailies/
Look for: - [ ] ... #task (without 📅)
```

### 2.3 Overdue Tasks
Search for tasks with dates before today:
```
Grep for: 📅 YYYY-MM-DD where date < today
```

### 2.4 Global Inbox
Read `/home/divideby/Yandex.Disk/Ocean/new-ocean/Inbox.md` for overview.

**Present tasks grouped**:
```
## Задачи на сегодня (due today)
- task 1
- task 2

## Без даты (inbox)
- task 3

## Просрочено
- task 4
```

---

## Step 3: Ask for Focus

Use AskUserQuestion:

```
Question: "Какие обязательные фокусы на сегодня?"
Options:
- "Deep work / coding"
- "Встречи и коммуникация"
- "Админ задачи"
- Other (free text)
```

Also ask:
```
Question: "Есть ли встречи или жёсткие блоки времени?"
```

---

## Step 4: Generate Schedule

Based on tasks and focus, create a schedule:

1. **Read existing daily note** at `Dailies/YYYY-MM-DD.md` (if exists)
2. **Plan time blocks** considering:
   - User's stated focus areas
   - Fixed meetings/appointments
   - Task priorities (⏫ > 🔼 > 🔽)
   - Natural energy patterns (deep work morning, meetings afternoon)
3. **Generate DataviewJS schedule block** using template from skill

### Schedule Generation Rules

- Start with morning routine (breakfast, meditation)
- Place deep work blocks in morning (08:00-12:00)
- Schedule meetings as stated
- Add breaks every 2-3 hours
- Include lunch around 12:00-14:00
- End day by 18:00-19:00

### Write Schedule

Create/update `## Расписание` section with DataviewJS block:

```dataviewjs
const schedule = [
  // Generated schedule items here
];
// ... rest of template from skill reference
```

---

## Step 5: Present Day Protocol

After writing schedule, tell user:

```
Расписание готово!

Первая задача: [next task from schedule]

Когда закончишь — вызови /day:checkin чтобы отметить прогресс и получить следующую задачу.
```

---

## Important Notes

- Use `obsidian-vault` skill knowledge for vault structure and formats
- Always include `#task` tag when creating tasks
- Preserve existing content in daily notes
- Use Russian language for all output
- Be concise — no lengthy explanations
