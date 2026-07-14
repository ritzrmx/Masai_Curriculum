# Lecture Script: Avoiding ML Pitfalls & Model Generalization
> **Instructor Reference** — Module 2: Classical ML | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can recognize the four failure modes that make a model look good in the notebook and fail in production — class imbalance, data leakage, unreliable single-split evaluation, and overfitting/underfitting — and apply the standard scikit-learn fix for each.

**Student profile at this point:** Completed Session 1 — comfortable with the end-to-end workflow (features/labels, `train_test_split`, encoding, scaling, and fitting a first `LinearRegression`/simple classifier). Has never been shown a model that lies to them yet.

**Key outcome:** By the end of class, every student has caught at least one "suspiciously perfect" model live, diagnosed why, and fixed it — plus a checklist they will run on every model from here on out.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Class Imbalance — The Accuracy Trap | 10 min | 0:15 |
| **Practical 1:** The Naive Accuracy Trap | 15 min | 0:30 |
| **Concept 2:** Data Leakage — Models That Cheat | 10 min | 0:40 |
| **Practical 2:** Catch & Fix a Leaky Model | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Simple Cross-Validation | 10 min | 1:15 |
| **Practical 3:** `cross_val_score` in Action | 15 min | 1:30 |
| **Concept 4:** Overfitting vs Underfitting | 10 min | 1:40 |
| **Practical 4:** Tree Depth & the Train/Test Gap | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Write this on the board (or show it inline):

```
Model A: 94.6% accuracy on fraud detection
Model B: 99% accuracy on loan default prediction
Model C: 100% accuracy on breast cancer diagnosis (train set)
```

Ask the class: *"Which of these three models would you deploy right now, no questions asked?"* Let a few hands go up for each. Then say: *"By the end of today, you will know that all three numbers are traps — and you'll know exactly how to check."*

**Context to set:** Session 1 gave you a working model. It did not give you a *trustworthy* model. A model that scores 99% in your notebook and fails in production isn't a bug in the code — it's usually one of four specific, well-known traps. Today is entirely about spotting and avoiding them before they cost you (or your company) real money.

**Learning contract for today:**
- Detect class imbalance and stop trusting accuracy blindly
- Recognize and eliminate data leakage before it inflates a score
- Use cross-validation instead of a single lucky/unlucky split
- Diagnose overfitting vs underfitting from a train/test accuracy gap

---

## Concept Block 1: Class Imbalance — The Accuracy Trap (10 min)

### Why Accuracy Lies

Accuracy is `correct predictions / total predictions`. That definition quietly assumes classes are roughly balanced. The moment one class dominates, a model can be *lazy* and still score high.

```
Fraud dataset: 95% legit transactions, 5% fraud
A model that predicts "legit" for EVERY transaction:
  → Accuracy = 95%
  → Fraud caught = 0%
  → Business value = zero (or negative)
```

**Key teaching point:** A high accuracy score on an imbalanced dataset tells you almost nothing about whether the model learned anything. Always check the class distribution *before* you trust any single metric.

### The Decision Flow

```text
Check class distribution: df[target].value_counts(normalize=True)
        │
        ▼
Minority class < ~20% of the data?
   No  → accuracy is mostly fine
   Yes → do NOT trust accuracy alone; check precision/recall/F1 too
              │
              ▼
        Fix options:
        1. class_weight='balanced' (reweight the loss)
        2. Resampling: oversample minority / undersample majority
           (full SMOTE tooling is a later topic — today: awareness)
        3. Pick metrics that reflect the real cost of mistakes
```

| Symptom | Wrong conclusion | Right response |
|---|---|---|
| 95% accuracy | "Great model!" | Check recall/precision on the minority class first |
| Model predicts only the majority class | "It's just conservative" | It has learned nothing — this is a dummy baseline in disguise |
| Business asks "did we catch the fraud?" | Accuracy can't answer this | Recall answers this |

**Teaching point:** Before judging any classifier, always compare it against a **`DummyClassifier`** that predicts the majority class every time. If your "real" model can't beat the dummy on the metric that matters, you don't have a model — you have an illusion.

---

## Practical Block 1: The Naive Accuracy Trap (15 min)

### Dataset
A synthetic fraud-detection dataset built with `make_classification`, deliberately imbalanced (95% legit / 5% fraud).

```python
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

X, y = make_classification(
    n_samples=2000, n_features=6, n_informative=4, n_redundant=0,
    weights=[0.95, 0.05], flip_y=0.01, random_state=42
)
df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(6)])
df["is_fraud"] = y

print("Class distribution:")
print(df["is_fraud"].value_counts())
print("\nClass distribution (%):")
print(df["is_fraud"].value_counts(normalize=True).round(3) * 100)
```

**Output:**
```
Class distribution:
is_fraud
0    1892
1     108
Name: count, dtype: int64

Class distribution (%):
is_fraud
0    94.6
1     5.4
Name: proportion, dtype: float64
```

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# The naive trap: a model that always predicts "not fraud"
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print("--- Dummy classifier (always predicts majority class) ---")
print("Accuracy:", round(accuracy_score(y_test, dummy.predict(X_test)), 3))
print("Recall on fraud class:", round(recall_score(y_test, dummy.predict(X_test)), 3))

# A real logistic regression, default settings
clf = LogisticRegression(max_iter=1000, random_state=42).fit(X_train, y_train)
preds = clf.predict(X_test)
print("\n--- LogisticRegression (default) ---")
print("Accuracy:", round(accuracy_score(y_test, preds), 3))
print("Recall (fraud):", round(recall_score(y_test, preds), 3))
print("Confusion matrix:\n", confusion_matrix(y_test, preds))

# The fix: tell the model the classes are not equally important
clf_bal = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced").fit(X_train, y_train)
preds_bal = clf_bal.predict(X_test)
print("\n--- LogisticRegression (class_weight='balanced') ---")
print("Accuracy:", round(accuracy_score(y_test, preds_bal), 3))
print("Precision (fraud):", round(precision_score(y_test, preds_bal, zero_division=0), 3))
print("Recall (fraud):", round(recall_score(y_test, preds_bal), 3))
print("F1 (fraud):", round(f1_score(y_test, preds_bal), 3))
print("Confusion matrix:\n", confusion_matrix(y_test, preds_bal))
```

**Output:**
```
--- Dummy classifier (always predicts majority class) ---
Accuracy: 0.946
Recall on fraud class: 0.0

--- LogisticRegression (default) ---
Accuracy: 0.946
Recall (fraud): 0.0
Confusion matrix:
 [[473   0]
 [ 27   0]]

--- LogisticRegression (class_weight='balanced') ---
Accuracy: 0.69
Precision (fraud): 0.11
Recall (fraud): 0.667
F1 (fraud): 0.188
Confusion matrix:
 [[327 146]
 [  9  18]]
```

**Stop here and let it sink in.** The "real" default model and the dummy that does zero work score *identical* accuracy — both catch zero fraud. Then look at the fix: accuracy *dropped* from 94.6% to 69%, and that is a *good* outcome. Recall on fraud jumped from 0% to 66.7%. The model now actually does its job, at the cost of more false alarms (146 legit transactions flagged). This is a business decision, not a modeling bug.

**Ask the class:** *"If a false alarm costs you a customer support ticket, but a missed fraud costs you $5,000 — which model do you deploy?"* There's no universally correct answer; the point is that accuracy alone could never have surfaced this conversation.

---

## Concept Block 2: Data Leakage — Models That Cheat (10 min)

### What Leakage Actually Is

Data leakage happens when information that would not be available at prediction time sneaks into training. The model doesn't "learn" — it **cheats**, and the test score becomes a lie.

| Pattern | What happens | Example |
|---|---|---|
| Target leakage | A feature is generated FROM or AFTER the outcome | `collections_flag` is only set once a loan has already defaulted — it encodes the answer |
| Preprocessing/split leakage | Scalers, imputers, or encoders fit on the FULL dataset before splitting | Test-set statistics quietly leak into training |

**Key teaching point:** The giveaway for leakage is almost always a score that is *too good to be true* — 98%+ accuracy on a genuinely hard real-world problem should make you suspicious, not proud.

### The Leakage Checklist

| Question | Why it matters |
|---|---|
| Could this feature exist at the moment I need to predict? | If not, it's leakage — drop it |
| Was any transformation (scaler, imputer, encoder) fit before the split? | Must fit only on train, then `.transform()` on test |
| Does removing a feature tank performance to something more realistic? | Confirms that feature was doing the leaking |

**Teaching point:** Leakage is the single most common reason a "great" model in a Jupyter notebook falls apart in production — because in production, that leaky feature simply doesn't exist yet.

---

## Practical Block 2: Catch & Fix a Leaky Model (15 min)

### Dataset
A synthetic loan-default dataset with one deliberately leaky column: `collections_flag`, which — in the real world — is only recorded *after* a loan has defaulted.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(42)
n = 800

income = rng.normal(50000, 15000, n).clip(10000)
credit_score = rng.normal(650, 80, n).clip(300, 850)
loan_amount = rng.normal(20000, 8000, n).clip(1000)
employment_years = rng.normal(5, 3, n).clip(0)

risk_score = (
    -0.00004 * income - 0.004 * credit_score + 0.00003 * loan_amount
    - 0.1 * employment_years + rng.normal(0, 1.5, n)
)
default = (risk_score > np.median(risk_score)).astype(int)

# LEAKY FEATURE: only exists AFTER a loan has already defaulted
collections_flag = np.where(
    default == 1,
    rng.choice([1, 0], size=n, p=[0.97, 0.03]),
    rng.choice([1, 0], size=n, p=[0.02, 0.98]),
)

df = pd.DataFrame({
    "income": income, "credit_score": credit_score, "loan_amount": loan_amount,
    "employment_years": employment_years, "collections_flag": collections_flag,
    "default": default,
})
print("Default rate:", round(df["default"].mean(), 3))

# --- BROKEN: train with the leaky feature included ---
leaky_features = ["income", "credit_score", "loan_amount", "employment_years", "collections_flag"]
X_leaky, y = df[leaky_features], df["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X_leaky, y, test_size=0.25, random_state=42, stratify=y
)
clf_leaky = LogisticRegression(max_iter=1000, random_state=42).fit(X_train, y_train)
print("\n--- Model WITH leaky feature ---")
print("Test accuracy:", round(accuracy_score(y_test, clf_leaky.predict(X_test)), 4))
print("Feature coefficients:")
for name, coef in zip(leaky_features, clf_leaky.coef_[0]):
    print(f"  {name}: {coef:.4f}")
```

**Output:**
```
Default rate: 0.5

--- Model WITH leaky feature ---
Test accuracy: 0.99
Feature coefficients:
  income: -0.0000
  credit_score: -0.0050
  loan_amount: 0.0000
  employment_years: -0.0441
  collections_flag: 5.8410
```

**Stop and point at the coefficients.** `collections_flag` has a coefficient of 5.84 — completely dwarfing every real financial feature. That is the signature of leakage: one feature doing all the work because it's basically a copy of the label.

```python
# --- FIX: remove the feature that only exists AFTER the outcome ---
clean_features = ["income", "credit_score", "loan_amount", "employment_years"]
X_clean = df[clean_features]

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_clean, y, test_size=0.25, random_state=42, stratify=y
)
clf_clean = LogisticRegression(max_iter=1000, random_state=42)
clf_clean.fit(X_train2, y_train2)
print("--- Model WITHOUT leaky feature ---")
print("Test accuracy:", round(accuracy_score(y_test2, clf_clean.predict(X_test2)), 4))
```

**Output:**
```
--- Model WITHOUT leaky feature ---
Test accuracy: 0.665
```

**Walk through the drop:** 99% → 66.5%. That is not a worse model — it is the *first honest number* we've seen. 66.5% is a believable score for predicting loan default from income/credit/loan size alone.

```python
# --- Preprocessing leakage: scaling BEFORE split (wrong) vs AFTER split (right) ---
Xtr_w, Xte_w, ytr_w, yte_w = train_test_split(
    StandardScaler().fit_transform(X_clean), y, test_size=0.25, random_state=42, stratify=y
)  # scaler fit on ALL data — wrong
clf_w = LogisticRegression(max_iter=1000, random_state=42).fit(Xtr_w, ytr_w)
print("Accuracy (scaled BEFORE split):", round(accuracy_score(yte_w, clf_w.predict(Xte_w)), 4))

Xtr_r, Xte_r, ytr_r, yte_r = train_test_split(X_clean, y, test_size=0.25, random_state=42, stratify=y)
scaler_right = StandardScaler().fit(Xtr_r)  # fit ONLY on train
clf_r = LogisticRegression(max_iter=1000, random_state=42).fit(scaler_right.transform(Xtr_r), ytr_r)
print("Accuracy (scaled AFTER split, fit on train only):", round(accuracy_score(yte_r, clf_r.predict(scaler_right.transform(Xte_r))), 4))
```

**Output:**
```
Accuracy (scaled BEFORE split): 0.665
Accuracy (scaled AFTER split, fit on train only): 0.665
```

**Nuance to call out:** here both approaches land on the same score — preprocessing leakage doesn't always blow up your number the way target leakage does, which is exactly why it's dangerous. The rule doesn't change: **always fit `StandardScaler`/`SimpleImputer`/encoders on train only.** Target leakage is usually loud; preprocessing leakage is quiet and still costs you in production.

**Ask the class:** *"Name a feature in a real product that would leak the label if included at training time."* Good answers: "approved_amount" for a loan model, "interview_score" for a resume-screening model.

---

## BREAK (10 min)

*Suggested break prompt — ask students to think of one leaky feature or imbalanced target from their own domain of interest (finance, healthcare, e-commerce). They'll share one example after the break.*

---

## Concept Block 3: Simple Cross-Validation (10 min)

### The Problem With One Split

`train_test_split` gives you **one** number. That number depends partly on which rows randomly landed in the test set. A different `random_state` can shift your reported accuracy by several points — with zero change to the model.

```text
random_state=0  →  test accuracy: 0.9580
random_state=1  →  test accuracy: 0.9650
random_state=2  →  test accuracy: 0.9720
random_state=3  →  test accuracy: 0.9860
random_state=4  →  test accuracy: 0.9720
```

**Key teaching point:** If your reported score moves this much just by reshuffling the split, a single train/test split is not a reliable way to report or compare models.

### K-Fold Cross-Validation, Simply

```text
Data split into 5 equal folds:  [1] [2] [3] [4] [5]
Round 1: train [2][3][4][5] → test [1] → score₁   (repeat, rotating the test fold, through Round 5)
Final reported score = mean(score₁ ... score₅) ± std
```

Every row gets used for testing exactly once, and for training four times. The result is one mean score plus a standard deviation — a much more honest picture than a single lucky/unlucky split.

| Approach | What you get | When to use |
|---|---|---|
| Single `train_test_split` | One score, high variance | Quick iteration, huge datasets |
| `cross_val_score(cv=5)` | Mean + std across 5 folds | Comparing models, reporting a real number |
| `cross_val_score(cv=10)` | More stable, more compute | Small datasets, final validation |

**Teaching point:** `cross_val_score` is not a replacement for the final held-out test set — it's what you use *while developing and comparing models*. Keep a separate, untouched test set for the very end.

---

## Practical Block 3: `cross_val_score` in Action (15 min)

### Dataset
`load_breast_cancer` — a real, moderately sized binary classification dataset (569 rows), ideal for showing split-to-split variance.

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

data = load_breast_cancer()
X, y = data.data, data.target
print("Dataset shape:", X.shape)
print("Class balance:", np.bincount(y))

# Single train/test split — repeated with different random_state values
for seed in [0, 1, 2, 3, 4]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed, stratify=y
    )
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=5000, random_state=42)),
    ])
    pipe.fit(X_train, y_train)
    print(f"random_state={seed} -> test accuracy: {pipe.score(X_test, y_test):.4f}")
```

**Output:**
```
Dataset shape: (569, 30)
Class balance: [212 357]
random_state=0 -> test accuracy: 0.9580
random_state=1 -> test accuracy: 0.9650
random_state=2 -> test accuracy: 0.9720
random_state=3 -> test accuracy: 0.9860
random_state=4 -> test accuracy: 0.9720
```

```python
# 5-fold cross-validation on the exact same pipeline
print("--- 5-fold cross-validation ---")
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=5000, random_state=42)),
])
scores = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
print("Fold scores:", np.round(scores, 4))
print("Mean accuracy:", round(scores.mean(), 4))
print("Std deviation:", round(scores.std(), 4))
```

**Output:**
```
--- 5-fold cross-validation ---
Fold scores: [0.9825 0.9825 0.9737 0.9737 0.9912]
Mean accuracy: 0.9807
Std deviation: 0.0065
```

**Walk through the contrast explicitly.** Five separate splits swung from 0.958 to 0.986 — a range of nearly 3 points, on the *same* model. Cross-validation instead reports 0.9807 ± 0.0065: one honest number with an uncertainty estimate attached.

**Important implementation detail to highlight:** notice we passed the whole `Pipeline` (scaler + classifier) into `cross_val_score`, not a pre-scaled `X`. This is exactly how you avoid the preprocessing leakage from the last block — `cross_val_score` refits the scaler on each fold's training portion automatically.

**Ask the class:** *"Why did we use `cv=5` and not `cv=569` (one fold per row)?"* → That's leave-one-out CV — technically valid, but 569x the compute for a marginal reliability gain. `cv=5` or `cv=10` is the practical default.

---

## Concept Block 4: Overfitting vs Underfitting (10 min)

### The Core Diagnostic

Once you trust your score (no leakage, checked with CV), the next question is: **is the model too simple, too complex, or about right?** You diagnose this by comparing train accuracy to test accuracy.

| Signal | Underfitting (High Bias) | Good fit | Overfitting (High Variance) |
|---|---|---|---|
| Train accuracy | Low | High | Very high (often ~100%) |
| Test accuracy | Low | High | Noticeably lower than train |
| Train − Test gap | Small | Small | Large |
| Typical cause | Model too simple / too few features | Right complexity for the data | Model too complex / too little data / no regularization |
| Fix | Add features, increase model complexity | — | Constrain the model (max_depth, k, regularization), get more data, use CV |

**Key teaching point:** Overfitting is not "the model is bad" — it's "the model is too good at the *wrong* thing." It learned the training set's noise instead of the underlying pattern, and noise doesn't repeat in new data.

### The Complexity Knob

```text
Model complexity:  Low (underfit) ───────────────► High (overfit)
DecisionTree:  max_depth=1  →  max_depth=None
KNN:           large k      →  k=1
Linear model:  strong reg.  →  no regularization
```

Every model family has some "complexity knob." Today we use `max_depth` for trees and `n_neighbors` for KNN. Next session (Regularization) we'll see the linear-model equivalent.

---

## Practical Block 4: Tree Depth & the Train/Test Gap (10 min)

### Dataset
Continuing with `load_breast_cancer` from the CV block — same data, new question.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"{'max_depth':>10} | {'train_acc':>10} | {'test_acc':>10} | {'gap':>6}")
print("-" * 46)
for depth in [1, 2, 3, 4, 5, None]:
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    clf.fit(X_train, y_train)
    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)
    gap = train_acc - test_acc
    print(f"{str(depth if depth is not None else 'None'):>10} | {train_acc:>10.3f} | {test_acc:>10.3f} | {gap:>6.3f}")
```

**Output:**
```
 max_depth |  train_acc |   test_acc |    gap
----------------------------------------------
         1 |      0.923 |      0.923 | -0.001
         2 |      0.958 |      0.909 |  0.049
         3 |      0.977 |      0.944 |  0.032
         4 |      0.988 |      0.944 |  0.044
         5 |      0.995 |      0.937 |  0.058
      None |      1.000 |      0.923 |  0.077
```

**Walk through this row by row.** `max_depth=1` is underfitting: both train and test accuracy are low (0.923) and nearly identical — the tree is too shallow to separate the classes well, even on data it has already seen. `max_depth=None` is overfitting: train accuracy hits a perfect 1.000, but test accuracy actually *drops* to 0.923, and the gap balloons to 0.077. The sweet spot here is around `max_depth=3` — best test accuracy (0.944) with a small, healthy gap.

**Note the same pattern holds for KNN** (`n_neighbors` is its complexity knob, running the opposite direction: `n_neighbors=1` overfits, a large `n_neighbors` underfits) — if time allows, have students swap `DecisionTreeClassifier(max_depth=...)` for `KNeighborsClassifier(n_neighbors=...)` on a scaled version of `X_train`/`X_test` and reproduce the same gap table themselves.

**Discussion prompt:** *"We just showed the train/test gap using ONE split. What did we learn 20 minutes ago about trusting a single split?"* → Push students to say it: in a real project, you'd wrap this whole depth sweep in cross-validation, not a single `train_test_split`. Today we kept it to one split only to make the gap easy to see on the board.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Class imbalance turns accuracy into a misleading metric — always check `value_counts()` first, compare against a `DummyClassifier`, and consider `class_weight='balanced'`
- Data leakage produces suspiciously perfect scores — target leakage (a feature derived from the label) is loud and obvious; preprocessing leakage (fitting scalers before the split) is quiet and easy to miss
- A single `train_test_split` score has real variance — `cross_val_score(cv=5)` gives a mean ± std you can actually trust
- Overfitting (huge train/test gap) and underfitting (both scores low) are diagnosed by comparing train vs test accuracy as you tune a model's complexity knob

**Bridge to next session:** *"Today you learned to diagnose a model that's too simple or too complex using tree depth and k. Next class — Regression Models & Regularization — you'll see the linear-model version of that same complexity knob: L1 and L2 regularization, and how Ridge/Lasso fight overfitting mathematically instead of by limiting depth."*

**Homework / self-practice:** Take the `load_wine` or `load_breast_cancer` dataset, pick any classifier, and (1) check the class balance, (2) run `cross_val_score(cv=5)`, and (3) sweep one complexity parameter to find where train/test accuracy starts to diverge. Bring your gap table to the next session.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: If `class_weight='balanced'` drops my accuracy, doesn't that mean the model got worse?**
→ No — it means accuracy was the wrong metric to optimize for an imbalanced problem in the first place. Look at recall/precision/F1 on the minority class before and after; that's where the real improvement shows up.

**Q: How do I know if a feature is "leaky" if I didn't build the dataset myself?**
→ Ask: "At the moment I need to make this prediction in the real world, would I actually have this value yet?" If the answer is no (it's recorded after the outcome, or it's an ID that correlates with the outcome by coincidence), it's leakage.

**Q: Does `cross_val_score` replace my test set entirely?**
→ No. Use CV during development to compare models and tune settings. Keep one final, untouched test set (or a fully held-out split) for your last, honest check before calling the project done.

**Q: My train accuracy and test accuracy are both around 70% — is that overfitting?**
→ No, that's underfitting (or just a genuinely hard problem) — both scores are low with a small gap. Overfitting specifically means a *big gap*, with train much higher than test.

**Q: Can a model be both leaking data AND overfitting at the same time? Is `max_depth=None` always a bad idea?**
→ Yes to the first — always fix leakage before diagnosing over/underfitting, since an inflated leaky score hides the real gap underneath it. And no to the second — for some datasets with lots of data and clear structure, an unconstrained tree does fine. The point isn't "always constrain," it's "always check the train/test gap before you trust the number."

---

## Instructor Notes

- **Datasets used:** `make_classification` (imbalance demo, synthetic and self-contained), a hand-built `numpy`-generated loan dataset (leakage demo), `load_breast_cancer` (CV + overfitting demos — reused deliberately so students see the same data support two different lessons). No internet access is required anywhere in this session.
- **Common student mistake:** Fitting `StandardScaler` (or any encoder/imputer) on the full dataset before `train_test_split`. Catch this early — ask "did you fit before or after the split?" every time a student's numbers look too good.
- **Live-coding tip:** In Practical 2, pause right after printing the leaky model's coefficients and let students guess which feature is the problem before you tell them. The 5.84 coefficient sitting next to near-zero coefficients is a strong visual cue.
- **For advanced students:** Have them wrap the Practical 4 depth/k sweep inside `cross_val_score` instead of a single split, and compare whether the "best" depth changes.
- **Time-check contingency:** If running behind after the break, compress Practical 3 by only running the `cv=5` cell (skip the five-single-splits loop) and describe the variance verbally instead of live-coding it — the mean ± std number still lands the point.
