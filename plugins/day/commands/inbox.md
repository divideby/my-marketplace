---
description: Обработка входящих — рассортировать задачи с #inbox по нутриентам
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "TodoWrite"]
---

# Inbox Processing Protocol

Process inbox items through formulation criteria and categorize into nutrients.

## Purpose

Transform unclear inbox items into:

- **Concrete tasks** ready for scheduling
- **Projects** requiring further decomposition
- **Reference info** for storage
- **Meetings** with time allocation

**Core principle:** Not to START doing, but to UNDERSTAND what exactly needs to be done.

---

## Workflow Overview

1. **Collect inbox items** — tasks with `#inbox` tag
2. **For each item:** validate against 4 criteria
3. **Reformulate if needed** — apply patterns
4. **Categorize** — task/project/info/meeting
5. **Dispatch** — update files accordingly

---

## Step 1: Collect Inbox Items

Run from Obsidian vault root (`~/Yandex.Disk/Ocean/new-ocean/`):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-tasks.py --inbox
```

Parse JSON output to get list of items with `#inbox` tag.

**Note:** Inbox items are tasks marked with `#inbox #task`. The file `Inbox.md` at vault root is a DataView dashboard that queries these tags.

Present summary:

```text
📥 Inbox: X items to process
- [list items numbered with source file]

Начнём с первого?
```

---

## Step 2: Process Each Item

For each inbox item, run this validation flow:

### 2.1 Display Item

```text
---
📌 Item N/Total: [item text]
Source: [file:line]
---
```

### 2.2 Check 4 Criteria

Evaluate internally:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Отвечает на "что нужно сделать" | Clear outcome? |
| 2 | Начинается с глагола | Action verb? |
| 3 | "Проще сделать, чем записать" | Atomic? |
| 4 | Первоочередное действие | Next action? |

If ALL 4 pass → go to Step 2.4 (categorization)
If ANY fails → go to Step 2.3 (reformulation)

### 2.3 Reformulation Help

If item fails criteria, help user reformulate:

**Use AskUserQuestion:**

```text
Question: "Что конкретно нужно сделать для '[item]'?"
Header: "Уточнение"
Options:
- "Написать/позвонить кому-то"
- "Найти/собрать информацию"
- "Создать/сделать что-то"
- Other (пользователь введёт сам)
```

**Apply reformulation patterns:**

| If user says | Transform to |
|--------------|--------------|
| "Встретиться с X" | "Написать X и предложить время встречи" |
| "Узнать Y" | "Написать/позвонить Z с вопросом о Y" |
| "Подумать о Z" | Ask: "Какой первый вопрос?" → "Ответить на: [вопрос]" |
| "Найти время на X" | "Открыть календарь и забронировать слот для X" |
| "Получить ответ от X" | "Написать X: нужна ли помощь / как успехи?" |

**Use Magic Fairy:**

```text
Представь, фея дала 20 свободных минут. Что сделаешь, чтобы продвинуться к результату?
```

Validate reformulated text against 4 criteria again.

### 2.4 Categorization

Once item passes criteria (or user accepts as-is), categorize:

**Use AskUserQuestion:**

```text
Question: "Куда относится: [reformulated item]?"
Header: "Категория"
Options:
- "📋 Задача — конкретное действие, делегировать обезьянке"
- "📁 Проект — надо ещё подумать прежде чем начать"
- "📚 Информация — пригодится позже, но действий не требует"
- "📅 Встреча — выделю время на это мероприятие"
```

Record: `{ item, category, reformulated_text }`

---

## Step 3: Multiple Nutrients Detection

**Before moving to next item, ask:**

```text
Question: "Есть ещё что-то в этом входящем?"
Header: "Ещё?"
Options:
- "Да, ещё одна задача"
- "Да, встреча или событие"
- "Да, справочная информация"
- "Нет, это всё"
```

If yes → repeat Step 2.3-2.4 for additional nutrient
If no → move to next inbox item

---

## Step 4: Dispatch Categorized Items

After all items processed, update files:

### 4.1 Tasks (📋)

After categorizing as task:

1. **Remove `#inbox` tag** from the original task line
2. **Add due date** if user specified one:

Edit original task in source file:

```markdown
# Before:
- [ ] Some task #inbox #task

# After (with date):
- [ ] Some task #task 📅 2026-01-17

# After (no date, stays in daily):
- [ ] Some task #task
```

**Finding the task:**
- Use file path and line number from parse-tasks.py output
- Edit in place using Edit tool

### 4.2 Projects (📁)

After categorizing as project:

1. **Remove original task** from source file (it becomes a project)
2. **Create project note** in `Base/`:

Ask for project name:

**Use AskUserQuestion:**

```text
Question: "Как назвать проект?"
Header: "Название"
Options:
- "[suggested name based on task]"
- "[alternative name]"
- Other (введу название)
```

Create file at `Base/[Project Name].md`:

```markdown
# [Project Name]

#project/inprogress

## Контекст
[Original task text and any user clarification]

## Следующие шаги
- [ ] Определить первый конкретный шаг #task
```

### 4.3 Information (📚)

After categorizing as info:

1. **Remove original task** from source file
2. **Save information** — ask where:

**Use AskUserQuestion:**

```text
Question: "Куда сохранить информацию?"
Header: "Место"
Options:
- "Создать новую заметку в Base/"
- "Добавить в существующую заметку"
```

**If new note:** Create `Base/[Info Title].md` with content

**If existing note:**

```text
Question: "В какую заметку добавить?"
Header: "Заметка"
Options:
- "[suggest related note from Base/]"
- "[another suggestion]"
- Other (укажу путь)
```

Append info to chosen note.

### 4.4 Meetings (📅)

After categorizing as meeting:

1. **Update original task** — remove `#inbox`, add date:

```markdown
# Before:
- [ ] Встретиться с Васей #inbox #task

# After:
- [ ] Встретиться с Васей #task 📅 2026-01-20
```

2. **Optionally add to calendar** — ask if needed

---

## Step 5: Cleanup and Summary

After processing all items:

### 5.1 Remove processed items from source files

For all items:

- **Tasks/Meetings:** `#inbox` tag already removed during dispatch
- **Projects/Info:** Original task line already deleted during dispatch

No additional cleanup needed — dispatch step handles everything.

### 5.2 Present Summary

```text
✅ Inbox обработан!

📋 Задачи добавлены (X):
- [list]

📁 Проекты созданы (Y):
- [list]

📚 Информация сохранена (Z):
- [list]

📅 Встречи запланированы (W):
- [list]

Следующий шаг: /day:today для планирования
```

---

## Important Notes

- **One nutrient = one record** — don't mix in same entry
- Process all items before dispatch (batch updates)
- Use Russian language throughout
- Be conversational but concise
- If user skips reformulation, accept their original text
- Track progress visually: "Item 3/7"
