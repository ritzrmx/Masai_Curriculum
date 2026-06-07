# Coding Problem: Introduction to Machine Learning and Problem Framing

> **Session 1** | ⏱ 10 mins | Module 2: Classical ML

---

## Scenario

You are a data analyst at an e-commerce company. Your manager wants to use ML to solve two business problems. Your job: frame each problem correctly and explore the dataset before any model is built.

---

## Dataset

```python
import pandas as pd

data = {
    "customer_id":    [1, 2, 3, 4, 5, 6, 7, 8],
    "age":            [25, 34, 45, 28, 52, 38, 29, 41],
    "total_spend":    [1200, 3400, 800, 5600, 2100, 990, 4300, 670],
    "num_orders":     [3, 8, 2, 12, 5, 3, 10, 2],
    "days_inactive":  [5, 2, 30, 1, 14, 22, 3, 45],
    "churned":        [0, 0, 1, 0, 0, 1, 0, 1]   # 1 = churned
}

df = pd.DataFrame(data)
print(df)
```

---

## Tasks

**Task 1 — Problem Framing**

Answer these questions in comments (no code needed):

```python
# Problem A: Predict whether a customer will churn (churned = 1 or 0)
# - Task type: ___ (regression / classification)
# - Features (X): ___
# - Target (y): ___

# Problem B: Predict how much a new customer will spend next month
# - Task type: ___ (regression / classification)
# - Features (X): ___
# - Target (y): ___
```

---

**Task 2 — Dataset Exploration**

Fill in the blanks to explore the dataset.

```python
# Shape of the dataset
print("Rows, Cols:", df.___)         # fill: shape

# Check for missing values
print(df.___)                         # fill: isnull().sum()

# Basic statistics
print(df.___)                         # fill: describe()

# Churn rate
churn_rate = df["churned"].___ / len(df)   # fill: sum()
print(f"Churn rate: {churn_rate:.0%}")
```

---

**Task 3 — Feature vs Target Split**

Separate features (X) and target (y) for the churn problem.

```python
X = df.drop(columns=["___", "___"])   # fill: drop customer_id and churned
y = df["___"]                          # fill: target column

print("Features:", X.___)             # fill: columns attribute
print("Target samples:", y.___)       # fill: values attribute
```

---

**Task 4 — Learning Type Identification**

```python
scenarios = {
    "Predict house price":              "___",   # regression / classification
    "Group customers by behaviour":     "___",   # supervised / unsupervised
    "Detect fraudulent transaction":    "___",   # regression / classification
    "Forecast next month's sales":      "___",   # regression / classification
}

for task, answer in scenarios.items():
    print(f"{task}: {answer}")
```

---

## Key Takeaways

- Always define your target variable before touching the data or picking a model
- Supervised learning needs labelled data (y column); unsupervised doesn't
- Regression → continuous output; Classification → categorical output
