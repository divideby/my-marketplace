---
name: obsidian-vault
description: Provides knowledge about Obsidian vault structure at ~/Yandex.Disk/Ocean/new-ocean/, task formats, DataviewJS schedule templates. Activates when working with daily planning, tasks due today, inbox tasks, overdue tasks, or generating daily schedules.
---

# Obsidian Vault Knowledge

Use this skill when working with daily planning, task management, or schedule generation in the user's Obsidian vault.

## Vault Location

**Path**: `/home/divideby/Yandex.Disk/Ocean/new-ocean/`

## Task Sources

Collect tasks from these locations:

### 1. Due Today
Tasks with `📅 YYYY-MM-DD` matching today's date.

**Query pattern**:
```tasks
not done
due today
```

### 2. Dailies Inbox
Tasks in `Dailies/` folder WITHOUT due dates — these need scheduling.

**Query pattern**:
```tasks
not done
path includes Dailies
no due date
```

### 3. Overdue Tasks
Tasks with due date before today.

**Query pattern**:
```tasks
not done
due before today
path does not include TG Channel
path does not include _templates
```

### 4. General Inbox
Check `/home/divideby/Yandex.Disk/Ocean/new-ocean/Inbox.md` for aggregated unscheduled tasks.

## Task Format

Standard task format in this vault:
```markdown
- [ ] Task description ⏫ #task 📅 2026-01-14
```

**Components**:
- `- [ ]` — unchecked task
- `⏫` / `🔼` / `🔽` — priority (high/medium/low)
- `⚡` — quick task (at start)
- `#task` — REQUIRED tag for Dataview queries
- `#wait` — waiting for someone
- `📅 YYYY-MM-DD` — due date

**Marking done**: Change `- [ ]` to `- [x]` and add `✅ YYYY-MM-DD` at the end.

## Daily Note Structure

Daily notes are at `Dailies/YYYY-MM-DD.md`.

**Key sections**:
1. `# Задачи на сегодня` — auto-query for `due today`
2. `## Расписание` — DataviewJS schedule block
3. `## Задачи` — `> [!todo]` callout with tasks grouped by category

## Schedule Generation

Generate DataviewJS schedule with this template.

**Color coding by task type**:
| Type | Color | Example |
|------|-------|---------|
| Food/meals | `#4ade8033` | Завтрак, Обед, Перекус |
| Routines | `#c4b5fd44` | Медитация, Дневник |
| Deep work | `#60a5fa44` | Coding, Reading, Focus tasks |
| Meetings | `#a78bfa44` | Встречи, Звонки |
| Exercise | `#fbbf2444` | Тренировка |
| Health | `#67e8f933` | Чекапы, Здоровье |
| Breaks | `#f9a8d433` | Отдых, Перерывы |

**DataviewJS Template**:

See `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-vault/references/schedule-template.js` for full template.

Key points:
- Each block: `{ time: "HH:MM", end: "HH:MM", task: "Icon Description", color: "#..." }`
- Short breaks: add `isBreak: true` with empty task and `#f9a8d422` color
- Real-time red progress line shows current time within active block
- Block height = max(30, duration in minutes), breaks = 8px

## Writing to Daily Note

When adding tasks to daily note:
1. Find or create today's file at `Dailies/YYYY-MM-DD.md`
2. Add tasks under `## Задачи` inside `> [!todo]` callout
3. Group by category with `> **Category:**` headers
4. Always include `#task` tag

**Example**:
```markdown
> [!todo]
> **Meetings:**
> - [ ] Weekly standup #task 📅 2026-01-14
>
> **Deep work:**
> - [ ] Review PR #task 📅 2026-01-14
```

## Projects Context

Active projects are tagged `#project/inprogress`. Query:
```dataview
list from #project/inprogress
```

## Schedule Update Rules

When updating the schedule:
1. Mark completed tasks with `✅` prefix in schedule
2. Keep structure and colors consistent
3. Update the `schedule` array in DataviewJS block
4. End time of one task should match start time of next (no gaps)
