# Coding Problem: Advanced Pandas & SQL Fundamentals
> **Session 10 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import pandas as pd
import sqlite3

data = {
    "order_id": ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"],
    "city":     ["Mumbai", "Delhi", "Mumbai", "Bangalore", "Delhi", "Mumbai", "Delhi", "Bangalore"],
    "sales":    [25000, 8000, 15000, 3000, 32000, 12000, 5500, 18000],
    "status":   ["completed", "completed", "completed", "cancelled", "completed", "completed", "cancelled", "completed"]
}
df = pd.DataFrame(data)

conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False, if_exists="replace")

def sql(q):
    return pd.read_sql_query(q, conn)
```

---

## Tasks

**Task 1 — Basic (Pandas)**
Using **named aggregation**, group by `city` and compute `total_sales` (sum of `sales`) and `order_count` (count of `order_id`) for **completed** orders only.

**Task 2 — Basic (Pandas)**
Add a column `pct_of_total` showing each completed order's share of **overall completed sales** (round to 1 decimal). Print `order_id`, `city`, `sales`, `pct_of_total` for Mumbai orders.

**Task 3 — Mid (SQL)**
Write a SQL query: **total sales per city** for completed orders, sorted highest first.

---

## Expected Output

```
         total_sales  order_count
city
Bangalore      18000            1
Delhi          40000            2
Mumbai         52000            3

  order_id    city  sales  pct_of_total
0       O1  Mumbai  25000          22.7
2       O3  Mumbai  15000          13.6
5       O6  Mumbai  12000          10.9

         city  total_sales
0      Mumbai        52000
1       Delhi        40000
2  Bangalore        18000
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import sqlite3

data = {
    "order_id": ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"],
    "city":     ["Mumbai", "Delhi", "Mumbai", "Bangalore", "Delhi", "Mumbai", "Delhi", "Bangalore"],
    "sales":    [25000, 8000, 15000, 3000, 32000, 12000, 5500, 18000],
    "status":   ["completed", "completed", "completed", "cancelled", "completed", "completed", "cancelled", "completed"]
}
df = pd.DataFrame(data)

conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False, if_exists="replace")

def sql(q):
    return pd.read_sql_query(q, conn)

completed = df[df["status"] == "completed"]

# Task 1
print(completed.groupby("city").agg(
    total_sales=("sales", "sum"),
    order_count=("order_id", "count")
))

# Task 2
total = completed["sales"].sum()
completed = completed.copy()
completed["pct_of_total"] = (completed["sales"] / total * 100).round(1)
print(completed[completed["city"] == "Mumbai"][["order_id", "city", "sales", "pct_of_total"]])

# Task 3
print(sql("""
    SELECT city, SUM(sales) AS total_sales
    FROM orders
    WHERE status = 'completed'
    GROUP BY city
    ORDER BY total_sales DESC
"""))
```

</details>
