# Coding Problem: Classification Metrics
> **Session 7 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Compute a confusion matrix on `transactions.csv`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

df = pd.read_csv("transactions.csv")
X = df[["amount", "hour_of_day"]]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(___, ___)
print(cm)
```

**Task 2 — Basic**

Compute precision, recall, and F1:

```python
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print(f"Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")
```

**Task 3 — Mid**

Print a full classification report and manually verify precision from the confusion matrix cells:

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

tn, fp, fn, tp = cm.ravel()
manual_precision = tp / (tp + fp)
print(f"Manual precision check: {manual_precision:.3f}")
```

---

## Expected Output

```
[[...]
 [...]]
Precision: ..., Recall: ..., F1: ...
              precision    recall  f1-score   support
...
Manual precision check: ...
```

*(Exact values depend on the fitted model on this dataset and split.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, classification_report

df = pd.read_csv("transactions.csv")
X = df[["amount", "hour_of_day"]]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(cm)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print(f"Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")

print(classification_report(y_test, y_pred))

tn, fp, fn, tp = cm.ravel()
manual_precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
print(f"Manual precision check: {manual_precision:.3f}")
```
</details>
