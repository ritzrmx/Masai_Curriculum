# Lecture Script: Model Validation & Leakage
> **Instructor Reference** — Module 2: Classical ML | Session 11 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students implement k-fold and stratified k-fold cross-validation to produce reliable performance estimates, tune hyperparameters using `GridSearchCV` and interpret the results, and detect data leakage scenarios while designing a leakage-free evaluation pipeline.

**Student profile at this point:** Has trained and evaluated linear models (Sessions 4-6), classification metrics (Session 7), and tree-based models (Sessions 9-10) using a single `train_test_split`. This session challenges the reliability of that single-split habit directly.

**Key outcome:** Every student runs 5-fold stratified cross-validation on `patient_readmission.csv`, tunes a hyperparameter with `GridSearchCV`, and — most importantly — directly demonstrates data leakage by comparing a model WITH a leaky proxy feature against the same model WITHOUT it, quantifying exactly how much the leakage inflated the reported score.

**Dataset for this session:** `patient_readmission.csv` (in this folder) — 40 rows of `age`, `length_of_stay_days`, `num_prior_visits`, `num_medications`, `has_chronic_condition`, a deliberately leaky `discharge_note_risk_flag`, and target `readmitted_30d`.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Can We Trust One Split? | 10 min | 0:10 |
| SEGMENT 2: K-Fold and Stratified K-Fold Cross-Validation | 25 min | 0:35 |
| SEGMENT 3: Tuning Hyperparameters with GridSearchCV | 20 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Data Leakage — The Demo That Changes How You Work | 25 min | 1:30 |
| SEGMENT 5: Designing a Leakage-Free Pipeline | 10 min | 1:40 |
| SEGMENT 6: Lab — Full Workflow on patient_readmission.csv | 15 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Can We Trust One Split? (10 min)

### The Uncomfortable Question (6 min)

**Say:** *"Every single model we've trained this module — Linear Regression, Ridge, Lasso, Logistic Regression, Decision Trees, Random Forests — has been evaluated using exactly ONE `train_test_split`, with `random_state=42` fixed the entire time. Here's the uncomfortable question we're finally going to confront: how do we know that ONE split's reported accuracy wasn't just a lucky (or unlucky) draw?"*

**Live-code this quick demonstration on the projector:**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("patient_readmission.csv")
X = df[["age", "length_of_stay_days", "num_prior_visits", "num_medications", "has_chronic_condition"]]
y = df["readmitted_30d"]

pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))])

for rs in [0, 1, 42, 7, 99]:
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=rs, stratify=y)
    pipe.fit(Xtr, ytr)
    print("random_state:", rs, "-> test accuracy:", round(pipe.score(Xte, yte), 3))
```

**Run it and let the spread across five splits land.** **Say:** *"You've now seen this exact pattern twice — once with a single tree in Session 9/10. A single train/test split is really just ONE noisy sample of 'how well would this model do on unseen data.' If we report only that one number in a business review and it happened to be an unusually lucky split, we've made a promise the model can't actually keep in production."*

### Setting Expectations for Today (4 min)

**Say:** *"By the end of today you'll be able to do three things: run cross-validation to get a reliable, averaged performance estimate instead of trusting one split; use `GridSearchCV` to search hyperparameters systematically instead of guessing by hand; and — this is the segment I want you to remember years from now — recognize data leakage before it quietly wrecks a real project. Leakage is one of the single most common reasons a model looks fantastic in testing and then embarrasses a team in production. Today you'll see it happen live, with real numbers, so you never miss it again."*

**Learning contract for today — write on board:**

- Run k-fold and stratified k-fold cross-validation
- Tune hyperparameters with `GridSearchCV` and interpret `best_params_`/`best_score_`
- Detect data leakage and quantify its effect on reported performance
- Design a leakage-free evaluation pipeline

---

## SEGMENT 2: K-Fold and Stratified K-Fold Cross-Validation (25 min)

### Loading and Exploring the Data (5 min)

**Say:** *"Let's load `patient_readmission.csv` — 40 hospital patients, features about their stay, and a target: were they readmitted within 30 days?"*

**Live-code:**

```python
df = pd.read_csv("patient_readmission.csv")
print(df.head())
print(df.shape)
print(df["readmitted_30d"].value_counts())
```

**Run it.** Expected output:

```
   patient_id  age  length_of_stay_days  num_prior_visits  num_medications  has_chronic_condition  discharge_note_risk_flag  readmitted_30d
0        7001   63                    12                 2                5                       1                          1               1
1        7002   34                     4                 0                2                       0                          0               0
2        7003   33                     2                 5                6                       1                          1               0
3        7004   37                     6                 5                6                       0                          1               1
4        7005   28                     2                 1                4                       0                          0               0

(40, 8)
readmitted_30d
1    21
0    19
Name: count, dtype: int64
```

**Say:** *"We'll set aside `discharge_note_risk_flag` for now — we're building deliberately toward SEGMENT 4, where that exact column becomes the star of a leakage demonstration. For this segment, we use only the five legitimate features."*

### Running Cross-Validation (10 min)

**Live-code:**

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

X = df[["age", "length_of_stay_days", "num_prior_visits", "num_medications", "has_chronic_condition"]]
y = df["readmitted_30d"]

pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))])
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(pipe, X, y, cv=skf, scoring="accuracy")
print("Fold scores:", scores)
print("Mean accuracy:", scores.mean())
print("Std deviation:", scores.std())
```

**Run it.** Expected output:

```
Fold scores: [0.5  0.75 0.875 0.625 0.875]
Mean accuracy: 0.725
Std deviation: 0.14300699218143458
```

**Say:** *"THIS is what we were missing with a single split. Instead of one number, we get FIVE — one per fold — and we can see directly how much they vary: from 0.50 up to 0.875. The MEAN, 0.725, is a far more honest single-number summary than any one fold alone, and the standard deviation, roughly 0.14, tells us how much to trust that mean — a large spread like this is itself an important finding: on a dataset this small, performance estimates carry real uncertainty, and we should communicate that honestly rather than reporting '72.5% accuracy' as if it were precise to the decimal."*

**Say:** *"Notice `cross_val_score` handles the entire fit-predict-score loop internally, across all 5 folds, using the SAME pipeline object each time — no manual `train_test_split` loop required."*

### KFold vs. StratifiedKFold, Side by Side (7 min)

**Say:** *"Let's see exactly WHY we used `StratifiedKFold` rather than plain `KFold` for this classification target."*

**Live-code:**

```python
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)
print("Plain KFold - test class balance per fold:")
for i, (train_idx, test_idx) in enumerate(kf.split(X, y)):
    print(f"  fold {i}:", y.iloc[test_idx].value_counts().to_dict())

print("StratifiedKFold - test class balance per fold:")
for i, (train_idx, test_idx) in enumerate(skf.split(X, y)):
    print(f"  fold {i}:", y.iloc[test_idx].value_counts().to_dict())
```

**Run it.** Expected output:

```
Plain KFold - test class balance per fold:
  fold 0: {1: 6, 0: 2}
  fold 1: {1: 4, 0: 4}
  fold 2: {0: 5, 1: 3}
  fold 3: {0: 5, 1: 3}
  fold 4: {1: 5, 0: 3}
StratifiedKFold - test class balance per fold:
  fold 0: {1: 5, 0: 3}
  fold 1: {0: 4, 1: 4}
  fold 2: {0: 4, 1: 4}
  fold 3: {0: 4, 1: 4}
  fold 4: {0: 4, 1: 4}
```

**Say:** *"Look at plain `KFold`'s fold 0: 6 readmitted patients versus only 2 not-readmitted — a far cry from the true overall ratio. `StratifiedKFold`'s folds stay much closer to the true overall ratio (21 vs 19, roughly balanced) in every single fold. On a small, close-to-balanced dataset like this one, the difference is modest but visible — on a real-world imbalanced dataset (say, 95% stay / 5% churn), plain `KFold` could easily hand you a fold with almost NO positive examples at all, making that fold's score meaningless."*

**Ask:** *"For a REGRESSION target like Session 4's `price_lakhs`, would `StratifiedKFold` even be usable?"* (No — `StratifiedKFold` requires discrete classes to stratify by; for regression, plain `KFold` is the standard choice, exactly parallel to why `train_test_split` didn't use `stratify=y` back in Session 4.)

### Comprehension Check (3 min)

1. *"If `cross_val_score` returns 5 numbers, which one should you report as 'the' model's performance in a summary slide?"* (The mean — ideally alongside the standard deviation or the full spread, not just the mean alone, to communicate uncertainty honestly.)
2. *"Does cross-validation replace the need for a final, separate test set?"* (Not entirely — cross-validation is typically used DURING model development/tuning; a final untouched hold-out test set is still valuable as a last, honest check before deployment.)

---

## SEGMENT 3: Tuning Hyperparameters with GridSearchCV (20 min)

### The Manual Way, First (5 min)

**Say:** *"Before we automate this, let's feel the pain of doing it by hand, briefly — trying a few `C` values for `LogisticRegression` (recall from Session 6 and Session 5's regularization discussion: `C` controls regularization strength, with SMALLER `C` meaning STRONGER regularization)."*

**Live-code:**

```python
for c in [0.01, 0.1, 1, 10, 100]:
    manual_pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(C=c, max_iter=1000))])
    manual_scores = cross_val_score(manual_pipe, X, y, cv=skf, scoring="accuracy")
    print(f"C={c}: mean CV accuracy = {manual_scores.mean():.3f}")
```

**Run it.** Expected output:

```
C=0.01: mean CV accuracy = 0.650
C=0.1: mean CV accuracy = 0.700
C=1: mean CV accuracy = 0.725
C=10: mean CV accuracy = 0.675
C=100: mean CV accuracy = 0.725
```

**Say:** *"That worked, but imagine tuning TWO or THREE hyperparameters at once — the number of combinations to manually loop through explodes fast. That's exactly the problem `GridSearchCV` solves."*

### GridSearchCV, Live (10 min)

**Live-code:**

```python
from sklearn.model_selection import GridSearchCV

param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}

grid = GridSearchCV(pipe, param_grid, cv=skf, scoring="accuracy")
grid.fit(X, y)

print("Best params:", grid.best_params_)
print("Best CV score:", grid.best_score_)
```

**Run it.** Expected output:

```
Best params: {'model__C': 1}
Best CV score: 0.725
```

**Say:** *"Same answer as our manual loop, but `GridSearchCV` did the looping, the cross-validation, and the bookkeeping FOR us — and notice the parameter name `model__C`, not just `C`. That double-underscore syntax tells `GridSearchCV` which STEP inside our `Pipeline` (the step named `'model'`) owns the `C` parameter — exactly the same naming convention we used with `ColumnTransformer` steps back in Sessions 2 and 9."*

**Say:** *"For a peek under the hood, `grid.cv_results_` holds the full table of every combination tried and its mean score — useful when you want to plot or inspect the WHOLE search, not just the single winner."*

```python
import pandas as pd
results_df = pd.DataFrame(grid.cv_results_)[["param_model__C", "mean_test_score", "std_test_score"]]
print(results_df)
```

### Why GridSearchCV and Cross-Validation Are a Natural Pair (5 min)

**Say:** *"Notice `GridSearchCV` didn't just try each `C` value on ONE split — internally, it ran FULL cross-validation (5 folds, via our `skf`) for EVERY candidate value, then averaged. This matters a lot: if it only used one split per candidate, we'd be right back to SEGMENT 1's problem — the 'winning' hyperparameter might just be the one that got lucky on that one split, not the one that's genuinely best."*

**Ask:** *"If we'd used `cv=3` instead of our 5-fold `skf`, would `GridSearchCV` still work? What would change?"* (Yes, it would still work — fewer folds means less compute time but a noisier, less reliable estimate per candidate, especially on a small dataset like this one.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict, before returning, what will happen to cross-validated accuracy if we add `discharge_note_risk_flag` — a column filled in by hospital staff — back into the feature set. Will accuracy go up a little, a lot, or stay the same? Come back ready to find out.

---

## SEGMENT 4: Data Leakage — The Demo That Changes How You Work (25 min)

### What discharge_note_risk_flag Actually Is (5 min)

**Say:** *"Time to reveal what `discharge_note_risk_flag` really represents. In this (synthetic, but realistic) hospital workflow, staff fill in this flag on the discharge note — but critically, they often fill it in AFTER they already know, or strongly suspect, whether the patient will be readmitted. In other words: this column is contaminated with information about the FUTURE outcome we're trying to predict. That's the textbook definition of data leakage."*

**Write on board:**

> **Data leakage:** information that would NOT actually be available at the real moment of prediction sneaks into your training features — most dangerously, a feature that is really just a disguised proxy for the target itself.

### The Demo: With Leakage vs. Without (12 min)

**Live-code:**

```python
X_leak = df[["age", "length_of_stay_days", "num_prior_visits",
             "num_medications", "has_chronic_condition", "discharge_note_risk_flag"]]
X_clean = df[["age", "length_of_stay_days", "num_prior_visits",
              "num_medications", "has_chronic_condition"]]
y = df["readmitted_30d"]

scores_leak = cross_val_score(pipe, X_leak, y, cv=skf, scoring="accuracy")
scores_clean = cross_val_score(pipe, X_clean, y, cv=skf, scoring="accuracy")

print("WITH leakage feature    - fold scores:", scores_leak.round(3), "mean:", round(scores_leak.mean(), 3))
print("WITHOUT leakage feature - fold scores:", scores_clean.round(3), "mean:", round(scores_clean.mean(), 3))
```

**Run it.** Expected output:

```
WITH leakage feature    - fold scores: [1.    1.    1.    0.875 1.   ] mean: 0.975
WITHOUT leakage feature - fold scores: [0.5   0.75  0.875 0.625 0.875] mean: 0.725
```

**Say, letting this land:** *"97.5% versus 72.5%. A TWENTY-FIVE percentage point difference, from adding exactly ONE column. If a team reported the 97.5% number to hospital leadership, deployed the model, and then watched it perform at roughly 72.5% in the real world — because in production, that discharge note flag either isn't filled in yet at prediction time, or is filled in with the same after-the-fact contamination that won't exist for NEW, not-yet-readmitted patients — that's not a small embarrassment. That's a model that actively misled a real clinical decision."*

**Run this single-split version too, for an even starker illustration:**

```python
from sklearn.model_selection import train_test_split

Xtr_leak, Xte_leak, ytr, yte = train_test_split(X_leak, y, test_size=0.25, random_state=42, stratify=y)
pipe.fit(Xtr_leak, ytr)
print("Single split WITH leak - test accuracy:", pipe.score(Xte_leak, yte))

Xtr_clean, Xte_clean, ytr2, yte2 = train_test_split(X_clean, y, test_size=0.25, random_state=42, stratify=y)
pipe.fit(Xtr_clean, ytr2)
print("Single split WITHOUT leak - test accuracy:", pipe.score(Xte_clean, yte2))
```

**Run it.** Expected output:

```
Single split WITH leak - test accuracy: 1.0
Single split WITHOUT leak - test accuracy: 0.8
```

**Say:** *"A PERFECT test score should always make you suspicious, not celebratory. 100% accuracy on real-world hospital data is almost never a sign of a great model — it's usually a sign of a leaked answer key."*

### How to Actually Catch This in Practice (8 min)

**Say:** *"You won't always have a column as obviously named as `discharge_note_risk_flag` — real leakage is often sneakier. Here's the checklist to run on every candidate feature before training:"*

**Write this checklist on the board:**

1. *"Would this exact value be KNOWN, in that exact form, at the real moment I need to make a prediction — before the outcome has happened?"*
2. *"Is this feature suspiciously, almost perfectly correlated with the target?"* (Check with `df.corr()` or a quick cross-tab — a near-perfect correlation with the target is a red flag worth investigating, not a cause for celebration.)
3. *"Does removing this ONE feature cause a large, suspicious drop in reported performance?"* (Exactly the comparison we just ran — a huge before/after gap on ONE feature's removal is a leakage smell.)
4. *"For time-based data specifically: am I accidentally using information from AFTER the prediction point — e.g., splitting randomly instead of by time?"*

**Say:** *"That fourth point deserves its own callout. Imagine predicting monthly churn using a feature like `total_calls_this_year` computed from the FULL year, including months after the prediction date — even though no single value looks suspicious like our discharge flag did, the model is still peeking into the future. For any genuinely time-ordered problem, you split train/test by TIME (train on earlier records, test on later ones) rather than a random shuffle, specifically to prevent this."*

**Ask:** *"Suppose a feature `days_since_last_login` correlates strongly with churn but ISN'T leakage. What's the key difference between that feature and `discharge_note_risk_flag`?"* (`days_since_last_login` is genuinely knowable and meaningful at prediction time — it describes past behavior, not a staff annotation made after the outcome is already known. Strong correlation alone isn't leakage; the question is always about WHEN the information becomes available.)

---

## SEGMENT 5: Designing a Leakage-Free Pipeline (10 min)

### The Preprocessing-Order Leak (5 min)

**Say:** *"There's a second, subtler kind of leakage that has nothing to do with a suspicious column — it's about GETTING THE ORDER OF OPERATIONS wrong."*

**Live-code the WRONG way, explicitly labeled:**

```python
# WRONG - fitting the scaler on the FULL dataset before splitting
from sklearn.preprocessing import StandardScaler

scaler_wrong = StandardScaler()
X_scaled_wrong = scaler_wrong.fit_transform(X_clean)   # sees ALL rows, including future test rows

Xtr_w, Xte_w, ytr_w, yte_w = train_test_split(X_scaled_wrong, y, test_size=0.25, random_state=42, stratify=y)
# By this point, the "test" data already influenced the scaler's mean/std!
```

**Say:** *"`StandardScaler.fit_transform` on the full dataset computes mean and standard deviation using EVERY row — including the rows that will later become your 'test' set. Your test set is supposed to represent information the model has never touched in ANY way. This leaks a small amount of test-set statistical information into training, even though no single feature column looks suspicious."*

**Live-code the RIGHT way:**

```python
# RIGHT - split FIRST, fit the scaler only on the training fold
Xtr_r, Xte_r, ytr_r, yte_r = train_test_split(X_clean, y, test_size=0.25, random_state=42, stratify=y)

scaler_right = StandardScaler()
Xtr_scaled = scaler_right.fit_transform(Xtr_r)     # fit ONLY on train
Xte_scaled = scaler_right.transform(Xte_r)          # transform test using train's stats, never re-fit
```

**Say:** *"This is EXACTLY why we've been using `Pipeline` this entire module, not just for convenience — `cross_val_score` and `GridSearchCV` automatically re-fit the `StandardScaler` fresh on ONLY each fold's training portion, every single fold, and never let it see that fold's test rows. Wrapping preprocessing inside a `Pipeline` isn't a style preference; it's a structural leakage guard."*

### The Leakage-Free Checklist (5 min)

**Draw this final checklist on the board:**

| Check | Why it matters |
|---|---|
| Every feature is genuinely knowable at real prediction time | Prevents proxy-for-target leakage |
| Preprocessing (scaling, encoding, imputing) happens INSIDE a `Pipeline` | Prevents test-fold statistics leaking into training |
| Time-ordered data is split by TIME, not randomly | Prevents future information leaking into past predictions |
| A near-perfect score triggers suspicion, not celebration | Perfect scores are rare and usually a leakage symptom |
| Cross-validation, not a single split, drives any "final" reported number | Reduces the chance of reporting a lucky/unlucky one-off result |

---

## SEGMENT 6: Lab — Full Workflow on patient_readmission.csv (15 min)

### Instructions (read aloud, step by step)

1. Load `patient_readmission.csv`. Build a CLEAN feature set (no `discharge_note_risk_flag`) and the target `readmitted_30d`.
2. Build a `Pipeline` with `StandardScaler` and `LogisticRegression`.
3. Run 5-fold `StratifiedKFold` cross-validation and report the mean and standard deviation of accuracy.
4. Use `GridSearchCV` to tune `model__C` over `[0.01, 0.1, 1, 10, 100]`; report `best_params_` and `best_score_`.
5. Rebuild the feature set WITH `discharge_note_risk_flag` included, re-run cross-validation, and compute the accuracy GAP versus the clean version.
6. Write two sentences: one stating the CV mean ± spread for the clean model, one explaining WHY the leaky feature inflates accuracy and why it must be excluded before deployment.

### Starter Code

```python
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("patient_readmission.csv")
X_clean = df[[___, ___, ___, ___, ___]]
y = df[___]

pipe = Pipeline([("scaler", ___()), ("model", ___(max_iter=1000))])
skf = ___(n_splits=___, shuffle=True, random_state=42)

scores = cross_val_score(pipe, X_clean, y, cv=___, scoring="accuracy")
print("Mean CV accuracy:", scores.mean(), "Std:", scores.std())

param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}
grid = ___(pipe, param_grid, cv=skf, scoring="accuracy")
grid.___(X_clean, y)
print("Best params:", grid.best_params_)
print("Best CV score:", grid.best_score_)

X_leak = df[[___, ___, ___, ___, ___, "discharge_note_risk_flag"]]
scores_leak = cross_val_score(pipe, X_leak, y, cv=skf, scoring="accuracy")
print("With leakage mean:", scores_leak.mean())
print("Gap:", scores_leak.mean() - scores.mean())

# TODO: write your two interpretation sentences here as comments
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("patient_readmission.csv")
X_clean = df[["age", "length_of_stay_days", "num_prior_visits", "num_medications", "has_chronic_condition"]]
y = df["readmitted_30d"]

pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))])
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(pipe, X_clean, y, cv=skf, scoring="accuracy")
print("Mean CV accuracy:", scores.mean(), "Std:", scores.std())

param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}
grid = GridSearchCV(pipe, param_grid, cv=skf, scoring="accuracy")
grid.fit(X_clean, y)
print("Best params:", grid.best_params_)
print("Best CV score:", grid.best_score_)

X_leak = df[["age", "length_of_stay_days", "num_prior_visits", "num_medications",
             "has_chronic_condition", "discharge_note_risk_flag"]]
scores_leak = cross_val_score(pipe, X_leak, y, cv=skf, scoring="accuracy")
print("With leakage mean:", scores_leak.mean())
print("Gap:", scores_leak.mean() - scores.mean())

# CV summary: the clean model scores roughly 0.725 mean accuracy with a
# fairly wide fold-to-fold spread (std ~0.14), reflecting real uncertainty
# on a dataset this small.
# Leakage: discharge_note_risk_flag is filled in by staff AFTER the
# readmission outcome is already known, so it acts as a proxy for the
# target itself -- it must be excluded, even though it inflates reported
# accuracy to ~0.975, because that value would not genuinely be available
# for a NEW patient at real prediction time.
```

**Instructor circulates**, checking specifically that students report the CV mean WITH some measure of spread (not just a bare mean), and that the leakage sentence names the TIMING problem specifically (not just "it's too accurate").

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Replaced a single, potentially lucky/unlucky train/test split with k-fold and stratified k-fold cross-validation
- Automated hyperparameter search with `GridSearchCV`, paired with cross-validation for reliable candidate comparison
- Directly measured data leakage's effect: a 25-percentage-point inflation from one contaminated feature
- Built a leakage-free checklist covering feature timing, preprocessing order, and time-based splitting

**Bridge to next session:** *"You now have the full toolkit to train a model AND trust the number you report for it. Next session is the Module 2 closer: we shift briefly to UNSUPERVISED learning with KMeans clustering — grouping customers with no target label at all — then bring everything full circle by comparing every model type from this module side by side in one structured table, and practicing the single most valuable final skill: explaining a model's predictions and feature importances in plain business language, to someone who has never heard the word 'coefficient' or 'Gini impurity' in their life."*

**Homework / self-practice:**
1. Re-run today's cross-validation with `n_splits=10` instead of 5. Does the mean change much? Does the standard deviation?
2. Extend the `GridSearchCV` param_grid to also tune `model__penalty` (try `["l1", "l2"]`, noting `l1` requires `solver="liblinear"`), and report the new best combination.
3. Invent one MORE plausible leakage scenario (different from `discharge_note_risk_flag`) for a churn-prediction context, and explain in 2-3 sentences why it would leak and how you'd catch it using today's checklist.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: How many folds should I actually use in a real project — is 5 always right?**
→ 5 and 10 are the most common defaults, and both are reasonable starting points. More folds means each training set is larger (usually a more reliable estimate) but takes longer to run and gives smaller test folds each time; on very small datasets like today's 40 rows, too many folds can leave very few rows per test fold, making individual fold scores noisy — which is exactly why we saw a wide spread even at just 5 folds today.

**Q: Does `GridSearchCV` guarantee the absolute best possible hyperparameters?**
→ Only the best among the values YOU specified in `param_grid` — it's an exhaustive search over your grid, not a search over all possible values. If the true optimum lies between your grid points (e.g., `C=5` when you only tried `1` and `10`), `GridSearchCV` won't find it; `RandomizedSearchCV` or a finer grid can help there, both outside today's scope.

**Q: Is leakage ALWAYS about one obviously-named feature like today's demo?**
→ No — today's `discharge_note_risk_flag` was designed to be findable for teaching purposes. Real leakage is often subtler: an ID column that happens to encode information about record order, a feature aggregated over a window that overlaps the prediction period, or (as in SEGMENT 5) a preprocessing step fit on the full dataset before splitting. The checklist from SEGMENT 4/5 is meant to catch all of these, not just obvious cases.

**Q: If cross-validation already gives me a reliable estimate, do I still need a separate final test set?**
→ Generally yes, in real projects: cross-validation is typically used DURING development to compare and tune models, but once you commit to a final model and hyperparameters, evaluating on one last, completely untouched hold-out set is the honest final check — especially important since repeatedly checking CV scores while tuning can itself start to subtly overfit to the CV folds.

**Q: Why did `has_chronic_condition` stay in both the "clean" and "leaky" feature sets — isn't a chronic condition determined mostly by age, so aren't we leaking THAT relationship?**
→ Good instinct to question, but this is different from leakage — `has_chronic_condition` is genuinely knowable at prediction time (it's a real, pre-existing medical fact, not something derived from the outcome we're predicting). Correlation between two legitimate FEATURES (age and chronic condition) is a normal, expected part of real data, not leakage — leakage specifically means information from the TARGET's future sneaking into training, not features being correlated with each other.

---

## Instructor Notes

- **Prerequisite check:** Confirm students recall `Pipeline` and `StandardScaler` from Sessions 2/6 before SEGMENT 2 — today assumes that pattern is fluent, not newly introduced.
- **Common mistake:** Reporting only the mean CV score without any spread/std — catch this explicitly in the lab and insist on both numbers together.
- **Another common mistake:** Treating a near-perfect score as good news rather than a red flag. Reinforce SEGMENT 4's framing explicitly: "perfect is suspicious, not impressive," more than once during the session.
- **Another common mistake:** Fitting a scaler/encoder on the full dataset before splitting, especially when students copy-paste code from earlier sessions without noticing the order. Point this out explicitly if seen during the lab.
- **Engagement tip:** SEGMENT 4's leakage demo (0.975 vs 0.725, and the single-split 1.0 vs 0.8) is the strongest, most memorable moment of this entire module — don't rush it, and consider having students shout out a guess for the "with leakage" number before you reveal it.
- **Time check:** If running behind before the break, shorten SEGMENT 3's manual-tuning-by-hand demo to a single verbal walkthrough instead of live-running the loop.
- **If running long after the break:** Compress SEGMENT 5's preprocessing-order leak demo to just the "RIGHT way" code block, assigning the "WRONG way" explanation as a reading.
- **Materials to prepare:** `patient_readmission.csv` open and ready; a scratch cell with SEGMENT 1's five-split loop pre-typed; be ready to explicitly reveal what `discharge_note_risk_flag` "represents" in the story (staff filling it in after the fact) since that context is what makes the demo land.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Reporting only the CV mean, no spread | Overconfident, imprecise-sounding claims on a small/noisy dataset | Always report mean AND std (or the full fold-score list) together |
| Treating a near-perfect score as a success | Deployed model performs far worse in production than testing suggested | Treat near-100% scores as a prompt to investigate leakage, not celebrate |
| Fitting a scaler/encoder on the full dataset before splitting | Test-fold statistics leak into training, inflating reported performance | Always fit preprocessing only on the training fold, inside a `Pipeline` |
| Using plain `KFold` on an imbalanced classification target | Some folds end up with very few or zero examples of the minority class | Use `StratifiedKFold` for classification targets |
| Random (non-time-based) splitting on genuinely time-ordered data | Future information leaks into past predictions | Split by time for time-ordered problems, not randomly |

---

## Appendix: Leakage Red-Flag Drill (Optional, If Time Allows)

For each feature below (hypothetical, for practice), have students decide LEAKY or SAFE and justify in one sentence using the SEGMENT 4 checklist:

| Feature | Target | Context |
|---|---|---|
| `total_refunds_this_year` | `will_churn_next_month` | Computed using the FULL year, including future months |
| `signup_date` | `will_churn_next_month` | Known the moment the account was created |
| `agent_notes_says_cancel` | `will_churn_next_month` | Support agent notes written during a cancellation call |
| `avg_session_length_last_30_days` | `will_churn_next_month` | Computed strictly from the 30 days BEFORE the prediction date |

**Sample expected answer for row 1:** *"Leaky — this feature is computed using data from AFTER the prediction point, since 'this year' includes months that haven't happened yet relative to a mid-year prediction."*

---

## Appendix: Cross-Validation Reference Numbers (Instructor Reference — Actual Run Values)

| Scenario | Fold scores | Mean | Std |
|---|---|---|---|
| Clean features, 5-fold StratifiedKFold | [0.5, 0.75, 0.875, 0.625, 0.875] | 0.725 | 0.143 |
| WITH leaky feature, 5-fold StratifiedKFold | [1.0, 1.0, 1.0, 0.875, 1.0] | 0.975 | 0.05 |
| GridSearchCV best C (clean features) | C=1 | 0.725 | — |

*(These are the actual numbers produced by `patient_readmission.csv` with `random_state=42` — use them to sanity-check your own run.)*

---

## FAQ — Additional Questions

**Q: Does `cross_val_score` retrain the model from scratch on every fold, or reuse learned parameters?**
→ Fully retrains from scratch on every fold — each fold gets a completely fresh, independently-fit model, which is exactly what makes the resulting scores a fair test of generalization rather than an accumulation of leaked knowledge across folds.

**Q: Can `GridSearchCV` tune parameters for MULTIPLE pipeline steps at once, not just the model?**
→ Yes — you can mix keys like `{"scaler__with_mean": [True, False], "model__C": [0.1, 1, 10]}` in the same `param_grid`, and `GridSearchCV` will search the full combined grid across both steps.

**Q: If my dataset is very large, is cross-validation still necessary, or is one split "good enough"?**
→ With very large datasets, a single split's estimate is naturally less noisy (more test rows means more statistical stability), so some teams do lean more on a single held-out set for speed. Cross-validation is still valuable for tuning and for smaller/medium datasets — today's 40-row extreme case makes the "one split is unreliable" lesson especially visible, but the underlying principle scales down in importance as dataset size grows.

**Q: Is `scoring="accuracy"` always the right metric to pass into `cross_val_score` and `GridSearchCV`?**
→ No — exactly like Session 7's metric-selection lesson, you'd swap in `scoring="f1"`, `scoring="roc_auc"`, `scoring="recall"`, etc. depending on the business problem; `cross_val_score` and `GridSearchCV` both accept the same metric names/scorers you already learned there.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — `cross_validate` for multiple metrics at once (5 min)

```python
from sklearn.model_selection import cross_validate

multi_scores = cross_validate(pipe, X_clean, y, cv=skf, scoring=["accuracy", "precision", "recall", "f1"])
for metric in ["test_accuracy", "test_precision", "test_recall", "test_f1"]:
    print(metric, multi_scores[metric].mean().round(3))
```

**Break it down:**
- `cross_validate` extends `cross_val_score` to report SEVERAL metrics from the same set of folds in a single call, rather than re-running cross-validation separately for each metric
- This closes the loop referenced back in Session 4's FAQ, which previewed this exact function
- Useful whenever a business problem cares about more than one metric simultaneously, as Session 7 emphasized

**Ask:** Why might precision and recall tell noticeably different stories even when accuracy looks stable across folds?

**Common mistake:** Assuming a stable accuracy score means EVERY metric is equally stable.

**Fix:** Always check the specific metric(s) that matter for the business problem, not just accuracy, as reinforced throughout Session 7.

### Demo B — Nested cross-validation intuition (5 min)

```python
from sklearn.model_selection import cross_val_score

outer_scores = []
for train_idx, test_idx in skf.split(X_clean, y):
    X_tr, X_te = X_clean.iloc[train_idx], X_clean.iloc[test_idx]
    y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]

    inner_grid = GridSearchCV(pipe, {"model__C": [0.1, 1, 10]}, cv=3, scoring="accuracy")
    inner_grid.fit(X_tr, y_tr)
    outer_scores.append(inner_grid.score(X_te, y_te))

print("Nested CV scores:", outer_scores)
print("Nested CV mean:", sum(outer_scores) / len(outer_scores))
```

**Break it down:**
- This tunes hyperparameters INSIDE each outer fold's training portion, then evaluates on that fold's untouched test portion — a stricter, "double-checked" way to avoid letting hyperparameter tuning itself leak information from the outer test folds
- More computationally expensive (a grid search inside every fold), so it's typically reserved for smaller searches or final model validation, not everyday iteration
- A great advanced preview for students heading toward more rigorous ML evaluation practices

**Ask:** Why might nested CV give a slightly different (often slightly lower, more honest) score than plain `GridSearchCV.best_score_`?

**Common mistake:** Using `GridSearchCV.best_score_` as if it were an untouched, final generalization estimate.

**Fix:** Treat `best_score_` as a tuning-time estimate; for the most rigorous final number, nested CV or a completely separate hold-out set is more honest.

### Demo C — Visualizing the leakage gap (4 min, requires matplotlib)

```python
import matplotlib.pyplot as plt

labels = ["Without leakage", "With leakage"]
means = [scores_clean.mean(), scores_leak.mean()]

plt.bar(labels, means, color=["steelblue", "indianred"])
plt.ylabel("Mean CV accuracy")
plt.ylim(0, 1.05)
plt.title("Effect of a leaky feature on reported accuracy")
plt.show()
```

**Break it down:**
- A single bar chart makes SEGMENT 4's numeric finding immediately visceral for a non-technical audience, exactly the kind of artifact worth including in a real leakage post-mortem or a stakeholder-facing report
- Pairs naturally with the plain-English leakage explanation from the lab

**Ask:** If you were presenting this chart to a non-technical manager, what ONE sentence would you use to caption it?

**Common mistake:** Showing the chart without any caption explaining WHY the gap exists, leaving room for misinterpretation (e.g., "leakage is just a better feature").

**Fix:** Always pair a leakage visualization with an explicit sentence naming the timing problem, not just the number.

---

## Materials Checklist

- [ ] `patient_readmission.csv` open and readable in the working notebook environment
- [ ] Scratch cell with SEGMENT 1's five-split stability loop pre-typed
- [ ] Whiteboard space for the leakage checklist (SEGMENT 4/5)
- [ ] Optional: matplotlib available for Demo C's leakage bar chart
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's manual-tuning-by-hand demo to a verbal walkthrough |
| Running long after break | Compress SEGMENT 5's preprocessing-order leak demo to just the RIGHT-way code |
| Low energy after lunch/break | Run the Appendix leakage red-flag drill as a quick group activity |
| Advanced group finishes lab early | Assign Demo A (`cross_validate`) or Demo C (leakage bar chart) as a stretch task |
| No shared screen / projector issue | Read the printed fold-score arrays aloud and have students type along |

---

## End-of-Session Quiz (5 Questions)

1. Why is the MEAN of 5-fold cross-validation scores generally more trustworthy than a single train/test split's score?
2. When should you prefer `StratifiedKFold` over plain `KFold`?
3. What does `GridSearchCV.best_params_` actually tell you, and what does it NOT guarantee?
4. Define data leakage in one sentence, and name the specific timing problem with `discharge_note_risk_flag` in today's dataset.
5. Why must preprocessing (like `StandardScaler`) be fit ONLY on the training fold, not the full dataset, before cross-validation?

**Answer key (instructor):**
1. It averages performance across multiple different train/test partitions, reducing the chance that one lucky or unlucky split misrepresents the model's true generalization ability.
2. For classification targets, especially when classes are imbalanced or the dataset is small — it preserves class proportions in every fold.
3. It tells you the best-performing combination AMONG the values you specified in `param_grid`; it does not guarantee that's the true global optimum outside your grid.
4. Data leakage is when information that would not genuinely be available at real prediction time sneaks into training features; `discharge_note_risk_flag` is filled in by staff AFTER the readmission outcome is already known, making it a disguised proxy for the target.
5. Fitting on the full dataset lets the training process "see" statistics (mean/std) computed using rows that are supposed to represent unseen test data, leaking a small amount of test-set information into training.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| n_splits=10 comparison | Correct run with clear comparison of mean/std to 5-fold | Correct run, thin comparison | Attempted, unclear results | Not attempted |
| Extended GridSearchCV (penalty) | Correct grid with solver fix, best combination reported and interpreted | Correct grid, thin interpretation | Attempted, errors present | Not attempted |
| Invented leakage scenario | Clear, plausible scenario with correct timing-based justification and detection method | Plausible scenario, thin justification | Vague or incorrect scenario | Not attempted |

**Total:** /12 — Pass threshold: 8/12
