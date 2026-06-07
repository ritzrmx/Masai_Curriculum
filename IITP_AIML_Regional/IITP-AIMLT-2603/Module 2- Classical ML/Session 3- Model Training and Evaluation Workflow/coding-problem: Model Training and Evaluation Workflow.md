# Coding Problem: Model Training and Evaluation Workflow

> **Session 3** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You're building your first ML model to predict whether a bank loan will default. You need to follow the proper workflow: split data, train a baseline, evaluate, and compare models.

---

## Setup

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = {
    "income":      [45000, 32000, 78000, 25000, 95000, 41000, 60000, 28000, 55000, 87000],
    "loan_amount": [10000, 8000, 20000, 5000, 30000, 12000, 15000, 7000, 18000, 25000],
    "credit_score":[650, 580, 720, 540, 780, 630, 700, 560, 690, 740],
    "defaulted":   [0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Train/Test Split**

```python
X = df.drop(columns=["___"])         # fill: target column
y = df["___"]                         # fill: target column

X_train, X_test, y_train, y_test = train_test_split(
    ___, ___, test_size=___, random_state=42   # fill: X, y, 0.2
)

print("Train size:", len(X_train))
print("Test size: ", len(X_test))
```

---

**Task 2 — Baseline Model**

Always start with a baseline — a simple model that makes predictions without learning. If your real model can't beat this, something is wrong.

```python
baseline = DummyClassifier(strategy="___")   # fill: "most_frequent"
baseline.fit(X_train, y_train)
y_pred_base = baseline.predict(___)          # fill: X_test

print("Baseline Accuracy:", accuracy_score(y_test, ___))  # fill: y_pred_base
```

---

**Task 3 — Real Model**

```python
model = DecisionTreeClassifier(max_depth=___, random_state=42)  # fill: 3
model.fit(___, ___)                                              # fill: X_train, y_train
y_pred = model.predict(___)                                      # fill: X_test

print("Model Accuracy:", accuracy_score(___, ___))              # fill: y_test, y_pred
```

---

**Task 4 — Comparison Table**

```python
results = {
    "Baseline": accuracy_score(y_test, y_pred_base),
    "Decision Tree": accuracy_score(y_test, y_pred),
}

for name, score in results.items():
    print(f"{name}: {score:.2f}")

# Is the Decision Tree better than the baseline?
# If not, what might be wrong?
```

---

## Key Takeaways

- Always split data **before** any fitting — the test set must stay unseen
- A **DummyClassifier** is your minimum bar — beat it or re-examine your approach
- Accuracy alone can mislead on imbalanced data — we'll see better metrics soon
