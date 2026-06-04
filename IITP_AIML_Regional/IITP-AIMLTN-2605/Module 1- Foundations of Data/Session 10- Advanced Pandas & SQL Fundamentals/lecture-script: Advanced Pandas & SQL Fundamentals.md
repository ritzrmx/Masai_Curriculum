# Lecture Script: Advanced Pandas & SQL Fundamentals
> **Instructor Reference** — Module 1: Foundations of Data | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can write multi-step aggregation pipelines in both Pandas and SQL — including window functions, pivot tables, and multi-table joins — and know when to use each tool.

**Student profile at this point:** Can filter and group in Pandas. Have seen SQL syntax for the first time (Session 9). Are comfortable with DataFrames and chaining.

**Key outcome:** Students leave able to answer "what percentage of total revenue does each city contribute?" and "what was last month's vs this month's revenue?" — in both Pandas and SQL.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Advanced GroupBy — Multi-metric, Named Agg, Transform | 10 min | 0:15 |
| **Practical 1:** Percent-of-total, running total, rank within group | 15 min | 0:30 |
| **Concept 2:** Pivot Tables — Reshaping Data | 10 min | 0:40 |
| **Practical 2:** `pivot_table()` vs `groupby().unstack()` | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** SQL Fundamentals — SELECT, WHERE, GROUP BY, ORDER BY | 10 min | 1:15 |
| **Practical 3:** Write and run SQL queries (SQLite in-memory) | 15 min | 1:30 |
| **Concept 4:** Combining DataFrames — `merge()` and SQL JOIN | 10 min | 1:40 |
| **Practical 4:** JOIN exercise with orders + customers tables | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Show this output and ask *"How would you produce this from raw sales data?"*

```
city       | total_sales | pct_of_total | rank
-----------|-------------|--------------|-----
Mumbai     | 52,000      | 41.3%        | 1
Delhi      | 45,500      | 36.1%        | 2
Bangalore  | 21,000      | 16.7%        | 3
```

*"Single groupby? Multiple groupbys? SQL? Today we learn how to produce all three output columns in one operation."*

**Context:** Real analyst work is rarely a single filter. It's multi-layered: filter → group → aggregate → compare → rank → present. Today we build that complete toolkit.

---

## Concept Block 1: Advanced GroupBy — Multi-metric, Named Agg, Transform (10 min)

### Named Aggregation (`.agg()` with keyword syntax)

The cleanest way to compute multiple aggregations and name the output columns:

```python
df.groupby('city').agg(
    total_sales   = ('sales', 'sum'),
    avg_sales     = ('sales', 'mean'),
    order_count   = ('order_id', 'count'),
    max_profit    = ('profit', 'max')
)
```

**Output:** A DataFrame with exactly those four columns, named as specified. Much cleaner than the old `.agg({'sales': ['sum','mean']})` approach.

### `transform()` — Group-level results at row level

`agg()` returns one row per group. `transform()` returns the same number of rows as the original DataFrame — each row gets the group's aggregate value.

```python
# Add a column showing each city's total sales to every row
df['city_total'] = df.groupby('city')['sales'].transform('sum')

# Now you can compute % of total at the row level
df['pct_of_city_total'] = df['sales'] / df['city_total'] * 100
```

**Use case:** "What % of its city's total sales does each order represent?" — impossible with `agg()`, trivial with `transform()`.

---

## Practical Block 1: Percent-of-Total, Running Total, Rank Within Group (15 min)

```python
import pandas as pd

data = {
    'order_id': ['O1','O2','O3','O4','O5','O6','O7','O8'],
    'city': ['Mumbai','Delhi','Mumbai','Bangalore','Delhi','Mumbai','Delhi','Bangalore'],
    'category': ['Tech','Furniture','Tech','Office','Tech','Furniture','Office','Tech'],
    'sales': [25000, 8000, 15000, 3000, 32000, 12000, 5500, 18000],
    'profit': [5000, -500, 3200, 800, 8000, 1200, 600, 4000],
    'order_date': pd.to_datetime(['2025-03-01','2025-03-05','2025-03-10','2025-03-12',
                                   '2025-03-15','2025-03-18','2025-03-20','2025-03-22'])
}
df = pd.DataFrame(data)

# --- Named aggregation ---
city_summary = df.groupby('city').agg(
    total_sales  = ('sales', 'sum'),
    avg_sales    = ('sales', 'mean'),
    order_count  = ('order_id', 'count')
).reset_index()
print("City summary:")
print(city_summary)

# --- Percent of total ---
city_summary['pct_of_total'] = (
    city_summary['total_sales'] / city_summary['total_sales'].sum() * 100
).round(1)
city_summary = city_summary.sort_values('total_sales', ascending=False)
city_summary['rank'] = range(1, len(city_summary)+1)
print("\nCity summary with % and rank:")
print(city_summary)

# --- transform() for row-level group stats ---
df['city_total'] = df.groupby('city')['sales'].transform('sum')
df['pct_of_city'] = (df['sales'] / df['city_total'] * 100).round(1)
print("\nOrders with city % share:")
print(df[['order_id','city','sales','city_total','pct_of_city']])

# --- Cumulative sum (running total) within groups ---
df_sorted = df.sort_values(['city', 'order_date'])
df_sorted['running_sales'] = df_sorted.groupby('city')['sales'].cumsum()
print("\nRunning total by city:")
print(df_sorted[['city','order_date','sales','running_sales']])
```

**Key discussion point after `transform`:** *"What shape is the result? Why is it the same number of rows as df?"* Show `df.groupby('city')['sales'].transform('sum')` and compare to `.agg()`.

---

## Concept Block 2: Pivot Tables — Reshaping Data (10 min)

### What Is a Pivot Table?

A pivot table rotates data — one column becomes the row index, another becomes column headers, and values are aggregated at each intersection.

```
Before (long format):          After pivot (wide format):
city       category  sales     category  Furniture  Office  Tech
Mumbai     Tech      25000     city
Delhi      Furniture  8000     Bangalore   0         3000   18000
Mumbai     Tech      15000     Delhi       8000      5500   32000
...                            Mumbai      12000     0      40000
```

**When to use long vs wide:**
- **Long (tidy) format:** Ideal for Pandas operations, plotting, ML
- **Wide (pivot) format:** Ideal for human-readable reports, dashboards

### Two Ways to Pivot

```python
# Method 1: pivot_table (handles duplicates via aggregation)
pd.pivot_table(df,
    values='sales',
    index='city',
    columns='category',
    aggfunc='sum',
    fill_value=0
)

# Method 2: groupby + unstack (equivalent, more explicit)
df.groupby(['city', 'category'])['sales'].sum().unstack(fill_value=0)
```

---

## Practical Block 2: Pivot Table vs GroupBy Unstack (15 min)

```python
# --- Method 1: pivot_table ---
pivot = pd.pivot_table(
    df,
    values='sales',
    index='city',
    columns='category',
    aggfunc='sum',
    fill_value=0
)
print("Pivot table — sales by city × category:")
print(pivot)

# Add row totals and column totals
pivot['TOTAL'] = pivot.sum(axis=1)
print("\nWith row totals:")
print(pivot)

# --- Method 2: groupby + unstack ---
pivot2 = (
    df.groupby(['city', 'category'])['sales']
    .sum()
    .unstack(fill_value=0)
)
print("\nUnstack result (same as above):")
print(pivot2)

# --- Multiple values in pivot ---
multi_pivot = pd.pivot_table(
    df,
    values=['sales', 'profit'],
    index='city',
    columns='category',
    aggfunc='sum',
    fill_value=0
)
print("\nMulti-value pivot:")
print(multi_pivot)
```

**Teaching point:** `pivot_table` requires an `aggfunc` because there might be multiple values at each intersection. Without it, Pandas defaults to mean — which is often wrong for sales totals.

---

## BREAK (10 min)

*Ask students to write (mentally or on paper): "What is the SQL equivalent of `df.groupby('city')['sales'].sum()`?" They will answer after the break.*

---

## Concept Block 3: SQL Fundamentals (10 min)

### Core SQL Query Structure

```sql
SELECT columns_or_aggregates
FROM   table_name
WHERE  row_filter_conditions
GROUP BY grouping_columns
HAVING aggregate_filter_conditions
ORDER BY sort_column DESC
LIMIT  n;
```

**Execution order (what the database does, not what you write):**

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

**Key rules to emphasise:**

1. `WHERE` filters individual rows **before** grouping — cannot reference aggregate functions
2. `HAVING` filters groups **after** grouping — can reference aggregate functions
3. Every `SELECT` column must be either in `GROUP BY` or wrapped in `SUM/AVG/COUNT/MAX/MIN`
4. `COUNT(*)` = count all rows; `COUNT(column)` = count non-null values in that column

### Pandas-to-SQL Cheat Sheet (write on board)

```
df[df['col'] > 100]                     →  WHERE col > 100
df.groupby('city')['sales'].sum()        →  GROUP BY city → SUM(sales)
df.sort_values('sales', ascending=False) →  ORDER BY sales DESC
df.head(5)                               →  LIMIT 5
df[df['sales'] > 10000]  (after group)  →  HAVING SUM(sales) > 10000
```

---

## Practical Block 3: SQL Queries with SQLite (15 min)

Use Python's built-in `sqlite3` — no installation needed:

```python
import sqlite3
import pandas as pd

# --- Setup: create in-memory DB from our DataFrame ---
conn = sqlite3.connect(':memory:')
df.to_sql('orders', conn, index=False, if_exists='replace')

# Helper function for clean output
def sql(query):
    return pd.read_sql_query(query, conn)

# --- Q1: Basic SELECT + WHERE ---
print("Completed orders:")
print(sql("""
    SELECT order_id, city, sales
    FROM orders
    WHERE status = 'completed'
    ORDER BY sales DESC
"""))

# --- Q2: GROUP BY + aggregation ---
print("\nSales by city:")
print(sql("""
    SELECT city,
           SUM(sales) AS total_sales,
           COUNT(*) AS order_count,
           ROUND(AVG(profit), 0) AS avg_profit
    FROM orders
    GROUP BY city
    ORDER BY total_sales DESC
"""))

# --- Q3: HAVING clause ---
print("\nCategories with total sales > 30,000:")
print(sql("""
    SELECT category, SUM(sales) AS total
    FROM orders
    GROUP BY category
    HAVING SUM(sales) > 30000
"""))

# --- Q4: Multi-condition WHERE ---
print("\nHigh-value Tech orders:")
print(sql("""
    SELECT *
    FROM orders
    WHERE category = 'Tech'
      AND sales > 15000
    ORDER BY sales DESC
"""))
```

**Teach the translation live:** After each SQL query, ask a student to write the Pandas equivalent. Confirm on screen.

---

## Concept Block 4: Combining DataFrames — `merge()` and SQL JOIN (10 min)

### The Four Join Types

```
INNER JOIN: only rows where the key exists in BOTH tables
LEFT JOIN:  all rows from left; NaN for non-matching right rows
RIGHT JOIN: all rows from right; NaN for non-matching left rows  
FULL JOIN:  all rows from both; NaN for any non-matches
```

**Most common in data work:** LEFT JOIN (keep all orders, enrich with customer data even if customer info is incomplete).

### Pandas `merge()` Syntax

```python
merged = orders_df.merge(
    customers_df,
    on='customer_id',     # key column
    how='left'            # join type: 'inner', 'left', 'right', 'outer'
)
```

**SQL equivalent:**
```sql
SELECT o.*, c.name, c.tier
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;
```

---

## Practical Block 4: JOIN Exercise (10 min)

```python
# --- Two tables ---
orders = pd.DataFrame({
    'order_id': ['O1','O2','O3','O4','O5'],
    'customer_id': ['C1','C2','C1','C3','C4'],
    'sales': [25000, 8000, 15000, 32000, 12000]
})

customers = pd.DataFrame({
    'customer_id': ['C1','C2','C3'],   # Note: C4 is missing
    'name': ['Alice', 'Bob', 'Charlie'],
    'tier': ['Gold', 'Silver', 'Gold']
})

# --- INNER JOIN ---
inner = orders.merge(customers, on='customer_id', how='inner')
print("INNER JOIN (only matching customers):")
print(inner)
print(f"Rows: {len(inner)} — O5 (C4) is dropped")

# --- LEFT JOIN ---
left = orders.merge(customers, on='customer_id', how='left')
print("\nLEFT JOIN (all orders, NaN for missing customer):")
print(left)
print(f"Rows: {len(left)} — O5 still present, name/tier = NaN")

# --- Post-join aggregation ---
summary = (
    left
    .groupby('tier')['sales']
    .agg(total=('sales','sum') if False else 'sum',  # works either way
         count='count')
    .reset_index()
)
# Cleaner:
summary = left.groupby('tier').agg(total_sales=('sales','sum'),
                                    order_count=('order_id','count')).reset_index()
print("\nSales by customer tier (after join):")
print(summary)
```

**Ask:** *"Why does the Gold tier have higher total sales — higher value customers or more orders? How would you tell from the data?"*

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- `agg()` with named outputs for multi-metric summaries
- `transform()` for group stats at the row level (% of total, running totals)
- Pivot tables: reshaping long → wide for reports
- Full SQL syntax: SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
- SQL JOINs and `pd.merge()` — always decide your join type before coding

**Bridge:** *"Next session is a Master Class on the mathematical foundations — coordinate geometry, descriptive statistics, and what 'mean' and 'variance' actually tell you. After that, we go deep on SQL joins and analysis in Session 12."*

---

## Q&A & Doubt Solving (5 min)

**Q: What is the difference between `merge()` and `join()`?**
→ `join()` merges on the DataFrame's index; `merge()` works on any column. Use `merge()` — it is more explicit and flexible.

**Q: When does `pivot_table` give different results from `groupby().unstack()`?**
→ They give the same result for simple cases. `pivot_table` is slightly more powerful (handles multiple aggfuncs, automatic margins/totals with `margins=True`). For production code, either works.

**Q: Can I run SQL and Pandas on the same data?**
→ Yes — that is exactly what we did with `df.to_sql()` and `pd.read_sql_query()`. You can also use `pandasql` or `duckdb` for running SQL directly on DataFrames without loading into SQLite.

**Q: What happens to NaN values in a groupby?**
→ By default, Pandas excludes NaN keys from groupby (NaN rows are not placed in any group). Use `dropna=False` in `groupby()` to include them as a group.

---

## Instructor Notes

- **Dataset:** Keep the compact 8-row dataset for clarity. For the SQL join exercise, the 5-row tables with one orphaned customer (C4) makes the INNER vs LEFT JOIN difference crystal clear.
- **SQLite in-memory:** Requires zero installation — every student can run it. If students want to persist the database, change `':memory:'` to a file path.
- **Common confusion:** `HAVING SUM(sales) > 30000` vs `WHERE sales > 30000`. Build a concrete example showing why `WHERE SUM(sales) > 30000` fails (SQL runs WHERE before aggregation).
- **Advanced extension:** Show `WITH` (CTE) syntax as a cleaner alternative to subqueries — mirrors Pandas chaining in readability.
