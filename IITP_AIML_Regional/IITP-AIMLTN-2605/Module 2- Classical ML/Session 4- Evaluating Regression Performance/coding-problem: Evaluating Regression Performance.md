# Coding Problem: Evaluating Regression Performance
> **Session 4 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

Actual house prices (in lakhs INR) for 8 houses, and predictions from two competing models:

```python
import numpy as np

actual       = np.array([45, 55, 60, 70, 80, 95, 110, 130])
model_a_pred = np.array([47, 52, 63, 68, 78, 99, 105, 128])
model_b_pred = np.array([40, 48, 58, 79, 68, 108, 95, 150])
```

---

## Tasks

**Task 1 — Basic**
For both `model_a_pred` and `model_b_pred`, compute **MAE**, **RMSE**, and **R²** against `actual` using `sklearn.metrics`. Round MAE and RMSE to 2 decimals, R² to 3 decimals.

**Task 2 — Basic**
Compute the **residuals** (`actual - predicted`) for both models and print them as lists. Then print each model's **residual standard deviation**, rounded to 2 decimals.

**Task 3 — Mid**
Find each model's **maximum absolute error**, then decide which model is better based on **lower RMSE and tighter (lower std) residuals**. Print the name of the better model.

---

## Expected Output

```
Model A -> MAE: 2.88  RMSE: 3.06  R2: 0.987
Model B -> MAE: 10.38  RMSE: 11.71  R2: 0.816

Model A residuals: [-2, 3, -3, 2, 2, -4, 5, 2]
Model B residuals: [5, 7, 2, -9, 12, -13, 15, -20]
Model A residual std: 3.0
Model B residual std: 11.71

Model A max abs error: 5
Model B max abs error: 20

Better model (lower RMSE, tighter residuals): Model A
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

actual       = np.array([45, 55, 60, 70, 80, 95, 110, 130])
model_a_pred = np.array([47, 52, 63, 68, 78, 99, 105, 128])
model_b_pred = np.array([40, 48, 58, 79, 68, 108, 95, 150])

# Task 1
mae_a = round(mean_absolute_error(actual, model_a_pred), 2)
rmse_a = round(root_mean_squared_error(actual, model_a_pred), 2)
r2_a = round(r2_score(actual, model_a_pred), 3)

mae_b = round(mean_absolute_error(actual, model_b_pred), 2)
rmse_b = round(root_mean_squared_error(actual, model_b_pred), 2)
r2_b = round(r2_score(actual, model_b_pred), 3)

print(f"Model A -> MAE: {mae_a}  RMSE: {rmse_a}  R2: {r2_a}")
print(f"Model B -> MAE: {mae_b}  RMSE: {rmse_b}  R2: {r2_b}")

# Task 2
resid_a = actual - model_a_pred
resid_b = actual - model_b_pred
print("\nModel A residuals:", resid_a.tolist())
print("Model B residuals:", resid_b.tolist())
print("Model A residual std:", round(resid_a.std(), 2))
print("Model B residual std:", round(resid_b.std(), 2))

# Task 3
max_err_a = round(np.max(np.abs(resid_a)), 2)
max_err_b = round(np.max(np.abs(resid_b)), 2)
print("\nModel A max abs error:", max_err_a)
print("Model B max abs error:", max_err_b)

better = "Model A" if rmse_a < rmse_b else "Model B"
print(f"\nBetter model (lower RMSE, tighter residuals): {better}")
```

</details>
