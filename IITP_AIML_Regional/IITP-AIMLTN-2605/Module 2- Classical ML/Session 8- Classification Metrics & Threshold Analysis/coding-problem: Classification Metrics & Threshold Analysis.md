# Coding Problem: Classification Metrics & Threshold Analysis
> **Session 8 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

12 patients screened for a disease. `y_true` is the actual outcome (1 = disease, 0 = healthy); `y_prob` is the model's predicted probability of disease for each patient:

```python
import numpy as np

y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1])
y_prob = np.array([0.82, 0.15, 0.40, 0.65, 0.30, 0.10, 0.55, 0.05, 0.45, 0.70, 0.20, 0.35])
```

---

## Tasks

**Task 1 — Basic**
Convert `y_prob` to hard labels using a threshold of **0.5**, then print the **confusion matrix** (rows = actual, columns = predicted) and the individual **TN, FP, FN, TP** counts.

**Task 2 — Basic**
Using the threshold-0.5 predictions, compute and print **precision**, **recall**, and **F1-score** (each rounded to 3 decimals).

**Task 3 — Mid**
Compute and print the **ROC-AUC score** using the raw `y_prob` values (not the hard labels) — rounded to 3 decimals.

**Task 4 — Stretch**
Lower the threshold to **0.3**, recompute **precision** and **recall**, and print both (rounded to 3 decimals). This is a disease screen — comment in your code on which threshold (0.5 or 0.3) you would recommend and why.

---

## Expected Output

```
Predicted labels: [1 0 0 1 0 0 1 0 0 1 0 0]
Confusion matrix (rows=actual, cols=predicted):
[[6 0]
 [2 4]]
TN=6 FP=0 FN=2 TP=4

Precision: 1.000
Recall: 0.667
F1-score: 0.800

ROC-AUC: 0.944

Threshold 0.3 -> Precision: 0.750, Recall: 1.000
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score

y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1])
y_prob = np.array([0.82, 0.15, 0.40, 0.65, 0.30, 0.10, 0.55, 0.05, 0.45, 0.70, 0.20, 0.35])

# Task 1: threshold at 0.5, build confusion matrix
y_pred = (y_prob >= 0.5).astype(int)
print("Predicted labels:", y_pred)

cm = confusion_matrix(y_true, y_pred)
print("Confusion matrix (rows=actual, cols=predicted):")
print(cm)

tn, fp, fn, tp = cm.ravel()
print(f"TN={tn} FP={fp} FN={fn} TP={tp}")

# Task 2: precision, recall, f1
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
print(f"\nPrecision: {prec:.3f}")
print(f"Recall: {rec:.3f}")
print(f"F1-score: {f1:.3f}")

# Task 3: ROC-AUC from raw probabilities
auc = roc_auc_score(y_true, y_prob)
print(f"\nROC-AUC: {auc:.3f}")

# Task 4: lower the threshold to 0.3 and recheck precision/recall
y_pred_03 = (y_prob >= 0.3).astype(int)
prec_03 = precision_score(y_true, y_pred_03)
rec_03 = recall_score(y_true, y_pred_03)
print(f"\nThreshold 0.3 -> Precision: {prec_03:.3f}, Recall: {rec_03:.3f}")
# For a disease screen, missing a real case (FN) is costlier than a false alarm (FP),
# so the lower threshold (0.3) is preferable here -- it catches every true case (recall=1.000)
# at an acceptable precision cost (0.750).
```

</details>
