# Lecture Script: Tableau — Tableau Basics and First Charts
> **Instructor Reference** — Module 3: Tableau Dashboards + Storytelling | Academic Session 17 | Duration: 2 Hours | Instructor: Balaji

---

## Session Overview
**Goal:** Students can load a real dataset into Tableau and independently build a bar chart and a line chart by correctly mapping fields to Rows, Columns, and the Marks card.

**Student profile at this point:** They've spent 9 sessions writing SQL — SELECT, WHERE, GROUP BY, JOIN, subqueries, CTEs. They are fluent in getting the *right rows back*, but they've never had to make those rows understandable to someone else at a glance. Expect two wrong assumptions: (1) that Tableau is "just a fancier Excel," which underestimates it, and (2) mild boredom risk if the session opens with menus and buttons instead of a real "aha" moment — SQL learners want to see something they couldn't easily see with a query.

**Key outcome:** Students should leave asking, "if a bar chart shows me this much in ten seconds, what else in my data have I been missing by only looking at tables?"

> 🎯 **The one sentence this session must land:** *A chart isn't decoration on top of your data — it's a different, faster way of reading the same truth.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening Hook | 8 min | 8 min |
| Concept + Practical Block 1: The Tableau Interface | 25 min | 33 min |
| Concept + Practical Block 2: Loading Data | 20 min | 53 min |
| **BREAK** | 10 min | 63 min |
| Concept + Practical Block 3: Bar Charts | 25 min | 88 min |
| Concept + Practical Block 4: Line Charts | 22 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "The 4,000-Row Wall" (8 min)

Open by projecting a raw spreadsheet of Kirana365's August order data — the full 4,000+ row export, unsorted, unformatted, just rows.

> "Take fifteen seconds. Look at this sheet and tell me: which city is Kirana365's strongest market right now."

Let the silence sit. Nobody can answer in fifteen seconds — that's the point.

> "You could write a SQL query for this in your sleep by now — `GROUP BY city, SUM(revenue), ORDER BY` — and you'd have the right numbers in five seconds. But watch what happens when I don't give you numbers. I give you *this*."

Switch to a pre-built Tableau bar chart of Revenue by City — four bars, Bengaluru clearly tallest.

> "Same data. Same truth. But now you didn't calculate the answer — you *saw* it."

**Pivot line:** "Today we're not learning a new way to calculate. We're learning a new way to *see*. Everything you've built in SQL so far becomes ten times more useful once someone else — your manager, a founder, a client — can look at it for three seconds and get it."

**Context for the sessions ahead:** "This is session 1 of 9 in our Tableau module. Everything from here — dashboards, KPIs, storytelling with insights — starts from the two chart types you'll build with your own hands today."

---

## Concept Block 1: The Tableau Interface (13 min)

> "Before we touch a single chart, we need to know where things live. Think of Tableau like a thali plate — separate compartments, each with exactly one job. Mix them up and the whole plate looks wrong."

Walk the room through the four zones live, projected: **Data pane** (left — Dimensions in blue, Measures in green), **Rows/Columns shelves** (top), **Marks card** (controls how marks look), **Canvas** (where the chart actually appears).

> "Blue pill, green pill — memorize this now. Blue is a category you group by. Green is a number you calculate with. Ninety percent of 'why is my chart broken' questions in the next eight weeks come down to someone ignoring this colour."

### 🔴 The trap / highest-value moment
Drag a Measure (Revenue) into a slot where Tableau expects a Dimension, in front of the class, and let it produce a nonsense chart (a single unbroken bar, or an error).

> "See that? Tableau isn't confused — I am. Write this rule down: **blue pill groups, green pill calculates.** Every time a chart looks wrong, check this first before you check anything else."

## Practical Block 1: Pill Sorting Sprint (12 min)

Give students the Kirana365 dataset already connected on their own machines. Ask them to simply open the Data pane and, without building any chart yet, correctly sort five fields (`City`, `Category`, `Order Date`, `Revenue`, `Quantity`) into "would group by this" vs "would calculate with this," writing their answer on paper first.

**Answer key with reasoning:**
- `City`, `Category` → group by (Dimensions) — they're labels, not quantities
- `Order Date` → group by, but special — it's a Dimension that behaves like a sequence, which is why it can drive a line chart
- `Revenue`, `Quantity` → calculate with (Measures) — you can sum, average, or count them

💬 **Expect an argument about `Order Date`.** Some students will insist a date is "not a category." Welcome it. Say: "You're half right — it's a Dimension, but a special ordered one. That's exactly why it's the one field we use to build a *line* chart later today. Hold that thought."

---

## Concept Block 2: Loading Data (10 min)

> "None of this works without ingredients. Think of this step as handing your chef the grocery bag before you ask for a dish."

Demonstrate live: **Connect to a File** → select the Kirana365 orders CSV → preview grid appears → drag table to canvas → click Sheet 1.

> "Look at the preview screen before you click anything else. This is your last chance to catch a problem before it becomes an hour of confusion later."

### 🔴 The trap / highest-value moment
Load a deliberately "dirty" version of the file where one `Revenue` cell has a stray ₹ symbol typed directly into it, causing the whole column to load as text (a blue pill instead of green).

> "This single row broke the entire column. Rule to write down: **after loading any file, scan the Data pane — every number field should be green. If one isn't, go hunt for the one bad row before you build anything.**"

## Practical Block 2: Spot the Broken Column (10 min)

Give each student (or pair) the same deliberately dirty file. Task: find which column loaded incorrectly and identify the exact row causing it.

**Answer key with reasoning:** The `Revenue` column shows as a Dimension (blue). Sorting or filtering the column reveals one row where revenue reads `₹450` as text instead of `450`. The fix: correct the source cell and reload, or use a calculated field to strip non-numeric characters (a preview of what's coming — full data cleaning already happened in Excel and SQL, but source files can still break upstream).

💬 **Expect pushback**: "Why didn't SQL have this problem?" Welcome it. Say: "Good catch — your SQL tables were already cleaned. Tableau usually connects to *live, fresh* exports, which means messiness can sneak back in. This is why 'scan before you build' becomes a permanent habit."

---

## BREAK (10 min)

---

## Concept Block 3: Your First Bar Chart (13 min)

> "A bar chart is a lineup of tiffin boxes on a shelf. One glance and you know which one's tallest — no measuring tape."

Live build: drag `City` to Columns, `Revenue` to Rows. Bars appear instantly, Bengaluru tallest.

> "Notice something — I didn't type SUM anywhere. Tableau assumed it. That's convenient, and it's also a trap."

### 🔴 The trap / highest-value moment
Right-click the Revenue pill, show the aggregation options, and demonstrate switching from SUM to AVG live — the bar heights visibly change and the ranking of cities can even flip.

> "Write this down: **Tableau's default aggregation is always SUM. If your question is about an average, you must change it yourself, or you'll answer a question nobody asked.**"

## Practical Block 3: Build and Break a Bar Chart (12 min)

Students build their own bar chart: Revenue by Category (not City this time). Then, deliberately, ask them to switch the aggregation to AVG and note whether the ranking of categories changes.

**Answer key with reasoning:** Categories with fewer but higher-value orders (e.g., a "Household Essentials" category with occasional bulk orders) may rank low on SUM but high on AVG. The exercise is designed to produce exactly this kind of flip, proving the trap is real, not theoretical.

💬 **Expect an argument about "which one is more correct."** Welcome it. Say: "Neither is more correct — they answer different questions. SUM tells you which category brings in the most total money. AVG tells you which category's *typical order* is biggest. A dashboard often needs both, side by side."

---

## Concept Block 4: Your First Line Chart (12 min)

> "A line chart is a heartbeat monitor. It exists to show movement over time — nothing else."

Live build: drag `Order Date` to Columns (Tableau auto-detects continuous date), `Revenue` to Rows. A daily revenue line appears across August, with visible weekend spikes.

> "Look at that shape. No SQL query gives you 'shape' — you'd have to eyeball forty rows of numbers to notice the weekend pattern. Here it's obvious in one second."

### 🔴 The trap / highest-value moment
Build a line chart using `Delivery Partner` (a category, not a sequence) on Columns instead of a date, producing a meaningless zig-zag line connecting unrelated categories.

> "This line implies a trend from Partner A to Partner B to Partner C. There is no trend — they're just names in a list. Rule: **lines are for time or any naturally ordered sequence. Categories get bars, not lines.**"

## Practical Block 4: Bar or Line? (10 min)

Give students five quick scenarios and ask them to say, in one word, "bar" or "line," with a one-line reason:
1. Revenue by City
2. Revenue by Week, June–August
3. Orders by Delivery Partner
4. Daily Order Count, last 30 days
5. Average Order Value by Customer Segment

**Answer key with reasoning:** 1-Bar (category comparison), 2-Line (time sequence), 3-Bar (category comparison), 4-Line (time sequence), 5-Bar (category comparison). The pattern: if the x-axis is time, it's a line; if it's a label, it's a bar.

💬 **Expect a question about mixing both on one dashboard.** Welcome it. Say: "Absolutely — real dashboards almost always have both side by side. That's exactly what we build in a few sessions from now."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Tableau interface | Blue pill groups, green pill calculates |
| Loading data | Scan the Data pane after loading — every number should be green |
| Bar charts | Great for comparing categories; check your aggregation (SUM vs AVG) |
| Line charts | Only use them for time or ordered sequences, never plain categories |

Close on the thesis: "A chart isn't decoration on top of your data — it's a different, faster way of reading the same truth. Today you built that for the first time with your own hands."

**Bridge to Session 18:** "Tomorrow we step back from Tableau for one session into statistics — Probability and Uncertainty. Because the very next thing an ops manager will ask after seeing your chart is: 'Okay, but how *likely* is this customer to actually buy?' You need probability to answer that honestly."

---

## Q&A & Doubt Solving (5 min)

**Q: Can Tableau connect directly to a SQL database instead of a CSV file?**
→ Yes — Tableau can connect live to MySQL and most databases. We're using files today just to keep the first session focused on charts, not connections.

**Q: What happens if my dataset has a million rows — will Tableau slow down?**
→ It can, which is why later sessions introduce extracts (a saved, optimized snapshot of your data) instead of always querying live.

**Q: Why did my bar chart show one giant bar instead of separate bars per city?**
→ Almost always a blue/green pill mix-up — check whether City actually landed on Columns as a Dimension, not accidentally converted to a Measure.

**Q: Is there a "best" chart type I should default to when unsure?**
→ Not really — but next session (Choosing the Right Chart) is built entirely around answering exactly this question with a decision framework.

**Q: Can I change a bar chart into a line chart without rebuilding it?**
→ Yes, the Marks card dropdown lets you switch chart type on the same fields — try it, but remember: switching type doesn't fix a wrong field choice underneath.

---

## Instructor Notes
- **Words not yet earned:** "calculated field," "extract," "LOD expression," "blended data source" — none of these belong in session 17. Stick to interface, loading, bar, line.
- **Biggest risk in this session:** Overconfidence bleeding over from SQL — students may think "I already know data, this is just drag-and-drop," and rush past the blue/green pill distinction. Counter this explicitly by making the broken-chart demo memorable, not just mentioned.
- **Board management:** Keep "Blue pill groups, green pill calculates" and "Lines are for time, bars are for categories" visible on the board for the entire session.
- **Common confusions:**
  1. Assuming Tableau's default SUM is always what they want.
  2. Forgetting Tableau treats "dirty" numeric text as a category.
  3. Using a line chart on non-time categories out of habit from Excel line charts.
- **Cross-references:** The bar/line distinction here is the seed for the full chart-selection framework in Session 19, and both chart types return, combined, inside the first dashboard in Session 20.
- **Local/cultural context notes:** The thali-plate and tiffin-box analogies land well with this cohort; Kirana365 as a relatable Bengaluru/Hyderabad/Chennai/Pune grocery delivery brand keeps every number grounded in ₹ and familiar cities rather than abstract "Company X" data.
