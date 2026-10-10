# TA Live Demo Script — Getting Started with Python Data
> Session 34 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A notebook with pandas installed and a file kirana_orders.csv with six orders: columns order_id, city, category, units, price; rows 201 Pune Staples 3 450; 202 Bengaluru Snacks 5 120; 203 Pune Snacks 2 120; 204 Chennai Staples 1 450; 205 Bengaluru Staples 4 450; 206 Chennai Snacks 6 120.

---

```
STEP 1 — Load it in one line (≈1 min)
  Action: Type import pandas as pd then df = pd.read_csv("kirana_orders.csv") then print(df).
  Result: The six-row table with the header used as column names
  Say out loud: "Last time we needed a page of code to read a CSV. pandas is the mover: one line, and the numbers already arrive as numbers."
```

```
STEP 2 — Look before you analyse (≈2 min)
  Action: Run df.head(3), df.shape and df.info(). Read the non-null counts and the dtypes aloud.
  Result: Shape (6, 5), every column with 6 non-null values
  Say out loud: "Always inspect first. Missing values and wrong types show up here, before they can quietly change an answer."
```

```
STEP 3 — Select columns (≈2 min)
  Action: Run df["units"].sum() and then df[["city", "units"]]. Then deliberately type df["city", "units"] to show the KeyError.
  Result: 21 total units, a two-column table, then a KeyError
  Say out loud: "One column: single brackets. Several columns: a list inside the brackets. Two pairs of brackets."
```

```
STEP 4 — Filter rows (≈2 min)
  Action: Run df[df["city"] == "Pune"], then df[df["units"] >= 4], then df[(df["city"] == "Bengaluru") & (df["category"] == "Staples")].
  Result: Orders 201 and 203; orders 202, 205 and 206; order 205
  Say out loud: "No loop needed: the condition runs over the whole column. Use ampersand with brackets around each condition, not the word and."
```

---

> **TA TALKING POINT:** "Load it, look at it, then ask it questions. Never total or filter a table you have not inspected."
