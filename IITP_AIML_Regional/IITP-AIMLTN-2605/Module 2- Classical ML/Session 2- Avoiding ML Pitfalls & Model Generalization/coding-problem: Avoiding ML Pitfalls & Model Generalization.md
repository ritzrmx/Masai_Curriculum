# Coding Problem: Avoiding ML Pitfalls & Model Generalization
> **Session 2 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A small student pass/fail dataset. `certificate_issued` is a **leaky feature** — in the real world it is only recorded *after* a student's pass/fail status is already decided.

```python
import pandas as pd

data = {
    "study_hours":        [2, 8, 6, 4, 1, 7, 4, 8, 4, 6, 2, 5, 1, 7, 1, 7, 7, 5, 8, 6,
                            8, 7, 9, 1, 1, 6, 7, 7, 8, 4, 8, 5, 2, 3, 8, 6, 8, 9, 8, 3],
    "attendance_pct":     [72, 67, 55, 92, 97, 72, 51, 64, 65, 79, 94, 41, 43, 49, 41, 91, 59, 49, 43, 41,
                            91, 94, 46, 84, 87, 97, 95, 84, 94, 94, 54, 60, 75, 84, 72, 49, 46, 88, 66, 83],
    "prev_score":         [48, 41, 79, 41, 83, 40, 38, 80, 36, 71, 77, 47, 38, 70, 76, 72, 80, 72, 52, 91,
                            67, 82, 35, 56, 74, 32, 73, 44, 52, 34, 84, 78, 88, 79, 36, 43, 53, 88, 91, 50],
    "certificate_issued": [0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                            1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    "passed":             [0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,
                            1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Print the count and percentage of each class in `passed` (use `value_counts()`).

**Task 2 — Basic**
Run `cross_val_score` (`cv=5`) with a `LogisticRegression` twice: once using all four features (including `certificate_issued`), and once using only `study_hours`, `attendance_pct`, `prev_score`. Print the mean accuracy for both and note which one is inflated by leakage.

**Task 3 — Mid**
Using only the clean features (`study_hours`, `attendance_pct`, `prev_score`), split the data with `train_test_split(test_size=0.3, random_state=42, stratify=y)`. Fit two `DecisionTreeClassifier(random_state=42)` models — one with `max_depth=None`, one with `max_depth=2` — and print train vs test accuracy for each to diagnose which one overfits.

---

## Expected Output

```
Class balance of 'passed':
passed
0    20
1    20
Name: count, dtype: int64
passed
0    50.0
1    50.0
Name: proportion, dtype: float64

CV accuracy WITH certificate_issued: [1.    1.    0.875 0.875 0.875] mean: 0.925
CV accuracy WITHOUT certificate_issued: [0.625 0.75  0.75  0.75  0.625] mean: 0.7

DecisionTree (unlimited) -> train acc: 1.000, test acc: 0.667

DecisionTree (max_depth=2) -> train acc: 0.857, test acc: 0.750
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

data = {
    "study_hours":        [2, 8, 6, 4, 1, 7, 4, 8, 4, 6, 2, 5, 1, 7, 1, 7, 7, 5, 8, 6,
                            8, 7, 9, 1, 1, 6, 7, 7, 8, 4, 8, 5, 2, 3, 8, 6, 8, 9, 8, 3],
    "attendance_pct":     [72, 67, 55, 92, 97, 72, 51, 64, 65, 79, 94, 41, 43, 49, 41, 91, 59, 49, 43, 41,
                            91, 94, 46, 84, 87, 97, 95, 84, 94, 94, 54, 60, 75, 84, 72, 49, 46, 88, 66, 83],
    "prev_score":         [48, 41, 79, 41, 83, 40, 38, 80, 36, 71, 77, 47, 38, 70, 76, 72, 80, 72, 52, 91,
                            67, 82, 35, 56, 74, 32, 73, 44, 52, 34, 84, 78, 88, 79, 36, 43, 53, 88, 91, 50],
    "certificate_issued": [0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                            1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    "passed":             [0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0,
                            1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
}
df = pd.DataFrame(data)

# Task 1
print("Class balance of 'passed':")
print(df["passed"].value_counts())
print(df["passed"].value_counts(normalize=True).round(2) * 100)

# Task 2
y = df["passed"]
leaky_features = ["study_hours", "attendance_pct", "prev_score", "certificate_issued"]
clean_features = ["study_hours", "attendance_pct", "prev_score"]

scores_leaky = cross_val_score(LogisticRegression(max_iter=1000), df[leaky_features], y, cv=5)
scores_clean = cross_val_score(LogisticRegression(max_iter=1000), df[clean_features], y, cv=5)
print("\nCV accuracy WITH certificate_issued:", scores_leaky.round(3), "mean:", round(scores_leaky.mean(), 3))
print("CV accuracy WITHOUT certificate_issued:", scores_clean.round(3), "mean:", round(scores_clean.mean(), 3))

# Task 3
X_train, X_test, y_train, y_test = train_test_split(
    df[clean_features], y, test_size=0.3, random_state=42, stratify=y
)
for depth, label in [(None, "unlimited"), (2, "max_depth=2")]:
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    clf.fit(X_train, y_train)
    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)
    print(f"\nDecisionTree ({label}) -> train acc: {train_acc:.3f}, test acc: {test_acc:.3f}")
```

</details>
