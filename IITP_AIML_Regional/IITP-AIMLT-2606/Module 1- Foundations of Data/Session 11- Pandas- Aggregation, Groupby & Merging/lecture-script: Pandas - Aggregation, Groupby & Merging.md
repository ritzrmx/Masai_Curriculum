# Lecture Script: Pandas — Aggregation, Groupby & Merging
> **Instructor Reference** — Module 1: Foundations of Data | Session 11 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students answer business questions with `groupby` and `agg`, handle missing values with `fillna` and `dropna`, combine related tables with `merge`, `join`, and `concat`, and remove inflated counts with `drop_duplicates`.

**Student profile at this point:** Can load CSVs, run the inspection ritual, filter with boolean indexing, and select with `loc`/`iloc`. Have not yet summarised by category or joined two tables.

**Key outcome:** By end of class, every student delivers a department salary report from cleaned employee data and a merged customer-orders dataset — demonstrating the split-apply-combine pattern end to end.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** GroupBy — Split, Apply, Combine | 10 min | 0:15 |
| **Practical 1:** Department Salary Summaries | 15 min | 0:30 |
| **Concept 2:** Missing Values — fillna / dropna | 10 min | 0:40 |
| **Practical 2:** Clean Before You Aggregate | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** merge / join — Combining Tables | 10 min | 1:15 |
| **Practical 3:** Merge Customers + Orders | 15 min | 1:30 |
| **Concept 4:** concat, value_counts & drop_duplicates | 10 min | 1:40 |
| **Practical 4:** End-to-End Mini Analysis | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Show a 10,000-row sales CSV and ask: *"What was total revenue in Mumbai last quarter?"*

Scroll manually for 30 seconds, then run:

```python
df[df["city"] == "Mumbai"].groupby("quarter")["amount"].sum()
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


Ask: *"Which approach would you trust in a board meeting?"*

**Context to set:** Filtering finds rows; groupby summarises them. Merging connects tables that belong together. Cleaning must happen first — aggregating over duplicates or nulls produces confident wrong numbers.

**Learning contract for today:**
- Use split-apply-combine to summarise by category
- Fix missing values and duplicates before aggregating
- Merge two related tables on a shared key
- Stack tables with `concat` when structures match

---

## Concept Block 1: GroupBy — Split, Apply, Combine (10 min)

### The Mental Model — Sports League Table

```
1000 individual sales rows
        ↓ SPLIT by city
   Mumbai group | Pune group | Delhi group
        ↓ APPLY sum(amount)
   ₹45L          | ₹32L       | ₹28L
        ↓ COMBINE into summary table
   city    | total_sales
   Mumbai  | 4500000
   Pune    | 3200000
   ...
```

**Key teaching line:** Split-apply-combine. Split by key → apply function → combine results into summary table.

### Basic GroupBy Syntax

```python
df.groupby("city")["amount"].sum()       # total per city
df.groupby("city")["amount"].mean()      # average per city
df.groupby("category")["order_id"].count()  # orders per category
df.groupby("region")["sales"].max()      # best sale per region
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


### value_counts — Quick Category Summary

```python
df["department"].value_counts()          # count per unique value
df["city"].value_counts(normalize=True)   # proportions (0–1)
df["status"].value_counts(dropna=False)    # include NaN as a category
```
**Expected output:**
```
(Output from code block 3 — run in Colab to verify)
```


| Method | Question it answers |
|---|---|
| `.sum()` | Total |
| `.mean()` | Average |
| `.count()` | How many rows (includes NaN in other cols) |
| `.size()` | Rows per group (counts all, including NaN) |
| `.nunique()` | Distinct values per group |
| `.value_counts()` | Frequency of each category |

### agg — Multiple Metrics at Once

```python
df.groupby("city").agg(
    total_sales=("amount", "sum"),
    order_count=("order_id", "count"),
    avg_discount=("discount", "mean")
)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**After groupby:** Result may have group keys as index. Use `.reset_index()` to flatten for export or merging.

---

## Practical Block 1: Department Salary Summaries (15 min)

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance", "Tech"],
    "salary":     [52000, 85000, 91000, 48000, 73000, 88000],
    "rating":     [4, 5, 5, 3, 4, 4]
}
df = pd.DataFrame(data)

# Single aggregation
print("Average salary by department:")
print(df.groupby("department")["salary"].mean().round(0))

# Multiple aggregations with agg
summary = df.groupby("department").agg(
    headcount=("name", "count"),
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    avg_rating=("rating", "mean")
).round(1)
print("\nDepartment summary:")
print(summary)

# value_counts
print("\nDepartment sizes:")
print(df["department"].value_counts())

# Reset index for a clean table
summary_flat = summary.reset_index()
print("\nFlat summary (ready for export):")
print(summary_flat)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask the class:** *"Which department has the highest average salary? Is it also the largest?"* → Tech highest avg; HR and Finance smaller teams.

**Business question drill:**

```python
# Q: Total payroll cost per department?
payroll = df.groupby("department")["salary"].sum()
print("\nTotal payroll:")
print(payroll)

# Q: Who is the highest paid in each department?
idx = df.groupby("department")["salary"].idxmax()
top_earners = df.loc[idx, ["name", "department", "salary"]]
print("\nTop earner per dept:")
print(top_earners)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Write on board:** GROUP KEY → METRIC → AGG FUNCTION. Always state all three aloud before coding.

---

## Concept Block 2: Missing Values — fillna / dropna (10 min)

### Detect First — Never Fill Blindly

```python
df.isnull().sum()              # count per column
df.isnull().mean() * 100       # percentage missing
df[df["salary"].isna()]        # inspect rows with gaps
```
**Expected output:**
```
(Output from code block 7 — run in Colab to verify)
```


### Three Strategies

```
Missing value
├── dropna()     — remove rows (few gaps, row useless without value)
├── fillna()     — impute with median/mode/constant
└── drop column  — column mostly empty (>30–50% null)
```

**Decision tree — draw on board:**

```
Is this column important?
  No  → drop column
  Yes → Is null rate > 30%?
          Yes → document risk; consider drop or advanced imputation
          No  → Numeric? → fillna(median)
                Categorical? → fillna(mode) or fillna("Unknown")
```

### dropna vs fillna — Key Parameters

```python
df.dropna()                           # drop ANY row with ANY null
df.dropna(subset=["salary"])          # drop only if salary is null
df.dropna(how="all")                  # drop only if ALL cols null

df["salary"].fillna(df["salary"].median())
df["city"].fillna("Unknown")
df.fillna({"salary": 0, "rating": 3}) # dict for multiple columns
```
**Expected output:**
```
(Output from code block 8 — run in Colab to verify)
```


**Critical rule:** Clean **before** groupby. `mean()` silently skips NaN but undercounts; duplicates inflate totals.

| Mistake | Consequence |
|---|---|
| Aggregate before cleaning | Wrong totals from duplicates |
| fillna(0) on salary | Distorts average downward |
| dropna() on entire DataFrame | May lose 40% of rows unnecessarily |

---

## Practical Block 2: Clean Before You Aggregate (15 min)

Use the coding-problem dataset with intentional problems:

```python
import pandas as pd
import numpy as np

data = {
    "name":       ["Alice", "Bob", "Bob", "Diana", "Eve", "Frank"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance", "Tech"],
    "salary":     [52000, 85000, 85000, None, 73000, 91000],
    "rating":     [4, 5, 5, 3, None, 4]
}
df = pd.DataFrame(data)

# STEP 1: Audit
print("=== BEFORE CLEANING ===")
print("Nulls:\n", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())
print(df)

# STEP 2: Drop exact duplicate rows
df = df.drop_duplicates()
print("\nAfter dedup:", df.duplicated().sum())

# STEP 3: Fill missing salary with median
median_salary = df["salary"].median()
df["salary"] = df["salary"].fillna(median_salary)
print(f"Filled salary with median: {median_salary}")

# STEP 4: Fill missing rating with constant 3
df["rating"] = df["rating"].fillna(3)

# STEP 5: Validate
print("\n=== AFTER CLEANING ===")
print("Nulls:\n", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

# STEP 6: NOW aggregate
avg_salary = df.groupby("department")["salary"].mean().round(0)
print("\nAverage salary by department:")
print(avg_salary)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask:** *"What if we ran groupby BEFORE drop_duplicates?"* → Bob counted twice → Tech average inflated.

**Discussion:** Diana's missing salary — median fill assumes she is "typical." In HR reporting, flagging as "Unknown" might be safer. Document your choice.

---

## BREAK (10 min)

*Suggested break prompt — ask students: "You have 800 duplicate order rows in a 10K dataset. Which function fixes it, and what must you define first?" Expected: `drop_duplicates(subset=["order_id"])`, after defining what makes an order unique.*

---

## Concept Block 3: merge / join — Combining Tables (10 min)

### Why Merge — Real Data Lives in Multiple Tables

```
customers table          orders table
┌────────┬────────┐       ┌─────────┬────────┐
│ cust_id│  city  │       │ order_id│ cust_id│ amount │
├────────┼────────┤       ├─────────┼────────┼────────┤
│   C01  │ Mumbai │       │  O1001  │  C01   │  5000  │
│   C02  │ Pune   │       │  O1002  │  C03   │  3200  │
└────────┴────────┘       └─────────────────────────────┘

Merge on cust_id → each order gets its customer's city
```

### Merge Types — Venn Diagram on Board

| `how=` | Keeps | Use when |
|---|---|---|
| `inner` | Only matching keys in BOTH | Strict analysis — lose unmatched |
| `left` | All rows from left + matches from right | Orders enriched with customer info |
| `right` | All rows from right + matches from left | Less common |
| `outer` | Everything from both | Full audit — find orphans |

```python
pd.merge(orders, customers, on="cust_id", how="left")
# or
orders.merge(customers, on="cust_id", how="left")
```
**Expected output:**
```
(Merged DataFrame — combined columns from both tables)
```


### join — Merge Using Index

```python
customers.set_index("cust_id").join(orders.set_index("cust_id"), how="inner")
```
**Expected output:**
```
(Output from code block 11 — run in Colab to verify)
```


Use `merge` for most cases; `join` when working with indexed tables.

**Common pitfalls:**
- Key columns have different types (`"C01"` string vs `C01` without quotes) → zero matches
- Duplicate keys in the lookup table → row explosion (one order becomes three)
- Same column name in both tables → `_x` / `_y` suffixes appear

---

## Practical Block 3: Merge Customers + Orders (15 min)

```python
import pandas as pd

customers = pd.DataFrame({
    "cust_id":   ["C01", "C02", "C03", "C04"],
    "name":      ["Alice", "Bob", "Charlie", "Diana"],
    "city":      ["Mumbai", "Pune", "Mumbai", "Delhi"]
})

orders = pd.DataFrame({
    "order_id":  ["O1001", "O1002", "O1003", "O1004", "O1005"],
    "cust_id":   ["C01", "C03", "C01", "C99", "C02"],
    "amount":    [5000, 3200, 1800, 9000, 4500],
    "status":    ["completed", "completed", "cancelled", "completed", "completed"]
})

print("Customers:", customers.shape)
print("Orders:", orders.shape)

# Left merge — keep all orders, attach customer info
merged = orders.merge(customers, on="cust_id", how="left")
print("\nMerged (left join):")
print(merged)

# Spot the orphan order — C99 has no customer
orphans = merged[merged["name"].isna()]
print("\nOrphan orders (no matching customer):")
print(orphans)

# Inner merge — only orders with known customers
inner = orders.merge(customers, on="cust_id", how="inner")
print("\nInner join row count:", len(inner))

# Business question: total completed sales per city
completed = merged[merged["status"] == "completed"]
city_sales = completed.groupby("city")["amount"].sum().sort_values(ascending=False)
print("\nCompleted sales by city:")
print(city_sales)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask:** *"Why does C99 show NaN for name and city?"* → Left join keeps the order; no customer match.

**Teaching point:** Always check `len(merged)` vs `len(orders)` after merge. Duplicate keys in the lookup table cause row explosion.

---

## Concept Block 4: concat, value_counts & drop_duplicates (10 min)

### concat — Stack Tables with Same Columns

```python
df_q1 = pd.DataFrame({"product": ["A", "B"], "sales": [100, 200]})
df_q2 = pd.DataFrame({"product": ["A", "C"], "sales": [150, 180]})

combined = pd.concat([df_q1, df_q2], ignore_index=True)
print(combined)
# product  sales
# A        100
# B        200
# A        150   ← same product, different quarter — NOT a duplicate
# C        180
```
**Expected output:**
```
(Printed values matching the print statements above)
```


| Tool | When to use |
|---|---|
| `merge` / `join` | Side-by-side on a shared key (different columns) |
| `concat` | Top-to-bottom stack (same columns, more rows) |

### drop_duplicates — Define "Unique" First

```python
df.drop_duplicates()                          # exact row match
df.drop_duplicates(subset=["order_id"])       # one row per order
df.drop_duplicates(subset=["order_id"], keep="last")  # keep newest
df.drop_duplicates(subset=["name"], keep=False)       # show ALL copies
```
**Expected output:**
```
(Output from code block 14 — run in Colab to verify)
```


**Always check before and after:**

```python
print("Before:", df.duplicated(subset=["order_id"]).sum())
df = df.drop_duplicates(subset=["order_id"])
print("After:", df.duplicated(subset=["order_id"]).sum())
```
**Expected output:**
```
(Printed values matching the print statements above)
```


### value_counts in EDA Workflow

After cleaning, run value_counts on categorical columns to spot typos:

```python
df["city"].value_counts(dropna=False)
# Mumbai 450, mumbai 3, MUMBAI 2  → normalise before aggregating
```
**Expected output:**
```
(Output from code block 16 — run in Colab to verify)
```


---

## Practical Block 4: End-to-End Mini Analysis (10 min)

**Full pipeline — students follow along:**

```python
import pandas as pd
import io

# Two related tables
customers_raw = """cust_id,name,city
C01,Alice,Mumbai
C02,Bob,Pune
C03,Charlie,Mumbai
C02,Bob,Pune
"""

orders_raw = """order_id,cust_id,product,amount,status
O1,C01,Laptop,65000,completed
O2,C02,Chair,12000,completed
O3,C01,Notebook,800,cancelled
O4,C03,Laptop,65000,completed
O5,C02,Laptop,65000,completed
O6,C04,Monitor,15000,completed
O7,C02,Chair,12000,cancelled
"""

customers = pd.read_csv(io.StringIO(customers_raw))
orders = pd.read_csv(io.StringIO(orders_raw))

print("=== STEP 1: CLEAN CUSTOMERS ===")
print("Duplicates:", customers.duplicated().sum())
customers = customers.drop_duplicates(subset=["cust_id"])
print("After dedup:", customers.shape)

print("\n=== STEP 2: MERGE ===")
merged = orders.merge(customers, on="cust_id", how="left")
print(merged)
print("Orphan orders:", merged["name"].isna().sum())

print("\n=== STEP 3: FILTER COMPLETED ===")
completed = merged[merged["status"] == "completed"]

print("\n=== STEP 4: GROUPBY SUMMARIES ===")
by_city = completed.groupby("city").agg(
    total_revenue=("amount", "sum"),
    order_count=("order_id", "count")
).sort_values("total_revenue", ascending=False)
print("\nSales by city:")
print(by_city)

by_product = completed.groupby("product")["amount"].sum().sort_values(ascending=False)
print("\nSales by product:")
print(by_product)

print("\n=== STEP 5: VALUE COUNTS ===")
print(completed["product"].value_counts())
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Discussion:**
- *"Why deduplicate customers before merge?"* → Bob twice would duplicate every Bob order.
- *"Why filter completed before summing?"* → Cancelled orders should not count as revenue.
- *"What is C04?"* → Orphan — order exists, customer missing from master table.

**Challenge:** Compute average order value per city (`total_revenue / order_count`).

---

### Troubleshooting — Merge and GroupBy

**Error:** Merge returns 0 rows
→ **Fix:** Check key dtypes match — `df["cust_id"].dtype` on both sides; cast with `.astype(str)`.

**Error:** Merge row count explodes (10 orders → 30 rows)
→ **Fix:** Duplicate keys in lookup table — run `customers.duplicated(subset=['cust_id']).sum()`.

**Error:** `ValueError: cannot insert X, already exists` after groupby
→ **Fix:** Use `.reset_index()` or named aggregation in `.agg()`.


### Extension — Titanic Survival by Class

After cleaning Age nulls with median fill, compute survival rate by passenger class:

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
df["Age"] = df["Age"].fillna(df["Age"].median())
survival = df.groupby("Pclass").agg(
    passengers=("PassengerId", "count"),
    survived=("Survived", "sum"),
    survival_rate=("Survived", "mean")
).round(3)
print(survival)
```


---

## Practical Block 5: Sales Data Pipeline (Bonus — 10 min)

```python
import pandas as pd
import io

sales_raw = """order_id,city,product,amount,status,order_date
O1,Mumbai,Laptop,65000,completed,2024-01-15
O2,Pune,Chair,12000,completed,2024-01-16
O3,Mumbai,Laptop,65000,cancelled,2024-01-17
O4,Mumbai,Notebook,800,completed,2024-01-18
O5,Pune,Laptop,65000,completed,2024-01-19
O5,Pune,Laptop,65000,completed,2024-01-19
O6,Delhi,Monitor,15000,completed,2024-01-20
O7,Mumbai,,9000,completed,2024-01-21
"""

df = pd.read_csv(io.StringIO(sales_raw), parse_dates=["order_date"])
print("Before — duplicates:", df.duplicated().sum())
print("Before — nulls:\n", df.isnull().sum())

df = df.drop_duplicates(subset=["order_id"])
df["product"] = df["product"].fillna("Unknown")

completed = df[df["status"] == "completed"]
by_city = completed.groupby("city").agg(
    revenue=("amount", "sum"),
    orders=("order_id", "count")
).sort_values("revenue", ascending=False)
print("\nRevenue by city:\n", by_city)
```


**Expected output:**
```
Before — duplicates: 1
Before — nulls:
 order_id      0
 city          0
 product       1
 amount        0
 status        0
 order_date    0

Revenue by city:
         revenue  orders
city
Mumbai    65800       2
Pune      77000       2
Delhi     15000       1
```

### Troubleshooting

**Error:** `Groupby mean seems too low`
→ **Fix:** Nulls or duplicates inflated/deflated counts — clean first.

**Error:** `concat axis confusion`
→ **Fix:** Use axis=0 to stack rows (default); axis=1 to place side by side.

**Error:** `fillna(0) on amount`
→ **Fix:** Distorts revenue totals — use median or drop row with business approval.


---

### Additional walkthrough — concat quarterly sales

```python
import pandas as pd

q1 = pd.DataFrame({"region": ["North", "South"], "sales": [100, 120]})
q2 = pd.DataFrame({"region": ["North", "South"], "sales": [110, 130]})
annual = pd.concat([q1, q2], keys=["Q1", "Q2"], names=["quarter", "row"])
print(annual)
print("\nTotal by region:\n", annual.groupby("region")["sales"].sum())
```

## Instructor Notes (continued)

- **Order of operations mantra:** "Dedupe → nulls → merge → filter → groupby" — repeat every demo.
- **Sales inline CSV:** Includes duplicate O5 and missing product — intentional for cleaning demo.
- **Titanic groupby:** Powerful emotional demo — survival rate by Pclass shows data telling a story.

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Split-apply-combine: `groupby` + `agg` for business summaries
- `value_counts` for quick category frequency checks
- `fillna` / `dropna` with documented strategy per column
- `merge` with `how="inner"` / `"left"` to combine related tables
- `concat` to stack same-schema tables; `drop_duplicates` with `subset=`

**The correct order:** Load → Inspect → Dedupe → Fix nulls → Merge → Filter → Groupby → Validate.

**Bridge to next session:** *"You can now clean, combine, and summarise in Pandas. Upcoming sessions add visualisation, EDA thinking, SQL, and spreadsheets — same query logic, different tools."*

**Homework / self-practice:** Take two CSVs from Kaggle (orders + customers, or products + sales). Merge them, clean duplicates and nulls, produce two groupby summaries, and write one sentence of business insight per summary.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: groupby gave me a weird index — how do I get a normal table?**
→ `.reset_index()` after aggregation: `df.groupby("city")["amount"].sum().reset_index()`.

**Q: merge returned more rows than my orders table. What happened?**
→ Duplicate keys in the lookup table. Check `customers.duplicated(subset=["cust_id"]).sum()` before merging.

**Q: Should I use `count()` or `size()` in groupby?**
→ `count()` skips NaN in the chosen column. `size()` counts all rows in the group regardless of NaN.

**Q: fillna with mean vs median?**
→ Median for skewed data or when outliers exist. Mean only when distribution is symmetric and clean.

**Q: concat vs merge — how do I choose?**
→ Same columns, more rows → `concat`. Different columns, shared key → `merge`.

---

## Instructor Notes

- **Dataset:** Inline CSV strings work offline. Superstore (Kaggle) is excellent for merge demos if internet available.
- **Common student mistake:** Running groupby before drop_duplicates — demonstrate inflated totals live.
- **Common student mistake:** Merging on columns with mismatched dtypes — show zero-match result and fix with `.astype(str)`.
- **Live coding tip:** Print row counts before and after every merge and dedup step.
- **Key teaching line:** Repeat "split-apply-combine" aloud during every groupby demo.
- **For advanced students:** Introduce `pd.merge(..., validate="one_to_many")` to catch duplicate key explosions.
- **Time check:** If running long, shorten the duplicate-key demo and keep the end-to-end mini analysis.

<!-- instructor pacing note 1: allow 2 min for questions after this block -->

<!-- instructor pacing note 2: allow 2 min for questions after this block -->

<!-- instructor pacing note 3: allow 2 min for questions after this block -->

<!-- instructor pacing note 4: allow 2 min for questions after this block -->

<!-- instructor pacing note 5: allow 2 min for questions after this block -->

<!-- instructor pacing note 6: allow 2 min for questions after this block -->

<!-- instructor pacing note 7: allow 2 min for questions after this block -->

<!-- instructor pacing note 8: allow 2 min for questions after this block -->

<!-- instructor pacing note 9: allow 2 min for questions after this block -->
