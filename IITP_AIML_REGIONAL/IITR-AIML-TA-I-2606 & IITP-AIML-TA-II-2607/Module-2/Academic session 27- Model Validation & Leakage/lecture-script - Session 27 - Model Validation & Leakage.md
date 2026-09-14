# Lecture Script: Machine Learning — Model Validation & Leakage
> **Instructor Reference** — Module 2: Classical ML | Academic Session 27 | Duration: 2 Hours | Instructor: Aswath Rao

---

## Session Overview
**Goal:** By the end of this session, students can implement k-fold and stratified k-fold cross-validation, search hyperparameters systematically with `GridSearchCV`, read its results, and detect data leakage scenarios beyond Session 18's preprocessing-order mistake.

**Student profile at this point:** Has hand-tuned `alpha` (Session 21), `max_depth` (Session 25), and `n_estimators` (Session 26) by trying a few values and eyeballing results. Comfortable with `cross_val_score` from Session 17, but has never seen it formalized or automated. Likely wrong assumption: several will assume shuffling always fixes any imbalance risk, not realizing stratification is a distinct, stronger guarantee. Boredom risk: low — the degenerate-fold demonstration is designed to be a genuine shock moment.

**Key outcome:** Students should leave with a default habit: reach for `StratifiedKFold` and `GridSearchCV` automatically for any future classification project, rather than hand-tuning one parameter at a time.

> 🎯 **The one sentence this session must land:** *Every hyperparameter you've hand-tuned since Session 21 can be found systematically instead of by trial and error — and a suspiciously good score is a leakage red flag, not a reason to celebrate.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Sorted Spreadsheet Trap" | 8 min | 8 min |
| Concept Block 1: K-Fold Cross-Validation, Formalized | 10 min | 18 min |
| Concept Block 2: Stratified K-Fold | 12 min | 30 min |
| Practical Block 1: Predict the Broken Fold | 8 min | 38 min |
| Concept Block 3: GridSearchCV | 12 min | 50 min |
| **BREAK** | 10 min | 60 min |
| Concept Block 4: Reading GridSearchCV Results | 10 min | 70 min |
| Practical Block 2: Live Coding Demo (TA Code) | 16 min | 86 min |
| Concept Block 5: Data Leakage Beyond Preprocessing | 12 min | 98 min |
| Practical Block 3: Spot the Leaky Feature | 10 min | 108 min |
| Summary & Bridge | 6 min | 114 min |
| Q&A & Doubt Solving | 6 min | 120 min |

---

## Opening — "The Sorted Spreadsheet Trap" (8 min)

Open with this, verbatim-ish:

> "Suppose your company's data export tool always pulls customer records sorted by signup date. You run a 5-fold cross-validation. What could possibly go wrong just from that sorting?"

Pause. Let a few guesses land.

> "Here's what actually happens with our churn data, sorted and run through plain `KFold` without shuffling: one fold has exactly zero churners in it. Another fold is 100% churners. Not approximately — exactly zero, and exactly all of them. Today we fix this, and then automate everything you've been hand-tuning since Session 21."

**Pivot line:** "This session has two halves: making cross-validation actually trustworthy, and making hyperparameter search actually systematic instead of guesswork."

**Context for sessions ahead:** "Every model you build for the rest of your career should default to the habits from today — this is the last new 'how do I trust my results' concept before Module 2 wraps up."

---

## Concept Block 1: K-Fold Cross-Validation, Formalized (10 min)

> "Recall Session 17's cricket selector — never judging form off one innings. K-fold cross-validation formalizes exactly this: split into k folds, train on k-1, test on the remaining one, rotate k times, average the results."

```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=1)
scores = cross_val_score(pipeline, X, y, cv=kf)
```

> "With `n_splits=5` on our 150-row churn dataset, that's 5 folds of 30 rows each — train on 120, test on 30, five times."

### 🔴 The trap / highest-value moment
> "Always set `shuffle=True` with a fixed `random_state`, unless you have a specific reason not to. Without shuffling, if your data is sorted or grouped in any way, some folds can become wildly unrepresentative. Write this down: *shuffle by default, or risk exactly the disaster from the opening.*"

---

## Concept Block 2: Stratified K-Fold (12 min)

> "Imagine randomly splitting a class into 5 groups for a mock election, but the class list happens to be sorted by which candidate students support. Even with shuffling, plain random splitting can still occasionally cluster too many or too few of one group's supporters into a single fold by chance. Without shuffling at all, that clustering becomes guaranteed, not just possible."

Write the definition:

> Stratified k-fold guarantees every fold preserves roughly the same class proportion as the whole dataset.

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
```

### 🔴 The trap / highest-value moment
> "This isn't a theoretical worst case — real datasets pulled from databases are very often sorted by date, region, or some other field. Write this down: *default to StratifiedKFold for classification, especially with imbalanced classes — it costs nothing and prevents a real, common failure.*"

---

## Practical Block 1: Predict the Broken Fold (8 min)

Show the class a version of the churn dataset sorted by the `churned` column (don't reveal results yet). Ask: "if I run plain, unshuffled `KFold` with 5 splits on this exact ordering, what do you predict happens to at least one of the folds?" Let pairs discuss for 2 minutes and commit to a prediction, then reveal the actual result in the next block's demo.

---

## Concept Block 3: GridSearchCV (12 min)

> "Recall hand-tuning alpha in Session 21, max_depth in Session 25, n_estimators in Session 26 — try a value, check the result, try another. GridSearchCV automates this entirely."

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__max_depth": [3, 5, None],
}

grid_search = GridSearchCV(pipeline, param_grid, cv=skf, scoring="accuracy")
grid_search.fit(X, y)
```

> "3 values times 3 values is 9 combinations, each evaluated with 5-fold CV — 45 total fits — and it automatically returns the best-performing combination."

### 🔴 The trap / highest-value moment
> "Because `GridSearchCV` wraps the entire pipeline, each fold's preprocessing is correctly fit only on that fold's training portion — Session 18's 'fit only on train' rule, applied automatically and correctly across every single fold. Write this down: *always wrap the FULL pipeline in GridSearchCV, not just the model, or you risk leakage creeping back in.*"

---

## BREAK (10 min)

---

## Concept Block 4: Reading GridSearchCV Results (10 min)

Write the three key attributes on the board:

| Attribute | What it tells you |
|---|---|
| `best_params_` | The winning combination |
| `best_score_` | Its average cross-validated score |
| `cv_results_` | The full leaderboard of every combination tried |

> "On our churn data, the winner might be `max_depth=5, n_estimators=50` — notably not the largest `n_estimators` tried, echoing Session 26's diminishing-returns point."

### 🔴 The trap / highest-value moment
> "The 'best' combination is only best for this specific dataset and this specific scoring metric. Changing from accuracy to F1 (Session 23) can change which combination wins. Write this down: *always confirm you're optimizing for the metric that matches your actual business scenario.*"

---

## Practical Block 2: Live Coding Demo (TA Code) (16 min)

**Handoff line (must match TA code file's opening comment):** "Let's actually see that broken fold happen, fix it with stratification, then run a real GridSearchCV search."

Hand off to `ta-code - Session 27 - Model Validation & Leakage.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Sort the churn dataset by `churned` to simulate realistic database-export ordering
2. Run plain unshuffled `KFold` and print each fold's churn count — reveal the exact 0-churner and 100%-churner folds, confirming Practical Block 1's predictions
3. Run `StratifiedKFold` on the same sorted data and show every fold now reflects the true ~25% churn rate
4. Run `GridSearchCV` over `n_estimators` and `max_depth` for a `RandomForestClassifier`, printing `best_params_` and `best_score_`
5. Add a deliberately leaky proxy feature and show cross-validated accuracy jump from a genuine ~81% to a suspicious ~97%, then remove it and explain why

💬 Expect real reaction at the 0/100% fold reveal — let it land before moving on.

---

## Concept Block 5: Data Leakage Beyond Preprocessing (12 min)

> "Session 18 taught one specific leakage mistake — scaling before splitting. Leakage can be far subtler. Imagine a churn dataset with a column called `flagged_for_retention_call` — set by customer support only *after* they've already identified someone as a likely churner."

> "That's like predicting a cricket match's outcome using the 'player of the match' award — which is only given out after the match ends. The feature technically sits in your dataset, but it wouldn't exist at the actual moment you need to make a real prediction."

### 🔴 The trap / highest-value moment
> "An unusually large jump in performance after adding a feature is not automatically good news — it's exactly as likely to be a leakage red flag as a genuine improvement. Write this down: *ask 'would I know this before the outcome happens?' — if the answer is no, the feature likely leaks the target.*"

---

## Practical Block 3: Spot the Leaky Feature (10 min)

Present 4 candidate features for a loan-default model (`monthly_income`, `days_since_last_missed_payment_notice`, `employment_type`, `account_closed_date`). Have students individually flag which ones are at risk of leakage and justify why, then cold-call for reasoning. `account_closed_date` and `days_since_last_missed_payment_notice` are the intended discussion points — both could easily only exist because the bad outcome already happened.

---

## Summary & Bridge (6 min)

| Concept | The one thing to remember |
|---|---|
| K-fold CV | Formalizes Session 17's "don't trust one split" into a repeatable procedure |
| Stratified k-fold | Guarantees every fold reflects true class balance, regardless of data ordering |
| `GridSearchCV` | Automates hyperparameter search that's been done by hand since Session 21 |
| Reading results | `best_params_`, `best_score_`, `cv_results_` — and confirm the right scoring metric |
| Feature leakage | A suspicious jump in performance is a red flag, not good news, until investigated |

Close on the thesis line: "Every hyperparameter you've hand-tuned since Session 21 can be found systematically instead of by trial and error — and a suspiciously good score is a leakage red flag, not a reason to celebrate."

**Bridge to next session:** "We've spent this entire module on supervised learning — predicting a known outcome. Session 28 shifts to unsupervised learning with `KMeans` clustering, and also shows you how to compare several trained models side by side using a structured metric table, closing out Module 2 before evaluation."

---

## Q&A & Doubt Solving (6 min)

**Q: Does GridSearchCV always use the same cv object I define, or does it re-shuffle each time?**
→ If you pass a specific `KFold` or `StratifiedKFold` object with a fixed `random_state`, it reuses those exact same folds for every combination it tries, ensuring a fair comparison.

**Q: Is there a faster alternative to GridSearchCV for large parameter grids?**
→ Yes — `RandomizedSearchCV` samples a random subset of combinations rather than trying all of them, useful when the grid is too large to search exhaustively. It's outside today's scope but good to know it exists.

**Q: How many folds should I use — is 5 always right?**
→ 5 or 10 are common defaults, balancing reliability against computation time. More folds generally give a more reliable estimate but take longer to compute.

**Q: If a feature seems leaky but genuinely improves test performance, should I ever keep it?**
→ Only if you're certain it would be genuinely available at real prediction time — the test is availability at deployment, not just whether it improves a backward-looking evaluation.

**Q: Can leakage happen even with a perfectly correct train/test split?**
→ Yes — that's exactly today's second half. Session 18's leakage was about preprocessing order; today's feature leakage can happen even with a technically correct split, if the feature itself encodes future information.

---

## Instructor Notes
- **Words not yet earned:** KMeans, elbow method, silhouette score — Session 28.
- **Biggest risk in this session:** treating this as "just more sklearn syntax" rather than genuinely internalizing the stratification and leakage lessons — the degenerate-fold demo exists specifically to make this visceral rather than abstract.
- **Board management:** keep the K-fold vs. Stratified K-fold contrast and the GridSearchCV code both visible through Practical Block 2.
- **Common confusions, numbered:**
  1. Assuming `shuffle=True` alone guarantees balanced folds, without needing stratification
  2. Wrapping only the model (not the full pipeline) in `GridSearchCV`, risking leakage
  3. Treating a big performance jump as automatically good news
  4. Forgetting that "best" hyperparameters are tied to a specific scoring metric
- **Cross-references:** Session 21 (Regularization), Session 25 (Decision Trees), and Session 26 (Random Forests) all get their hand-tuned hyperparameters formalized by today's `GridSearchCV`; Session 18 (Data Preparation) is the direct precursor to today's expanded leakage discussion.
- **Local/cultural context notes:** the sorted-by-churn demonstration works well because it mirrors a genuinely common real-world data export pattern (sorted by signup date, region, or status) that students are likely to encounter in actual job settings.
