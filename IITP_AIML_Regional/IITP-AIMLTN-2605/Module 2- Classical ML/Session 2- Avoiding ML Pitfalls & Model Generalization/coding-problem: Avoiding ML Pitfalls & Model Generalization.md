# Coding Problem: Avoiding ML Pitfalls & Model Generalization
> **Session 2 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

40 noisy readings from a sensor. The true underlying pattern is a smooth wave — everything else is noise.

```python
import numpy as np

rng = np.random.RandomState(42)
X = rng.uniform(0, 1, 40).reshape(-1, 1)                      # 40 inputs
y = np.sin(2 * np.pi * X).ravel() + rng.normal(0, 0.3, 40)    # true wave + noise
```

---

## Tasks

**Task 1 — Basic**
Split the data into 75% train and 25% test with `random_state=42`, and print the number of rows in each.

**Task 2 — Basic**
Fit three polynomial models — **degree 1**, **degree 3**, and **degree 10** — on the training set.
For each, print the train R², the test R², and the **gap** (`train - test`), rounded to 2 decimals.
Use `make_pipeline(PolynomialFeatures(degree), LinearRegression())`.

**Task 3 — Mid**
Run **5-fold cross-validation** on the *full* dataset for the same three degrees, using `KFold(n_splits=5, shuffle=True, random_state=42)`.
Print `mean ± std` for each — then print which degree generalises best, and why the *training* score alone would have led you to the wrong answer.

---

## Expected Output

```
Train rows: 30 | Test rows: 10

degree  train R2   test R2    gap
   1       0.47      0.29     0.18   <- underfit: both scores low
   3       0.85      0.80     0.05   <- good fit: small gap
  10       0.93      0.59     0.34   <- overfit: best train, worst gap

5-fold cross-validation (full dataset):
degree  1  ->  R2 = 0.079 ± 0.740
degree  3  ->  R2 = 0.736 ± 0.261
degree 10  ->  R2 = 0.558 ± 0.513

Best generalising degree: 3
Degree 10 had the HIGHEST training score (0.93) but the worst gap.
Training score rewards memorisation, not learning.
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, KFold

# --- Dataset ---
rng = np.random.RandomState(42)
X = rng.uniform(0, 1, 40).reshape(-1, 1)
y = np.sin(2 * np.pi * X).ravel() + rng.normal(0, 0.3, 40)

# --- Task 1: 75 / 25 split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
print(f"Train rows: {len(X_train)} | Test rows: {len(X_test)}\n")

# --- Task 2: fit three complexities, measure the gap ---
degrees = [1, 3, 10]
print("degree  train R2   test R2    gap")
for d in degrees:
    model = make_pipeline(PolynomialFeatures(d), LinearRegression())
    model.fit(X_train, y_train)
    train_r2 = model.score(X_train, y_train)
    test_r2 = model.score(X_test, y_test)
    gap = train_r2 - test_r2
    print(f"  {d:2d}       {train_r2:.2f}      {test_r2:.2f}     {gap:.2f}")

# --- Task 3: 5-fold cross-validation on the full dataset ---
cv = KFold(n_splits=5, shuffle=True, random_state=42)
cv_means = {}

print("\n5-fold cross-validation (full dataset):")
for d in degrees:
    model = make_pipeline(PolynomialFeatures(d), LinearRegression())
    scores = cross_val_score(model, X, y, cv=cv)
    cv_means[d] = scores.mean()
    print(f"degree {d:2d}  ->  R2 = {scores.mean():.3f} ± {scores.std():.3f}")

best = max(cv_means, key=cv_means.get)
print(f"\nBest generalising degree: {best}")
print("Degree 10 had the HIGHEST training score (0.93) but the worst gap.")
print("Training score rewards memorisation, not learning.")
```

</details>
