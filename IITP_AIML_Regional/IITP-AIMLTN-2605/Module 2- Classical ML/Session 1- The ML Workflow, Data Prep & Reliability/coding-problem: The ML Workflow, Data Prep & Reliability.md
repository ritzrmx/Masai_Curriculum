# Coding Problem: The ML Workflow, Data Prep & Reliability
> **Session 1 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

Sixteen used two-wheelers listed on a resale portal. You want to predict the **resale price (₹)**.

```python
import pandas as pd

bikes = pd.DataFrame({
    "age_years":         [1, 3, 5, 2, 7, 4, 6, 1, 8, 3, 5, 2, 9, 4, 6, 2],
    "km_driven":         [4000, 21000, 38000, 12000, 55000, 30000, 46000, 6500,
                          62000, 18000, 41000, 9000, 70000, 26000, 49000, 15000],
    "engine_cc":         [150, 125, 110, 200, 100, 150, 125, 220, 100, 160, 110, 180, 100, 150, 125, 200],
    "services_done":     [2, 5, 8, 3, 11, 6, 9, 1, 13, 4, 8, 3, 14, 7, 10, 4],
    "dealer_commission": [5850, 3425, 2825, 6525, 1600, 4300, 2450, 7525,
                          1175, 5725, 2750, 6000, 925, 4275, 2600, 6525],
    "price":             [117000, 68500, 56500, 130500, 32000, 86000, 49000, 150500,
                          23500, 114500, 55000, 120000, 18500, 85500, 52000, 130500],
})
```

> The dealer takes a flat 5% commission on every sale.

---

## Tasks

**Task 1 — Basic**
Separate the data into features `X` and target `y`. The target is `price`. Print the shape of each.

**Task 2 — Basic**
Split `X` and `y` into a training set and a test set using `test_size=0.25` and `random_state=42`. Print how many rows ended up in each.

**Task 3 — Mid**
Fit a `LinearRegression` on the training set and print the **test MAE**. Then look hard at the feature list: **one column is a data leak**. Identify it, drop it, re-split, re-fit, and print the test MAE again. Which of the two models would you actually deploy, and why?

---

## Expected Output

```
X shape: (16, 5)
y shape: (16,)
Training rows: 12 | Test rows: 4

MAE with dealer_commission   : 0
MAE without dealer_commission: 4,737
```

The first model is off by ₹0 on every test bike — a perfect score. It is also useless: `dealer_commission` is 5% of `price`, so it hands the model the answer. On a bike that has not sold yet, there is no commission to look up.

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

bikes = pd.DataFrame({
    "age_years":         [1, 3, 5, 2, 7, 4, 6, 1, 8, 3, 5, 2, 9, 4, 6, 2],
    "km_driven":         [4000, 21000, 38000, 12000, 55000, 30000, 46000, 6500,
                          62000, 18000, 41000, 9000, 70000, 26000, 49000, 15000],
    "engine_cc":         [150, 125, 110, 200, 100, 150, 125, 220, 100, 160, 110, 180, 100, 150, 125, 200],
    "services_done":     [2, 5, 8, 3, 11, 6, 9, 1, 13, 4, 8, 3, 14, 7, 10, 4],
    "dealer_commission": [5850, 3425, 2825, 6525, 1600, 4300, 2450, 7525,
                          1175, 5725, 2750, 6000, 925, 4275, 2600, 6525],
    "price":             [117000, 68500, 56500, 130500, 32000, 86000, 49000, 150500,
                          23500, 114500, 55000, 120000, 18500, 85500, 52000, 130500],
})

# --- Task 1: features (X) and target (y) ---
X = bikes.drop(columns=["price"])
y = bikes["price"]
print("X shape:", X.shape)
print("y shape:", y.shape)

# --- Task 2: hold out a test set BEFORE doing anything else ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print(f"Training rows: {len(X_train)} | Test rows: {len(X_test)}")
print()

# --- Task 3a: fit with the leaky column still in ---
leaky = LinearRegression().fit(X_train, y_train)
mae_leaky = mean_absolute_error(y_test, leaky.predict(X_test))
print(f"MAE with dealer_commission   : {mae_leaky:,.0f}")

# --- Task 3b: dealer_commission = 5% of price -> it IS the target. Drop it. ---
X_clean = X.drop(columns=["dealer_commission"])
Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    X_clean, y, test_size=0.25, random_state=42
)
honest = LinearRegression().fit(Xc_train, yc_train)
mae_honest = mean_absolute_error(yc_test, honest.predict(Xc_test))
print(f"MAE without dealer_commission: {mae_honest:,.0f}")

# Deploy the SECOND model. The first scores perfectly only because it can read
# the answer off dealer_commission — a value that does not exist until the bike
# has already been sold. A worse score on honest features beats a perfect score
# on a leak, every time.
```

</details>
