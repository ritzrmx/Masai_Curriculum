# Coding Problem: Control Flow & Decision Making
> **Session 3 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Print ticket price: child (<12) = 100, adult = 200.

```python
age = 10
# your if/else here
```

**Task 2 — Basic**

```python
score = 78
# Print A if >=90, B if >=75, C if >=60, else F
```

**Task 3 — Mid**

Free shipping if `total >= 500` **and** `is_member`. Set variables and print message.

```python
total = 650
is_member = True
```

---

## Expected Output

```
100
B
Free shipping applied
```

---

<details>
<summary>Solution</summary>

```python
age = 10
print(100 if age < 12 else 200)

score = 78
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")

total = 650
is_member = True
if total >= 500 and is_member:
    print("Free shipping applied")
```
</details>
