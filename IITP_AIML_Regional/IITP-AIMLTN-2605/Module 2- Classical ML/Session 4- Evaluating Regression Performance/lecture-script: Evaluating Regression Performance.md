# Lecture Script: Evaluating Regression Performance
> **Instructor Reference** — Module 2: Classical ML | Session 4 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can compute, interpret, and choose between MAE, RMSE, and R² for a regression model — and use residual analysis to diagnose *why* a model is wrong, not just *how* wrong it is.

**Student profile at this point:** Have fit Linear Regression, Ridge, and Lasso in the previous session. Have called `.score()` and treated the number as "good enough" without knowing what it means, what its blind spots are, or what else exists.

**Key outcome:** By end of class, every student can look at a set of predictions, compute all three core metrics by hand and with `sklearn.metrics`, read a residual plot to spot underfitting, and defend a model choice using more than one number.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Why `.score()` Alone Isn't Enough | 10 min | 0:15 |
| **Practical 1:** MAE, MSE, RMSE — By Hand, Then `sklearn` | 15 min | 0:30 |
| **Concept 2:** R² — What It Really Measures | 10 min | 0:40 |
| **Practical 2:** Comparing Models on the Diabetes Dataset | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Residual Analysis — Reading the Shape of Error | 10 min | 1:15 |
| **Practical 3:** Plotting Residuals — Good Fit vs Bad Fit | 15 min | 1:30 |
| **Concept 4:** Identifying Where a Model Fails | 10 min | 1:40 |
| **Practical 4:** Error Audit — Best, Worst, and Biased Predictions | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Write two numbers on the board:

```
Model X: R² = 0.85
Model Y: R² = 0.85
```

Ask the class: *"Same R². Are these two models equally good?"* Most will say yes. Then reveal: Model X is off by ₹2 lakh on average across all houses. Model Y is nearly perfect on 95% of houses but catastrophically wrong (off by ₹50 lakh) on the remaining 5% — maybe exactly the luxury properties a real estate business cares most about. **Same R², completely different risk profile.**

**Context to set:** Last session you learned to *build* regression models — OLS, Ridge, Lasso. You called `.score()` and moved on. But `.score()` returns exactly one number (R²), and one number can never tell you the full story of how a model fails. Today you learn the vocabulary and tools to evaluate a regression model properly — the same vocabulary you'll see in every ML job posting, Kaggle leaderboard, and production monitoring dashboard.

**Learning contract for today:**
- Compute MAE, MSE, RMSE, and R² — by hand once, then with `sklearn.metrics`
- Know when each metric misleads you, and why you almost always report more than one
- Read a residual plot to catch problems R² hides
- Use error analysis to say *which* predictions are bad, not just *how many*

---

## Concept Block 1: Why `.score()` Alone Isn't Enough (10 min)

### The Problem With a Single Number

`.score()` on a fitted regressor returns R² — a number between (mostly) 0 and 1 describing how much variance in the target the model explains. It is useful, but it hides three things:

1. **Units.** R² = 0.85 tells you nothing about whether your predictions are off by ₹500 or ₹5,00,000. It is unitless.
2. **Error distribution.** R² is a single average-like summary. It cannot tell you if errors are spread evenly or concentrated in a few disastrous predictions.
3. **Direction and pattern.** R² cannot tell you if the model systematically over-predicts for one segment of the data and under-predicts for another.

**Teaching point:** Evaluation is not "run one function, read one number." It is a small toolkit — MAE, RMSE, R², and residual plots — where each tool answers a different question. Today's session builds that toolkit.

### The Metric Family Tree

```
Regression Evaluation
├── Error-magnitude metrics (same unit as target)
│   ├── MAE  — average absolute error
│   └── RMSE — root of average squared error (penalizes big misses)
├── Goodness-of-fit metric (unitless, 0-1 scale, comparable across problems)
│   └── R²   — variance explained
└── Diagnostic tools (visual / row-level)
    ├── Residual plots — is the error random or patterned?
    └── Error audit — which specific rows are worst, and why?
```

### MAE vs RMSE — the Core Trade-off

| Metric | Formula | Penalizes large errors? | Best used when |
|---|---|---|---|
| MAE | mean(\|actual − predicted\|) | No — linear penalty | You want an interpretable "typical miss," and outliers shouldn't dominate |
| RMSE | sqrt(mean((actual − predicted)²)) | Yes — squares amplify large errors | Large errors are especially costly (e.g., predicting hospital stay length) |
| R² | 1 − SS_res / SS_tot | N/A (relative measure) | You want a scale-free "how much better than guessing the mean" score |

**Teaching point:** RMSE is always ≥ MAE for the same predictions. If RMSE is much larger than MAE, that gap itself is a signal — it means a few predictions are *very* wrong, dragging RMSE up while MAE stays moderate. Students should learn to read the *gap* between the two, not just each number alone.

---

## Practical Block 1: MAE, MSE, RMSE — By Hand, Then `sklearn` (15 min)

### Step 1 — Compute by hand on a tiny toy example

Use a 5-house toy dataset so every number is checkable on paper.

```python
import numpy as np

# Toy example: predicting house price (in lakhs INR) for 5 houses
actual    = np.array([50, 60, 70, 80, 90])
predicted = np.array([48, 65, 68, 85, 95])

errors = actual - predicted
abs_errors = np.abs(errors)
sq_errors = errors ** 2

print("Actual:   ", actual)
print("Predicted:", predicted)
print("Error (actual - predicted):", errors)
print("Abs Error:", abs_errors)
print("Squared Error:", sq_errors)
```

**Output:**
```
Actual:    [50 60 70 80 90]
Predicted: [48 65 68 85 95]
Error (actual - predicted): [ 2 -5  2 -5 -5]
Abs Error: [2 5 2 5 5]
Squared Error: [ 4 25  4 25 25]
```

**Walk through it on the board.** Sum the abs errors (19), divide by 5 → MAE. Sum the squared errors (83), divide by 5 → MSE. Square-root that → RMSE.

```python
mae_manual = abs_errors.mean()
mse_manual = sq_errors.mean()
rmse_manual = np.sqrt(mse_manual)

print("\nMAE (manual):", mae_manual)
print("MSE (manual):", mse_manual)
print("RMSE (manual):", rmse_manual)
```

**Output:**
```
MAE (manual): 3.8
MSE (manual): 16.6
RMSE (manual): 4.0743097574926725
```

**Discussion prompt:** *"MAE is 3.8, RMSE is 4.07 — close together. What would it take to make RMSE much bigger than MAE without changing MAE?"* → Answer: concentrate the same total error into fewer, larger misses (e.g., one house off by 15, the rest off by 1). Squaring punishes concentration.

### Step 2 — Compute R² by hand

```python
mean_actual = actual.mean()
ss_res = np.sum((actual - predicted) ** 2)   # error the model makes
ss_tot = np.sum((actual - mean_actual) ** 2)  # error a "predict-the-mean" baseline makes
r2_manual = 1 - (ss_res / ss_tot)

print("Mean of actual:", mean_actual)
print("SS_res:", ss_res)
print("SS_tot:", ss_tot)
print("R2 (manual):", r2_manual)
```

**Output:**
```
Mean of actual: 70.0
SS_res: 83
SS_tot: 1000.0
R2 (manual): 0.917
```

**Teaching point:** R² compares your model's total squared error (SS_res) against the total squared error of the dumbest possible baseline — always predicting the mean (SS_tot). R² = 0.917 means the model explains 91.7% of the variance the mean-baseline couldn't. **R² = 1 − (your model's error / a baseline that guesses the average).**

### Step 3 — Confirm with `sklearn.metrics`

Check the installed version first — the RMSE API changed across sklearn releases (`sklearn.__version__` is `1.8.0` here, so `root_mean_squared_error` is available directly).

```python
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error,
    root_mean_squared_error, r2_score
)

mae = mean_absolute_error(actual, predicted)
mse = mean_squared_error(actual, predicted)
rmse = root_mean_squared_error(actual, predicted)
r2 = r2_score(actual, predicted)

print("MAE (sklearn):", mae)
print("MSE (sklearn):", mse)
print("RMSE (sklearn):", rmse)
print("R2 (sklearn):", r2)
```

**Output:**
```
MAE (sklearn): 3.8
MSE (sklearn): 16.6
RMSE (sklearn): 4.0743097574926725
R2 (sklearn): 0.917
```

**Instructor note:** Numbers match the hand calculation exactly — that is the entire point of the exercise. If a student's sklearn predates `root_mean_squared_error` (pre-1.4), the version-proof fallback is `np.sqrt(mean_squared_error(...))` — write it on the board so nobody gets stuck.

---

## Concept Block 2: R² — What It Really Measures (10 min)

### R² Is Not a Percentage of "Correctness"

The most common misconception: *"R² = 0.85 means the model is 85% accurate."* This is wrong. R² measures **variance explained relative to a naive mean-baseline**, not accuracy in any absolute sense.

```
R² = 1 − (SS_res / SS_tot)

SS_res = Σ(actual − predicted)²        ← your model's total squared error
SS_tot = Σ(actual − mean(actual))²     ← a baseline that always predicts the average
```

### Reading the R² Scale

| R² value | Meaning |
|---|---|
| 1.0 | Perfect predictions — SS_res = 0 |
| 0.0 | Model is exactly as good as always predicting the mean |
| Negative | Model is **worse** than predicting the mean — a real possibility, not a bug |
| Close to 1 but on training data only | Possible overfitting — always check R² on a held-out test set |

**Teaching point:** R² can go negative. Many students assume 0 is the floor. Demonstrate mentally: if a model's predictions are wildly wrong (e.g., predicted values inverted), SS_res can exceed SS_tot, making R² negative. This is a good diagnostic — negative test R² is a loud alarm that something is badly broken (wrong feature, wrong target, data leakage in reverse, or a bug in preprocessing).

### R²'s Blind Spots

- **Scale invariant, so it hides absolute error.** R² = 0.9 on a target ranging 0–1,000,000 and R² = 0.9 on a target ranging 0–10 imply very different absolute error sizes. Always pair R² with MAE/RMSE in the same report.
- **Sensitive to the variance of the test set.** A test set with naturally low variance in the target makes R² unstable and hard to compare across different data splits.
- **Says nothing about *where* the model fails.** A high R² can coexist with a badly biased model on a specific subgroup (recall the Opening hook).

**Teaching point:** Never report R² alone. The professional convention is **MAE or RMSE (for scale) + R² (for relative fit)**, reported together.

---

## Practical Block 2: Comparing Models on the Diabetes Dataset (15 min)

We now move from a toy example to a real dataset, and compare two models from last session side by side using all three metrics.

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import (
    mean_absolute_error, root_mean_squared_error, r2_score
)

data = load_diabetes()
X, y = data.data, data.target
print("Features:", data.feature_names)
print("X shape:", X.shape, "y shape:", y.shape)
print("y range:", y.min(), "-", y.max())
```

**Output:**
```
Features: ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
X shape: (442, 10) y shape: (442,)
y range: 25.0 - 346.0
```

`y` here is a quantitative measure of disease progression one year after baseline — a genuine regression target with real-world units, not an arbitrary toy number.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Train size:", X_train.shape[0], "Test size:", X_test.shape[0])
```

**Output:**
```
Train size: 353 Test size: 89
```

```python
def report(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"{name:20s} MAE={mae:8.2f}  RMSE={rmse:8.2f}  R2={r2:6.3f}")
    return mae, rmse, r2

lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
report("LinearRegression", y_test, y_pred_lr)

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)
report("Ridge (alpha=1.0)", y_test, y_pred_ridge)
```

**Output:**
```
LinearRegression     MAE=   42.79  RMSE=   53.85  R2= 0.453
Ridge (alpha=1.0)    MAE=   46.14  RMSE=   55.47  R2= 0.419
```

**Discussion prompt:** *"Plain LinearRegression beats Ridge here on all three metrics. Does that mean regularization was a bad idea last session?"* → No — it means at `alpha=1.0`, on this particular train/test split, the bias introduced by shrinkage outweighs the variance it removed. Regularization is not universally better; it is a tool you tune (recall: alpha) and *verify with metrics like these*, not something you apply blindly. This is exactly why we evaluate — to catch cases where the "safer-looking" model actually underperforms.

```python
print("\nSample predictions (LinearRegression):")
for i in range(5):
    print(f"  Actual={y_test[i]:6.1f}  Predicted={y_pred_lr[i]:6.1f}  "
          f"Residual={y_test[i]-y_pred_lr[i]:6.1f}")
```

**Output:**
```
Sample predictions (LinearRegression):
  Actual= 219.0  Predicted= 139.5  Residual=  79.5
  Actual=  70.0  Predicted= 179.5  Residual=-109.5
  Actual= 202.0  Predicted= 134.0  Residual=  68.0
  Actual= 230.0  Predicted= 291.4  Residual= -61.4
  Actual= 111.0  Predicted= 123.8  Residual= -12.8
```

**Teaching point:** MAE ≈ 43 with individual residuals as large as 109 tells you the *average* miss hides real spread. This is the bridge into residual analysis after the break.

---

## BREAK (10 min)

*Suggested break prompt — ask students to write down, on paper, one guess: "If I plotted every residual against every predicted value for the LinearRegression model above, what shape would I expect if the model were doing a good job?" Collect a few answers verbally right after the break, before revealing the concept.*

---

## Concept Block 3: Residual Analysis — Reading the Shape of Error (10 min)

### What Is a Residual?

```
residual = actual − predicted
```

A residual is signed: positive means the model under-predicted (actual was higher), negative means it over-predicted. Plotting residuals (y-axis) against predicted values (x-axis) is one of the single most useful diagnostic habits in regression.

### Good Residual Plot vs Bad Residual Plot

```
GOOD (random scatter around zero)          BAD (systematic pattern / curve)
                                       
   residual                                   residual
      ^                                          ^
   4  |  .   .    .                         30   | .  .
   2  |    . .  .    .   .                  15   |    .  .
   0  |--.---.-.------.------> predicted     0   |        .   .
  -2  |  .  .    .  .                       -15   |            .   .
  -4  |    .    .                           -30   |                  . .
      |________________                          |________________
        no pattern, evenly                    U-shape or curve → model
        spread above & below 0                is missing structure in data
```

**Teaching point:** A *good* residual plot has no visible pattern — errors are randomly scattered above and below zero, with roughly constant spread across the range of predictions. A *bad* residual plot shows structure: a curve (U-shape or arc) means the model is underfitting — it's fitting a straight line to data that actually curves. A funnel/cone shape (spread widening as predictions increase) signals heteroscedasticity — the model's error grows with the size of the prediction, which can bias RMSE-based comparisons.

### Reading Checklist for a Residual Plot

| Pattern | What it means | Likely fix |
|---|---|---|
| Random scatter around 0 | Model captures the structure well | None needed — this is the goal |
| U-shape / curve | Underfitting — relationship isn't actually linear | Add polynomial features, use a non-linear model |
| Funnel shape (spread grows) | Heteroscedasticity — error scales with prediction size | Log-transform target, weighted regression |
| Residuals cluster off-center | Systematic bias — model consistently over/under-predicts | Check for missing feature or leakage |

**Key teaching point:** R² and RMSE can look "fine" while the residual plot screams a problem. Residual plots catch structural mistakes that a single summary number cannot.

---

## Practical Block 3: Plotting Residuals — Good Fit vs Bad Fit (15 min)

We build one dataset where a straight line is the right model, and one where it isn't — so students see the residual signature of underfitting with their own eyes.

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

np.random.seed(42)

# --- "Good" case: data is genuinely linear + noise ---
X_lin = np.linspace(0, 10, 60).reshape(-1, 1)
y_lin = 3 * X_lin.ravel() + 5 + np.random.normal(0, 2, size=60)

lr_good = LinearRegression().fit(X_lin, y_lin)
pred_good = lr_good.predict(X_lin)
resid_good = y_lin - pred_good

print("GOOD FIT (linear data, linear model)")
print("R2:", round(r2_score(y_lin, pred_good), 3))
print("Residual mean:", round(resid_good.mean(), 3))
print("Residual std:", round(resid_good.std(), 3))
print("Corr(predicted, residual):", round(np.corrcoef(pred_good, resid_good)[0, 1], 3))
```

**Output:**
```
GOOD FIT (linear data, linear model)
R2: 0.96
Residual mean: -0.0
Residual std: 1.802
Corr(predicted, residual): -0.0
```

```python
# --- "Bad" case: data is curved (quadratic), but we fit a straight line ---
X_curve = np.linspace(0, 10, 60).reshape(-1, 1)
y_curve = 2 * (X_curve.ravel() - 5) ** 2 + 10 + np.random.normal(0, 5, size=60)

lr_bad = LinearRegression().fit(X_curve, y_curve)
pred_bad = lr_bad.predict(X_curve)
resid_bad = y_curve - pred_bad

print("BAD FIT (curved data, straight-line model = underfitting)")
print("R2:", round(r2_score(y_curve, pred_bad), 3))
print("Residual mean:", round(resid_bad.mean(), 3))
print("Residual std:", round(resid_bad.std(), 3))
print("Corr(predicted, residual):", round(np.corrcoef(pred_bad, resid_bad)[0, 1], 3))
```

**Output:**
```
BAD FIT (curved data, straight-line model = underfitting)
R2: 0.0
Residual mean: -0.0
Residual std: 16.543
Corr(predicted, residual): -0.0
```

**Discussion prompt:** *"R² is basically 0.0 — the model explains almost nothing, even though we clearly generated the data from a formula. What happened?"* → The relationship is real, but it's quadratic, not linear. A straight line through symmetric parabola-shaped data ends up nearly flat, close to just predicting the mean everywhere. `lr_bad.coef_` is close to 0 — check it live: the model "gave up" and learned almost no slope.

```python
# Show the U-shape pattern numerically: residuals at edges vs middle
print("Residuals at start (x~0-2): ", np.round(resid_bad[:12], 1))
print("Residuals in middle (x~4-6):", np.round(resid_bad[24:36], 1))
print("Residuals at end (x~8-10):  ", np.round(resid_bad[48:], 1))
```

**Output:**
```
Residuals at start (x~0-2):  [30.7 28.8 21.  17.4 24.5 24.3 14.4 17.1 11.4  3.9  6.6 10.3]
Residuals in middle (x~4-6): [-19.5 -18.5 -11.9 -15.2 -19.7 -14.6 -16.7 -12.3 -20.4 -18.2 -18.1 -22.9]
Residuals at end (x~8-10):   [ 3.5  4.1 -2.9  9.  11.9 26.6 16.1 21.4 22.7 20.1 34.9 36.2]
```

**Walk through this out loud:** positive residuals at the start, negative in the middle, positive again at the end — a textbook U-shape. This is what "the model is missing structure" looks like as numbers, before it's a picture. If a plotting library is available, project `plt.scatter(predicted, residuals)` for both cases side by side — the visual lands faster than the printed numbers for most students, but the printed pattern works identically on a laptop with no display.

**Teaching point:** This is precisely the setup for next session's masterclass — once you can *see* that a straight line is wrong, the natural next question is "how do we find the *right* curve, and how does the model search for it?" That's gradient descent, coming next.

---

## Concept Block 4: Identifying Where a Model Fails (10 min)

### Beyond Averages — Row-Level Error Auditing

MAE and RMSE are averages across the whole test set. They can conceal a model that is excellent on 90% of cases and disastrous on 10%. **Error auditing** means sorting individual predictions by error size and asking *what do the worst ones have in common?*

```
Error Audit Workflow
1. Compute residual for every test row
2. Sort by |residual| descending
3. Inspect the worst N rows — look for shared traits
       (same feature range? same category? same data source?)
4. Segment the test set (e.g. by a feature's median) and
   compare average error across segments
5. Decide: is this random noise, or a fixable systematic gap?
```

### Two Kinds of Error Patterns to Look For

| Pattern | Diagnostic question | What it might reveal |
|---|---|---|
| A few huge outlier errors | Do the worst rows share a feature value? | Missing feature, rare edge case, data entry error |
| Consistent bias in one segment | Is MAE higher for one subgroup than another? | Model underrepresents that subgroup in training data |
| Systematic over/under-prediction | Are residuals mostly positive or mostly negative? | Model has a directional bias — check for a skewed target or leakage |

**Teaching point:** "Model has R² = 0.85" is a headline. "Model has R² = 0.85, but MAE is twice as high for high-value cases" is an insight you can act on — collect more data for that segment, add a feature, or accept the limitation explicitly before shipping.

**Bridge forward:** This kind of error decomposition is also the intuitive seed of *why* gradient descent works — the algorithm is, at its core, repeatedly asking "which direction reduces this same residual the fastest?" You'll formalize that next session.

---

## Practical Block 4: Error Audit — Best, Worst, and Biased Predictions (10 min)

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = load_diabetes()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

lr = LinearRegression().fit(X_train, y_train)
pred = lr.predict(X_test)
residuals = y_test - pred

results = pd.DataFrame({
    "actual": y_test,
    "predicted": pred.round(1),
    "residual": residuals.round(1),
    "abs_error": np.abs(residuals).round(1)
})

print("Worst 5 predictions (largest absolute error):")
print(results.sort_values("abs_error", ascending=False).head(5).to_string(index=False))
```

**Output:**
```
Worst 5 predictions (largest absolute error):
 actual  predicted  residual  abs_error
   52.0      206.5    -154.5      154.5
  200.0       71.7     128.3      128.3
   70.0      179.5    -109.5      109.5
   77.0      180.4    -103.4      103.4
  310.0      207.4     102.6      102.6
```

```python
print("\nBest 5 predictions (smallest absolute error):")
print(results.sort_values("abs_error").head(5).to_string(index=False))
```

**Output:**
```
Best 5 predictions (smallest absolute error):
 actual  predicted  residual  abs_error
   48.0       48.0       0.0        0.0
   94.0       94.1      -0.1        0.1
  108.0      107.7       0.3        0.3
  107.0      109.0      -2.0        2.0
  102.0      105.6      -3.6        3.6
```

**Discussion prompt:** *"The worst prediction is off by 154.5 — more than 3x the MAE. Should we remove this row as an outlier?"* → Not automatically. First check: is it a data error, or a genuinely hard-to-predict patient? Removing inconvenient errors to make metrics look better is a red flag, not a fix.

```python
over = (residuals < 0).sum()   # predicted > actual
under = (residuals > 0).sum()  # predicted < actual
print(f"Model over-predicts on {over} of {len(residuals)} test cases")
print(f"Model under-predicts on {under} of {len(residuals)} test cases")

median_actual = np.median(y_test)
high_group = results[results['actual'] >= median_actual]
low_group = results[results['actual'] < median_actual]
print(f"\nMAE for low-target half  (actual < {median_actual}): "
      f"{round(low_group['abs_error'].mean(), 2)}")
print(f"MAE for high-target half (actual >= {median_actual}): "
      f"{round(high_group['abs_error'].mean(), 2)}")
```

**Output:**
```
Model over-predicts on 42 of 89 test cases
Model under-predicts on 47 of 89 test cases

MAE for low-target half  (actual < 129.0): 39.05
MAE for high-target half (actual >= 129.0): 46.46
```

**Teaching point:** Over/under-prediction is roughly balanced (42 vs 47) — no strong directional bias here. But error is notably higher for high-target patients (46.46 vs 39.05 MAE) — the model struggles more with severe disease progression cases. That's an actionable, segment-specific finding a single R² would have completely hidden.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- MAE and RMSE measure error in the target's own units; RMSE penalizes large errors more heavily
- R² measures variance explained relative to a mean-baseline — it is not "percent accuracy," and it can go negative
- Always report an error-magnitude metric (MAE/RMSE) alongside R² — never rely on one number alone
- Residual plots reveal patterns (curves, funnels) that summary metrics hide entirely
- Error auditing — sorting and segmenting residuals — tells you *where* and *why* a model fails, not just *how much*

**Bridge to next session:** *"Today you learned to read a residual plot and recognize when a straight line is the wrong shape for the data. Next session is a masterclass: we go under the hood of exactly how a line finds its slope and intercept in the first place, what a derivative tells us about a residual, and how gradient descent uses that information to learn — the mathematics behind everything we've been calling `.fit()`."*

**Homework / self-practice:** Take the Ridge vs LinearRegression comparison from Practical 2 and repeat it with `alpha=0.1` and `alpha=10`. For each, record MAE, RMSE, and R². Write one sentence on what changes as alpha increases, and why.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: If RMSE is always ≥ MAE, why not just always report RMSE?**
→ RMSE's sensitivity to large errors is a feature *and* a risk — right emphasis when big misses are costly (e.g., medical dosing). MAE is more representative of "typical" performance when a few outliers shouldn't dominate. Reporting both is the safest default.

**Q: Can R² be greater than 1?**
→ No. SS_res can be 0 at best (perfect predictions), giving R² = 1 as the ceiling — but it has no lower bound and can go arbitrarily negative for a bad enough model.

**Q: Is a "good" R² value the same across every project?**
→ No — it's domain-dependent. R² = 0.3 can be impressive for predicting human behavior (inherently noisy) but poor for a physics-based engineering measurement. Always check what's typical for your domain before judging a number in isolation.

**Q: Does the metric change if we use a different `random_state` for the split?**
→ Yes, often noticeably on a dataset this small (442 rows). That's exactly why cross-validation (Session 2) matters for a trustworthy estimate — a single split's metrics can shift meaningfully. Today's numbers are for teaching clarity; in practice you'd average across folds.

**Q: How do I know if a residual pattern is "real" or just noise from a small test set?**
→ Look for a shape that repeats across multiple splits or CV folds. A pattern in every fold is structural (fix the model); a pattern in only one fold is likely a sample artifact.

---

## Instructor Notes

- **Dataset:** `sklearn.datasets.load_diabetes()` is fully offline and has a real continuous target with actual units — ideal for a metrics-focused session. The synthetic linear/quadratic arrays in Practical 3 use `np.random.seed(42)` for exact reproducibility across machines.
- **sklearn version:** `root_mean_squared_error` was added in 1.4. On older installs, the version-proof fallback is `np.sqrt(mean_squared_error(y_true, y_pred))` — have it ready on the board.
- **Common mistake:** Flipping the residual sign convention (`actual − predicted` vs `predicted − actual`) mid-analysis — every "over-predicts vs under-predicts" statement inverts. This lecture uses `actual − predicted` throughout; pick one and stay consistent.
- **Common mistake:** Treating R² as "percent correct," like classification accuracy. Repeat the mean-baseline framing (Concept Block 2) if this resurfaces during Practical 2 or 4.
- **Live-coding tip:** In Practical 3, if a display is available, plot `plt.scatter(pred_good, resid_good)` next to `plt.scatter(pred_bad, resid_bad)` with a line at 0 — the visual U-shape lands faster than the printed arrays. Without a display, the printed start/middle/end grouping achieves the same goal.
- **For advanced students:** Have them compute Ridge's residual std vs LinearRegression's on the diabetes test set and connect it to the Session 3 bias-variance discussion — regularization should reduce residual variance at some cost to bias.
- **Time check:** If running long, compress Practical 4 by pre-computing the `results` DataFrame and only live-coding the sort/segment lines — the fitting boilerplate duplicates Practical 2.
