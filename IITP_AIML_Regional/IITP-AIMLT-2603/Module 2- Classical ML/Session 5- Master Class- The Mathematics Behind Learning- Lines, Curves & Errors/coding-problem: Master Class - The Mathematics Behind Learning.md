# Coding Problem: Master Class — The Mathematics Behind Learning

> **Session 5** | ⏱ 10 mins | Module 2: Classical ML

---

## Scenario

This Master Class focuses on building intuition for the mathematics behind linear regression — specifically: what a line is, what a residual is, and how gradient descent finds the best line by minimising errors. No heavy formulas — just visualisation and hands-on calculation.

---

## Setup

```python
import numpy as np
import matplotlib.pyplot as plt
```

---

## Dataset

```python
# Study hours vs exam score
hours = np.array([1, 2, 3, 4, 5, 6, 7, 8])
scores = np.array([40, 50, 55, 60, 65, 70, 78, 85])
```

---

## Tasks

**Task 1 — Plot the Data**

```python
plt.scatter(hours, scores, color="steelblue", s=80)
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.title("Study Hours vs Score")
plt.show()
```

> Does the relationship look linear? Would a straight line fit well?

---

**Task 2 — Draw a Line (y = mx + c)**

Given the line `score = 6 * hours + 34`, draw it over the scatter plot.

```python
m = ___   # fill: slope (6)
c = ___   # fill: intercept (34)

x_line = np.linspace(1, 8, 100)
y_line = ___ * x_line + ___     # fill: m, c

plt.scatter(hours, scores, color="steelblue", s=80, label="Data")
plt.plot(x_line, y_line, color="red", label=f"y = {m}x + {c}")
plt.legend()
plt.title("Fitting a Line")
plt.show()
```

---

**Task 3 — Calculate Residuals**

A **residual** is the gap between the actual value and the line's prediction.

```python
y_pred = m * hours + c                    # predictions from our line

residuals = scores - ___                  # fill: y_pred
print("Residuals:", residuals)

# Plot residuals as vertical lines
plt.scatter(hours, scores, color="steelblue", s=80)
plt.plot(x_line, y_line, color="red")
for i in range(len(hours)):
    plt.plot([hours[i], hours[i]], [y_pred[i], scores[i]], color="gray", linestyle="--")
plt.title("Residuals (gaps between line and points)")
plt.show()
```

---

**Task 4 — Mean Squared Error**

MSE measures how large the residuals are on average (squared to penalise big errors more).

```python
mse = np.mean(residuals ___ 2)       # fill: ** (exponentiation)
print(f"MSE with m={m}, c={c}: {mse:.2f}")

# Now try m=5, c=38 — does MSE go up or down?
m2, c2 = 5, 38
residuals2 = scores - (m2 * hours + c2)
mse2 = np.mean(residuals2 ** 2)
print(f"MSE with m={m2}, c={c2}: {mse2:.2f}")
```

> Which line gives a lower MSE? That's the "better" line — gradient descent finds it automatically.

---

**Task 5 — Gradient Descent Intuition (Manual)**

Manually try 3 slopes and find the one with the lowest MSE.

```python
slopes = [4, 6, 8]
intercept = 34

for slope in ___:                          # fill: slopes
    preds = slope * hours + intercept
    mse_val = np.mean((scores - preds) ** 2)
    print(f"slope={slope}, MSE={mse_val:.2f}")

# Which slope minimises the error? That's what gradient descent discovers.
```

---

## Key Takeaways

- A line y = mx + c has two knobs: **slope** (m) and **intercept** (c)
- **Residuals** are the vertical gaps between predictions and actual values
- **MSE** measures overall error — the lower, the better
- Gradient descent finds m and c that minimise MSE — it's just "walking downhill"
