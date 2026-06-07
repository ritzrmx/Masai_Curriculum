# Coding Problem: Regularization Techniques

> **Session 7** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

Your linear regression model performs well on training data but poorly on test data — a sign of overfitting. You'll apply Ridge and Lasso regularization and compare them against the plain model.

---

## Setup

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

np.random.seed(42)
n = 100
X = pd.DataFrame({
    "feature_1": np.random.randn(n),
    "feature_2": np.random.randn(n),
    "feature_3": np.random.randn(n),
    "feature_4": np.random.randn(n) * 0.01,   # near-useless feature
    "feature_5": np.random.randn(n) * 0.01,   # near-useless feature
})
y = 3*X["feature_1"] + 2*X["feature_2"] - X["feature_3"] + np.random.randn(n)*0.5
```

---

## Tasks

**Task 1 — Split and Scale**

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(___)    # fill: X_train
X_test_s  = scaler.transform(___)        # fill: X_test
```

---

**Task 2 — Train Three Models**

```python
models = {
    "Linear Regression": LinearRegression(),
    "Ridge (α=1.0)":     Ridge(alpha=___),     # fill: 1.0
    "Lasso (α=0.1)":     Lasso(alpha=___),     # fill: 0.1
}

results = {}
for name, model in models.items():
    model.fit(X_train_s, y_train)
    train_r2 = r2_score(y_train, model.predict(X_train_s))
    test_r2  = r2_score(y_test,  model.predict(X_test_s))
    results[name] = {"Train R²": round(train_r2, 3), "Test R²": round(test_r2, 3)}

print(pd.DataFrame(results).T)
```

---

**Task 3 — Compare Coefficients**

```python
coef_df = pd.DataFrame(index=X.columns)

for name, model in models.items():
    coef_df[name] = model.coef_

print(coef_df.round(3))
```

> **Questions:**
> - Which model drives `feature_4` and `feature_5` closest to zero?
> - Does Lasso zero out any coefficients completely? (This is **feature selection**.)

---

**Task 4 — Hyperparameter Tuning**

Try different `alpha` values for Ridge and observe the test R².

```python
alphas = [0.01, 0.1, 1.0, 10.0, 100.0]

for alpha in ___:                                    # fill: alphas
    r = Ridge(alpha=alpha)
    r.fit(X_train_s, y_train)
    test_r2 = r2_score(y_test, r.predict(___))       # fill: X_test_s
    print(f"Ridge α={alpha}: Test R²={test_r2:.3f}")

# Which alpha value gives the best test R²?
```

---

## Key Takeaways

- **Ridge** shrinks all coefficients towards zero but keeps them all — reduces overfitting
- **Lasso** can drive coefficients to exactly zero — acts as automatic feature selection
- Always scale features before regularization — otherwise `alpha` affects features unequally
