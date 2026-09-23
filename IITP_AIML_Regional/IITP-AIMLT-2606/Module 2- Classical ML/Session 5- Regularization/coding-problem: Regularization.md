# Coding Problem: Regularization
> **Session 5 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Train a baseline `LinearRegression` and a `Ridge` on `housing_multicollinear.csv`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge

df = pd.read_csv("housing_multicollinear.csv")
X = df[["sqft", "num_rooms", "age_years", "distance_center_km"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

baseline = LinearRegression().fit(X_train, y_train)
ridge = Ridge(alpha=___).fit(X_train, y_train)
print("Baseline R2:", baseline.score(X_test, y_test))
print("Ridge R2:", ridge.score(X_test, y_test))
```

**Task 2 — Basic**

Train a `Lasso` and count non-zero coefficients:

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=___).fit(X_train, y_train)
non_zero = sum(c != 0 for c in lasso.coef_)
print("Lasso R2:", lasso.score(X_test, y_test))
print("Non-zero coefficients:", non_zero)
```

**Task 3 — Mid**

Sweep several alpha values for Ridge using cross-validation and print the best one:

```python
from sklearn.model_selection import cross_val_score

alphas = [0.001, 0.01, 0.1, 1, 10, 100]
best_alpha, best_score = None, -float("inf")
for a in alphas:
    scores = cross_val_score(Ridge(alpha=a), X_train, y_train, cv=5, scoring="r2")
    mean_score = scores.mean()
    if mean_score > best_score:
        best_alpha, best_score = a, mean_score
print(f"Best alpha: {best_alpha}, CV R2: {best_score:.3f}")
```

---

## Expected Output

```
Baseline R2: ...
Ridge R2: ...
Lasso R2: ...
Non-zero coefficients: ...
Best alpha: ..., CV R2: ...
```

*(Exact values depend on the fitted model on this dataset and the alpha grid.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso

df = pd.read_csv("housing_multicollinear.csv")
X = df[["sqft", "num_rooms", "age_years", "distance_center_km"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

baseline = LinearRegression().fit(X_train, y_train)
ridge = Ridge(alpha=1.0).fit(X_train, y_train)
print("Baseline R2:", baseline.score(X_test, y_test))
print("Ridge R2:", ridge.score(X_test, y_test))

lasso = Lasso(alpha=0.5).fit(X_train, y_train)
non_zero = sum(c != 0 for c in lasso.coef_)
print("Lasso R2:", lasso.score(X_test, y_test))
print("Non-zero coefficients:", non_zero)

alphas = [0.001, 0.01, 0.1, 1, 10, 100]
best_alpha, best_score = None, -float("inf")
for a in alphas:
    scores = cross_val_score(Ridge(alpha=a), X_train, y_train, cv=5, scoring="r2")
    mean_score = scores.mean()
    if mean_score > best_score:
        best_alpha, best_score = a, mean_score
print(f"Best alpha: {best_alpha}, CV R2: {best_score:.3f}")
```
</details>
