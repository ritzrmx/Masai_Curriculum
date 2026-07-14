# Coding Problem: Classification Metrics & Threshold Analysis
> **Session 8 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A fraud model has already scored 20 UPI transactions. You are given the **true labels**
(`1` = fraud, `0` = legitimate) and the **fraud probability** the model assigned to each one.
No training needed — your job is only to evaluate.

```python
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# 20 transactions. Only 5 are actually fraud (an imbalanced problem).
y_true = np.array([0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
                   1, 0, 0, 1, 0, 0, 1, 0, 0, 0])

# What the model believes: P(fraud) for each transaction
y_proba = np.array([0.05, 0.12, 0.31, 0.08, 0.72, 0.44, 0.02, 0.38, 0.19, 0.55,
                    0.91, 0.07, 0.26, 0.41, 0.15, 0.03, 0.63, 0.22, 0.09, 0.34])
```

---

## Tasks

**Task 1 — Basic**
Convert `y_proba` into predictions using the **default threshold of 0.5** (flag as fraud if probability ≥ 0.5). Print the **confusion matrix** and the **accuracy**.

**Task 2 — Basic**
Print the **classification report** with `target_names=["Legit", "Fraud"]`. Read off the precision and recall for the **Fraud** class.

**Task 3 — Mid**
Re-threshold at **0.35** instead of 0.5. Print the new confusion matrix and the new recall for the Fraud class. Then print **which of the two error boxes (FP or FN) went down**, and by how many.

---

## Expected Output

```
=== Threshold 0.5 (the default) ===
[[14  1]
 [ 2  3]]
Accuracy: 0.85

              precision    recall  f1-score   support

       Legit       0.88      0.93      0.90        15
       Fraud       0.75      0.60      0.67         5

    accuracy                           0.85        20
   macro avg       0.81      0.77      0.78        20
weighted avg       0.84      0.85      0.84        20

=== Threshold 0.35 ===
[[13  2]
 [ 0  5]]
Fraud recall: 0.60 -> 1.00
Missed frauds (FN): 2 -> 0   (we now catch every fraud)
False alarms (FP):  1 -> 2   (the price we paid)
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
from sklearn.metrics import (confusion_matrix, classification_report,
                             accuracy_score, recall_score)

y_true = np.array([0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
                   1, 0, 0, 1, 0, 0, 1, 0, 0, 0])

y_proba = np.array([0.05, 0.12, 0.31, 0.08, 0.72, 0.44, 0.02, 0.38, 0.19, 0.55,
                    0.91, 0.07, 0.26, 0.41, 0.15, 0.03, 0.63, 0.22, 0.09, 0.34])

# --- Task 1: default threshold 0.5 ---
pred_50 = (y_proba >= 0.5).astype(int)
cm_50 = confusion_matrix(y_true, pred_50)

print("=== Threshold 0.5 (the default) ===")
print(cm_50)
print("Accuracy:", round(accuracy_score(y_true, pred_50), 2))

# --- Task 2: the full report ---
print()
print(classification_report(y_true, pred_50, target_names=["Legit", "Fraud"]))

# --- Task 3: slide the threshold down to 0.35 ---
pred_35 = (y_proba >= 0.35).astype(int)
cm_35 = confusion_matrix(y_true, pred_35)

print("=== Threshold 0.35 ===")
print(cm_35)

tn_50, fp_50, fn_50, tp_50 = cm_50.ravel()
tn_35, fp_35, fn_35, tp_35 = cm_35.ravel()

rec_50 = recall_score(y_true, pred_50)
rec_35 = recall_score(y_true, pred_35)

print(f"Fraud recall: {rec_50:.2f} -> {rec_35:.2f}")
print(f"Missed frauds (FN): {fn_50} -> {fn_35}   (we now catch every fraud)")
print(f"False alarms (FP):  {fp_50} -> {fp_35}   (the price we paid)")
```

**The point:** the model never changed. `y_proba` is identical in both cases. Lowering the
cut-off from 0.5 to 0.35 pushed recall from 0.60 to 1.00 — every fraud caught — at the cost
of exactly one extra false alarm. That trade is the entire job.

</details>
