# Coding Problem: Logistic Regression for Classification

> **Session 8** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You are building a model to predict whether a student will pass or fail an exam based on their study hours and attendance. Logistic Regression outputs a **probability** — you then decide the threshold for Pass/Fail.

---

## Setup

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

np.random.seed(0)
n = 80
study_hours  = np.random.uniform(1, 10, n)
attendance   = np.random.uniform(40, 100, n)
passed       = ((study_hours * 5 + attendance * 0.3 + np.random.randn(n)*5) > 50).astype(int)

df = pd.DataFrame({"study_hours": study_hours, "attendance": attendance, "passed": passed})
print(df["passed"].value_counts())
```

---

## Tasks

**Task 1 — Split and Scale**

```python
X = df[["study_hours", "attendance"]]
y = df["___"]                                      # fill: passed

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.___(X_train)                    # fill: fit_transform
X_test_s  = scaler.___(X_test)                     # fill: transform
```

---

**Task 2 — Train Logistic Regression**

```python
model = LogisticRegression(random_state=42)
model.fit(___, ___)                                # fill: X_train_s, y_train

y_pred = model.predict(___)                        # fill: X_test_s
print("Accuracy:", accuracy_score(___, ___))       # fill: y_test, y_pred
```

---

**Task 3 — Probability Outputs**

Logistic Regression doesn't just predict 0 or 1 — it outputs a **probability score** first.

```python
# Get probabilities for each class [prob_fail, prob_pass]
proba = model.predict_proba(___)                   # fill: X_test_s

prob_pass = proba[:, ___]                          # fill: 1 (index for pass)

print("First 5 probability scores (passing):")
print(prob_pass[:5].round(3))

# The default threshold is 0.5 — anything above is predicted as Pass
```

---

**Task 4 — Change the Threshold**

Lower the threshold to 0.3 (catch more at-risk students earlier).

```python
threshold = ___                                    # fill: 0.3
y_pred_custom = (prob_pass >= threshold).astype(int)

print("With threshold 0.3:")
print(classification_report(y_test, y_pred_custom, target_names=["Fail", "Pass"]))

print("With default threshold 0.5:")
print(classification_report(y_test, y_pred, target_names=["Fail", "Pass"]))
```

> Which threshold catches more failing students? What's the trade-off?

---

**Task 5 — Predict a New Student**

```python
new_student = scaler.transform([[___, ___]])       # fill: 6 study hours, 75% attendance
prob = model.predict_proba(new_student)[0][1]
print(f"Pass probability: {prob:.1%}")
print(f"Prediction (threshold=0.5): {'Pass' if prob >= 0.5 else 'Fail'}")
```

---

## Key Takeaways

- Logistic Regression outputs a **probability** (0–1), then a threshold converts it to a class
- Lower threshold → catches more positives (but also more false alarms)
- Always scale features before logistic regression — it's a distance-based model
