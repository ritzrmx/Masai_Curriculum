# Coding Problem: Classification Foundations
> **Session 6 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A food-delivery company has logged 24 orders. For each, they recorded the rider's
**distance** and the restaurant's **prep time**, and whether the order arrived **late**
(`1`) or **on time** (`0`).

```python
import pandas as pd

data = {
    "distance_km":   [1.2, 2.0, 1.5, 3.0, 2.4, 4.1, 3.6, 2.8, 5.0, 4.5,
                      6.2, 5.5, 7.0, 6.6, 4.8, 8.5, 9.0, 7.2, 10.1, 8.8,
                      9.6, 7.9, 8.1, 10.5],
    "prep_time_min": [10, 12, 8, 15, 11, 30, 9, 14, 34, 13,
                      18, 33, 16, 31, 12, 32, 28, 35, 30, 15,
                      38, 27, 33, 36],
    "late":          [0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                      0, 1, 1, 1, 0, 1, 1, 1, 1, 0,
                      1, 1, 1, 1],
}
df = pd.DataFrame(data)

X = df[["distance_km", "prep_time_min"]]
y = df["late"]
```

---

## Tasks

**Task 1 — Basic**
Split the data with `test_size=0.25`, `random_state=42` and `stratify=y`. Then build a pipeline of `StandardScaler` + `LogisticRegression(random_state=42)`, fit it on the training set, and print the **test accuracy** rounded to 2 decimals.

**Task 2 — Basic**
For the **first 3 orders in the test set**, print the model's **probability of being late** (from `predict_proba`) next to its hard `predict` label. Note which of the three the model was least confident about.

**Task 3 — Mid**
Two parts, both on the same training set:
**(a)** Fit a `DecisionTreeClassifier(max_depth=2, random_state=42)`. Print its test accuracy, then use `feature_importances_` to print **which single feature the tree relied on most**.
**(b)** Fit a scaled `KNeighborsClassifier(n_neighbors=1)` and print **both its train and its test accuracy**. Explain in a comment why the train accuracy is what it is.

---

## Expected Output

```
Logistic Regression test accuracy: 0.83

First 3 test orders:
  order 0: P(late) = 0.93  ->  predict = 1
  order 1: P(late) = 0.32  ->  predict = 0
  order 2: P(late) = 0.16  ->  predict = 0

Decision Tree test accuracy: 0.83
Tree split on: prep_time_min

KNN k=1 train accuracy: 1.00
KNN k=1 test  accuracy: 0.83
```

Order 1 is the least confident call — at 0.32 it is far closer to the 0.5 threshold than the other two.

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

data = {
    "distance_km":   [1.2, 2.0, 1.5, 3.0, 2.4, 4.1, 3.6, 2.8, 5.0, 4.5,
                      6.2, 5.5, 7.0, 6.6, 4.8, 8.5, 9.0, 7.2, 10.1, 8.8,
                      9.6, 7.9, 8.1, 10.5],
    "prep_time_min": [10, 12, 8, 15, 11, 30, 9, 14, 34, 13,
                      18, 33, 16, 31, 12, 32, 28, 35, 30, 15,
                      38, 27, 33, 36],
    "late":          [0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                      0, 1, 1, 1, 0, 1, 1, 1, 1, 0,
                      1, 1, 1, 1],
}
df = pd.DataFrame(data)

X = df[["distance_km", "prep_time_min"]]
y = df["late"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# --- Task 1: Logistic Regression baseline ---
logreg = make_pipeline(StandardScaler(), LogisticRegression(random_state=42))
logreg.fit(X_train, y_train)
print(f"Logistic Regression test accuracy: {logreg.score(X_test, y_test):.2f}")

# --- Task 2: predict vs predict_proba ---
probs = logreg.predict_proba(X_test)[:3]   # column 1 = P(late)
preds = logreg.predict(X_test)[:3]
print("\nFirst 3 test orders:")
for i in range(3):
    print(f"  order {i}: P(late) = {probs[i][1]:.2f}  ->  predict = {preds[i]}")

# --- Task 3a: Decision Tree + which feature it leaned on ---
tree = DecisionTreeClassifier(max_depth=2, random_state=42)
tree.fit(X_train, y_train)
print(f"\nDecision Tree test accuracy: {tree.score(X_test, y_test):.2f}")
importances = pd.Series(tree.feature_importances_, index=X.columns)
print(f"Tree split on: {importances.idxmax()}")

# --- Task 3b: KNN with k=1 ---
knn1 = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1))
knn1.fit(X_train, y_train)
print(f"\nKNN k=1 train accuracy: {knn1.score(X_train, y_train):.2f}")
print(f"KNN k=1 test  accuracy: {knn1.score(X_test, y_test):.2f}")

# Why is train accuracy exactly 1.00?
# With k=1, the single nearest neighbour of any training point IS that point itself
# (distance zero), so it always votes for its own label. The model has memorised the
# training set, not learnt a pattern. A perfect training score here is a warning sign,
# not an achievement — only the TEST score tells you anything.
```

</details>
