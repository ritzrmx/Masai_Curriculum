# Coding Problem: SQL Joins & Relational Analysis
> **Session 13 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import sqlite3, pandas as pd

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE orders (
    order_id TEXT, customer_id TEXT,
    amount REAL, status TEXT
);
CREATE TABLE customers (
    customer_id TEXT, name TEXT, city TEXT
);
INSERT INTO orders VALUES
('O1','C1',65000,'completed'),
('O2','C2',12000,'completed'),
('O3','C1', 5000,'cancelled'),
('O4','C3',85000,'completed'),
('O5','C4', 9000,'completed');

INSERT INTO customers VALUES
('C1','Alice','Mumbai'),
('C2','Bob','Delhi'),
('C3','Charlie','Bangalore');
-- Note: C4 has NO customer record
""")

def sql(q): return pd.read_sql_query(q, conn)
```

---

## Tasks

**Task 1 — Basic**
Write an **INNER JOIN** to show `order_id`, `name`, `city`, and `amount` for completed orders only.

**Task 2 — Basic**
Write a **LEFT JOIN** to show all orders. For orders with no matching customer, the name should appear as `NULL`.

**Task 3 — Mid**
Write a query to show **total completed revenue per city**, sorted highest first.

---

## Expected Output

```
-- Task 1 (INNER JOIN — only orders with a known customer)
  order_id     name       city   amount
0       O1    Alice     Mumbai  65000.0
1       O2      Bob      Delhi  12000.0
2       O4  Charlie  Bangalore  85000.0

-- Task 2 (LEFT JOIN — all orders, NULL for unknown customer)
  order_id     name       city   amount     status
0       O1    Alice     Mumbai  65000.0  completed
1       O2      Bob      Delhi  12000.0  completed
2       O3    Alice     Mumbai   5000.0  cancelled
3       O4  Charlie  Bangalore  85000.0  completed
4       O5     None       None   9000.0  completed

-- Task 3 (Revenue per city)
        city  total_revenue
0  Bangalore        85000.0
1     Mumbai        65000.0
2      Delhi        12000.0
```

---

<details>
<summary>Solution</summary>

```python
# Task 1 — INNER JOIN
print(sql("""
    SELECT o.order_id, c.name, c.city, o.amount
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
"""))

# Task 2 — LEFT JOIN
print(sql("""
    SELECT o.order_id, c.name, c.city, o.amount, o.status
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
"""))

# Task 3 — GROUP BY with JOIN
print(sql("""
    SELECT c.city, SUM(o.amount) AS total_revenue
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.city
    ORDER BY total_revenue DESC
"""))
```

</details>
