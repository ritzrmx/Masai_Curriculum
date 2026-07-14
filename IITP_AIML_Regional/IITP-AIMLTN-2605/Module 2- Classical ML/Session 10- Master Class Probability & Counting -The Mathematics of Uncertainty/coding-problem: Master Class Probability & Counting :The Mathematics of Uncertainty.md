# Coding Problem: Master Class — Probability & Counting: The Mathematics of Uncertainty
> **Session 10 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A screening test for a rare condition. Everything you need is in three numbers.

```python
import numpy as np

test_info = {
    "prevalence":  0.001,   # P(disease)              — 1 person in 1,000
    "sensitivity": 0.99,    # P(test positive | disease)
    "specificity": 0.99,    # P(test negative | healthy)
}

N_PEOPLE = 100_000
rng = np.random.default_rng(42)
```

Before you write a line of code, work the answer out on paper using the 100,000-people table from the pre-read. Your code is here to *confirm* you, not to *tell* you.

---

## Tasks

**Task 1 — Basic**
Compute `P(positive)` — the chance a randomly chosen person tests positive — using the law of total probability:
`P(+) = P(+|D) × P(D) + P(+|healthy) × P(healthy)`. Print it to 5 decimal places.

**Task 2 — Basic**
Use **Bayes' theorem** to compute `P(disease | positive) = P(+|D) × P(D) / P(+)`. Print it as a decimal to 4 places and as a percentage to 1 place.

**Task 3 — Mid**
Simulate `N_PEOPLE` patients with `rng`: first decide who actually has the disease, then run the test on each person (positive with probability `sensitivity` if ill, and with probability `1 − specificity` if healthy). Count the **true positives** and **false positives**, then print the simulated `P(disease | positive) = TP / (TP + FP)` and check that it lands close to your Bayes answer from Task 2.

---

## Expected Output

```
P(positive) = 0.01098
P(disease | positive) = 0.0902  (9.0%)

Simulated 100,000 patients
Positive tests   : ~1,100
True positives   : ~100
False positives  : ~1,000
Simulated P(disease | positive) = 0.09xx
Bayes  said                     = 0.0902
```

(The simulated counts wobble a little each run; the ratio should always sit near 0.09.)

---

<details>
<summary>Solution</summary>

```python
import numpy as np

test_info = {
    "prevalence":  0.001,
    "sensitivity": 0.99,
    "specificity": 0.99,
}
N_PEOPLE = 100_000
rng = np.random.default_rng(42)

p_d  = test_info["prevalence"]
sens = test_info["sensitivity"]
spec = test_info["specificity"]

# --- Task 1: law of total probability -------------------------------------
# A positive can come from an ill person (correctly) or a healthy one (falsely).
p_pos = sens * p_d + (1 - spec) * (1 - p_d)
print(f"P(positive) = {p_pos:.5f}")

# --- Task 2: Bayes' theorem -----------------------------------------------
# P(D|+) = P(+|D) * P(D) / P(+)
p_d_given_pos = (sens * p_d) / p_pos
print(f"P(disease | positive) = {p_d_given_pos:.4f}  ({p_d_given_pos * 100:.1f}%)")

# --- Task 3: simulate 100,000 patients and just count ----------------------
has_disease = rng.random(N_PEOPLE) < p_d                      # who is actually ill
prob_positive = np.where(has_disease, sens, 1 - spec)         # each person's chance of a positive
tests_positive = rng.random(N_PEOPLE) < prob_positive         # run the test

n_positive       = tests_positive.sum()
n_true_positive  = ( has_disease & tests_positive).sum()
n_false_positive = (~has_disease & tests_positive).sum()

print(f"\nSimulated {N_PEOPLE:,} patients")
print(f"Positive tests   : {n_positive}")
print(f"True positives   : {n_true_positive}")
print(f"False positives  : {n_false_positive}")
print(f"Simulated P(disease | positive) = {n_true_positive / n_positive:.4f}")
print(f"Bayes  said                     = {p_d_given_pos:.4f}")

# The false positives massively outnumber the true positives — that is the base
# rate at work, and it is exactly why precision (Session 8) collapses on rare classes.
```

</details>
