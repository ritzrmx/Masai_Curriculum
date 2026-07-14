# Lecture Script: Model Selection, Persistence & Module Review
> **Instructor Reference** — Module 2: Classical ML | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can compare multiple trained models on the same data using a metrics table, choose a "best" model using criteria beyond raw accuracy, save and reload that model reliably with `joblib`, and articulate the full Module 2 workflow end-to-end — plus recognize where classical ML's limitations open the door to Module 3.

**Student profile at this point:** Have completed all 11 prior sessions of Module 2 — the ML workflow, regression + regularization, regression evaluation, a probability masterclass, classification foundations, ensembles, classification metrics, clustering, and PCA/time series. Comfortable with `train_test_split`, `StandardScaler`, and fitting/evaluating a single sklearn model. Today is the first time they compare several models side by side and ship one.

**Key outcome:** By the end of class, every student has: (1) a reusable model-comparison snippet, (2) a working save/load pattern with `joblib` that includes the scaler, and (3) a one-page mental map of every model type in Module 2 — what it's for, its key knob, its strength, its weakness.

**Tone for this session:** The first ~100 minutes are hands-on and practical — this is the "how do I actually ship something" session. The last 20 minutes shift to reflective module review, similar in spirit to a capstone debrief.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Why "Best Model" Isn't Just Highest Accuracy | 10 min | 0:15 |
| **Practical 1:** Compare 3 Classifiers on One Dataset | 15 min | 0:30 |
| **Concept 2:** Interpretability, Cost & Latency — The Other Axes | 10 min | 0:40 |
| **Practical 2:** Compare Training Time & Interpretability | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Model Persistence — Save It Right, or Don't Save It | 10 min | 1:15 |
| **Practical 3:** `joblib.dump` / `joblib.load` + the Scaler Pitfall | 15 min | 1:30 |
| **Concept 4:** Module 2 Review — Every Model, One Table + ML's Limits | 10 min | 1:40 |
| **Practical 4:** Full Pipeline Recap — Load → Persist, End-to-End | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Ask the class: *"You've now trained Logistic Regression, Decision Trees, Random Forests, K-Means, and PCA. Suppose your manager says: 'Ship the best model to production by Friday.' What do you do — literally, step by step?"*

Let 2-3 students answer. Almost everyone will say some version of "train a few models, pick the one with the highest accuracy." Push back gently: *"What if the highest-accuracy model takes 40 minutes to retrain every week, and nobody on your team can explain why it makes a decision, and it's 0.3% more accurate than the simple one? Do you still ship it?"*

**Context to set:** Every session so far has ended with "here's how good the model is." Today we answer three questions those sessions skipped: How do I compare models *fairly*? What matters besides the metric? And once I've picked one — how do I actually save it so it survives past my notebook session? Then we zoom out and review the whole module, because next session, we leave classical ML behind entirely and enter GenAI.

**Learning contract for today:**
- Compare multiple models on identical data using a shared metrics table
- Justify a model choice using more than one criterion
- Save and reload a model (and its preprocessing) without breaking it
- Walk out with a one-page summary of every Module 2 model type

---

## Concept Block 1: Why "Best Model" Isn't Just Highest Accuracy (10 min)

### The Fair Comparison Rule

**Teaching point:** You can only compare models if everything *except the model* is held constant — same train/test split, same random state, same preprocessing. Comparing Model A on one split and Model B on another is not a comparison; it's noise.

```
Fair comparison checklist:
✓ Same train_test_split() call (same random_state)
✓ Same features (same X columns, same scaling applied consistently)
✓ Same evaluation metric(s), computed on the same test set
✓ Same random_state inside each model where applicable
```

### Recap: Which Metric, Again? (bridge to Session 8)

| Situation | Prefer | Why |
|---|---|---|
| Balanced classes, all errors equally costly | Accuracy | Simple, interpretable |
| Imbalanced classes (fraud, disease) | F1 / Recall | Accuracy is misleadingly high on the majority class |
| Need to compare models across thresholds | ROC-AUC | Threshold-independent; measures ranking quality |
| Business cares more about false positives OR false negatives specifically | Precision or Recall individually | F1 blends both — sometimes you need just one |

**Key teaching point:** "Best model" is never a single number in isolation — it's the best model *for this metric, on this data, under these constraints*. A model that's best for fraud detection (high recall) might be the worst choice for a spam filter (which needs high precision, or users lose real email).

**Discussion prompt:** *"If two models have identical accuracy but different F1 scores, which one do you trust more, and why?"*

---

## Practical Block 1: Compare 3 Classifiers on One Dataset (15 min)

### Dataset: Breast Cancer Wisconsin (built into sklearn)

```python
import pandas as pd
import numpy as np
import time
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name="target")

print("Shape:", X.shape)
print("Classes:", dict(zip(*np.unique(y, return_counts=True))))
print("Target names:", list(data.target_names))
```

**Output:**
```
Shape: (569, 30)
Classes: {0: 212, 1: 357}
Target names: ['malignant', 'benign']
```

```python
# ONE split, reused for every model — this is the fair-comparison rule in action
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Train shape:", X_train.shape, "Test shape:", X_test.shape)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Output:**
```
Train shape: (455, 30) Test shape: (114, 30)
```

```python
models = {
    "LogisticRegression": LogisticRegression(max_iter=5000, random_state=42),
    "DecisionTree": DecisionTreeClassifier(max_depth=4, random_state=42),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
}

results = []
for name, model in models.items():
    # Logistic Regression is distance-based -> needs scaled features.
    # Trees split on raw thresholds -> scaling doesn't matter for them.
    uses_scaled = name == "LogisticRegression"
    Xtr = X_train_scaled if uses_scaled else X_train
    Xte = X_test_scaled if uses_scaled else X_test

    start = time.perf_counter()
    model.fit(Xtr, y_train)
    train_time = time.perf_counter() - start

    preds = model.predict(Xte)
    proba = model.predict_proba(Xte)[:, 1]

    results.append({
        "Model": name,
        "Accuracy": round(accuracy_score(y_test, preds), 4),
        "F1": round(f1_score(y_test, preds), 4),
        "ROC-AUC": round(roc_auc_score(y_test, proba), 4),
        "Train Time (s)": round(train_time, 4),
    })

results_df = pd.DataFrame(results).set_index("Model")
print(results_df)
```

**Output:**
```
                    Accuracy      F1  ROC-AUC  Train Time (s)
Model
LogisticRegression    0.9825  0.9861   0.9954          0.0023
DecisionTree          0.9386  0.9510   0.9342          0.0034
RandomForest          0.9561  0.9655   0.9931          0.1572
```

**Walk through the table live.** Ask: *"Purely by the metrics — which model would you ship?"* Most will say Logistic Regression (it wins on all three metrics here). **Note for instructors:** exact numbers will vary slightly by sklearn/OS/BLAS version — the *relative ordering* and the teaching point are what matter, not the fourth decimal place.

**Teaching point:** This is a rare case where the simplest model wins outright. That won't always happen — flag it now so students don't walk away thinking "logistic regression always wins." On messier, more nonlinear data, Random Forest usually pulls ahead.

---

## Concept Block 2: Interpretability, Cost & Latency — The Other Axes (10 min)

### Four Questions Beyond the Metric

```
1. INTERPRETABILITY — Can a human explain why the model made this decision?
2. TRAINING COST     — How long / how much compute to retrain from scratch?
3. INFERENCE LATENCY — How fast is one prediction, at request time, in production?
4. MAINTENANCE       — How much monitoring/retraining does it need as data drifts?
```

| Model | Interpretability | Training Cost | Inference Latency | Typical Use Case Fit |
|---|---|---|---|---|
| Logistic Regression | High — coefficients are directly readable | Very low | Very low | Regulated domains (credit, healthcare) where "why" matters |
| Decision Tree (shallow) | High — can draw the whole tree | Low | Very low | Rules that need to be explained to non-technical stakeholders |
| Random Forest | Low — 100s of trees averaged | Higher | Higher (must query every tree) | Best raw performance when explainability isn't a hard requirement |

**Teaching point:** In healthcare, finance, and hiring, regulators or auditors may legally require you to explain *why* a model rejected someone. A 0.5% accuracy gain from a Random Forest is not worth losing the ability to answer "why was this loan denied?" in one sentence.

**Real-world framing:** *"A fraud model that takes 200ms to score one transaction is useless if the payment gateway times out at 100ms. Latency isn't a footnote — it's a hard constraint."*

---

## Practical Block 2: Compare Training Time & Interpretability (15 min)

```python
# Same three fitted models from Practical 1 (log_reg / tree / rf)
log_reg = LogisticRegression(max_iter=5000, random_state=42)
log_reg.fit(X_train_scaled, y_train)

tree = DecisionTreeClassifier(max_depth=4, random_state=42)
tree.fit(X_train, y_train)

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# How many numbers does a human need to read to fully explain each model?
n_coefs = log_reg.coef_.size + 1          # weights + intercept
n_tree_nodes = tree.tree_.node_count
n_rf_trees = rf.n_estimators

print("LogisticRegression:", n_coefs, "numbers total (one readable equation)")
print("DecisionTree (max_depth=4):", n_tree_nodes, "nodes (fits on one diagram)")
print("RandomForest (200 trees):", n_rf_trees, "separate trees averaged (not human-readable directly)")
```

**Output:**
```
LogisticRegression: 31 numbers total (one readable equation)
DecisionTree (max_depth=4): 21 nodes (fits on one diagram)
RandomForest (200 trees): 200 separate trees averaged (not human-readable directly)
```

```python
# Top-5 most influential features -- each model computes "importance" differently
coef_importance = pd.Series(np.abs(log_reg.coef_[0]), index=X.columns).sort_values(ascending=False).head(5)
tree_importance = pd.Series(tree.feature_importances_, index=X.columns).sort_values(ascending=False).head(5)
rf_importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).head(5)

print("Top 5 -- LogisticRegression (|coefficient|, scaled data):")
print(coef_importance.round(3))
print("\nTop 5 -- DecisionTree (impurity-based importance):")
print(tree_importance.round(3))
print("\nTop 5 -- RandomForest (impurity-based importance):")
print(rf_importance.round(3))
```

**Output:**
```
Top 5 -- LogisticRegression (|coefficient|, scaled data):
worst texture           1.255
radius error            1.083
worst concave points    0.954
worst area               0.948
worst radius             0.948
dtype: float64

Top 5 -- DecisionTree (impurity-based importance):
worst radius             0.734
worst concave points     0.122
texture error            0.046
worst texture            0.032
worst concavity          0.017
dtype: float64

Top 5 -- RandomForest (impurity-based importance):
worst perimeter          0.133
worst area               0.128
worst concave points     0.108
mean concave points      0.094
worst radius             0.091
dtype: float64
```

**Discussion prompt:** *"Notice the three models don't agree on the #1 most important feature. Why might that be — and if a doctor asked you 'what actually drives this prediction,' which answer would you trust?"* (Guide toward: no single "importance" is ground truth — each is a different lens on the same data, and disagreement across models is itself useful information.)

---

## BREAK (10 min)

*Suggested break prompt: ask students to think of one product they use daily (maps app, food delivery, email spam filter) and guess which model family it's likely using and why — accuracy vs. speed vs. explainability trade-offs.*

---

## Concept Block 3: Model Persistence — Save It Right, or Don't Save It (10 min)

### Why Persistence Matters

**Teaching point:** A trained model living only inside a Jupyter kernel is worthless the moment that kernel restarts. Persistence turns a training run into a reusable artifact — something a web app, an API, or a teammate can load without retraining.

```
Training (expensive, done once)  →  model.fit(X_train, y_train)
Persistence (do this once)       →  joblib.dump(model, "model.joblib")
Serving (cheap, done many times) →  joblib.load("model.joblib").predict(new_row)
```

### `joblib` vs `pickle`

| | `pickle` | `joblib` |
|---|---|---|
| General Python objects | Yes | Yes |
| Large NumPy arrays (model weights, tree structures) | Slower, larger files | Optimized, faster, smaller files |
| Standard for sklearn models | Works, but not preferred | **Recommended by sklearn docs** |

**The #1 persistence mistake:** Saving only the model and forgetting the `StandardScaler` (or `OneHotEncoder`, or any other preprocessing step) fit on the training data. At inference time, if you scale new data with a *freshly fit* scaler instead of the *saved* one, the numbers fed to the model are on a completely different scale than what it was trained on — predictions silently become garbage. No error is raised. This is one of the most common production ML bugs.

**Versioning pitfalls to flag:**
- sklearn model files are **not guaranteed compatible** across major version changes — a model saved with sklearn 1.3 may fail (or worse, silently mispredict) when loaded with sklearn 2.0. Always record the sklearn version alongside the artifact.
- Never save a model without also saving: the feature column order, the preprocessing objects, and ideally the library versions used to train it.
- Retraining isn't optional forever — real-world data drifts. A model frozen in 2024 slowly degrades as the world changes; persistence is not "save once, use forever."

---

## Practical Block 3: `joblib.dump` / `joblib.load` + the Scaler Pitfall (15 min)

```python
import joblib
import sklearn

# Re-use the winning model from Practical 1: LogisticRegression
winner = LogisticRegression(max_iter=5000, random_state=42)
winner.fit(X_train_scaled, y_train)

preds_before = winner.predict(X_test_scaled)
print("Predictions before saving (first 10):", preds_before[:10])

# Persist BOTH the model and the scaler -- this is the pitfall students miss
joblib.dump(winner, "/tmp/scratch_model.joblib")
joblib.dump(scaler, "/tmp/scratch_scaler.joblib")
print("\nsklearn version at save time:", sklearn.__version__)
print("Saved model + scaler to disk.")
```

**Output:**
```
Predictions before saving (first 10): [0 1 0 1 0 1 1 0 0 0]

sklearn version at save time: 1.8.0
Saved model + scaler to disk.
```

```python
# --- Simulate a fresh session: reload from disk, as if this were a new process ---
loaded_model = joblib.load("/tmp/scratch_model.joblib")
loaded_scaler = joblib.load("/tmp/scratch_scaler.joblib")

X_test_scaled_reloaded = loaded_scaler.transform(X_test)   # re-scale with the SAVED scaler
preds_after = loaded_model.predict(X_test_scaled_reloaded)

print("Predictions after loading  (first 10):", preds_after[:10])
print("Identical predictions:", np.array_equal(preds_before, preds_after))
```

**Output:**
```
Predictions after loading  (first 10): [0 1 0 1 0 1 1 0 0 0]
Identical predictions: True
```

```python
# Now demonstrate the bug: forget the saved scaler, feed raw (unscaled) data straight to the model
preds_wrong = loaded_model.predict(X_test)   # BUG: raw, unscaled features!
agreement = (preds_wrong == preds_before).mean()
print(f"If we skip the saved scaler (bug): agreement with correct predictions = {agreement:.2%}")
```

**Output:**
```
If we skip the saved scaler (bug): agreement with correct predictions = 36.84%
```

**Run this live and let it land.** The model doesn't crash. It doesn't warn loudly by default in most setups. It just quietly gets 63% of predictions *wrong* compared to the correctly-scaled version. This is exactly the kind of bug that ships to production undetected because "the code runs fine."

**Ask the class:** *"Whose fault is this bug — the model's, or the pipeline's?"* → Neither is "wrong" in isolation; the model faithfully does what it was trained to do on a distribution it was never shown. The lesson: **persist the whole pipeline, not just the model.**

**Extension for faster students:**
```python
# Cleaner pattern: wrap scaler + model into a single sklearn Pipeline,
# then there is only ONE object to save and load -- no chance of mismatch.
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=5000, random_state=42)),
])
pipe.fit(X_train, y_train)          # fits scaler AND model together
joblib.dump(pipe, "/tmp/scratch_pipeline.joblib")
# One load call now reconstructs the entire pipeline correctly, every time.
```

---

## Concept Block 4: Module 2 Review — Every Model, One Table + ML's Limits (10 min)

### The Complete Module 2 Model Comparison Table

**Teaching point:** Put this on the board / screen and walk through each row out loud — this is the "cheat sheet" students should photograph before leaving.

| Model | Type | Typical Use Case | Key Hyperparameter | Main Strength | Main Weakness |
|---|---|---|---|---|---|
| Linear Regression | Supervised (regression) | Predicting a continuous number (price, revenue) with a roughly linear relationship | None core (baseline) | Simple, fast, fully interpretable coefficients | Assumes linearity; sensitive to outliers |
| Ridge Regression | Supervised (regression) | Same as above, but with many/correlated features | `alpha` (L2 penalty strength) | Reduces overfitting, stabilizes coefficients | Doesn't zero out useless features |
| Lasso Regression | Supervised (regression) | Feature selection + regression together | `alpha` (L1 penalty strength) | Shrinks weak features to exactly 0 | Can be unstable with correlated features |
| Logistic Regression | Supervised (classification) | Binary/multiclass classification, especially where "why" matters | `C` (inverse regularization strength) | Highly interpretable, fast, strong baseline | Struggles with non-linear decision boundaries |
| Decision Tree | Supervised (classification/regression) | Rule-based decisions that need to be explained | `max_depth` | Fully interpretable; no scaling needed | Prone to overfitting if too deep |
| Random Forest | Supervised (classification/regression) | Best general-purpose accuracy on tabular data | `n_estimators` | High accuracy, robust to overfitting, handles non-linearity | Slower, low interpretability |
| K-Means Clustering | Unsupervised | Segmenting customers/items into groups with no labels | `n_clusters` (k) | Fast, simple, scales well | Must choose k in advance; assumes round/equal-size clusters |
| Hierarchical Clustering | Unsupervised | Exploring nested/nested-subgroup structure, small-to-medium data | `linkage` method | No need to pre-choose k; dendrogram shows structure at every level | Computationally expensive at scale |
| PCA | Unsupervised (dimensionality reduction) | Compressing many correlated features into a few components before modeling/plotting | `n_components` | Removes redundancy, speeds up downstream models, enables visualization | Components lose direct real-world meaning |

### The Full Module 2 Workflow, One More Time

```
Raw Data
   │
   ▼
CLEAN / SPLIT / SCALE   (Session 1, Session 8 callback)
   │
   ▼
TRAIN                    (fit on training data only)
   │
   ▼
EVALUATE                 (Session 4, Session 9 metrics — on TEST data only)
   │
   ▼
TUNE                     (GridSearchCV / hyperparameters — Session 2)
   │
   ▼
SELECT                   (metric + interpretability + cost + latency — TODAY)
   │
   ▼
PERSIST                  (joblib.dump — model + preprocessing — TODAY)
```

### ML's Limitations — Why This Isn't the Whole Story

Even a perfectly tuned, perfectly evaluated classical ML model has hard boundaries:

- **Needs quality labeled data** — a model is only as good as the examples it was shown; garbage in, garbage out (Session 1 callback).
- **Correlation ≠ causation** — a model can find that ice cream sales predict drowning rates without understanding either causes the other (Session 10 callback).
- **Cannot reason or generalize outside its training distribution** — ask a model trained on Indian housing prices to predict prices in a country it has never seen data from, and it will confidently produce a number anyway, with no idea it's out of its depth.
- **Bias amplification** — if the training data reflects historical bias, the model doesn't just repeat it, it can systematically amplify it at scale.
- **No common sense or world knowledge** — a Decision Tree doesn't "know" what a hospital is; it only knows numeric thresholds on the columns it was given.
- **Requires retraining as data drifts** — a model is a frozen snapshot; the real world keeps moving, so accuracy silently decays over time (concept drift).
- **One task per model** — a spam classifier cannot suddenly answer a question or summarize a document; every new task traditionally means training a brand new model from scratch.

**Bridge to Module 3:** *"That last point is exactly where classical ML hits its ceiling — one model, one narrow task, retrained from scratch every time the task changes. Module 3 introduces a fundamentally different paradigm: models trained once on massive, general data that can be *prompted* into thousands of different tasks without retraining. That's Generative AI — and that's where we go next."*

---

## Practical Block 4: Full Pipeline Recap — Load → Persist, End-to-End (10 min)

**Give students a fresh dataset and have them run the complete workflow live, narrating each step out loud.**

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score

# STEP 1: LOAD
data = load_wine()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name="target")
print("STEP 1 - LOAD: shape =", X.shape, "| classes =", list(data.target_names))

# STEP 2: CLEAN / SPLIT / SCALE
print("\nSTEP 2 - CLEAN: nulls =", X.isnull().sum().sum(), "| duplicates =", X.duplicated().sum())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("STEP 2 - SPLIT/SCALE: train =", X_train.shape, "test =", X_test.shape)
```

**Output:**
```
STEP 1 - LOAD: shape = (178, 13) | classes = ['class_0', 'class_1', 'class_2']

STEP 2 - CLEAN: nulls = 0 | duplicates = 0
STEP 2 - SPLIT/SCALE: train = (142, 13) test = (36, 13)
```

```python
# STEP 3: TRAIN (baseline)
baseline = RandomForestClassifier(random_state=42)
baseline.fit(X_train_scaled, y_train)
baseline_preds = baseline.predict(X_test_scaled)
print("STEP 3 - TRAIN (baseline RandomForest, default params):")
print("  Accuracy:", round(accuracy_score(y_test, baseline_preds), 4))
print("  F1 (macro):", round(f1_score(y_test, baseline_preds, average="macro"), 4))

# STEP 4: TUNE
param_grid = {"n_estimators": [50, 150], "max_depth": [3, 6, None]}
grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring="f1_macro")
grid.fit(X_train_scaled, y_train)
print("\nSTEP 4 - TUNE (GridSearchCV, 5-fold):")
print("  Best params:", grid.best_params_)
print("  Best CV F1 (macro):", round(grid.best_score_, 4))

# STEP 5: SELECT + EVALUATE final model on held-out test set
best_model = grid.best_estimator_
final_preds = best_model.predict(X_test_scaled)
print("\nSTEP 5 - SELECT/EVALUATE: tuned model on test set")
print("  Accuracy:", round(accuracy_score(y_test, final_preds), 4))
print("  F1 (macro):", round(f1_score(y_test, final_preds, average="macro"), 4))

# STEP 6: PERSIST
joblib.dump(best_model, "/tmp/wine_model.joblib")
joblib.dump(scaler, "/tmp/wine_scaler.joblib")
print("\nSTEP 6 - PERSIST: saved tuned model + scaler to disk (2 files)")
```

**Output:**
```
STEP 3 - TRAIN (baseline RandomForest, default params):
  Accuracy: 1.0
  F1 (macro): 1.0

STEP 4 - TUNE (GridSearchCV, 5-fold):
  Best params: {'max_depth': 3, 'n_estimators': 50}
  Best CV F1 (macro): 0.9863

STEP 5 - SELECT/EVALUATE: tuned model on test set
  Accuracy: 1.0
  F1 (macro): 1.0

STEP 6 - PERSIST: saved tuned model + scaler to disk (2 files)
```

**Teaching point:** Wine is a small, clean, well-separated dataset — that's *why* the baseline already hits a perfect test score and tuning doesn't move it further. Say this explicitly: *"Don't conclude that tuning is pointless. On messier, larger, real-world data the gap between baseline and tuned is usually much bigger. The takeaway today is the workflow shape, not this particular score."* The 5-fold CV score (0.9863) is actually the more honest number to trust — it's estimated across many splits, not just the one lucky test split.

```python
# Confirm the persisted pipeline is trustworthy
reloaded = joblib.load("/tmp/wine_model.joblib")
reloaded_scaler = joblib.load("/tmp/wine_scaler.joblib")
reloaded_preds = reloaded.predict(reloaded_scaler.transform(X_test))
print("Reloaded model predictions match original:", np.array_equal(reloaded_preds, final_preds))
```

**Output:**
```
Reloaded model predictions match original: True
```

**Close the loop:** *"That's the entire Module 2 arc in eleven lines: load, clean, split, scale, train, tune, evaluate, select, persist, reload, confirm. Every session for the last six weeks fed into one of these steps."*

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Fair model comparison requires holding the split, features, and scaling constant across all models
- "Best" is multi-dimensional: metric performance + interpretability + training cost + inference latency
- `joblib.dump` / `joblib.load` persist a model; **always persist the scaler (or the whole Pipeline) alongside it**
- Forgetting to save/apply preprocessing at inference time fails silently — it doesn't crash, it just quietly produces wrong predictions
- The full Module 2 model line-up: Linear/Ridge/Lasso Regression, Logistic Regression, Decision Tree, Random Forest, K-Means, Hierarchical Clustering, PCA
- Classical ML's hard limits: data-hungry, correlation ≠ causation, no generalization outside training distribution, bias amplification, drift, one-model-one-task

**Bridge to next session:** *"Module 2 is complete. You can now take raw tabular data all the way to a saved, reloadable model. Module 3 — GenAI & Agents — starts fresh with a different kind of model entirely: Large Language Models that are trained once and then *prompted* into new tasks without retraining. Session 1 is GenAI Foundations & Prompt Engineering — bring your curiosity, not your scaler."*

**Homework / self-practice:** Pick any classification dataset from `sklearn.datasets` you haven't used yet (`load_digits` or `load_iris` both work well). Run the full 6-step pipeline from Practical 4 on it, compare at least two model types, and save the winner with `joblib`. Write one sentence justifying your choice beyond "it had higher accuracy."

---

## Q&A & Doubt Solving (5 min)

**Q: If Random Forest usually performs best, why would I ever ship Logistic Regression?**
→ "Best" on a metrics table is not the same as "best for this deployment." If you need to explain individual decisions (loan denials, medical flags) or need sub-millisecond latency at massive scale, the small accuracy gain from Random Forest often isn't worth the interpretability or speed cost.

**Q: Do I need to save the scaler even if my model is a Decision Tree, which doesn't need scaling?**
→ No — trees split on raw feature thresholds, so scaling doesn't change their predictions. But if your pipeline scales features for *any* other reason (e.g., you reuse the same preprocessing for multiple models), save it anyway for consistency. When in doubt, use a single `Pipeline` object so you never have to reason about it manually.

**Q: What's the difference between `pickle` and `joblib` in practice — do I need to worry about it?**
→ For plain Python objects they're interchangeable. For sklearn models specifically, `joblib` is recommended because it handles large NumPy arrays (weights, tree splits) more efficiently — smaller files, faster save/load. Default to `joblib` for anything sklearn.

**Q: My saved model works today. Will it still work in a year?**
→ Not guaranteed. Major sklearn version upgrades can break compatibility with old saved models. Best practice: pin your sklearn version in requirements, record it alongside the saved model file, and re-save (retrain if needed) after major upgrades rather than assuming old files will "just work."

**Q: Is a Random Forest with 200 trees really impossible to interpret?**
→ Not impossible, but harder. Tools like SHAP or permutation importance can approximate "why" for ensemble models — that's a topic for further self-study, but know that the trade-off is real, not absolute. It's "much harder to fully explain," not "impossible to gain any insight into."

**Q: Why did GridSearchCV pick fewer trees (`n_estimators=50`) as "best" here — isn't more always better?**
→ Not necessarily, and this is a good catch. More trees generally help until returns flatten, but with cross-validation scoring, a smaller forest that generalizes equally well can tie or edge out a larger one on a small, easy dataset like this. On harder data you'd typically see more estimators win.

---

## Instructor Notes

- **Dataset choices:** `load_breast_cancer` (binary, 30 features) drives Practicals 1-3; `load_wine` (3-class, 13 features) drives Practical 4 so students see the pipeline applied to a fresh dataset, not a repeat. Both are built into sklearn — zero internet dependency, fully reproducible with `random_state=42`.
- **Numbers will drift slightly:** Exact accuracy/F1/timing values can shift by a thousandth of a point across sklearn versions, OS, or CPU. Tell students up front: match the *shape* of the output and the *ordering* of models, not the literal decimal digits.
- **Common mistake to watch for:** Students scaling `X_test` with `scaler.fit_transform()` instead of `scaler.transform()` — this silently re-fits a new scaler on test data (data leakage) instead of reusing the training scaler. Catch this live if you see it; it's one of the most common and hardest-to-notice bugs in the whole module.
- **Live-coding tip:** For the persistence "bug" demo (Practical 3), narrate it as a detective story — "the code ran with no errors, the shapes matched, everything *looked* fine... so why are 63% of predictions wrong?" Let students sit with the discomfort for a moment before revealing the missing scaler.
- **For advanced students:** Show the `Pipeline` extension in Practical 3 as the "professional" pattern, and mention `mlflow` or a model registry conceptually (no need to install) as what real teams use to track which model version is in production.
- **Time-check contingency:** If running behind after the break, compress Practical 4 to a walkthrough (instructor runs it, students follow along) rather than live independent coding — the review content in Concept 4 must not be cut, since the comparison table and ML-limitations list are the main takeaway artifacts of the entire module.
- **Closing the module:** This is the last classical ML session. Consider a 1-minute show-of-hands: "Which Module 2 model type do you feel most confident explaining to a non-technical friend?" It's a light, low-stakes way to surface any lingering confusion before Module 3 begins.
