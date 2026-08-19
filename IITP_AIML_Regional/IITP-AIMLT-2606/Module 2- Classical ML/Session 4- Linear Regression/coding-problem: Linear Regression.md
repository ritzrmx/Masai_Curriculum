# Coding Problem: Linear Regression
> **Session 4 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Train a `LinearRegression` model:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.DataFrame({
    "sqft": [800, 1200, 1500, 2000, 2500, 900, 1700, 2200],
    "bedrooms": [2, 3, 3, 4, 4, 2, 3, 4],
    "price_lakhs": [40, 65, 78, 105, 130, 45, 88, 115],
})
X = df[["sqft", "bedrooms"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = ___()
model.fit(___, ___)
```

**Task 2 — Basic**

Evaluate with MAE, RMSE, R²:

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)
print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.3f}")
```

**Task 3 — Mid**

Print coefficients and compare train vs test R²:

```python
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.3f}")

print(f"Train R2: {model.score(X_train, y_train):.3f}")
print(f"Test R2: {model.score(X_test, y_test):.3f}")
```

---

## Expected Output

```
MAE: ...
RMSE: ...
R2: ...
sqft: ...
bedrooms: ...
Train R2: ...
Test R2: ...
```

*(Exact numbers depend on the fitted model on this toy dataset — values will be printed, not fixed constants.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.DataFrame({
    "sqft": [800, 1200, 1500, 2000, 2500, 900, 1700, 2200],
    "bedrooms": [2, 3, 3, 4, 4, 2, 3, 4],
    "price_lakhs": [40, 65, 78, 105, 130, 45, 88, 115],
})
X = df[["sqft", "bedrooms"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)
print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.3f}")

for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.3f}")

print(f"Train R2: {model.score(X_train, y_train):.3f}")
print(f"Test R2: {model.score(X_test, y_test):.3f}")
```
</details>
