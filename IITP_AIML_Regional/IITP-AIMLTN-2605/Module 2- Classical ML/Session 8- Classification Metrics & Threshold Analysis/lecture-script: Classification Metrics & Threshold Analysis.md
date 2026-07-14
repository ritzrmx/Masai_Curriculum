# Lecture Script: Classification Metrics & Threshold Analysis
> **Instructor Reference** — Module 2: Classical ML | Session 8 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students build a fraud classifier on deliberately imbalanced data, watch it score 96% accuracy while missing more than half the frauds, and then fix it — not by retraining, but by reading the confusion matrix, choosing the right metric, and moving the decision threshold to a value justified by a real business cost.

**Student profile at this point:** They can train classifiers (Session 6), build ensembles (Session 7), and call `.predict()` and `.predict_proba()`. They have used `accuracy_score` and believe it. They have never seen a confusion matrix, a threshold sweep, or an ROC curve.

**Key outcome:** A notebook that takes one trained model and produces: a confusion matrix, a classification report, a threshold sweep table, ROC and precision–recall curves, and a single chosen operating threshold with a rupee figure justifying it.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The 95% Model That Catches Nothing | 5 min | 0:05 |
| **Concept 1:** The Accuracy Paradox and the Confusion Matrix | 10 min | 0:15 |
| **Practical 1:** Build the imbalanced data, expose the lie | 15 min | 0:30 |
| **Concept 2:** Precision, Recall, F1, Specificity | 10 min | 0:40 |
| **Practical 2:** classification_report and naming the errors | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** The Threshold Is a Dial, Not a Law | 10 min | 1:15 |
| **Practical 3:** Sweep the threshold, walk the tradeoff | 15 min | 1:30 |
| **Concept 4:** ROC-AUC vs the Precision–Recall Curve | 10 min | 1:40 |
| **Practical 4:** Curves, AUC, and a threshold chosen by cost | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — write this on the board before anyone opens a laptop:**

```
I have built a fraud detection model.
It is 95% accurate.
It is one line of code:

    def predict(transaction):
        return "not fraud"
```

Let it sit in silence for a few seconds. Then ask the room:

*"Out of 10,000 transactions, 500 are fraud. My model says 'not fraud' every single time. How many does it get right? 9,500. That's 95% accuracy — better than most models any of you trained last week. Would you deploy it?"*

Someone will say "obviously not." Push them: *"Then tell me the number that proves it's bad. Because accuracy says it's good."* They will not have one. That is the session.

**What model evaluation is NOT:**
- Printing `accuracy_score` and moving on
- Assuming `.predict()` is telling you what the model actually thinks
- Treating 0.5 as a sacred, mathematically derived cut-off
- Believing one number can summarise every kind of mistake

**What model evaluation IS:**
- Knowing exactly *which* of your two errors the model is making
- Deciding, before you look at any metric, which error costs your business more
- Treating the threshold as a dial you are paid to tune, not a default you inherit
- Being able to say "we chose 0.14, and it saves us ₹1,07,500 on this test set"

---

## Concept Block 1: The Accuracy Paradox and the Confusion Matrix (10 min)

### Why accuracy breaks (board)

```
accuracy = (TP + TN) / (TP + TN + FP + FN)
```

On balanced data this is fine. On **imbalanced** data — where the class you care about is rare — TN is enormous and it drowns everything else. The model gets rewarded for correctly ignoring the boring class.

**The rule to write on the board:** *Accuracy is only meaningful when the classes are roughly balanced. The moment they are not, accuracy is a distraction.*

### The confusion matrix — the four boxes

Choose your **positive class** first. It is always the rare, interesting, expensive thing: fraud, disease, churn, defect. Everything else is negative.

|  | **Predicted: Negative** | **Predicted: Positive** |
|---|---|---|
| **Actual: Negative** | TN — correctly ignored | **FP — false alarm** |
| **Actual: Positive** | **FN — missed it** | TP — caught it |

Draw this 2×2 grid on the board and leave it there for the entire session. You will point at it thirty times.

### Make them name the errors

This is the single most important five minutes of the session. Give the room a scenario and make them say the errors *in English*, not initials:

> *"You're building a model that flags UPI transactions as fraud. What is a false positive? What is a false negative? Say it as a sentence about a real person."*

Force the full sentences out of them:
- **FP:** "We froze Ravi's card while he was paying for his mother's medicine."
- **FN:** "₹40,000 left Ravi's account, and we did nothing."

If students cannot articulate their two errors in plain words, they cannot choose a metric. Everything after this depends on it.

**Note the lazy model in matrix form:** TP = 0, FP = 0, FN = 500, TN = 9,500. Every error is stacked in one box. Accuracy hid it. The matrix cannot.

---

## Practical Block 1: Build the Imbalanced Data, Expose the Lie (15 min)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# --- A deliberately imbalanced "fraud" dataset: 95% legit, 5% fraud ---
X, y = make_classification(
    n_samples=5000,
    n_features=10,
    n_informative=5,
    n_redundant=2,
    weights=[0.95, 0.05],   # <-- this is the whole point
    class_sep=1.5,
    flip_y=0.01,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

print("Test set class counts:", np.bincount(y_test))
print("Fraud rate in test set:", round(y_test.mean(), 3))
```

Expect roughly 1,419 legitimate and 81 fraudulent transactions in the test set — about 5.4% fraud.

```python
# --- The lazy model: always predict "not fraud" ---
lazy_pred = np.zeros_like(y_test)
print("Lazy model accuracy:", round(accuracy_score(y_test, lazy_pred), 4))
```

This should print roughly **0.946**. Stop here. Let it land.

```python
# --- A real model, trained properly ---
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Trained model accuracy:", round(accuracy_score(y_test, y_pred), 4))

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion matrix:\n", cm)

tn, fp, fn, tp = cm.ravel()
print(f"\nTN (correctly ignored): {tn}")
print(f"FP (false alarms):      {fp}")
print(f"FN (frauds MISSED):     {fn}   <-- the expensive box")
print(f"TP (frauds caught):     {tp}")
```

The trained model lands around **0.966 accuracy** — only about two points above the lazy model. But the matrix shows it catches roughly 36 of the 81 frauds and misses about 45.

```python
ConfusionMatrixDisplay(cm, display_labels=["Legit", "Fraud"]).plot(cmap="Blues")
plt.title("Logistic Regression @ default threshold 0.5")
plt.show()
```

**Live walk-through:** Put the two accuracy numbers side by side on the board — lazy ≈ 0.946, trained ≈ 0.966. Say: *"We did all that work for two percentage points."* Then point at the FN cell. *"But look — this model misses more than half the frauds. Accuracy told you it was excellent. The matrix is telling you it is barely functional."* Ask the room: **"Which single number in this matrix would you take to your manager?"** Steer them towards FN. That question sets up Concept 2.

---

## Concept Block 2: Precision, Recall, F1, Specificity (10 min)

### The two questions (board)

```
precision = TP / (TP + FP)   "Of what I FLAGGED, how much was right?"
                             --> punished by FALSE ALARMS

recall    = TP / (TP + FN)   "Of what was REALLY there, how much did I CATCH?"
                             --> punished by MISSES
```

Teach the denominators, not the formulas. *Precision looks at your column of flags. Recall looks at the row of real positives.* Point at the 2×2 grid as you say it.

### Choosing between them

| Scenario | The expensive error | Optimise | Reasoning |
|---|---|---|---|
| Cancer screening | FN — missing a tumour | **Recall** | A false alarm costs one extra scan. A miss costs a life. |
| Spam filter | FP — binning a job offer | **Precision** | Users tolerate spam. They never forgive a lost email. |
| Fraud alerts | FN — letting fraud through | **Recall** | A blocked card annoys. Stolen money is gone. |
| Loan approval | FP — approving a defaulter | **Precision** | Every bad approval is a direct rupee loss. |

**The tradeoff is real and unavoidable.** Flag more aggressively → recall up, precision down. Flag conservatively → precision up, recall down. You cannot have both for free; you can only choose where to sit.

### F1 — the harmonic mean

```
F1 = 2 * (precision * recall) / (precision + recall)
```

Ask: *"Why not just average them?"* Then show why:

| Precision | Recall | Plain average | F1 |
|---|---|---|---|
| 1.00 | 0.02 | 0.51 — looks fine | **0.04** — correctly awful |
| 0.90 | 0.85 | 0.875 | **0.87** |

The harmonic mean is dragged towards the **smaller** number. It refuses to let a model hide a terrible recall behind a perfect precision. Use F1 when both errors genuinely matter and you need one number. Do *not* use it when one error clearly dominates — optimise that one and just report the other.

### Specificity

```
specificity = TN / (TN + FP)   "Of the genuine negatives, how many did I leave alone?"
```

Recall is also called **sensitivity**. Sensitivity and specificity are the medical world's pair — sensitivity catches the sick, specificity avoids terrifying the healthy.

---

## Practical Block 2: classification_report and Naming the Errors (15 min)

```python
from sklearn.metrics import (classification_report, precision_score,
                             recall_score, f1_score)

print(classification_report(
    y_test, y_pred,
    target_names=["Legit (0)", "Fraud (1)"],
    digits=3
))
```

Read the **Fraud** row out loud. Precision is high (around 0.88) — when it does flag something, it is usually right. Recall is low (around 0.44) — it catches under half the frauds. Note the `support` column: 81 frauds vs 1,419 legit. That column is where the imbalance becomes impossible to ignore.

```python
# --- Compute the same numbers by hand from the matrix, to demystify them ---
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

precision   = tp / (tp + fp)
recall      = tp / (tp + fn)
specificity = tn / (tn + fp)
f1          = 2 * precision * recall / (precision + recall)

print(f"Precision   : {precision:.3f}  (of flagged, this fraction was real fraud)")
print(f"Recall      : {recall:.3f}  (of real frauds, this fraction was caught)")
print(f"Specificity : {specificity:.3f}  (of legit txns, this fraction left alone)")
print(f"F1          : {f1:.3f}")

# Sanity check against sklearn
print("\nsklearn agrees:",
      round(precision_score(y_test, y_pred), 3),
      round(recall_score(y_test, y_pred), 3),
      round(f1_score(y_test, y_pred), 3))
```

```python
# --- Put a rupee value on each error box ---
COST_MISSED_FRAUD = 5000   # money gone
COST_FALSE_ALARM  = 500    # manual review + annoyed customer

total_cost = fn * COST_MISSED_FRAUD + fp * COST_FALSE_ALARM
print(f"\nMissed frauds : {fn} x Rs.5000 = Rs.{fn * COST_MISSED_FRAUD:,}")
print(f"False alarms  : {fp} x Rs.500  = Rs.{fp * COST_FALSE_ALARM:,}")
print(f"TOTAL COST at threshold 0.5   = Rs.{total_cost:,}")
```

At the default threshold this lands somewhere near ₹2,30,000 — and almost all of it is missed frauds.

**Live walk-through:** Point at the cost split. *"Ninety-eight percent of our loss is coming from one box — the misses. And what metric measures misses? Recall. So recall is our metric. We are not going to argue about it again."* Then ask the room the question that sets up the break: **"The model's recall is 0.44. We did not choose that number. So who did?"** Let them sit with it. The answer is: a hardcoded 0.5 that nobody thought about.

---

## BREAK (10 min)

*Mull this over: the model gave every transaction a fraud probability. Then something quietly turned those probabilities into yes/no answers using a cut-off of 0.5. Nobody in this room chose 0.5. What happens if we choose something else?*

---

## Concept Block 3: The Threshold Is a Dial, Not a Law (10 min)

### What `.predict()` is hiding

Write this on the board:

```
model.predict_proba(X)[:, 1]   -->  0.03, 0.71, 0.12, 0.48, 0.95, ...
                                    (the model's actual belief)

model.predict(X)               -->  0,    1,    0,    0,    1,    ...
                                    (probabilities silently cut at 0.5)
```

`.predict()` is not a separate model. It is `.predict_proba()` plus one hardcoded line: `if p >= 0.5: positive`.

**Ask the room:** *"Where did 0.5 come from? Was it derived from our data? From our cost of fraud? From anything at all about our problem?"* The answer is no. It is a library default. It is the single most unexamined number in machine learning.

### Moving the dial

Lowering the threshold to 0.2 means: *flag anything the model is even 20% suspicious of.*

| Threshold | Rows flagged | FN (misses) | FP (false alarms) | Recall | Precision |
|---|---|---|---|---|---|
| 0.10 | Many | Few | Many | **High** | Low |
| 0.50 | Default | Medium | Few | Medium | High |
| 0.90 | Very few | Many | Almost none | Low | **Very high** |

**Critical point to hammer:** moving the threshold **does not retrain the model**. The probabilities are frozen. The model's knowledge is unchanged. You are only choosing where to draw the line — which means you can tune your model's behaviour to the business *after* training, in one line, for free.

### The threshold analysis workflow

```
1. Get probabilities:    proba = model.predict_proba(X_test)[:, 1]
2. Sweep thresholds:     for t in 0.05 ... 0.95
3. At each t:            preds = (proba >= t); record precision, recall, FN, FP
4. Apply your rule:      "recall must be >= 0.90"  OR  "minimise total rupee cost"
5. Pick t. Justify it in a sentence a manager understands.
```

Step 4 is not a machine learning decision. It is a business decision. That is the whole point.

---

## Practical Block 3: Sweep the Threshold, Walk the Tradeoff (15 min)

```python
# --- The probabilities that .predict() was hiding from us ---
proba = model.predict_proba(X_test)[:, 1]

print("First 10 fraud probabilities:", np.round(proba[:10], 3))
print("Highest probability in test set:", round(proba.max(), 3))
```

```python
# --- Sweep the threshold and record what happens ---
rows = []
for t in [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]:
    preds = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
    rows.append({
        "threshold": t,
        "flagged": tp + fp,
        "TP": tp, "FP": fp, "FN": fn,
        "precision": round(precision_score(y_test, preds, zero_division=0), 3),
        "recall": round(recall_score(y_test, preds), 3),
        "f1": round(f1_score(y_test, preds, zero_division=0), 3),
    })

sweep = pd.DataFrame(rows)
print(sweep.to_string(index=False))
```

The shape to expect: as the threshold falls from 0.90 down to 0.05, **recall climbs steadily** (from under 0.10 up to roughly 0.89) while **precision collapses** (from around 0.90 down to roughly 0.22). FN drains out of the miss box and FP fills up the false-alarm box. Same model. Same probabilities. Completely different behaviour.

```python
# --- Plot the tradeoff ---
plt.figure(figsize=(9, 5))
plt.plot(sweep["threshold"], sweep["precision"], "o-", label="Precision", lw=2)
plt.plot(sweep["threshold"], sweep["recall"], "s-", label="Recall", lw=2)
plt.plot(sweep["threshold"], sweep["f1"], "^--", label="F1", lw=1.5, alpha=0.7)
plt.axvline(0.5, color="grey", ls=":", label="Default 0.5 (chosen by nobody)")
plt.xlabel("Decision threshold")
plt.ylabel("Score")
plt.title("One model, eleven personalities — the precision-recall tradeoff")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
```

```python
# --- Apply a business rule: "we must catch at least 80% of frauds" ---
target_recall = 0.80
ok = sweep[sweep["recall"] >= target_recall]
print(f"Thresholds that hit recall >= {target_recall}:")
print(ok.to_string(index=False))
print("\nOf those, the one with the best precision:")
print(ok.loc[ok["precision"].idxmax()])
```

**Live walk-through:** Point at the two crossing lines. *"The default threshold put us here, at recall 0.44. Nobody chose that. If the business says 'catch 80% of frauds', we just read the answer off this table — around 0.10 — and we did not retrain anything."* Then ask: **"What did that recall cost us? Look at the FP column."** They will see false alarms jump from about 5 to over 140. That honest tradeoff is the lesson.

---

## Concept Block 4: ROC-AUC vs the Precision–Recall Curve (10 min)

### The problem with the sweep table

The table above is the model at eleven thresholds. What if you want to judge the model at **every** threshold at once — and compare two models before choosing any operating point?

### The ROC curve

Plot, as the threshold slides from 1 down to 0:

```
y-axis: TPR (True Positive Rate)  = TP / (TP + FN)   <-- this is just RECALL
x-axis: FPR (False Positive Rate) = FP / (FP + TN)   <-- share of legit rows wrongly flagged
```

- Top-left corner = perfect: full recall, zero false alarms
- The diagonal = random guessing
- **ROC-AUC** = area under that curve

| ROC-AUC | Meaning |
|---|---|
| 1.00 | Perfect ranking — every fraud scores above every legit row |
| 0.90 | A random fraud outranks a random legit row 90% of the time |
| 0.50 | Coin flip. The model learnt nothing. |

AUC is **threshold-independent**. It does not ask "how good is your cut-off?" — it asks "does the model *rank* the rows well?" That makes it the right tool for comparing two models.

### Where ROC lies to you

Look hard at the FPR denominator: `FP / (FP + TN)`.

**TN is in there.** On our data, TN is around 1,400. So 140 false alarms move FPR by only 0.1 — barely a wobble on the plot. On heavily imbalanced data, ROC curves flatter every model.

### The precision–recall curve

```
y-axis: Precision = TP / (TP + FP)
x-axis: Recall    = TP / (TP + FN)
```

**There is no TN anywhere in that curve.** The vast, boring majority class cannot inflate your score. Every false alarm hits precision immediately.

| | ROC curve | Precision–Recall curve |
|---|---|---|
| Uses TN? | Yes (in FPR) | **No** |
| Baseline for a random model | Diagonal, AUC = 0.5 | A flat line at the positive-class rate |
| On balanced data | Excellent | Fine |
| On rare positives | **Over-optimistic** | **Honest — use this one** |

**The rule:** balanced classes → ROC is fine. Rare positive class → trust the PR curve.

---

## Practical Block 4: Curves, AUC, and a Threshold Chosen by Cost (10 min)

```python
from sklearn.metrics import (roc_curve, roc_auc_score,
                             precision_recall_curve, average_precision_score)
from sklearn.ensemble import RandomForestClassifier

# Train a second model so we have something to compare against
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
proba_rf = rf.predict_proba(X_test)[:, 1]

print("Logistic Regression  ROC-AUC:", round(roc_auc_score(y_test, proba), 3))
print("Random Forest        ROC-AUC:", round(roc_auc_score(y_test, proba_rf), 3))
print()
print("Logistic Regression  PR-AUC :", round(average_precision_score(y_test, proba), 3))
print("Random Forest        PR-AUC :", round(average_precision_score(y_test, proba_rf), 3))
```

Expect the ROC-AUCs to look close (both in the 0.91–0.95 range) while the PR-AUCs are **far apart** (roughly 0.67 vs 0.87). That gap is the entire lesson of Concept 4 — do not skip past it.

```python
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# --- ROC curves ---
for name, p in [("Logistic Regression", proba), ("Random Forest", proba_rf)]:
    fpr, tpr, _ = roc_curve(y_test, p)
    axes[0].plot(fpr, tpr, lw=2, label=f"{name} (AUC={roc_auc_score(y_test, p):.3f})")
axes[0].plot([0, 1], [0, 1], "k--", lw=1, label="Random guessing")
axes[0].set_xlabel("False Positive Rate")
axes[0].set_ylabel("True Positive Rate (Recall)")
axes[0].set_title("ROC — both models look great")
axes[0].legend(); axes[0].grid(alpha=0.3)

# --- Precision-Recall curves ---
for name, p in [("Logistic Regression", proba), ("Random Forest", proba_rf)]:
    pr, rc, _ = precision_recall_curve(y_test, p)
    axes[1].plot(rc, pr, lw=2, label=f"{name} (AP={average_precision_score(y_test, p):.3f})")
axes[1].axhline(y_test.mean(), color="k", ls="--", lw=1,
                label=f"Random baseline = {y_test.mean():.3f}")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].set_title("Precision-Recall — the honest picture")
axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

```python
# --- Choose the operating threshold from BUSINESS COST, not from a metric ---
COST_MISSED_FRAUD = 5000   # rupees lost per fraud we let through
COST_FALSE_ALARM  = 500    # rupees per manual review of an honest customer

thresholds = np.arange(0.02, 0.99, 0.01)
costs = []
for t in thresholds:
    preds = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
    costs.append(fn * COST_MISSED_FRAUD + fp * COST_FALSE_ALARM)

costs = np.array(costs)
best_t = thresholds[costs.argmin()]
cost_at_default = costs[np.argmin(np.abs(thresholds - 0.5))]

print(f"Cost at default threshold 0.50 : Rs.{cost_at_default:,}")
print(f"Best threshold                 : {best_t:.2f}")
print(f"Cost at best threshold         : Rs.{costs.min():,}")
print(f"Saving, purely from moving one number: Rs.{cost_at_default - costs.min():,}")

plt.figure(figsize=(9, 4))
plt.plot(thresholds, costs, lw=2)
plt.axvline(best_t, color="green", ls="--", label=f"Best = {best_t:.2f}")
plt.axvline(0.50, color="red", ls=":", label="Default = 0.50")
plt.xlabel("Threshold"); plt.ylabel("Total cost (Rs.)")
plt.title("The threshold is a business decision")
plt.legend(); plt.grid(alpha=0.3)
plt.show()
```

The optimum should land low — somewhere near **0.14** — because a missed fraud costs ten times a false alarm, so the model should be told to be far more suspicious than 0.5 allows. The saving versus the default is large, roughly half the total cost.

**Live walk-through:** Point at the green line. *"We did not collect more data. We did not tune a hyperparameter. We did not retrain anything. We changed one number from 0.5 to 0.14 and cut the company's losses roughly in half. This is the highest-return line of code in the whole module."*

---

## Summary & Wrap-Up (5 min)

**The spine of this session:**

1. **Accuracy lies on imbalanced data.** A model that predicts "not fraud" forever scored 94.6%. Never report accuracy alone again.
2. **The confusion matrix splits your errors into FP and FN.** Name them in plain English, as sentences about a real person, before you pick a metric.
3. **Precision punishes false alarms; recall punishes misses.** Choose based on which error costs more. F1 only when both matter equally.
4. **`.predict()` hides `predict_proba()` and a hardcoded 0.5.** That 0.5 was chosen by nobody. Moving it retrains nothing and changes everything.
5. **ROC-AUC judges ranking at every threshold** — but on rare positives it flatters. The precision–recall curve has no TN in it, so it tells the truth.
6. **The final threshold is a business decision**, justified in rupees, not in metrics.

**Bridge:** *"Everything for the last three sessions has depended on one luxury: labels. We knew which transactions were fraud, so we could count our mistakes. Next session — **Unsupervised Learning: Clustering** — the labels vanish. You get raw data and no answer key, and you have to find the structure anyway. There is no confusion matrix waiting for you there."*

---

## Q&A & Doubt Solving (5 min)

**Q: If I move the threshold, am I cheating? Am I just tuning until the numbers look good?**
→ No — as long as you choose the threshold using a rule fixed *in advance* ("catch 80% of frauds", "minimise rupee cost") and you select it on validation data, not the final test set. Cheating would be trying twenty thresholds on the test set and reporting the best one. Choosing an operating point from a stated business requirement is the job.

**Q: Should I fix imbalance with `class_weight='balanced'` instead of moving the threshold?**
→ They are different tools that often reach a similar place. `class_weight='balanced'` changes the *training* objective, so the model itself is penalised more for missing the rare class. Threshold moving changes only the *decision* after training. Threshold tuning is cheaper, reversible, and lets one model serve several business rules at once. In practice people do both and compare.

**Q: My ROC-AUC is 0.93 but my precision is 0.22. How can both be true?**
→ Perfectly consistent, and it is the classic imbalanced-data signature. AUC 0.93 says the model *ranks* well — frauds generally score above legit rows. Precision 0.22 says that at your chosen threshold, you are flagging far more rows than there are frauds. Good ranking, bad operating point. Fix it with the threshold, not with a new model.

**Q: Which class does sklearn treat as "positive"?**
→ The one with the higher label value — so class `1`, by default, in a 0/1 problem. This is why you must encode the interesting, rare class as `1`. If you label fraud as `0`, every precision and recall number you print will be about legitimate transactions, and you will draw exactly the wrong conclusion.

**Q: What if the classes are balanced? Do I still need all this?**
→ You still need the confusion matrix, because FP and FN almost never cost the same even when they are equally common. But accuracy becomes a defensible headline number again, and ROC-AUC becomes reliable. The threshold discipline still applies — 0.5 is still just a default.

---

## Instructor Notes

- **No installs needed** beyond the standard stack: `scikit-learn`, `pandas`, `numpy`, `matplotlib`. Everything is generated with `make_classification`, so nothing depends on a download.
- **Do not change the `make_classification` parameters.** `weights=[0.95, 0.05]` with `class_sep=1.5` and `random_state=42` is tuned so that the lazy model gets ~94.6%, the trained model gets ~96.6% with recall only ~0.44 (the paradox lands hard), *and* the ROC/PR curves are still well-shaped. Raise `class_sep` and the paradox dissolves; lower it and the curves become ugly.
- **The exact numbers will vary slightly** across sklearn versions. Never promise a specific figure to the room — write the print statements and read the output live. The *shape* of the result is what matters, and that is stable.
- **The single most common student mistake:** reporting `accuracy_score` on imbalanced data and declaring victory. Pre-empt it by making the lazy-model demo the very first thing they run in Practical 1, before they see any real model. Once they have personally printed 0.946 for a model that is literally `np.zeros()`, they never fully trust accuracy again — which is exactly the reflex you want.
- **The second most common mistake:** believing that moving the threshold retrains the model. Say "the probabilities did not change" out loud at least three times during Practical 3, while pointing at the same `proba` array.
- **Pacing:** Practical 4 is the tightest block. If you are running behind, cut the Random Forest comparison and plot only the logistic regression curves — but *never* cut the cost-based threshold selection at the end. That is the takeaway the whole session is built towards.
