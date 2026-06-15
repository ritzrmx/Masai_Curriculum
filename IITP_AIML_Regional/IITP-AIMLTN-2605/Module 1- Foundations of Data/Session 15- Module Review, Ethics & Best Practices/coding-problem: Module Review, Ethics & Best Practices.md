# Coding Problem: Module Review, Ethics & Best Practices
> **Session 15 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

DataMart's raw sales export — duplicates, nulls, and mixed date formats:

```python
import pandas as pd
import io

raw_data = """
order_id,rep,region,product,revenue,cost,order_date,status
1001,Priya,North,Laptop,65000,50000,01-03-2025,completed
1002,Arjun,South,Chair,12000,8000,05/03/2025,completed
1001,Priya,North,Laptop,65000,50000,01-03-2025,completed
1003,Meera,East,Laptop,65000,50000,2025-03-10,cancelled
1004,Arjun,South,Notebook,800,400,12-03-2025,completed
1005,Priya,North,Laptop,65000,50000,15-03-2025,completed
1006,Ravi,West,Chair,12000,,18-03-2025,completed
1007,Meera,East,Notebook,800,400,20-03-2025,completed
1008,Ravi,West,Laptop,65000,50000,22-03-2025,
1009,Arjun,South,Laptop,65000,50000,25-03-2025,completed
"""

df = pd.read_csv(io.StringIO(raw_data))
```

---

## Tasks

**Task 1 — Basic**
Audit the raw data: print **shape**, **null counts per column**, and **duplicate row count**.

**Task 2 — Basic**
Clean the data:
- Drop duplicates
- Parse `order_date` with `pd.to_datetime(..., dayfirst=True)`
- Fill missing `cost` with the **median cost per product**
- Fill missing `status` with `'unknown'`
- Add `profit = revenue - cost`

**Task 3 — Mid**
On **completed** orders only, print which **region has the highest total profit** and the **sales rep with the highest total profit**.

---

## Expected Output

```
Shape: (9, 8)

Nulls:
order_id      0
rep           0
region        0
product       0
revenue       0
cost          1
order_date    0
status        1

Duplicate rows: 1

Top region by profit: North
Top rep by profit: Priya
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import io

raw_data = """
order_id,rep,region,product,revenue,cost,order_date,status
1001,Priya,North,Laptop,65000,50000,01-03-2025,completed
1002,Arjun,South,Chair,12000,8000,05/03/2025,completed
1001,Priya,North,Laptop,65000,50000,01-03-2025,completed
1003,Meera,East,Laptop,65000,50000,2025-03-10,cancelled
1004,Arjun,South,Notebook,800,400,12-03-2025,completed
1005,Priya,North,Laptop,65000,50000,15-03-2025,completed
1006,Ravi,West,Chair,12000,,18-03-2025,completed
1007,Meera,East,Notebook,800,400,20-03-2025,completed
1008,Ravi,West,Laptop,65000,50000,22-03-2025,
1009,Arjun,South,Laptop,65000,50000,25-03-2025,completed
"""

df = pd.read_csv(io.StringIO(raw_data))

# Task 1
print("Shape:", df.shape)
print("\nNulls:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# Task 2
df_clean = df.drop_duplicates().copy()
df_clean["order_date"] = pd.to_datetime(df_clean["order_date"], dayfirst=True, errors="coerce")
df_clean["cost"] = df_clean.groupby("product")["cost"].transform(
    lambda s: s.fillna(s.median())
)
df_clean["status"] = df_clean["status"].fillna("unknown")
df_clean["profit"] = df_clean["revenue"] - df_clean["cost"]

# Task 3
completed = df_clean[df_clean["status"] == "completed"]
top_region = completed.groupby("region")["profit"].sum().idxmax()
top_rep = completed.groupby("rep")["profit"].sum().idxmax()
print(f"\nTop region by profit: {top_region}")
print(f"Top rep by profit: {top_rep}")
```

</details>
