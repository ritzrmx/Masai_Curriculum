# Coding Problem: Master Class — Probability & Counting

> **Session 14** | ⏱ 10 mins | Module 2: Classical ML

---

## Scenario

This Master Class explores probability through code — simulating coin flips, applying Bayes' Theorem step-by-step, and seeing how conditional probability works in practice. No ML library needed.

---

## Setup

```python
import numpy as np
np.random.seed(42)
```

---

## Tasks

**Task 1 — Basic Probability with Simulation**

Simulate rolling a die 10,000 times and calculate the probability of each outcome.

```python
rolls = np.random.randint(1, ___, size=10000)   # fill: 7 (range 1–6)

for face in range(1, 7):
    prob = np.sum(rolls == face) / len(rolls)
    print(f"P(rolling {face}) ≈ {prob:.3f}  (expected: {1/6:.3f})")
```

---

**Task 2 — Addition Rule**

Using the die simulation, verify the addition rule: P(A or B) = P(A) + P(B) − P(A and B).

```python
# Event A: rolling an even number {2, 4, 6}
# Event B: rolling a number > 4 {5, 6}

p_A        = np.sum(rolls % 2 == ___) / len(rolls)   # fill: 0 (even)
p_B        = np.sum(rolls > ___) / len(rolls)          # fill: 4
p_A_and_B  = np.sum((rolls % 2 == 0) & (rolls > 4)) / len(rolls)

p_A_or_B   = ___ + ___ - ___                          # fill: p_A + p_B - p_A_and_B

print(f"P(A) = {p_A:.3f}")
print(f"P(B) = {p_B:.3f}")
print(f"P(A and B) = {p_A_and_B:.3f}")
print(f"P(A or B) = {p_A_or_B:.3f}  (expected ≈ 0.667)")
```

---

**Task 3 — Conditional Probability**

In a class of 50 students, 20 like maths and 12 like both maths and science.

```python
total       = 50
p_maths     = ___ / total           # fill: 20
p_both      = ___ / total           # fill: 12

# P(science | maths) = P(both) / P(maths)
p_sci_given_maths = ___ / ___       # fill: p_both / p_maths

print(f"P(likes maths):           {p_maths:.2f}")
print(f"P(likes both):            {p_both:.2f}")
print(f"P(science | maths):       {p_sci_given_maths:.2f}")
# Expected: 0.60
```

---

**Task 4 — Bayes' Theorem (Medical Test)**

A disease affects 1% of the population. The test is 99% accurate (99% TPR, 5% FPR). You test positive — what's the real probability you have the disease?

```python
p_disease      = ___     # fill: 0.01  — 1% base rate
p_no_disease   = 1 - p_disease

p_pos_given_disease    = ___    # fill: 0.99  — sensitivity
p_pos_given_no_disease = ___    # fill: 0.05  — false positive rate

# Bayes: P(disease | positive) = P(pos|disease)*P(disease) / P(positive)
p_positive = (p_pos_given_disease * p_disease) + \
             (p_pos_given_no_disease * p_no_disease)

p_disease_given_pos = (___ * ___) / ___   # fill: p_pos_given_disease, p_disease, p_positive

print(f"\nP(disease | positive test) = {p_disease_given_pos:.1%}")
print("Surprised? The rare base rate dominates the result.")
```

**Expected output:**
```
P(disease | positive test) = 16.6%
```

---

**Task 5 — Multiplication Rule (Independent Events)**

What's the probability of getting 3 heads in a row on a fair coin?

```python
p_head = ___                        # fill: 0.5
p_three_heads = ___ ** ___          # fill: p_head ** 3
print(f"P(3 heads in a row) = {p_three_heads:.3f}")

# Verify with simulation
flips = np.random.choice([0,1], size=(10000, 3))   # 10000 trials of 3 flips
three_heads_sim = np.sum(flips.sum(axis=1) == 3) / 10000
print(f"Simulated P(3 heads) ≈ {three_heads_sim:.3f}")
```

---

## Key Takeaways

- Probability is a number between 0 and 1 — simulation confirms theory
- **Conditional probability** updates what we know: P(A|B) ≠ P(A) unless A and B are independent
- **Bayes' Theorem** shows how rare base rates dramatically affect real-world test results
