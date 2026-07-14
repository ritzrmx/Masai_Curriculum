# Lecture Script: Master Class Probability & Counting :The Mathematics of Uncertainty
> **Instructor Reference** — Module 2: Classical ML | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can compute probabilities from first principles (sample spaces, addition rule, multiplication rule, conditional probability) and can derive and apply Bayes' Theorem by hand and in code to update a belief given new evidence.

**Student profile at this point:** Has built and evaluated classifiers (Logistic Regression, Decision Trees, ensembles) and just finished K-Means / Hierarchical Clustering. Has called `predict_proba()` and seen a model output "0.83 probability of class 1" without ever being told formally what that number means or where it comes from.

**Key outcome:** By the end of class, every student can explain — with a worked example, not just a formula — why a "99% accurate" medical test can still be wrong more often than right on a rare disease, and can compute a posterior probability from a prior and new evidence, by hand and in code.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Sample Spaces, Events & the Basic Rules | 10 min | 0:15 |
| **Practical 1:** Simulating Probability — Coins & Dice | 15 min | 0:30 |
| **Concept 2:** Multiplication Rule & Conditional Probability | 10 min | 0:40 |
| **Practical 2:** Enumerating a Deck of Cards | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Deriving Bayes' Theorem from First Principles | 10 min | 1:15 |
| **Practical 3:** Bayes by Hand — The Disease Test Problem | 15 min | 1:30 |
| **Concept 4:** Prior + Evidence = Updated Belief | 10 min | 1:40 |
| **Practical 4:** Bayes for Spam Filtering | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Write this on the board without explanation:

```
A medical test for a rare disease is 99% accurate.
You test positive.
What is the probability you actually have the disease?
```

Ask the class to write down a guess — a single number — before you say anything else. Collect a few answers out loud. Most will say "99%" or "close to it." Tell them: *"By the end of today, you will compute the real answer yourselves, from scratch, with no formula memorized — and it will surprise you."*

**Context to set:** Every classifier you have built this module — Logistic Regression, Random Forest, even K-Means's cluster assignments — ultimately outputs or relies on a probability. `predict_proba()` gives you a number between 0 and 1. But *what is a probability, mathematically*, and how do you combine two pieces of evidence into an updated belief? That is not a machine learning question — it is 300-year-old mathematics, and it is the foundation under everything "confidence," "likelihood," and "uncertainty" mean in this course, including the LLM systems you will build in Module 3.

**Learning contract for today:**
- Compute probabilities from a sample space by counting outcomes — not by guessing
- State and use the complement, addition, and multiplication rules correctly
- Distinguish P(A) from P(A|B) — and explain why the difference matters
- Derive Bayes' Theorem step by step and use it to update a belief with new evidence

---

## Concept Block 1: Sample Spaces, Events & the Basic Rules (10 min)

### What Probability Actually Measures

**Teaching point:** Probability is a ratio. Every probability question reduces to: *"Out of all the things that could happen, what fraction are the thing I care about?"*

**Sample space (S):** the set of *all possible outcomes* of an experiment. **Event (A):** any *subset* of the sample space — the outcomes you actually care about.

```
Coin flip:        S = {Heads, Tails}                    |S| = 2
Single die roll:  S = {1, 2, 3, 4, 5, 6}                 |S| = 6
Two dice roll:    S = {(1,1), (1,2), ..., (6,6)}         |S| = 36
```

**Classical probability formula (equally likely outcomes):**

```
        Number of outcomes in event A          |A|
P(A) = ---------------------------------- =    -----
        Number of outcomes in sample space      |S|
```

### Example: rolling a single die

| Event | Outcomes | Count | P(A) |
|---|---|---|---|
| A: Even number | {2, 4, 6} | 3 | 3/6 = 0.5 |
| B: Number > 4 | {5, 6} | 2 | 2/6 = 0.333 |
| A ∩ B: Even AND > 4 | {6} | 1 | 1/6 = 0.167 |
| A ∪ B: Even OR > 4 | {2, 4, 5, 6} | 4 | 4/6 = 0.667 |

### Rule 1 — The Complement Rule

Every outcome either is in A or is not. There is no third option.

```
P(A) + P(not A) = 1        =>       P(not A) = 1 - P(A)
```

**Teaching point:** Use this as a sanity check. If P(A) + P(A') ≠ 1, something is wrong in the counting.

### Rule 2 — The Addition Rule

For **any** two events (they may overlap):

```
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
```

**ASCII Venn diagram — why we subtract the overlap:**

```
   S:  ┌──── A ────┬──── B ────┐
       │      ▓▓▓▓▓▓▓▓▓        │    ▓ = A∩B, counted once in P(A) AND once in P(B)
       └───────────┴───────────┘
```

**Teaching point:** Adding P(A) + P(B) counts the overlap region *twice*, so we subtract it once. If A and B never overlap ("mutually exclusive"), P(A ∩ B) = 0 and the rule simplifies to P(A ∪ B) = P(A) + P(B).

### Rule 3 — The Multiplication Rule (for independent events)

Two events are **independent** if knowing one happened tells you *nothing* about whether the other happened.

```
P(A and B) = P(A) × P(B)     (only valid when A and B are independent)

Example: two coin flips -> P(Heads then Heads) = 0.5 × 0.5 = 0.25
```

**Teaching point:** This rule is *only* valid for independent events. Drawing two cards from a deck *without replacement* is NOT independent — the second draw's sample space has changed. We hit this trap directly in Practical 2.

---

## Practical Block 1: Simulating Probability — Coins & Dice (15 min)

### Part A — The Law of Large Numbers, live

**Teaching point:** A probability is a *theoretical* long-run ratio. Simulation lets us watch that ratio emerge from randomness as sample size grows — the bridge between probability theory and why a model's confidence score is trustworthy only at scale.

```python
import numpy as np

np.random.seed(42)

print("=== Coin flip convergence to theoretical P(Heads) = 0.5 ===")
for n in [10, 100, 1_000, 10_000, 100_000]:
    flips = np.random.randint(0, 2, size=n)  # 0 = Tails, 1 = Heads
    p_heads = flips.mean()
    print(f"n={n:>7,} flips -> P(Heads) = {p_heads:.4f}")
```

**Output:**
```
=== Coin flip convergence to theoretical P(Heads) = 0.5 ===
n=     10 flips -> P(Heads) = 0.3000
n=    100 flips -> P(Heads) = 0.6100
n=  1,000 flips -> P(Heads) = 0.4920
n= 10,000 flips -> P(Heads) = 0.4995
n=100,000 flips -> P(Heads) = 0.5014
```

**Walk through this live.** At n=10 the estimate is wildly off (0.30!). By n=100,000 it is essentially exact. Ask: *"Why does the small sample lie to us?"* — the same reason a train/test split of 20 rows gives an unreliable accuracy score.

### Part B — Enumerate, don't just formula-chase

**Teaching point:** Formulas are a shortcut for *counting*. When in doubt, enumerate the full sample space and count directly — `itertools` makes this trivial. Below: a single die (complement rule check), then the full 36-outcome two-dice space (addition rule and multiplication rule checks).

```python
import itertools

die_space = list(range(1, 7))
event_even = [x for x in die_space if x % 2 == 0]
event_odd = [x for x in die_space if x not in event_even]
print("Sample space S:", die_space, " |S| =", len(die_space))
print("Event A (even):", event_even, "-> P(A) =", round(len(event_even) / len(die_space), 4))
print("Complement A' (odd):", event_odd, "-> P(A') =", round(len(event_odd) / len(die_space), 4))
print("Check: P(A) + P(A') =", round(len(event_even) / len(die_space) + len(event_odd) / len(die_space), 4))

# Two dice: enumerate the full 36-outcome sample space
two_dice_space = list(itertools.product(die_space, die_space))
print("\n|S| (two dice) =", len(two_dice_space), "outcomes, e.g.", two_dice_space[:5], "...")

sum_7 = [pair for pair in two_dice_space if sum(pair) == 7]
print("Outcomes where sum = 7:", sum_7, "-> P(sum=7) =", round(len(sum_7) / len(two_dice_space), 4))

# Addition rule: A = sum is 7, B = doubles (both dice equal)
event_A, event_B = set(sum_7), set(p for p in two_dice_space if p[0] == p[1])
p_A, p_B = len(event_A) / 36, len(event_B) / 36
p_union_direct = len(event_A | event_B) / 36
p_union_formula = p_A + p_B - len(event_A & event_B) / 36
print("\nP(A)=", round(p_A, 4), " P(B)=", round(p_B, 4), " P(A∩B)=", len(event_A & event_B), "/36")
print("P(A ∪ B) direct count  =", round(p_union_direct, 4))
print("P(A ∪ B) addition rule =", round(p_union_formula, 4))

# Multiplication rule for independent events: P(die1=6 AND die2=6)
both_six = set(p for p in two_dice_space if p[0] == 6) & set(p for p in two_dice_space if p[1] == 6)
print("\nP(die1=6 AND die2=6) by count      =", round(len(both_six) / 36, 4))
print("P(die1=6) * P(die2=6) (mult. rule) =", round((1/6) * (1/6), 4))
```

**Output:**
```
Sample space S: [1, 2, 3, 4, 5, 6]  |S| = 6
Event A (even): [2, 4, 6] -> P(A) = 0.5
Complement A' (odd): [1, 3, 5] -> P(A') = 0.5
Check: P(A) + P(A') = 1.0

|S| (two dice) = 36 outcomes, e.g. [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)] ...
Outcomes where sum = 7: [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)] -> P(sum=7) = 0.1667

P(A)= 0.1667  P(B)= 0.1667  P(A∩B)= 0 /36
P(A ∪ B) direct count  = 0.3333
P(A ∪ B) addition rule = 0.3333

P(die1=6 AND die2=6) by count      = 0.0278
P(die1=6) * P(die2=6) (mult. rule) = 0.0278
```

**Ask the class:** *"Why is P(A ∩ B) = 0 for sum-is-7 and doubles?"* → No pair of equal dice sums to an odd number, so the events are mutually exclusive. The direct-count answer and the formula answer match exactly — that agreement is what builds trust in the formula.

---

## Concept Block 2: Multiplication Rule & Conditional Probability (10 min)

### The Multiplication Rule, generalized

The rule from Concept 1 (`P(A and B) = P(A) × P(B)`) only works for *independent* events. What if they are **not** independent — like drawing two cards from a deck without putting the first one back?

```
General multiplication rule:  P(A and B) = P(A) × P(B | A)
```

This introduces the most important idea of the day.

### Conditional Probability: P(A | B)

**Definition:** P(A | B) is "the probability of A, *given that we already know B happened*." Knowing B shrinks the sample space down to only the outcomes consistent with B — then we ask what fraction of *that* smaller space is also A.

```
              P(A ∩ B)
P(A | B)  =  ----------          (only defined when P(B) > 0)
               P(B)

Conditioning shrinks the sample space: universe S -> universe B only.
We stop looking at all of S and ask what fraction of B is also A: P(A|B) = |A∩B| / |B|
```

**Worked example — cards:** P(King | Face card)? Face cards = {J,Q,K} × 4 suits = 12 cards; Kings among them = 4. So P(King | Face) = 4/12 = 1/3 — much higher than the unconditional P(King) = 4/52 ≈ 0.077. **Knowing it's a face card changed the probability** — that is the whole point of conditioning.

**Teaching point:** A and B are independent *exactly when* P(A | B) = P(A) — knowing B changes nothing about A. We test this directly in code next.

**Common confusion to pre-empt:** P(A | B) is almost never equal to P(B | A). "P(King | Face)" (1/3) is very different from "P(Face | King)" (4/4 = 1). Mixing these up is the single most common Bayes' Theorem mistake — flag it now, it pays off in Concept Block 3.

---

## Practical Block 2: Enumerating a Deck of Cards (15 min)

### Build the sample space, then apply the addition rule

```python
import itertools

ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
suits = ['Hearts','Diamonds','Clubs','Spades']
deck = list(itertools.product(ranks, suits))
print("|S| (full deck) =", len(deck))

kings = [c for c in deck if c[0] == 'K']
hearts = [c for c in deck if c[1] == 'Hearts']
p_king, p_heart = len(kings) / len(deck), len(hearts) / len(deck)
print("Kings:", kings)
print("P(King) =", round(p_king, 4), " P(Heart) =", round(p_heart, 4))

# Addition rule: P(King OR Heart)
king_and_heart = set(kings) & set(hearts)
p_king_and_heart = len(king_and_heart) / len(deck)
p_union_direct = len(set(kings) | set(hearts)) / len(deck)
p_union_formula = p_king + p_heart - p_king_and_heart
print("\nP(King ∩ Heart) =", len(king_and_heart), "/", len(deck), "=", round(p_king_and_heart, 4))
print("P(King ∪ Heart) by direct count  =", round(p_union_direct, 4))
print("P(King ∪ Heart) by addition rule =", round(p_union_formula, 4))
```

**Output:**
```
|S| (full deck) = 52
Kings: [('K', 'Hearts'), ('K', 'Diamonds'), ('K', 'Clubs'), ('K', 'Spades')]
P(King) = 0.0769  P(Heart) = 0.25

P(King ∩ Heart) = 1 / 52 = 0.0192
P(King ∪ Heart) by direct count  = 0.3077
P(King ∪ Heart) by addition rule = 0.3077
```

### Conditional probability — and testing independence

```python
# Conditional probability: P(King | Face card)
face_ranks = {'J', 'Q', 'K'}
face_cards = [c for c in deck if c[0] in face_ranks]
king_given_face = [c for c in face_cards if c[0] == 'K']
p_king_given_face = len(king_given_face) / len(face_cards)
print("Face cards |B| =", len(face_cards), " Kings within them |A∩B| =", len(king_given_face))
print("P(King | Face) = |A∩B|/|B| =", round(p_king_given_face, 4))
print("Unconditional P(King) =", round(p_king, 4), " vs Conditional P(King|Face) =",
      round(p_king_given_face, 4), "-> knowing it's a face card raises the odds")

# Independence check: is suit independent of rank being a King?
king_given_heart = [c for c in hearts if c[0] == 'K']
p_king_given_heart = len(king_given_heart) / len(hearts)
print("\nP(King | Heart) =", round(p_king_given_heart, 4), " vs P(King) =", round(p_king, 4),
      "-> equal, so 'King' and 'Heart' are independent events")
```

**Output:**
```
Face cards |B| = 12  Kings within them |A∩B| = 4
P(King | Face) = |A∩B|/|B| = 0.3333
Unconditional P(King) = 0.0769  vs Conditional P(King|Face) = 0.3333 -> knowing it's a face card raises the odds

P(King | Heart) = 0.0769  vs P(King) = 0.0769 -> equal, so 'King' and 'Heart' are independent events
```

**Teaching point:** Rank and suit are independent by construction — the deck has every rank in every suit equally. But "King" and "Face card" are *not* independent (0.333 ≠ 0.077). Have students predict, before running the code, whether each pair is independent — it builds the intuition Bayes' Theorem depends on.

---

## BREAK (10 min)

*Suggested break prompt — ask students to think of one real situation where they update a belief after new evidence arrives (e.g., "I thought my flight was on time, then I got a delay notification"). They will share one example after the break — we will formalize it in the next block.*

---

## Concept Block 3: Deriving Bayes' Theorem from First Principles (10 min)

### Start from something students already trust

We already know the conditional probability formula from Concept 2, and by the exact same logic with A and B swapped:

```
(1)  P(A | B) = P(A ∩ B) / P(B)
(2)  P(B | A) = P(A ∩ B) / P(A)
```

**Teaching point — this is the entire derivation:** Both equations describe the *same* quantity, P(A ∩ B), just divided differently. Rearrange each to isolate it:

```
From (1):   P(A ∩ B) = P(A | B) × P(B)
From (2):   P(A ∩ B) = P(B | A) × P(A)
```

Both right-hand sides equal the same thing, so they equal each other. Divide both sides by P(B):

```
P(A | B) × P(B) = P(B | A) × P(A)     =>     P(A | B) = [P(B | A) × P(A)] / P(B)
```

**That is Bayes' Theorem.** No new assumption was introduced — it is a direct algebraic rearrangement of the conditional probability definition applied twice.

### Renaming the terms for the way we actually use it

In practice we relabel A as the **Hypothesis** (what we want to know, e.g. "has disease") and B as the **Evidence** (what we observed, e.g. "tested positive"):

```
                    P(Evidence | Hypothesis) × P(Hypothesis)
P(Hypothesis | Evidence) = ------------------------------------------
                                    P(Evidence)
```

| Term | Name | Meaning |
|---|---|---|
| P(Hypothesis) | **Prior** | What we believed before seeing evidence |
| P(Evidence \| Hypothesis) | **Likelihood** | How probable the evidence is, if the hypothesis is true |
| P(Evidence) | **Marginal / Normalizer** | Total probability of seeing this evidence, under all hypotheses |
| P(Hypothesis \| Evidence) | **Posterior** | Our updated belief, after seeing the evidence |

**In one sentence: Posterior ∝ Likelihood × Prior.** This is not a machine learning model — it is a formula for rational belief-updating, and it predates computers by two centuries (Thomas Bayes, 1763).

### Expanding the denominator: Law of Total Probability

P(Evidence) usually isn't given directly — it must be built from *every way* the evidence could occur:

```
P(Evidence) = P(Evidence|Hypothesis)×P(Hypothesis) + P(Evidence|not Hypothesis)×P(not Hypothesis)
```

**Teaching point:** This is exactly the complement rule from Concept 1, put to work. "Positive test" can happen two ways — a sick person correctly flagged, or a healthy person incorrectly flagged. We compute this by hand next.

---

## Practical Block 3: Bayes by Hand — The Disease Test Problem (15 min)

### Setting up the problem

Return to the opening hook. State the numbers explicitly — this is exactly what "99% accurate" hides:

```python
# Bayes' Theorem from scratch: rare disease test
# P(D)      = prior probability of having the disease
# P(+|D)    = sensitivity: P(test positive | disease present)
# P(+|~D)   = false positive rate: P(test positive | disease absent)

p_disease = 0.01          # 1% of population has the disease
p_pos_given_disease = 0.99      # 99% sensitivity (true positive rate)
p_pos_given_no_disease = 0.05   # 5% false positive rate
p_no_disease = 1 - p_disease

print("=== Priors and likelihoods ===")
print("P(Disease) =", p_disease, " P(No Disease) =", p_no_disease)
print("P(+|Disease) =", p_pos_given_disease, " (sensitivity)   P(+|No Disease) =",
      p_pos_given_no_disease, " (false positive rate)")

# Step 1: Total probability of testing positive (law of total probability)
p_positive = (p_pos_given_disease * p_disease) + (p_pos_given_no_disease * p_no_disease)
print("\n=== Step 1: P(+) via law of total probability ===")
print("P(+) = P(+|D)*P(D) + P(+|~D)*P(~D)")
print(f"P(+) = {p_pos_given_disease * p_disease:.4f} + {p_pos_given_no_disease * p_no_disease:.4f} = {p_positive:.4f}")

# Step 2: Bayes' Theorem -> P(Disease | +)
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive
print("\n=== Step 2: Bayes' Theorem ===")
print("P(D|+) = P(+|D) * P(D) / P(+)")
print(f"P(D|+) = ({p_pos_given_disease} * {p_disease}) / {p_positive:.4f} = {p_disease_given_pos:.4f}  -> {p_disease_given_pos*100:.2f}%")
```

**Output:**
```
=== Priors and likelihoods ===
P(Disease) = 0.01  P(No Disease) = 0.99
P(+|Disease) = 0.99  (sensitivity)   P(+|No Disease) = 0.05  (false positive rate)

=== Step 1: P(+) via law of total probability ===
P(+) = P(+|D)*P(D) + P(+|~D)*P(~D)
P(+) = 0.0099 + 0.0495 = 0.0594

=== Step 2: Bayes' Theorem ===
P(D|+) = P(+|D) * P(D) / P(+)
P(D|+) = (0.99 * 0.01) / 0.0594 = 0.1667  -> 16.67%
```

**Stop here and let the number land.** A 99%-sensitive test, and a positive result means only a **16.67%** chance of actually having the disease. Ask: *"Was anyone's opening guess close to 16.67%?"* Almost never — the "99% accurate" framing tricks intuition. This is **base rate neglect**, one of the most well-documented reasoning errors in humans.

### Make it concrete — a population of 100,000, then a second positive test

```python
# Sanity check with a population of 100,000
population = 100_000
n_disease = population * p_disease
n_no_disease = population * (1 - p_disease)
true_positives = n_disease * p_pos_given_disease
false_positives = n_no_disease * p_pos_given_no_disease
total_positives = true_positives + false_positives
p_disease_given_pos_counts = true_positives / total_positives

print(f"People with disease: {n_disease:,.0f}   People without: {n_no_disease:,.0f}")
print(f"True positives: {true_positives:,.0f}   False positives: {false_positives:,.0f}   Total positive tests: {total_positives:,.0f}")
print(f"P(Disease | +) = {true_positives:,.0f} / {total_positives:,.0f} = {p_disease_given_pos_counts:.4f}")

# Second positive test: yesterday's posterior becomes today's prior
new_prior = p_disease_given_pos_counts
p_positive_round2 = (p_pos_given_disease * new_prior) + (p_pos_given_no_disease * (1 - new_prior))
p_disease_given_pos_round2 = (p_pos_given_disease * new_prior) / p_positive_round2
print(f"\nNew prior P(D) = previous posterior = {new_prior:.4f}")
print(f"After second positive test, P(D | ++) = {p_disease_given_pos_round2:.4f} -> {p_disease_given_pos_round2*100:.2f}%")
```

**Output:**
```
People with disease: 1,000   People without: 99,000
True positives: 990   False positives: 4,950   Total positive tests: 5,940
P(Disease | +) = 990 / 5,940 = 0.1667

New prior P(D) = previous posterior = 0.1667
After second positive test, P(D | ++) = 0.7984 -> 79.84%
```

**Teaching point:** Out of 5,940 people who test positive, only 990 actually have the disease — the rest are healthy people caught by the 5% false-positive rate applied to a *much bigger* healthy population. Base rates dominate when the prior is small.

**Teaching point — the single most important idea of the session:** *Today's posterior becomes tomorrow's prior.* One positive test moved belief from 1% to 16.67%. A *second* independent positive test moved it further, to 79.84%. This iterative "prior → evidence → posterior → new prior" loop is exactly how doctors order confirmatory tests.

---

## Concept Block 4: Prior + Evidence = Updated Belief (10 min)

### Reframing Bayes' Theorem as a belief-updating machine

```
  OLD BELIEF (Prior)  +  NEW EVIDENCE (Likelihood)  ==>  NEW BELIEF (Posterior)
  What did I think        How well does this evidence     What should I believe
  before?                 fit each hypothesis?             now, having seen it?
```

**Teaching point:** This reframing matters more than the algebra. Bayes' Theorem is a *procedure for rational thought under uncertainty*, not a formula to memorize: start with a belief, weigh new evidence by how well it fits, land on an updated belief. Every time `predict_proba()` outputs a number, some model ran a version of this same weighing process.

### Why the prior matters so much

Revisit the disease example: if the disease were **not** rare — say 50% of the *tested* population actually had it (e.g., testing only symptomatic people) — plugging P(D)=0.5 into the same formula gives:

```
P(+) = 0.99×0.5 + 0.05×0.5 = 0.52
P(D|+) = 0.495 / 0.52 = 0.952  ->  95.2%
```

Same test, same sensitivity, same false-positive rate — **completely different posterior**, because the prior changed. "The test is 99% accurate" is an incomplete sentence; you always need the base rate too.

### Connecting back to the course

| Where you've seen this before | What was really happening |
|---|---|
| `model.predict_proba(X)` (Session 6) | Model outputs a posterior-like probability given input features as "evidence" |
| Threshold tuning / precision-recall (Session 8) | Choosing how much posterior evidence you require before acting |
| Naive Bayes classifiers | Apply exactly this formula, assuming features are conditionally independent |
| Ahead, Module 3 (LLMs) | Token prediction is a giant, learned version of "what's most likely given the evidence so far" |

**Teaching point:** You are not learning probability *and separately* learning ML — probability is the language ML is written in. Today was about reading that language directly, without a model in between.

---

## Practical Block 4: Bayes for Spam Filtering (10 min)

### Setting priors and likelihoods, then updating with one word

```python
# Bayes' Theorem applied to spam filtering (a preview of Naive Bayes / NLP classifiers)
p_spam = 0.30            # 30% of incoming mail is spam (prior)
p_ham = 1 - p_spam

# Likelihoods: P(word appears | class), estimated from a labeled training set
p_free_given_spam, p_free_given_ham = 0.60, 0.05   # "free": 60% of spam, 5% of legit mail
p_win_given_spam, p_win_given_ham = 0.45, 0.03      # "win":  45% of spam, 3% of legit mail

print("=== Priors ===")
print("P(Spam) =", p_spam, " P(Ham) =", p_ham)

# Step 1: single word evidence -> "free" appears in the email
p_free = p_free_given_spam * p_spam + p_free_given_ham * p_ham
p_spam_given_free = (p_free_given_spam * p_spam) / p_free
print("\n=== Step 1: 'free' appears ===")
print(f"P('free') = {p_free_given_spam}*{p_spam} + {p_free_given_ham}*{p_ham} = {p_free:.4f}")
print(f"P(Spam | 'free') = ({p_free_given_spam}*{p_spam}) / {p_free:.4f} = {p_spam_given_free:.4f}")
print(f"-> Prior belief moved from {p_spam*100:.0f}% to {p_spam_given_free*100:.1f}% after one word")
```

**Output:**
```
=== Priors ===
P(Spam) = 0.3  P(Ham) = 0.7

=== Step 1: 'free' appears ===
P('free') = 0.6*0.3 + 0.05*0.7 = 0.2150
P(Spam | 'free') = (0.6*0.3) / 0.2150 = 0.8372
-> Prior belief moved from 30% to 83.7% after one word
```

### Update again with a second word (Naive Bayes independence assumption)

```python
print("=== Step 2: 'free' AND 'win' both appear (conditionally independent given class) ===")
joint_spam = p_free_given_spam * p_win_given_spam * p_spam
joint_ham = p_free_given_ham * p_win_given_ham * p_ham
p_evidence = joint_spam + joint_ham
p_spam_given_both = joint_spam / p_evidence

print(f"P('free','win'|Spam)*P(Spam) = {p_free_given_spam}*{p_win_given_spam}*{p_spam} = {joint_spam:.5f}")
print(f"P('free','win'|Ham) *P(Ham)  = {p_free_given_ham}*{p_win_given_ham}*{p_ham} = {joint_ham:.5f}")
print(f"P(Spam | 'free','win') = {joint_spam:.5f} / {p_evidence:.5f} = {p_spam_given_both:.4f}")

print("\n=== Belief update trail ===")
print(f"Prior P(Spam)                      = {p_spam*100:.1f}%")
print(f"After 'free'      -> P(Spam|free)  = {p_spam_given_free*100:.1f}%")
print(f"After 'free'+'win'-> P(Spam|both)  = {p_spam_given_both*100:.2f}%")
```

**Output:**
```
=== Step 2: 'free' AND 'win' both appear (conditionally independent given class) ===
P('free','win'|Spam)*P(Spam) = 0.6*0.45*0.3 = 0.08100
P('free','win'|Ham) *P(Ham)  = 0.05*0.03*0.7 = 0.00105
P(Spam | 'free','win') = 0.08100 / 0.08205 = 0.9872

=== Belief update trail ===
Prior P(Spam)                      = 30.0%
After 'free'      -> P(Spam|free)  = 83.7%
After 'free'+'win'-> P(Spam|both)  = 98.72%
```

**Teaching point (bridge to Module 3):** Each new word is new evidence updating a prior into a posterior — exactly the "prior → likelihood → posterior" loop from the disease example, applied to text. This is literally how a **Naive Bayes** text classifier works, and it is the conceptual ancestor of how a language model assigns a probability to the next token given everything written so far.

**Note the word "naive":** it comes from assuming the words are conditionally independent given the class — rarely exactly true in real language ("free" and "win" tend to co-occur in spammy phrasing), but the approximation works well enough to be one of the most widely deployed text classifiers in production.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Sample spaces and events — probability is just counting outcomes as a ratio
- Three rules: complement (P(A) + P(A')=1), addition (P(A∪B)=P(A)+P(B)-P(A∩B)), multiplication for independent events (P(A∩B)=P(A)×P(B))
- Conditional probability P(A|B) = P(A∩B)/P(B) — the entire foundation Bayes' Theorem is built from
- Derived Bayes' Theorem algebraically from the conditional probability definition, applied twice
- Worked the classic disease-test example by hand: prior 1%, sensitivity 99%, false-positive rate 5% → posterior only 16.67%, and how a second positive test pushes it to 79.84%
- Applied the same formula to spam filtering with word evidence, connecting Bayes to Naive Bayes classifiers and, ahead, to LLM token probabilities

**Bridge to next session:** *"We've spent today on the probability that underlies every 'confidence score' you've used this module. Next class, we go back to full pipelines: Dimensionality Reduction — compressing many features into few — and Time Series, where the 'evidence' arriving over time is exactly the kind of sequential update we just practiced with the two-positive-test example."*

**Homework / self-practice:** Pick any two everyday claims involving a "percentage accurate" test or filter (a spam folder, a security alarm, a COVID test, a lie detector). For each, estimate a plausible prior, sensitivity, and false-positive rate, and compute the actual posterior probability using Bayes' Theorem. Bring one surprising result to share next class.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Is Bayes' Theorem a machine learning algorithm?**
→ No — it's a mathematical identity, derived purely from the meaning of conditional probability. Naive Bayes is an ML *algorithm* that applies this theorem repeatedly with an independence assumption; today's formula has no "training" step, just arithmetic on known priors and likelihoods.

**Q: Where do the prior and likelihood numbers come from in real life?**
→ From data. The prior P(Disease) comes from population health statistics; the likelihoods come from clinical trials of the test. In a spam filter, both come from counting word frequencies in a labeled training set — exactly what a Naive Bayes classifier automates.

**Q: Why does P(A|B) ≠ P(B|A) trip people up so much?**
→ Natural language makes them sound interchangeable ("rain given clouds" vs "clouds given rain" — very different numbers). The card example (P(King|Face)=1/3 vs P(Face|King)=1) makes the asymmetry concrete — revisit it if confusion resurfaces.

**Q: If P(A∩B) = 0, are A and B independent?**
→ No — that's the opposite. P(A∩B)=0 means mutually exclusive. Independent means knowing one tells you nothing about the other; mutually exclusive events are actually strongly *dependent* — knowing A happened tells you B definitely did not.

**Q: Does a higher posterior always mean "act on it"?**
→ Not necessarily — that's decision theory layered on top of probability. A 16.67% posterior might still justify a confirmatory test depending on the cost of a missed case versus a false alarm. Bayes' Theorem gives the probability; what to *do* with it is a separate judgment call.

---

## Instructor Notes

- **Dataset/data notes:** Every example is fully synthetic and hand-specified (coins, dice, a standard 52-card deck, stated priors/likelihoods for disease and spam) — no external files needed. This keeps the arithmetic auditable.
- **Common student mistake:** Confusing P(A|B) with P(B|A) — many will answer "99%" on the disease hook because they're really answering P(+|Disease), not P(Disease|+). The card example pre-empts this before Bayes is introduced.
- **Live-coding tip:** Poll the room for guesses before revealing the disease-test output. The gap between the guess and 16.67% is the best teaching moment of the session — don't rush past it.
- **For advanced students:** Have them turn the sequential two-test update (Practical 3) into a loop that feeds the posterior back as the new prior for N tests, and find how many consecutive positives are needed to cross 99%.
- **Time-check contingency:** If running behind after the break, compress Concept Block 4's P(D)=0.5 board example to a verbal walk-through, and run Practical 4 as a live-typed demo rather than hands-on typing.
