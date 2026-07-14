# Coding Problem: Master Class — The Mathematics Behind Learning: Lines, Curves & Errors
> **Session 5 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

Five flats in Bengaluru. `size` is in **hundreds of square feet**, `rent` is in **thousands of rupees per month**. Small enough to check every line of your output on paper.

```python
import numpy as np

size = np.array([1., 2., 3., 4., 5.])        # hundreds of sq ft
rent = np.array([12., 18., 26., 31., 38.])   # ₹ thousands per month

# Our current guess at the line:  rent = m * size + c
m = 6.0     # ₹6,000 more rent per extra 100 sq ft
c = 7.0     # base rent of ₹7,000  (keep c FIXED for this exercise)
lr = 0.05   # learning rate
```

---

## Tasks

**Task 1 — Basic**
Use the line `rent = m * size + c` to compute the **predicted rent** for all five flats, and print the array.

**Task 2 — Basic**
Compute the **residuals** (`actual − predicted`), then print the **SSE** (sum of squared residuals) and the **MSE** (mean of squared residuals). Check both against your paper working before you trust them.

**Task 3 — Mid**
Take **one gradient descent step on the slope `m`**, keeping `c` fixed.

- Part (a): compute the slope of the error curve using `gradient = -2 * mean(size * residual)`, and print it.
- Part (b): apply the update rule `new_m = m - lr * gradient`, print `new_m`, then recompute the MSE with `new_m` and print it. Finish the sentence: *"MSE went from ___ to ___, so the step moved us ___ the bowl."*

---

## Expected Output

```
Predicted rent: [13. 19. 25. 31. 37.]

Residuals: [-1. -1.  1.  0.  1.]
SSE: 4.00
MSE: 0.80

Gradient (slope of the error curve at m = 6.0): -2.00
New m after one step: 6.10
New MSE: 0.71
MSE went from 0.80 to 0.71, so the step moved us DOWN the bowl.
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np

size = np.array([1., 2., 3., 4., 5.])        # hundreds of sq ft
rent = np.array([12., 18., 26., 31., 38.])   # ₹ thousands per month

m, c, lr = 6.0, 7.0, 0.05

# ---- Task 1: predictions from the line rent = m*size + c ----
pred = m * size + c
print("Predicted rent:", pred)               # [13. 19. 25. 31. 37.]

# ---- Task 2: residuals, SSE, MSE ----
resid = rent - pred                          # actual - predicted
sse = np.sum(resid ** 2)                     # squaring stops +/- cancelling
mse = np.mean(resid ** 2)                    # = SSE / n
print("\nResiduals:", resid)                 # [-1. -1.  1.  0.  1.]
print(f"SSE: {sse:.2f}")                     # 4.00
print(f"MSE: {mse:.2f}")                     # 0.80

# ---- Task 3a: slope of the error curve at this m ----
gradient = -2 * np.mean(size * resid)
print(f"\nGradient (slope of the error curve at m = {m}): {gradient:.2f}")   # -2.00

# ---- Task 3b: one step downhill, then re-score ----
new_m = m - lr * gradient                    # move AGAINST the slope
new_resid = rent - (new_m * size + c)
new_mse = np.mean(new_resid ** 2)

print(f"New m after one step: {new_m:.2f}")  # 6.10
print(f"New MSE: {new_mse:.2f}")             # 0.71
print(f"MSE went from {mse:.2f} to {new_mse:.2f}, "
      f"so the step moved us {'DOWN' if new_mse < mse else 'UP'} the bowl.")
```

**Why it works:** the gradient came out **negative**, which says the error bowl is still falling away to the right of `m = 6`. The minus sign in `new_m = m - lr * gradient` therefore pushes `m` **upward**, to 6.10 — and the MSE drops from 0.80 to 0.71. Run this update in a loop and `m` settles at about **6.09**, which is the exact best slope for this data when `c` is held at 7.

</details>
