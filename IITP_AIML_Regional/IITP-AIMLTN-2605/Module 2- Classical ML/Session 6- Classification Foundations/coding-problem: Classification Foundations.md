# Coding Problem: Classification Foundations
> **Session 6 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A small study-habits dataset — hours studied and practice tests taken, and whether the student passed:

```python
import pandas as pd

data = {
    "study_hours":    [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9],
    "practice_tests": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
    "passed":         [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Split into train/test sets (`test_size=0.25`, `random_state=42`, `stratify=y`) using `study_hours` and `practice_tests` as features and `passed` as the target. Print the train and test set sizes.

**Task 2 — Basic**
Fit a `LogisticRegression` on the training set. Print its **predictions** and **predicted probabilities of passing** on the test set, rounded to 3 decimals, plus its **accuracy**.

**Task 3 — Mid**
Fit a `DecisionTreeClassifier` (`max_depth=2`, `random_state=42`) on the same split. Print its **predictions**, **accuracy**, and its **feature importances**.

---

## Expected Output

```
Train size: 9 Test size: 3

Logistic Regression predictions: [0, 1, 1]
Logistic Regression P(pass): [0.283, 0.974, 0.997]
Logistic Regression accuracy: 1.0

Decision Tree predictions: [0, 1, 1]
Decision Tree accuracy: 1.0

Decision Tree feature importances: {'study_hours': 1.0, 'practice_tests': 0.0}
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = {
    "study_hours":    [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9],
    "practice_tests": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
    "passed":         [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1]
}
df = pd.DataFrame(data)

X = df[["study_hours", "practice_tests"]]
y = df["passed"]

# Task 1
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("Train size:", len(X_train), "Test size:", len(X_test))

# Task 2
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
log_preds = logreg.predict(X_test)
log_proba = logreg.predict_proba(X_test)[:, 1]
log_acc = accuracy_score(y_test, log_preds)

print("\nLogistic Regression predictions:", log_preds.tolist())
print("Logistic Regression P(pass):", log_proba.round(3).tolist())
print("Logistic Regression accuracy:", round(log_acc, 4))

# Task 3
tree = DecisionTreeClassifier(max_depth=2, random_state=42)
tree.fit(X_train, y_train)
tree_preds = tree.predict(X_test)
tree_acc = accuracy_score(y_test, tree_preds)

print("\nDecision Tree predictions:", tree_preds.tolist())
print("Decision Tree accuracy:", round(tree_acc, 4))

importances = {col: float(val) for col, val in zip(X.columns, tree.feature_importances_.round(3))}
print("\nDecision Tree feature importances:", importances)
```

</details>
