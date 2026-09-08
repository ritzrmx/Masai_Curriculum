# Workshop on Linear and Logistic Regression

**Duration:** 2 hours
**Format:** Single dataset, hands-on, code-along + labs
**Purpose:** Pilot session to evaluate a new instructor before deployment to the main IIT AI/ML batch

**Dataset:** Telco Customer Churn (IBM sample dataset, 7,043 customers, 21 columns) — one real dataset carries the entire session. Part 1 uses it for a genuine regression task. Parts 2–3 pose a classification question on the same customers and let learners watch Linear Regression fail before Logistic Regression fixes it.

---

## Learning Objectives

**Linear Regression**
1. Apply `LinearRegression()`, `fit()`, and `predict()` to train a model and generate predictions on unseen data.
2. Interpret model coefficients and intercept to explain how each feature drives the predicted target.
3. Evaluate model performance using MAE, RMSE, and R² from `sklearn.metrics`.
4. Analyze residuals to judge whether the model's errors are random or patterned.
5. Diagnose overfitting vs underfitting by comparing train-set and test-set performance.

**Logistic Regression**
1. Apply `LogisticRegression()` to train a binary classifier.
2. Interpret predicted probabilities via `predict_proba()` and connect them to the sigmoid function.
3. Adjust the classification threshold and analyze its effect on predictions.
4. Distinguish binary vs multiclass classification setups.

## Sub-Topics

- Train-test split and why it matters
- `LinearRegression()` → `fit()` → `predict()` workflow
- Reading coefficients and intercept as a real-world relationship
- MAE, RMSE, R² — what each one tells you
- Residual analysis — spotting non-random error patterns
- Overfitting vs underfitting via train-vs-test comparison
- Why linear regression breaks for classification (motivating the sigmoid)
- `LogisticRegression()` workflow
- `predict()` vs `predict_proba()` — hard labels vs probabilities
- Threshold adjustment and its effect on precision/recall
- Binary vs multiclass classification (brief conceptual note)

## Session Flow (120 min)

| Time | Duration | Block |
|---|---|---|
| 0:00–0:10 | 10 min | Hook — introduce the dataset, pose two business questions: "How much will this customer pay monthly?" and "Will this customer leave us?" |
| 0:10–0:35 | 25 min | Part 1 — Linear Regression code-along: predict `MonthlyCharges` |
| 0:35–0:50 | 15 min | Hands-on Lab 1 — learners retrain on a different feature subset, compare train vs test scores |
| 0:50–0:55 | 5 min | Break |
| 0:55–1:05 | 10 min | Transition + Guess Round — "Churn is Yes/No. Can Linear Regression still handle it?" |
| 1:05–1:20 | 15 min | Part 2 — Reveal: fit Linear Regression on the churn target, show it break |
| 1:20–1:40 | 20 min | Part 3 — Reveal: fit Logistic Regression, compare head-to-head |
| 1:40–1:55 | 15 min | Hands-on Lab 2 — threshold sweep, learners write down why logistic wins |
| 1:55–2:00 | 5 min | Synthesis + Q&A |

---

## Setup

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, confusion_matrix, precision_score, recall_score
)

df = pd.read_csv("telco.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

print("Rows before dropping nulls:", len(df))
df = df.dropna(subset=["TotalCharges"])
print("Rows after dropping nulls:", len(df))

df = df.drop(columns=["customerID"])
```

**Output:**
```
Rows before dropping nulls: 7043
Rows after dropping nulls: 7032
```

11 customers had a blank `TotalCharges` (new customers with 0 tenure) — dropped rather than imputed, to keep the workshop focused on modeling, not cleaning.

---

## Part 1 — Linear Regression: Predicting Monthly Charges

**Business question:** "How much will this customer pay per month, given their tenure, contract, and services?"

```python
features = ["tenure", "TotalCharges", "SeniorCitizen", "Contract", "InternetService", "PaperlessBilling"]
target = "MonthlyCharges"

X = df[features].copy()
y = df[target].copy()

X = pd.get_dummies(X, columns=["Contract", "InternetService", "PaperlessBilling"], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

y_train_pred = lin_reg.predict(X_train)
y_test_pred = lin_reg.predict(X_test)
```

### Coefficients

```python
for name, coef in zip(X.columns, lin_reg.coef_):
    print(f"{name:35s} {coef:10.4f}")
print(f"{'Intercept':35s} {lin_reg.intercept_:10.4f}")
```

**Output:**
```
tenure                                 -0.3170
TotalCharges                            0.0070
SeniorCitizen                          -0.3081
Contract_One year                       2.6131
Contract_Two year                       4.8092
InternetService_Fiber optic            26.4487
InternetService_No                    -27.9502
PaperlessBilling_Yes                    1.1547
Intercept                              51.0938
```

**Instructor talking point:** Fiber optic internet adds ~₹26/month over the DSL baseline, while having no internet service at all *reduces* the bill by ~₹28 — coefficients read directly as "holding everything else fixed, this feature changes the predicted bill by this much."

### Evaluation

```python
def report(y_true, y_pred, label):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"--- {label} ---")
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2   : {r2:.4f}")

report(y_train, y_train_pred, "TRAIN performance")
report(y_test, y_test_pred, "TEST performance")
```

**Output:**
```
--- TRAIN performance ---
MAE  : 6.6120
RMSE : 8.6252
R2   : 0.9183

--- TEST performance ---
MAE  : 6.7758
RMSE : 8.8318
R2   : 0.9117
```

**Overfitting/underfitting diagnosis:** Train R² (0.918) and test R² (0.912) are almost identical — a gap of 0.0065. This is a well-fit model, not overfitting. If train R² had been far higher than test R², that would signal overfitting; if both were low, that would signal underfitting.

### Residual Analysis

```python
residuals = y_test - y_test_pred
print(residuals.describe())
```

**Output:**
```
count    1407.000000
mean       -0.150676
std         8.833670
min       -27.471807
25%        -5.119613
50%        -0.683543
75%         5.004350
max        29.044025
```

Residuals center near zero (mean ≈ -0.15, median ≈ -0.68) with no strong skew — a healthy sign the model isn't systematically over- or under-predicting any particular range.

### Sample Predictions

```python
sample = pd.DataFrame({"Actual": y_test.values[:5], "Predicted": np.round(y_test_pred[:5], 2)})
print(sample)
```

**Output:**
```
   Actual  Predicted
0   25.00      18.88
1   24.70      20.40
2  102.25      84.14
3   55.05      54.82
4   29.45      50.33
```

---

## Hands-on Lab 1 (15 min)

Learners drop `TotalCharges` from the feature set (a near-duplicate of `tenure × MonthlyCharges`) and retrain. They report the new train/test R² and MAE, and state in one sentence whether the model got better, worse, or stayed the same, and why.

---

## Transition + Guess Round (10 min)

**Instructor poses to the room, before running any code:**

> "`Churn` is Yes/No, not a number. If we encode it as 0 and 1 and throw it straight into `LinearRegression()`, will it work? Vote: Yes, it'll work fine / No, it'll struggle — and explain why in one sentence."

Collect a show of hands and 2–3 verbal justifications before revealing anything. This is the moment that most directly tests whether the instructor can run a discussion, not just narrate code.

---

## Part 2 — Reveal 1: Linear Regression on a Classification Target

```python
features = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen",
            "Partner", "Dependents", "Contract", "InternetService", "PaperlessBilling"]

X = df[features].copy()
y = df["Churn"].map({"Yes": 1, "No": 0})

X = pd.get_dummies(X, columns=["Partner", "Dependents", "Contract", "InternetService", "PaperlessBilling"],
                    drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

lin_clf = LinearRegression()
lin_clf.fit(X_train, y_train)
raw_preds = lin_clf.predict(X_test)

print(np.round(raw_preds[:10], 3))
print("Min predicted value :", round(raw_preds.min(), 3))
print("Max predicted value :", round(raw_preds.max(), 3))
```

**Output:**
```
[ 0.002  0.618 -0.015  0.218  0.088  0.286 -0.027  0.206  0.552  0.002]
Min predicted value : -0.155
Max predicted value : 0.744
Predictions below 0 : 205 (14.6%)
Predictions above 1 : 0 (0.0%)
```

**Reveal moment:** 14.6% of predictions are negative — a nonsensical "probability" of churn. Linear Regression has no mechanism to keep output between 0 and 1; it just fits a straight line through 0/1 labels.

```python
pred_labels = (raw_preds >= 0.5).astype(int)
print("Accuracy when thresholded at 0.5 :", accuracy_score(y_test, pred_labels))
print(confusion_matrix(y_test, pred_labels))
```

**Output:**
```
Accuracy when thresholded at 0.5 : 0.7896
Confusion matrix [[TN FP] [FN TP]]:
[[921 112]
 [184 190]]
```

---

## Part 3 — Reveal 2: Logistic Regression, Head-to-Head

```python
log_clf = LogisticRegression(max_iter=1000)
log_clf.fit(X_train, y_train)

probs = log_clf.predict_proba(X_test)[:, 1]
print(np.round(probs[:10], 3))
print("Min probability :", round(probs.min(), 3))
print("Max probability :", round(probs.max(), 3))
```

**Output:**
```
[0.02  0.659 0.004 0.212 0.072 0.339 0.018 0.173 0.548 0.012]
Min probability : 0.001
Max probability : 0.77
```

Every value is bounded in [0, 1] — the sigmoid guarantees it. There is no equivalent guarantee for Linear Regression's raw output.

```python
default_preds = (probs >= 0.5).astype(int)
print("Accuracy @ threshold 0.5 :", accuracy_score(y_test, default_preds))
print(confusion_matrix(y_test, default_preds))
```

**Output:**
```
Accuracy @ threshold 0.5 : 0.7910
Confusion matrix [[TN FP] [FN TP]]:
[[920 113]
 [181 193]]
```

**Head-to-head:**
```
Linear Regression (thresholded @0.5) accuracy : 0.7896
Logistic Regression (@0.5) accuracy            : 0.7910
```

**This is the real, unscripted result** — accuracy is nearly tied. This is a deliberate teaching trap: if the instructor treats "logistic regression wins on accuracy" as the takeaway, that is the wrong lesson and a red flag for the pilot review. The actual reasons Logistic Regression is the correct choice are:
- Its output is a genuine, bounded probability that can be trusted and compared across customers — Linear Regression's cannot.
- It is trained with a loss function (log loss) that matches a classification problem, rather than minimizing squared error against 0/1 labels.
- Its threshold can be moved in a principled way to trade off precision and recall — shown next. Linear Regression's raw output has no such calibrated meaning to move.

A strong instructor catches this nuance and doesn't oversell accuracy. Watch for this specifically during the pilot.

### Threshold Sweep

```python
for t in [0.3, 0.5, 0.7]:
    preds_t = (probs >= t).astype(int)
    acc = accuracy_score(y_test, preds_t)
    prec = precision_score(y_test, preds_t, zero_division=0)
    rec = recall_score(y_test, preds_t, zero_division=0)
    print(f"threshold={t:.1f}  accuracy={acc:.4f}  precision={prec:.4f}  recall={rec:.4f}  flagged={preds_t.sum()}")
```

**Output:**
```
threshold=0.3  accuracy=0.7335  precision=0.4991  recall=0.7834  flagged=587
threshold=0.5  accuracy=0.7910  precision=0.6307  recall=0.5160  flagged=306
threshold=0.7  accuracy=0.7527  precision=0.7600  recall=0.1016  flagged=50
```

**Instructor talking point:** Lowering the threshold to 0.3 catches far more true churners (recall jumps from 0.52 to 0.78) at the cost of more false alarms (precision drops). For a retention campaign, missing a churner is usually costlier than one wasted discount offer — so a business might deliberately pick 0.3 over the default 0.5. This is the payoff moment for "why adjust the threshold at all."

---

## Hands-on Lab 2 (15 min)

Learners re-run the threshold sweep at 0.4 and 0.6, add the new numbers to the table, and write 2–3 sentences answering: *"Why did Logistic Regression handle this problem correctly while Linear Regression struggled, even though their accuracy was almost the same?"*

---

## Synthesis (5 min)

The takeaway is not "Logistic Regression is better than Linear Regression" as a general rule — it is **match the model to the target type**: a continuous target (`MonthlyCharges`) calls for regression; a categorical target (`Churn`) calls for classification. Accuracy alone can hide this distinction; bounded probabilities, the right loss function, and a controllable threshold do not.

---

## Instructor Evaluation Checklist (Pilot Focus)

- [ ] Explains *why* before *how* (frames the business question before touching code)
- [ ] Runs the Guess Round as a real discussion, not a rhetorical aside
- [ ] Explains the Linear-Regression-on-Churn failure mechanically (unbounded output, wrong loss function), not just "it doesn't work"
- [ ] Does **not** conclude from the near-tied accuracy that "logistic regression wins" without explaining why
- [ ] Connects the threshold sweep to a real business trade-off (missed churners vs false alarms)
- [ ] Paces each block within ±5 minutes of the plan
- [ ] Checks for understanding at least once per block
