# TA Live Demo Script — Cleaning Data with Pandas
> Session 35 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A notebook with a messy file kirana_orders_messy.csv of seven rows: 201 Pune Staples 3 450; 202 Bengaluru Snacks 5 120; 202 repeated exactly; 203 "pune " Snacks 2 120 (lowercase with a trailing space); 204 Chennai Staples with units blank; 205 Bengaluru Staples 4 450; 206 Chennai Snacks 6 120. Keep an untouched copy of the raw file.

---

```
STEP 1 — Diagnose before fixing (≈2 min)
  Action: Load the file and run df.shape, df.isna().sum(), df.duplicated().sum() and df["city"].unique().
  Result: 7 rows; 1 missing units; 1 duplicate; the cities include 'pune ' with a space
  Say out loud: "A mechanic diagnoses before touching anything. Four problems, found with four commands."
```

```
STEP 2 — Fix the duplicate and the text (≈2 min)
  Action: Run df = df.drop_duplicates(), then df.groupby("city")["units"].sum() to show Pune 3 and 'pune ' 2 split apart. Then run df["city"] = df["city"].str.strip().str.title() and group again.
  Result: 6 rows; Pune becomes a single group with 5 units
  Say out loud: "Before the fix, Pune looked smaller than it is, and no error told us. Cleaning changed the answer."
```

```
STEP 3 — Handle the missing value on purpose (≈2 min)
  Action: Run df = df.dropna(subset=["units"]) then df["units"] = df["units"].astype(int). Ask the room: why not fill the blank with the average?
  Result: 5 rows left, units now whole numbers
  Say out loud: "We have no basis for a number, and a made-up number is invented sales. Drop it, and say so."
```

```
STEP 4 — Say what you changed (≈1 min)
  Action: Say the cleaning note aloud and show units by city. Save with df.to_csv("kirana_orders_clean.csv", index=False).
  Result: Pune 5, Bengaluru 9, Chennai 6
  Say out loud: "Removed 1 duplicate, dropped 1 order with no units, fixed 1 city spelling. Seven rows became five. That sentence is what makes the result trustworthy."
```

---

> **TA TALKING POINT:** "Diagnose first, fix on purpose, and write down what you changed. Dirty data gives confident, wrong answers."
