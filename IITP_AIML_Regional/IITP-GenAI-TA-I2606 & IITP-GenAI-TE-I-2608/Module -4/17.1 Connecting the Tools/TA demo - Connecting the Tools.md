# TA Live Demo Script — Connecting the Tools
> Session 37 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A notebook with the cleaned orders units by city from the SQL export (Pune 5, Bengaluru 9, Chennai 6, total 20) and the marketing spreadsheet's ad spend in ₹ lakh (Pune 2, Bengaluru 3, Chennai 4), both loaded as DataFrames. A whiteboard.

---

```
STEP 1 — Draw the relay (≈1 min)
  Action: Draw: SQL export -> CSV -> Python -> Tableau and GenAI summary. Label the files between the boxes as the baton.
  Say out loud: "Each tool is a runner. The baton is the file. The mistakes happen in the gaps between tools, not inside them."
```

```
STEP 2 — Merge the two sources (≈2 min)
  Action: Run combined = units.merge(ad, on="city") then combined["units_per_lakh"] = combined["units"] / combined["ad_spend"].
  Result: Bengaluru 3.0, Pune 2.5, Chennai 1.5 units per lakh
  Say out loud: "The merge works because the city names match exactly, like a SQL join or a spreadsheet lookup."
```

```
STEP 3 — Break the key on purpose (≈2 min)
  Action: Change order 203's city to "pune " with a trailing space, rebuild the units table and merge again. Print len(combined) and combined["units"].sum().
  Result: Still 3 rows, but Pune shows 3 units and the total is 18 instead of 20
  Say out loud: "No error and no missing row. Just a wrong answer. That is the silent failure."
```

```
STEP 4 — Add the hand-off checks (≈2 min)
  Action: Show the two checks side by side: len(combined) passes at 3, but combined["units"].sum() against the source total of 20 fails. Fix with .str.strip().str.title() and rerun.
  Result: Total back to 20
  Say out loud: "Two checks beat one. The row count missed it and the total caught it. Check at every hand-off."
```

---

> **TA TALKING POINT:** "Clean the key, then check row counts and totals at every hand-off. The mistakes live in the gaps between tools."
