# Coding Problem: SQL with MySQL Workbench
> **Session 15 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
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

def sql(q):
    return pd.read_sql_query(q, conn)
```

---

## Tasks

**Task 1 — Basic**
Write a **3-table INNER JOIN** to show `order_id`, customer `name`, `product_name`, and `amount` for **completed** orders, sorted by `amount` descending.

**Task 2 — Basic**
Write a query to show **total completed revenue per customer tier**, sorted highest first.

**Task 3 — Mid**
Write a query using a **subquery** to list customers whose **total completed spend exceeds ₹70,000**.

---

## Expected Output

```
-- Task 1
  order_id     name     product_name   amount
0       O1    Alice       Laptop Pro  65000.0
1       O4  Charlie       Laptop Pro  65000.0
2       O2      Bob     Office Chair  12000.0
3       O6    Alice     Office Chair  12000.0
4       O8  Charlie     Office Chair  12000.0
5       O3    Alice  Notebook Bundle    800.0
6       O7     Dave  Notebook Bundle    800.0

-- Task 2
     tier  total_revenue
0    Gold        154800.0
1  Silver        12000.0
2  Bronze          800.0

-- Task 3
      name  total_spend
0    Alice      77800.0
1  Charlie      77000.0
```

---

<details>
<summary>Solution</summary>

```python
# Task 1
print(sql("""
    SELECT o.order_id, c.name, p.product_name, o.amount
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN products p  ON o.product_id  = p.product_id
    WHERE o.status = 'completed'
    ORDER BY o.amount DESC
"""))

# Task 2
print(sql("""
    SELECT c.tier, SUM(o.amount) AS total_revenue
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.tier
    ORDER BY total_revenue DESC
"""))

# Task 3
print(sql("""
    SELECT c.name, SUM(o.amount) AS total_spend
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.name
    HAVING SUM(o.amount) > 70000
    ORDER BY total_spend DESC
"""))
```

</details>
