# Coding Problem: Linear Regression and Model Interpretation

> **Session 4** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You're predicting employee salaries based on years of experience, age, and training hours. After training, you must interpret what the model learned — not just the accuracy.

---

## Setup

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

data = {
    "experience_yrs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "age":            [23, 25, 27, 28, 30, 32, 35, 37, 40, 42],
    "training_hrs":   [10, 20, 15, 30, 25, 40, 35, 50, 45, 60],
    "salary":         [30000, 36000, 42000, 48000, 54000,
                       62000, 70000, 79000, 88000, 98000]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Split and Train**

```python
X = df.drop(columns=["___"])               # fill: salary
y = df["___"]                               # fill: salary

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.___(X_train, y_train)                # fill: fit
```

---

**Task 2 — Predict and Evaluate**

```python
y_pred = model.___(X_test)                 # fill: predict

print("R² score:", round(r2_score(___, ___), 3))  # fill: y_test, y_pred

# R² interpretation:
# 1.0 = perfect, 0.0 = no better than predicting the mean, <0 = worse than mean
```

---

**Task 3 — Interpret Coefficients**

```python
coef_df = pd.DataFrame({
    "Feature":     X.___,                  # fill: columns
    "Coefficient": model.___               # fill: coef_
}).sort_values("Coefficient", ascending=False)

print(coef_df)
print("\nIntercept:", model.___)           # fill: intercept_
```

> **Question:** Which feature has the most influence on salary? Does the direction (positive/negative) make real-world sense?

---

**Task 4 — Make a Prediction**

A new employee has 5 years experience, is 31 years old, and did 28 training hours. Predict their salary.

```python
new_employee = pd.DataFrame({
    "experience_yrs": [___],    # fill: 5
    "age":            [___],    # fill: 31
    "training_hrs":   [___]     # fill: 28
})

predicted_salary = model.predict(___)[0]    # fill: new_employee
print(f"Predicted salary: ₹{predicted_salary:,.0f}")
```

---

**Task 5 — Overfitting Check**

```python
train_r2 = r2_score(y_train, model.predict(X_train))
test_r2  = r2_score(y_test,  model.predict(X_test))

print(f"Train R²: {train_r2:.3f}")
print(f"Test  R²: {test_r2:.3f}")

# If Train R² >> Test R², what does that indicate?
```

---

## Key Takeaways

- Each **coefficient** tells you: for every 1-unit increase in that feature, salary changes by that amount (holding others constant)
- **Intercept** = predicted value when all features are 0
- A large gap between train and test R² signals **overfitting**
