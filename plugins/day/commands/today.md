---
description: Утреннее планирование дня с задачами из Obsidian
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "TodoWrite"]
---

# Daily Planning Protocol

Execute morning planning workflow for Obsidian vault.

**Assumes**: Claude is running from the vault's root directory.

## Workflow Overview

1. **Загрузить паттерны** — привычные времена из settings/patterns.md
2. **Что уже сделано** — утренняя рутина до планирования
3. **Собрать задачи** — due today, inbox, просроченные
4. **Фиксированные события** — встречи и события, которые НЕЛЬЗЯ перенести
5. **Фокусы дня** — приоритеты для свободного времени
6. **Сгенерировать расписание** — с учётом всего выше

---

## Step 1: Load Patterns

Read patterns from vault: `.claude/day-patterns.md` (relative to current directory)

(If file doesn't exist, see `${CLAUDE_PLUGIN_ROOT}/settings/patterns.example.md` for template)

Use patterns to understand:
- Typical times for recurring activities
- Fixed events (cannot be moved)
- User's time preferences

---

## Step 2: What's Already Done

Get current time with `date +%Y-%m-%d` and `date +%H:%M` — this is when planning starts.

### Auto-detect completed activities

**Check for reading session today:**

```bash
ls Base/Сессия-*-$(date +%Y-%m-%d).md 2>/dev/null
```

If file exists:
1. Read the file
2. Extract `started` and `ended` times from frontmatter
3. Add to schedule as completed: `{ time: "started", end: "ended", task: "✅ Чтение: [book name]", color: "#60a5fa44" }`

Example frontmatter:
```yaml
started: 08:15
ended: 09:00
book: "[[Deep Work]]"
```

### Ask about remaining routine

Based on auto-detection, ask user about what else is done (use AskUserQuestion with multiSelect=true):
```
Question: "Сейчас [TIME]. Что из утренней рутины уже сделано?"
Options:
- "Завтрак"
- "Медитация/дневник"
- "Чтение" (pre-select if session file found)
- "Самообразование"
```

**Start time = current time** — планирование начинается с момента запуска команды.

---

## Step 3: Collect Tasks

Read and present ALL tasks from these sources:

### 3.1 Due Today
```
Grep for: 📅 {today's date}
Path: ./
```

### 3.2 Dailies Inbox (no due date)
Tasks WITHOUT `📅` in recent daily notes.

### 3.3 Overdue Tasks
Tasks with dates before today.

### 3.4 Global Inbox
Read `./Inbox.md`

**Present grouped**:
```
## Задачи на сегодня
- task 1 (⏫)
- task 2

## Без даты (inbox)
- task 3

## Просрочено
- task 4
```

---

## Step 4: Fixed Events (CANNOT be moved)

**Critical step** — identify events that MUST happen at specific times.

Ask user:
```
Question: "Какие фиксированные события сегодня? (встречи, звонки, события которые нельзя перенести)"
```

For each event, get:
- Name
- Start time
- End time (or duration)
- Can it be skipped? (default: no)

**Check patterns file** for recurring fixed events (e.g., if today is ~14th, remind about rent payment at 19:00).

**These events are ANCHORS** — schedule builds around them.

### 4.1 Meeting Preparation

**ВАЖНО:** Спросить о подготовке к КАЖДОЙ встрече отдельно. Не пропускать ни одной.

**Шаг 1: Для КАЖДОЙ встречи из Step 4 задать вопрос:**

Используй AskUserQuestion для каждой встречи отдельно:

```text
Question: "Нужна подготовка к встрече [Название встречи]?"
Options:
- "Да, добавить слот 🔶 перед встречей"
- "Нет, подготовка не нужна"
```

**КРИТИЧНО:**

- Спрашивай по ОДНОЙ встрече за раз
- Если встреч 5 — задай 5 вопросов
- Если встреч 10 — задай 10 вопросов
- НЕ объединяй несколько встреч в один вопрос

**Шаг 2: Если пользователь ответил "Да" — уточни детали:**

- Что конкретно нужно подготовить?
- Сколько времени займёт? (15 мин / 30 мин / 1 час)

**Шаг 3: Создать задачи подготовки:**

Для каждой встречи с подготовкой создай задачу в формате:

```markdown
- [ ] Подготовка к [Название встречи]: [что именно] #task ⏫
```

**Шаг 4: Учесть в расписании:**

- Запланировать подготовку ПЕРЕД встречей (с буфером 10-15 мин)
- Если подготовка требует deep work — поставить в утренние слоты
- Пометить подготовку цветом `#fcd34d44` (золотой)

---

## Step 5: Day Focus

Now that we know constraints, ask about priorities for FREE time:

```text
Question: "Какие фокусы на свободное время?"
Options:
- "Deep work / coding"
- "Встречи и коммуникация"
- "Админ задачи"
- Other
```

---

## Step 6: Generate Schedule

Build schedule with this priority:

### 6.1 Already Done (marked with ✅)

Add completed morning routine at their typical times with ✅ prefix:

```javascript
{ time: "07:00", end: "07:30", task: "✅ Завтрак", color: "#4ade8033" },
{ time: "07:30", end: "08:00", task: "✅ Медитация", color: "#c4b5fd44" },
```

### 6.2 Fixed Events (ANCHORS)

Place fixed events at their exact times — these CANNOT move:

```javascript
{ time: "14:00", end: "15:00", task: "📌 Встреча с командой", color: "#a78bfa44" },
{ time: "19:00", end: "19:30", task: "📌 Оплата квартиры", color: "#67e8f933" },
```

### 6.3 Meeting Preparation (🔶)

Place preparation tasks BEFORE their meetings:

```javascript
{ time: "13:00", end: "13:45", task: "🔶 Подготовка: Встреча с командой", color: "#fcd34d44" },
{ time: "14:00", end: "15:00", task: "📌 Встреча с командой", color: "#a78bfa44" },
```

Rules:

- Schedule prep based on estimated duration from Step 4.1
- Leave 10-15 min buffer between prep end and meeting start
- If prep requires deep work — schedule in morning slot, not just before meeting

### 6.4 Fill Free Slots

Distribute remaining tasks into free time slots based on:

- User's focus priorities
- Task priorities (⏫ > 🔼 > 🔽)
- Time preferences from patterns (deep work morning, meetings afternoon)
- Appropriate durations

### 6.5 Add Breaks

- 5-10 min between deep work blocks
- Lunch around 13:00-14:00
- Buffer before important meetings

### Schedule Generation Rules

```text
START_TIME = user's specified start time (default: current time)
END_TIME = 19:00-20:00 or after last fixed event

1. Mark already-done as ✅
2. Place fixed events as 📌 anchors
3. Place meeting preparation (🔶) before meetings
4. Identify free slots between anchors and prep
5. Fill slots with tasks by priority
6. Add breaks every 2-3 hours
7. Ensure no conflicts with fixed events or prep
```

---

## Step 7: Write and Present

1. Create/update `Dailies/YYYY-MM-DD.md` with DataviewJS schedule
2. Present summary:

```text
Расписание готово!

✅ Уже сделано:
- Завтрак, медитация, чтение

📌 Фиксированные события:
- 14:00 Встреча с командой
- 19:00 Оплата квартиры

🔶 Подготовка к встречам:
- 13:00-13:45 Подготовка: Встреча с командой

📋 Запланировано:
- 10:00-12:00 Deep work: [task]
- 13:00-14:00 Обед
- 15:00-17:00 [tasks by focus]

Первая задача: [next task]

Когда закончишь — /day:checkin
```

---

## Important Notes

- **Fixed events are sacred** — never move them
- Use `obsidian-vault` skill for vault structure
- Check patterns.md for user's typical schedule
- Start time = when PLANNED part begins (after morning routine)
- Use Russian language
- Be concise

---

## Task Creation Rules

### Проверка дубликатов

**ПЕРЕД созданием любой задачи** проверь, нет ли её уже:

```bash
grep -r "ключевые слова задачи" --include="*.md" Base/ Dailies/ | head -5
```

Если найден дубликат — не создавай новую, сошлись на существующую.

### Проектные задачи и канбан

**Если задача относится к проекту с канбаном:**

- **НЕ добавлять в Dailies** — создавать только в канбане проекта
- В daily note добавить ссылку вместо задачи:

```markdown
**Африка** — см. [[Абиджан 2026|канбан]]
```

### Делегированные задачи

- Формат: `- [ ] (делегировано Имя) Описание #task #wait`
- **НЕ добавлять в расписание дня**
- Оставлять в канбане проекта для трекинга

---

## Schedule Rules

### Не объединять активности

**НИКОГДА** не писать "Обед + X" или "Перерыв + Y".

Каждая активность — отдельный блок:

```javascript
// ❌ НЕПРАВИЛЬНО
{ time: "13:00", task: "Обед + просмотр документов" }

// ✅ ПРАВИЛЬНО
{ time: "13:00", end: "13:30", task: "🍽️ Обед", color: "#4ade8033" },
{ time: "13:30", end: "14:00", task: "Просмотр документов", color: "#60a5fa44" },
```

### Заполнять все слоты

Не оставлять пустые промежутки между задачами:

- **Короткие перерывы (5 мин):** `isBreak: true` — отображается тонкой линией
- **Буферы между задачами:** явно показывать как "⏸️ Буфер"
- **Все остальное:** заполнять задачами

```javascript
{ time: "11:55", end: "12:00", task: "", isBreak: true },  // 5-мин перерыв
{ time: "14:45", end: "15:00", task: "⏸️ Буфер перед встречей", color: "#f9a8d433" },
```
