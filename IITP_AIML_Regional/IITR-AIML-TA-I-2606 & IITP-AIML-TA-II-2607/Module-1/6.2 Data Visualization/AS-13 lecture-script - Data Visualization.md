# Lecture Script: Foundations of Data — Data Visualization
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 13 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can build line, bar, scatter, and histogram plots using Matplotlib, build a basic interactive Plotly chart, and choose the correct chart type based on the variable type and analytical goal.

**Student profile at this point:** Just completed the Master class on coordinate geometry and statistics (Session 6.1) — has the mathematical foundation but hasn't yet built a real chart. Likely wrong assumption: that chart type is a stylistic choice rather than something determined by the data and question. Boredom risk is low — this is highly visual and satisfying; confidence risk is moderate around correctly distinguishing bar charts from histograms.

**Key outcome:** Students should leave with a decision habit: before building any chart, first ask "am I comparing categories, showing a trend, showing a relationship, or showing a distribution?" — and let that answer dictate the chart type.

> 🎯 **The one sentence this session must land:** *The chart type isn't a style choice — it's determined by the question you're asking and the type of variable(s) you're showing.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Chart With No Name" | 8 min | 8 min |
| Concept + Practical Block 1: Line & Bar Charts | 22 min | 30 min |
| Concept + Practical Block 2: Scatter Plots & Histograms | 25 min | 55 min |
| ☕ BREAK | 5 min | 60 min |
| Concept + Practical Block 3: Labels, Titles & Legends | 18 min | 78 min |
| Concept + Practical Block 4: Plotly & Choosing the Right Chart | 22 min | 100 min |
| Summary & Bridge | 5 min | 105 min |
| Q&A & Doubt Solving | 15 min | 120 min |

---

## Opening — "The Chart With No Name" (8 min)

Project a bare Matplotlib chart on screen — a plotted line with no title, no axis labels, nothing.

> "What does this chart show? Take a guess."

[Let students genuinely try and fail to guess confidently — the point is that it's IMPOSSIBLE to know for certain.]

> "You built the mathematics behind this in the last session — you know it's data mapped onto (x, y) coordinates. But without labels, this chart is useless to anyone except the person who built it, and honestly, even to them a week later. Today, you'll learn not just to build charts, but to build ones that actually communicate."

Pivot line: "Let's start with the two most common chart types you'll reach for constantly — line and bar."

---

## Concept + Practical Block 1: Line & Bar Charts (22 min)

### "Petrol prices over the week vs. sales across branches"
> "Petrol prices changing day by day — that's a trend over time, told with a line chart. Sales totals across three different branches — that's a comparison between categories, told with a bar chart. Same data structure, completely different chart."

**Hands-on, live-coded:**
```python
import matplotlib.pyplot as plt

dates = ["Mon", "Tue", "Wed", "Thu", "Fri"]
petrol_prices = [102.5, 102.7, 102.6, 103.0, 103.2]
plt.plot(dates, petrol_prices)
plt.show()

branches = ["Hyderabad", "Mumbai", "Delhi"]
sales = [45000, 62000, 38000]
plt.bar(branches, sales)
plt.show()
```

**Answer key / reasoning to say aloud:** Point at the line chart's connecting lines between days — "Monday connects meaningfully to Tuesday, there's a real sequence here." Then point at the bar chart — "there's no meaningful 'between' Hyderabad and Mumbai — they're just separate categories sitting side by side."

### 🔴 The trap / highest-value moment
Write on the board: **"A line chart implies a meaningful SEQUENCE between points. Never use it for unordered categories like branch names."**

Demonstrate live: force a line chart using the branch data instead of a bar chart, and ask the room: "does this line between Hyderabad and Mumbai mean anything real?"

💬 **Expect an argument about:** "Couldn't I just use a bar chart for everything to be safe?" Welcome it. Say: *"You could, and it's rarely 'wrong' to use a bar chart for categories — but a line chart genuinely communicates trend-over-time better than a bar chart would, especially with many time points. The skill is matching the chart to what the data actually represents."*

---

## Concept + Practical Block 2: Scatter Plots & Histograms (25 min)

### "Study hours vs. marks, and the shape of a class's scores"
> "Plotting each student's study hours against their marks — one dot per student — reveals whether the two move together. That's a scatter plot: relationship between two variables. Counting how many students fall into each score range — that's a histogram: the shape of ONE variable."

**Hands-on:**
```python
hours_studied = [2, 4, 5, 7, 8]
marks_scored = [40, 55, 60, 78, 85]
plt.scatter(hours_studied, marks_scored)
plt.show()

exam_scores = [45, 67, 89, 34, 56, 78, 90, 23, 65, 71]
plt.hist(exam_scores, bins=5)
plt.show()
```

Ask the room: "Looking at the scatter plot, does more study time seem related to higher marks?" — let them read the trend directly off the dots, connecting back to slope from the Master class.

**Answer key / reasoning to say aloud:** Point out that the histogram's bars represent RANGES of score (like 40-60), not individual students or categories — this is the key visual and conceptual difference from a bar chart.

### 🔴 The trap / highest-value moment
Write on the board: **"A bar chart compares CATEGORIES. A histogram groups a CONTINUOUS range into bins. Both use bars — they are NOT the same chart."**

💬 **Expect an argument about:** "They genuinely look almost identical — how do I tell them apart at a glance?" Welcome it. Say: *"Check the x-axis. If it lists distinct names (Hyderabad, Mumbai, Delhi), it's a bar chart. If it lists numeric ranges (0-20, 20-40, 40-60), it's a histogram. That single check resolves the confusion every time."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: Labels, Titles & Legends (18 min)

### "The beautiful map with no place names"
> "A perfectly drawn map with no place names is technically accurate and completely useless to anyone but the person who drew it. That's exactly what an unlabeled chart is."

**Hands-on — rebuild the opening hook's chart properly:**
```python
plt.plot(dates, petrol_prices)
plt.title("Weekly Petrol Prices — Hyderabad")
plt.xlabel("Day")
plt.ylabel("Price (₹ per litre)")
plt.show()
```

> "This is the exact chart from our opening — now anyone, including you in six months, can understand it in three seconds."

**Answer key / reasoning to say aloud:** Walk through why each piece matters specifically — the title answers "what am I looking at," the axis labels answer "what do these numbers mean," and (when multiple lines are present) a legend answers "which line is which."

### 🔴 The trap / highest-value moment
Write on the board: **"Labels aren't optional polish — add them AS you build the chart, not as an afterthought. An unlabeled chart fails at its actual job."**

💬 **Expect an argument about:** "For a quick personal exploration, do I really need to label everything every time?" Welcome it. Say: *"For a chart you're only glancing at yourself, mid-analysis, sure, skip it. But the MOMENT that chart is going into a report, a presentation, or shared with anyone else — even your own future self a week later — full labeling is non-negotiable."*

---

## Concept + Practical Block 4: Plotly & Choosing the Right Chart (22 min)

### "The touchable stock chart vs. the printed newspaper graph"
> "A static Matplotlib chart is like a graph printed in a newspaper — fixed, final. A Plotly chart is like the interactive stock charts on a money-control app — you can hover to see exact values, zoom into a date range."

**Hands-on:**
```python
import plotly.express as px

fig = px.line(x=dates, y=petrol_prices, title="Weekly Petrol Prices")
fig.show()
```

> "Notice — same data, same basic chart type, but now genuinely explorable."

**Decision framework — build live with the room, testing it against every example from today:**

| Situation | Chart type |
|---|---|
| Trend over time | Line chart |
| Comparing categories | Bar chart |
| Relationship between two variables | Scatter plot |
| Distribution of one variable | Histogram |
| Viewer needs to explore | Plotly |

### 🔴 The trap / highest-value moment
Write on the board: **"Choose the chart type that answers the question — not the fanciest or most 'impressive-looking' one available."**

💬 **Expect an argument about:** "Shouldn't I just always use Plotly then, since it's strictly more capable than Matplotlib?" Welcome it. Say: *"Interactivity isn't always useful — for a printed report or a quick static comparison, Matplotlib is simpler, faster to build, and often clearer. Reach for Plotly specifically when someone actually needs to explore the data themselves, not by default."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Line & bar charts | Line = trend over sequence; bar = comparison between categories |
| Scatter & histogram | Scatter = relationship between two variables; histogram = distribution of one |
| Labels, titles & legends | A chart without these fails to communicate — add them as you build, not after |
| Plotly & chart choice | Choose based on the question, not visual appeal — Plotly when exploration is needed |

Close on the thesis: *"The chart type isn't a style choice — it's determined by the question you're asking and the type of variable(s) you're showing."*

Bridge: "Today you learned to build individual charts. Next session, you'll use these exact tools inside a structured investigation of a real dataset — asking business questions and letting the data answer them — in **EDA & Business Thinking**."

---

## Q&A & Doubt Solving (15 min)

**Q: Can I show more than one line on the same line chart?**
→ Yes — calling `plt.plot()` multiple times before `plt.show()` overlays multiple lines on the same chart, and `plt.legend()` lets you label which line is which.

**Q: How do I decide how many bins to use in a histogram?**
→ There's no single correct number — too few bins hides detail, too many creates noise; a common starting point is somewhere between 5 and 20 bins, then adjusting based on how clearly the shape of the distribution comes through.

**Q: Is Plotly harder to learn than Matplotlib?**
→ Not really — Plotly Express (`plotly.express`) is designed to be nearly as simple as Matplotlib for common chart types, while adding interactivity essentially for free.

**Q: Can I combine a scatter plot with a trend line showing the slope from the Master class?**
→ Yes — this is a very common combination, often called a "regression line" or "trend line" overlaid on a scatter plot, directly connecting back to the slope concept from Session 6.1.

**Q: What if my data has both a time trend AND multiple categories I want to compare?**
→ You can often use a multi-line chart (one line per category, over time) or a grouped bar chart — the right choice again depends on exactly what comparison you want the viewer to make most easily.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "subplot," "figure vs axes objects," "colormaps," "faceting." These are more advanced Matplotlib/Plotly features worth flagging as "possible later" but not needed for this foundational session.
- **Biggest risk this session:** bar-chart-vs-histogram confusion in Block 2 — spend extra time on the "check the x-axis" trick, since this distinction is genuinely subtle and will resurface directly in the EDA session next.
- **Board management:** Keep the "which chart, when" decision table from Block 4 visible for the rest of the session once built — it functions as the session's complete summary and should be referenced explicitly during Q&A.
- **Common confusions, numbered:**
  1. Using a line chart to connect unrelated categories.
  2. Confusing a bar chart (categories) with a histogram (numeric ranges/bins).
  3. Treating labels, titles, and legends as optional finishing touches rather than essential communication.
- **Cross-references to later sessions:** Every chart type here becomes a working tool inside the EDA checklist (Session 6.3) — histograms specifically resurface for spotting skewness and outliers; scatter plots resurface for correlation analysis in the same session.
- **Local/cultural context notes:** Petrol price tracking, kirana/branch sales comparison, and money-control-style stock charts continue the running Indian-context thread — the study-hours-vs-marks scatter plot deliberately echoes the slope discussion from the Master class for continuity.
