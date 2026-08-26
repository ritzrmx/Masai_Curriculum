# Lecture Script: Classification Metrics
> **Instructor Reference** — Module 2: Classical ML | Session 7 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students compute and interpret the full classification metrics toolkit via `sklearn.metrics` on an imbalanced fraud-detection dataset — confusion matrix, precision, recall, F1 — and can pick the right metric for a given business scenario.

**Student profile at this point:** Just trained a `LogisticRegression` classifier and explored threshold tuning by eye in Session 6. Ready to attach precise numbers to the tradeoffs they explored qualitatively.

**Key outcome:** Every student produces a confusion matrix and classification report for the fraud model on `transactions.csv`, correctly identifies why accuracy is misleading on this imbalanced dataset, and writes a justified metric recommendation for a given business scenario.

**Dataset for this session:** `transactions.csv` (in this folder) — 35 rows of `transaction_id`, `amount`, `merchant_category`, `hour_of_day`, `is_fraud`. Deliberately imbalanced: fraud is a minority class (roughly 20% of rows), mirroring real-world fraud detection.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — "95% Accuracy, So What?" | 10 min | 0:10 |
| SEGMENT 2: Confusion Matrix Anatomy | 20 min | 0:30 |
| SEGMENT 3: Precision and Recall | 25 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Precision-Recall Tradeoff & F1 | 20 min | 1:25 |
| SEGMENT 5: Matching Metric to Business Cost | 20 min | 1:45 |
| SEGMENT 6: Lab — Metrics Report + Written Justification | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — "95% Accuracy, So What?" (10 min)

### The Misleading Number (6 min)

**Say:** *"Let's start with a number that SOUNDS impressive: a fraud detection model with 95% accuracy. Great, right? Let's check."*

**Live-code:**

```python
import pandas as pd

df = pd.read_csv("transactions.csv")
print(df["is_fraud"].value_counts())
print(df["is_fraud"].value_counts(normalize=True))
```

**Run it and read the class balance aloud.** **Say:** *"Roughly 80% of these transactions are legitimate, 20% are fraud. Now imagine a 'model' that NEVER flags anything as fraud — it just predicts 'legitimate' for every single transaction, no learning involved at all."*

```python
naive_accuracy = (df["is_fraud"] == 0).mean()
print(f"Naive 'always predict legitimate' accuracy: {naive_accuracy:.3f}")
```

**Run it.** **Say:** *"Look at that — a model that does ZERO work, catches ZERO fraud, achieves roughly 80% accuracy just by always guessing the majority class. A REAL model reporting 95% accuracy might sound better, but is it actually catching fraud, or just being slightly better at the same lazy trick? Accuracy alone can't tell us. That's the entire problem this session solves."*

### Setting Up the Session (4 min)

**Ask:** *"What questions would you actually want answered about a fraud model, beyond just 'accuracy'?"* Collect answers, steering toward: how much real fraud does it catch? How many false alarms does it raise? Is missing fraud or raising false alarms worse for this business?

**Learning contract for today — write on board:**

- Read a confusion matrix and name all four outcome types
- Compute precision, recall, and F1 with `sklearn.metrics`
- Explain the precision-recall tradeoff and connect it to threshold choice from Session 6
- Recommend the right metric for a given business scenario, with justification

---

## SEGMENT 2: Confusion Matrix Anatomy (20 min)

### The Smoke Detector Story (5 min)

**Say:** *"A smoke detector can be right two ways and wrong two ways. Right: it alarms during a real fire, or stays silent when there's no fire. Wrong: it stays silent DURING a real fire — dangerous — or it alarms with NO fire — annoying but safe. The confusion matrix names all four of these outcomes precisely, for any binary classifier."*

Draw the 2x2 grid on the board:

```
                    Predicted No Fraud   Predicted Fraud
Actual No Fraud            TN                  FP
Actual Fraud                FN                  TP
```

**Say:** *"TN = true negative (correctly said 'legitimate'). FP = false positive (false alarm — flagged a legit transaction as fraud). FN = false negative (missed fraud — the dangerous one). TP = true positive (correctly caught real fraud)."*

### Live Demo — Building the Confusion Matrix (10 min)

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

X = df[["amount", "hour_of_day"]]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(cm)

ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Legitimate", "Fraud"]).plot()
plt.show()
```

**Run it and read the printed matrix aloud, mapping each number to TN/FP/FN/TP explicitly on the board.** **Say:** *"Notice `amount` and `hour_of_day` are strong signals here by design — fraud in this dataset tends to be high-amount, late-night transactions. Real fraud detection needs many more features and far more data, but the metrics mechanics we practice today are identical regardless of dataset size."*

**Ask:** *"Looking at your printed matrix, which cell would you look at FIRST if you were the fraud team's manager? Why?"* Guide toward: FN (missed fraud) — usually the costliest cell for a fraud team specifically.

### Reading the Matrix in Both Directions (5 min)

**Say:** *"One subtlety worth flagging: `confusion_matrix`'s row/column convention can vary by library. In scikit-learn's default output, ROWS are the ACTUAL class, COLUMNS are the PREDICTED class. Always check `display_labels` or the axis titles when reading someone else's confusion matrix plot — this mix-up is a common source of miscommunication in real teams."*

**Live-code a manual unpacking to reinforce the layout:**

```python
tn, fp, fn, tp = cm.ravel()
print(f"TN={tn}, FP={fp}, FN={fn}, TP={tp}")
```

**Run it and confirm these four numbers match what students identified on the board.**

---

## SEGMENT 3: Precision and Recall (25 min)

### The Airport Security Analogy (5 min)

**Say:** *"A metal detector at airport security that beeps at EVERYTHING has perfect RECALL — it catches every real weapon, guaranteed, since it flags everyone. But it has terrible PRECISION — almost every beep is a false alarm. One that only beeps when it's 99% sure has high precision but might miss real threats — low recall."*

### Deriving the Formulas on the Board (8 min)

**Say:** *"Let's derive both formulas directly from the confusion matrix cells."*

Write on the board:

```
Precision = TP / (TP + FP)
  "Of everything we PREDICTED positive, how much was actually positive?"

Recall = TP / (TP + FN)
  "Of everything that was ACTUALLY positive, how much did we catch?"
```

**Ask:** *"Using our printed confusion matrix numbers from SEGMENT 2, can someone compute precision by hand?"* Have a student do the arithmetic on the board using the actual TN/FP/FN/TP values from the live run.

### Live Demo — sklearn.metrics (7 min)

```python
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1: {f1:.3f}")
print(classification_report(y_test, y_pred))
```

**Run it and compare the printed `precision_score` to the manual hand-calculation from the previous step — they should match exactly.** **Say:** *"This confirms `precision_score` isn't a black box — it's literally computing `TP / (TP + FP)` from the confusion matrix cells, just automated."*

### Reading classification_report (5 min)

**Say:** *"`classification_report` gives you precision, recall, and F1 for BOTH classes at once, plus 'support' — how many actual examples of each class exist in the test set. Always check support on an imbalanced dataset like ours — a tiny support number for the fraud class means our precision/recall estimates themselves are less statistically reliable, since they're based on very few examples."*

**Ask:** *"Looking at the 'support' column in your printed report, how many actual fraud cases are in our test set? Does that number feel like 'enough' to trust the reported precision/recall confidently?"* Guide toward: with a small dataset like this, support for the minority class will be quite low (single digits), which is worth flagging honestly — real fraud detection systems train on much larger datasets specifically because rare-class metrics need more examples to be trustworthy.

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to recall Session 6's threshold discussion — did they argue for raising or lowering the threshold for a "cautious bank"? Come back ready to connect that discussion to precision and recall by name.

---

## SEGMENT 4: Precision-Recall Tradeoff & F1 (20 min)

### Connecting Back to Session 6's Threshold Discussion (5 min)

**Say:** *"Remember Session 6: lowering the threshold approves MORE positives, catching more true positives but also more false positives. Raising it does the opposite. Let's now put PRECISE NUMBERS on that intuition."*

### Live Demo — Sweeping the Threshold and Watching Both Metrics (10 min)

```python
probs = model.predict_proba(X_test)[:, 1]

for t in [0.1, 0.3, 0.5, 0.7, 0.9]:
    preds_at_t = (probs >= t).astype(int)
    p = precision_score(y_test, preds_at_t, zero_division=0)
    r = recall_score(y_test, preds_at_t, zero_division=0)
    print(f"threshold={t}: precision={p:.3f}, recall={r:.3f}")
```

**Run it and read the table aloud, row by row.** **Say:** *"Watch the pattern: as threshold RISES, precision generally goes UP (or stays high) and recall generally goes DOWN. This is the precision-recall tradeoff, made completely concrete — not just a qualitative direction like in Session 6, but exact numbers you can compare."*

**Note the `zero_division=0` parameter:** *"With so few fraud examples in our test set, some thresholds might produce zero predicted positives at all, which would otherwise raise a warning or error when computing precision (dividing by zero). This parameter tells scikit-learn to report 0 in that case instead of crashing."*

### The precision_recall_curve (3 min)

```python
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

precisions, recalls, thresholds = precision_recall_curve(y_test, probs)

plt.plot(thresholds, precisions[:-1], label="Precision")
plt.plot(thresholds, recalls[:-1], label="Recall")
plt.xlabel("Threshold")
plt.legend()
plt.show()
```

**Run it.** **Say:** *"This plots exactly what we just tabulated by hand, across EVERY possible threshold rather than just five samples — the two lines should cross somewhere, and that crossing point is often a reasonable 'balanced' choice if you have no strong business reason to prefer one over the other."*

### F1 as a Single Balancing Number (2 min)

**Say:** *"F1 is the harmonic mean of precision and recall — a single number that's high only when BOTH precision and recall are reasonably high. It's useful exactly when you have no strong business reason to prioritize one over the other. When you DO have such a reason — as we're about to explore — a raw precision or recall number, considered alone, is often more informative than F1."*

---

## SEGMENT 5: Matching Metric to Business Cost (20 min)

### The Core Question (5 min)

**Say:** *"Every classification project should start by asking: which error costs us more, a false positive or a false negative? The answer determines whether you chase precision, recall, or accept the F1 balance."*

Draw this table on the board, building it WITH the class rather than presenting it complete:

| Business scenario | Costlier error | Prioritize |
|---|---|---|
| Fraud detection | Missing fraud (FN) | Recall, with precision monitored |
| Spam filter | Blocking a real email (FP) | Precision |
| Disease screening | Missing a sick patient (FN) | Recall |
| Balanced classes, no strong asymmetry | Either | Accuracy can be reasonable |

### Small Group Discussion (10 min)

**Say:** *"Get into small groups. I'm assigning each group one scenario. Argue for precision, recall, or F1, and be ready to defend your choice."*

**Scenarios to assign:**

1. Medical screening for a treatable but dangerous disease
2. Spam filter for a busy executive's inbox
3. Loan approval fraud check (flagging suspicious applications for manual review, not auto-rejecting)
4. Quality control on a manufacturing line (flagging defective products before shipping)

**Facilitation:** Walk the room during discussion. For scenario 3 specifically, note that "flagging for REVIEW" (not auto-rejecting) changes the cost calculus — a false positive here just costs a human reviewer's time, not a lost customer, which might shift the group toward favoring recall more heavily than they would for a harsher auto-decision.

### Debrief (5 min)

Have one representative from each group share their recommendation and reasoning. **Say, closing:** *"Notice that NONE of these decisions required training a different model — they're about which METRIC to optimize and monitor, a decision made with business stakeholders BEFORE or alongside modeling, echoing Session 1's problem-framing worksheet."*

---

## SEGMENT 6: Lab — Metrics Report + Written Justification (10 min)

### Instructions (read aloud, step by step)

1. Load `transactions.csv`, split `X` (`amount`, `hour_of_day`) and `y` (`is_fraud`) with `train_test_split(test_size=0.3, random_state=42, stratify=y)`.
2. Train a `LogisticRegression(max_iter=1000)`.
3. Print the confusion matrix and full `classification_report`.
4. Compute accuracy separately and compare it to precision/recall for the fraud class — note any discrepancy.
5. Write 2-3 sentences justifying which metric (precision, recall, or F1) this fraud-detection business should optimize for, and why.

### Starter Code

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

df = pd.read_csv("transactions.csv")
X = df[["amount", "hour_of_day"]]
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___, random_state=42, stratify=___)

model = ___(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)

print(confusion_matrix(___, ___))
print(classification_report(___, ___))
print("Accuracy:", accuracy_score(___, ___))

# TODO: write your 2-3 sentence metric justification here as a comment
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

df = pd.read_csv("transactions.csv")
X = df[["amount", "hour_of_day"]]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# Justification: fraud is the minority class and missing real fraud (a false
# negative) is far costlier to the business than reviewing a legitimate
# transaction unnecessarily (a false positive). This business should
# prioritize RECALL for the fraud class, while still monitoring precision
# so the review team isn't overwhelmed with false alarms. Accuracy alone
# is misleading here since a model that predicts "legitimate" for
# everything would already score roughly 80% by doing no real work.
```

**Instructor circulates**, checking that students' written justification explicitly references the imbalance and names a specific metric with reasoning, not just a number.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Why accuracy alone is misleading on imbalanced data — the "always predict majority class" trap
- Confusion matrix anatomy: TN, FP, FN, TP, and reading row/column conventions carefully
- Precision (`TP/(TP+FP)`) and recall (`TP/(TP+FN)`), derived from the confusion matrix
- The precision-recall tradeoff, now with precise numbers attached to Session 6's threshold intuition
- Matching the right metric to business cost — recall-first, precision-first, or F1-balanced

**Bridge to next session:** *"Today you learned to MEASURE a classifier honestly and pick the right yardstick for the job. Next session is a master class — we step back from code and build the mathematical intuition for probability, conditional probability, and Bayes' Theorem, which is the foundation underneath every probability a classifier has ever reported to you, including every `predict_proba()` output from the last two sessions."*

**Homework / self-practice:**
1. Retrain the model using only `amount` as a single feature (drop `hour_of_day`). Compare the confusion matrix to today's two-feature version.
2. Sweep thresholds from 0.1 to 0.9 and find the threshold that MAXIMIZES F1 specifically. Report it.
3. Write, in your own words, a one-paragraph explanation of why a model with 95% accuracy could still be a BAD fraud detector.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Is there a metric that combines precision and recall differently than F1, weighting one more than the other?**
→ Yes — the F-beta score generalizes F1, letting you weight recall more or less heavily than precision via a `beta` parameter. `fbeta_score` in `sklearn.metrics` supports this directly. Worth a one-line mention as "further reading," not required for this course.

**Q: What does `zero_division=0` actually prevent?**
→ Without it, computing precision when there are ZERO predicted positives (dividing by zero) raises a warning and returns `nan` by default in some scikit-learn versions. Setting it to 0 gives a clean, defined number instead, useful for automated sweeps like our threshold loop.

**Q: If precision and recall are both important, why not just always use F1 and skip the debate?**
→ F1 assumes precision and recall matter EQUALLY, which is rarely true in practice. A fraud team that explicitly cares more about not missing fraud than about false alarms should track recall directly (perhaps alongside precision as a secondary check), rather than blending them into one number that could hide a real recall shortfall behind a decent-looking F1.

**Q: How do I know if my dataset is "imbalanced enough" to worry about all this?**
→ There's no strict cutoff, but as a rule of thumb, if the minority class is much less than 50% (say, under 30%, and especially under 10%), accuracy alone becomes increasingly unreliable and confusion-matrix-based metrics become essential.

**Q: Can I compute these metrics for a MULTICLASS problem too, not just binary?**
→ Yes — `precision_score`, `recall_score`, and `f1_score` all support an `average` parameter (`"macro"`, `"weighted"`, `"micro"`) for multiclass problems, computing per-class metrics and combining them. This is beyond today's binary-focused scope but good to know exists.

**Q: Does the ORDER of arguments matter when calling `confusion_matrix(y_test, y_pred)`?**
→ Yes — scikit-learn's convention is `confusion_matrix(y_true, y_pred)`, true values first. Swapping the order would transpose the matrix and could lead to misreading which cell is which.

---

## Instructor Notes

- **Prerequisite check:** Confirm students recall Session 6's threshold discussion by name before SEGMENT 4 — today's tradeoff demo depends on that intuition already being in place.
- **Common mistake:** Reporting accuracy alone on this imbalanced dataset. Catch it immediately in the lab and connect back to SEGMENT 1's "naive always-legitimate" demo.
- **Another common mistake:** Misreading the confusion matrix's row/column convention. Address this explicitly with the `.ravel()` unpacking demo in SEGMENT 2 if any confusion appears.
- **Engagement tip:** SEGMENT 5's small-group scenario debate tends to generate strong, sometimes passionate disagreement (especially the fraud-review scenario) — let it run, since the disagreement itself is the learning moment; there often isn't one single "correct" answer, only a well-justified one.
- **Time check:** If running behind before the break, shorten SEGMENT 3's `classification_report` walkthrough to reading just the fraud-class row, skipping the full table discussion.
- **If running long after the break:** Compress SEGMENT 5 to two scenarios instead of four, prioritizing the fraud and spam-filter cases since they contrast most clearly.
- **Materials to prepare:** `transactions.csv` open and ready; a pre-typed notebook with the naive "always predict majority class" demo ready to run first for maximum impact.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Reporting accuracy alone on imbalanced data | Misleadingly high number that hides poor minority-class detection | Always pair accuracy with confusion matrix / precision / recall on imbalanced data |
| Misreading confusion matrix row/column convention | Precision and recall computed backwards | Use `.ravel()` to explicitly unpack TN/FP/FN/TP and double-check `display_labels` |
| Treating F1 as always the "best" metric | Hides a business-critical recall or precision shortfall | Ask "which error costs more" first; use F1 only when truly balanced |
| Computing precision/recall without `zero_division` handling on sparse predictions | Warnings or `nan` results during threshold sweeps | Pass `zero_division=0` when appropriate |
| Confusing precision and recall's formulas | Swapped interpretation of "false alarm rate" vs "catch rate" | Precision = TP/(TP+FP); Recall = TP/(TP+FN) — write both on the board every time |

---

## Appendix: Metric Formula Quick Reference (Instructor Reference)

| Metric | Formula | Answers |
|---|---|---|
| Accuracy | (TP+TN) / (TP+TN+FP+FN) | What fraction of ALL predictions were correct? |
| Precision | TP / (TP+FP) | Of predicted positives, how many were real? |
| Recall | TP / (TP+FN) | Of real positives, how many did we catch? |
| F1 | 2 * (Precision*Recall) / (Precision+Recall) | Single balanced number, when both matter equally |

---

## Appendix: Supplemental Practice Bank (Optional, If Time Allows)

### Drill 1 — Manual confusion matrix arithmetic

Given TN=50, FP=5, FN=8, TP=12:

```
Precision = 12 / (12+5) = 0.706
Recall    = 12 / (12+8) = 0.600
Accuracy  = (12+50) / (50+5+8+12) = 0.827
```

**Ask the class to verify this arithmetic independently before revealing it.**

### Drill 2 — Metric-to-scenario matching

Match each scenario to precision, recall, or F1:

1. A company wants to minimize customer complaints about wrongly-blocked legitimate purchases → Precision
2. A hospital wants to minimize missed cases of a contagious disease → Recall
3. A general-purpose spam/ham classifier with no stated business priority → F1

---

## FAQ — Additional Questions

**Q: Is there a version of the confusion matrix for more than two classes?**
→ Yes — for multiclass problems, the confusion matrix becomes an NxN grid (N = number of classes), with the diagonal representing correct predictions and off-diagonal cells representing specific types of misclassification between class pairs.

**Q: Why does `classification_report` show a `support` column — what is it for?**
→ It's the actual COUNT of true instances of each class in the test set. It's essential context for judging how statistically reliable a given precision/recall number is — a precision of 1.00 based on only 2 true examples is far less trustworthy than the same number based on 200.

**Q: If I'm choosing between two models, should I always pick the one with higher F1?**
→ Only if F1 is genuinely the right metric for your business problem, as determined by SEGMENT 5's analysis. If recall is what actually matters (e.g. fraud, disease screening), a model with slightly lower F1 but meaningfully higher recall may be the better real-world choice.

**Q: Does regularization (Session 5) or the threshold (Session 6) have any effect on which metrics we should even bother computing?**
→ No — precision, recall, F1, and the confusion matrix apply to ANY classifier's predictions, regardless of what algorithm or hyperparameters produced them. What changes based on your metric goals is HOW you tune the threshold and possibly which model/regularization settings you select via cross-validation — the metrics themselves are model-agnostic measurement tools.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Finding the F1-optimal threshold programmatically (6 min)

```python
best_threshold, best_f1 = None, -1
for t in [i / 100 for i in range(5, 100, 5)]:
    preds_at_t = (probs >= t).astype(int)
    f1_at_t = f1_score(y_test, preds_at_t, zero_division=0)
    if f1_at_t > best_f1:
        best_threshold, best_f1 = t, f1_at_t

print(f"Best threshold for F1: {best_threshold}, F1 = {best_f1:.3f}")
```

**Break it down:**
- This automates what SEGMENT 4 did by hand at five threshold values, now sweeping a much finer grid
- The "best" threshold here is optimal specifically FOR F1 — if the business actually prioritizes recall instead, this would NOT be the right threshold to deploy
- This is a good bridge into Session 11's `GridSearchCV`, which automates hyperparameter search more generally

**Ask:** If we changed the loop to maximize recall instead of F1, what threshold would likely win, and why?

**Common mistake:** Assuming the F1-optimal threshold is always the "correct" one to use in production.

**Fix:** Always tie the optimization target back to the business-cost analysis from SEGMENT 5, not just whichever metric is easiest to compute.

### Demo B — ROC-AUC as a threshold-independent summary (5 min)

```python
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

auc = roc_auc_score(y_test, probs)
print(f"ROC-AUC: {auc:.3f}")

fpr, tpr, _ = roc_curve(y_test, probs)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.show()
```

**Break it down:**
- Unlike precision/recall/F1, ROC-AUC summarizes performance ACROSS ALL possible thresholds into one number, between 0.5 (no better than random) and 1.0 (perfect)
- It's a common metric to report alongside precision/recall, especially when COMPARING two different models before deciding on a specific threshold
- The diagonal dashed line represents "random guessing" — a useful visual anchor

**Ask:** If two models have the same ROC-AUC but very different precision at your chosen threshold, which one would you actually deploy?

**Common mistake:** Treating ROC-AUC as a replacement for precision/recall rather than a complementary, threshold-independent summary.

**Fix:** Use ROC-AUC to compare overall model quality; use precision/recall/F1 to evaluate a SPECIFIC deployed threshold's real-world behavior.

### Demo C — Precision and recall on the training set vs test set (4 min)

```python
train_preds = model.predict(X_train)
print("Train classification report:")
print(classification_report(y_train, train_preds))
print("Test classification report:")
print(classification_report(y_test, y_pred))
```

**Break it down:**
- This directly extends Session 4-5's overfitting diagnostic (comparing train vs test) into the classification-metrics world
- A large gap between train and test precision/recall for the fraud class would suggest overfitting, exactly as a large train/test R2 gap did for regression
- This reinforces that "diagnose overfitting by comparing train vs test" is a general ML habit, not specific to regression

**Ask:** What would a much higher train recall than test recall suggest about this model?

**Common mistake:** Only ever checking test-set metrics and never comparing back to training-set metrics for an overfitting sanity check.

**Fix:** Make train-vs-test metric comparison a standing habit for every classifier, not just every regressor.

---

## Materials Checklist

- [ ] `transactions.csv` open and readable in the working notebook environment
- [ ] Pre-typed notebook with the naive "always predict majority class" demo ready to run first
- [ ] Whiteboard space for the confusion matrix grid and precision/recall formulas
- [ ] Optional: matplotlib available for the precision-recall curve and Demo B's ROC curve
- [ ] Timer visible for the lab and small-group discussion segments

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's `classification_report` walkthrough to the fraud-class row only |
| Running long after break | Compress SEGMENT 5 to two scenarios instead of four |
| Low energy after lunch/break | Run Appendix Drill 1 (manual confusion matrix arithmetic) as a quick energizer |
| Advanced group finishes lab early | Assign Demo A or Demo B from SEGMENT 8 as a stretch task |
| No shared screen / projector issue | Read code blocks aloud and have students type along from the printed lecture script |

---

## End-of-Session Quiz (5 Questions)

1. Why can a "model" that always predicts the majority class still score high accuracy on imbalanced data?
2. Write the formulas for precision and recall in terms of TP, FP, and FN.
3. If a business cares most about not missing real fraud, which metric should be prioritized?
4. What does F1 measure, and when is it the wrong metric to optimize?
5. What does the `support` column in a `classification_report` tell you?

**Answer key (instructor):**
1. Because the majority class already makes up most of the data, so predicting it every time is "correct" most of the time by default, without any real learning.
2. Precision = TP/(TP+FP); Recall = TP/(TP+FN).
3. Recall (while still monitoring precision so false alarms don't overwhelm the review process).
4. F1 is the harmonic mean of precision and recall, a single balanced number; it's the wrong metric when the business genuinely cares about one of the two more than the other.
5. The actual count of true examples of each class in the test set — important context for how statistically reliable the reported metrics are.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Single-feature confusion matrix comparison | Correct retrain and comparison with clear observations | Comparison present, thin observations | Partial attempt | Not attempted |
| F1-optimal threshold search | Correct sweep, correct best threshold reported | Sweep run, minor reporting issues | Partial sweep | Not attempted |
| "95% accuracy could still be bad" paragraph | Clear, correct, references the imbalance/majority-class trap | Mostly correct, some vagueness | Attempted, misses the core mechanism | Not attempted |

**Total:** /12 — Pass threshold: 8/12

---

## Appendix: Extended Practice Bank (Optional Take-Home or Fast-Finisher Set)

### Bank 1 — Confusion matrix cell identification

For a fraud model, classify each described outcome as TN, FP, FN, or TP:

1. Model predicted "fraud," transaction was actually fraud → TP
2. Model predicted "legitimate," transaction was actually fraud → FN
3. Model predicted "fraud," transaction was actually legitimate → FP
4. Model predicted "legitimate," transaction was actually legitimate → TN

### Bank 2 — Precision/recall from raw counts

Given TP=18, FP=2, FN=6, TN=74:

```
Precision = 18 / (18+2) = 0.900
Recall    = 18 / (18+6) = 0.750
F1        = 2 * (0.9*0.75) / (0.9+0.75) = 0.818
```

**Instructor note:** Have students compute this independently before revealing it.

### Bank 3 — Metric priority reasoning

For each scenario, state the single metric this team should track most closely, with a one-sentence reason:

1. A social media platform flagging posts for manual moderation review (not auto-removal) → Recall — a missed harmful post is worse than an extra review, especially when a human still checks flagged posts
2. An e-commerce site auto-blocking suspicious-looking listings before they go live → Precision — wrongly blocking a legitimate seller's listing has a real, direct cost to that seller

---

## Closing Instructor Reflection Notes

- This session is where "problem framing" from Session 1 and "threshold tuning" from Session 6 fully converge into a rigorous measurement practice — students who struggled with either earlier concept often have their strongest "aha" moment here, once the abstract tradeoff gets attached to concrete formulas.
- If a cohort is unusually strong technically, SEGMENT 8's Demo A (F1-optimal threshold search) and Demo B (ROC-AUC) both land well and can be promoted from optional to core.
- If a cohort is running behind, the single highest-value cut is the small-group debate in SEGMENT 5 — trim it to two scenarios rather than four, but do not skip it entirely, since it's what makes the metric-selection skill feel like a real decision rather than a memorized rule.
