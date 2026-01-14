---
description: Полугодовое планирование — mid-year review + актуализация года
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Half-Year Planning

Execute half-year planning session — mid-year checkpoint.

**Assumes**: Running from Obsidian vault root.

## Workflow

1. Determine current half-year (H1: Jan-Jun, H2: Jul-Dec)
2. Review previous half-year
3. Set half-year priorities
4. Break into quarters
5. Actualize annual plan

---

## Step 1: Determine Half-Year

H1 = months 1-6, H2 = months 7-12

File: `Base/HalfYear-{YEAR}-H{N}.md`

---

## Step 2: Load Context

1. Previous half-year (or year plan if H1)
2. Year plan: `Base/Year-{YEAR}.md`
3. Quarterly OKRs

---

## Step 3: Half-Year Review

If reviewing H1 → mid-year check:
```
Question: "Полгода прошло. Как прогресс по годовым целям?"
```

If reviewing H2 → prepare for new year:
```
Question: "Что удалось во второй половине года?"
```

Ask:
```
Question: "Главные достижения полугодия?"
```

```
Question: "Что требует корректировки курса?"
```

---

## Step 4: Half-Year Priorities

Based on annual goals (Harada 8 directions):

```
Question: "Какие 3-4 направления в приоритете на это полугодие?"
```

For each priority:
```
Question: "Конкретная цель по направлению '{area}'?"
```

---

## Step 5: Quarterly Breakdown

Break half-year into 2 quarters:

```
Question: "Фокус Q{N}? Что должно быть достигнуто?"
```

```
Question: "Фокус Q{N+1}?"
```

---

## Step 6: Actualize Year

If year plan exists:

1. Review Harada 8 directions
2. Ask:
```
Question: "Годовые цели актуальны? Изменились ли приоритеты?"
Options:
- "Всё актуально"
- "Нужны корректировки"
- "Кардинально пересмотреть"
```

---

## Step 7: Write Half-Year File

Create `Base/HalfYear-{YEAR}-H{N}.md` with:
- Review previous period
- Priorities (3-4 focus areas)
- Goals per area
- Quarterly breakdown
- Link to year plan

---

## Output

```
Полугодие H{N} спланировано!

Приоритеты:
- {priority 1}
- {priority 2}
- {priority 3}

Файл: Base/HalfYear-{YEAR}-H{N}.md
```
