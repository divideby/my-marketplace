// DataviewJS Schedule Template for Obsidian Daily Notes
// Copy this entire block into the ## Расписание section

/*
Usage:
1. Define schedule array with time blocks
2. Each block: { time: "HH:MM", end: "HH:MM", task: "Icon Description", color: "#..." }
3. Short breaks: add isBreak: true

Color palette:
- #4ade8033 - green (meals)
- #c4b5fd44 - lavender (routines)
- #60a5fa44 - blue (deep work)
- #a78bfa44 - purple (meetings)
- #fbbf2444 - amber (exercise)
- #67e8f933 - cyan (health)
- #f9a8d433 - pink (breaks)
- #f9a8d422 - pink transparent (short breaks with isBreak: true)
*/

const schedule = [
  { time: "07:00", end: "07:30", task: "🍳 Завтрак", color: "#4ade8033" },
  { time: "07:30", end: "08:00", task: "✅ Медитация", color: "#c4b5fd44" },
  { time: "08:00", end: "10:00", task: "💻 Deep work block 1", color: "#60a5fa44" },
  { time: "10:00", end: "10:05", task: "", color: "#f9a8d422", isBreak: true },
  { time: "10:05", end: "12:00", task: "💻 Deep work block 2", color: "#60a5fa44" },
  { time: "12:00", end: "12:30", task: "🍽️ Обед", color: "#4ade8033" },
  { time: "12:30", end: "13:00", task: "☕ Отдых", color: "#f9a8d433" },
  { time: "13:00", end: "14:00", task: "📅 Встреча", color: "#a78bfa44" },
  { time: "14:00", end: "16:00", task: "💻 Deep work block 3", color: "#60a5fa44" },
  { time: "16:00", end: "17:00", task: "🏋️ Тренировка", color: "#fbbf2444" },
  { time: "17:00", end: "18:00", task: "🌅 Завершение дня", color: "#f9a8d433" },
];

const toMinutes = (t) => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };

const container = dv.el("div", "");

function render() {
  const now = new Date();
  const nowMinutes = now.getHours() * 60 + now.getMinutes();
  const nowTime = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

  let html = `<div style="font-family: sans-serif; font-size: 13px; width: 300px;">`;

  for (const item of schedule) {
    const startMin = toMinutes(item.time);
    const endMin = toMinutes(item.end);
    const duration = endMin - startMin;
    const isBreak = item.isBreak;
    const height = isBreak ? 8 : Math.max(30, duration);

    const isCurrentBlock = nowMinutes >= startMin && nowMinutes < endMin;
    const progressPercent = isCurrentBlock ? ((nowMinutes - startMin) / duration) * 100 : 0;

    const timeLine = isCurrentBlock ? `
      <div style="position: absolute; top: ${progressPercent}%; left: 0; right: 0; height: 2px; background: #ef4444; z-index: 10;">
        <div style="position: absolute; left: -6px; top: -4px; width: 10px; height: 10px; background: #ef4444; border-radius: 50%;"></div>
        <span style="position: absolute; left: 12px; top: -7px; color: #ef4444; font-size: 10px; background: var(--background-primary); padding: 0 4px; border-radius: 3px;">${nowTime}</span>
      </div>
    ` : "";

    html += `
    <div style="display: flex; border-left: 2px solid #444;">
      <div style="width: 45px; text-align: right; padding-right: 8px; color: #888;">${isBreak ? "" : item.time}</div>
      <div style="flex: 1; min-height: ${height}px; border-top: ${isBreak ? "none" : "1px solid #333"}; background: ${item.color}; padding: ${isBreak ? "0" : "4px"}; border-radius: 4px; margin: 2px; position: relative;">
        ${item.task}${timeLine}
      </div>
    </div>`;
  }

  // End marker
  const lastItem = schedule[schedule.length - 1];
  html += `
    <div style="display: flex; border-left: 2px solid #444;">
      <div style="width: 45px; text-align: right; padding-right: 8px; color: #888;">${lastItem.end}</div>
      <div style="flex: 1; min-height: 20px; border-top: 1px solid #333;"></div>
    </div>
  </div>`;

  container.innerHTML = html;
}

render();
const intervalId = setInterval(render, 60000);

this.container.addEventListener("unload", () => clearInterval(intervalId));
