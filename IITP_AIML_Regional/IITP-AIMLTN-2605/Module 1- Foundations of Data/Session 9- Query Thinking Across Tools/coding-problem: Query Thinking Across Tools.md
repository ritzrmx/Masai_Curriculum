# Coding Problem: Query Thinking Across Tools
> **Session 9 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import pandas as pd

data = {
    "order_id": ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"],
    "city":     ["Mumbai", "Delhi", "Mumbai", "Bangalore", "Delhi", "Mumbai", "Delhi", "Bangalore"],
    "category": ["Tech", "Furniture", "Tech", "Office", "Tech", "Furniture", "Office", "Tech"],
    "sales":    [25000, 8000, 15000, 3000, 32000, 12000, 5500, 18000],
    "profit":   [5000, -500, 3200, 800, 8000, 1200, 600, 4000],
    "status":   ["completed", "completed", "completed", "cancelled", "completed", "completed", "cancelled", "completed"]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Filter and print all **completed** orders from **Mumbai** (`order_id`, `city`, `sales`, `profit`).

**Task 2 — Basic**
Among **completed** orders, sort by `sales` descending and print the **top 3**.

**Task 3 — Mid**
Group by `city` and print **total sales** for completed orders only, sorted highest first.

---

## Expected Output

```
  order_id    city  sales  profit
0       O1  Mumbai  25000    5000
2       O3  Mumbai  15000    3200
5       O6  Mumbai  12000    1200

  order_id    city  sales  profit
4       O5   Delhi  32000    8000
0       O1  Mumbai  25000    5000
2       O3  Mumbai  15000    3200

         sales
city
Mumbai   52000
Delhi    40000
Bangalore 18000
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd

data = {
    "order_id": ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"],
    "city":     ["Mumbai", "Delhi", "Mumbai", "Bangalore", "Delhi", "Mumbai", "Delhi", "Bangalore"],
    "category": ["Tech", "Furniture", "Tech", "Office", "Tech", "Furniture", "Office", "Tech"],
    "sales":    [25000, 8000, 15000, 3000, 32000, 12000, 5500, 18000],
    "profit":   [5000, -500, 3200, 800, 8000, 1200, 600, 4000],
    "status":   ["completed", "completed", "completed", "cancelled", "completed", "completed", "cancelled", "completed"]
}
df = pd.DataFrame(data)

completed = df[df["status"] == "completed"]

# Task 1
print(completed[completed["city"] == "Mumbai"][["order_id", "city", "sales", "profit"]])

# Task 2
print(completed.sort_values("sales", ascending=False).head(3)[["order_id", "city", "sales", "profit"]])

# Task 3
city_sales = completed.groupby("city")["sales"].sum().sort_values(ascending=False)
print(city_sales)
```

</details>
