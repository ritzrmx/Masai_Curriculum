# Coding Problem: Model Selection, Persistence & Module Review
> **Session 12 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A synthetic loan-approval dataset: 400 applicants, 8 features, and a yes-or-no target (`1` = approved).

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=400, n_features=8, n_informative=4,
    n_redundant=0, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
```

The test set is now locked away. It does **not** participate in any decision until the very last step.

---

## Tasks

**Task 1 — Basic**
Build a `Pipeline` with two steps: a `StandardScaler` named `"scaler"`, then a `LogisticRegression(max_iter=1000, random_state=42)` named `"model"`.

**Task 2 — Basic**
Wrap that pipeline in a `GridSearchCV` that searches `C` over `[0.01, 0.1, 1, 10, 100]`, with `cv=5` and `scoring="accuracy"`. Fit it on the **training data only** and print `best_params_` and `best_score_`.

**Task 3 — Mid**
Two parts:
- (a) Take `best_estimator_` and score it **once** on the untouched test set. Print the test accuracy.
- (b) `joblib.dump` the **whole pipeline** to `loan_pipeline.joblib`, load it back with `joblib.load`, and print its prediction for the first row of `X_test`.

> ⚠️ Watch the grid key. It is `"model__C"` — the step name, **two** underscores, then the hyperparameter.

---

## Expected Output

```
Best params: {'model__C': 10}
Best CV accuracy: 0.7x
Test accuracy: 0.7x

Reloaded pipeline — prediction for first test applicant: 1
Reloaded predictions match original: True
```

---

<details>
<summary>Solution</summary>

```python
import joblib
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ---- Data: split first, test set locked away -----------------------------
X, y = make_classification(
    n_samples=400, n_features=8, n_informative=4,
    n_redundant=0, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ---- Task 1: the Pipeline ------------------------------------------------
# The scaler lives INSIDE the pipeline, so cross-validation refits it
# separately in every fold. No leakage.
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=1000, random_state=42)),
])

# ---- Task 2: tune on the TRAINING data only ------------------------------
param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}   # note: model__C
search = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy")
search.fit(X_train, y_train)

print("Best params:", search.best_params_)
print("Best CV accuracy:", round(search.best_score_, 3))

# ---- Task 3a: score ONCE on the untouched test set -----------------------
best_pipeline = search.best_estimator_          # scaler + tuned model together
test_acc = accuracy_score(y_test, best_pipeline.predict(X_test))
print("Test accuracy:", round(test_acc, 3))

# ---- Task 3b: persist the WHOLE pipeline, then reload it -----------------
joblib.dump(best_pipeline, "loan_pipeline.joblib")
reloaded = joblib.load("loan_pipeline.joblib")

print("\nReloaded pipeline — prediction for first test applicant:",
      reloaded.predict(X_test[:1])[0])
print("Reloaded predictions match original:",
      (reloaded.predict(X_test) == best_pipeline.predict(X_test)).all())
```

**Why we saved `best_estimator_` and not `best_estimator_.named_steps["model"]`:** saving only the `LogisticRegression` would throw away the scaler. The reloaded model would then receive raw, unscaled data — and it would return confident, wrong predictions **without raising a single error**.

</details>
