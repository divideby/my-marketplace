---
description: Чекин — отметить прогресс и получить следующую задачу
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "TodoWrite"]
---

# Day Check-in Protocol

Handle task completion and provide next action.

## Workflow

1. **Determine context** — what was user working on
2. **Ask for result** — what happened, what completed
3. **Update daily note** — mark tasks done, add notes
4. **Provide next task** — based on schedule and priorities

---

## Step 1: Load Context

1. Get current time: `date`
2. Read today's daily note: `./Dailies/YYYY-MM-DD.md`
3. Parse the `## Расписание` DataviewJS block to find:
   - Current time block (what should be happening now)
   - Previous block (what user likely just finished)
   - Next block (upcoming task)

---

## Step 2: Ask About Results

Use AskUserQuestion based on what user was doing:

### For Regular Tasks:
```
Question: "Что получилось сделать?"
Options:
- "Задача выполнена полностью"
- "Частично сделано, нужно продолжить"
- "Не получилось, отложить"
- Other (free text for details)
```

### For Meetings (if previous block was a meeting):
```
Question: "Как прошла встреча?"
Options:
- "Продуктивно, есть action items"
- "Информационная, без задач"
- "Отменилась / перенеслась"
- Other
```

If user mentions action items or follow-ups, ask:
```
Question: "Какие следующие шаги?"
Options:
- "Создать задачи"
- "Написать кому-то"
- "Нет действий"
```

---

## Step 3: Update Daily Note

Based on user's response:

### If task completed:
1. In `## Задачи` section, change `- [ ]` to `- [x]` for the task
2. Add completion date: `✅ YYYY-MM-DD`
3. In schedule, add `✅` prefix to task name

### If partially done:
1. Keep task as `- [ ]`
2. Optionally add note about progress
3. Ask if user wants to continue or move to next task

### If meeting had action items:
1. Add new tasks under `> [!todo]` callout in daily note
2. Format: `- [ ] Action item #task 📅 YYYY-MM-DD`
3. Group by category if multiple items

### If needs to write someone:
Add task with `#wait` tag:
```markdown
- [ ] Написать [имя]: [тема] #task #wait 📅 YYYY-MM-DD
```

---

## Step 4: Provide Next Task

Look at schedule and determine next action:

1. **If within current time block** — suggest continuing or starting the block's task
2. **If between blocks** — announce upcoming task and time until it starts
3. **If no more scheduled items** — check for remaining undone tasks

Present to user:

```
Отлично! Отметил.

Сейчас по плану: [current/next task from schedule]
Начало: HH:MM

[If meeting] Подготовься к: [meeting name]
[If deep work] Фокус на: [task description]

Когда закончишь — снова /day:checkin
```

---

## Step 5: End of Day Detection

If current time is after last scheduled item or user says "закончил день":

1. Summarize completed tasks
2. List remaining undone tasks
3. Ask if user wants to reschedule anything to tomorrow:
```
Question: "Перенести незавершённые задачи на завтра?"
Options:
- "Да, все"
- "Нет, оставить"
- "Выбрать конкретные"
```

---

## Important Notes

- Use `obsidian-vault` skill for vault structure knowledge
- Be conversational but brief
- If user seems to have had a meeting, suggest meeting-processor agent
- Always update schedule with `✅` for visual tracking
- Use Russian language for all output
