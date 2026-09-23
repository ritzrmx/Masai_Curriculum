# Coding Problem: Data Analysis with Spreadsheets
> **Session 16 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import sqlite3, pandas as pd

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE sales (
    rep TEXT, region TEXT, product TEXT,
    amount REAL, status TEXT
);
INSERT INTO sales VALUES
('Alice','North','Laptop',65000,'completed'),
('Bob','South','Chair',12000,'completed'),
('Alice','North','Notebook',800,'cancelled'),
('Charlie','East','Laptop',65000,'completed'),
('Bob','South','Laptop',65000,'completed'),
('Charlie','East','Chair',12000,'cancelled');
""")

def sql(q): return pd.read_sql_query(q, conn)
```

---

## Tasks

**Task 1 — Basic**
Write a query to show all **completed** sales, ordered by `amount` descending.

**Task 2 — Basic**
Write a query to show the **total amount** per `rep` for completed sales only.

**Task 3 — Mid**
Write a query to show only reps whose **total completed sales exceed ₹70,000**.

---

## Expected Output

```
-- Task 1
       rep   region   product   amount    status
0    Alice    North    Laptop  65000.0  completed
1  Charlie     East    Laptop  65000.0  completed
2      Bob    South    Laptop  65000.0  completed
3      Bob    South     Chair  12000.0  completed

-- Task 2
       rep  total_amount
0    Alice       65000.0
1      Bob       77000.0
2  Charlie       65000.0

-- Task 3
   rep  total_amount
0  Bob       77000.0
```

---

<details>
<summary>Solution</summary>

```python
# Task 1
print(sql("""
    SELECT * FROM sales
    WHERE status = 'completed'
    ORDER BY amount DESC
"""))

# Task 2
print(sql("""
    SELECT rep, SUM(amount) AS total_amount
    FROM sales
    WHERE status = 'completed'
    GROUP BY rep
"""))

# Task 3
print(sql("""
    SELECT rep, SUM(amount) AS total_amount
    FROM sales
    WHERE status = 'completed'
    GROUP BY rep
    HAVING SUM(amount) > 70000
"""))
```

</details>
