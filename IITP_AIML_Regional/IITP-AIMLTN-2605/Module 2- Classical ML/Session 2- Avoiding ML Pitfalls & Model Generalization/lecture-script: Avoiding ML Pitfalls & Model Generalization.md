# Lecture Script: Avoiding ML Pitfalls & Model Generalization
> **Instructor Reference** — Module 2: Classical ML | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students learn to tell a model that has *learned* from a model that has *memorised* — diagnosing overfitting and underfitting from scores and learning curves, producing a trustworthy estimate with k-fold cross-validation, and auditing any workflow for the three forms of data leakage.

**Student profile at this point:** After Session 1 they can call `train_test_split`, `.fit()`, `.predict()` and `.score()`. They have trained one or two models in their life. Most instinctively believe a higher training score means a better model. That belief is what this session dismantles.

**Key outcome:** A working "generalisation audit" notebook: the degree-1 / 4 / 15 comparison, a learning-curve diagnostic, a `cross_val_score` evaluation, and leaky-vs-clean demos that show leakage inflating a score in front of their eyes.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The 100% Accurate Model That Is Worthless | 5 min | 0:05 |
| **Concept 1:** Generalisation, Overfitting and Underfitting | 10 min | 0:15 |
| **Practical 1:** The degree 1 / 4 / 15 polynomial experiment | 15 min | 0:30 |
| **Concept 2:** The Bias–Variance Tradeoff and Learning Curves | 10 min | 0:40 |
| **Practical 2:** Plotting and reading learning curves | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Train / Validation / Test and k-Fold CV | 10 min | 1:15 |
| **Practical 3:** Three-way split, then `cross_val_score` and `KFold` | 15 min | 1:30 |
| **Concept 4:** Data Leakage — The Three Kinds | 10 min | 1:40 |
| **Practical 4:** Leakage demos and the `Pipeline` fix | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — perform this live, before any theory.** Put this on the screen and run it:

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)
print("Accuracy:", model.score(X, y))   # prints 1.0
```

Let the number land. Then say it out loud:

*"This model is 100% accurate. Should we ship it to a hospital tomorrow?"*

Wait for the room. Someone will say "no" but struggle to say why. Then reveal the trick: we scored the model on the exact same rows we trained it on. We asked the student to sit an exam made entirely of questions from the homework she just finished. Of course she got 100%.

**What a good model is NOT:**
- A model that fits the training data perfectly
- A model with the highest score you have seen so far
- A model you evaluated on data it has already seen

**What a good model IS:**
- A model that performs on rows it has **never** encountered
- A model whose score you can defend to someone who will bet money on it
- A model whose evaluation process you could publish without embarrassment

Write this on the board and leave it there all session:

```
    TRAINING SCORE  =  how well it memorised
    TEST SCORE      =  how well it learned
```

---

## Concept Block 1: Generalisation, Overfitting and Underfitting (10 min)

### The core definition (board)

```
GENERALISATION = performance on data the model has never seen.
That is the ONLY thing we care about. Everything else today
is a technique for measuring it honestly.
```

### The two failure modes

Every failed model fails in one of two directions. There is no third.

| | Underfitting | Overfitting |
|---|---|---|
| The model is | Too simple | Too flexible |
| It learned | Not enough | Too much — including the noise |
| Train score | Low | High |
| Test score | Low | Much lower than train |
| Everyday version | Read only the chapter headings | Memorised the textbook word for word, understood nothing |

### The signal to teach them: **the gap**

Write this formula on the board and make them copy it:

```
    gap = train_score - test_score

    gap ≈ 0, both scores low   →  UNDERFITTING (high bias)
    gap ≈ 0, both scores high  →  GOOD FIT
    gap large                  →  OVERFITTING (high variance)
    test > train, by a lot     →  something is broken; check your split
```

### Signal vs noise

Every dataset is `signal + noise`. The **signal** is the real pattern that will repeat in future data. The **noise** is random junk — measurement error, a customer who behaved oddly that day, monsoon traffic on a Tuesday. An underfit model misses part of the signal. An overfit model fits the signal *and then keeps going* and fits the noise too — and since the noise never repeats, everything learned from it is actively wrong.

**Key line to say:** *"Overfitting is not a bug in your code. Your code ran perfectly. It is a bug in your judgement."*

---

## Practical Block 1: The Degree 1 / 4 / 15 Experiment (15 min)

This is the single most important 15 minutes of the session. Type it live.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Build a small, noisy dataset with a KNOWN true pattern ---
rng = np.random.RandomState(42)
X = rng.uniform(0, 1, 40).reshape(-1, 1)          # 40 points between 0 and 1
y = np.sin(2 * np.pi * X).ravel() + rng.normal(0, 0.3, 40)   # true curve + noise

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
print("Train rows:", len(X_train), "| Test rows:", len(X_test))   # 30 | 10
```

Pause here. **State the truth of the universe out loud:** the real pattern is a sine wave. The `rng.normal(0, 0.3, 40)` is noise — it will never repeat. In real life you never get to know this. Today you do, which is the whole point.

```python
# --- Fit three models of increasing flexibility ---
grid = np.linspace(0, 1, 300).reshape(-1, 1)   # smooth grid, just for drawing
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for ax, degree in zip(axes, [1, 4, 15]):
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)

    train_r2 = model.score(X_train, y_train)
    test_r2  = model.score(X_test,  y_test)

    ax.scatter(X_train, y_train, color='steelblue', label='train', s=35)
    ax.scatter(X_test,  y_test,  color='coral', marker='^', label='test', s=45)
    ax.plot(grid, model.predict(grid), color='black', lw=2, label=f'degree {degree}')
    ax.plot(grid, np.sin(2 * np.pi * grid), color='green', ls='--', lw=1.5,
            label='true pattern')
    ax.set_ylim(-2, 2)
    ax.set_title(f"Degree {degree}\ntrain R2 = {train_r2:.2f} | test R2 = {test_r2:.2f}")
    ax.legend(fontsize=7)

plt.suptitle("Same data, three levels of flexibility", fontsize=13)
plt.tight_layout()
plt.show()
```

**Expected pattern of results** (run it once before class to confirm on your machine):

| Degree | Train R² | Test R² | Gap | Verdict |
|---|---|---|---|---|
| 1 | ≈ 0.47 | ≈ 0.29 | 0.18 | Underfit — a line cannot bend |
| 4 | ≈ 0.85 | ≈ 0.79 | 0.06 | Just right — tracks the green curve |
| 15 | ≈ 0.94 | ≈ 0.47 | 0.47 | Overfit — best train score, worst gap |

**Live walk-through:** Point at the degree-15 panel. The black curve threads through the blue training dots almost perfectly — and misses the orange test triangles by a mile. Now point at the *numbers*. Degree 15 has the **highest training score of all three**. Ask the room:

*"If I had only shown you the training scores, which model would you have picked? And what would that have cost you?"*

Then make them compute the gap themselves: degree 15 gives `0.94 - 0.47 = 0.47`. Degree 4 gives `0.85 - 0.79 = 0.06`. The gap, not the score, is the diagnosis.

---

## Concept Block 2: Bias, Variance, and the Learning Curve (10 min)

### Bias and variance in plain language (board)

```
BIAS     = error from the model being TOO SIMPLE. Wrong the same way every time.
VARIANCE = error from the model being TOO SENSITIVE to the exact rows it saw.
           Change the rows slightly and the predictions swing wildly.
```

The darts image works well here: high bias is a tight cluster in the wrong corner. High variance is a wide scatter centred on the bullseye. You want tight *and* centred, and you can rarely have both perfectly.

### The tradeoff

| Model complexity | Bias | Variance | Total test error |
|---|---|---|---|
| Very low (degree 1) | High | Low | High |
| **Sweet spot (degree 4)** | Moderate | Moderate | **Lowest** |
| Very high (degree 15) | Low | High | High |

Total error goes *down* then back *up* as you add complexity. It is a U-shape. Your job is to find the bottom of the U — and Practical 3 will show you how to find it without cheating.

### The learning curve — a free diagnostic

A **learning curve** plots training score and validation score against the *number of training rows used*. Three shapes, three verdicts:

| Shape | Diagnosis | Action |
|---|---|---|
| Both curves converge **low** | High bias / underfit | More data will NOT help. Change the model. |
| Curves stay far **apart** | High variance / overfit | More data WILL help. Or simplify. |
| Both converge **high**, close | Healthy | Stop tuning complexity. |

**Say this and repeat it:** *"The learning curve is the only tool that tells you whether more data is worth collecting. If your model is underfitting, another 10,000 rows will change nothing — and you were about to spend a month getting them."*

---

## Practical Block 2: Plotting and Reading Learning Curves (15 min)

We need more rows for a clean curve, so regenerate the same sine data at n = 300.

```python
from sklearn.model_selection import learning_curve, KFold

# Same underlying truth, more rows
rng = np.random.RandomState(42)
X_big = rng.uniform(0, 1, 300).reshape(-1, 1)
y_big = np.sin(2 * np.pi * X_big).ravel() + rng.normal(0, 0.3, 300)

cv = KFold(n_splits=5, shuffle=True, random_state=42)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

for ax, degree in zip(axes, [1, 4, 15]):
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    sizes, train_scores, val_scores = learning_curve(
        model, X_big, y_big,
        cv=cv,
        train_sizes=np.linspace(0.15, 1.0, 6),
        scoring='r2',
        shuffle=True, random_state=42)      # shuffle=True matters — see note below

    ax.plot(sizes, train_scores.mean(axis=1), 'o-', color='steelblue', label='train')
    ax.plot(sizes, val_scores.mean(axis=1),  's-', color='coral',     label='validation')
    ax.set_ylim(-0.2, 1.05)
    ax.set_xlabel("Training rows used")
    ax.set_title(f"Degree {degree}")
    ax.grid(alpha=0.3)
    ax.legend()

axes[0].set_ylabel("R² score")
plt.suptitle("Learning curves — the shape IS the diagnosis", fontsize=13)
plt.tight_layout()
plt.show()
```

**What you will see** (verify on your machine before class):

- **Degree 1:** both lines flatten out together around R² ≈ 0.5. They have already converged. This is high bias. More rows are pointless.
- **Degree 4:** both lines converge around R² ≈ 0.84 with a small gap. This is what healthy looks like.
- **Degree 15:** the validation line starts *catastrophically* low (a large negative R² with only ~36 training rows) and climbs steeply as rows are added, eventually meeting the training line. This is high variance — and the rising validation curve is literally the model saying *"give me more data and I will be fine."*

**Live walk-through:** Cover the titles with your hand and ask the room to diagnose each panel from the shape alone. Then ask the killer question: *"Your manager offers ₹5 lakh to buy 10,000 more rows of data. Looking at the degree-1 panel — do you take the money?"* (No. Those curves have already converged. Spend it on better features instead.)

> **Instructor note on `shuffle=True`:** `learning_curve` takes the *first* n rows of each training fold. If your data is sorted, the small-n models only ever see one end of the range and produce absurd scores. `shuffle=True, random_state=42` fixes it. A real trap — mention it, students will hit it.

---

## BREAK (10 min)

*Think about this while you get chai: in Practical 1, degree 15 had the highest training score of all three models. If a colleague showed you only that number and asked for your sign-off — what single question would you ask them before saying yes?*

---

## Concept Block 3: Train / Validation / Test and k-Fold CV (10 min)

### Why two sets are not enough

Here is the trap almost every beginner falls into:

```
1. Split into train and test.
2. Try degree 1  → test score 0.29
3. Try degree 4  → test score 0.79
4. Try degree 15 → test score 0.47
5. "Degree 4 is best! Our model scores 0.79."
```

Step 5 is a lie. You used the test set to *choose* the model. The test set is no longer unseen — it participated in the decision. Your 0.79 is optimistic, because you picked the degree that happened to suit those 10 particular test rows.

### The three-way split (board)

```
  ┌──────────── 60% ────────────┬──── 20% ────┬──── 20% ────┐
  │           TRAIN             │  VALIDATION │    TEST     │
  │        .fit() the model     │ choose the  │ report ONCE │
  │                             │   model     │  at the end │
  └─────────────────────────────┴─────────────┴─────────────┘
```

| Set | Used to | How often you may look |
|---|---|---|
| Train | Fit parameters | Always |
| Validation | Compare candidate models | As often as you like |
| Test | Report the final, honest number | **Exactly once** |

**Say it plainly:** *"The moment a dataset influences a decision, it is contaminated. The test set gets exactly one look, on the last day, and whatever number it gives you is the number you report — even if you hate it."*

### k-fold cross-validation

With 40 rows, a 20% validation set is 8 rows. Eight rows is nothing — your entire model-selection decision would hinge on which 8 rows landed there. **k-fold cross-validation** fixes this: split into k folds, train k times, each time holding out a different fold, then average.

```
Fold 1: [TEST][----------- train -----------]  → score 1
Fold 2: [--][TEST][-------- train --------]    → score 2
Fold 3: [-----][TEST][----- train --------]    → score 3
Fold 4: [--------][TEST][-- train --------]    → score 4
Fold 5: [------------ train ---------][TEST]   → score 5

              report:  mean ± standard deviation
```

**The standard deviation is not optional.** `0.78 ± 0.11` is a dependable model. `0.78 ± 0.40` means one fold collapsed and the average is hiding a disaster. Always print both.

---

## Practical Block 3: Three-Way Split, then `cross_val_score` (15 min)

### Part A — the honest three-way split

```python
# Reuse the original 40-point dataset (X, y) from Practical 1.

# Split 1: hold out 40% for later
X_train, X_rest, y_train, y_rest = train_test_split(
    X, y, test_size=0.4, random_state=42)

# Split 2: cut that 40% in half → 20% validation, 20% test
X_val, X_test, y_val, y_test = train_test_split(
    X_rest, y_rest, test_size=0.5, random_state=42)

print(f"train={len(X_train)}  val={len(X_val)}  test={len(X_test)}")   # 24  8  8

# Choose the degree using VALIDATION only. The test set stays in the drawer.
val_scores = {}
for degree in [1, 2, 3, 4, 6, 9, 15]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)
    val_scores[degree] = model.score(X_val, y_val)
    print(f"degree {degree:2d}  ->  validation R2 = {val_scores[degree]:.3f}")

best_degree = max(val_scores, key=val_scores.get)
print(f"\nWinner on validation: degree {best_degree}")

# NOW — and only now — open the test set. Once.
final = make_pipeline(PolynomialFeatures(best_degree), LinearRegression())
final.fit(X_train, y_train)
print(f"FINAL honest test R2 = {final.score(X_test, y_test):.3f}")
```

The validation scores jump sharply from degree 2 to degree 3, then slide steadily downwards as the model gets more flexible; degree 3 wins and degree 15 is far worse. The final honest test R² lands in the low-to-mid 0.8s — and that is the number you report, full stop.

Note how small the validation set is: **8 rows**. The entire model-selection decision rests on 8 data points. That fragility is exactly the problem Part B solves.

### Part B — the same job, done properly with k-fold

```python
from sklearn.model_selection import cross_val_score, KFold

cv = KFold(n_splits=5, shuffle=True, random_state=42)

print("degree |   mean R2  |   std   | individual folds")
print("-" * 60)
for degree in [1, 2, 3, 4, 6, 9, 15]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    scores = cross_val_score(model, X, y, cv=cv)      # 5 fits, 5 scores
    print(f"  {degree:2d}   |   {scores.mean():7.3f}  | {scores.std():7.3f} | "
          f"{np.round(scores, 2)}")
```

**Live walk-through:** Three things to call out, in this order.

1. **The middle degrees cluster together** — degrees 3, 4, 6 and 9 all land around R² ≈ 0.70–0.74. Cross-validation is telling you these are basically the same model. The single-split experiment made one of them look uniquely special; it was not.
2. **Look at the individual folds for degree 15.** Four folds look ordinary and one is a catastrophic large negative number, which drags the mean into nonsense. Ask: *"What does one exploding fold tell you about this model?"* (That it is wildly unstable on data it has not seen — that IS high variance.)
3. **The standard deviation is the story.** Degree 3's `std` is small; degree 15's is astronomical. Even before you look at the means, the spread has already told you which model you can trust.
4. **`shuffle=True` is doing real work.** Without it, `KFold` slices the data in order. If your CSV happens to be sorted by date or by label, your folds are not representative. Make them add it every time.

*"Which number would you put in a report — the flattering single-split score, or the cross-validated mean with its standard deviation?"* The second. It is lower, and it is true.

---

## Concept Block 4: Data Leakage — The Three Kinds (10 min)

This is the block that will save their careers. Slow down here.

**Data leakage** = information that will not be available at prediction time leaks into training. The model scores brilliantly in your notebook and falls apart in production.

### Kind 1 — Preprocessing leak (the one *everybody* does)

```python
# WRONG — the scaler saw every row, including the test rows
X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, ... = train_test_split(X_scaled, y)

# RIGHT — the scaler only ever learns from training rows
X_train, X_test, ... = train_test_split(X, y)
scaler = StandardScaler().fit(X_train)      # fit on train ONLY
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)        # test is transformed, never fitted
```

The mean and standard deviation a scaler computes are *learned parameters*. Fit them on all rows and your training data carries a whisper of the test set. On toy data the score damage is small; with outliers, small test sets, or feature selection done before the split, it can be enormous. **The process is wrong regardless of whether you can see the damage today.**

### Kind 2 — Target leakage (the most expensive)

A feature that secretly contains the answer.

| Predicting | Leaky feature | Why it leaks |
|---|---|---|
| Will the student pass? | `final_marks` | Pass is *defined* by final marks |
| Will this customer churn? | `cancellation_reason` | Only exists after they churned |
| Will this loan default? | `recovery_agent_assigned` | Only assigned after default |
| Will this ride take > 30 min? | `actual_fare_paid` | Fare depends on the duration |

**The test question — burn this into their heads:** *"At the moment I need to make this prediction, would I actually have this value?"* If the answer is no, the column must go.

### Kind 3 — Duplicate leak

The same row appears twice in the dataset. One copy goes to train, the other to test — the model has literally memorised the answer. Common causes: merging two exports, re-running an ETL job, a customer registering twice. **Fix:** `df = df.drop_duplicates()` **before** the split, every single time.

### The golden rule (board, in big letters)

```
IF THE SCORE LOOKS TOO GOOD TO BE TRUE — IT IS. Go and find the leak.
```

---

## Practical Block 4: Leakage Demos and the `Pipeline` Fix (10 min)

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.pipeline import make_pipeline
```

### Demo 1 — Preprocessing leak: show the contaminated statistics

```python
Xc, yc = make_classification(n_samples=200, n_features=5, n_informative=3,
                             random_state=42)
Xc = Xc * np.array([1, 10, 100, 1, 5])      # give the features different scales

X_tr, X_te, y_tr, y_te = train_test_split(Xc, yc, test_size=0.3, random_state=42)

leaky_scaler = StandardScaler().fit(Xc)       # fitted on EVERYTHING  ❌
clean_scaler = StandardScaler().fit(X_tr)     # fitted on train only  ✅

print("Scaler mean, fitted on ALL rows  :", leaky_scaler.mean_.round(2))
print("Scaler mean, fitted on TRAIN only:", clean_scaler.mean_.round(2))
print("Difference                       :", (leaky_scaler.mean_ - clean_scaler.mean_).round(2))
```

The two mean vectors are **different numbers**. That difference is exactly the amount of test-set information that leaked into your training data. Don't argue about how much it hurt the score — the point is that it should be zero, and it isn't.

**The permanent fix — a `Pipeline`:**

```python
# The Pipeline re-fits the scaler inside every fold, on training rows only.
# It is structurally impossible to leak. Use it always.
clean = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
scores = cross_val_score(clean, Xc, yc, cv=KFold(5, shuffle=True, random_state=42))
print(f"Leak-proof CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

### Demo 2 — Duplicate leak (this one gets gasps)

```python
Xd, yd = make_classification(n_samples=150, n_features=8, n_informative=4,
                             random_state=42)
knn = KNeighborsClassifier(n_neighbors=1)

# Clean
a, b, c, d = train_test_split(Xd, yd, test_size=0.3, random_state=42)
print("Clean 1-NN test accuracy      :", round(knn.fit(a, c).score(b, d), 3))

# Now duplicate every row, then split
X_dup = np.vstack([Xd, Xd])
y_dup = np.hstack([yd, yd])
a, b, c, d = train_test_split(X_dup, y_dup, test_size=0.3, random_state=42)
print("With duplicated rows          :", round(knn.fit(a, c).score(b, d), 3))
```

The clean accuracy sits in the mid-0.8s. With duplicates it becomes **exactly 1.000** — perfect. The 1-nearest-neighbour model finds each test row's identical twin sitting in the training set. *"Congratulations, you have built a lookup table."*

### Demo 3 — Target leakage

```python
rng = np.random.RandomState(0)
n = 200
hours = rng.uniform(1, 10, n)
marks = 5 * hours + rng.normal(0, 8, n) + 30
df = pd.DataFrame({
    "study_hours": hours,
    "attendance":  rng.uniform(50, 100, n),
    "final_marks": marks,
    "passed":      (marks > 60).astype(int),      # the target
})

cv = KFold(5, shuffle=True, random_state=42)
pipe = lambda: make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

honest = cross_val_score(pipe(), df[["study_hours", "attendance"]], df["passed"], cv=cv)
leaky  = cross_val_score(pipe(), df[["study_hours", "attendance", "final_marks"]],
                         df["passed"], cv=cv)

print(f"Honest features        : {honest.mean():.3f}")
print(f"With 'final_marks'     : {leaky.mean():.3f}   <-- looks amazing!")
```

Honest lands around 0.82. Add `final_marks` and it jumps to roughly 0.96.

**Live walk-through:** *"That is a 14-point accuracy gain. In an interview you'd be thrilled. Now tell me: on the morning of the exam, before it is written — do you have the student's final marks?"* No. The feature is useless in the real world. The 0.96 is a mirage. Note that cross-validation did **not** save us here — leakage is the one pitfall CV cannot detect for you. Only *you* can, by thinking about each column.

---

## Summary & Wrap-Up (5 min)

**The spine of today:**

1. **Generalisation is the only goal.** Training score measures memorisation; test score measures learning.
2. **Two failure modes.** Underfit (both scores low) and overfit (train high, test far lower). The **gap** is the diagnosis.
3. **Bias–variance is a tradeoff**, not a problem to be solved. Total error is a U-shape; find the bottom.
4. **The learning curve** tells you which failure mode you have — and whether more data would even help.
5. **Three-way split.** Train fits. Validation chooses. Test is opened exactly once.
6. **k-fold cross-validation** beats one split: `cross_val_score` with `KFold(shuffle=True, random_state=42)`. Always report `mean ± std`.
7. **Data leakage** is the biggest real-world killer. Scale after splitting (or use a `Pipeline`), interrogate every feature for target leakage, and `drop_duplicates()` before you split.

**Bridge:** *"Today you learned to **detect** overfitting. Next session — **Regression Models & Regularization** — you learn to **fight** it: Ridge and Lasso, models that build the resistance to overfitting directly into the maths, so you don't have to keep guessing the right complexity by hand."*

---

## Q&A & Doubt Solving (5 min)

**Q: My test score came out higher than my training score. Did I do something wrong?**
→ Not necessarily. A small gap in that direction happens by luck with a tiny test set — you may simply have drawn 10 easy rows. A *large* gap almost always means a bug: a shuffled target, a leak, or an unrepresentative test set. Re-run with a different `random_state`; if it persists, hunt for the bug.

**Q: What value of k should I use for cross-validation?**
→ 5 or 10; 5 is the sane default. Larger k trains each model on more data but costs more fits and shrinks the folds. For very small datasets you can set k = number of rows (leave-one-out), but it is slow and noisy.

**Q: If cross-validation is better, why bother with a separate test set at all?**
→ Because you used cross-validation to *choose* something — the degree, the model, the settings. That choice was informed by every row in the CV data. A final untouched test set is the only thing left that can tell you whether your *entire process*, choices included, generalises.

**Q: How do I know a feature is leaking if it's not obvious like `final_marks`?**
→ Ask the timestamp question: *"When does this value become known — before or after the thing I'm predicting?"* If after, it leaks. Also treat any single feature with suspiciously huge predictive power as guilty until proven innocent. Real signal is rarely that clean.

**Q: Doesn't more data always fix overfitting?**
→ It genuinely helps overfitting — that is what the rising validation curve on the degree-15 panel showed. But it does **nothing** for underfitting, and nothing for leakage. Ten million leaky rows give you a beautiful, worthless model.

---

## Instructor Notes

- **No installs, no downloads.** Everything runs on `numpy`, `pandas`, `matplotlib`, `scikit-learn` — all present from Module 1. All data is generated inline, so nothing depends on a network connection or a CSV.
- **Run the notebook once before class.** Scores match the values quoted here on scikit-learn 1.x with `random_state=42`, but confirm on your machine — and quote them to the room as "around 0.85", not to three decimals.
- **The `learning_curve` trap:** without `shuffle=True`, the small training subsets come from the top of the array. On sorted data this yields bizarre negative R² values that will derail your session. It is already in the code — don't remove it.
- **Pacing:** Practical 1 is the heart of the session. If you are behind, trim Practical 3 Part A (the manual three-way split) and go straight to `cross_val_score` — but never cut the leakage block. Leakage is what they will actually meet at work.
- **The single most common student mistake:** treating a high training score as good news, and — the moment they learn about the test set — silently using it to pick their model, then reporting that score. Pre-empt it: have them write `# TEST SET — DO NOT OPEN` above the test split, and delete the comment only in the final cell.
- **Second most common mistake:** `fit_transform` on the whole `X` before splitting. It is muscle memory from Module 1 cleaning, where it was harmless. Teach `Pipeline` as the reflex that makes it impossible.
