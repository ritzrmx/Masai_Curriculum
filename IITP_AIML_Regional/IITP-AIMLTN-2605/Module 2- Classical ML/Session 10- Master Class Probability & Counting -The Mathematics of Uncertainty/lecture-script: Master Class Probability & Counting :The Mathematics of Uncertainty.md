# Lecture Script: Master Class — Probability & Counting: The Mathematics of Uncertainty
> **Instructor Reference** — Module 2: Classical ML | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can compute probabilities by hand — sample spaces, complements, unions, conditionals — and can derive and apply Bayes' theorem to the classic base-rate problem, then confirm every hand answer with a short simulation.

**Student profile at this point:** They have trained regression models, classifiers and clustering models. They know precision, recall and the confusion matrix from Session 8. They have **never formally studied probability** in this course. Assume rusty school-level maths and zero comfort with notation.

**Key outcome:** Students leave able to say *why* a 99%-accurate test for a rare disease is right only ~9% of the time when it fires — and able to prove it three ways: by formula, by a natural-frequency table, and by simulating 100,000 patients in NumPy.

**Tone for this session:** This is a **maths master class**. Hand first, code second. Every code block here exists only to *verify* a number the room already computed on paper. Do not open the laptop until the board answer is agreed.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The 99% Test That Is Wrong 91% of the Time | 5 min | 0:05 |
| **Concept 1:** Sample Space, Events, and the Complement Rule | 10 min | 0:15 |
| **Practical 1:** Simulating coins and dice — does the maths hold? | 15 min | 0:30 |
| **Concept 2:** Addition Rule, Mutually Exclusive vs Independent | 10 min | 0:40 |
| **Practical 2:** A deck of cards in Pandas — union and independence | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Conditional Probability — Shrink the World Down to B | 10 min | 1:15 |
| **Practical 3:** Two dice, contingency tables, conditioning by filtering | 15 min | 1:30 |
| **Concept 4:** Bayes' Theorem, Derived and Then Believed | 10 min | 1:40 |
| **Practical 4:** 100,000 patients — simulate the base-rate fallacy | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Do this before saying anything else.** Write on the board:

```
A disease affects 1 in 1,000 people.
A test for it is 99% accurate.
You test POSITIVE.
What is the chance you actually have the disease?
```

Take a show of hands: *"Who says above 90%? Above 50%? Below 20%?"* Most of the room will vote 99% or 90%. Let that sit, then say:

*"The answer is about 9%. Not 99. Nine. And by the end of today, every one of you will be able to derive that number three different ways — and you will never be fooled by it again."*

**Why this matters for AI/ML:** Session 8 taught you that precision collapses on rare classes — today you learn *the mathematical law that forces it to*. That same law is the engine of Naive Bayes, of spam filters, and of every fraud-alert system that keeps phoning innocent customers.

**What probability is NOT:**
- NOT a gut feeling about how confident you are
- NOT "99% accurate means 99% of my alerts are correct"
- NOT the same when you flip the bar: `P(A|B)` is not `P(B|A)`
- NOT something you need calculus for

**What probability IS:**
- Careful counting, divided by careful counting
- A number between 0 and 1, always
- A *language* for updating a belief when new evidence arrives
- Checkable — you can always simulate it and see

---

## Concept Block 1: Sample Space, Events, and the Complement Rule (10 min)

**Write these three lines on the board and circle them:**

```
Sample space  S  = the list of everything that could happen
Event         A  = a subset of S that you care about
P(A)             = count(A) / count(S)        [only if all outcomes are equally likely]
```

That last bracket is doing enormous work. Classical probability is *only* counting, and only when the outcomes are equally likely — a fair coin, a fair die, a shuffled deck.

| Experiment | Sample space | Size | Event | P |
|---|---|---|---|---|
| One coin | H, T | 2 | Heads | 1/2 |
| One die | 1..6 | 6 | Even | 3/6 = 1/2 |
| Two dice | all ordered pairs | 36 | Sum = 7 | 6/36 = 1/6 |
| One card | 52 cards | 52 | A King | 4/52 = 1/13 |

**Ask the room:** *"Why is the two-dice sample space 36 and not 21?"* Because (2,5) and (5,2) are different outcomes — the dice are distinguishable. This is the single most common counting error; call it out now.

### The complement rule

```
P(not A) = 1 − P(A)
```

Something must happen, so the two halves add to 1. Trivial-looking. Enormously useful.

**Board demo — the "at least one" trick.** Roll a die four times. P(at least one six)? *"Listing the ways to get one six, or two, or three, or four is a nightmare. So don't."*

```
P(no six on one roll)     = 5/6
P(no six on four rolls)   = (5/6)^4 = 625/1296 ≈ 0.4823
P(at least one six)       = 1 − 0.4823 ≈ 0.5177
```

**Write on the board in red:** *"'AT LEAST ONE' → compute the complement."*

---

## Practical Block 1: Simulating Coins and Dice (15 min)

### Hand first (5 min)

Get the room to agree on three numbers on paper before any code:
1. P(die shows 6) = 1/6 ≈ 0.167
2. P(at least one six in four rolls) = 1 − (5/6)⁴ ≈ 0.518
3. P(exactly two heads in three coin tosses) = 3/8 = 0.375 — enumerate: HHT, HTH, THH out of 8

### Then verify (10 min)

```python
import numpy as np

rng = np.random.default_rng(42)   # reproducible randomness
N = 100_000

# --- 1. A single die: P(six) should be about 0.167 ---
rolls = rng.integers(1, 7, size=N)          # integers 1..6
print("P(six), simulated :", (rolls == 6).mean())
print("P(six), by hand   :", 1/6)

# --- 2. At least one six in four rolls ---
four_rolls = rng.integers(1, 7, size=(N, 4))     # N experiments, 4 rolls each
at_least_one_six = (four_rolls == 6).any(axis=1) # True if ANY of the 4 is a six
print("\nP(at least one six), simulated :", at_least_one_six.mean())
print("P(at least one six), by hand   :", 1 - (5/6)**4)

# --- 3. Exactly two heads in three tosses ---
tosses = rng.integers(0, 2, size=(N, 3))    # 0 = tails, 1 = heads
heads_count = tosses.sum(axis=1)
print("\nP(exactly two heads), simulated :", (heads_count == 2).mean())
print("P(exactly two heads), by hand   :", 3/8)
```

**Expected output:** each simulated figure lands within about 0.005 of the hand-computed one — roughly 0.167, 0.518 and 0.375. They will not match to four decimals, and that is the point.

**Live walk-through:** Point at `.any(axis=1)` — *"That single call is the complement rule made mechanical: I never counted the sixes, I only asked whether zero happened."* Then ask the room: *"Why doesn't the simulation give exactly 0.5177?"* Answer: 100,000 trials is a sample, not the truth. Re-run with `N = 1_000` and let them watch the answer wobble by 2–3 percentage points; re-run with `N = 1_000_000` and watch it tighten. **Simulation approaches the maths, it does not replace it.**

---

## Concept Block 2: Addition Rule, Mutually Exclusive vs Independent (10 min)

### The addition rule and the wedding-guest problem

**Board:**

```
P(A or B) = P(A) + P(B) − P(A and B)
```

*"Two families send guest lists for a wedding. Add both lists to order the food, and you over-order — the cousins who appear on both lists got counted twice. Subtract them once."*

**Draw two overlapping circles (Venn).** Shade the lens in the middle. *"This region is inside A and inside B. When I add the circles, I add the lens twice. So I take it away once."*

**Worked on the board — one card from a deck:**

```
P(King)            = 4/52
P(Heart)           = 13/52
P(King and Heart)  = 1/52       (the King of Hearts, one card)
P(King or Heart)   = 4/52 + 13/52 − 1/52 = 16/52 ≈ 0.308
```

*"Skip the subtraction and you get 17/52 — you have just invented a second King of Hearts."*

### The distinction that ruins exam papers

| | Mutually exclusive | Independent |
|---|---|---|
| Can both happen together? | Never | Yes |
| P(A and B) = | 0 | P(A) × P(B) |
| Does knowing A tell you about B? | Yes — everything | No — nothing |
| Card example | King and Queen | King and Heart |

**Say this out loud, slowly:** *"Mutually exclusive events are the most DEPENDENT events that exist. If I tell you the card is a King, you now know with total certainty it is not a Queen. That is a mountain of information. Independence means the opposite — learning A changes nothing."*

### The multiplication rule

```
P(A and B) = P(A) × P(B)      -- ONLY for independent events
```

Test it: P(King) × P(Heart) = (1/13) × (1/4) = 1/52. And the deck really contains exactly one King of Hearts. The rule holds, so suit and rank are independent.

Two coins: P(both heads) = 1/2 × 1/2 = 1/4. *"And no — five heads in a row does not make tails 'due'. Coins have no memory. That belief has a name: the gambler's fallacy."*

---

## Practical Block 2: A Deck of Cards in Pandas (15 min)

### Hand first (4 min)

Get the room to state, on paper: P(King or Heart) = 16/52 ≈ 0.3077, and P(King and Heart) = 1/52 ≈ 0.0192.

### Then verify (11 min)

```python
import numpy as np
import pandas as pd

# --- Build a full 52-card deck, then draw 200,000 cards WITH replacement ---
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck  = pd.DataFrame([(r, s) for r in ranks for s in suits], columns=['rank', 'suit'])
draws = deck.sample(n=200_000, replace=True, random_state=42)

is_king  = draws['rank'] == 'K'
is_heart = draws['suit'] == 'Hearts'
is_queen = draws['rank'] == 'Q'

print("--- Addition rule ---")
print("P(King)            :", round(is_king.mean(), 4),  " by hand 4/52  =", round(4/52, 4))
print("P(Heart)           :", round(is_heart.mean(), 4), " by hand 13/52 =", round(13/52, 4))
print("P(King and Heart)  :", round((is_king & is_heart).mean(), 4), " by hand 1/52  =", round(1/52, 4))
print("P(King or Heart)   :", round((is_king | is_heart).mean(), 4), " by hand 16/52 =", round(16/52, 4))

# --- Independence check: does P(A and B) equal P(A) x P(B)? ---
product, joint = is_king.mean() * is_heart.mean(), (is_king & is_heart).mean()
print("\nP(King) x P(Heart) :", round(product, 4), " vs  P(King and Heart):", round(joint, 4))
print("Independent?       :", np.isclose(product, joint, atol=0.003))

# --- Mutually exclusive check: a card cannot be both a King and a Queen ---
print("\nP(King and Queen)  :", (is_king & is_queen).mean(), "  <- exactly 0, cannot co-occur")
print("P(King or Queen)   :", round((is_king | is_queen).mean(), 4), " by hand 8/52  =", round(8/52, 4))
```

**Expected output:** the simulated union lands near 0.308, the joint near 0.019, and `P(King and Queen)` is exactly `0.0`.

**Live walk-through:** Stop on the two boolean operators. *"`&` is the word AND — the overlap. `|` is the word OR — the union."* Then ask: *"P(King and Queen) came out as exactly zero, not approximately zero. Why is that different from every other number on this screen?"* Because it is a structural impossibility, not a rare event — no sample size will ever produce one.

---

## BREAK (10 min)

*Think about this while you get chai: a test is 99% accurate. Ten thousand healthy people take it. How many of them does it wrongly accuse? Now — how many sick people were even in the room to begin with?*

---

## Concept Block 3: Conditional Probability — Shrink the World Down to B (10 min)

### The one sentence that carries the whole concept

*"You lost your keys. They could be anywhere in the house. Then someone says: 'I saw them in the kitchen.' Nothing about the keys changed. Your WORLD changed — it shrank from a house to a room. Conditional probability is the arithmetic of that shrinking."*

**Board:**

```
P(A | B) = P(A and B) / P(B)

           ^ top:    the part of the new world where A is also true
                ^ bottom: the NEW WORLD — everything where B is true
```

Read the bar `|` out loud as the word **"given"**.

### Board demo — one die

```
A = "the roll is a six"          P(A) = 1/6
B = "the roll is even"           P(B) = 3/6 = 1/2

P(A and B) = 1/6                 (a six IS even, so the overlap is just the six)

P(A | B) = (1/6) / (1/2) = 1/3
```

*"Being told 'it's even' doubled the chance of a six, from 1/6 to 1/3. Evidence moved the number. That is what evidence DOES."*

### The mistake that Bayes exists to fix

**Write both on the board and box them:**

```
P(four legs | it's a dog)  ≈  1.0
P(it's a dog | four legs)  ≈  small — cats, cows, tables, goats...
```

**Say:** *"Same two events. Bar flipped. Wildly different answers. Anyone who says '99% accurate, therefore 99% of positives are sick' has flipped the bar without permission. Bayes' theorem is the licence to flip it — legally."*

---

## Practical Block 3: Two Dice and Contingency Tables (15 min)

### Hand first (5 min)

Two fair dice. Let A = "sum is 10 or more", B = "the first die shows a 6".

Have the room compute both on paper:
- P(A) unconditionally: sums of 10, 11, 12 → outcomes (4,6)(5,5)(6,4)(5,6)(6,5)(6,6) = 6 out of 36 = **1/6 ≈ 0.167**
- P(A | B): if the first die is already a 6, the sum reaches 10 only if the second is 4, 5 or 6 → **3/6 = 0.5**

*"Knowing the first die is a six tripled the probability. Write that down — it is the whole idea."*

### Then verify (10 min)

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 200_000

die1 = rng.integers(1, 7, size=N)
die2 = rng.integers(1, 7, size=N)
total = die1 + die2

A = total >= 10       # event A: sum is 10 or more
B = die1 == 6         # event B: first die shows a six

print("P(A)      unconditional :", round(A.mean(), 4), "  by hand 6/36 =", round(6/36, 4))
print("P(A and B)              :", round((A & B).mean(), 4), "  by hand 3/36 =", round(3/36, 4))

# --- Conditioning = FILTERING. Shrink the world to B, then recount. ---
print("\nP(A | B) by filtering   :", round(A[B].mean(), 4))   # only rows where B is True
print("P(A | B) by formula     :", round((A & B).mean() / B.mean(), 4))
print("P(A | B) by hand        :", round(3/6, 4))

# --- The same story as a contingency table. Each ROW is a conditional distribution. ---
print("\nRow proportions — each row is P(A | that row):")
print(pd.crosstab(B, A, rownames=['first die is 6'], colnames=['sum >= 10'],
                  normalize='index').round(3))
```

**Expected output:** `P(A)` lands near 0.167, `P(A | B)` near 0.500, and the `True` row of the normalised table reads roughly `0.5 / 0.5` while the `False` row reads roughly `0.9 / 0.1`.

**Live walk-through:** Land hard on the line `A[B].mean()`. *"That is conditional probability with the mask off. `[B]` throws away every experiment where B did not happen. `.mean()` recounts inside what survives. Shrink the world; recount. That is all the formula ever said."* Then point at the two rows of the crosstab: *"Same dice, same universe — but the row you are standing in completely changes the odds. That is what it means for evidence to be informative."*

---

## Concept Block 4: Bayes' Theorem, Derived and Then Believed (10 min)

### Derive it live — do not show a finished formula

**Step 1.** There are two honest ways to write the probability of "A and B":

```
P(A and B) = P(A | B) × P(B)          ... rearranged from Concept 3
P(A and B) = P(B | A) × P(A)          ... same thing, roles swapped
```

**Step 2.** They describe the same event, so they are equal:

```
P(A | B) × P(B) = P(B | A) × P(A)
```

**Step 3.** Divide both sides by P(B):

```
              P(B | A) × P(A)
   P(A | B) = ---------------
                    P(B)
```

*"That is Bayes' theorem. Three lines. No calculus. It is nothing but conditional probability, read backwards."*

### Name the parts

| Piece | Name | In plain words |
|---|---|---|
| P(A) | **Prior** | What you believed before any evidence |
| P(B\|A) | **Likelihood** | How well the evidence fits the hypothesis |
| P(B) | **Evidence** | How likely that evidence was, over all hypotheses |
| P(A\|B) | **Posterior** | Your updated belief |

**Write across the board:** `PRIOR + EVIDENCE = POSTERIOR`

### The medical test — by hand, with 100,000 people

**Do not use the formula yet.** Draw this table live and fill it in with the class:

*Disease affects 1 in 1,000. Test is 99% accurate (99% of sick people test positive; 99% of healthy people test negative).*

| Out of 100,000 people | Count | Test positive | Test negative |
|---|---|---|---|
| Actually have the disease | 100 | 99 | 1 |
| Actually healthy | 99,900 | 999 | 98,901 |
| **Total** | **100,000** | **1,098** | **98,902** |

**Now just read the answer off the table:**

```
P(disease | positive) = 99 / 1098 ≈ 0.090  →  about 9%
```

**And confirm with the formula:**

```
P(+|D) × P(D)            0.99 × 0.001         0.00099
------------------  =  ------------------  =  --------  ≈ 0.090
      P(+)              0.00099 + 0.00999      0.01098
```

*"The base rate is the villain. There are 999 healthy people for every sick one, so even a 1% error rate on the healthy crowd manufactures 999 false alarms — ten times more than the 99 real cases. The test isn't bad. The disease is just rare."*

**Connect it back — this is Session 8's precision.** `precision = TP / (TP + FP) = 99 / 1098 = 9%`. Recall is a magnificent 99%. Precision is a miserable 9%. *"When you saw precision collapse on an imbalanced dataset in Session 8, THIS was the reason. Bayes was under the bonnet the whole time."*

**Forward pointer:** A classifier that computes exactly this — a prior per class, a likelihood per feature, pick the biggest posterior — has a name: **Naive Bayes**. It is the reason your Gmail spam folder works.

---

## Practical Block 4: 100,000 Patients (10 min)

```python
import numpy as np

rng = np.random.default_rng(42)

PREVALENCE  = 0.001   # 1 in 1,000 people have the disease
SENSITIVITY = 0.99    # P(test positive | diseased)
SPECIFICITY = 0.99    # P(test negative | healthy)
N = 100_000

# --- Step 1: who is actually ill? ---
has_disease = rng.random(N) < PREVALENCE

# --- Step 2: run the test. Ill people test positive 99% of the time;
#             healthy people test positive 1% of the time (a false alarm). ---
p_test_positive = np.where(has_disease, SENSITIVITY, 1 - SPECIFICITY)
tests_positive  = rng.random(N) < p_test_positive

# --- Step 3: build the confusion matrix by hand ---
TP = ( has_disease &  tests_positive).sum()
FP = (~has_disease &  tests_positive).sum()
FN = ( has_disease & ~tests_positive).sum()
TN = (~has_disease & ~tests_positive).sum()

print(f"Actually diseased : {has_disease.sum():>6}")
print(f"Tested positive   : {tests_positive.sum():>6}")
print(f"  True positives  : {TP:>6}")
print(f"  False positives : {FP:>6}   <-- the healthy people we frightened")

print(f"\nP(disease | positive), simulated : {TP / (TP + FP):.4f}")

# --- Step 4: Bayes' theorem, same number, no simulation ---
p_pos = SENSITIVITY * PREVALENCE + (1 - SPECIFICITY) * (1 - PREVALENCE)
posterior = (SENSITIVITY * PREVALENCE) / p_pos
print(f"P(disease | positive), by Bayes  : {posterior:.4f}")

print(f"\nRecall    (caught the sick people) : {TP / (TP + FN):.2f}")
print(f"Precision (positives that are real): {TP / (TP + FP):.2f}   <-- Session 8, remember?")
```

**Expected output:** roughly 100 diseased people, roughly 1,100 positive tests, and a simulated `P(disease | positive)` in the neighbourhood of 0.09 — sitting right next to the Bayes value of 0.0902. Recall will read at or near 1.00 (with only ~100 sick people, the one expected false negative often does not appear); precision will read about 0.09.

**Live walk-through:** Freeze on the two numbers side by side — the simulation and Bayes. *"I never told the computer the formula. I just built 100,000 fake patients and counted. The universe agrees with the algebra."* Then ask the room the closing question: *"You are building a fraud detector. Fraud is 1 in 2,000 transactions. Your model is 99% accurate. Your manager wants an SMS sent on every positive. How many innocent customers do you wake up at 2 a.m.?"* Let them do the arithmetic in their heads. That is the lesson of the day.

---

## Summary & Wrap-Up (5 min)

**The spine of today:**

1. **P(A) = favourable / total** — probability is counting, when outcomes are equally likely
2. **Complement:** `P(not A) = 1 − P(A)` — and "at least one" always means "1 minus none"
3. **Addition:** `P(A or B) = P(A) + P(B) − P(A and B)` — subtract the overlap or you double-count
4. **Mutually exclusive ≠ independent** — exclusive events are maximally *dependent*
5. **Multiplication:** `P(A and B) = P(A) × P(B)` — for independent events only
6. **Conditional:** `P(A|B) = P(A and B) / P(B)` — shrink the world to B, then recount
7. **Bayes:** `P(A|B) = P(B|A) × P(A) / P(B)` — prior + evidence = posterior
8. **The base rate rules everything.** A great test for a rare thing still mostly cries wolf.

**Bridge:** *"Today we handled uncertainty in one or two variables. Next session — **Dimensionality Reduction & Time Series** — we face the opposite problem: datasets with a hundred columns, most of them redundant. You will learn to squeeze them down to the few directions that actually carry the signal, and to handle data where the order of the rows finally matters."*

---

## Q&A & Doubt Solving (5 min)

**Q: If the test is 99% accurate, how can it be right only 9% of the time?**
→ Both are true; they answer different questions. "99% accurate" is `P(positive | diseased)` — of the sick, 99% get flagged. "9%" is `P(diseased | positive)` — of the flagged, 9% are sick. The bar is flipped. There are 999 healthy people for every sick one, so the healthy crowd's 1% error rate produces far more positives in raw numbers than the sick crowd's 99% success rate.

**Q: Are mutually exclusive events independent?**
→ Almost never — they are the *opposite*. Independence needs `P(A and B) = P(A) × P(B)`. For exclusive events `P(A and B) = 0` while `P(A) × P(B) > 0`, so the equation fails. Knowing A happened tells you B definitely did not: that is maximal dependence.

**Q: How do I know if two real-world events are independent? I can't check every deck of cards.**
→ Test it on data: compute `P(A and B)` from your dataset and compare it to `P(A) × P(B)`. If they are close, independence is a reasonable working assumption. Naive Bayes is called "naive" precisely because it *assumes* all features are independent given the class — usually false, but the classifier works surprisingly well anyway.

**Q: Where does the prior come from if I have no data?**
→ Usually the base rate — how common the thing is in the population (disease prevalence, fraud rate, spam rate). With genuinely nothing, people start from a flat prior and let evidence do the work. But an honest prior beats a clever likelihood: get the base rate wrong and your posterior is wrong however good your test is.

**Q: If simulations agree with the formula, why bother with the formula?**
→ Simulation only approximates, and needs enormous N for rare events (try a 1-in-10-million disease). It cannot tell you *why* an answer is what it is. And you cannot put a simulation inside a training loop — Naive Bayes needs the closed form.

---

## Instructor Notes

- **Nothing to install.** Only `numpy` and `pandas`, both already in their environment. `np.random.default_rng(42)` is the modern NumPy generator — if a student's NumPy predates 1.17, `np.random.seed(42)` plus the legacy functions works identically.
- **Resist the laptop.** Every practical block here is scaffolded as *hand-compute, agree as a room, then verify*. If you invert that order, students stop doing the algebra.
- **The single most common student mistake:** flipping the conditional bar — reading `P(positive | diseased)` as if it meant `P(diseased | positive)`. Pre-empt it in Concept 3 with the dog/four-legs example and keep pointing back to it. It *will* resurface in Concept 4. The runner-up mistake is treating "mutually exclusive" and "independent" as synonyms; the table in Concept 2 is the antidote.
- **Natural frequencies beat formulas.** If the room glazes over during the Bayes algebra, abandon it and go straight to the 100,000-people table — people reason correctly with counts and incorrectly with percentages. Land the intuition, then return to the formula as "the shorthand for what we just did".
- **Pacing:** Concept 4 plus Practical 4 are the point of the whole session. If you are running late, compress Practical 2 (the card deck) — it is the most cuttable block. Never compress the medical test.
- **For advanced students:** ask them to iterate Bayes — take the 9% posterior as the new prior and run a *second independent* test. The posterior jumps to roughly 90%. That is why doctors retest, and it is a clean demonstration of belief updating in sequence.
