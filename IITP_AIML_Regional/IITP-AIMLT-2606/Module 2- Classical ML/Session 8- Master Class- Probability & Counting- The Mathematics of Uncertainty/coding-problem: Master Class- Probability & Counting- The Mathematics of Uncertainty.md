# Coding Problem: Master Class — Probability & Counting: The Mathematics of Uncertainty
> **Session 8 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Compute a basic probability from a sample space and event:

```python
sample_space = set(range(1, 21))          # numbers 1 to 20
event_multiple_of_4 = {n for n in sample_space if n % 4 == 0}

probability = len(event_multiple_of_4) / len(sample_space)
print(event_multiple_of_4)
print(probability)
```

**Task 2 — Basic**

Compute a conditional probability from counts:

```python
total_customers = 200
members = 80
members_and_purchased = 60

p_purchased_given_member = members_and_purchased / members
print(f"P(purchased | member) = {p_purchased_given_member:.3f}")
```

**Task 3 — Mid**

Apply Bayes' Theorem to a spam-filter scenario:

```python
p_spam = 0.20                 # 20% of all emails are spam (prior)
p_flagged_given_spam = 0.98    # filter flags 98% of real spam
p_flagged_given_not_spam = 0.05  # filter wrongly flags 5% of real (non-spam) emails

p_not_spam = 1 - p_spam
p_flagged = (p_flagged_given_spam * p_spam) + (p_flagged_given_not_spam * p_not_spam)

p_spam_given_flagged = (p_flagged_given_spam * p_spam) / p_flagged
print(f"P(spam | flagged) = {p_spam_given_flagged:.3f}")
```

---

## Expected Output

```
{4, 8, 12, 16, 20}
0.25
P(purchased | member) = 0.750
P(spam | flagged) = 0.831
```

---

<details>
<summary>Solution</summary>

```python
sample_space = set(range(1, 21))
event_multiple_of_4 = {n for n in sample_space if n % 4 == 0}
probability = len(event_multiple_of_4) / len(sample_space)
print(event_multiple_of_4)
print(probability)

total_customers = 200
members = 80
members_and_purchased = 60
p_purchased_given_member = members_and_purchased / members
print(f"P(purchased | member) = {p_purchased_given_member:.3f}")

p_spam = 0.20
p_flagged_given_spam = 0.98
p_flagged_given_not_spam = 0.05

p_not_spam = 1 - p_spam
p_flagged = (p_flagged_given_spam * p_spam) + (p_flagged_given_not_spam * p_not_spam)
p_spam_given_flagged = (p_flagged_given_spam * p_spam) / p_flagged
print(f"P(spam | flagged) = {p_spam_given_flagged:.3f}")
```
</details>
