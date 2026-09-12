# TA Live Demo Script — Choosing the Right Chart
> Session 19 | Runtime: ~8 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** Kirana365 August orders file already loaded in Tableau, with City, Category, Order Date, Quantity, and Revenue available in the Data pane.

---

```
STEP 1 — Start from the wrong chart, on purpose (≈1 min)
  Action: Build a pie chart of Revenue by Category (8 categories)
  Result: several thin, hard-to-distinguish slices
  Say out loud: "Try to tell me, right now, which category is third
  biggest. This is the exact trap from today's opening — let's fix it
  together, live."
```

```
STEP 2 — Convert to a sorted, labelled bar chart (≈2 min)
  Action: Change Marks type from Pie to Bar
  Action: Right-click the Revenue axis → Sort → Descending
  Action: Drag Revenue onto the Label shelf on the Marks card
  Result: clean, sorted bar chart with values labelled
  Say out loud: "Same 8 categories, same numbers. Now the third
  biggest is obvious in one second."
```

```
STEP 3 — Build a stacked bar to add a second layer of insight (≈2 min)
  Action: Drag `City` to Columns, `Revenue` to Rows, `Category` to Color
  Result: stacked bars per city, coloured by category
  Say out loud: "Now we're answering two questions in one chart —
  which city is biggest, AND what's driving that city's number."
```

```
STEP 4 — Build a scatter plot to reveal what bars can't (≈2 min)
  Action: New sheet — drag `Quantity` to Columns, `Revenue` to Rows,
  set Marks type to Circle
  Result: a scatter of individual orders
  Say out loud: "Every dot here is one real order. Watch — a handful
  of dots sit way out to the right. Those are bulk orders quietly
  pulling up the citywide average you saw in the bar chart. No bar
  chart could ever show you this."
```

```
STEP 5 — Apply the three formatting fixes as a checklist (≈1 min)
  Action: On the sorted bar chart, colour only the lowest-performing
  bar red using a calculated highlight, leave the rest in the
  default colour
  Say out loud: "Sort, label the ones that matter, colour with a
  purpose. That's it — three small moves turn a correct chart into a
  fast one."
```

---

> **TA TALKING POINT:** "Before you open Tableau for your own dashboards, write your question in one sentence first — the chart type you just watched me pick each time came straight out of that sentence, never out of habit."
