# Coding Problem: Pandas — Cleaning & Aggregation
> **Session 11 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

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
```

---

## Tasks

**Task 1 — Basic**
Check and print the **number of nulls** in each column and **count of duplicate rows**.

**Task 2 — Basic**
Drop duplicate rows and fill missing `salary` with the **column median**. Fill missing `rating` with `3`.

**Task 3 — Mid**
Group by `department` and print the **average salary** per department, rounded to 0 decimals.

---

## Expected Output

```
Nulls per column:
name          0
department    0
salary        1
rating        1

Duplicate rows: 1

Average salary by department:
department
Finance    73000.0
HR         52000.0
Tech       87000.0
```

---

<details>
<summary>Solution</summary>

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

# Task 1
print("Nulls per column:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# Task 2
df = df.drop_duplicates()
df["salary"] = df["salary"].fillna(df["salary"].median())
df["rating"] = df["rating"].fillna(3)

# Task 3
avg_salary = df.groupby("department")["salary"].mean().round(0)
print("\nAverage salary by department:")
print(avg_salary)
```

</details>
