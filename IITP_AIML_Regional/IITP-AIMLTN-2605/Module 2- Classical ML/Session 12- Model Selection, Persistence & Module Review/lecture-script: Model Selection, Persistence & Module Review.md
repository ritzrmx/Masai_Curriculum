# Lecture Script: Model Selection, Persistence & Module Review
> **Instructor Reference** — Module 2: Classical ML | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students build ONE end-to-end capstone artifact — load data → `Pipeline(StandardScaler + model)` → `GridSearchCV` → score once on an untouched test set → `joblib.dump` → reload and predict — and leave with a decision framework for choosing a model in the first place.

**Student profile at this point:** They have completed Sessions 1–11. They can split data, spot leakage and overfitting, fit linear/Ridge/Lasso regression, evaluate with MAE/RMSE/R², fit logistic regression, KNN, decision trees, random forests and gradient boosting, evaluate with precision/recall/F1/ROC-AUC, cluster with K-Means and DBSCAN, and reduce dimensions with PCA. What they have **never** done: chosen between all of these deliberately, tuned hyperparameters automatically, or saved a model to disk.

**Key outcome:** A `.joblib` file on their machine containing a tuned, leak-proof pipeline that predicts on new rows — plus the checklist they will use on every ML project for the rest of their career.

**Tone for this session:** Consolidating and slightly celebratory. This is the last session of Module 2. Roughly half of it is new machinery (tuning, Pipeline, persistence), half is stepping back and connecting the dots.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — Nine algorithms, one decision | 5 min | 0:05 |
| **Concept 1:** The Model Selection Framework | 10 min | 0:15 |
| **Practical 1:** Bake-off — baseline vs six candidates | 15 min | 0:30 |
| **Concept 2:** Hyperparameter Tuning — Grid vs Randomized | 10 min | 0:40 |
| **Practical 2:** Pipeline + GridSearchCV, and the leakage proof | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Persistence — shipping the whole Pipeline | 10 min | 1:15 |
| **Practical 3:** The capstone — end-to-end and saved to disk | 15 min | 1:30 |
| **Concept 4:** Module Review and the Bridge to Module 3 | 10 min | 1:40 |
| **Practical 4:** Reload the artifact and score a new customer | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Write these nine names on the board, in a single row:**

```
Linear · Ridge · Lasso · Logistic · KNN · Decision Tree · Random Forest · Gradient Boosting · K-Means / DBSCAN / PCA
```

*"Every one of these, you can now fit in three lines of code. Here is the uncomfortable question: a manager drops a CSV on your desk on Monday and asks for a model by Friday. Which one do you type first — and how do you defend that choice?"*

Let the silence sit. Then: *"For eleven sessions we taught you tools. Today we teach you judgement — and then how to hand the finished thing to someone else, so it is a product and not a notebook."*

**What model selection is NOT:**
- NOT trying all nine and shipping whichever has the highest test score
- NOT always reaching for the fanciest algorithm you know
- NOT a permanent decision — it is a starting bet you are willing to revise

**What model selection IS:**
- A **decision** driven by problem type, data size, and how much you need to explain the result
- Starting at the **simplest defensible baseline** and forcing complexity to earn its place
- A comparison made on **cross-validation scores of the training set**, never on the test set

---

## Concept Block 1: The Model Selection Framework (10 min)

### The board table — students should copy this

| Target | Data size | Need to explain it? | Start with | Escalate to |
|---|---|---|---|---|
| Number | Any | Yes | Linear / Ridge | Lasso if many useless columns |
| Number | Large | No | Ridge | Random Forest → Gradient Boosting |
| Category | Small | Yes | Logistic Regression | Decision Tree |
| Category | Small, few columns | No | KNN | Random Forest |
| Category | Large | No | Random Forest | Gradient Boosting |
| None (no labels) | Any | — | K-Means | DBSCAN if odd shapes / outliers |
| Too many columns | Any | — | PCA | — |

### The three questions, in order

1. **What is `y`?** A number → regression. A category → classification. Nothing → unsupervised.
2. **How big is the data, and how many columns?** KNN dies on wide data. Gradient boosting needs rows to be worth it.
3. **Who has to trust the answer?** If a bank regulator or a doctor must audit the decision, an unexplainable model is not on the menu at any accuracy.

### Say this out loud, twice

> *"Start with the simplest baseline. Only add complexity if it earns its place."*

**Earning its place means:** a *meaningfully* better cross-validation score (not a 0.2% flicker inside the standard deviation), worth the extra training time and tuning effort, and still auditable enough for whoever consumes the prediction.

*"There are real production systems, at real companies, running logistic regression today. Not because nobody knew about boosting — because logistic regression won the bake-off and nothing since has beaten it."*

---

## Practical Block 1: The Bake-Off (15 min)

**Goal:** Compare a dumb baseline against six candidates, fairly, using cross-validation on the *training* set only.

```python
import time
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

X, y = load_breast_cancer(return_X_y=True, as_frame=True)

# Split FIRST. The test set does not participate in today's decision at all.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Train:", X_train.shape, " Test:", X_test.shape)

candidates = {
    "Baseline (most frequent)": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression":      LogisticRegression(max_iter=5000, random_state=42),
    "KNN (k=5)":                KNeighborsClassifier(n_neighbors=5),
    "Decision Tree":            DecisionTreeClassifier(random_state=42),
    "Random Forest":            RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting":        GradientBoostingClassifier(random_state=42),
}

rows = []
for name, estimator in candidates.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", estimator)])
    t0 = time.time()
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")
    rows.append({
        "model":      name,
        "cv_roc_auc": round(scores.mean(), 4),
        "std":        round(scores.std(), 4),
        "fit_secs":   round(time.time() - t0, 2),
    })

results = pd.DataFrame(rows).sort_values("cv_roc_auc", ascending=False)
print(results.to_string(index=False))
```

**Expected shape of the output:** the baseline sits at ROC-AUC 0.50 (it is a coin that always says "malignant"), the tree lands around 0.90, and **Logistic Regression, KNN, Random Forest and Gradient Boosting all cluster around 0.98–0.99** — with logistic regression typically edging it out while training in a fraction of the time of the ensembles.

**Live walk-through:** Read the table out from the bottom up. First: *"the baseline is 0.50 — every real model beats a coin flip, good, that is the minimum bar and it is not a compliment."* Then point at the `fit_secs` column next to the `cv_roc_auc` column and ask the room:

> *"Gradient boosting took roughly 40 times longer than logistic regression. Look at the score column. Did it earn its place?"*

Make them say "no" out loud. Then land the punch: *"The simplest model on this table won. That is not a rigged demo — that happens constantly, and if you skip the bake-off you will never know it."* Also point at the `std` column: a 0.003 gap between two models whose standard deviations are 0.014 is not a real gap. It is noise.

---

## Concept Block 2: Hyperparameter Tuning (10 min)

### Parameters vs hyperparameters — the distinction that unlocks this

**Write on the board:**

```
PARAMETERS      →  the model LEARNS them from data   →  coefficients, split points
HYPERPARAMETERS →  YOU choose them before training   →  alpha, k, max_depth, n_estimators, C
```

*"Every hyperparameter you have set this module — `alpha=1.0`, `n_neighbors=5`, `max_depth=3` — you guessed. Today the computer stops you guessing."*

### The two searches

| | `GridSearchCV` | `RandomizedSearchCV` |
|---|---|---|
| What it tries | **Every** combination | `n_iter` random draws |
| Cost | Explodes: 5 × 4 × 3 = 60 fits × cv folds | You set the budget |
| Use when | Few hyperparameters, small ranges | Many hyperparameters, wide ranges |
| Grid format | Lists of values | Lists **or** distributions |

### The anatomy of a search

```
GridSearchCV(
    estimator = pipe,          # the Pipeline being tuned
    param_grid = {...},        # what to try — note the "model__" prefix
    cv = 5,                    # 5-fold cross-validation, from Session 2
    scoring = "roc_auc",       # WHICH metric decides the winner
)
→ .best_params_      the winning settings
→ .best_score_       its cross-validated score  (NOT a test score)
→ .best_estimator_   the winner, already refitted on ALL training data
```

**The double underscore.** `"model__C"` means "the `C` hyperparameter of the step named `model`". Two underscores, not one. This is the single most common typo in this session.

**When the grid explodes, switch to random draws.** Same API, but you buy a fixed budget of `n_iter` fits instead of an exhaustive sweep:

```python
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint

rf_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  RandomForestClassifier(random_state=42)),
])

dist = {
    "model__n_estimators":     randint(50, 300),     # a RANGE, not a list
    "model__max_depth":        [3, 5, 10, None],
    "model__min_samples_leaf": randint(1, 10),
}

rs = RandomizedSearchCV(rf_pipe, dist, n_iter=10, cv=5,
                        scoring="roc_auc", random_state=42, n_jobs=-1)
rs.fit(X_train, y_train)
print(rs.best_params_, round(rs.best_score_, 4))
```

*"An exhaustive grid over those three ranges is thousands of fits. This is 10. And it usually lands within a hair of the grid's answer — because most hyperparameters barely matter, and random draws find the two that do."*

**`scoring` is a decision, not a default.** Set `scoring="roc_auc"` and the search optimises ranking quality. Set `scoring="recall"` and it will happily accept more false alarms to catch more true cases. On a cancer screen or a fraud detector, that choice matters more than the algorithm you picked.

### The one unbreakable rule

**Draw this on the board:**

```
TRAIN  ───┬─── fold, fold, fold, fold, fold  →  cross-validation  →  tune here ✅
          │
TEST   ───┴───────────────────────────────────  touch ONCE, at the very end ✅
```

*"If you try 50 hyperparameter settings and keep the one with the best **test** score, you have used the test set 50 times. It is now training data wearing a disguise, and your reported number is a lie — not to me, to yourself. Tuning happens inside the training data. Full stop."*

---

## Practical Block 2: Pipeline + GridSearchCV (15 min)

**Part A — see the leak, then close it.** This is the most important twelve lines of the session.

```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# 100 rows, 2000 columns of PURE NOISE, and a target that is PURE COIN FLIPS.
# There is genuinely nothing to learn here. The honest score is 0.50.
rng = np.random.RandomState(42)
X_noise = rng.normal(size=(100, 2000))
y_coin  = rng.randint(0, 2, size=100)

# WRONG — pick the "best" 10 columns using ALL the data, then cross-validate
selector = SelectKBest(f_classif, k=10).fit(X_noise, y_coin)
X_leaked = selector.transform(X_noise)
wrong = cross_val_score(LogisticRegression(max_iter=1000), X_leaked, y_coin, cv=5)
print("WRONG — prepare first, CV after :", round(wrong.mean(), 3))

# RIGHT — the SAME selection step, but inside a Pipeline so it refits per fold
pipe = Pipeline([
    ("select", SelectKBest(f_classif, k=10)),
    ("model",  LogisticRegression(max_iter=1000)),
])
right = cross_val_score(pipe, X_noise, y_coin, cv=5)
print("RIGHT — selection inside Pipeline:", round(right.mean(), 3))
```

**Expected output:** the WRONG line lands around **0.8**. The RIGHT line lands around **0.5**.

**Live walk-through:** Stop everything here. *"There is no signal in this data. None. I generated the labels with a random coin. And the first approach reports 80% accuracy."* Ask the room: *"Where did the information come from?"* → It came from the selector, which peeked at all 100 labels to pick the 10 columns that happened to correlate with the coin flips by luck. When cross-validation later "held out" a fold, those columns had **already seen** that fold's labels. Same data, same model, same `cv=5` — the only difference is *where the preparation step lives*. **The Pipeline is not a convenience wrapper. It is the leakage fix from Session 2, made structural.**

**Part B — now tune the winner from the bake-off.**

```python
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=5000, random_state=42)),
])

param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}   # note: model__C, TWO underscores

search = GridSearchCV(pipe, param_grid, cv=5, scoring="roc_auc", n_jobs=-1)
search.fit(X_train, y_train)          # training data ONLY

print("Best params:", search.best_params_)
print("Best CV ROC-AUC:", round(search.best_score_, 4))
print("Winning estimator:", search.best_estimator_)
```

**Expected output:** a small `C` (strong regularisation) wins, with a cross-validated ROC-AUC around 0.99. Note that `best_estimator_` prints as a whole `Pipeline`, scaler included — **that object is the artifact we are going to ship.**

---

## BREAK (10 min)

*Mull this over: you tried 5 values of `C` and reported the best cross-validation score of the five. Is that number itself slightly optimistic? Why? And does the untouched test set fix it?*

---

## Concept Block 3: Persistence — Shipping the Whole Pipeline (10 min)

### The problem

*"Your model exists in the RAM of a Jupyter kernel. Close the laptop and it is gone. Nobody can use it, nobody can audit it, and the web team certainly cannot call it. A model that lives only in a notebook is a hobby, not a product."*

### The fix — two lines

```python
import joblib

joblib.dump(search.best_estimator_, "cancer_pipeline.joblib")   # write to disk
model = joblib.load("cancer_pipeline.joblib")                   # read it anywhere
model.predict(new_rows)
```

`joblib` is scikit-learn's preferred saver because it handles the big NumPy arrays inside models efficiently. It is a superset of `pickle` for this purpose.

### The four rules — put these on the board

**1. Save the WHOLE Pipeline, never just the model.**

```python
joblib.dump(search.best_estimator_.named_steps["model"], "bad.joblib")   # ❌ DISASTER
joblib.dump(search.best_estimator_,                     "good.joblib")   # ✅
```

*"Save only the `LogisticRegression` and you have thrown the scaler in the bin. Tomorrow, production sends raw, unscaled data. Does it crash? **No.** It happily returns confident, wrong predictions forever, with no error message. This is the worst kind of bug — a silent one."*

**2. Pin your versions.** A pipeline pickled under scikit-learn 1.3 may warn or fail under 1.6. Write a `requirements.txt` next to your `.joblib`, and record the version *inside* the artifact:

```python
import sklearn
artifact = {
    "pipeline":        search.best_estimator_,
    "sklearn_version": sklearn.__version__,
    "test_roc_auc":    0.99,        # your one honest test score
    "trained_on":      "2026-07-14",
    "feature_names":   list(X_train.columns),
}
joblib.dump(artifact, "cancer_artifact.joblib")
```

**3. Never load an untrusted `.joblib` or `.pkl`.** Unpickling **executes code**. A malicious file can run anything on your machine the moment you load it — it is exactly as dangerous as running a stranger's script. Only load files you or your team produced.

**4. Save the score with the model.** Six months later, "is this model still good?" is unanswerable unless you wrote down what "good" was on the day.

---

## Practical Block 3: The Capstone — End-to-End (15 min)

**This is the artifact of the whole module. Every student should end with a `.joblib` file on disk.**

```python
import joblib
import sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                             confusion_matrix, classification_report)

# ---- 1. LOAD -------------------------------------------------------------
X, y = load_breast_cancer(return_X_y=True, as_frame=True)

# ---- 2. SPLIT (test set locked away from here on) ------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---- 3. PIPELINE ---------------------------------------------------------
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=5000, random_state=42)),
])

# ---- 4. TUNE (training data only) ---------------------------------------
param_grid = {"model__C": [0.01, 0.1, 1, 10, 100]}
search = GridSearchCV(pipe, param_grid, cv=5, scoring="roc_auc", n_jobs=-1)
search.fit(X_train, y_train)
print("Best params :", search.best_params_)
print("Best CV AUC :", round(search.best_score_, 4))

best_pipeline = search.best_estimator_   # scaler + tuned model, refitted on all of X_train

# ---- 5. SCORE ONCE on the untouched test set ----------------------------
y_pred  = best_pipeline.predict(X_test)
y_proba = best_pipeline.predict_proba(X_test)[:, 1]

test_auc = roc_auc_score(y_test, y_proba)
print("\n--- HONEST TEST SCORES (first and only look) ---")
print("Accuracy :", round(accuracy_score(y_test, y_pred), 3))
print("F1       :", round(f1_score(y_test, y_pred), 3))
print("ROC-AUC  :", round(test_auc, 4))
print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
print("\n", classification_report(y_test, y_pred, digits=3))

# ---- 6. PERSIST the whole thing -----------------------------------------
artifact = {
    "pipeline":        best_pipeline,
    "best_params":     search.best_params_,
    "test_roc_auc":    round(test_auc, 4),
    "sklearn_version": sklearn.__version__,
    "feature_names":   list(X_train.columns),
}
joblib.dump(artifact, "cancer_artifact.joblib")
print("\nSaved -> cancer_artifact.joblib")
```

**Expected output:** test accuracy in the mid-to-high 0.9s, ROC-AUC around 0.99, a confusion matrix with only a handful of mistakes, and a file on disk.

**Live walk-through:** Number the six comment banners on the board as you go — **load, split, pipeline, tune, score once, persist.** Say plainly: *"This is the shape of every supervised ML project you will ever build. The only things that change are the dataset and which estimator sits in the `model` slot."*

Then ask: *"Why is `best_score_` not the same number as the test ROC-AUC? Which of the two would you put in an email to your manager?"* → `best_score_` is a cross-validated average on training folds, and it is the *winner of five attempts*, so it is mildly optimistic. The test score is the one honest number, because that data was never used for any decision. That is the number that goes in the email.

---

## Concept Block 4: Module Review and the Bridge to Module 3 (10 min)

### The whole module on one board

| Sessions | Theme | What you can now do |
|---|---|---|
| 1–2 | Workflow and honesty | Split, spot leakage, diagnose over/underfitting |
| 3–5 | Supervised: numbers | Linear, Ridge, Lasso; MAE, RMSE, R²; the maths of the fitted line |
| 6–8 | Supervised: categories | Logistic, KNN, tree, forest, boosting; precision, recall, F1, ROC-AUC, thresholds |
| 9–11 | Unsupervised and structure | K-Means, DBSCAN, probability, PCA, time series |
| 12 | Selection and shipping | Choose, tune, Pipeline, persist |

**The eight-step checklist — dictate it, make them write it:**

```
1. What is y?  Number / category / nothing.
2. Split FIRST. Lock the test set away.
3. Establish the dumb baseline. Beat it, or stop.
4. Simplest reasonable model, inside a Pipeline.
5. Cross-validate + GridSearchCV on the TRAINING set.
6. Score ONCE on the untouched test set.
7. Did complexity earn its place? If not, ship simple.
8. joblib.dump the whole Pipeline, with its score and versions.
```

### The bridge

*"Everything in Module 2 followed one pattern: you had YOUR data, and you FIT a small model to it. You owned the weights. In Module 3 the model arrives already trained — on more text than you could read in a thousand lifetimes — and you do not fit it. You **prompt** it."*

**Draw the two columns:**

```
CLASSICAL ML (Module 2)          GENAI & AGENTS (Module 3)
────────────────────────         ─────────────────────────
Your tabular data          →     Giant pre-trained model
You call .fit()            →     You write a prompt
Weights are yours          →     Weights are someone else's
Feature engineering        →     Context and retrieval
Fixed output: number/class →     Open output: text, code, actions
```

**But here is the part that matters — say it slowly:**

*"What carries over is everything that was hard to learn. Evaluate on held-out examples. Know your baseline. Garbage in, garbage out. Never let the answer leak into the input. Teams who skipped baselines in classical ML skip them with LLMs too — and they ship things that are confidently, fluently wrong. The discipline you built in this module is exactly what will make you good at the next one."*

---

## Practical Block 4: Reload the Artifact and Score a New Customer (10 min)

**Restart the kernel first.** This is the point of the exercise — prove that nothing is left in memory.

```python
# ===== FRESH SCRIPT — pretend this is a different machine, a week later =====
import joblib
import pandas as pd
from sklearn.datasets import load_breast_cancer

# No training. No fitting. No scaler. Just load.
artifact = joblib.load("cancer_artifact.joblib")
model    = artifact["pipeline"]

print("Loaded model trained with :", artifact["best_params"])
print("Its honest test ROC-AUC   :", artifact["test_roc_auc"])
print("Built on sklearn version  :", artifact["sklearn_version"])

# A "new patient" arriving today — RAW, unscaled values.
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
new_patient = X.iloc[[7]]         # keep the double brackets: predict needs a 2-D frame

prediction  = model.predict(new_patient)[0]
p_benign    = model.predict_proba(new_patient)[0, 1]

label = "benign" if prediction == 1 else "malignant"
print(f"\nPrediction        : {label}")
print(f"P(benign)         : {p_benign:.1%}")
print(f"True label was    : {'benign' if y.iloc[7] == 1 else 'malignant'}")
```

**Expected output:** the artifact's metadata prints, and the prediction comes back with a probability — and it matches the true label — with **no scaler in sight in this script**.

**Live walk-through:** This is the closing beat of the whole module. Point out that this script contains **zero** training code and **zero** preprocessing code — and yet the raw patient row got scaled correctly, because the scaler travelled inside the pipeline. Then ask the killer question:

> *"Delete the `StandardScaler` step from the saved artifact and rerun this. What happens?"*

→ It does **not** crash. It returns a confident, wrong answer. Silently. Forever. *"That is why we save the whole Pipeline. Not the model. The Pipeline."*

**Stretch (if time):** show `ColumnTransformer` for a mixed table:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
import pandas as pd

flats = pd.DataFrame({
    "area_sqft":  [650, 1200, 850, 1500, 700, 1100],
    "bedrooms":   [1, 3, 2, 3, 1, 2],
    "city":       ["Mumbai", "Delhi", "Bengaluru", "Mumbai", "Delhi", "Bengaluru"],
    "price_lakh": [95, 80, 70, 180, 62, 72],
})
num_cols, cat_cols = ["area_sqft", "bedrooms"], ["city"]

prep = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])
pipe = Pipeline([("prep", prep), ("model", Ridge(alpha=1.0))])
pipe.fit(flats[num_cols + cat_cols], flats["price_lakh"])
print(pipe.predict(flats[num_cols + cat_cols]).round(1))
```

*"Numeric columns get scaled, the city column gets one-hot encoded, and the model never sees the difference. Same `fit`, same `predict`, same `joblib.dump`."*

---

## Summary & Wrap-Up (5 min)

**The spine of today, in six lines:**

1. **Choose** deliberately — problem type, data size, need to explain. Simplest baseline first.
2. **Complexity must earn its place** — a 0.2% gain inside the noise band is not a gain.
3. **Tune** with `GridSearchCV` or `RandomizedSearchCV`, on the **training set only**. Tuning on test is cheating.
4. **`Pipeline`** makes leakage structurally impossible — the scaler refits inside every fold.
5. **`joblib.dump` the whole Pipeline**, with its versions and its one honest test score.
6. **The module in one line:** clean data → honest split → simple baseline → earn your complexity → measure once → ship it.

**And the closing frame:** *"You started Module 2 having never trained a model. You are ending it with a tuned, leak-proof, saved pipeline on disk — which is more than a lot of people with 'ML' in their job title have ever personally built."*

**Bridge:** *"Module 3 — **GenAI & Agents** — opens next. The model will already be trained, and your job shifts from fitting to prompting, retrieving, and evaluating. But the very first thing we will ask about any LLM output is the same thing we asked all module: **compared to what baseline, and measured on what held-out data?** Bring that question with you."*

---

## Q&A & Doubt Solving (5 min)

**Q: If `GridSearchCV` already cross-validates, why do I still need a test set?**
→ Because you *selected* on the cross-validation score. You ran five candidates and kept the best of five — the maximum of several noisy numbers is optimistically biased upward. The test set is the only data that participated in **zero** decisions, which is exactly what makes its score believable. `best_score_` is for choosing; the test score is for reporting.

**Q: `GridSearchCV` is taking forever. What do I actually do?**
→ Three levers, in order. First, `n_jobs=-1` to use all cores. Second, switch to `RandomizedSearchCV` with an `n_iter` you can afford — with many hyperparameters, random draws find near-optimal settings far faster than an exhaustive grid, because most hyperparameters barely matter. Third, shrink the grid: tune the two or three hyperparameters that actually move the score, not all nine.

**Q: Should I always use a Pipeline, even for a quick experiment?**
→ Yes, and this is not pedantry. The leakage demo scored 80% accuracy on pure noise, silently, with no error. There is no warning message for a leak — the only symptom is a score that is too good, which is precisely the symptom you are least motivated to investigate. Pipelines make the mistake unrepresentable.

**Q: Why `joblib` and not `pickle`? And is a `.joblib` file safe to email?**
→ `joblib` is more efficient with the large NumPy arrays inside fitted models, which is why scikit-learn recommends it. But it shares pickle's security model: **loading a file can execute arbitrary code**. Emailing one you built is fine. Loading one you downloaded from a stranger is exactly as safe as running a stranger's `.py` script — which is to say, not at all.

**Q: My model works perfectly today. Will the `.joblib` still work in a year?**
→ Only if the environment matches. A pipeline saved under scikit-learn 1.3 can warn or outright fail under a later version, because the internal object layouts change. Pin your versions in `requirements.txt`, store the version string inside the artifact, and — the deeper issue — remember the *world* also drifts. Prices, behaviour, and seasons change. A model is not a permanent truth; it is a snapshot of the data it saw, and it needs re-checking on fresh data.

---

## Instructor Notes

- **Installs:** nothing new. `joblib` ships with scikit-learn. `RandomizedSearchCV` with distributions uses `scipy.stats.randint`, and SciPy is already a scikit-learn dependency.
- **Pacing:** Practicals 3 and 4 are the point of the session — protect them. If you are running late, compress Concept 1 (they read the selection table in the pre-read) and shorten the bake-off to four candidates. Do **not** cut the leakage demo in Practical 2; it is the emotional core of the session.
- **File paths:** Practical 4 assumes `cancer_artifact.joblib` sits in the working directory that Practical 3 wrote to. If students use Colab, warn them the file lives in the ephemeral session storage and vanishes on disconnect — have them download it or mount Drive.
- **THE most common mistake:** the `param_grid` key. Students write `{"C": [...]}` instead of `{"model__C": [...]}` and get a baffling `Invalid parameter` error. Pre-empt it: write `model__C` on the board, circle the **two** underscores, and say the rule aloud — *"step name, two underscores, hyperparameter name."*
- **Second most common:** saving `named_steps["model"]` instead of the pipeline, then being confused when production predictions are garbage. Make them break it on purpose in Practical 4 — the silence of the failure is the lesson.
- **Emotional note:** this is the last session of Module 2. Leave two minutes at the end to name what they have built. Many of them arrived unable to train a single model; they are leaving with a shippable artifact. Say it out loud — they will not say it to themselves.
