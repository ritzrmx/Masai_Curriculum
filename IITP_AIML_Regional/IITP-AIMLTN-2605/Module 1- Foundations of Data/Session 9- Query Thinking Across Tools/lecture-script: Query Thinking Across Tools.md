# Lecture Script: Query Thinking Across Tools
> **Instructor Reference** — Module 1: Foundations of Data | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students understand that filtering, grouping, sorting, and joining data is the *same logical operation* regardless of whether the tool is Pandas, SQL, or Excel — so they can translate any query mentally across all three.

**Student profile at this point:** Have completed data cleaning (Session 8). Comfortable with Pandas basics and Python. No formal SQL knowledge required yet (Session 12 goes deeper).

**Key outcome:** Given a business question ("What are the top 5 products by revenue last month?"), students can write it in both Pandas and SQL and see the structural equivalence.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** The Universal Query Model — SELECT, FILTER, GROUP | 10 min | 0:15 |
| **Practical 1:** Pandas → SQL translation side by side | 15 min | 0:30 |
| **Concept 2:** Filtering and Sorting Logic | 10 min | 0:40 |
| **Practical 2:** Multi-condition filters, sorting, ranking | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** GroupBy — the heart of aggregation | 10 min | 1:15 |
| **Practical 3:** GroupBy in Pandas + SQL equivalents | 15 min | 1:30 |
| **Concept 4:** Thinking in Pipelines | 10 min | 1:40 |
| **Practical 4:** End-to-end business question walkthrough | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — write this on the board:**

```
Business question: "Which city had the highest average order value last month, 
                    among orders that were not cancelled?"
```

Ask: *"How many different ways can you think of to answer this? Excel pivot table? Pandas? SQL?"*

**Key message to set:** The *thinking* is identical. You are always doing the same four things:
1. **Select** — which columns do I need?
2. **Filter** — which rows qualify?
3. **Group** — do I need to aggregate by a category?
4. **Order/Limit** — which results do I care about most?

Learning one tool deeply makes every other tool a translation exercise.

---

## Concept Block 1: The Universal Query Model (10 min)

### The Four Operations — Everywhere

| Operation | Pandas | SQL |
|---|---|---|
| Select columns | `df[['col1','col2']]` | `SELECT col1, col2` |
| Filter rows | `df[df['col'] > 100]` | `WHERE col > 100` |
| Sort | `df.sort_values('col', ascending=False)` | `ORDER BY col DESC` |
| Limit | `df.head(5)` | `LIMIT 5` |
| Group + Aggregate | `df.groupby('cat')['val'].sum()` | `GROUP BY cat` + `SUM(val)` |
| Count rows | `len(df)` / `df.shape[0]` | `SELECT COUNT(*)` |

**Draw on the board:** Every query, no matter how complex, is a combination of these 5 operations. "Complex" queries just stack them.

**The execution order mental model:**

```
SQL execution order (not what you write, but how it runs):
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

Pandas equivalent mental order:
Load df → filter rows → groupby → agg → sort → head/tail
```

**Why this matters:** SQL beginners write `WHERE` after `GROUP BY` when they should use `HAVING`. Understanding execution order prevents this category of error.

---

## Practical Block 1: Pandas ↔ SQL Side-by-Side Translation (15 min)

### Dataset — Superstore Sales (use a subset)

```python
import pandas as pd

# Load the Superstore-style dataset
data = {
    'order_id': ['O1','O2','O3','O4','O5','O6','O7','O8'],
    'city': ['Mumbai','Delhi','Mumbai','Bangalore','Delhi','Mumbai','Delhi','Bangalore'],
    'category': ['Tech','Furniture','Tech','Office','Tech','Furniture','Office','Tech'],
    'sales': [25000, 8000, 15000, 3000, 32000, 12000, 5500, 18000],
    'profit': [5000, -500, 3200, 800, 8000, 1200, 600, 4000],
    'status': ['completed','completed','completed','cancelled','completed','completed','cancelled','completed']
}
df = pd.DataFrame(data)
print(df)
```

### Translation Exercise — run both in class

**Q1: Show all completed orders from Mumbai**

```python
# Pandas
result = df[(df['status'] == 'completed') & (df['city'] == 'Mumbai')]
print(result[['order_id','city','sales','profit']])
```

```sql
-- SQL equivalent
SELECT order_id, city, sales, profit
FROM orders
WHERE status = 'completed'
  AND city = 'Mumbai';
```

**Q2: Top 3 orders by sales**

```python
# Pandas
top3 = df.sort_values('sales', ascending=False).head(3)
print(top3[['order_id','city','sales']])
```

```sql
-- SQL equivalent
SELECT order_id, city, sales
FROM orders
ORDER BY sales DESC
LIMIT 3;
```

**Ask students:** *"If I want the BOTTOM 3, what changes in each?"*

---

## Concept Block 2: Filtering and Sorting Logic (10 min)

### Boolean Indexing — the mechanism behind all filters

**Pandas** turns a condition into a series of True/False, then selects only True rows:

```python
df['sales'] > 10000
# Returns: [True, False, True, False, True, True, False, True]
```

Show this intermediate step on screen — many students don't realise the mask exists.

### Multi-Condition Filters — Operator Rules

| Intention | Pandas | SQL | Common mistake |
|---|---|---|---|
| AND (both must be true) | `&` with parentheses | `AND` | Using Python `and` → TypeError |
| OR (either can be true) | `\|` with parentheses | `OR` | Forgetting parentheses: `(A) \| (B)` |
| NOT | `~` | `NOT` | — |
| Value in a list | `.isin([...])` | `IN (...)` | — |
| Value is null | `.isnull()` | `IS NULL` | Using `== None` → doesn't work |

**Demonstrate the common mistake:**
```python
# Wrong — this crashes
# df[df['sales'] > 10000 and df['status'] == 'completed']

# Right
df[(df['sales'] > 10000) & (df['status'] == 'completed')]
```

### Sorting on Multiple Columns

```python
df.sort_values(['city', 'sales'], ascending=[True, False])
# All cities sorted A-Z; within each city, sales sorted highest first
```

---

## Practical Block 2: Multi-Condition Filters, Sorting, Ranking (15 min)

```python
# --- Multi-condition filter ---
# Completed orders with sales > 10000
high_value = df[(df['status'] == 'completed') & (df['sales'] > 10_000)]
print("High-value completed orders:")
print(high_value)

# --- isin filter ---
# Orders from metro cities only
metros = ['Mumbai', 'Delhi']
metro_orders = df[df['city'].isin(metros)]
print("\nMetro orders:")
print(metro_orders)

# --- NOT filter ---
# All orders that are NOT cancelled
active = df[~(df['status'] == 'cancelled')]
# Equivalent: df[df['status'] != 'cancelled']
print("\nActive orders:", len(active))

# --- Multi-column sort ---
sorted_df = df.sort_values(['city', 'sales'], ascending=[True, False])
print("\nSorted by city then sales (desc):")
print(sorted_df[['order_id','city','sales','status']])

# --- Rank within groups ---
df['city_rank'] = df.groupby('city')['sales'].rank(ascending=False, method='dense').astype(int)
print("\nRanked within city:")
print(df[['order_id','city','sales','city_rank']].sort_values(['city','city_rank']))
```

**Discussion question:** *"A cancelled order had sales of ₹32,000. Should we include it when calculating average order value? Why not?"* → Introduce the concept of business logic driving filter decisions.

---

## BREAK (10 min)

*Ask students to write (on paper or a note) one business question they would ask about the Superstore dataset. They will try to write it in Pandas after the break.*

---

## Concept Block 3: GroupBy — The Heart of Aggregation (10 min)

### What GroupBy Actually Does

```
Original table:           After groupby('city').sum():
city    | sales           city      | sales
Mumbai  | 25000           Bangalore | 21000
Delhi   | 8000    ──>     Delhi     | 45500
Mumbai  | 15000           Mumbai    | 52000
...                       
```

**Visual mental model on board:** GroupBy splits the table into buckets (one per city), applies a function to each bucket (sum, mean, count), and combines the results.

### The Split-Apply-Combine Pattern

```
Split:   df.groupby('city')  → 3 sub-DataFrames (Mumbai, Delhi, Bangalore)
Apply:   .sum() / .mean() / .count() / .agg({...})
Combine: results joined back into a new DataFrame
```

### Aggregation Functions Reference

```python
df.groupby('city')['sales'].sum()    # Total per city
df.groupby('city')['sales'].mean()   # Average per city
df.groupby('city')['sales'].count()  # Non-null rows per city
df.groupby('city')['sales'].max()    # Highest sale per city
df.groupby('city')['sales'].std()    # Variability per city

# Multiple aggregations at once
df.groupby('city')['sales'].agg(['sum', 'mean', 'count', 'max'])
```

### SQL Equivalent

```sql
SELECT city,
       SUM(sales) AS total_sales,
       AVG(sales) AS avg_sales,
       COUNT(*) AS order_count
FROM orders
GROUP BY city;
```

**Key teaching point:** In SQL, every column in SELECT must either be in GROUP BY or wrapped in an aggregate function. This rule exists in Pandas too — `groupby` keys stay as index, everything else gets aggregated.

---

## Practical Block 3: GroupBy in Pandas + SQL Equivalents (15 min)

```python
# --- Basic GroupBy ---
city_sales = df.groupby('city')['sales'].sum().reset_index()
city_sales.columns = ['city', 'total_sales']
city_sales = city_sales.sort_values('total_sales', ascending=False)
print("Sales by city:")
print(city_sales)

# --- Multi-column GroupBy ---
cat_city = df.groupby(['city', 'category'])['sales'].sum().reset_index()
print("\nSales by city and category:")
print(cat_city)

# --- Multi-metric aggregation ---
summary = df.groupby('city').agg(
    total_sales=('sales', 'sum'),
    avg_profit=('profit', 'mean'),
    order_count=('order_id', 'count')
).reset_index()
print("\nCity summary:")
print(summary)

# --- HAVING equivalent: filter AFTER groupby ---
# Cities with more than 2 orders
city_counts = df.groupby('city')['order_id'].count().reset_index()
city_counts.columns = ['city', 'order_count']
big_cities = city_counts[city_counts['order_count'] > 2]
print("\nCities with > 2 orders:")
print(big_cities)
```

**SQL equivalents to show alongside (in comments or on board):**

```sql
-- HAVING example
SELECT city, COUNT(*) AS order_count
FROM orders
GROUP BY city
HAVING COUNT(*) > 2;
```

---

## Concept Block 4: Thinking in Pipelines (10 min)

### Method Chaining — Writing Queries as Pipelines

Instead of creating intermediate variables for every step, chain operations:

```python
# Without chaining (imperative)
filtered = df[df['status'] == 'completed']
grouped = filtered.groupby('city')['sales'].sum()
sorted_result = grouped.sort_values(ascending=False)
top = sorted_result.head(3)

# With chaining (pipeline — reads like a sentence)
top = (
    df[df['status'] == 'completed']
    .groupby('city')['sales']
    .sum()
    .sort_values(ascending=False)
    .head(3)
)
```

**Rule:** Each method returns a DataFrame or Series. You can immediately call the next method on it.

**Reading chained code:** Read top-to-bottom: "Take df, filter to completed, group by city, sum sales, sort descending, take top 3."

### When to Break the Chain

- When you need to inspect an intermediate result for debugging
- When the same intermediate result is used multiple times
- When a step produces a fundamentally different object (e.g., after `groupby` you have a GroupBy object, not a DataFrame)

---

## Practical Block 4: End-to-End Business Question (10 min)

**Business question (write on board):**
> "For completed orders, which category has the highest average profit per order in each city? Show top result per city."

Walk through the solution together, letting students guide the steps:

```python
# Load a richer dataset for this question
import pandas as pd

# Using our existing df
result = (
    df[df['status'] == 'completed']                      # Filter: only completed
    .groupby(['city', 'category'])                        # Group by city + category
    .agg(
        avg_profit=('profit', 'mean'),
        order_count=('order_id', 'count')
    )
    .reset_index()
    .sort_values('avg_profit', ascending=False)          # Sort: best profit first
)

# For each city, pick the top category
top_per_city = result.loc[result.groupby('city')['avg_profit'].idxmax()]
print("Best category by avg profit per city:")
print(top_per_city)
```

**Deconstruct each step and ask: "What does the DataFrame look like at this point?"** This is the core debugging skill — knowing what shape your data is in at every step.

---

## Summary & Wrap-Up (5 min)

**The five transferable ideas from today:**
1. Every query is SELECT + FILTER + GROUP + ORDER — the same in every tool
2. Boolean masks are the mechanism behind every filter
3. GroupBy = split data into buckets, apply function, combine results
4. HAVING in SQL = filter after groupby in Pandas
5. Method chaining makes query intent readable top-to-bottom

**Bridge:** *"Next session we go deeper on Pandas aggregation and introduce SQL syntax formally. The query thinking you built today is exactly what you'll use to write GROUP BY and HAVING in SQL."*

---

## Q&A & Doubt Solving (5 min)

**Q: Why does `groupby()` make the grouped column an index? How do I undo that?**
→ Pandas makes the groupby key(s) the index for efficient lookups. Use `.reset_index()` at the end to bring it back as a regular column.

**Q: Can I groupby multiple columns?**
→ Yes: `df.groupby(['city', 'category'])`. The result is a MultiIndex — use `reset_index()` to flatten it.

**Q: What's the difference between `count()` and `size()` on a GroupBy?**
→ `count()` excludes NaN values. `size()` counts all rows including NaN. For accurate order counts, use `size()` or count a non-nullable column like an ID.

**Q: When is method chaining a bad idea?**
→ When debugging — break the chain to inspect intermediate results. Also, very long chains (10+ methods) become hard to read and maintain.

---

## Instructor Notes

- **Dataset:** The small inline Superstore-style dataset is intentional — students can see every row at once. For deeper practice, use the full Superstore CSV.
- **SQL display:** Even if students don't run SQL today, always show the SQL equivalent side-by-side. It builds the mental bridge for Sessions 10 and 12.
- **Common struggle:** `groupby` returning a GroupBy object (not a DataFrame) before `.sum()` is called. Show `type(df.groupby('city'))` and `type(df.groupby('city')['sales'].sum())` explicitly.
- **For advanced students:** Show `transform()` vs `agg()` — `transform()` returns a same-shape result (useful for adding a "% of total" column without merging).
