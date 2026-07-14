# Coding Problem: Regression Models & Regularization
> **Session 3 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A food-delivery service in Bengaluru wants to predict how many **minutes** an order takes, from the trip's distance, the number of pickup stops, and a traffic score from 1 to 10.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge

deliveries = pd.DataFrame({
    "distance_km":   [2, 5, 3, 8, 6, 12, 4, 9, 15, 7, 11, 14, 3, 10, 6, 13],
    "num_stops":     [1, 2, 3, 1, 4,  2, 2, 5,  3, 1,  4,  2, 4,  3, 1,  5],
    "traffic_index": [3, 7, 5, 2, 8,  4, 6, 9,  3, 5,  7,  6, 8,  4, 2,  9],
    "minutes":       [14, 31, 27, 26, 44, 38, 28, 55, 47, 26, 52, 47, 35, 41, 20, 62],
})

X = deliveries[["distance_km", "num_stops", "traffic_index"]]
y = deliveries["minutes"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
```

---

## Tasks

**Task 1 — Basic**
Scale the features with `StandardScaler` (fit on **train only**, then transform both train and test). Fit a `LinearRegression` on the scaled training data, and print the intercept and each feature's coefficient.

**Task 2 — Basic**
Print the model's train and test R² using `.score()`. Check the sign of every coefficient — do they all match what common sense says about delivery time?

**Task 3 — Mid**
Fit a `Ridge` model for each `alpha` in `[0.1, 1, 10, 100]`. For each one, print the **sum of the absolute coefficients** and the **test R²**. Then state which alpha you would choose, and what went wrong at the largest one.

---

## Expected Output

```
--- Task 1: what the model learned ---
intercept     : 40.83
distance_km   : +7.94
num_stops     : +5.54
traffic_index : +3.47

--- Task 2: scores ---
Train R2: 0.992
Test  R2: 0.988

--- Task 3: coefficients shrink as alpha grows ---
alpha=  0.1 | sum |coef| = 16.84 | test R2 =  0.987
alpha=  1.0 | sum |coef| = 15.95 | test R2 =  0.973
alpha= 10.0 | sum |coef| = 10.52 | test R2 =  0.466
alpha=100.0 | sum |coef| =  2.46 | test R2 = -1.636
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge

deliveries = pd.DataFrame({
    "distance_km":   [2, 5, 3, 8, 6, 12, 4, 9, 15, 7, 11, 14, 3, 10, 6, 13],
    "num_stops":     [1, 2, 3, 1, 4,  2, 2, 5,  3, 1,  4,  2, 4,  3, 1,  5],
    "traffic_index": [3, 7, 5, 2, 8,  4, 6, 9,  3, 5,  7,  6, 8,  4, 2,  9],
    "minutes":       [14, 31, 27, 26, 44, 38, 28, 55, 47, 26, 52, 47, 35, 41, 20, 62],
})

X = deliveries[["distance_km", "num_stops", "traffic_index"]]
y = deliveries["minutes"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# --- Task 1: scale (fit on TRAIN only), then fit and read the coefficients ---
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)   # fit + transform on train
X_test_s  = scaler.transform(X_test)        # transform ONLY on test — no leakage

linear = LinearRegression()
linear.fit(X_train_s, y_train)

print("--- Task 1: what the model learned ---")
print(f"intercept     : {linear.intercept_:.2f}")
for name, coef in zip(X.columns, linear.coef_):
    print(f"{name:14s}: {coef:+.2f}")

# --- Task 2: scores ---
print("\n--- Task 2: scores ---")
print(f"Train R2: {linear.score(X_train_s, y_train):.3f}")
print(f"Test  R2: {linear.score(X_test_s,  y_test):.3f}")
# All three coefficients are POSITIVE, which matches common sense:
# a longer trip, more stops, and worse traffic each ADD minutes.

# --- Task 3: watch the coefficients shrink as the penalty grows ---
print("\n--- Task 3: coefficients shrink as alpha grows ---")
for alpha in [0.1, 1, 10, 100]:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_s, y_train)
    total = np.abs(ridge.coef_).sum()
    print(f"alpha={alpha:5.1f} | sum |coef| = {total:5.2f} "
          f"| test R2 = {ridge.score(X_test_s, y_test):6.3f}")

# Which alpha would you choose?
#   alpha = 0.1 — it keeps the best test R2 (~0.99).
#
# What went wrong at alpha = 100?
#   The penalty became so expensive that the model crushed every coefficient
#   toward zero (sum |coef| fell from 16.84 to 2.46). With almost no
#   coefficients left, it can barely use the features at all — so it now
#   predicts worse than simply guessing the average, and test R2 goes
#   NEGATIVE. That is UNDERFITTING: alpha was turned up far too high.
```

</details>
