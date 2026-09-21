# Lecture Script: Tableau — Building a Dashboard
> **Instructor Reference** — Module 3: Tableau Dashboards + Storytelling | Academic Session 20 | Duration: 2 Hours | Instructor: Balaji

---

## Session Overview
**Goal:** Students can combine multiple existing Tableau sheets into a single dashboard, arrange them in a layout that mirrors natural reading order, and connect at least one pair of charts using a dashboard action.

**Student profile at this point:** They can build well-chosen, well-formatted individual charts. They've never assembled several charts into one connected view. Expect the natural but wrong assumption that a dashboard is "just a bigger canvas to draw more charts on" rather than a container for finished sheets — this needs correcting early and explicitly.

**Key outcome:** Students should leave able to explain, in one sentence, why a dashboard is more useful than the same charts sent as separate images.

> 🎯 **The one sentence this session must land:** *A dashboard isn't a bigger chart — it's a container that brings finished charts together so someone can understand the whole business in one glance.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening Hook | 8 min | 8 min |
| Concept + Practical Block 1: What a Dashboard Actually Is | 20 min | 28 min |
| Concept + Practical Block 2: Adding Multiple Charts | 22 min | 50 min |
| **BREAK** | 10 min | 60 min |
| Concept + Practical Block 3: Arranging the Layout | 25 min | 85 min |
| Concept + Practical Block 4: Dashboard Actions | 25 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "Five Emails or One Link" (8 min)

> "Picture Kirana365's ops manager's inbox this morning: five separate emails, each with one chart attached — city revenue, daily trend, category mix, delivery times, customer segments. She has to open all five, hold them in her head at once, and mentally cross-reference them."

Show, side by side: five separate chart screenshots vs one assembled dashboard screen showing all five at once.

> "Same five charts. One version costs her ten minutes and real mental effort every single morning. The other costs her ten seconds."

**Pivot line:** "Today you build that second version for the first time — not a new chart, but a container that brings your existing charts together."

**Context for the sessions ahead:** "This is the dashboard skill everything else in this module sits on top of — KPIs, design polish, and decision-support all assume you can already assemble one of these."

---

## Concept Block 1: What a Dashboard Actually Is (10 min)

> "A single chart is one photo from a trip. A dashboard is the photo album — several related photos arranged together so the whole story makes sense at once."

Show the Tableau interface: point out the difference between a **Sheet** tab and a **Dashboard** tab.

> "This distinction matters more than it looks. A dashboard doesn't let you draw a new bar directly — it's built entirely from sheets you've already finished."

### 🔴 The trap / highest-value moment
> "The trap: thinking a dashboard is just a bigger blank canvas for more charts. Write this down: **a dashboard is a container assembled from finished sheets, not a place to build new ones from scratch.**"

## Practical Block 1: Sheet or Dashboard? (10 min)

Show five Tableau screenshots (some Sheet tabs, some Dashboard tabs, some ambiguous) and ask students to identify which is which, and how they knew.

**Answer key with reasoning:** Sheet tabs show the Rows/Columns shelves and Marks card actively available for editing fields; Dashboard tabs show a canvas with a sheet list on the left and no direct Rows/Columns editing — that structural difference is the reliable tell, not just visual style.

💬 **Expect a question about whether you can still filter a chart while inside a dashboard.** Welcome it. Say: "Yes — dashboards have their own filter and action tools, which we cover today and next time. You're just not building brand-new bars or lines directly there."

---

## Concept Block 2: Adding Multiple Charts (11 min)

> "Before today's dashboard exists, three sheets need to already exist: Revenue by City, Daily Revenue Trend, Revenue by Category. We built versions of all three across the last two sessions."

Live demo: create a new Dashboard tab, then drag each of the three sheets from the sheet list onto the canvas one at a time.

> "Watch what happens if I now change something on the dashboard version of this chart — say, switch a filter."

Demonstrate that editing the chart inside the dashboard also updates the original sheet.

### 🔴 The trap / highest-value moment
> "This confuses everyone the first time. Rule to write down: **charts inside a dashboard are live references to the same sheet — not copies. Edit one, and you've edited both. If you want a different version, duplicate the sheet first.**"

## Practical Block 2: Build the Three-Chart Dashboard (11 min)

Students create their own new dashboard and drag in their own versions of the three Kirana365 sheets, confirming all three appear and update correctly.

**Answer key with reasoning:** Success is a dashboard showing all three charts simultaneously, correctly reflecting the underlying Kirana365 data — the grading focus is whether students understand these are references, tested by asking them to change a filter on one sheet and observe it update on the dashboard.

💬 **Expect pushback**: "This feels like it should be more complicated." Welcome it. Say: "The mechanics are genuinely this simple — drag and drop. The judgement calls, which we get to next, about arrangement and connection, are where the real skill lives."

---

## BREAK (10 min)

---

## Concept Block 3: Arranging the Layout (13 min)

> "Arranging dashboard charts is like laying out vegetables at a sabzi mandi stall — the biggest, most important items go at eye level, front and centre. Smaller supporting items go to the side."

Live demo: rearrange the three-chart dashboard so `Daily Revenue Trend` sits at the top (full width), with `Revenue by City` and `Revenue by Category` side by side underneath.

> "This mirrors how a manager actually scans a page — trend first, since it answers 'how are we doing right now,' then the two breakdowns that explain why."

### 🔴 The trap / highest-value moment
> "The trap: cramming too many charts in because Tableau technically allows it. Past 4 to 6 charts on one dashboard, everything shrinks and nobody can read anything. Write this down: **if you're tempted to add a 7th chart, you probably need a second dashboard page, not a smaller version of chart 7.**"

## Practical Block 3: Fix the Bad Layout (12 min)

Give students a deliberately poorly arranged dashboard — least-important chart (delivery-partner breakdown) at the top, daily trend buried at the bottom, all four charts squeezed into equal tiny tiles. Task: rearrange it following the top-to-bottom, most-important-first principle.

**Answer key with reasoning:** The daily trend should move to the top (or largest position), with supporting breakdowns arranged below or beside it in a clear visual hierarchy — the specific pixel layout matters less than demonstrating the reasoning behind what goes where.

💬 **Expect an argument about "what counts as most important."** Welcome it. Say: "That depends on the question the dashboard is meant to answer for its specific audience — which is exactly the judgement call you'll practice more in Session 22, Dashboard Design Basics."

---

## Concept Block 4: Dashboard Actions — Making Charts Talk (13 min)

> "Right now our three charts sit next to each other but don't know about each other. A dashboard action changes that."

Live demo: add a filter action so clicking "Bengaluru" on the `Revenue by City` chart automatically filters `Revenue by Category` to show only Bengaluru's breakdown.

> "Watch — one click, and the whole dashboard drills down together. That's the difference between a collage and a connected experience."

### 🔴 The trap / highest-value moment
> "The trap: building several genuinely related charts and never connecting them, leaving the reader to manually cross-reference by eye — which defeats half the point of putting them on one screen together. Even one well-placed action transforms a dashboard."

## Practical Block 4: Add Your Own Action (12 min)

Students add a filter action of their own to their three-chart dashboard, connecting `Revenue by City` to `Revenue by Category`, and test it by clicking through two different cities.

**Answer key with reasoning:** A correctly built action updates the category chart the moment a city bar is clicked, and resets when clicked again — testing both behaviours confirms the action is genuinely working, not just visually coincidental.

💬 **Expect a question about "what if I want the action to work the opposite direction?"** Welcome it. Say: "You can add actions in both directions, or even chain more than two charts together — we'll build on this specific skill again once we cover full decision-support dashboards."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| What a dashboard is | A container assembled from finished sheets, not a bigger blank canvas |
| Adding multiple charts | Dashboard charts are live references to the original sheet, not copies |
| Arranging the layout | Most important chart goes top/largest; past 4-6 charts, split into pages |
| Dashboard actions | Connecting charts with a click turns a collage into one experience |

Close on the thesis: "A dashboard isn't a bigger chart — it's a container that brings finished charts together so someone can understand the whole business in one glance. You built exactly that today."

**Bridge to Session 21:** "Next session we add headline KPI numbers and trend indicators to this same dashboard — turning it from a gallery of charts into something closer to a cockpit."

---

## Q&A & Doubt Solving (5 min)

**Q: Can a dashboard include a sheet from a completely different data source?**
→ Yes, Tableau supports multiple data sources on one dashboard, though it adds complexity we'll leave for a later, more advanced context.

**Q: How many dashboards can one Tableau workbook hold?**
→ As many as you need — large real-world workbooks often hold dozens, organised by audience or business area.

**Q: If I resize the dashboard, do the charts resize automatically?**
→ Yes, using Tableau's "Fit" and container/layout tools, which is part of why planning your layout structure matters before you start dragging charts in.

**Q: What's the difference between a filter action and a highlight action?**
→ A filter action actually removes non-matching data from other charts; a highlight action just visually emphasizes matching data while keeping everything else visible — useful when you don't want to filter anything away.

**Q: Should every dashboard have at least one action?**
→ Not strictly required, but any dashboard with genuinely related charts almost always benefits from at least one — it's one of the cheapest improvements you can make.

---

## Instructor Notes
- **Words not yet earned:** "parameters," "calculated KPIs," "dashboard extensions" — these come later; today stays focused on assembly, layout, and basic actions.
- **Biggest risk in this session:** Students rushing past the "dashboard charts are live references" concept because the drag-and-drop mechanics feel too easy — slow down deliberately on this point since it causes real confusion later if missed now.
- **Board management:** Keep "container, not canvas" and the sabzi-mandi layout principle visible throughout; add the thesis line before Concept Block 4.
- **Common confusions:**
  1. Believing a dashboard lets you build new charts directly on it.
  2. Being surprised that editing a chart inside a dashboard changes the original sheet.
  3. Cramming too many charts into one dashboard instead of splitting into pages.
- **Cross-references:** This session's layout hierarchy is formalized further in Session 22 (Dashboard Design Basics), and dashboard actions return in full force in Session 23 (Dashboards That Support Decisions).
- **Local/cultural context notes:** The sabzi-mandi stall-layout analogy and the "five emails vs one link" opening both land well with this cohort; continue framing every chart and dashboard around Kirana365's real operational needs across its four cities.
