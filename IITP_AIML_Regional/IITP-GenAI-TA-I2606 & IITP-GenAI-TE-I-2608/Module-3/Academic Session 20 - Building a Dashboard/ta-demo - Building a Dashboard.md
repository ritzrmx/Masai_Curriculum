# TA Live Demo Script — Building a Dashboard
> Session 20 | Runtime: ~8 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** Three Kirana365 sheets already built and saved in the workbook: `Revenue by City` (bar), `Daily Revenue Trend` (line), `Revenue by Category` (bar).

---

```
STEP 1 — Create a new dashboard (≈1 min)
  Action: Click the "New Dashboard" tab at the bottom
  Result: blank canvas with sheet list appearing on the left
  Say out loud: "Notice there's no Rows or Columns shelf here — this
  isn't a place to build new charts, it's a place to assemble
  finished ones."
```

```
STEP 2 — Drag in the three sheets (≈2 min)
  Action: Drag `Daily Revenue Trend` onto the top of the canvas
  Action: Drag `Revenue by City` onto the bottom-left
  Action: Drag `Revenue by Category` onto the bottom-right
  Result: a three-chart dashboard, trend on top, breakdowns below
  Say out loud: "Trend first, because it answers 'how are we doing
  right now.' The two breakdowns underneath explain why."
```

```
STEP 3 — Prove they're live references, not copies (≈2 min)
  Action: Click on the `Revenue by City` chart inside the dashboard,
  go to its underlying sheet tab, and add a quick colour change
  Result: the dashboard version updates automatically
  Say out loud: "See that? I edited the sheet, and the dashboard
  updated on its own. These aren't separate copies — they're the
  exact same chart, viewed in two places."
```

```
STEP 4 — Add a filter action (≈2 min)
  Action: Dashboard menu → Actions → Add Action → Filter
  Action: Source sheet: Revenue by City, Target sheet: Revenue by
  Category, Run action on: Select
  Result: clicking a city bar filters the category chart to that city
  Say out loud: "Watch — I click Bengaluru, and the category chart
  instantly narrows to just Bengaluru's mix. One click now does what
  used to take manual cross-referencing across three separate charts."
```

```
STEP 5 — Test both directions (≈1 min)
  Action: Click Bengaluru, then click it again to deselect
  Result: category chart filters, then resets to all cities
  Say out loud: "Always test the reset, not just the filter — a
  dashboard action that only works one way will frustrate real
  users fast."
```

---

> **TA TALKING POINT:** "A dashboard earns its name the moment its charts start talking to each other — three unconnected charts on one screen is still just a collage; one working filter action, like the one you just watched, is what makes it a dashboard."
