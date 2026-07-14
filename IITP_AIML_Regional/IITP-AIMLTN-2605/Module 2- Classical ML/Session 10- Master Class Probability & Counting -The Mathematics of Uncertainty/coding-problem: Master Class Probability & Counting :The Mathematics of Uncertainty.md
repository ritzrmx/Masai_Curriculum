# Coding Problem: Master Class Probability & Counting :The Mathematics of Uncertainty
> **Session 10 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

No file to load — enumerate the sample space directly, and use the stated medical-test numbers below.

**Two dice, all 36 equally-likely outcomes:**
```python
import itertools

faces = [1, 2, 3, 4, 5, 6]
sample_space = list(itertools.product(faces, faces))   # 36 outcomes, e.g. (1,1), (1,2), ...
```

**Medical test priors and likelihoods (stated, not computed):**
```
P(Disease)          = 0.02   (2% of the population has the condition)
P(+ | Disease)      = 0.95   (sensitivity)
P(+ | No Disease)   = 0.10   (false positive rate)
```

---

## Tasks

**Task 1 — Basic**
Using the enumerated two-dice `sample_space`, compute `P(sum = 8)` and `P(at least one die shows 5)` by counting outcomes directly. Then compute `P(sum=8 OR at least one die shows 5)` using the addition rule.

**Task 2 — Basic**
Compute the conditional probability `P(sum=8 | at least one die shows 5)` — i.e., among only the outcomes where at least one die is a 5, what fraction also sum to 8?

**Task 3 — Mid**
Using the medical test numbers above, apply the Law of Total Probability to find `P(Positive test)`, then apply Bayes' Theorem to find `P(Disease | Positive test)`.

Round every probability to 4 decimal places with `round(x, 4)`.

---

## Expected Output

```
Sample space size: 36
P(sum = 8): 0.1389
P(at least one 5): 0.3056
P(sum=8 OR at least one 5): 0.3889

P(sum=8 | at least one 5): 0.1818

P(Positive test): 0.117
P(Disease | Positive): 0.1624
```

---

<details>
<summary>Solution</summary>

```python
import itertools

# --- Dataset: two-dice sample space (enumerated) ---
faces = [1, 2, 3, 4, 5, 6]
sample_space = list(itertools.product(faces, faces))

# Task 1
event_sum8 = [pair for pair in sample_space if sum(pair) == 8]
event_has5 = [pair for pair in sample_space if 5 in pair]
p_sum8 = len(event_sum8) / len(sample_space)
p_has5 = len(event_has5) / len(sample_space)

union = set(event_sum8) | set(event_has5)
p_union = len(union) / len(sample_space)

print("Sample space size:", len(sample_space))
print("P(sum = 8):", round(p_sum8, 4))
print("P(at least one 5):", round(p_has5, 4))
print("P(sum=8 OR at least one 5):", round(p_union, 4))

# Task 2
intersect = set(event_sum8) & set(event_has5)
p_sum8_given_has5 = len(intersect) / len(event_has5)
print("\nP(sum=8 | at least one 5):", round(p_sum8_given_has5, 4))

# Task 3 - Bayes' Theorem
p_disease = 0.02
p_pos_given_disease = 0.95
p_pos_given_no_disease = 0.10
p_no_disease = 1 - p_disease

p_positive = p_pos_given_disease * p_disease + p_pos_given_no_disease * p_no_disease
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive

print("\nP(Positive test):", round(p_positive, 4))
print("P(Disease | Positive):", round(p_disease_given_pos, 4))
```

</details>
