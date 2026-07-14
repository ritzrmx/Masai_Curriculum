# Lecture Script: Classification Metrics & Threshold Analysis
> **Instructor Reference** — Module 2: Classical ML | Session 8 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can explain why accuracy is misleading on imbalanced data, build and read a confusion matrix, compute precision/recall/F1 by hand and with `sklearn`, and use `predict_proba()` with threshold tuning and ROC/AUC to choose the right operating point for a classifier.

**Student profile at this point:** Have built Logistic Regression, Decision Tree, and Random Forest classifiers across Sessions 6–7. Have only ever evaluated them with `.score()` (accuracy). Comfortable with `train_test_split`, `fit`/`predict`, and basic Pandas.

**Key outcome:** By end of class, every student can look at a confusion matrix and immediately say "this model is 90% accurate but useless" — and knows exactly which metric and which threshold to reach for instead.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Why Accuracy Lies | 10 min | 0:15 |
| **Practical 1:** The Imbalance Trap | 15 min | 0:30 |
| **Concept 2:** The Confusion Matrix | 10 min | 0:40 |
| **Practical 2:** Building & Reading the Confusion Matrix | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Precision, Recall & F1-Score | 10 min | 1:15 |
| **Practical 3:** Computing Precision, Recall, F1 | 15 min | 1:30 |
| **Concept 4:** Threshold Tuning, ROC Curve & AUC | 10 min | 1:40 |
| **Practical 4:** Threshold Sweep & ROC/AUC | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Write this on the board without context:

```
Model A accuracy: 89.4%
Model B accuracy: 90.2%
```

Ask: *"Which model would you deploy?"* Most hands go up for Model B — it's higher. Then reveal: **Model A never even looks at the data — it just predicts "not fraud" for every single transaction.** Model B is a real, trained Logistic Regression. It only beats the "do-nothing" model by 0.8 percentage points, and — as we'll see in twenty minutes — it catches almost none of the actual fraud.

**Context to set:** Back in Session 2 we discussed class imbalance and why it breaks naive train/test assumptions. Today we go one level deeper: even after you've handled imbalance in your *data*, you can still be completely misled by the *metric* you choose to judge your model. Accuracy treats every mistake as equally bad. In the real world, mistakes are not equal — missing a cancer diagnosis is not the same mistake as a false alarm. Today we build the vocabulary and tools to measure that difference.

**Learning contract for today:**
- Explain why a 90%-accurate model can be worthless
- Read a confusion matrix and derive precision, recall, and F1 from it
- Choose a classification threshold deliberately, using ROC/AUC, instead of defaulting to 0.5

---

## Concept Block 1: Why Accuracy Lies (10 min)

### The Base Rate Problem

When one class dominates the dataset, a model can score high accuracy by simply ignoring the minority class entirely.

```
Fraud detection dataset:  ~90% legitimate, ~10% fraud
A model that ALWAYS predicts "legitimate" scores ~90% accuracy
...and catches ZERO fraud cases.
```

**Teaching point:** Accuracy answers *"how often is the model right overall?"* It does not answer *"is the model right about the cases I actually care about?"* In imbalanced problems, those are very different questions.

### Where This Shows Up in the Real World

| Domain | Majority class | Minority class (the one that matters) | Accuracy of "predict majority always" |
|---|---|---|---|
| Fraud detection | Legitimate transaction | Fraud | ~90–99% |
| Disease screening | Healthy | Disease present | ~90–99% |
| Spam filtering | Not spam | Spam | ~80–95% |
| Manufacturing defect detection | Good part | Defective part | ~95–99.9% |
| Churn prediction | Stays | Churns | ~70–90% |

**Key teaching point:** In every one of these domains, the class you care about most is the *minority* class. This is not a coincidence — rare, costly events are exactly what businesses build models to catch. An evaluation metric that rewards ignoring the minority class is actively dangerous in production.

**Bridge back to Session 2:** Recall the imbalance discussion — we talked about *resampling* and *stratification* as data-side fixes. Today's tools are *metric-side* fixes: even with the same imbalanced data, choosing the right metric changes what "good" means.

---

## Practical Block 1: The Imbalance Trap (15 min)

### Dataset
A synthetic fraud-style dataset with a deliberate 90/10 class imbalance, built with `make_classification`.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

# Imbalanced dataset: 90% class 0 (legit), 10% class 1 (fraud)
X, y = make_classification(
    n_samples=2000, n_features=6, n_informative=4, n_redundant=1,
    weights=[0.9, 0.1], flip_y=0.02, random_state=42
)

print("Class distribution:")
print(pd.Series(y).value_counts())
print("Class balance %:")
print((pd.Series(y).value_counts(normalize=True) * 100).round(2))
```

**Output:**
```
Class distribution:
0    1786
1     214
Name: count, dtype: int64
Class balance %:
0    89.3
1    10.7
Name: proportion, dtype: float64
```

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)
print("Test set class distribution:")
print(pd.Series(y_test).value_counts())
```

**Output:**
```
Test set class distribution:
0    447
1     53
Name: count, dtype: int64
```

**Teaching point:** Note `stratify=y` — this keeps the same 90/10 ratio in train and test. Ask the class: *"What would happen to our test set if we forgot `stratify`?"* (Answer: on a small test set, random chance could give you an even more skewed — or occasionally more balanced — split, making results unreliable.)

```python
# "Always predict majority class" baseline
dummy = DummyClassifier(strategy="most_frequent")
dummy.fit(X_train, y_train)
dummy_preds = dummy.predict(X_test)
print("Dummy (always predict 0) accuracy:", round(accuracy_score(y_test, dummy_preds), 4))
print("Unique predictions from dummy:", np.unique(dummy_preds))

# Real model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
print("LogisticRegression .score() accuracy:", round(model.score(X_test, y_test), 4))
```

**Output:**
```
Dummy (always predict 0) accuracy: 0.894
Unique predictions from dummy: [0]
LogisticRegression .score() accuracy: 0.902
```

**Walk through this live.** The dummy classifier — which never even looks at a feature — scores 89.4%. Our real, trained Logistic Regression scores 90.2%. **That's only a 0.8-point improvement for an entire trained model.** Ask the class: *"Based on accuracy alone, would you say this model learned anything useful?"* Hold the tension here — we'll answer it precisely in Practical Block 2 with the confusion matrix.

**Discussion prompt:** *"If your manager only ever asks 'what's the accuracy?', how would you push back?"* Let a few students answer before moving on.

---

## Concept Block 2: The Confusion Matrix (10 min)

### The 2×2 Matrix

Every binary classifier's predictions can be sorted into exactly four buckets. Draw this on the board:

```
                         PREDICTED
                    Negative      Positive
              +--------------+--------------+
   A   Neg    |      TN      |      FP      |
   C          |  (correct)   | (false alarm)|
   T          +--------------+--------------+
   U   Pos    |      FN      |      TP      |
   A          |   (missed)   |  (correct)   |
   L          +--------------+--------------+
```

**Concrete framing — disease screening:**

| | Predicted Healthy | Predicted Disease |
|---|---|---|
| **Actually Healthy** | **TN** — correctly cleared | **FP** — false alarm, unnecessary follow-up test |
| **Actually Has Disease** | **FN** — disease missed, patient sent home untreated | **TP** — disease correctly caught |

**The four outcomes, defined precisely:**
- **True Positive (TP):** Model predicted positive, and it *was* positive. A correct catch.
- **True Negative (TN):** Model predicted negative, and it *was* negative. A correct clearance.
- **False Positive (FP):** Model predicted positive, but it was *actually negative*. A false alarm (Type I error).
- **False Negative (FN):** Model predicted negative, but it was *actually positive*. A miss (Type II error).

**Teaching point:** FP and FN are not equally costly in most real problems.
- In **disease screening**, a **False Negative** (missed disease) can be fatal — recall matters most.
- In **spam filtering**, a **False Positive** (a real email marked spam and never seen) is worse than letting one spam email through — precision matters most.
- The confusion matrix is what lets you *see* and *choose* this tradeoff instead of guessing.

`sklearn.metrics.confusion_matrix(y_true, y_pred)` builds this matrix for you; `ConfusionMatrixDisplay` plots it as a heatmap with the four cells labeled and colored — worth showing once live so students recognize it in a notebook.

---

## Practical Block 2: Building & Reading the Confusion Matrix (15 min)

### Step 1 — build one by hand on a tiny example first

```python
import numpy as np
from sklearn.metrics import confusion_matrix

# Tiny hand example: 10 patients, disease screening
# 1 = disease present, 0 = disease absent
y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 0, 1])
y_pred = np.array([1, 0, 0, 1, 0, 1, 1, 0, 0, 0])

cm = confusion_matrix(y_true, y_pred)
print("Confusion matrix (rows=actual, cols=predicted):")
print(cm)

tn, fp, fn, tp = cm.ravel()
print(f"TN={tn}  FP={fp}")
print(f"FN={fn}  TP={tp}")
```

**Output:**
```
Confusion matrix (rows=actual, cols=predicted):
[[4 1]
 [2 3]]
TN=4  FP=1
FN=2  TP=3
```

**Before running the code**, have the class count TP/TN/FP/FN by hand, comparing each pair of `(y_true[i], y_pred[i])` one at a time. This builds the muscle memory that `confusion_matrix()` is just automating a count they can already do.

### Step 2 — apply it to the fraud model from Practical 1

```python
preds = model.predict(X_test)
cm = confusion_matrix(y_test, preds)
print("Confusion matrix (fraud model, rows=actual, cols=predicted):")
print(cm)

tn, fp, fn, tp = cm.ravel()
print(f"TN={tn}  FP={fp}")
print(f"FN={fn}  TP={tp}")
print(f"\nTotal legit (0): {tn+fp}, Total fraud (1): {fn+tp}")
print(f"Fraud caught: {tp}/{fn+tp}")
print(f"Fraud missed: {fn}/{fn+tp}")
```

**Output:**
```
Confusion matrix (fraud model, rows=actual, cols=predicted):
[[446   1]
 [ 48   5]]
TN=446  FP=1
FN=48  TP=5

Total legit (0): 447, Total fraud (1): 53
Fraud caught: 5/53
Fraud missed: 48/53
```

**This is the payoff moment for the whole session.** Our "90.2% accurate" model catches **5 out of 53 fraud cases** — it misses 48 of them. It is barely better than doing nothing, and the accuracy score completely hid that from us.

**Ask the class:** *"If this model went to production at a bank, what would happen?"* Let them reason it through: nearly all fraud slips through, while the accuracy dashboard reports "90%, looks great."

**Write on the board:** *A single accuracy number can never tell you which of the four confusion-matrix cells your errors are landing in. Always ask for the matrix.*

---

## BREAK (10 min)

*Suggested break prompt — ask students to predict, before they come back: "Given this confusion matrix, do you think precision or recall will be closer to zero?" They'll find out in the next block.*

---

## Concept Block 3: Precision, Recall & F1-Score (10 min)

### The Formulas — Derived Directly from the Confusion Matrix

```
Precision = TP / (TP + FP)   → "Of everything I flagged positive, how much was right?"
Recall    = TP / (TP + FN)   → "Of everything that was actually positive, how much did I catch?"
F1-Score  = 2 · (Precision · Recall) / (Precision + Recall)   → harmonic mean of the two
```

**Teaching point — say this slowly:** Precision is about the *quality* of your positive predictions. Recall is about the *completeness* of your positive predictions. A model can be excellent at one and terrible at the other — that's exactly what happened with our fraud model.

### When Each Metric Matters Most

| Scenario | Which matters more | Why |
|---|---|---|
| Disease screening | **Recall** | Missing a real case (FN) can cost a life; a false alarm (FP) just means one extra test |
| Spam filter | **Precision** | Blocking a real email (FP) can cost a job offer; letting one spam through (FN) is a minor annoyance |
| Fraud detection | Usually **Recall**, tuned with precision in mind | Missed fraud (FN) is a direct financial loss; too many false alarms (FP) annoys customers and burns investigator time |
| Search/recommendation results | **Precision** | Users only see the top few results; irrelevant ones (FP) waste their attention |

**Why F1 exists:** Precision and recall trade off against each other. If you want to compare two models with a *single* number, F1 punishes models that are lopsided (very high on one, very low on the other) — because it's a *harmonic* mean, not a simple average. A model with precision=1.0 and recall=0.01 gets an F1 near 0.02, not 0.5.

**Teaching point:** There is no universal "best" metric — the right choice depends on which error (FP or FN) is more expensive *in your specific business context*. Always ask: "What does a false positive cost us? What does a false negative cost us?" before picking a metric.

---

## Practical Block 3: Computing Precision, Recall, F1 (15 min)

```python
from sklearn.metrics import (precision_score, recall_score,
                              f1_score, classification_report, accuracy_score)

preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
prec = precision_score(y_test, preds)
rec = recall_score(y_test, preds)
f1 = f1_score(y_test, preds)

print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1-score:  {f1:.4f}")
```

**Output:**
```
Accuracy:  0.9020
Precision: 0.8333
Recall:    0.0943
F1-score:  0.1695
```

**Pause here.** Accuracy says 90%. F1 says 17%. **Same model, same predictions — wildly different verdicts depending on the metric.** This is the entire lesson of today in four printed lines.

```python
print(classification_report(y_test, preds, target_names=["legit(0)", "fraud(1)"]))
```

**Output:**
```
              precision    recall  f1-score   support

    legit(0)       0.90      1.00      0.95       447
    fraud(1)       0.83      0.09      0.17        53

    accuracy                           0.90       500
   macro avg       0.87      0.55      0.56       500
weighted avg       0.90      0.90      0.87       500
```

**Walk through every column.** Precision for fraud (0.83) is *not bad* — when the model does flag fraud, it's usually right. But recall for fraud (0.09) is disastrous — it catches only 9% of actual fraud cases. Point out **macro avg** (unweighted average across classes — treats both classes as equally important) versus **weighted avg** (weighted by class size — dominated by the majority class, and therefore *just as misleading as accuracy* for imbalanced problems). Ask: *"Which average would you report to a manager who wants to know if fraud is being caught?"* → macro avg, or better, the fraud row alone.

```python
# Manual verification from the confusion matrix — precision/recall are NOT magic
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, preds)
tn, fp, fn, tp = cm.ravel()
manual_prec = tp / (tp + fp)
manual_rec = tp / (tp + fn)
manual_f1 = 2 * manual_prec * manual_rec / (manual_prec + manual_rec)
print(f"Manual check -> precision: {manual_prec:.4f}, recall: {manual_rec:.4f}, f1: {manual_f1:.4f}")
```

**Output:**
```
Manual check -> precision: 0.8333, recall: 0.0943, f1: 0.1695
```

**Teaching point:** Every one of these metrics is arithmetic on four numbers you already know how to count. `sklearn` just saves you the typing — there is no hidden magic. Have students compute `manual_prec` by hand on paper from the printed `tn, fp, fn, tp` before revealing the sklearn numbers match.

---

## Concept Block 4: Threshold Tuning, ROC Curve & AUC (10 min)

### Every Classifier is Secretly a Probability Model

`model.predict()` defaults to a **0.5 probability threshold** — anything ≥ 0.5 becomes class 1. That threshold is a *choice*, not a law of nature. `model.predict_proba(X)` exposes the raw probability so you can choose your own cutoff.

```
Raw probability:   0.04   0.12   0.48   0.55   0.91
Threshold = 0.5:    0      0      0      1      1
Threshold = 0.3:    0      0      1      1      1
Threshold = 0.7:    0      0      0      0      1
```

**Teaching point:** Lowering the threshold makes the model flag *more* things as positive → recall goes up, precision typically goes down (more false alarms). Raising the threshold does the opposite. This is THE core lever for tuning a classifier to a business need, and it costs nothing to change — no retraining required.

### The ROC Curve: TPR vs FPR Across Every Threshold

Instead of picking one threshold and computing one precision/recall pair, the **ROC curve** (Receiver Operating Characteristic) plots two rates as the threshold sweeps from 1.0 down to 0.0:

```
True Positive Rate (TPR) = TP / (TP + FN)   →  this IS recall
False Positive Rate (FPR) = FP / (FP + TN)  →  "how often do we cry wolf on negatives?"
```

```
TPR
 1.0 |                                    ***** (perfect classifier: top-left corner)
     |                            ****
     |                      ***
     |                 **
     |             *. .  <- our model's curve
     |         . '
     |     . '
     | . '  <- diagonal = random guessing (AUC = 0.5)
 0.0 +---------------------------------------- FPR
    0.0                                      1.0
```

**Teaching point:** A curve that hugs the top-left corner is a strong classifier — high TPR (catches positives) at low FPR (few false alarms). A curve that sits on the diagonal is no better than a coin flip. **AUC (Area Under the Curve)** compresses the whole curve into one number between 0 and 1: **AUC = the probability that the model ranks a randomly chosen positive example higher than a randomly chosen negative one.** AUC = 0.5 is random; AUC = 1.0 is a perfect ranker.

**Key distinction to hammer home:** Precision/recall/F1 evaluate one *fixed threshold*. ROC/AUC evaluate the model's *entire ranking ability*, independent of any threshold — useful for comparing models before you've decided where to draw the line.

---

## Practical Block 4: Threshold Sweep & ROC/AUC (10 min)

```python
from sklearn.metrics import roc_curve, roc_auc_score

probs = model.predict_proba(X_test)[:, 1]
print("First 10 predicted fraud probabilities:")
print(np.round(probs[:10], 3))
```

**Output:**
```
First 10 predicted fraud probabilities:
[0.004 0.08  0.095 0.128 0.062 0.013 0.208 0.112 0.011 0.042]
```

```python
print(f"{'Threshold':>10} {'Precision':>10} {'Recall':>10} {'F1':>8} {'FraudCaught':>12}")
for t in [0.3, 0.5, 0.7]:
    preds_t = (probs >= t).astype(int)
    p = precision_score(y_test, preds_t, zero_division=0)
    r = recall_score(y_test, preds_t, zero_division=0)
    f1 = f1_score(y_test, preds_t, zero_division=0)
    tp = ((preds_t == 1) & (y_test == 1)).sum()
    total_fraud = (y_test == 1).sum()
    print(f"{t:>10} {p:>10.3f} {r:>10.3f} {f1:>8.3f} {tp:>8}/{total_fraud}")
```

**Output:**
```
 Threshold  Precision     Recall       F1  FraudCaught
       0.3      0.593      0.302    0.400       16/53
       0.5      0.833      0.094    0.169        5/53
       0.7      1.000      0.019    0.037        1/53
```

**Walk through this table slowly — it's the crux of threshold tuning.** At threshold 0.5 (the default), we catch only 5 fraud cases. Simply **lowering the threshold to 0.3** more than triples our catch rate to 16 fraud cases, at the cost of more false alarms (precision drops from 0.83 to 0.59). At 0.7, precision is perfect (every flag is real fraud) but we catch almost nothing.

**Discussion prompt:** *"You're the fraud team lead. Investigating a false alarm costs 10 minutes. Missing real fraud costs $2,000 on average. Which threshold do you pick?"* Let students argue for 0.3 using the cost numbers — this is a live cost-benefit calculation, not just a metrics exercise.

```python
fpr, tpr, thresholds = roc_curve(y_test, probs)
auc = roc_auc_score(y_test, probs)
print(f"ROC AUC: {auc:.4f}")

idx_show = np.linspace(0, len(thresholds) - 1, 6).astype(int)
print("\nSample ROC points (threshold, FPR, TPR):")
for i in idx_show:
    print(f"thresh={thresholds[i]:.3f}  FPR={fpr[i]:.3f}  TPR={tpr[i]:.3f}")
```

**Output:**
```
ROC AUC: 0.7218

Sample ROC points (threshold, FPR, TPR):
thresh=inf  FPR=0.000  TPR=0.000
thresh=0.257  FPR=0.049  TPR=0.340
thresh=0.114  FPR=0.262  TPR=0.509
thresh=0.081  FPR=0.396  TPR=0.679
thresh=0.058  FPR=0.557  TPR=0.849
thresh=0.004  FPR=1.000  TPR=1.000
```

**Interpretation:** An AUC of 0.72 means the model is meaningfully better than random guessing (0.5) but far from perfect (1.0) — it *can* rank fraud higher than legit transactions reasonably often, but the default 0.5 threshold was throwing that ranking ability away. This is the punchline: **the model was never as bad as the 0.5-threshold confusion matrix suggested — we were just using the wrong cutoff.**

**If time allows / advanced students:** Plot the curve with `RocCurveDisplay.from_predictions(y_test, probs)` and show visually how moving along the curve corresponds to sliding the threshold.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Why accuracy is misleading on imbalanced data — a do-nothing baseline scored 89.4%, barely below our trained model's 90.2%
- The confusion matrix: TP, TN, FP, FN, and how to read each cell in context (disease screening, fraud)
- Precision, recall, and F1 — derived directly from the confusion matrix, and *when* each one matters
- Threshold tuning with `predict_proba()` — the default 0.5 cutoff is a choice, not a rule
- ROC curve (TPR vs FPR) and AUC — evaluating a model's ranking ability across *all* thresholds at once

**Bridge to next session:** *"Every metric today assumed we already had labels — `y_true` was given to us. Next class we flip that assumption entirely: Unsupervised Learning and Clustering, where there are no labels at all, and the model's job is to discover structure in the data on its own."*

**Homework / self-practice:** Load `sklearn.datasets.load_breast_cancer()`, train a Logistic Regression, and produce: (1) the confusion matrix, (2) precision/recall/F1, (3) the ROC-AUC score. Then write two sentences: which threshold would you recommend for a cancer-screening deployment, and why?

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: If accuracy is so misleading, why do we still see it reported everywhere?**
→ Accuracy is intuitive and fine when classes are roughly balanced and errors are equally costly. The mistake is using it *by default* on every problem without checking the class balance first.

**Q: Is there a "correct" threshold I should always use instead of 0.5?**
→ No universal answer — it depends on the relative cost of false positives vs. false negatives in your specific application. The threshold sweep and ROC curve are how you *find* the right one for your business case, not a fixed formula.

**Q: Why does F1 use the harmonic mean instead of just averaging precision and recall?**
→ The harmonic mean punishes imbalance between the two more heavily than a simple average. A model with precision=1.0, recall=0.01 would get a misleadingly high simple average (0.505) but a correctly low F1 (~0.02) — F1 reflects that the model is barely usable.

**Q: Does a higher AUC always mean a better model to deploy?**
→ AUC measures ranking quality across all thresholds, which is great for comparing models. But you still deploy at *one* threshold, so always pair AUC comparison with a look at precision/recall at your intended operating point.

**Q: Can I compute precision/recall for problems with more than two classes?**
→ Yes — `sklearn` computes per-class precision/recall/F1 (one-vs-rest) and then lets you average them (`macro`, `weighted`, `micro`). The `classification_report` output already shows this pattern for two classes; the same table extends to N classes.

**Q: What's the difference between ROC-AUC and just looking at the confusion matrix?**
→ The confusion matrix is a snapshot at one threshold. ROC-AUC summarizes performance across *every possible* threshold in one number, so it's better for comparing models before you've committed to an operating point.

---

## Instructor Notes

- **Dataset:** `make_classification(weights=[0.9, 0.1], flip_y=0.02, random_state=42)` gives a reproducible, deliberately imbalanced dataset where the "always predict majority" trap is obvious and the trained model's recall failure is dramatic (5/53 fraud caught) — ideal for the emotional payoff in Practical Block 2. No internet access needed.
- **Common student mistake:** Confusing precision and recall directionally. Anchor it with the mnemonic: **Recall** = "did I **re-call** (catch) everyone who mattered?" **Precision** = "when I said yes, was I **precise** (correct)?"
- **Common student mistake:** Assuming `confusion_matrix()` always orders rows/columns as `[negative, positive]` — it sorts by label value, so with non-0/1 labels the order can differ. Always check `model.classes_` or pass `labels=[0, 1]` explicitly.
- **Live coding tip:** Before printing `classification_report`, ask students to predict whether precision or recall will be lower for the fraud class, based only on the confusion matrix numbers from Practical 2. This forces active recall of the formulas rather than passive reading.
- **For advanced students:** Have them re-run Practical 4 with `class_weight='balanced'` in `LogisticRegression` and compare the new confusion matrix and AUC — a preview of handling imbalance at the model level rather than just the threshold level.
- **For advanced students:** Introduce `precision_recall_curve()` as a companion to `roc_curve()` — more informative than ROC when the positive class is very rare, since ROC's FPR term can look artificially good with a huge negative class.
- **Time check:** If running long after the break, compress Practical 3 to just the `classification_report` output (skip the manual verification code) and move straight to Practical 4 — the threshold sweep table is the highest-value, most memorable part of the session and should not be cut.
