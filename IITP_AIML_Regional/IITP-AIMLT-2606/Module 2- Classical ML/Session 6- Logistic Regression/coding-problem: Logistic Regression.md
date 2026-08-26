# Coding Problem: Logistic Regression
> **Session 6 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Train a logistic regression classifier on `loan_applications.csv`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("loan_applications.csv")
X = df[["age", "income_k", "credit_score", "loan_amount_k"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = ___(max_iter=1000)
model.fit(___, ___)
print(model.predict(X_test))
```

**Task 2 — Basic**

Print predicted probabilities:

```python
probs = model.predict_proba(X_test)
print(probs)
print(probs[:, 1])  # probability of approval (class 1)
```

**Task 3 — Mid**

Apply a custom threshold of 0.7 and compare predicted positive counts to the default:

```python
import numpy as np

default_preds = model.predict(X_test)
custom_preds = (probs[:, 1] >= ___).astype(int)

print("Default approvals:", default_preds.sum())
print("Custom (0.7) approvals:", custom_preds.sum())
```

---

## Expected Output

```
[...predicted labels...]
[[... , ...] ...]
[...probabilities of class 1...]
Default approvals: ...
Custom (0.7) approvals: ...
```

*(Exact values depend on the fitted model on this dataset; custom threshold count should be <= default count since 0.7 > 0.5.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("loan_applications.csv")
X = df[["age", "income_k", "credit_score", "loan_amount_k"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print(model.predict(X_test))

probs = model.predict_proba(X_test)
print(probs)
print(probs[:, 1])

default_preds = model.predict(X_test)
custom_preds = (probs[:, 1] >= 0.7).astype(int)

print("Default approvals:", default_preds.sum())
print("Custom (0.7) approvals:", custom_preds.sum())
```
</details>
