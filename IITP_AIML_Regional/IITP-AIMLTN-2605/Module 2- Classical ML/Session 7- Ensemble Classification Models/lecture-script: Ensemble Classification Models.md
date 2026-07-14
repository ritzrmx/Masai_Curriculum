# Lecture Script: Ensemble Classification Models
> **Instructor Reference** — Module 2: Classical ML | Session 7 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can explain *why* combining many weak/overfit trees produces a stronger, lower-variance classifier, fit and tune a `RandomForestClassifier`, and interpret `.feature_importances_` responsibly.

**Student profile at this point:** Comfortable with `LogisticRegression`, a single `DecisionTreeClassifier`, `train_test_split`, and reading Gini/information-gain splits from Session 6. Has NOT yet seen bootstrapping, ensembling, or any tuning beyond `max_depth`.

**Key outcome:** By end of class, every student can articulate the bias-variance story of ensembling in one sentence, has a working Random Forest that measurably beats a single tree on the same data, and can rank + sanity-check feature importances.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Why Ensembles? From One Tree to a Forest | 10 min | 0:15 |
| **Practical 1:** A Single Tree Overfits — Prove It | 15 min | 0:30 |
| **Concept 2:** Bagging — Bootstrap Aggregating & Majority Vote | 10 min | 0:40 |
| **Practical 2:** Random Forest vs. Single Tree — The Variance Showdown | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Forest Parameters — Tuning the Ensemble | 10 min | 1:15 |
| **Practical 3:** Sweep `n_estimators`, `max_depth`, `max_features` | 15 min | 1:30 |
| **Concept 4:** Feature Importance — Reading It Right | 10 min | 1:40 |
| **Practical 4:** Rank Importances + the Correlated-Feature Trap | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Ask the class a non-ML question first: *"You need a medical diagnosis. Do you trust one doctor's opinion, or would you rather get the majority opinion of 200 independent doctors, each of whom saw a slightly different subset of your test results?"*

Let a few students answer. Steer toward: more opinions, if independent enough, average out individual mistakes. This is exactly the idea behind ensembles in ML.

**Context to set:** Last session you built a single Decision Tree — powerful, interpretable, but prone to memorizing the training data (100% train accuracy, weaker test accuracy). A single tree is like one doctor: confident, sometimes wrong, and very sensitive to which patients (rows) it happened to study. Today we fix that by growing a **forest** of trees and combining their votes.

**Learning contract for today:**
- Explain *why* many trees beat one tree (bagging + bootstrap sampling)
- Fit a `RandomForestClassifier` and quantify how much variance it removes versus a single tree
- Tune the three parameters that matter most: `n_estimators`, `max_depth`, `max_features`
- Extract, rank, and correctly interpret feature importances

---

## Concept Block 1: Why Ensembles? From One Tree to a Forest (10 min)

### Recall from Session 6: the single-tree problem

A Decision Tree with no depth limit will keep splitting until every leaf is pure (or nearly pure). That gives it very low **bias** — it can fit almost any pattern — but very high **variance**: change the training rows slightly (a different random sample, a different year of data) and you can get a *very different* tree with different splits, different depth, different predictions.

**Teaching point:** "Overfitting" and "high variance" are the same idea seen from two angles. Overfitting = fits training noise. High variance = unstable across resamples of the same population. A single unconstrained tree suffers from both.

### The core ensembling idea

```
ONE MODEL                          MANY MODELS, COMBINED
──────────                         ──────────────────────
 One tree                           Tree 1   Tree 2   Tree 3  ...  Tree N
 sees ALL rows                      each sees a DIFFERENT resample of rows
 memorizes noise                    each memorizes DIFFERENT noise
 one confident (maybe wrong)        N slightly-different opinions
 prediction                         → majority vote / average
                                     → individual noise cancels out,
                                       the shared real signal survives
```

**Key teaching point:** An ensemble does not work because each individual model becomes smarter. Each tree in a forest is still allowed to overfit its own bootstrap sample. The ensemble works because the trees' *mistakes* are different from each other while the *true pattern* is shared by all of them — averaging keeps the signal and cancels the noise.

### Two families of ensembles (preview only — bagging is today's focus)

| Family | Idea | Example | This session? |
|---|---|---|---|
| **Bagging** | Train models in parallel on different bootstrap samples, then vote/average | Random Forest | ✅ Yes |
| **Boosting** | Train models sequentially, each one fixing the previous one's errors | Gradient Boosting, XGBoost | Later in course |

**Teaching point:** Random Forest = Bagging + Decision Trees + one extra trick (random feature subsets per split). We build up to that definition piece by piece over the next two blocks.

---

## Practical Block 1: A Single Tree Overfits — Prove It (15 min)

### Dataset for today
We use `sklearn.datasets.load_breast_cancer` — 569 patient records, 30 numeric measurements from cell nuclei (radius, texture, perimeter, concavity, etc.), binary label (malignant / benign). It is built into scikit-learn (no internet needed), realistic, and has enough correlated features to make the feature-importance caveat later in class concrete.

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = load_breast_cancer()
X, y = data.data, data.target

print("Dataset shape:", X.shape)
print("Classes:", dict(zip(*np.unique(y, return_counts=True))))
print("Feature count:", len(data.feature_names))
```

**Output:**
```
Dataset shape: (569, 30)
Classes: {np.int64(0): np.int64(212), np.int64(1): np.int64(357)}
Feature count: 30
```

*(0 = malignant, 1 = benign — mention `data.target_names` if a student asks.)*

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("Train size:", X_train.shape[0], "Test size:", X_test.shape[0])

# Single deep, unrestricted tree -- exactly like Session 6
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)

train_acc = tree.score(X_train, y_train)
test_acc = tree.score(X_test, y_test)
print(f"\nSingle Decision Tree (no depth limit)")
print(f"Train accuracy: {train_acc:.3f}")
print(f"Test accuracy:  {test_acc:.3f}")
print(f"Tree depth reached: {tree.get_depth()}")
print(f"Overfit gap (train - test): {train_acc - test_acc:.3f}")
```

**Output:**
```
Train size: 426 Test size: 143

Single Decision Tree (no depth limit)
Train accuracy: 1.000
Test accuracy:  0.923
Tree depth reached: 7
Overfit gap (train - test): 0.077
```

**Walk through:** Train accuracy is a perfect 1.000 — the tree memorized every training row. Test accuracy drops to 0.923. That 7.7-point gap is the overfitting signature we flagged last session.

### Now show instability — same tree logic, different data slice

```python
print("--- Instability check: same tree, 5 different train/test splits ---")
for seed in range(5):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    t = DecisionTreeClassifier(random_state=42)
    t.fit(Xtr, ytr)
    print(f"seed={seed}  train_acc={t.score(Xtr, ytr):.3f}  test_acc={t.score(Xte, yte):.3f}")
```

**Output:**
```
seed=0  train_acc=1.000  test_acc=0.930
seed=1  train_acc=1.000  test_acc=0.930
seed=2  train_acc=1.000  test_acc=0.930
seed=3  train_acc=1.000  test_acc=0.937
seed=4  train_acc=1.000  test_acc=0.944
```

**Discussion prompt:** *"Train accuracy is 1.000 every single time — is that reassuring or worrying?"* → It's worrying. A model that always perfectly fits training data regardless of which rows it sees isn't learning a stable pattern; it's memorizing whatever rows happen to be in front of it. Test accuracy bounces around because the memorized noise differs per split.

**Bridge line into Concept 2:** *"What if, instead of training one tree on all 426 rows, we trained 200 trees, each on a different random resample of those same 426 rows, and let them vote?"*

---

## Concept Block 2: Bagging — Bootstrap Aggregating & Majority Vote (10 min)

### What "bagging" means

**Bagging** = **B**ootstrap **AGG**regat**ING**. Two ingredients:

1. **Bootstrap sampling** — from your training set of size *n*, draw *n* rows **with replacement**. Some rows appear multiple times, some are left out entirely (on average, about 37% of rows are left out of any single bootstrap sample — these are called "out-of-bag" rows, useful for a free validation estimate).
2. **Aggregating** — train one model per bootstrap sample, then combine their predictions: majority vote for classification, average for regression.

### ASCII walkthrough — sampling with replacement

Imagine 8 training rows labeled A–H. Three bootstrap samples drawn from them:

```
Original rows:  A  B  C  D  E  F  G  H

Bootstrap sample 1: G  D  E  G  C  H  E  E    (E appears 3x, A/B/F missing)
Bootstrap sample 2: G  B  C  G  C  C  H  E    (C appears 3x, A/D/F missing)
Bootstrap sample 3: D  H  H  C  F  E  B  H    (H appears 3x, A/G missing)
```

**Teaching point:** Every bootstrap sample is the *same size* as the original (8 rows here), but each one is a *different mix* — different rows repeated, different rows dropped. Each tree trained on one of these samples "sees the world" slightly differently.

### From samples to a vote

```
Bootstrap 1 → Tree 1 → predicts "malignant"
Bootstrap 2 → Tree 2 → predicts "benign"
Bootstrap 3 → Tree 3 → predicts "malignant"
        ...                  ...
Bootstrap N → Tree N → predicts "malignant"
                 |
                 v
        MAJORITY VOTE across all N trees
                 |
                 v
        Final ensemble prediction: "malignant"
```

For `RandomForestClassifier`, scikit-learn actually averages the trees' predicted class *probabilities* and picks the highest — a "soft vote" — but the majority-vote intuition is the right mental model.

### The Random Forest's extra trick: random feature subsets

Bagging alone (train N trees on N bootstrap samples of *rows*) is already an ensemble — it's literally called `BaggingClassifier` in scikit-learn. A **Random Forest** adds one more randomization: at **every split**, each tree is only allowed to consider a random subset of the *features* (controlled by `max_features`), not all 30.

**Teaching point — why this matters:** Without it, if one feature (say `worst perimeter`) is extremely predictive, almost every tree in the "forest" would pick it for the very first split, and all the trees would end up highly correlated — nearly identical, defeating the purpose of averaging. Restricting the feature pool per split forces the trees to *disagree* with each other more, and it is exactly that diversity that cancels out individual errors when you vote.

```
Bagging alone:        every split considers ALL features   → trees look similar
Random Forest:        every split considers a RANDOM SUBSET → trees look different
                       of features (e.g. sqrt(30) ≈ 5 at a time)
```

**One-line definition to put on the board:**
> Random Forest = many Decision Trees, each trained on a bootstrap sample of rows, each split restricted to a random subset of features, combined by majority/probability vote.

---

## Practical Block 2: Random Forest vs. Single Tree — The Variance Showdown (15 min)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)

forest = RandomForestClassifier(n_estimators=200, random_state=42)
forest.fit(X_train, y_train)

print("Model            Train Acc   Test Acc   Gap")
t_train, t_test = tree.score(X_train, y_train), tree.score(X_test, y_test)
f_train, f_test = forest.score(X_train, y_train), forest.score(X_test, y_test)
print(f"Single Tree      {t_train:.3f}       {t_test:.3f}      {t_train - t_test:.3f}")
print(f"Random Forest    {f_train:.3f}       {f_test:.3f}      {f_train - f_test:.3f}")
```

**Output:**
```
Model            Train Acc   Test Acc   Gap
Single Tree      1.000       0.923      0.077
Random Forest    1.000       0.958      0.042
```

**Walk through:** Both models still fit training data perfectly (1.000) — each individual tree in the forest is *still* an overfit tree. But the forest's *test* accuracy is higher (0.958 vs. 0.923) and its overfit gap nearly halves (0.042 vs. 0.077). This is the promised effect: combining overfit trees produces a *less* overfit ensemble.

### The real variance story: repeat across many resamples

A single comparison could be luck. Let's check variance directly with 5-fold cross-validation and with 10 independent train/test splits.

```python
print("--- 5-fold cross-validation accuracy (whole dataset) ---")
tree_cv = cross_val_score(DecisionTreeClassifier(random_state=42), X, y, cv=5)
forest_cv = cross_val_score(RandomForestClassifier(n_estimators=200, random_state=42), X, y, cv=5)

print("Single Tree   fold scores:", np.round(tree_cv, 3))
print(f"Single Tree   mean={tree_cv.mean():.3f}  std={tree_cv.std():.3f}")
print("Random Forest fold scores:", np.round(forest_cv, 3))
print(f"Random Forest mean={forest_cv.mean():.3f}  std={forest_cv.std():.3f}")
```

**Output:**
```
--- 5-fold cross-validation accuracy (whole dataset) ---
Single Tree   fold scores: [0.912 0.904 0.93  0.956 0.885]
Single Tree   mean=0.917  std=0.024
Random Forest fold scores: [0.921 0.939 0.982 0.974 0.973]
Random Forest mean=0.958  std=0.024
```

```python
print("--- Test accuracy across 10 different train/test splits ---")
tree_scores, forest_scores = [], []
for seed in range(10):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    t = DecisionTreeClassifier(random_state=42).fit(Xtr, ytr)
    f = RandomForestClassifier(n_estimators=200, random_state=42).fit(Xtr, ytr)
    tree_scores.append(t.score(Xte, yte))
    forest_scores.append(f.score(Xte, yte))

tree_scores, forest_scores = np.array(tree_scores), np.array(forest_scores)
print(f"Single Tree:   mean={tree_scores.mean():.3f}  std={tree_scores.std():.3f}  "
      f"min={tree_scores.min():.3f}  max={tree_scores.max():.3f}")
print(f"Random Forest: mean={forest_scores.mean():.3f}  std={forest_scores.std():.3f}  "
      f"min={forest_scores.min():.3f}  max={forest_scores.max():.3f}")
```

**Output:**
```
--- Test accuracy across 10 different train/test splits ---
Single Tree:   mean=0.932  std=0.023  min=0.874  max=0.965
Random Forest: mean=0.963  std=0.010  min=0.951  max=0.979
```

**Key teaching point — read this out loud:** The Random Forest's standard deviation across 10 splits (0.010) is less than half the single tree's (0.023). Its *worst* result (0.951) beats the single tree's *average* result (0.932). This is variance reduction made concrete — not a promise, a measurement.

**Discussion prompt:** *"We used `n_estimators=200` — 200 trees. Is more always better? What do you think happens with 1 tree in a 'forest'? What about 1000?"* → Bridges directly into Concept Block 3.

---

## BREAK (10 min)

*Suggested break prompt — ask students to guess, before returning: "If I set `n_estimators=1000` instead of `200`, will test accuracy go up, down, or stay about the same? Will training take longer?" Collect a show of hands informally when class resumes.*

---

## Concept Block 3: Forest Parameters — Tuning the Ensemble (10 min)

Three parameters do almost all of the work when tuning a Random Forest.

| Parameter | What it controls | Typical effect of increasing it |
|---|---|---|
| `n_estimators` | Number of trees in the forest | Accuracy improves then **plateaus**; more trees = more training time, not more overfitting |
| `max_depth` | Max depth of each individual tree | Too shallow → underfits (high bias); too deep → each tree overfits more, but forest still absorbs some of it |
| `max_features` | Features considered at each split | Smaller subset → more diverse trees (usually better generalization); `None` (all features) → trees more correlated, closer to plain bagging |

### `n_estimators` — more trees, diminishing returns

```
Accuracy
   ^
   |            ___________________  <- plateau: adding more trees barely helps
   |         __/
   |      __/
   |   __/
   |__/
   +---------------------------------> n_estimators
   1    10    50   100   200   500
```

**Teaching point:** Unlike a single tree's `max_depth`, more trees do **not** cause a Random Forest to overfit more. Each additional tree is just another independent (bootstrap) vote — it adds averaging power, not memorization power. The only real cost of a very large `n_estimators` is compute time. A common default: start at 100–200, increase only if cross-validation still shows the score climbing.

### `max_depth` — shallow trees still work in a forest

**Teaching point:** A single shallow tree (`max_depth=2`) usually underfits badly on its own. But a *forest* of 200 shallow trees can still perform reasonably, because averaging many weak-but-diverse opinions recovers signal that any one shallow tree misses. This is the same idea behind boosting's "weak learners," previewed briefly last block.

### `max_features` — the diversity dial

```
max_features = 'sqrt'  → each split sees ~sqrt(n_features) options → high diversity
max_features = None    → each split sees ALL features              → low diversity (≈ bagging)
```

**Teaching point:** `max_features=None` does not disable randomness entirely — rows are still bootstrapped — but it removes the feature-level randomization that makes a Random Forest different from plain bagging. Expect it to perform similarly to, or slightly worse than, `sqrt`/`log2` on datasets with a few dominant features (exactly what we'll measure next).

### How to tune in practice

**Teaching point:** Don't grid-search all three blindly. Fix `n_estimators` generously (150–300; it rarely hurts), then tune `max_depth` and `max_features` with cross-validation. We will do a manual sweep now; `GridSearchCV`/`RandomizedSearchCV` (automated tuning) is covered in a later session.

---

## Practical Block 3: Sweep `n_estimators`, `max_depth`, `max_features` (15 min)

```python
print("--- Sweep 1: n_estimators (max_depth=None, max_features='sqrt') ---")
print(f"{'n_estimators':>12} {'train_acc':>10} {'test_acc':>10} {'gap':>8}")
for n in [1, 5, 10, 50, 100, 300]:
    f = RandomForestClassifier(n_estimators=n, random_state=42)
    f.fit(X_train, y_train)
    tr, te = f.score(X_train, y_train), f.score(X_test, y_test)
    print(f"{n:>12} {tr:>10.3f} {te:>10.3f} {tr-te:>8.3f}")
```

**Output:**
```
--- Sweep 1: n_estimators (max_depth=None, max_features='sqrt') ---
n_estimators  train_acc   test_acc      gap
           1      0.986      0.923    0.063
           5      1.000      0.937    0.063
          10      1.000      0.951    0.049
          50      1.000      0.951    0.049
         100      1.000      0.958    0.042
         300      1.000      0.958    0.042
```

**Walk through:** Test accuracy climbs sharply from 1 tree (0.923 — barely better than a single tree) up through 10–50 trees, then **plateaus** at 0.958 from 100 trees onward. Going from 100 to 300 trees buys nothing here — exactly the diminishing-returns curve from the concept block.

```python
print("--- Sweep 2: max_depth (n_estimators=200) ---")
print(f"{'max_depth':>12} {'train_acc':>10} {'test_acc':>10} {'gap':>8}")
for d in [1, 2, 3, 5, 10, None]:
    f = RandomForestClassifier(n_estimators=200, max_depth=d, random_state=42)
    f.fit(X_train, y_train)
    tr, te = f.score(X_train, y_train), f.score(X_test, y_test)
    label = d if d is not None else "None"
    print(f"{str(label):>12} {tr:>10.3f} {te:>10.3f} {tr-te:>8.3f}")
```

**Output:**
```
--- Sweep 2: max_depth (n_estimators=200) ---
   max_depth  train_acc   test_acc      gap
           1      0.932      0.916    0.016
           2      0.965      0.944    0.021
           3      0.984      0.951    0.033
           5      0.993      0.951    0.042
          10      1.000      0.958    0.042
        None      1.000      0.958    0.042
```

**Walk through:** Even `max_depth=1` ("stumps" — one split per tree) reaches 0.916 test accuracy purely from voting across 200 of them — striking proof that weak individual learners can combine into a strong ensemble. Test accuracy keeps improving up to `max_depth=10`, then flattens (10 and `None` tie) — the trees stop needing more depth once they're already separating the classes well.

```python
print("--- Sweep 3: max_features (n_estimators=200, max_depth=None) ---")
print(f"{'max_features':>12} {'train_acc':>10} {'test_acc':>10} {'gap':>8}")
for mf in ["sqrt", "log2", 0.5, None]:
    f = RandomForestClassifier(n_estimators=200, max_features=mf, random_state=42)
    f.fit(X_train, y_train)
    tr, te = f.score(X_train, y_train), f.score(X_test, y_test)
    print(f"{str(mf):>12} {tr:>10.3f} {te:>10.3f} {tr-te:>8.3f}")
```

**Output:**
```
--- Sweep 3: max_features (n_estimators=200, max_depth=None) ---
max_features  train_acc   test_acc      gap
        sqrt      1.000      0.958    0.042
        log2      1.000      0.958    0.042
         0.5      1.000      0.958    0.042
        None      1.000      0.951    0.049
```

**Walk through:** `max_features=None` (every split sees all 30 features — plain bagging, no feature randomization) is the *worst* performer here (0.951 test accuracy, largest gap 0.049), while `sqrt`, `log2`, and `0.5` all tie at 0.958. This directly confirms the concept-block claim: feature-level randomness adds tree diversity, and diversity is what variance reduction is built on.

**Discussion prompt:** *"Sweep 3 shows only a 0.007 difference — is `max_features` a big deal on this dataset? Would you expect the gap to be larger on a dataset with one wildly dominant feature?"* → Yes; the more one feature dominates, the more `max_features=None` causes trees to correlate around it.

---

## Concept Block 4: Feature Importance — Reading It Right (10 min)

### How `.feature_importances_` is computed

For each tree, every time a feature is used to split, scikit-learn records how much that split reduced impurity (Gini/entropy), weighted by how many samples reached that node. Average this across all trees in the forest, then normalize so all feature importances sum to 1.0.

```
feature_importances_[i]  ∝  average impurity reduction credited to feature i,
                             across every split, in every tree, weighted by
                             how many samples passed through that split
```

**Teaching point:** Importance measures **how useful a feature was for splitting**, not causation, and not "how correlated with the label" in isolation — a feature can be individually weakly correlated with `y` but highly important because it combines well with other features at deeper splits.

### The critical caveat: correlated / duplicate features split the credit

**Teaching point — this is the single most important warning in this session:** If two features carry the same information (e.g. `radius` and `perimeter` of a roughly circular cell — mathematically related), the forest will sometimes split on one, sometimes on the other. Their *combined* importance reflects the real signal, but *each one individually* will look less important than it actually is — because they're sharing credit. Ranking features by importance and dropping the "unimportant" ones can accidentally discard a feature that matters, just because a correlated twin absorbed part of its credit.

```
Feature X alone (not correlated): importance = 0.15
Feature Y duplicated into Y and Y':
   importance(Y)  = 0.09  \
                            }--- still worth ~0.15 combined, but each LOOKS
   importance(Y') = 0.06  /    individually less important than X
```

**Rule of thumb to give students:** Before trusting a low importance score, check whether that feature is correlated with a higher-ranked one (a correlation matrix or heatmap from Module 1 is the tool for this). Don't drop a feature on importance rank alone without that check.

### `.feature_importances_` vs. permutation importance (brief mention)

**Teaching point:** The built-in `.feature_importances_` (also called "Gini importance" / "Mean Decrease in Impurity") is fast but biased toward high-cardinality numeric features. `sklearn.inspection.permutation_importance` is a slower but more trustworthy alternative — worth a link for curious students, not required today.

---

## Practical Block 4: Rank Importances + the Correlated-Feature Trap (10 min)

```python
import pandas as pd

forest = RandomForestClassifier(n_estimators=300, random_state=42)
forest.fit(X_train, y_train)

importances = pd.Series(forest.feature_importances_, index=data.feature_names)
ranked = importances.sort_values(ascending=False)

print("Top 10 features by importance:")
print(ranked.head(10).round(4))
print("\nSum of all importances:", round(importances.sum(), 4))
```

**Output:**
```
Top 10 features by importance:
worst perimeter         0.1457
worst area              0.1441
worst concave points    0.1146
mean concave points     0.0983
worst radius            0.0724
mean radius             0.0607
mean perimeter          0.0560
mean concavity          0.0452
mean area               0.0368
worst concavity         0.0282
dtype: float64

Sum of all importances: 1.0
```

**Walk through:** `worst perimeter`, `worst area`, and `worst radius` are all near the top — and geometrically, perimeter, area, and radius of a roughly circular shape are all derived from the same underlying measurement. That's not a coincidence — it's the correlated-feature effect predicted in the concept block. Confirm with the class: *"If perimeter, area, and radius are basically the same information measured three ways, should we trust their individual rankings, or think of them as one 'size' signal?"*

### Prove the caveat directly: duplicate the top feature

```python
top_feature = ranked.index[0]
copy_name = top_feature + " (duplicate)"
print("Top feature:", top_feature, "importance:", round(ranked.iloc[0], 4))

X_df = pd.DataFrame(X, columns=data.feature_names)
X_df[copy_name] = X_df[top_feature]  # exact duplicate column

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_df, y, test_size=0.25, random_state=42, stratify=y
)
forest2 = RandomForestClassifier(n_estimators=300, random_state=42)
forest2.fit(X_train2, y_train2)
importances2 = pd.Series(forest2.feature_importances_, index=X_df.columns).sort_values(ascending=False)

print("\nAfter duplicating the top feature, importances for the two copies:")
print(importances2[[top_feature, copy_name]].round(4))
print("Combined importance of the two copies:",
      round(importances2[[top_feature, copy_name]].sum(), 4))
print("Test accuracy unaffected:", round(forest2.score(X_test2, y_test2), 3))
```

**Output:**
```
Top feature: worst perimeter importance: 0.1457

After duplicating the top feature, importances for the two copies:
worst perimeter                0.1105
worst perimeter (duplicate)    0.1270
dtype: float64
Combined importance of the two copies: 0.2375
Test accuracy unaffected: 0.958
```

**Walk through — this is the payoff moment of the session:** We added a column that is a **literal, perfect duplicate** of `worst perimeter` — zero new information. Its original importance (0.1457) *dropped* to 0.1105 once it had to share credit with its exact twin. If a student only looked at `worst perimeter`'s new score, they might wrongly conclude it became less predictive — it didn't; the model's test accuracy (0.958) is unchanged. The credit was simply split between two identical columns.

**Discussion prompt:** *"If you saw this in a real project — a feature's importance dropped after adding a new column — what would you check before concluding the feature stopped mattering?"* → Correlation with the new column, first.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Why a single deep tree has low bias but high variance, and why that instability motivates ensembling
- Bagging = bootstrap sampling (rows, with replacement) + aggregating (majority/probability vote)
- Random Forest = bagging + a random subset of *features* considered at every split, which is what keeps the trees diverse
- Measured variance reduction directly: forest std (0.010) less than half the single tree's std (0.023) across 10 splits
- Tuned `n_estimators` (diminishing returns after ~100), `max_depth` (even stumps vote well), `max_features` (`None` under-performs `sqrt`/`log2`)
- Extracted and ranked `.feature_importances_`, and proved by direct experiment that correlated/duplicate features split their importance credit — don't drop features on rank alone

**Bridge to next session:** *"Today we asked 'is this Random Forest accurate?' using plain accuracy. But accuracy hides a lot — a model can be 95% accurate and still be useless if it never catches the 5% of cases you actually care about, like fraud or disease. Next class: Classification Metrics & Threshold Analysis — precision, recall, ROC-AUC, and how to choose the right decision threshold for your problem."*

**Homework / self-practice:** Using `load_wine()` (or `load_digits()` for more of a challenge) from `sklearn.datasets`, repeat today's workflow: fit a single tree and a Random Forest, compare train/test accuracy and 5-fold CV std, sweep `max_features`, and rank the top 5 features by importance. Write one sentence on whether any of the top features look correlated.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: If each tree in the forest still overfits its own bootstrap sample, how is the forest not also overfit?**
→ Each tree overfits *differently* — it memorizes noise specific to its own resample. When you average/vote across many trees, the noise (which differs tree to tree) tends to cancel out, while the true signal (shared by all trees, because it's really in the data) reinforces itself. Individual overfitting does not imply ensemble overfitting.

**Q: Is a Random Forest a "black box" now that it's 200 trees instead of one readable tree?**
→ You lose the ability to trace one clean decision path like you could with a single tree, but you gain `.feature_importances_` for global interpretability, and tools like `permutation_importance` or SHAP (mentioned briefly, not required yet) for deeper explanation. It's a trade: less step-by-step readability, more robustness.

**Q: Why does `max_features=None` (using all features) not just always win, since the tree gets more information at each split?**
→ More information per split makes each individual tree *slightly* more accurate, but it also makes the trees more similar to each other. Similar trees make similar mistakes, and voting across similar mistakes doesn't cancel them out. The whole point of the forest is diversity, and `max_features=None` reduces that diversity.

**Q: Do I need to scale/normalize features before `RandomForestClassifier`, like we did for Logistic Regression?**
→ No. Trees split on thresholds ("is `worst radius` > 16.8?"), and thresholds are unaffected by the scale of the feature. Scaling is a non-issue for tree-based models — one of their practical advantages.

**Q: How many trees is "enough" for a real project, not just this toy dataset?**
→ There's no universal number. Start around 100–300, watch cross-validation score as you increase `n_estimators`, and stop once the score plateaus (like Sweep 1 today). More trees past the plateau only cost training time, not accuracy.

**Q: Can Random Forest be used for regression, not just classification?**
→ Yes — `RandomForestRegressor` works identically, but aggregates by averaging predicted numbers instead of voting on classes. Everything from today (bagging, `n_estimators`, `max_features`, feature importance, the correlated-feature caveat) applies the same way.

---

## Instructor Notes

- **Dataset:** `load_breast_cancer()` is fully offline, loads instantly, has 30 real (and usefully correlated) numeric features, and is small enough that every sweep in this script runs in well under a second — safe for live coding without dead air.
- **Common student mistake:** Assuming more trees can overfit a Random Forest the same way a deeper single tree can. Reinforce with Sweep 1's output: test accuracy plateaus, it does not fall, as `n_estimators` grows. This is a genuinely different behavior from `max_depth`, and worth repeating twice.
- **Common student mistake:** Reading `.feature_importances_` as "this feature causes the outcome." Importance is about split usefulness, not causal effect. Use the duplicate-column demo in Practical 4 as the concrete counter-example whenever this comes up.
- **Live-coding tip:** Before running Practical Block 2's variance comparison, ask the class to predict whether the Random Forest's std will be higher, lower, or the same as the single tree's. Getting a wrong prediction on record makes the correct result (std cut by more than half) land harder.
- **Live-coding tip:** In Practical 4, before running the duplication demo, ask "what do you think will happen to `worst perimeter`'s importance number?" Most students guess it stays the same (since nothing about the real signal changed) — the drop to 0.1105 is a genuine surprise and the best teaching moment of the day.
- **For advanced students:** Introduce `forest.estimators_[0]` to inspect one individual tree from the forest directly (e.g., `.get_depth()`, `.tree_.node_count`), and `oob_score_` (set `oob_score=True` at construction) as a "free" validation estimate that doesn't require a held-out test set, because each tree already ignores ~37% of rows during its own training.
- **For advanced students:** Pose the question — "Since bagging trains trees independently, could this be parallelized?" Yes: `n_jobs=-1` in `RandomForestClassifier` trains trees on all CPU cores simultaneously, unlike boosting methods (next-next session territory), which are inherently sequential.
- **Time check:** If running long after the break, compress Practical 3 to just the `n_estimators` and `max_features` sweeps (skip `max_depth`) — the diminishing-returns and diversity stories are the two that matter most for the wrap-up narrative. If running short, add the `oob_score_` demonstration from the advanced-student note above as a live bonus.
