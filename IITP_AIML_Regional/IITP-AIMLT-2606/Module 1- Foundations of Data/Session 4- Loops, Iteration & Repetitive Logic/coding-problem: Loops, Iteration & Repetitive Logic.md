# Coding Problem: Loops, Iteration & Repetitive Logic
> **Session 4 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Print squares of 1 through 5 using `for` and `range`.

**Task 2 — Basic**

```python
nums = [4, 7, 2, 9, 1]
# Print sum using a loop
```

**Task 3 — Mid**

Print only values > 5 from `nums`; stop early if sum exceeds 15 (use break).

---

## Expected Output

```
1 1
2 4
3 9
4 16
5 25

23
7
9
```

*(Task 3: prints 7, then 9, then breaks when running sum > 15.)*

---

<details>
<summary>Solution</summary>

```python
for i in range(1, 6):
    print(i, i * i)

nums = [4, 7, 2, 9, 1]
s = 0
for n in nums:
    s += n
print(s)

s = 0
for n in nums:
    if n > 5:
        print(n)
    s += n
    if s > 15:
        break
```
</details>
