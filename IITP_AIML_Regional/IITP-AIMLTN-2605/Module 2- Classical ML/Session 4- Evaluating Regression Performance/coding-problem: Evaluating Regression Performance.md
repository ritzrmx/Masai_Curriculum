# Coding Problem: Evaluating Regression Performance
> **Session 4 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

Ten flats in Bengaluru. `area_sqft` is the only feature; `price_lakh` is the target (₹ lakh).

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = {
    "area_sqft":  [ 600,  850, 1100, 1250, 1400, 1600, 1850, 2100, 2300, 2500],
    "price_lakh": [  42,   55,   68,   71,   84,   90,  108,  115,  132,  138],
}
df = pd.DataFrame(data)

X = df[["area_sqft"]]
y = df["price_lakh"]
```

---

## Tasks

**Task 1 — Basic**
Fit a `LinearRegression` on `X` and `y`, predict on `X`, then compute the **residuals** (`y_true - y_pred`) and print the first three, rounded to 2 decimals.

**Task 2 — Basic**
Using `sklearn.metrics`, print the model's **MAE**, **RMSE** and **R²**. (Get RMSE with `np.sqrt(mean_squared_error(...))`.)

**Task 3 — Mid**
Fit a `DummyRegressor(strategy="mean")` baseline on the same data and print **its** MAE and R². Then print how many ₹ lakh of average error your real model *saves* compared to the baseline.

---

## Expected Output

```
First 3 residuals: [0.65, 0.83, 1.02]

Model    -> MAE: 2.0x | RMSE: 2.3x | R²: 0.99x
Baseline -> MAE: 26.3x | R²: 0.000

Model beats baseline by 24.3x lakh of average error
```

*(Note: the baseline's R² is exactly `0.000`. That is not a coincidence — "always predict the mean" is the definition of R² = 0.)*

---

<details>
<summary>Solution</summary>

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = {
    "area_sqft":  [ 600,  850, 1100, 1250, 1400, 1600, 1850, 2100, 2300, 2500],
    "price_lakh": [  42,   55,   68,   71,   84,   90,  108,  115,  132,  138],
}
df = pd.DataFrame(data)

X = df[["area_sqft"]]
y = df["price_lakh"]

# --- Task 1: fit, predict, residuals ---
model = LinearRegression().fit(X, y)
y_pred = model.predict(X)
residuals = y - y_pred                     # the atom of every metric
print("First 3 residuals:", residuals.head(3).round(2).tolist())

# --- Task 2: the metric report card ---
mae  = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))   # sqrt puts us back in ₹ lakh
r2   = r2_score(y, y_pred)
print(f"\nModel    -> MAE: {mae:.2f} | RMSE: {rmse:.2f} | R²: {r2:.3f}")

# --- Task 3: the baseline, and what we gain over it ---
baseline  = DummyRegressor(strategy="mean").fit(X, y)
base_pred = baseline.predict(X)

base_mae = mean_absolute_error(y, base_pred)
base_r2  = r2_score(y, base_pred)
print(f"Baseline -> MAE: {base_mae:.2f} | R²: {base_r2:.3f}")

print(f"\nModel beats baseline by {base_mae - mae:.2f} lakh of average error")
```

</details>
