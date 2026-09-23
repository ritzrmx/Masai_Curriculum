# Coding Problem: ML Workflow & Problem Framing
> **Session 1 — Module 2: Classical ML** | ⏱ 5 mins

---

## Scenario

You're given a small customer dataset and asked to set up an honest evaluation workflow before any modeling.

---

## Tasks

**Task 1 — Basic**

Load the data and separate features from target:

```python
import pandas as pd

data = {
    "age": [25, 45, 35, 50, 23, 41, 33, 60],
    "monthly_spend": [20, 80, 40, 95, 15, 70, 38, 100],
    "churned": [1, 0, 1, 0, 1, 0, 1, 0],
}
df = pd.DataFrame(data)

X = df.drop(columns=["___"])
y = df["___"]
print(X.shape, y.shape)
```

**Task 2 — Basic**

Split into train/test with stratification:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=___, random_state=42, stratify=___
)
print(X_train.shape, X_test.shape)
```

**Task 3 — Mid**

Run 4-fold cross-validation on a baseline classifier and print the mean accuracy:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

model = LogisticRegression()
scores = cross_val_score(model, X_train, y_train, cv=___, scoring="___")
print(f"Mean CV accuracy: {scores.mean():.3f}")
```

---

## Expected Output

```
(8, 2) (8,)
(6, 2) (2, 2)
Mean CV accuracy: 1.000
```

*(Exact CV score depends on the tiny toy dataset and fold split.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression

data = {
    "age": [25, 45, 35, 50, 23, 41, 33, 60],
    "monthly_spend": [20, 80, 40, 95, 15, 70, 38, 100],
    "churned": [1, 0, 1, 0, 1, 0, 1, 0],
}
df = pd.DataFrame(data)

X = df.drop(columns=["churned"])
y = df["churned"]
print(X.shape, y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print(X_train.shape, X_test.shape)

model = LogisticRegression()
scores = cross_val_score(model, X_train, y_train, cv=3, scoring="accuracy")
print(f"Mean CV accuracy: {scores.mean():.3f}")
```
</details>
