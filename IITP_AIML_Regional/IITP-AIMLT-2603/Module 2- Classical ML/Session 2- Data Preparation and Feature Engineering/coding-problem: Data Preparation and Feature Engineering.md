# Coding Problem: Data Preparation and Feature Engineering

> **Session 2** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You have a raw dataset of job applicants. Before building any model, you need to clean and prepare it: handle missing values, encode categories, scale numbers, and engineer a new feature.

---

## Dataset

```python
import pandas as pd
import numpy as np

data = {
    "applicant_id": [1, 2, 3, 4, 5, 6],
    "age":          [28, None, 35, 42, 29, None],
    "city":         ["Mumbai", "Delhi", "Mumbai", "Delhi", "Bengaluru", "Mumbai"],
    "experience":   [3, 7, None, 12, 2, 5],
    "education":    ["Low", "High", "Medium", "High", "Low", "Medium"],
    "hired":        [1, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)
print(df)
```

---

## Tasks

**Task 1 — Handle Missing Values**

```python
# Fill missing 'age' with the median age
df["age"] = df["age"].fillna(df["age"].___())    # fill: median

# Fill missing 'experience' with the mean
df["experience"] = df["experience"].fillna(df["experience"].___())   # fill: mean

print(df[["age", "experience"]])
```

---

**Task 2 — Remove Duplicates**

```python
print("Duplicates before:", df.___(). ___())    # fill: duplicated().sum()
df = df.drop_duplicates()
print("Duplicates after:", df.duplicated().sum())
```

---

**Task 3 — Encode Categorical Variables**

```python
from sklearn.preprocessing import LabelEncoder

# One-hot encode 'city' (nominal — no order)
df = pd.get_dummies(df, columns=["___"], drop_first=True)   # fill: city

# Label encode 'education' (ordinal — Low < Medium < High)
order_map = {"Low": ___, "Medium": ___, "High": ___}        # fill: 0, 1, 2
df["education"] = df["education"].map(order_map)

print(df.head())
```

---

**Task 4 — Feature Scaling**

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
cols_to_scale = ["age", "experience"]

df[cols_to_scale] = scaler.fit_transform(df[___])   # fill: cols_to_scale

print(df[["age", "experience"]].round(2))
# Expected: mean ≈ 0, values spread around 0
```

---

**Task 5 — Feature Engineering**

Create a new feature `experience_per_year_of_age` that captures relative experience.

```python
# Un-scale the original values first (use the raw df) OR
# Just create from the raw values before scaling if run separately
df_raw = pd.DataFrame(data).fillna({"age": 31.5, "experience": 5.8})

df_raw["exp_per_age"] = df_raw["___"] / df_raw["___"]   # fill: experience / age
print(df_raw[["age", "experience", "exp_per_age"]].round(3))
```

---

## Key Takeaways

- Missing values must be handled before any model — `fillna()` with mean/median/mode
- Use **one-hot encoding** for unordered categories, **label encoding** for ordered ones
- Scale numeric features so no single column dominates by size
