# Coding Problem: Regression Models & Regularization
> **Session 3 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A small study-hours vs. exam-score dataset:

```python
import pandas as pd

data = {
    "study_hours": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "exam_score":  [35, 42, 48, 55, 58, 64, 70, 75, 80, 88]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Fit a `LinearRegression` model with `study_hours` as the feature and `exam_score` as the target. Print the **slope (`coef_`)** and **intercept**, rounded to 3 decimals.

**Task 2 — Basic**
Using the fitted model, predict the exam score for a student who studied **9.5 hours**. Round to 2 decimals.

**Task 3 — Mid**
Fit `Ridge(alpha=1)` and `Ridge(alpha=50)` on the same data. Print all three slopes (plain `LinearRegression`, `Ridge(alpha=1)`, `Ridge(alpha=50)`) side by side and observe how the slope shrinks as `alpha` increases.

---

## Expected Output

```
Slope (coef_): 5.63
Intercept: 24.903

Predicted score for 9.5 study hours: 78.39

Coefficient comparison:
LinearRegression coef_: 5.63
Ridge(alpha=1) coef_:   5.563
Ridge(alpha=50) coef_:  3.506
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge

data = {
    "study_hours": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "exam_score":  [35, 42, 48, 55, 58, 64, 70, 75, 80, 88]
}
df = pd.DataFrame(data)

# Task 1
X = df[["study_hours"]]
y = df["exam_score"]

model = LinearRegression()
model.fit(X, y)

print("Slope (coef_):", round(model.coef_[0], 3))
print("Intercept:", round(model.intercept_, 3))

# Task 2
pred_9_5 = model.predict(pd.DataFrame({"study_hours": [9.5]}))
print("\nPredicted score for 9.5 study hours:", round(pred_9_5[0], 2))

# Task 3
ridge_low = Ridge(alpha=1)
ridge_low.fit(X, y)

ridge_high = Ridge(alpha=50)
ridge_high.fit(X, y)

print("\nCoefficient comparison:")
print("LinearRegression coef_:", round(model.coef_[0], 3))
print("Ridge(alpha=1) coef_:  ", round(ridge_low.coef_[0], 3))
print("Ridge(alpha=50) coef_: ", round(ridge_high.coef_[0], 3))
```

</details>
