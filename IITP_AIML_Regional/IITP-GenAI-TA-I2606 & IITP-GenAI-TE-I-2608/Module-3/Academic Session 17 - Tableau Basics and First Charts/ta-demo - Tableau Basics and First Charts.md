# TA Live Demo Script — Tableau Basics and First Charts
> Session 17 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** Kirana365 August orders file already downloaded and Tableau open on the demo machine, but NOT yet connected to any data source — the TA connects live, in front of students, so they see the full sequence end to end.

---

```
STEP 1 — Connect to the data source (≈1 min)
  Action: Click "Connect to a File" → select Kirana365_Orders_Aug2026.csv
  Say out loud: "Watch the preview grid that appears — this is your
  one chance to catch a problem before you build anything."
  Point at: the preview grid, specifically the Revenue column header
  Check: confirm Revenue and Quantity show as numbers, not text
```

```
STEP 2 — Scan the Data pane (≈1 min)
  Action: Click "Sheet 1", look at the Data pane on the left
  Say out loud: "Blue pill, green pill. City, Category, Order Date —
  all blue, all Dimensions. Revenue, Quantity — green, Measures.
  If any number field shows up blue here, stop and fix it before
  you build a single chart."
```

```
STEP 3 — Build the bar chart live (≈2 min)
  Action: Drag `City` to Columns
  Action: Drag `Revenue` to Rows
  Result: four bars appear, Bengaluru tallest
  Say out loud: "Notice I didn't type SUM anywhere — Tableau assumed
  it. Right-click the Revenue pill with me."
  Action: Right-click Revenue pill on Rows → change Measure to Average
  Result: bar heights shift, and point out if the city ranking changes
  Say out loud: "Same fields, different question, different answer.
  Always check which aggregation you're actually looking at."
```

```
STEP 4 — Build the line chart live (≈2 min)
  Action: Open a new sheet, drag `Order Date` to Columns
  Action: Drag `Revenue` to Rows
  Result: a daily revenue line appears across August with visible
  weekend spikes
  Say out loud: "This shape — the weekend spikes — would take you
  ten minutes of eyeballing a spreadsheet to notice. Here it's
  instant."
```

```
STEP 5 — Break it on purpose (≈1 min)
  Action: On a third sheet, drag `Delivery Partner` to Columns instead
  of a date, and `Revenue` to Rows, with a line chart selected
  Result: a meaningless zig-zag line connecting unrelated partner names
  Say out loud: "This line is lying to you — there's no 'before and
  after' between delivery partners. Lines are for time. Bars are for
  categories. Always."
```

---

> **TA TALKING POINT:** "Everything you build for the rest of this module — every dashboard, every KPI tile — starts from exactly these two chart types and exactly this one rule: know your pill colour, and know whether your x-axis is a category or a timeline."
