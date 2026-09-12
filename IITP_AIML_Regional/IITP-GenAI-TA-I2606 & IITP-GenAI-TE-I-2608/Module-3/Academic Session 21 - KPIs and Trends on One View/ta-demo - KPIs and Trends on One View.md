# TA Live Demo Script — KPIs and Trends on One View
> Session 21 | Runtime: ~9 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** The Session 20 Kirana365 dashboard (Daily Revenue Trend, Revenue by City, Revenue by Category) already open, plus the underlying data with a `Last Month Revenue` reference field available.

---

```
STEP 1 — Build a bare KPI tile (≈2 min)
  Action: New worksheet → drag `Revenue` to Text on the Marks card
  Action: Format the text to a large font size, remove all gridlines
  and axis labels
  Result: one large number, "₹12,40,000", nothing else on the sheet
  Say out loud: "That's it. No chart. No axis. This should be
  readable from the back of the room."
```

```
STEP 2 — Add a labelled trend (≈2 min)
  Action: Create a calculated field:
  ([This Month Revenue] - [Last Month Revenue]) / [Last Month Revenue]
  Action: Add it below the KPI number as "▲ 8% vs last month"
  Say out loud: "Watch — I didn't just write '+8%'. I wrote what
  it's compared against. That label is not optional."
```

```
STEP 3 — Build the segment comparison table (≈2 min)
  Action: New worksheet → drag `City` to Rows, `Revenue` to Text,
  and the trend calculated field to Text as a second column
  Result: a small table — City, Revenue, vs Last Month — with
  Chennai showing a red down arrow while others show green up arrows
  Say out loud: "The company number said +8% and everything's fine.
  This table says Chennai is actually down 3%. Same data, honest
  picture only when you break it down."
```

```
STEP 4 — Wire it into the dashboard with an action (≈2 min)
  Action: Drag the KPI tile and segment table onto the Session 20
  dashboard, above the existing three charts
  Action: Dashboard → Actions → Add Filter Action: source = segment
  table, target = Revenue by Category, run on Select
  Result: clicking "Chennai" in the segment table filters the
  category chart to Chennai only
  Say out loud: "One click, and we go from 'the company is fine' to
  'Chennai's Groceries category specifically is the problem.' That's
  live analysis, not a static report."
```

```
STEP 5 — Compare Bengaluru vs Chennai live (≈1 min)
  Action: Click Bengaluru, observe its category mix, then click
  Chennai, observe its category mix
  Say out loud: "Bengaluru's growth is broad across categories.
  Chennai's decline is concentrated in one category. You'd never
  see that difference from the single company-wide KPI alone."
```

---

> **TA TALKING POINT:** "Any time a KPI feels reassuring, break it into segments before you believe it — the honest number is almost always hiding one level down, exactly like Chennai was hiding inside today's +8%."
