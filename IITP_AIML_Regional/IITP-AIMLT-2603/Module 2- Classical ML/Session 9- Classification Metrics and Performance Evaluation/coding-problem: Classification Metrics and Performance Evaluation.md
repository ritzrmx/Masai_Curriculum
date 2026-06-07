# Coding Problem: Classification Metrics and Performance Evaluation

> **Session 9** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You've built a fraud detection model. The dataset is imbalanced — most transactions are legitimate. You'll see why accuracy alone is misleading, and learn to use the confusion matrix, precision, recall, and F1-score.

---

## Setup

```python
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

# Actual labels: 1 = fraud, 0 = legitimate
y_true = np.array([0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1])
y_pred = np.array([0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1])
# Model missed 2 out of 4 fraud cases
```

---

## Tasks

**Task 1 — Confusion Matrix**

```python
cm = confusion_matrix(___, ___)    # fill: y_true, y_pred
print("Confusion Matrix:")
print(cm)

# Label the cells:
tn, fp, fn, tp = cm.ravel()
print(f"\nTrue Negatives (correct non-fraud): {___}")   # fill: tn
print(f"False Positives (flagged wrongly):   {___}")   # fill: fp
print(f"False Negatives (missed fraud!):     {___}")   # fill: fn
print(f"True Positives (caught fraud):       {___}")   # fill: tp
```

---

**Task 2 — Why Accuracy Misleads**

```python
acc = accuracy_score(___, ___)    # fill: y_true, y_pred
print(f"\nAccuracy: {acc:.0%}")

# A model that predicts 0 for EVERY transaction:
y_all_zero = np.zeros(len(y_true), dtype=int)
naive_acc  = accuracy_score(y_true, ___)    # fill: y_all_zero
print(f"Naive model accuracy: {naive_acc:.0%}")

# Which is higher? Does the naive model "find" any fraud?
```

---

**Task 3 — Precision, Recall, F1**

```python
precision = precision_score(___, ___)    # fill: y_true, y_pred
recall    = recall_score(___, ___)       # fill: y_true, y_pred
f1        = f1_score(___, ___)           # fill: y_true, y_pred

print(f"\nPrecision: {precision:.2f}  — of all flagged, how many are real fraud?")
print(f"Recall:    {recall:.2f}  — of all real fraud, how many did we catch?")
print(f"F1-Score:  {f1:.2f}  — balance of precision and recall")
```

---

**Task 4 — Full Report**

```python
print(classification_report(___, ___, target_names=["Legit", "Fraud"]))
# fill: y_true, y_pred
```

> Which class has lower recall? What is the business cost of missing fraud?

---

**Task 5 — Business Interpretation**

```python
# Which metric would you optimise for each scenario?
scenarios = {
    "Fraud detection (missing fraud is very costly)":     "___",  # precision / recall
    "Spam filter (wrongly blocking real email is costly)":"___",  # precision / recall
    "Cancer screening (must catch all cases)":            "___",  # precision / recall
}
for s, ans in scenarios.items():
    print(f"{s}: {ans}")
```

---

## Key Takeaways

- **Precision** = when you flag something, how often are you right?
- **Recall** = of all real positives, how many did you catch?
- **F1** = harmonic mean of precision and recall — use when both matter
- Accuracy is useless on imbalanced datasets — always check the confusion matrix
