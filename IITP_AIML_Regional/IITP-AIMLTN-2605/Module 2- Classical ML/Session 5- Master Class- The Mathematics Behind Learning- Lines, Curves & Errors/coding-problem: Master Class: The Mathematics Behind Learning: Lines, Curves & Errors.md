# Coding Problem: Master Class: The Mathematics Behind Learning: Lines, Curves & Errors
> **Session 5 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

House size (in units of 100 sq ft) vs price (in $1000s):

```python
import numpy as np

size = np.array([5, 6, 7, 8, 9, 10])
price = np.array([150, 165, 183, 200, 218, 240])
```

---

## Tasks

**Task 1 — Basic**
Write a function `sse(m, c, x, y)` that returns the **Sum of Squared Errors** for the line `y = mx + c`. Use it to print the SSE for two candidate lines: guess A (`m=20, c=40`) and guess B (`m=25, c=10`).

**Task 2 — Basic**
Fit a `LinearRegression` model on `size` vs `price`. Print the fitted slope and intercept (rounded to 4 decimals), then use your `sse()` function to confirm the fitted line's SSE is lower than **both** guesses from Task 1.

**Task 3 — Mid**
Starting from `m_current = 10.0` and the intercept frozen at the fitted intercept from Task 2, run **6 steps** of gradient descent on `SSE(m)` with `learning_rate = 0.001`. At each step, print the current `m` (rounded to 4 decimals) and its SSE. Use the gradient rule `grad = -2 * sum(x * (y - (m*x + c)))`.

---

## Expected Output

```
SSE for guess A (m=20, c=40): 138
SSE for guess B (m=25, c=10): 1043

Fitted slope (m): 17.8857
Fitted intercept (c): 58.5238
Fitted line SSE: 17.1
Fitted line beats both guesses: True

Gradient descent steps:
step 0: m=10.0, SSE=22092.61
step 1: m=15.5989, SSE=1873.65
step 2: m=17.2225, SSE=173.24
step 3: m=17.6934, SSE=30.24
step 4: m=17.8299, SSE=18.21
step 5: m=17.8695, SSE=17.2

Final m after 6 steps: 17.881
Fitted slope from sklearn: 17.8857
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
from sklearn.linear_model import LinearRegression

size = np.array([5, 6, 7, 8, 9, 10])
price = np.array([150, 165, 183, 200, 218, 240])

def sse(m, c, x, y):
    pred = m * x + c
    return np.round(np.sum((y - pred) ** 2), 2)

# Task 1
sse_a = sse(20, 40, size, price)
sse_b = sse(25, 10, size, price)
print("SSE for guess A (m=20, c=40):", sse_a)
print("SSE for guess B (m=25, c=10):", sse_b)

# Task 2
model = LinearRegression()
model.fit(size.reshape(-1, 1), price)
m_fit = round(model.coef_[0], 4)
c_fit = round(model.intercept_, 4)
sse_fit = sse(m_fit, c_fit, size, price)
print("\nFitted slope (m):", m_fit)
print("Fitted intercept (c):", c_fit)
print("Fitted line SSE:", sse_fit)
print("Fitted line beats both guesses:", sse_fit < sse_a and sse_fit < sse_b)

# Task 3
def grad_m(m, c, x, y):
    pred = m * x + c
    return -2 * np.sum(x * (y - pred))

m_current = 10.0
learning_rate = 0.001
print("\nGradient descent steps:")
for i in range(6):
    current_sse = sse(m_current, c_fit, size, price)
    print(f"step {i}: m={round(m_current, 4)}, SSE={current_sse}")
    g = grad_m(m_current, c_fit, size, price)
    m_current = m_current - learning_rate * g

print(f"\nFinal m after 6 steps: {round(m_current, 4)}")
print(f"Fitted slope from sklearn: {m_fit}")
```

</details>
