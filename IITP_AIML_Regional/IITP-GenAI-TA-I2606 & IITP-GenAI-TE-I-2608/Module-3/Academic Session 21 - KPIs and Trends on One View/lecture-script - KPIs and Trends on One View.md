# Lecture Script: Tableau — KPIs and Trends on One View
> **Instructor Reference** — Module 3: Tableau Dashboards + Storytelling | Academic Session 21 | Duration: 2 Hours | Instructor: Balaji

---

## Session Overview
**Goal:** Students can add a headline KPI tile with an explicitly labelled trend, build a segment comparison that can reveal what a company-wide total hides, and connect both into a dashboard using actions so it supports live analysis, not just static reporting.

**Student profile at this point:** They can assemble multiple charts into a connected dashboard using actions. They've never built a KPI tile — expect them to treat "add a KPI" as "add another chart," which misses the point of a KPI's deliberate simplicity. There's also a real risk of students reporting trend percentages without stating the comparison point, a habit worth catching immediately.

**Key outcome:** Students should leave able to explain why a company-wide KPI going up can still hide a struggling segment underneath it.

> 🎯 **The one sentence this session must land:** *A KPI tells you what's happening; a trend tells you if it's improving; a segment comparison tells you whether that improvement is real everywhere or hiding a problem.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening Hook | 8 min | 8 min |
| Concept + Practical Block 1: What Makes a KPI Tile | 20 min | 28 min |
| Concept + Practical Block 2: Showing Trends Next to a KPI | 20 min | 48 min |
| **BREAK** | 10 min | 58 min |
| Concept + Practical Block 3: Comparing Segments | 25 min | 83 min |
| Concept + Practical Block 4: Supporting Live Analysis | 27 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "The Number That Hid a Problem" (8 min)

> "Kirana365's company-wide revenue this month: up 8%. Founder's reaction: great news, right?"

Pause, then reveal the segment breakdown: Bengaluru +12%, Hyderabad +5%, Pune +9%, **Chennai -3%**.

> "The company-wide number said everything's fine. It was lying by omission. Chennai has been quietly declining for three months, and the one big rounded-up total buried it completely."

**Pivot line:** "Today you learn to build the two things that expose this: a headline KPI with an honest trend, and a segment view that never lets a single total hide a real problem underneath it."

**Context for the sessions ahead:** "KPIs are the first thing any real audience looks at on a dashboard. Everything about design and decision-support in the sessions ahead assumes you've already built these correctly."

---

## Concept Block 1: What Makes a KPI Tile (10 min)

> "Think of a KPI tile like a car's speedometer — one big number, always in the same spot, telling the driver the single most important fact right now. Nobody wants to pop the hood to check their speed."

Live demo: build a plain KPI tile showing Total Revenue as one big number, no chart, no axis, using Tableau's text/number formatting on a blank worksheet placed on the dashboard.

> "Notice what I didn't add — gridlines, a chart type, multiple numbers crammed in. That's deliberate."

### 🔴 The trap / highest-value moment
> "The trap: turning a KPI tile into a mini chart by adding clutter. Write this down: **a KPI tile should be readable from across the room. If it needs close reading, it has stopped being a KPI.**"

## Practical Block 1: Strip It Down (10 min)

Give students an over-cluttered "KPI tile" (gridlines, three overlapping numbers, tiny font) and ask them to redesign it down to one clean, large number.

**Answer key with reasoning:** The finished tile should contain exactly one number, one short label, nothing else — success is tested by asking a classmate across the room to read it without walking closer.

💬 **Expect pushback**: "Isn't more information always better?" Welcome it. Say: "Not on a KPI tile specifically — its entire job is instant absorption. More information belongs in the detail charts underneath it, which is exactly where dashboard actions come in later today."

---

## Concept Block 2: Showing Trends Next to a KPI (10 min)

> "₹12.4L alone tells you the current state, not whether that's good or bad. A trend answers 'compared to what?'"

Live demo: add "▲ 8% vs last month" beneath the Total Revenue KPI tile using a calculated field comparing this month to last month.

> "Now the same number carries direction and size of change, not just a static figure."

### 🔴 The trap / highest-value moment
> "The trap: showing '+8%' with no stated comparison point. Up 8% versus what — last month? Same month last year? A target? Write this down: **never show a trend arrow without explicitly labelling what it's compared against.**"

## Practical Block 2: Label the Comparison (10 min)

Give students three unlabelled trend numbers ("+8%", "-3%", "+15%") and ask them to write, for each, at least two plausible comparison points it could mean, then explain why the ambiguity matters.

**Answer key with reasoning:** "+8%" could mean vs last month, vs last year, or vs a target — each implies a very different story (a modest improvement vs a huge year-over-year jump vs falling short of/exceeding a goal). The point is that the same raw number can mean wildly different things depending on the hidden comparison.

💬 **Expect a question about which comparison point is "best."** Welcome it. Say: "Depends entirely on the audience's question — month-over-month for operational dashboards, year-over-year for strategic reviews. The mistake isn't picking one; it's not saying which one you picked."

---

## BREAK (10 min)

---

## Concept Block 3: Comparing Segments Within a Dashboard (13 min)

> "A single KPI is like checking your own exam score. Comparing segments is like seeing your score next to your classmates' — same number, much more meaning."

Live demo: build the segment comparison table (City, Revenue, vs Last Month) revealing Chennai's -3% hidden inside the company-wide +8%.

> "This is the exact reveal from this morning's opening — and now you can build it yourselves."

### 🔴 The trap / highest-value moment
> "The trap: reporting only the company-wide total and assuming every segment behaves the same way underneath it. Write this down: **a rising overall number can hide a declining segment — always check the breakdown before declaring victory.**"

## Practical Block 3: Find the Hidden Problem (12 min)

Give students a new dataset: company-wide Orders KPI showing +10%, broken down by Customer Segment (New Customers +25%, Repeat Customers -5%). Task: identify what the company-wide number is hiding and write a one-sentence explanation for a founder.

**Answer key with reasoning:** The +10% is driven entirely by new customer acquisition, while repeat customers — arguably the more sustainable, cheaper-to-serve group — are actually declining. A one-sentence founder explanation: "Growth looks strong, but it's coming entirely from new customers; repeat customers are quietly leaving, which is a longer-term risk worth investigating."

💬 **Expect an argument that "new customer growth is still good news."** Welcome it. Say: "It genuinely is — the point isn't that the +10% is fake, it's that celebrating it without checking underneath means missing a real, separate problem that needs its own response."

---

## Concept Block 4: Using Dashboards to Support Live Analysis (14 min)

> "A dashboard with KPIs and trends stops being a static report the moment someone can click through to 'why,' right there on the screen, without opening a new file."

Live demo: click Chennai on the segment table (using last session's dashboard action skill), watch the connected `Revenue by Category` chart filter to Chennai alone, revealing that Groceries specifically dropped while Snacks held steady.

> "That's analysis happening live. Nobody opened Excel. Nobody wrote a new SQL query. It happened inside the dashboard, in one click."

### 🔴 The trap / highest-value moment
> "The trap: building a dashboard full of KPIs and trends but with no path from the headline number into the detail behind it. A dashboard that only reports numbers, without letting someone ask 'why,' has stopped short of its real value. Write this down: **every KPI should have a path to the detail that explains it.**"

## Practical Block 4: Build the Drill-Down Path (13 min)

Students connect their own segment comparison table to a detail chart (Revenue by Category) using a filter action, then test clicking through both a growing city (Bengaluru) and the declining one (Chennai) to see two contrasting category breakdowns.

**Answer key with reasoning:** Success is a working action where clicking any city filters the category chart to that specific city's mix — the pedagogical point is comparing Bengaluru's healthy, broad-based growth against Chennai's Groceries-specific decline, proving the same mechanism reveals different real stories depending on which segment is clicked.

💬 **Expect a question about whether this could get too complex for a "simple" dashboard.** Welcome it. Say: "One well-placed action rarely adds real complexity for the viewer — it removes a click; the complexity is all on your side, building it once, well."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| KPI tiles | One big number, minimal clutter, readable from across the room |
| Trends | Never show a percentage change without stating what it's compared against |
| Segment comparison | A rising company-wide total can hide a declining segment underneath |
| Supporting live analysis | Every KPI should have a path, via an action, to the detail that explains it |

Close on the thesis: "A KPI tells you what's happening; a trend tells you if it's improving; a segment comparison tells you whether that improvement is real everywhere or hiding a problem. Today you built all three, connected together."

**Bridge to Session 22:** "Next session we zoom out from individual KPIs to the whole page — Dashboard Design Basics — applying real design principles so every part of your dashboard, not just the KPI tiles, is instantly readable."

---

## Q&A & Doubt Solving (5 min)

**Q: How many KPI tiles should one dashboard have?**
→ As a rule of thumb, 1 to 4 — beyond that, nothing feels like a genuine headline anymore, and you've built a cluttered list instead of a clear cockpit.

**Q: Can a trend indicator use colour, like green for up and red for down?**
→ Yes, and it's common — but be careful: for some metrics (like churn), "up" is bad, so a naive green-for-up rule can mislead; colour logic should follow business meaning, not just direction.

**Q: What if a segment comparison table has 20 rows, like 20 delivery partners — is that still a "quick glance" view?**
→ No — past roughly 5-8 rows, a table stops being a glance-able KPI companion and becomes its own detailed chart; consider showing only the top and bottom performers instead.

**Q: Is a KPI tile always a single number, or can it show a small trend line too?**
→ Tableau supports small "sparkline" style trend visuals right on a KPI tile — that's still acceptable as long as it stays minimal and doesn't turn into a full chart.

**Q: Should every KPI have a drill-down action, even minor ones?**
→ Prioritize actions on your headline KPIs first — not every supporting number needs one, but your one or two most important KPIs almost always should.

---

## Instructor Notes
- **Words not yet earned:** "LOD (level of detail) expressions," "table calculations," "parameters" — the trend and comparison logic today can be built with straightforward calculated fields; save the more advanced calculation techniques for later.
- **Biggest risk in this session:** Students building a technically correct trend number but never stating the comparison point out loud or on the tile — treat this as a non-negotiable habit, not an optional nicety.
- **Board management:** Keep "readable from across the room" and "never show a % without its comparison" visible throughout; add the segment-hiding-a-problem example before Concept Block 3.
- **Common confusions:**
  1. Treating a KPI tile like a small chart and over-decorating it.
  2. Reporting a trend percentage with no stated comparison baseline.
  3. Trusting a healthy company-wide KPI without checking for a hidden declining segment.
- **Cross-references:** The KPI and segment-comparison patterns here are formalized visually in Session 22 (Dashboard Design Basics) and used directly for real decision-making in Session 23 (Dashboards That Support Decisions).
- **Local/cultural context notes:** The car-speedometer and exam-score analogies land well with this cohort; keep the Chennai-decline example prominent, since a real, specific city "hiding" behind a healthy total makes the segment-comparison lesson concrete rather than abstract.
