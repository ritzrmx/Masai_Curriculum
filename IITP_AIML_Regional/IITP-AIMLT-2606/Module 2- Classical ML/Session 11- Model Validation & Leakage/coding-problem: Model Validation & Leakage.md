# Coding Problem: Model Validation & Leakage
> **Session 11 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Run 5-fold stratified cross-validation:

```python
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({
    "age": [45, 34, 33, 37, 28, 60, 50, 42, 39, 55, 30, 47],
    "num_visits": [2, 0, 5, 5, 1, 3, 2, 4, 1, 3, 0, 2],
    "readmitted": [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
})
X = df[["age", "num_visits"]]
y = df["readmitted"]

pipe = Pipeline([("scaler", ___()), ("model", ___(max_iter=1000))])
skf = ___(n_splits=___, shuffle=True, random_state=42)

scores = cross_val_score(___, X, y, cv=___, scoring="accuracy")
print(scores, scores.mean())
```

**Task 2 — Basic**

Tune `C` with `GridSearchCV`:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {"model__C": [0.1, 1, 10]}
grid = GridSearchCV(pipe, param_grid, cv=skf, scoring="accuracy")
grid.fit(X, y)
print("Best params:", grid.best_params_)
print("Best CV score:", grid.best_score_)
```

**Task 3 — Mid**

Demonstrate leakage by adding a proxy feature and comparing scores:

```python
df["staff_flag"] = df["readmitted"]  # deliberately leaky: literally copies the target
X_leak = df[["age", "num_visits", "staff_flag"]]

scores_leak = cross_val_score(pipe, X_leak, y, cv=skf, scoring="accuracy")
scores_clean = cross_val_score(pipe, X, y, cv=skf, scoring="accuracy")
print("With leakage:", scores_leak.mean())
print("Without leakage:", scores_clean.mean())
```

---

## Expected Output

```
[...] ...
Best params: {...}
Best CV score: ...
With leakage: ...
Without leakage: ...
```

*(Exact numbers depend on the fitted model on this toy dataset — values will be printed, not fixed constants.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({
    "age": [45, 34, 33, 37, 28, 60, 50, 42, 39, 55, 30, 47],
    "num_visits": [2, 0, 5, 5, 1, 3, 2, 4, 1, 3, 0, 2],
    "readmitted": [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
})
X = df[["age", "num_visits"]]
y = df["readmitted"]

pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))])
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(pipe, X, y, cv=skf, scoring="accuracy")
print(scores, scores.mean())

param_grid = {"model__C": [0.1, 1, 10]}
grid = GridSearchCV(pipe, param_grid, cv=skf, scoring="accuracy")
grid.fit(X, y)
print("Best params:", grid.best_params_)
print("Best CV score:", grid.best_score_)

df["staff_flag"] = df["readmitted"]
X_leak = df[["age", "num_visits", "staff_flag"]]

scores_leak = cross_val_score(pipe, X_leak, y, cv=skf, scoring="accuracy")
scores_clean = cross_val_score(pipe, X, y, cv=skf, scoring="accuracy")
print("With leakage:", scores_leak.mean())
print("Without leakage:", scores_clean.mean())
```
</details>
