# Coding Problem: Model Validation and Data Issues

> **Session 10** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

Your model shows great training accuracy but poor real-world results. You'll investigate cross-validation, data leakage, and class imbalance — the three silent killers of ML models.

---

## Setup

```python
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report

np.random.seed(42)
n = 200
X = np.random.randn(n, 4)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# Imbalanced version: 90% class 0, 10% class 1
y_imb = np.zeros(n, dtype=int)
y_imb[:20] = 1  # only 20 positives
```

---

## Tasks

**Task 1 — Cross-Validation**

A single train/test split can be lucky or unlucky. Cross-validation gives a more reliable estimate.

```python
model = DecisionTreeClassifier(max_depth=3, random_state=42)

# 5-fold cross-validation
cv_scores = cross_val_score(model, X, y, cv=___, scoring="accuracy")  # fill: 5
print("CV Scores:", cv_scores.round(3))
print(f"Mean: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

---

**Task 2 — Data Leakage Demo**

Leakage = the model sees future/target information during training.

```python
df = pd.DataFrame(X, columns=["f1","f2","f3","f4"])
df["target"] = y

# LEAKY: include a feature derived from the target
df["leaky_feature"] = df["target"] * 10 + np.random.randn(n) * 0.1

X_leak = df.drop(columns=["___"])            # fill: "target"
X_clean = df.drop(columns=["target", "___"]) # fill: "leaky_feature"

for name, features in [("Leaky", X_leak), ("Clean", X_clean)]:
    Xtr, Xte, ytr, yte = train_test_split(features, y, test_size=0.2, random_state=42)
    m = DecisionTreeClassifier(max_depth=3).fit(Xtr, ytr)
    print(f"{name} model test accuracy: {m.score(Xte, yte):.3f}")
```

> Why does the leaky model score so much higher? Would this score hold in production?

---

**Task 3 — Class Imbalance**

```python
from sklearn.utils import class_weight

# Naive model on imbalanced data
Xtr, Xte, ytr, yte = train_test_split(X, y_imb, test_size=0.2, random_state=42)

naive = DecisionTreeClassifier(max_depth=3).fit(Xtr, ytr)
print("Naive accuracy:", naive.score(Xte, yte))
print(classification_report(yte, naive.predict(Xte)))

# Balanced model — give more weight to the minority class
balanced = DecisionTreeClassifier(max_depth=3, class_weight="___")  # fill: "balanced"
balanced.fit(Xtr, ytr)
print("\nBalanced accuracy:", balanced.score(Xte, yte))
print(classification_report(yte, balanced.predict(Xte)))
```

> Does the balanced model improve recall for class 1 (the minority)?

---

**Task 4 — Reliable Evaluation Rule**

```python
# Always: fit preprocessing on TRAIN only, apply to TEST
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_s = scaler.___(Xtr)     # fill: fit_transform (learns mean/std from train)
X_test_s  = scaler.___(Xte)     # fill: transform only (applies train stats to test)

# Why is scaler.fit_transform(X_test) wrong?
```

---

## Key Takeaways

- **Cross-validation** gives more reliable accuracy than a single split
- **Data leakage** inflates scores — always verify no future/target info leaks into features
- **Class imbalance** makes accuracy misleading — use `class_weight="balanced"` or check recall
