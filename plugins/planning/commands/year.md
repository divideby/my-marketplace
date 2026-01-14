---
description: Годовое планирование — Harada Method (64 шага) + ретро года
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Annual Planning

Execute annual planning using Harada Method (1 goal, 8 directions, 64 steps).

**Assumes**: Running from Obsidian vault root.

## Workflow

1. Determine year
2. Full year retrospective
3. Define main goal
4. Set 8 life directions with sub-goals
5. Break into quarters
6. Identify key dates

---

## Step 1: Determine Year

```bash
date +%Y
```

File: `Base/Year-{YEAR}.md`

---

## Step 2: Load Context

1. Previous year: `Base/Year-{PREV}.md`
2. Any existing quarterly/half-year plans

---

## Step 3: Year Retrospective

Deep reflection on past year:

```
Question: "Топ-3 достижения прошлого года?"
```

```
Question: "Топ-3 провала или разочарования?"
```

```
Question: "Как ты изменился за год? Что узнал о себе?"
```

---

## Step 4: Main Goal (Harada Core)

The ONE thing that defines the year:

```
Question: "Одна главная цель на год — что сделает этот год успешным?"
```

This should be inspiring, ambitious, and specific enough to measure.

---

## Step 5: 8 Life Directions

Harada Method uses 8 areas. For each area:

**Areas:**
1. Карьера / Работа
2. Финансы
3. Здоровье
4. Отношения / Семья
5. Личностный рост
6. Отдых / Хобби
7. Окружение / Быт
8. Вклад / Влияние

For each area ask:
```
Question: "Цель в области '{area}' на год?"
```

Then:
```
Question: "8 конкретных шагов для достижения цели в '{area}'?"
```

(Can do 4 now, 4 later if overwhelming)

---

## Step 6: Quarterly Breakdown

Distribute focus across quarters:

```
Question: "Какой фокус Q1? Какие направления приоритетны?"
```

Repeat for Q2, Q3, Q4.

---

## Step 7: Key Dates

```
Question: "Важные даты года? (отпуск, события, дедлайны)"
```

---

## Step 8: Write Year File

Create `Base/Year-{YEAR}.md` with:
- Full retrospective
- Main goal
- 8 directions with sub-goals and 64 steps
- Quarterly breakdown
- Key dates
- Links to quarter files

---

## Output

```
Год {YEAR} спланирован!

Главная цель: {main goal}

8 направлений:
1. Карьера: {goal}
2. Финансы: {goal}
...

Файл: Base/Year-{YEAR}.md

Следующий шаг: /planning:quarter для Q1
```
