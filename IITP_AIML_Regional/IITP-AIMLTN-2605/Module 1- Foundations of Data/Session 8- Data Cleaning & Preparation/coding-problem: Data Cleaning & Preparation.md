# Coding Problem: Data Cleaning & Preparation
> **Session 8 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

A messy employee export with duplicates, missing values, and mixed date formats:

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Bob", "Charlie", "Diana"],
    "department": ["HR", "Tech", "Tech", "Sales", "HR"],
    "salary":     [52000, 85000, 85000, None, 48000],
    "rating":     [4, 5, 5, 3, None],
    "join_date":  ["01-03-2025", "05-03-2025", "05-03-2025", "10/03/2025", "2025-03-15"]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Print the **number of nulls per column** and the **count of duplicate rows**.

**Task 2 — Basic**
Drop duplicate rows, fill missing `salary` with the **column median**, and fill missing `rating` with `3`.

**Task 3 — Mid**
Convert `join_date` to datetime (`dayfirst=True`), then print the **average salary by department** (rounded to 0 decimals).

---

## Expected Output

```
Nulls per column:
name          0
department    0
salary        1
rating        1
join_date     0

Duplicate rows: 1

Average salary by department:
department
HR         50000.0
Sales      52000.0
Tech       85000.0
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Bob", "Charlie", "Diana"],
    "department": ["HR", "Tech", "Tech", "Sales", "HR"],
    "salary":     [52000, 85000, 85000, None, 48000],
    "rating":     [4, 5, 5, 3, None],
    "join_date":  ["01-03-2025", "05-03-2025", "05-03-2025", "10/03/2025", "2025-03-15"]
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
df["join_date"] = pd.to_datetime(df["join_date"], dayfirst=True, errors="coerce")
avg_salary = df.groupby("department")["salary"].mean().round(0)
print("\nAverage salary by department:")
print(avg_salary)
```

</details>
