# Coding Problem: Master class - Numbers, Logic & Structure
> **Session 5 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Evaluate and print boolean results:

```python
a, b = True, False
print(a and b)
print(a or b)
print(not a)
```

**Task 2 — Basic**

De Morgan check — should match:

```python
a, b = True, False
print(not (a and b))
print((not a) or (not b))
```

**Task 3 — Mid**

Use a set to print unique tags from a list:

```python
tags = ["ml", "ai", "ml", "data", "ai", "python"]
# unique tags, sorted
```

---

## Expected Output

```
False
True
False
True
True
['ai', 'data', 'ml', 'python']
```

---

<details>
<summary>Solution</summary>

```python
a, b = True, False
print(a and b)
print(a or b)
print(not a)
print(not (a and b))
print((not a) or (not b))

tags = ["ml", "ai", "ml", "data", "ai", "python"]
print(sorted(set(tags)))
```
</details>
