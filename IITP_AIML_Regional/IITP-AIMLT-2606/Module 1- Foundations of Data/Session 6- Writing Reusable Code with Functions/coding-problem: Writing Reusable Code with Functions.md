# Coding Problem: Writing Reusable Code with Functions
> **Session 6 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Write `double(n)` returning n×2. Print `double(7)`.

**Task 2 — Basic**

Write `discounted(price, pct=10)` returning price after pct% off. Test with default and `pct=25`.

**Task 3 — Mid**

Write `summary(name, scores)` returning average of list `scores`; print one f-string line for `summary("Ria", [80, 90, 70])`.

---

## Expected Output

```
14
90.0
75.0
Ria avg: 80.0
```

---

<details>
<summary>Solution</summary>

```python
def double(n):
    return n * 2
print(double(7))

def discounted(price, pct=10):
    return price * (1 - pct / 100)
print(discounted(100))
print(discounted(100, 25))

def summary(name, scores):
    avg = sum(scores) / len(scores)
    return avg

name, scores = "Ria", [80, 90, 70]
print(f"{name} avg: {summary(name, scores)}")
```
</details>
