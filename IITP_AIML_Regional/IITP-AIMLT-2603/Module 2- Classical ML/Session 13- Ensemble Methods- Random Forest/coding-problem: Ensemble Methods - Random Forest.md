# Coding Problem: Ensemble Methods — Random Forest

> **Session 13** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

A single Decision Tree is fragile — small changes in data can produce a very different tree. Random Forest builds many trees and votes, making it far more robust. You'll compare the two and explore feature importance.

---

## Setup

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(
    n_samples=500, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)
feature_names = [f"feature_{i}" for i in range(10)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

---

## Tasks

**Task 1 — Decision Tree vs Random Forest**

```python
dt = DecisionTreeClassifier(random_state=42)
rf = RandomForestClassifier(n_estimators=___, random_state=42)   # fill: 100

dt.fit(___, ___)    # fill: X_train, y_train
rf.fit(___, ___)    # fill: X_train, y_train

print("Decision Tree:")
print(f"  Train: {accuracy_score(y_train, dt.predict(X_train)):.3f}")
print(f"  Test:  {accuracy_score(y_test,  dt.predict(X_test)):.3f}")

print("Random Forest:")
print(f"  Train: {accuracy_score(y_train, rf.predict(X_train)):.3f}")
print(f"  Test:  {accuracy_score(y_test,  rf.predict(X_test)):.3f}")
```

> Which model overfits more? Why does Random Forest generalise better?

---

**Task 2 — Feature Importance**

```python
importances = rf.feature_importances_

feat_df = pd.DataFrame({
    "Feature":    feature_names,
    "Importance": ___             # fill: importances
}).sort_values("Importance", ascending=False)

print(feat_df)

# Plot
feat_df.plot(kind="bar", x="Feature", y="Importance", legend=False, figsize=(9,4))
plt.title("Random Forest Feature Importance")
plt.ylabel("Importance Score")
plt.tight_layout()
plt.show()
```

> The dataset has 5 informative features and 5 noise features. Does the importance plot reflect this?

---

**Task 3 — Effect of n_estimators**

```python
for n_trees in [1, 5, 10, 50, 100, 200]:
    rf_n = RandomForestClassifier(n_estimators=___, random_state=42)   # fill: n_trees
    rf_n.fit(X_train, y_train)
    test_acc = accuracy_score(y_test, rf_n.predict(X_test))
    print(f"n_estimators={n_trees:3d}: Test accuracy = {test_acc:.3f}")
```

> At what point does adding more trees stop helping? This is the **diminishing returns** of ensembles.

---

**Task 4 — Model Robustness**

Run the Decision Tree 5 times with different random seeds. Compare variance.

```python
dt_scores = []
for seed in range(5):
    dt_s = DecisionTreeClassifier(random_state=___)    # fill: seed
    dt_s.fit(X_train, y_train)
    dt_scores.append(accuracy_score(y_test, dt_s.predict(X_test)))

print("DT scores across seeds:", [round(s,3) for s in dt_scores])
print("DT std dev:", round(np.std(dt_scores), 4))
# Random Forest is stable because it averages many trees — try it too
```

---

## Key Takeaways

- Random Forest = many trees trained on random data subsets and random feature subsets, then **majority vote**
- **Feature importance** shows which features the forest relied on most — useful for feature selection
- More trees → more stable, but returns diminish after ~100; training time increases linearly
