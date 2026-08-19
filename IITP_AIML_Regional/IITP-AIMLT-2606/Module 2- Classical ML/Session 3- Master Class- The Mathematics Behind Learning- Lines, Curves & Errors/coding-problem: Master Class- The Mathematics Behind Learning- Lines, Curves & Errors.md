# Coding Problem: Master Class — The Mathematics Behind Learning: Lines, Curves & Errors
> **Session 3 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Compute predictions from a line equation:

```python
def predict(x, m, c):
    return m * x + c

xs = [1, 2, 3, 4]
m, c = 2, 1
predictions = [predict(x, m, c) for x in xs]
print(predictions)
```

**Task 2 — Basic**

Compute residuals and MSE:

```python
actual = [3, 5, 7, 9]
predicted = predictions  # from Task 1

residuals = [a - p for a, p in zip(actual, predicted)]
mse = sum(r ** 2 for r in residuals) / len(residuals)
print("Residuals:", residuals)
print("MSE:", mse)
```

**Task 3 — Mid**

Implement one full gradient descent loop to learn `m` for `y = m*x` (fit only slope, no intercept):

```python
x_vals = [1, 2, 3, 4]
y_vals = [3, 5, 7, 9]  # true: y = 2x + 1 (approx)

m = 0.0
learning_rate = ___
for step in range(___):
    preds = [m * x for x in x_vals]
    errors = [p - y for p, y in zip(preds, y_vals)]
    gradient = sum(e * x for e, x in zip(errors, x_vals)) / len(x_vals)
    m = m - learning_rate * gradient

print(f"Learned m ≈ {m:.3f}")
```

---

## Expected Output

```
[3, 5, 7, 9]
Residuals: [0, 0, 0, 0]
MSE: 0.0
Learned m ≈ 2.3...
```

*(Task 3's exact value depends on learning_rate and step count; it should converge close to the best-fit slope for this data.)*

---

<details>
<summary>Solution</summary>

```python
def predict(x, m, c):
    return m * x + c

xs = [1, 2, 3, 4]
m, c = 2, 1
predictions = [predict(x, m, c) for x in xs]
print(predictions)

actual = [3, 5, 7, 9]
residuals = [a - p for a, p in zip(actual, predictions)]
mse = sum(r ** 2 for r in residuals) / len(residuals)
print("Residuals:", residuals)
print("MSE:", mse)

x_vals = [1, 2, 3, 4]
y_vals = [3, 5, 7, 9]

m = 0.0
learning_rate = 0.01
for step in range(2000):
    preds = [m * x for x in x_vals]
    errors = [p - y for p, y in zip(preds, y_vals)]
    gradient = sum(e * x for e, x in zip(errors, x_vals)) / len(x_vals)
    m = m - learning_rate * gradient

print(f"Learned m ≈ {m:.3f}")
```
</details>
