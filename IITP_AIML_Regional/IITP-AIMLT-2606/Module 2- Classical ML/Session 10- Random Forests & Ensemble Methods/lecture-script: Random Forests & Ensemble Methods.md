# Lecture Script: Random Forests & Ensemble Methods
> **Instructor Reference** — Module 2: Classical ML | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train a `RandomForestClassifier`, extract and interpret `feature_importances_`, compare a random forest against a single decision tree on performance and interpretability, and save/load a trained model using `joblib`.

**Student profile at this point:** Just finished Session 9 — comfortable with `DecisionTreeClassifier`, `plot_tree`, `export_text`, and diagnosing overfitting via depth sweeps. They've seen ONE tree can be unstable and prone to overfitting when too deep.

**Key outcome:** Every student trains a random forest on `customer_churn.csv`, prints a ranked feature importance table, directly compares train/test accuracy against a single tree, and successfully saves and reloads a model with `joblib`, confirming the reloaded model produces identical predictions.

**Dataset for this session:** `customer_churn.csv` (in this folder) — same 36-row telecom churn dataset as Session 9, reused here specifically so today's random forest results are directly comparable to last session's single-tree results.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — From One Tree to a Forest | 10 min | 0:10 |
| SEGMENT 2: Fit/Predict with RandomForestClassifier | 20 min | 0:30 |
| SEGMENT 3: Feature Importances — Explaining the Forest | 20 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 4: Random Forest vs. Single Tree — Head to Head | 20 min | 1:20 |
| SEGMENT 5: Saving and Loading with joblib | 15 min | 1:35 |
| SEGMENT 6: Lab — Full Workflow on customer_churn.csv | 20 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — From One Tree to a Forest (10 min)

### The "Ask 200 Experts" Reveal (6 min)

**Say:** *"Last session, we watched a single decision tree's test accuracy actually PEAK at `max_depth=1` and get no better — sometimes worse — as we let it grow deeper. A single tree, especially on a small dataset, tends to be what statisticians call 'high variance': train it on a slightly different random sample of the same population, and you can get a noticeably different tree with different splits."*

**Live-code this quick demonstration on the projector, reusing Session 9's setup:**

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

df = pd.read_csv("customer_churn.csv")
X = df[["age", "monthly_spend", "tenure_months", "support_tickets"]]
y = df["churned"]

# Same model, five DIFFERENT random splits of the same data
for rs in [0, 1, 42, 7, 99]:
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=rs, stratify=y)
    tree = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree.fit(Xtr, ytr)
    print("split random_state:", rs, "-> test accuracy:", round(tree.score(Xte, yte), 3))
```

**Run it.** Expected output:

```
split random_state: 0 -> test accuracy: 0.556
split random_state: 1 -> test accuracy: 0.889
split random_state: 42 -> test accuracy: 0.778
split random_state: 7 -> test accuracy: 0.778
split random_state: 99 -> test accuracy: 0.889
```

**Say, pointing at the spread from 0.556 to 0.889:** *"Same model, same hyperparameters, same dataset — but depending on which 27 rows happen to land in the training set, this single tree's test accuracy swings by more than 30 percentage points. That's instability, and it's a real problem: it means we can't fully trust ANY single tree's reported accuracy as 'the' performance of this approach. Today's fix: instead of training one tree and hoping we got a lucky split, we train HUNDREDS of trees, each on a randomly resampled version of the training data, and let them vote."*

### Setting Expectations for Today (4 min)

**Say:** *"By the end of today you'll be able to do four things: train a `RandomForestClassifier`, extract feature importances that explain the model's behavior in aggregate, directly compare a forest against a single tree on both performance and interpretability, and save a trained model to disk so it can be reused without retraining. That last skill — saving and loading models — is the first genuinely 'production' skill in this module: every real ML system trains a model ONCE and then reuses it thousands of times, it doesn't retrain from scratch on every single prediction request."*

**Learning contract for today — write on board:**

- Fit and predict with `RandomForestClassifier`
- Extract and interpret `feature_importances_`
- Compare random forest vs. single tree on performance and interpretability
- Save and load a trained model using `joblib`

---

## SEGMENT 2: Fit/Predict with RandomForestClassifier (20 min)

### Building the Pipeline (8 min)

**Say:** *"Same preprocessing pattern as Session 9 — encode the categorical columns, pass numeric columns through — but now the model itself is a `RandomForestClassifier` instead of a single `DecisionTreeClassifier`."*

**Live-code:**

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

X = df_full = pd.read_csv("customer_churn.csv")
X = df_full[["age", "monthly_spend", "tenure_months", "support_tickets",
             "contract_type", "used_mobile_app"]]
y = df_full["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cat_cols = ["contract_type", "used_mobile_app"]
preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(drop="if_binary"), cat_cols),
], remainder="passthrough")

rf_pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42)),
])
rf_pipe.fit(X_train, y_train)

print("Train accuracy:", rf_pipe.score(X_train, y_train))
print("Test accuracy: ", rf_pipe.score(X_test, y_test))
```

**Run it.** Expected output:

```
Train accuracy: 1.0
Test accuracy:  0.8888888888888888
```

**Say:** *"Two new hyperparameters here worth naming explicitly. `n_estimators=200` means we're training 200 individual trees and combining their votes. `max_depth=4` limits how deep EACH of those 200 trees is allowed to grow — same knob as last session, just applied to every tree in the forest rather than one."*

### What "Random" Actually Means in Random Forest (8 min)

**Say:** *"The name isn't just marketing — there are TWO separate sources of randomness baked into how each tree gets built, and both matter."*

**Write on board:**

1. **Bootstrap sampling (row randomness):** Each of the 200 trees is trained on a random SAMPLE of the training rows, drawn WITH replacement — so each tree sees a slightly different (overlapping but not identical) subset of customers, and some rows are seen multiple times by one tree while being skipped entirely by another.
2. **Feature randomness at each split:** At every single split, each tree only considers a random SUBSET of the available features (not all of them) as candidates — so even features that are individually strong predictors don't dominate every single tree's structure.

**Say:** *"Both of these exist for the same underlying reason: to make the 200 trees genuinely DIFFERENT from each other. If every tree saw identical data and considered every feature at every split, they'd all end up nearly identical — and averaging 200 near-identical trees gives you basically nothing beyond what one tree already gave you. The diversity is the entire point."*

**Ask:** *"If `n_estimators=1`, is a Random Forest just... a single decision tree?"* (Almost — with one estimator, you still get bootstrap sampling and feature randomness at each split, which can make it slightly different from a plain `DecisionTreeClassifier`, but the majority-vote averaging benefit disappears entirely since there's nothing to average.)

### Comprehension Check (4 min)

1. *"Why does bootstrap sampling draw rows WITH replacement rather than just splitting the data into 200 non-overlapping chunks?"* (With only ~27 training rows, 200 non-overlapping chunks would be impossibly tiny; sampling with replacement lets every tree train on a full-sized sample while still differing from the others.)
2. *"What would happen to the forest's diversity if we removed the 'random subset of features per split' rule, keeping only row-level bootstrap sampling?"* (Trees would likely look more similar to each other, since the single strongest feature would dominate the root split of nearly every tree — reducing the diversity that makes averaging valuable.)

---

## SEGMENT 3: Feature Importances — Explaining the Forest (20 min)

### Extracting and Ranking Importances (7 min)

**Say:** *"A random forest trades away the single clean root-to-leaf story from last session — you can't meaningfully trace ONE path through 200 trees at once. What it gives you instead is `feature_importances_`, averaged across all 200 trees, which is often a MORE reliable signal than any single tree's importances."*

**Live-code:**

```python
feature_names = rf_pipe.named_steps["pre"].get_feature_names_out()
importances = rf_pipe.named_steps["model"].feature_importances_

for name, score in sorted(zip(feature_names, importances), key=lambda t: -t[1]):
    print(f"{name}: {score:.4f}")
```

**Run it.** Expected output:

```
remainder__support_tickets: 0.2260
remainder__tenure_months: 0.1882
cat__contract_type_Monthly: 0.1836
remainder__monthly_spend: 0.1467
cat__used_mobile_app_Yes: 0.1329
remainder__age: 0.1226
```

**Say:** *"Read this as: `support_tickets` was the single most useful feature for splitting decisions, averaged across all 200 trees — slightly ahead of `tenure_months` and `contract_type`. Notice these all sum to roughly 1.0 — `feature_importances_` is normalized, so you can read each number directly as 'this feature's SHARE of total splitting usefulness,' roughly 22.6% for `support_tickets`."*

### Turning This Into a Business Sentence (6 min)

**Write this template on the board — same "translation" habit from Session 4's coefficients:**

```
"Across the whole forest, [feature] was the [most/2nd most/...] useful signal
for predicting [target], accounting for roughly [importance*100]% of the
model's total splitting decisions."
```

**Have a student phrase this for `support_tickets`.** Expect: *"Across the whole forest, support_tickets was the single most useful signal for predicting churn, accounting for roughly 22.6% of the model's total splitting decisions — customers who file more support tickets are more likely to churn."*

**Say:** *"Notice the phrasing is DELIBERATELY different from Session 4's coefficient sentences. We're not saying 'each additional support ticket adds X to churn probability' — feature importance doesn't give us that precise, per-unit story the way a linear coefficient does. It tells us RELATIVE usefulness across the whole model, not a specific direction or magnitude for a one-unit change."*

### The Instability-of-a-Single-Tree Caveat, Resolved (4 min)

**Say:** *"This directly answers a question you might have from Session 9: a single tree's `feature_importances_` can shift noticeably if you retrain it on a slightly different split — we effectively saw this with the instability demo in SEGMENT 1. Averaging across 200 trees, each seeing a different bootstrap sample, smooths out exactly that kind of noise. This is the single biggest practical reason to prefer a forest's feature importances over one tree's, even when raw accuracy is similar."*

### Quick Check-for-Understanding (3 min)

*"If `age` has the LOWEST importance score in our printed list, does that mean age has NO relationship at all with churn?"* (Not necessarily — it means age was less useful for SPLITTING decisions relative to the other features available; a weak or redundant relationship with other features, or a genuinely weaker signal, can both produce a low importance score.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to guess, before returning, whether a random forest's test accuracy will beat, tie, or lose to the single tree's test accuracy from last session, on this exact dataset and split. Come back ready to compare guesses to the real printed numbers.

---

## SEGMENT 4: Random Forest vs. Single Tree — Head to Head (20 min)

### The Direct Comparison (8 min)

**Say:** *"Let's settle the break-time guess with the actual numbers, side by side, on the identical train/test split."*

**Live-code:**

```python
from sklearn.tree import DecisionTreeClassifier

tree_pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", DecisionTreeClassifier(max_depth=4, random_state=42)),
])
tree_pipe.fit(X_train, y_train)

print("Single tree   - train:", tree_pipe.score(X_train, y_train), "| test:", tree_pipe.score(X_test, y_test))
print("Random forest - train:", rf_pipe.score(X_train, y_train), "| test:", rf_pipe.score(X_test, y_test))
```

**Run it.** Expected output:

```
Single tree   - train: 0.9629629629629629 | test: 0.7777777777777778
Random forest - train: 1.0                | test: 0.8888888888888888
```

**Say:** *"On THIS split, the forest wins on test accuracy — 0.889 versus 0.778. But the more important lesson isn't this one number, it's what we saw in SEGMENT 1: across FIVE different random splits, the single tree's test accuracy ranged from 0.556 to 0.889, while the forest stayed in a tighter 0.778 to 1.0 band. The forest isn't just more accurate here — it's more RELIABLY accurate, run after run."*

### The Stability Re-Run, Side by Side (5 min)

**Live-code, reusing SEGMENT 1's five-split loop but adding the forest:**

```python
for rs in [0, 1, 42, 7, 99]:
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=rs, stratify=y)

    t_pipe = Pipeline([("pre", preprocess), ("model", DecisionTreeClassifier(max_depth=4, random_state=42))])
    t_pipe.fit(Xtr, ytr)

    r_pipe = Pipeline([("pre", preprocess), ("model", RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42))])
    r_pipe.fit(Xtr, ytr)

    print(f"split={rs:>3} | tree test: {t_pipe.score(Xte, yte):.3f} | forest test: {r_pipe.score(Xte, yte):.3f}")
```

**Run it.** Expected output:

```
split=  0 | tree test: 0.556 | forest test: 0.778
split=  1 | tree test: 0.889 | forest test: 0.889
split= 42 | tree test: 0.778 | forest test: 0.889
split=  7 | tree test: 0.778 | forest test: 0.889
split= 99 | tree test: 0.889 | forest test: 1.000
```

**Say:** *"Look at every single row — the forest is never WORSE than the tree, and on the worst-case tree split (random_state=0, 0.556), the forest still manages 0.778. This is the ensemble effect in its purest, most visible form."*

### The Interpretability Trade-Off Table (4 min)

**Draw this summary table on the board:**

| Aspect | Single Decision Tree | Random Forest |
|---|---|---|
| Typical test accuracy | Good, but can be unstable | Usually higher, more stable across splits |
| Overfitting risk (deep trees) | High | Lower — averaging cancels individual trees' noise |
| Explaining ONE prediction | Full root-to-leaf path, fully traceable | No single path — only aggregate `feature_importances_` |
| Training/inference speed | Fast | Slower (many trees), but still fast at this data scale |
| Best used when... | Regulatory/compliance needs a fully traceable decision | Raw predictive performance and stability matter most |

**Ask:** *"A regulator asks your team to explain EXACTLY why one specific loan applicant was rejected, step by step, in a format a non-technical auditor can follow. Which model from today's table would you reach for, and why?"* (Single decision tree — its root-to-leaf path is a complete, literal explanation for that one applicant, something a forest's aggregate importances cannot fully replicate for a SINGLE prediction.)

---

## SEGMENT 5: Saving and Loading with joblib (15 min)

### Why We Need This At All (4 min)

**Say:** *"Training this forest took a noticeable fraction of a second on 27 rows. On a real production dataset — millions of rows, hundreds of trees — training can take minutes to hours. No real system retrains from scratch every time it needs to make one prediction. You train ONCE, save the trained model to disk, and load that saved file whenever you need predictions — potentially thousands of times, across many separate program runs, without ever retraining."*

### Saving and Reloading, Live (7 min)

**Live-code:**

```python
import joblib

joblib.dump(rf_pipe, "churn_rf_model.joblib")
print("Model saved.")

loaded_pipe = joblib.load("churn_rf_model.joblib")

original_preds = rf_pipe.predict(X_test)
loaded_preds = loaded_pipe.predict(X_test)

print("Predictions identical:", (original_preds == loaded_preds).all())
print("Loaded model test accuracy:", loaded_pipe.score(X_test, y_test))
```

**Run it.** Expected output:

```
Model saved.
Predictions identical: True
Loaded model test accuracy: 0.8888888888888888
```

**Say:** *"This confirms the entire trained pipeline — preprocessing AND all 200 trees, with every learned threshold intact — survived the round trip to disk and back, byte for byte in terms of behavior. Notice we saved the whole `Pipeline`, not just the `RandomForestClassifier` — this means the ColumnTransformer's fitted encoder (which learned exactly which categories exist for `contract_type` and `used_mobile_app`) is saved too, so the loaded model can accept raw, unencoded new data directly."*

### Common `joblib` Pitfalls (4 min)

**Say:** *"Three things to watch for in real projects, all common enough to be worth naming explicitly:"*

1. *"The scikit-learn VERSION used to save and the version used to load should match, or at least be close — loading a model saved with a much older or newer scikit-learn version can silently produce warnings or, in worse cases, subtly wrong behavior."*
2. *"`joblib` files are Python-specific and not meant to be human-readable or portable to other languages — if you need to serve a model from a non-Python system, you'd typically look at formats like ONNX instead, which is beyond today's scope."*
3. *"Never load a `.joblib` file from an untrusted source — like Python's `pickle` module (which `joblib` builds on for many object types), loading a malicious file can execute arbitrary code. Only load files you trained yourself or that came from a trusted, verified source."*

---

## SEGMENT 6: Lab — Full Workflow on customer_churn.csv (20 min)

### Instructions (read aloud, step by step)

1. Load `customer_churn.csv`; build `X` with all six features and `y` as `churned`.
2. Split with `train_test_split(test_size=0.25, random_state=42, stratify=y)`.
3. Build the same `ColumnTransformer` preprocessing as Session 9.
4. Train a `RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42)` inside a `Pipeline`.
5. Report train and test accuracy, and print the ranked `feature_importances_` table.
6. Train a `DecisionTreeClassifier(max_depth=4, random_state=42)` on the SAME split and compare test accuracy directly against the forest.
7. Save the forest pipeline with `joblib.dump`, reload it, and confirm predictions match.
8. Write two sentences: one naming the top feature by importance in business language, one stating whether the forest beat the single tree on this split.

### Starter Code

```python
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("customer_churn.csv")
X = df[[___, ___, ___, ___, ___, ___]]
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=___, random_state=42, stratify=___
)

cat_cols = ["contract_type", "used_mobile_app"]
preprocess = ColumnTransformer([
    ("cat", ___(drop="if_binary"), cat_cols),
], remainder="passthrough")

rf_pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", ___(n_estimators=___, max_depth=___, random_state=42)),
])
rf_pipe.___(X_train, y_train)

print("RF Train accuracy:", rf_pipe.score(___, ___))
print("RF Test accuracy: ", rf_pipe.score(___, ___))

feature_names = rf_pipe.named_steps["pre"].get_feature_names_out()
importances = rf_pipe.named_steps["model"].___
for name, score in sorted(zip(feature_names, importances), key=lambda t: -t[1]):
    print(f"{name}: {score:.4f}")

tree_pipe = Pipeline(steps=[("pre", preprocess), ("model", ___(max_depth=4, random_state=42))])
tree_pipe.fit(X_train, y_train)
print("Tree test accuracy:", tree_pipe.score(X_test, y_test))

joblib.___(rf_pipe, "churn_rf_model.joblib")
loaded = joblib.___("churn_rf_model.joblib")
print("Predictions match:", (rf_pipe.predict(X_test) == loaded.predict(X_test)).all())

# TODO: write your two interpretation sentences here as comments
```

### Reference Solution

```python
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("customer_churn.csv")
X = df[["age", "monthly_spend", "tenure_months", "support_tickets",
        "contract_type", "used_mobile_app"]]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cat_cols = ["contract_type", "used_mobile_app"]
preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(drop="if_binary"), cat_cols),
], remainder="passthrough")

rf_pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42)),
])
rf_pipe.fit(X_train, y_train)

print("RF Train accuracy:", rf_pipe.score(X_train, y_train))
print("RF Test accuracy: ", rf_pipe.score(X_test, y_test))

feature_names = rf_pipe.named_steps["pre"].get_feature_names_out()
importances = rf_pipe.named_steps["model"].feature_importances_
for name, score in sorted(zip(feature_names, importances), key=lambda t: -t[1]):
    print(f"{name}: {score:.4f}")

tree_pipe = Pipeline(steps=[("pre", preprocess), ("model", DecisionTreeClassifier(max_depth=4, random_state=42))])
tree_pipe.fit(X_train, y_train)
print("Tree test accuracy:", tree_pipe.score(X_test, y_test))

joblib.dump(rf_pipe, "churn_rf_model.joblib")
loaded = joblib.load("churn_rf_model.joblib")
print("Predictions match:", (rf_pipe.predict(X_test) == loaded.predict(X_test)).all())

# Top feature: support_tickets was the single most useful signal for the
# forest, accounting for roughly 22.6% of total splitting usefulness --
# customers who raise more support tickets are more likely to churn.
# Comparison: the random forest (test accuracy 0.889) beat the single tree
# (test accuracy 0.778) on this split, consistent with the stability
# advantage discussed in SEGMENT 4.
```

**Instructor circulates**, checking specifically that students save the `Pipeline` object (not just the raw `RandomForestClassifier`), and that the feature-importance sentence uses the "relative usefulness" framing rather than a Session 4-style coefficient/direction claim.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Trained a `RandomForestClassifier` and understood the two sources of randomness (bootstrap rows + feature subsets per split) that make ensembling work
- Extracted and interpreted `feature_importances_`, and phrased them correctly as relative usefulness, not per-unit direction
- Directly compared random forest vs. single tree on both accuracy/stability and interpretability
- Saved and reloaded a trained model with `joblib`, confirming identical predictions

**Bridge to next session:** *"Today you saw that a random forest is more accurate and more stable than a single tree — but we only checked that stability across FIVE manually-chosen random splits, which is itself a bit ad hoc. Next session formalizes this properly: k-fold and stratified k-fold cross-validation give us a systematic, repeatable way to estimate how reliable a model's performance really is, `GridSearchCV` automates hyperparameter tuning instead of us manually trying `n_estimators` and `max_depth` combinations by hand, and we'll learn to spot and prevent data leakage — a mistake that can make a model look great in testing while being secretly broken in production."*

**Homework / self-practice:**
1. Sweep `n_estimators` over `[1, 10, 50, 100, 200]` with `max_depth=4` fixed, and report train/test accuracy at each value. At what point do additional trees stop meaningfully helping?
2. Retrain the forest with `max_depth=None` (unlimited) instead of `max_depth=4`. Does the forest show the same clear overfitting signature a single unlimited-depth tree showed last session? Why might a forest be more resistant to this?
3. Load your saved `churn_rf_model.joblib` in a FRESH Python session (restart the kernel first) and confirm it still produces correct predictions without re-running any training code.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: If more trees is generally better, why not always use `n_estimators=10000`?**
→ Returns diminish quickly — beyond a certain point (often a few hundred trees for small-to-medium datasets), additional trees barely move accuracy but do increase training time, memory usage, and file size when saved with `joblib`. A common practice is to sweep `n_estimators` (like today's homework) and pick a value where the curve visibly flattens.

**Q: Does a random forest ever perform WORSE than a single well-tuned tree?**
→ It's uncommon but possible, particularly on very small or very simple datasets where one tree already captures the full pattern cleanly and averaging adds mostly noise rather than diversity. In practice, on real-world tabular data, random forests are one of the most reliable "first strong baseline" choices precisely because this failure case is rare.

**Q: Can I get a feature importance ranking that's specific to just ONE prediction, not the whole model?**
→ Not from `feature_importances_` directly — that's a GLOBAL, whole-model summary. For per-prediction explanations, dedicated tools like SHAP values exist (outside today's scope), which decompose one specific prediction into each feature's individual contribution.

**Q: Is `random_state` doing the same job here as it did for `train_test_split`?**
→ Same underlying purpose — reproducibility — but controlling a different randomness source: here it fixes which rows get bootstrap-sampled into each tree and which features are considered at each split, so re-running the exact same code produces an identical forest.

**Q: We used `max_depth=4` for both the tree and forest today — was that a fair comparison?**
→ Yes, deliberately — keeping `max_depth` identical isolates the ENSEMBLE effect as the only difference between the two models. If we'd also changed depth, we couldn't be sure whether accuracy differences came from ensembling or from depth alone.

---

## Instructor Notes

- **Prerequisite check:** Confirm students still have Session 9's `ColumnTransformer` + `DecisionTreeClassifier` pattern fresh — today reuses it directly for the head-to-head comparison in SEGMENT 4.
- **Common mistake:** Saving just the raw `RandomForestClassifier` with `joblib.dump` instead of the full `Pipeline`, which then fails or behaves unexpectedly when fed raw, unencoded new data later. Catch this explicitly during the lab.
- **Another common mistake:** Interpreting `feature_importances_` with a Session-4-style "direction and magnitude" claim (e.g., "for every extra support ticket, churn goes up by X"). Model the correct "relative usefulness" phrasing explicitly, more than once.
- **Another common mistake:** Assuming the forest will ALWAYS beat the tree on every single run/split without checking — reinforce that SEGMENT 4's multi-split comparison, not a single lucky run, is what makes the case convincingly.
- **Engagement tip:** SEGMENT 4's five-split side-by-side table (tree column noticeably more volatile than forest column) is the strongest "aha" moment of the day — don't rush it, and consider running one or two EXTRA random states live if there's time and energy in the room.
- **Time check:** If running behind before the break, shorten SEGMENT 3's "why this matters" business-sentence exercise to a single instructor-led example rather than having a student phrase it live.
- **If running long after the break:** Compress SEGMENT 5's `joblib` pitfalls list to just the "save the whole Pipeline" point, assigning the version-mismatch and security notes as a reading.
- **Materials to prepare:** `customer_churn.csv` open and ready; confirm `joblib` is installed (it ships with scikit-learn by default, but verify on the training machine); a scratch cell with SEGMENT 1's five-split loop pre-typed so it doesn't eat live-coding time.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Saving only `RandomForestClassifier`, not the full `Pipeline` | Loaded model fails on raw, unencoded new data | Always `joblib.dump` the entire fitted `Pipeline` |
| Interpreting `feature_importances_` with a direction/magnitude claim | Misleading claims like "importance 0.23 means +0.23 churn probability per unit" | Use "relative usefulness / share of splitting decisions" framing instead |
| Comparing forest vs. tree at DIFFERENT `max_depth` values | Invalid comparison — can't isolate the ensembling effect | Keep `max_depth` identical when comparing model types |
| Drawing conclusions about stability from a SINGLE train/test split | Overconfident or misleading "the forest always wins" claim | Compare across multiple `random_state` splits, as in SEGMENT 4 |
| Loading a `.joblib` file from an untrusted source | Potential arbitrary code execution (security risk) | Only load files you trained yourself or from a verified, trusted source |

---

## Appendix: Feature Importance Interpretation Drill (Optional, If Time Allows)

For each printed importance below (hypothetical, for practice), have students phrase the plain-English business sentence using the board template:

| Feature | Importance | Target |
|---|---|---|
| days_since_last_login | 0.31 | churn |
| claim_amount | 0.27 | fraud_flag |
| num_pages_visited | 0.18 | conversion |
| response_time_hours | 0.22 | customer_satisfaction |

**Sample expected answer for row 1:** *"Across the whole forest, days_since_last_login was the single most useful signal for predicting churn, accounting for roughly 31% of the model's total splitting decisions."*

---

## Appendix: n_estimators Sweep Reference Table (Instructor Reference — Actual Run Values)

| n_estimators | Train accuracy | Test accuracy |
|---|---|---|
| 1 | 0.889 | 0.889 |
| 10 | 1.000 | 1.000 |
| 50 | 1.000 | 0.889 |
| 100 | 1.000 | 0.889 |
| 200 | 1.000 | 0.889 |

*(These are the actual numbers produced by `customer_churn.csv` with `random_state=42`, `max_depth=4` — a good discussion point: more trees is not a monotonic improvement on tiny datasets, and stabilizes quickly. Emphasize that this exact curve shape is dataset-specific; the general "returns diminish" lesson is what generalizes.)*

---

## FAQ — Additional Questions

**Q: Does `RandomForestClassifier` need `stratify=y` for the same reason as Session 9's single tree?**
→ Yes — nothing about using a forest changes the reasoning; `stratify=y` is about the TRAIN/TEST split itself, independent of which model you plan to fit afterward.

**Q: Can I control HOW MANY features each tree considers per split?**
→ Yes, via the `max_features` parameter (default `"sqrt"` for classifiers, meaning each split considers roughly the square root of the total feature count). This is the exact knob behind the "feature randomness at each split" idea discussed in SEGMENT 2.

**Q: Is a Random Forest the same thing as "Gradient Boosting"?**
→ No — both are ensembles of trees, but they combine trees differently. A random forest trains all trees independently, in parallel, and averages their votes. Gradient boosting (e.g. `GradientBoostingClassifier`, XGBoost) trains trees SEQUENTIALLY, where each new tree tries to correct the previous trees' mistakes. Both are valuable, but boosting is outside today's scope.

**Q: If I retrain the exact same `RandomForestClassifier(random_state=42)` on the exact same data, will I get the exact same trees every time?**
→ Yes — `random_state` makes the bootstrap sampling and feature-subset selection fully reproducible, so identical code and identical data will always produce an identical forest.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Out-of-bag (OOB) score as a "free" validation estimate (5 min)

```python
rf_oob = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42, oob_score=True)
rf_oob_pipe = Pipeline(steps=[("pre", preprocess), ("model", rf_oob)])
rf_oob_pipe.fit(X_train, y_train)
print("OOB score:", rf_oob_pipe.named_steps["model"].oob_score_)
print("Test score:", rf_oob_pipe.score(X_test, y_test))
```

**Break it down:**
- Each tree's bootstrap sample leaves out roughly a third of the training rows ("out-of-bag" rows) — those rows can be used to evaluate that specific tree without touching the actual test set at all
- Averaging each row's out-of-bag predictions across every tree that didn't see it gives a built-in performance estimate, `oob_score_`, essentially "free" cross-validation
- It's a nice sanity check, but doesn't replace a proper held-out test set or the cross-validation techniques coming next session

**Ask:** Why might `oob_score_` sometimes differ noticeably from the actual test accuracy on such a small dataset?

**Common mistake:** Treating `oob_score_` as a full replacement for train/test splitting or cross-validation.

**Fix:** Use it as a helpful extra signal, especially useful when data is too scarce to comfortably carve out a separate validation set, but not as the ONLY evaluation method for a real project.

### Demo B — Visualizing one tree FROM the forest (5 min, requires matplotlib)

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

one_tree_from_forest = rf_pipe.named_steps["model"].estimators_[0]
feature_names = rf_pipe.named_steps["pre"].get_feature_names_out()

plt.figure(figsize=(14, 8))
plot_tree(one_tree_from_forest, feature_names=feature_names, class_names=["Stay", "Churn"], filled=True)
plt.show()
```

**Break it down:**
- `estimators_` is the list of all 200 individual fitted trees inside the forest — indexing `[0]` grabs just the first one
- Visually comparing this tree to a couple of its siblings (`estimators_[1]`, `estimators_[50]`, etc.) makes the "each tree is genuinely different" claim from SEGMENT 2 concrete rather than abstract
- A great bridge back into the bootstrap-sampling and feature-randomness discussion

**Ask:** Do you expect the ROOT split to be the same feature across most of the 200 trees, given `support_tickets` had the highest overall importance?

**Common mistake:** Assuming every tree in the forest looks roughly identical to the single tree trained in Session 9.

**Fix:** Actually plot 2-3 different `estimators_` indices side by side to see the real diversity.

### Demo C — Predicting on a brand-new customer with the saved model (4 min)

```python
new_customer = pd.DataFrame({
    "age": [30], "monthly_spend": [600], "tenure_months": [4],
    "support_tickets": [5], "contract_type": ["Monthly"], "used_mobile_app": ["No"],
})
loaded_pipe = joblib.load("churn_rf_model.joblib")
print("Predicted churn:", loaded_pipe.predict(new_customer))
print("Predicted probability:", loaded_pipe.predict_proba(new_customer))
```

**Break it down:**
- This is the real-world payoff of SEGMENT 5 — a freshly loaded model, with zero retraining, making a prediction on a brand-new customer it has never seen
- `predict_proba` works on the forest exactly like it did on `LogisticRegression` back in Session 6 — it returns the fraction of the 200 trees that voted for each class, which doubles as a natural confidence estimate
- A strong closing demo before the lab, tying together saving/loading with the prediction workflow

**Ask:** Given this customer's high support ticket count and short tenure, does the predicted probability align with what we'd intuitively expect from SEGMENT 3's feature importance ranking?

**Common mistake:** Forgetting that `predict_proba` returns probabilities for BOTH classes (column 0 = stay, column 1 = churn), and mis-reading which column is which.

**Fix:** Always check `.classes_` on the underlying model to confirm column order before reading `predict_proba` output.

---

## Materials Checklist

- [ ] `customer_churn.csv` open and readable in the working notebook environment
- [ ] Confirm `joblib` is available (ships with scikit-learn)
- [ ] Scratch cell with SEGMENT 1's five-split stability loop pre-typed
- [ ] matplotlib available for Demo B's single-tree-from-forest visualization
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's business-sentence exercise to one instructor-led example |
| Running long after break | Compress SEGMENT 5's joblib pitfalls list to just the "save the whole Pipeline" point |
| Low energy after lunch/break | Run the Appendix feature-importance interpretation drill as a quick group activity |
| Advanced group finishes lab early | Assign Demo A (OOB score) or Demo B (visualize one tree from the forest) as a stretch task |
| No shared screen / projector issue | Read the printed importance tables aloud and have students type along |

---

## End-of-Session Quiz (5 Questions)

1. What are the TWO sources of randomness inside a Random Forest, and what does each one accomplish?
2. Why is `feature_importances_` from a forest generally more reliable than from a single tree?
3. What is the main interpretability trade-off you give up when moving from a single tree to a forest?
4. Why must you save the entire `Pipeline` with `joblib`, not just the `RandomForestClassifier`?
5. In SEGMENT 4's five-split comparison, what pattern in the printed numbers demonstrated the forest's added STABILITY (not just accuracy)?

**Answer key (instructor):**
1. Bootstrap sampling of rows (each tree trains on a different random sample) and random feature subsets considered at each split — both increase diversity across the 200 trees, which is what makes averaging valuable.
2. Because it's averaged across many trees, each trained on a different bootstrap sample, smoothing out the split-to-split instability a single tree can show.
3. You lose the single, fully-traceable root-to-leaf explanation for one specific prediction — you're left with aggregate feature importances instead.
4. The Pipeline includes the fitted `ColumnTransformer`/encoder; saving only the model would break when new, unencoded raw data is passed in later.
5. The forest's test accuracy stayed in a tighter range (0.778-1.0) across all five splits, while the single tree's ranged much more widely (0.556-0.889).

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| n_estimators sweep | All five values reported with a clear "diminishing returns" observation | Values reported, thin interpretation | Partial values, no interpretation | Not attempted |
| max_depth=None forest comparison | Correct run with clear reasoning about forest's overfitting resistance | Correct run, thin reasoning | Attempted, unclear results | Not attempted |
| Fresh-kernel model reload | Confirmed correct predictions with no retraining, clearly demonstrated | Reload worked, demonstration unclear | Attempted, errors present | Not attempted |

**Total:** /12 — Pass threshold: 8/12
