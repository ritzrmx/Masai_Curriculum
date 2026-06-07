# Coding Problem: Regression Evaluation and Error Analysis

> **Session 6** | ⏱ 10 mins | Module 2: Classical ML

---

## Scenario

You've trained a model to predict apartment rental prices. Now you need to evaluate it properly — not just with one metric, but with MAE, RMSE, and R² — and understand what each one tells you.

---

## Setup

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Actual vs predicted rent (₹ per month)
y_true = np.array([15000, 22000, 18000, 30000, 12000, 25000, 20000, 35000])
y_pred = np.array([14000, 24000, 17500, 28000, 13500, 26000, 19000, 32000])
```

---

## Tasks

**Task 1 — Calculate MAE**

MAE = average of |actual − predicted|. It tells you how far off you are on average, in original units.

```python
mae = mean_absolute_error(___, ___)    # fill: y_true, y_pred
print(f"MAE: ₹{mae:,.0f}")

# Manually verify for the first two rows:
manual_mae_2 = (abs(y_true[0] - y_pred[0]) + abs(y_true[1] - y_pred[1])) / 2
print(f"Manual MAE (2 samples): ₹{manual_mae_2:,.0f}")
```

---

**Task 2 — Calculate RMSE**

RMSE penalises large errors more than MAE does.

```python
mse  = mean_squared_error(___, ___)    # fill: y_true, y_pred
rmse = np.___(mse)                     # fill: sqrt

print(f"MSE:  {mse:,.0f}")
print(f"RMSE: ₹{rmse:,.0f}")

# Is RMSE larger or smaller than MAE here? Why?
```

---

**Task 3 — Calculate R²**

R² tells you what proportion of the variance in the target the model explains.

```python
r2 = r2_score(___, ___)    # fill: y_true, y_pred
print(f"R²: {r2:.4f}")

# Interpret the result:
# R² > 0.9 → excellent
# R² 0.7–0.9 → good
# R² < 0.5 → poor — consider better features or model
```

---

**Task 4 — Error Analysis**

Identify which predictions had the largest absolute errors.

```python
import pandas as pd

errors = pd.DataFrame({
    "actual":    y_true,
    "predicted": y_pred,
    "abs_error": np.abs(___ - ___)    # fill: y_true, y_pred
}).sort_values("abs_error", ascending=False)

print(errors)

# Which apartment had the worst prediction?
# What business impact could a ₹3000 error in rent prediction have?
```

---

**Task 5 — Metric Comparison Table**

```python
metrics = {
    "MAE":  round(mae, 0),
    "RMSE": round(rmse, 0),
    "R²":   round(r2, 4)
}

for metric, value in metrics.items():
    print(f"{metric}: {value}")

# Fill in the blank:
# RMSE > MAE because RMSE ___ large errors more heavily.
```

---

## Key Takeaways

- **MAE** = average error in original units — easy to explain to stakeholders
- **RMSE** = punishes large outlier errors more — use when big mistakes are costly
- **R²** = proportion of variance explained — higher is better, max is 1.0
