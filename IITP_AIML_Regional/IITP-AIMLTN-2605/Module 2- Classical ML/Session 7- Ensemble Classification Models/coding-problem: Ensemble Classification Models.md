# Coding Problem: Ensemble Classification Models
> **Session 7 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A synthetic binary classification dataset — self-contained, no file or network needed:

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=300, n_features=6, n_informative=4, n_redundant=1,
    n_clusters_per_class=2, random_state=42
)
feature_names = [f"feature_{i}" for i in range(X.shape[1])]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
```

---

## Tasks

**Task 1 — Basic**
Fit a `DecisionTreeClassifier(random_state=42)` and a `RandomForestClassifier(n_estimators=100, random_state=42)` on the training set. Print each model's **test accuracy**, rounded to 3 decimals.

**Task 2 — Basic**
Print the **accuracy improvement** of the forest over the single tree (`forest_acc - tree_acc`, rounded to 3 decimals).

**Task 3 — Mid**
Extract `.feature_importances_` from the fitted forest, rank them, and print the **top 3 features** (rounded to 4 decimals).

---

## Expected Output

```
Single Tree test accuracy: 0.778
Random Forest test accuracy: 0.867

Accuracy improvement (forest - tree): 0.089

Top 3 features by importance:
feature_5    0.3033
feature_4    0.1813
feature_0    0.1708
dtype: float64
```

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
    n_samples=300, n_features=6, n_informative=4, n_redundant=1,
    n_clusters_per_class=2, random_state=42
)
feature_names = [f"feature_{i}" for i in range(X.shape[1])]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Task 1
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
forest = RandomForestClassifier(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)

tree_acc = round(tree.score(X_test, y_test), 3)
forest_acc = round(forest.score(X_test, y_test), 3)
print("Single Tree test accuracy:", tree_acc)
print("Random Forest test accuracy:", forest_acc)

# Task 2
print("\nAccuracy improvement (forest - tree):", round(forest_acc - tree_acc, 3))

# Task 3
importances = pd.Series(forest.feature_importances_, index=feature_names)
top3 = importances.sort_values(ascending=False).head(3)
print("\nTop 3 features by importance:")
print(top3.round(4))
```

</details>
