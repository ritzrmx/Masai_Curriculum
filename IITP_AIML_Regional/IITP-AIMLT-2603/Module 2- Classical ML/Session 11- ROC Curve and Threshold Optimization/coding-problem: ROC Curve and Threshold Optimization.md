# Coding Problem: ROC Curve and Threshold Optimization

> **Session 11** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You are comparing two disease screening models. One has higher accuracy, the other catches more actual cases. You'll use the ROC curve and AUC score to evaluate and compare them — and tune the threshold for the better one.

---

## Setup

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, classification_report

X, y = make_classification(n_samples=300, n_features=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```

---

## Tasks

**Task 1 — Train Two Models**

```python
lr  = LogisticRegression(random_state=42)
dt  = DecisionTreeClassifier(max_depth=3, random_state=42)

lr.fit(___, ___)    # fill: X_train, y_train
dt.fit(___, ___)    # fill: X_train, y_train

# Get probability scores (not class labels)
lr_proba = lr.predict_proba(X_test)[:, ___]    # fill: 1
dt_proba = dt.predict_proba(X_test)[:, ___]    # fill: 1
```

---

**Task 2 — AUC Score**

AUC (Area Under Curve) measures how well the model separates classes. 0.5 = random, 1.0 = perfect.

```python
lr_auc = roc_auc_score(___, ___)    # fill: y_test, lr_proba
dt_auc = roc_auc_score(___, ___)    # fill: y_test, dt_proba

print(f"Logistic Regression AUC: {lr_auc:.3f}")
print(f"Decision Tree AUC:       {dt_auc:.3f}")
# Which model is better at ranking/separating?
```

---

**Task 3 — Plot the ROC Curve**

```python
lr_fpr, lr_tpr, _ = roc_curve(y_test, ___)    # fill: lr_proba
dt_fpr, dt_tpr, _ = roc_curve(y_test, ___)    # fill: dt_proba

plt.figure(figsize=(7, 5))
plt.plot(lr_fpr, lr_tpr, label=f"Logistic Regression (AUC={lr_auc:.2f})", color="steelblue")
plt.plot(dt_fpr, dt_tpr, label=f"Decision Tree (AUC={dt_auc:.2f})", color="orange")
plt.plot([0,1], [0,1], "k--", label="Random (AUC=0.5)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate (Recall)")
plt.title("ROC Curve Comparison")
plt.legend()
plt.show()
```

---

**Task 4 — Threshold Tuning**

The default threshold is 0.5. For disease screening, we want high recall (catch all cases).

```python
lr_fpr_arr, lr_tpr_arr, thresholds = roc_curve(y_test, lr_proba)

# Find the threshold where TPR >= 0.90
for fpr, tpr, thresh in zip(lr_fpr_arr, lr_tpr_arr, thresholds):
    if tpr >= ___:                          # fill: 0.90
        print(f"Threshold: {thresh:.3f}, TPR: {tpr:.3f}, FPR: {fpr:.3f}")
        best_thresh = thresh
        break

# Apply the new threshold
y_pred_tuned = (lr_proba >= ___).astype(int)    # fill: best_thresh
print(classification_report(y_test, y_pred_tuned))
```

---

## Key Takeaways

- **ROC curve** shows the trade-off between catching true positives and triggering false alarms across all thresholds
- **AUC** is a single score comparing models: closer to 1.0 is better
- Lower threshold → higher recall, lower precision — tune based on business cost of each error type
