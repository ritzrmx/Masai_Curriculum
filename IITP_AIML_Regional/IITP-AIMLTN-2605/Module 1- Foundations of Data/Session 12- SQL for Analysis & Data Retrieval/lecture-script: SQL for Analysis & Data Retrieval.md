# Lecture Script: SQL for Analysis & Data Retrieval
> **Instructor Reference** — Module 1: Foundations of Data | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can write intermediate SQL — multi-table JOINs, subqueries, window functions, and CTEs — to answer real analytical questions, and they understand when SQL is the right tool vs Pandas.

**Student profile at this point:** Have seen basic SQL (Session 10) and GroupBy deeply (Session 9-10). This session formalises and advances their SQL knowledge.

**Key outcome:** Given a multi-table schema (orders, customers, products), students can write a 10-15 line SQL query to answer: *"Who are the top 5 customers by revenue this quarter, and what is their average order value compared to the overall average?"*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Schema Walkthrough | 5 min | 0:05 |
| **Concept 1:** JOINs in depth — INNER, LEFT, and when each matters | 10 min | 0:15 |
| **Practical 1:** Multi-table JOIN queries with business context | 15 min | 0:30 |
| **Concept 2:** Subqueries — queries inside queries | 10 min | 0:40 |
| **Practical 2:** Subquery patterns: scalar, IN, EXISTS, derived table | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Window Functions — RANK, ROW_NUMBER, running totals | 10 min | 1:15 |
| **Practical 3:** Window function queries | 15 min | 1:30 |
| **Concept 4:** CTEs — Writing Readable Multi-Step Queries | 10 min | 1:40 |
| **Practical 4:** CTE-based analytical query end-to-end | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Show the schema on board/screen:**

```
orders (order_id, customer_id, product_id, amount, status, order_date)
customers (customer_id, name, city, tier)
products (product_id, product_name, category, unit_price)
```

**Business question to open with:**
> *"I want to know: for each customer tier, what is the total revenue, the number of unique customers, and the name of their single highest-value order?"*

*"This is a real analyst request. Let's count how many concepts it requires: a JOIN (3 tables), a GROUP BY (by tier), an aggregate (SUM, COUNT), and a within-group operation (find the max order per customer). We'll have all of these by the end of today."*

---

## Concept Block 1: JOINs in Depth (10 min)

### The Four JOIN Types — Visual Explanation

Draw Venn-diagram style on board:

```
INNER JOIN: Only rows with a match in BOTH tables

LEFT JOIN:  All rows from left table
            Matched rows from right (NULLs for no match)

RIGHT JOIN: All rows from right table (rarely used in practice)

FULL JOIN:  All rows from both (NULLs for non-matches on either side)
```

### When to Use Each

| Scenario | JOIN type |
|---|---|
| "Show me all orders with customer name" | INNER (only valid orders with customers) |
| "Show me ALL orders, even if customer data is missing" | LEFT JOIN |
| "Find customers who have NEVER placed an order" | LEFT JOIN + WHERE right_key IS NULL |
| "Find all mismatches in two tables" | FULL JOIN |

### JOIN Syntax

```sql
SELECT o.order_id, c.name, c.city, o.amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id

-- Three-table join
SELECT o.order_id, c.name, p.product_name, o.amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p  ON o.product_id = p.product_id
```

**Key points:**
- Always use table aliases (`o`, `c`, `p`) in multi-table queries
- Specify which table each column comes from when column names might overlap: `o.order_id`, not just `order_id`

---

## Practical Block 1: Multi-Table JOIN Queries (15 min)

### Setup — create the SQLite database

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')

# Create tables
conn.executescript("""
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT, city TEXT, tier TEXT
);
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT, category TEXT, unit_price REAL
);
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT, product_id TEXT,
    amount REAL, status TEXT, order_date TEXT
);
""")

# Insert data
conn.executescript("""
INSERT INTO customers VALUES
('C1','Alice','Mumbai','Gold'),
('C2','Bob','Delhi','Silver'),
('C3','Charlie','Bangalore','Gold'),
('C4','Dave','Mumbai','Bronze');

INSERT INTO products VALUES
('P1','Laptop Pro','Tech',65000),
('P2','Office Chair','Furniture',12000),
('P3','Notebook Bundle','Office',800);

INSERT INTO orders VALUES
('O1','C1','P1',65000,'completed','2025-03-01'),
('O2','C2','P2',12000,'completed','2025-03-05'),
('O3','C1','P3',800,'completed','2025-03-10'),
('O4','C3','P1',65000,'completed','2025-03-12'),
('O5','C2','P1',65000,'cancelled','2025-03-15'),
('O6','C1','P2',12000,'completed','2025-03-18'),
('O7','C4','P3',800,'completed','2025-03-20'),
('O8','C3','P2',12000,'completed','2025-03-22');
""")

def sql(query):
    return pd.read_sql_query(query, conn)

print("Setup complete. Tables: orders, customers, products")
```

### JOIN Queries

```python
# Q1: All completed orders with customer name and product name
print("=== Completed orders (3-table join) ===")
print(sql("""
    SELECT o.order_id, c.name, p.product_name, o.amount
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN products p  ON o.product_id  = p.product_id
    WHERE o.status = 'completed'
    ORDER BY o.amount DESC
"""))

# Q2: LEFT JOIN — find customers with no orders (anti-join pattern)
print("\n=== Customers who placed zero orders ===")
print(sql("""
    SELECT c.name, c.city, o.order_id
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_id IS NULL
"""))

# Q3: Revenue by customer tier (join + group)
print("\n=== Revenue by tier ===")
print(sql("""
    SELECT c.tier,
           COUNT(DISTINCT c.customer_id) AS num_customers,
           SUM(o.amount) AS total_revenue,
           ROUND(AVG(o.amount), 0) AS avg_order_value
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.tier
    ORDER BY total_revenue DESC
"""))
```

---

## Concept Block 2: Subqueries (10 min)

### What Is a Subquery?

A subquery is a complete `SELECT` statement nested inside another query. It runs first and its result is used by the outer query.

**Three types:**

| Type | Where it appears | Returns | Example use |
|---|---|---|---|
| **Scalar** | In SELECT or WHERE | Single value | Compare to overall average |
| **IN/NOT IN** | In WHERE | A list | Find customers from a list |
| **Derived table** | In FROM | A table | Aggregate, then filter the aggregate |

```sql
-- Scalar subquery: orders above overall average
SELECT order_id, amount
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders WHERE status='completed');

-- IN subquery: orders from Gold customers
SELECT *
FROM orders
WHERE customer_id IN (SELECT customer_id FROM customers WHERE tier='Gold');

-- Derived table: top customer per city
SELECT city, name, city_total
FROM (
    SELECT c.city, c.name, SUM(o.amount) AS city_total
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.city, c.name
) ranked
ORDER BY city, city_total DESC;
```

---

## Practical Block 2: Subquery Patterns (15 min)

```python
# Q1: Scalar subquery — orders above overall average
print("=== Orders above average value ===")
print(sql("""
    SELECT o.order_id, c.name, o.amount,
           ROUND((SELECT AVG(amount) FROM orders WHERE status='completed'), 0) AS avg_order,
           o.amount - (SELECT AVG(amount) FROM orders WHERE status='completed') AS above_avg
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
      AND o.amount > (SELECT AVG(amount) FROM orders WHERE status='completed')
    ORDER BY o.amount DESC
"""))

# Q2: IN subquery
print("\n=== Orders from Gold-tier customers ===")
print(sql("""
    SELECT o.order_id, o.amount, o.status
    FROM orders o
    WHERE o.customer_id IN (
        SELECT customer_id FROM customers WHERE tier = 'Gold'
    )
"""))

# Q3: NOT IN — find customers who have never placed a COMPLETED order
print("\n=== Customers with no completed orders ===")
print(sql("""
    SELECT name, tier
    FROM customers
    WHERE customer_id NOT IN (
        SELECT DISTINCT customer_id 
        FROM orders 
        WHERE status = 'completed'
    )
"""))

# Q4: Derived table — customer totals, then filter to those > 50,000
print("\n=== High-value customers (total > ₹50,000) ===")
print(sql("""
    SELECT name, tier, total_spent
    FROM (
        SELECT c.name, c.tier, SUM(o.amount) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'completed'
        GROUP BY c.name, c.tier
    ) customer_totals
    WHERE total_spent > 50000
    ORDER BY total_spent DESC
"""))
```

---

## BREAK (10 min)

*Ask students to think: "Can I solve the derived table query above without a subquery? What Pandas method would be equivalent to HAVING on a grouped result?"*

---

## Concept Block 3: Window Functions (10 min)

### What Window Functions Do

Regular `GROUP BY` collapses rows. **Window functions** compute aggregates over a "window" of rows *while keeping all rows*.

```sql
SELECT order_id, customer_id, amount,
       SUM(amount) OVER ()                           AS grand_total,
       SUM(amount) OVER (PARTITION BY customer_id)  AS customer_total,
       RANK()      OVER (ORDER BY amount DESC)       AS overall_rank,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS cust_rank
FROM orders
WHERE status = 'completed';
```

**Key clauses:**
- `OVER ()` — window = all rows
- `OVER (PARTITION BY col)` — separate window per group (like groupby without collapsing)
- `OVER (ORDER BY col)` — ordered window (enables running totals, ranks)

### Common Window Functions

| Function | What it computes |
|---|---|
| `RANK()` | Rank with gaps (ties get same rank, next rank skips) |
| `DENSE_RANK()` | Rank without gaps |
| `ROW_NUMBER()` | Unique sequential number |
| `SUM() OVER (ORDER BY ...)` | Running total |
| `LAG(col, n)` | Value from n rows before |
| `LEAD(col, n)` | Value from n rows ahead |

---

## Practical Block 3: Window Function Queries (15 min)

```python
# Q1: Rank orders by amount (global)
print("=== Orders ranked by amount ===")
print(sql("""
    SELECT o.order_id, c.name, o.amount,
           RANK()       OVER (ORDER BY o.amount DESC) AS rank,
           DENSE_RANK() OVER (ORDER BY o.amount DESC) AS dense_rank
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
"""))

# Q2: Running total of revenue over time
print("\n=== Running revenue by date ===")
print(sql("""
    SELECT order_date, amount,
           SUM(amount) OVER (ORDER BY order_date) AS running_total
    FROM orders
    WHERE status = 'completed'
    ORDER BY order_date
"""))

# Q3: Rank orders within each customer (useful for "top N per customer")
print("\n=== Rank within each customer ===")
print(sql("""
    SELECT c.name, o.order_id, o.amount,
           ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.amount DESC) AS cust_rank
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    ORDER BY c.name, cust_rank
"""))

# Q4: Top 1 order per customer (using subquery on window result)
print("\n=== Highest order per customer ===")
print(sql("""
    SELECT name, order_id, amount
    FROM (
        SELECT c.name, o.order_id, o.amount,
               ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.amount DESC) AS rn
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'completed'
    )
    WHERE rn = 1
"""))
```

---

## Concept Block 4: CTEs — Readable Multi-Step Queries (10 min)

### What Is a CTE?

A **Common Table Expression (CTE)** is a named temporary result set defined at the top of a query with `WITH`. It replaces nested subqueries and makes complex queries readable top-to-bottom.

```sql
WITH customer_revenue AS (
    SELECT customer_id, SUM(amount) AS total_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
top_customers AS (
    SELECT customer_id, total_revenue
    FROM customer_revenue
    WHERE total_revenue > 50000
)
SELECT c.name, c.tier, tc.total_revenue
FROM top_customers tc
JOIN customers c ON tc.customer_id = c.customer_id
ORDER BY tc.total_revenue DESC;
```

**CTE = Pandas chained operations.** Each `WITH` clause is like storing an intermediate result in a variable.

**When to use CTEs:**
- When a subquery is used more than once
- When the query is more than 3 levels deep (nested subqueries become unreadable)
- When you want to name intermediate steps for documentation

---

## Practical Block 4: CTE-Based Analytical Query (10 min)

**The full opening question — solved with CTEs:**
*"For each customer tier: total revenue, number of unique customers, average order value, and the name of the single highest-value customer."*

```python
print("=== Full tier analysis with CTEs ===")
print(sql("""
    WITH completed AS (
        -- Step 1: filter to completed orders only
        SELECT o.*, c.name, c.tier
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'completed'
    ),
    tier_summary AS (
        -- Step 2: aggregate by tier
        SELECT tier,
               COUNT(DISTINCT customer_id) AS num_customers,
               SUM(amount) AS total_revenue,
               ROUND(AVG(amount), 0) AS avg_order_value
        FROM completed
        GROUP BY tier
    ),
    top_customer_per_tier AS (
        -- Step 3: find highest-value customer per tier
        SELECT tier, name, customer_revenue,
               ROW_NUMBER() OVER (PARTITION BY tier ORDER BY customer_revenue DESC) AS rn
        FROM (
            SELECT tier, name, SUM(amount) AS customer_revenue
            FROM completed
            GROUP BY tier, name
        )
    )
    -- Step 4: combine tier summary with top customer name
    SELECT ts.tier, ts.num_customers, ts.total_revenue,
           ts.avg_order_value, tc.name AS top_customer
    FROM tier_summary ts
    LEFT JOIN top_customer_per_tier tc 
           ON ts.tier = tc.tier AND tc.rn = 1
    ORDER BY ts.total_revenue DESC
"""))
```

**Walk through each CTE:** `completed` → `tier_summary` → `top_customer_per_tier` → final join. Ask students: *"Could you build this without CTEs? How many nesting levels would it need?"*

---

## Summary & Wrap-Up (5 min)

**The SQL toolkit we built today:**
- JOINs: INNER (both match), LEFT (keep all from left), anti-join pattern (`LEFT JOIN ... WHERE right IS NULL`)
- Subqueries: scalar (single value), IN list, derived table (aggregate then filter)
- Window functions: RANK, ROW_NUMBER, running totals, PARTITION BY for group-level results at row level
- CTEs: named intermediate steps that replace nested subqueries

**Bridge:** *"Next session is EDA — Exploratory Data Analysis. You'll take the SQL and Pandas tools you've built and apply them to tell a visual story from a dataset. We'll add charts, distributions, and correlations."*

---

## Q&A & Doubt Solving (5 min)

**Q: When should I use a subquery vs a CTE?**
→ Use a CTE when the subquery is long, reused, or when you want readable named steps. Subqueries are fine for simple, one-time inline conditions. Never nest more than 2 levels deep without a CTE.

**Q: What's the difference between RANK and DENSE_RANK?**
→ With three items scoring 100, 100, 80: RANK gives 1, 1, 3 (skips rank 2). DENSE_RANK gives 1, 1, 2 (no gap). Use DENSE_RANK when you want "top 3 unique ranks" — RANK would give you position counts.

**Q: Can I use window functions in WHERE?**
→ No — window functions are evaluated in SELECT, after WHERE. To filter on a window function result, wrap it in a subquery or CTE and filter in the outer query.

**Q: How do I run this SQL on a real file, not just in-memory?**
→ Connect to a real SQLite file: `conn = sqlite3.connect('mydata.db')`. Or use pandas directly: `pd.read_sql_query(query, conn)` works with any database connection (SQLite, PostgreSQL, MySQL via their respective connectors).

---

## Instructor Notes

- **SQLite limitations:** SQLite does not support `RIGHT JOIN` or `FULL OUTER JOIN`. For those, demonstrate on PostgreSQL or mention as a note. For this session, INNER and LEFT cover 90% of real use cases.
- **Window function gotcha:** SQLite supports window functions from version 3.25 (released 2018). Verify student Python installations have a recent sqlite3. `SELECT sqlite_version()` in the session confirms this.
- **Dataset size:** The 8-row dataset is intentional — students can verify results mentally. For homework, give them the full Superstore/Titanic dataset as a SQL file.
- **For advanced students:** Show CTEs with `RECURSIVE` for hierarchical data (org charts, bill-of-materials). Even one simple example (counting 1 to 5) makes the concept clear.
