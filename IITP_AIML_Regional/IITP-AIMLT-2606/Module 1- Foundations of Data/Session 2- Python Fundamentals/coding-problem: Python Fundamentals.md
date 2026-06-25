# Coding Problem: Python Fundamentals
> **Session 2 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Create variables and print their types:

```python
item = "Notebook"
qty = 3
price = 249.50
in_stock = True
# Print each value and its type
```

**Task 2 — Basic**

Compute and print (use f-strings):

```python
qty = 4
price = 125.0
# subtotal, 18% tax, grand total
```

**Task 3 — Mid**

Ask the user for item name and quantity; print a one-line order summary.

```python
item = input("Item: ")
qty = int(input("Quantity: "))
# Print: "Order: <qty>x <item>"
```

---

## Expected Output

```
Notebook <class 'str'>
3 <class 'int'>
249.5 <class 'float'>
True <class 'bool'>

Subtotal: 500.0
Tax: 90.0
Total: 590.0
```

*(Task 3 output depends on user input.)*

---

<details>
<summary>Solution</summary>

```python
item = "Notebook"
qty = 3
price = 249.50
in_stock = True
for v in [item, qty, price, in_stock]:
    print(v, type(v))

qty = 4
price = 125.0
sub = qty * price
tax = sub * 0.18
print(f"Subtotal: {sub}")
print(f"Tax: {tax}")
print(f"Total: {sub + tax}")

item = input("Item: ")
qty = int(input("Quantity: "))
print(f"Order: {qty}x {item}")
```
</details>
