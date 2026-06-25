# Lecture Script: Python Fundamentals
> **Instructor Reference** — Module 1: Foundations of Data | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write and run Python in Colab using variables, types, operators, input/output, and f-strings.

**Key outcome:** Each student completes a mini "profile card" program that asks for name, age, and city and prints a formatted greeting.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Colab setup & first cell | 15 min | 0:15 |
| Variables & types live demo | 20 min | 0:35 |
| Operators & type inspection | 15 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| input(), print(), f-strings | 25 min | 1:25 |
| Lab: Profile card + tip calculator | 25 min | 1:50 |
| Summary & homework | 10 min | 2:00 |

---

## Live Demo Highlights

```python
x = 10
print(type(x))
print(f"Double is {x * 2}")

name = input("Name: ")
print(f"Welcome, {name}!")
```

Discuss: `input()` always returns a **string** — cast with `int()` when needed.

---

## Lab: Profile Card

Requirements: ask name, age, favourite language; print two lines using f-strings; show age in 5 years.

---

## Common Errors to Address

- NameError (typo in variable)
- TypeError (str + int)
- Forgetting quotes on strings
