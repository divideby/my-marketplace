---
name: planning-methods
description: Provides knowledge of strategic planning methodologies (GTD, Jedi Techniques, Harada Method, OKRs, 12 Week Year). Activates when user plans weeks, months, quarters, or years. Use for goal setting, review sessions, prioritization, and task decomposition.
---

# Planning Methods

Knowledge base for strategic planning across different time horizons.

## Core Methodologies

### GTD (Getting Things Done)

**Use for**: Processing inputs, organizing tasks, weekly reviews.

**Key concepts**:
- **Capture**: Get everything out of your head into a trusted system
- **Clarify**: Process each item — is it actionable?
- **Organize**: Put items where they belong (next actions, projects, someday)
- **Reflect**: Regular reviews to stay current
- **Engage**: Do the work with confidence

**Weekly Review checklist**:
1. Get clear (inbox zero, collect loose papers)
2. Get current (review calendars, action lists, projects)
3. Get creative (review someday/maybe, think about what's new)

### Джедайские техники (Jedi Techniques)

**Use for**: Focus, energy management, saying "no".

**Key concepts**:
- **Мыслетопливо**: Cognitive resources are limited — protect them
- **Инбокс-зеро**: Empty inbox = clear mind
- **Контекст "Не делать"**: Sometimes the best action is no action
- **Правило 2 минут**: If it takes <2 min, do it now
- **Фокус-блоки**: Protected time for deep work

**Energy management**:
- Morning = high energy → deep work
- Afternoon = moderate → meetings, collaboration
- Evening = low → admin, routine

### Harada Method (64 Steps)

**Use for**: Long-term goal decomposition (year, half-year, quarter).

**Structure**:
1. **1 Main Goal** — the ultimate objective
2. **8 Sub-goals** — supporting objectives
3. **64 Action Items** — concrete steps (8 per sub-goal)

**Template**:
```
Main Goal: [Your big vision]

Sub-goal 1: [Support area]
  - Action 1.1
  - Action 1.2
  ... (8 actions)

Sub-goal 2: [Support area]
  - Action 2.1
  ...
```

### OKRs (Objectives & Key Results)

**Use for**: Quarterly and annual planning.

**Structure**:
- **Objective**: Qualitative, inspiring, time-bound
- **Key Results**: 3-5 quantitative metrics that measure success

**Example**:
```
Objective: Launch successful product beta
Key Results:
- 100 beta users signed up
- NPS score > 40
- <5 critical bugs reported
```

**Grading**: 0.0-1.0 scale, 0.7 = success

### 12 Week Year

**Use for**: Quarterly planning with urgency.

**Concept**: Treat 12 weeks as a "year" — creates urgency without burnout.

**Weekly structure**:
- Week 1-11: Execute tactics
- Week 12: Buffer week
- Week 13: Review and plan next "year"

**Weekly Accountability**:
- Score execution (did you do what you planned?)
- Adjust tactics, not goals

## Horizon-Specific Guidance

### Week Planning

**Review**: GTD weekly review
**Methods**: Jedi techniques for focus blocks
**Output**:
- 3-5 weekly focuses
- Daily task distribution
- Protected deep work time

### Month Planning

**Review**: Check progress on quarterly OKRs
**Methods**: Jedi + GTD
**Output**:
- Monthly themes/focuses
- Key milestones
- Habits to maintain

### Quarter Planning

**Review**: Grade previous quarter's OKRs
**Methods**: OKRs + 12 Week Year
**Output**:
- 1-3 Objectives with Key Results
- 12-week execution plan
- Weekly milestones

### Half-Year Planning

**Review**: Mid-year check on annual goals
**Methods**: Harada (partial) + OKRs
**Output**:
- Progress assessment
- Course corrections
- Next half priorities

### Year Planning

**Review**: Full retrospective
**Methods**: Harada Method (64 steps)
**Output**:
- Annual vision (1 main goal)
- 8 sub-goals across life areas
- Quarterly breakdown

## Cascade Logic

**Actualization happens upward**:
- Weekly review → check monthly relevance
- Monthly review → check quarterly OKRs
- Quarterly review → check half-year goals
- Half-year review → check annual vision

**Questions for actualization**:
1. Is the higher-level goal still relevant?
2. Are we on track or need adjustment?
3. Has context changed significantly?

## File Naming Convention

Store in `Base/` with consistent naming:
- `Week-2026-W03.md`
- `Month-2026-01.md`
- `Quarter-2026-Q1.md`
- `HalfYear-2026-H1.md`
- `Year-2026.md`

## Template References

See `${CLAUDE_PLUGIN_ROOT}/skills/planning-methods/references/` for:
- `week-template.md`
- `month-template.md`
- `quarter-template.md`
- `year-template.md`
