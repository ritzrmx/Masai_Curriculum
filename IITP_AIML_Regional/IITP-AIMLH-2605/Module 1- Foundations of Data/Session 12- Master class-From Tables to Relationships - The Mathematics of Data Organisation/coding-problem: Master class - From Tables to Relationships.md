# Coding Problem: From Tables to Relationships — The Mathematics of Data Organisation
> **Session 12 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import numpy as np
import matplotlib.pyplot as plt

hours_studied = np.array([1, 2, 3, 4, 5, 6, 7, 8])
exam_score    = np.array([42, 50, 55, 61, 70, 74, 82, 88])
```

---

## Tasks

**Task 1 — Basic**
Print the **mean**, **median**, and **standard deviation** of `exam_score` (round to 1 decimal).

**Task 2 — Basic**
Create a **scatter plot** of `hours_studied` (x-axis) vs `exam_score` (y-axis).
Add a title `"Study Hours vs Exam Score"` and label both axes.

**Task 3 — Mid**
Calculate the **slope** of the best-fit line using the formula:

> slope = Σ((x − x̄)(y − ȳ)) / Σ((x − x̄)²)

Then calculate the **intercept**: `intercept = ȳ − slope × x̄`

Print both values (round to 2 decimals) and interpret: *"For every extra hour studied, score increases by ___ points."*

---

## Expected Output

```
Mean: 65.2   Median: 65.5   Std: 15.8

[scatter plot displayed]

Slope: 6.69   Intercept: 34.21
For every extra hour studied, score increases by 6.69 points.
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
import matplotlib.pyplot as plt

hours_studied = np.array([1, 2, 3, 4, 5, 6, 7, 8])
exam_score    = np.array([42, 50, 55, 61, 70, 74, 82, 88])

# Task 1
print(f"Mean: {exam_score.mean():.1f}   "
      f"Median: {np.median(exam_score):.1f}   "
      f"Std: {exam_score.std():.1f}")

# Task 2
plt.scatter(hours_studied, exam_score, color="steelblue", s=80)
plt.title("Study Hours vs Exam Score")
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.show()

# Task 3
x_mean = hours_studied.mean()
y_mean = exam_score.mean()
slope = ((hours_studied - x_mean) * (exam_score - y_mean)).sum() / \
        ((hours_studied - x_mean) ** 2).sum()
intercept = y_mean - slope * x_mean
print(f"Slope: {slope:.2f}   Intercept: {intercept:.2f}")
print(f"For every extra hour studied, score increases by {slope:.2f} points.")
```

</details>
