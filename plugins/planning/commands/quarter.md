---
description: Квартальное планирование — OKRs + 12 Week Year + актуализация полугодия
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Quarterly Planning

Execute quarterly planning using OKRs and 12 Week Year methodology.

**Assumes**: Running from Obsidian vault root.

## Workflow

1. Determine current quarter
2. Grade previous quarter's OKRs
3. Set new OKRs
4. Create 12-week execution plan
5. Actualize half-year plan

---

## Step 1: Determine Quarter

```bash
# Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec
date +%Y
```

Calculate quarter from current month.

File: `Base/Quarter-{YEAR}-Q{N}.md`

---

## Step 2: Load Context

1. Previous quarter: `Base/Quarter-{PREV}.md`
2. Half-year plan: `Base/HalfYear-{YEAR}-H{N}.md`
3. Year plan: `Base/Year-{YEAR}.md`

---

## Step 3: Grade Previous OKRs

If previous quarter exists:

For each Objective, ask:
```
Question: "Objective: {obj}. Оценка Key Results (0.0-1.0)?"
```

Calculate overall score. 0.7+ = success.

Ask:
```
Question: "Главные уроки квартала?"
```

---

## Step 4: Set New OKRs

Explain OKR format:
- Objective = qualitative, inspiring
- Key Results = 3-5 quantitative metrics

Ask:
```
Question: "Objective 1 на этот квартал? (качественная цель)"
```

For each objective:
```
Question: "Key Results для '{objective}'? (измеримые результаты)"
```

Recommend 1-3 objectives max.

---

## Step 5: 12-Week Execution Plan

Break quarter into 3 months.

For each month:
```
Question: "Тема месяца {N}? Ключевые milestones?"
```

---

## Step 6: Actualize Half-Year

If half-year file exists:

1. Show half-year goals
2. Ask:
```
Question: "Полугодовые цели актуальны?"
Options:
- "Да, на треке"
- "Нужна корректировка"
- "Посмотреть план"
```

---

## Step 7: Write Quarter File

Create `Base/Quarter-{YEAR}-Q{N}.md` with:
- Ретро + OKR scores
- New OKRs (objectives + key results)
- 12-week plan by month
- Weekly scorecard template
- Link to half-year

---

## Output

```
Квартал Q{N} спланирован!

OKRs:
1. {Objective 1}
   - KR: {key result}

Файл: Base/Quarter-{YEAR}-Q{N}.md
```
