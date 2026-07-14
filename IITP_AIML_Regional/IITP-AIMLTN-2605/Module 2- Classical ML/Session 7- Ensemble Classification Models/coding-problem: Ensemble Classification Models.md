# Coding Problem: Ensemble Classification Models
> **Session 7 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

Six features. Only **three** of them actually carry signal — the other three are pure noise. Your forest has to figure out which is which, without being told.

```python
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=400, n_features=6, n_informative=3,
    n_redundant=0, n_classes=2, random_state=42
)

cols = ["f1", "f2", "f3", "f4", "f5", "f6"]
df = pd.DataFrame(X, columns=cols)
df["target"] = y

X_train, X_test, y_train, y_test = train_test_split(
    df[cols], df["target"], test_size=0.25, random_state=42, stratify=df["target"]
)
```

---

## Tasks

**Task 1 — Basic**
Train a `DecisionTreeClassifier(random_state=42)` with **no depth limit** on the training set. Print its **train** accuracy and its **test** accuracy, each rounded to 3 decimals.

**Task 2 — Basic**
Train a `RandomForestClassifier` with `n_estimators=200` and `random_state=42` on the same training set. Print its test accuracy, rounded to 3 decimals.

**Task 3 — Mid**
Two parts.
**(a)** Print how many accuracy points the forest gained over the single tree on the **test** set.
**(b)** Print the forest's **top 3 features** by `feature_importances_`, sorted highest first. Then answer in a comment: did the forest correctly identify 3 informative features out of the 6?

---

## Expected Output

```
Tree  — train: 1.000  test: 0.8x
Forest — test: 0.8x

Gain from ensembling: +0.0x

Top 3 features by importance:
f1    0.4xx
f3    0.1xx
f6    0.1xx
```

The tree's train accuracy will be **exactly 1.000** — it memorised every training row. Its test accuracy will be several points lower. The forest closes part of that gap. The three noise columns should each land near 0.05, far below the top three.

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = make_classification(
    n_samples=400, n_features=6, n_informative=3,
    n_redundant=0, n_classes=2, random_state=42
)

cols = ["f1", "f2", "f3", "f4", "f5", "f6"]
df = pd.DataFrame(X, columns=cols)
df["target"] = y

X_train, X_test, y_train, y_test = train_test_split(
    df[cols], df["target"], test_size=0.25, random_state=42, stratify=df["target"]
)

# --- Task 1: one deep tree — low bias, high variance ---
tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
tree_test = tree.score(X_test, y_test)
print(f"Tree  — train: {tree.score(X_train, y_train):.3f}  test: {tree_test:.3f}")

# --- Task 2: 200 trees, each on a bootstrap sample with random feature subsets ---
forest = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
forest_test = forest.score(X_test, y_test)
print(f"Forest — test: {forest_test:.3f}")

# --- Task 3a: the variance reduction, in accuracy points ---
print(f"\nGain from ensembling: +{forest_test - tree_test:.3f}")

# --- Task 3b: which columns did the forest actually lean on? ---
importances = (
    pd.Series(forest.feature_importances_, index=cols)
    .sort_values(ascending=False)
)
print("\nTop 3 features by importance:")
print(importances.head(3).round(3))

# Yes — the top 3 scores are far above the rest, and the bottom 3 columns
# all sit near 0.05. The forest found the 3 informative features on its own.
# Reminder: high importance means the model USED it, not that it CAUSES the label.
```

</details>
