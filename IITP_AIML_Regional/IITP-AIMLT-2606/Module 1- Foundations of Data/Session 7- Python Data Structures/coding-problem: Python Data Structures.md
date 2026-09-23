# Coding Problem: Python Data Structures
> **Session 7 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Given list, print first, last, and slice middle two:

```python
nums = [5, 10, 15, 20, 25]
```

**Task 2 — Basic**

Count unique words using a set:

```python
words = ["data", "ml", "data", "ai", "ml", "ai"]
```

**Task 3 — Mid**

Build dict `inventory` with keys `"apple"`, `"banana"` and counts; print total items.

```python
inventory = {"apple": 3, "banana": 5}
```

---

## Expected Output

```
5
25
[10, 15]
3
8
```

---

<details>
<summary>Solution</summary>

```python
nums = [5, 10, 15, 20, 25]
print(nums[0])
print(nums[-1])
print(nums[1:3])

words = ["data", "ml", "data", "ai", "ml", "ai"]
print(len(set(words)))

inventory = {"apple": 3, "banana": 5}
print(sum(inventory.values()))
```
</details>
