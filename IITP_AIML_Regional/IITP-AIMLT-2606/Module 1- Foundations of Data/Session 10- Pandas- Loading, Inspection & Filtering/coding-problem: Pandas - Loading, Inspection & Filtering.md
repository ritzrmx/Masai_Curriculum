# Coding Problem: Pandas — Data Loading & Selection
> **Session 10 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance"],
    "salary":     [52000, 85000, 91000, 48000, 73000],
    "experience": [3, 6, 8, 2, 5]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Print the **shape**, **column names**, and the **first 3 rows** of `df`.

**Task 2 — Basic**
Select and print only the `name` and `salary` columns.

**Task 3 — Mid**
Filter and print all employees from the **Tech department** with a **salary above 88,000**.

---

## Expected Output

```
Shape: (5, 4)
Columns: ['name', 'department', 'salary', 'experience']

      name  department  salary  experience
0    Alice          HR   52000           3
1      Bob        Tech   85000           6
2  Charlie        Tech   91000           8

      name  salary
0    Alice   52000
1      Bob   85000
2  Charlie   91000
3    Diana   48000
4      Eve   73000

      name department  salary  experience
2  Charlie       Tech   91000           8
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance"],
    "salary":     [52000, 85000, 91000, 48000, 73000],
    "experience": [3, 6, 8, 2, 5]
}
df = pd.DataFrame(data)

# Task 1
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head(3))

# Task 2
print(df[["name", "salary"]])

# Task 3
print(df[(df["department"] == "Tech") & (df["salary"] > 88000)])
```

</details>
