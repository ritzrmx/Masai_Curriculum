# Coding Problem: Model Selection, Persistence & Module Review
> **Session 12 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A self-contained synthetic binary classification dataset (no internet, fully reproducible):

```python
import pandas as pd
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=300, n_features=6, n_informative=4,
    n_redundant=0, random_state=42
)
X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(1, 7)])
y = pd.Series(y, name="target")
```

---

## Tasks

**Task 1 — Basic**
Split the data (`test_size=0.25`, `random_state=42`, `stratify=y`). Train a `LogisticRegression(random_state=42)` and a `DecisionTreeClassifier(max_depth=3, random_state=42)` on the training set.

**Task 2 — Basic**
Compare both models on the test set using **Accuracy** and **F1**. Print the results as a small table (rounded to 4 decimals).

**Task 3 — Mid**
Pick the model with the higher F1 score as the "winner." Save it with `joblib.dump`, reload it with `joblib.load`, and print whether the reloaded model's predictions on the test set are **identical** to the original model's predictions.

---

## Expected Output

```
Model comparison:
                    Accuracy      F1
Model
LogisticRegression    0.7733  0.7733
DecisionTree          0.7867  0.8049

Winner: DecisionTree
Reloaded predictions identical: True
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import numpy as np
import joblib
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

# Dataset
X, y = make_classification(
    n_samples=300, n_features=6, n_informative=4,
    n_redundant=0, random_state=42
)
X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(1, 7)])
y = pd.Series(y, name="target")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Task 1: train two models
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train, y_train)
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

# Task 2: compare accuracy + F1
log_preds = log_reg.predict(X_test)
tree_preds = tree.predict(X_test)

results = pd.DataFrame({
    "Model": ["LogisticRegression", "DecisionTree"],
    "Accuracy": [accuracy_score(y_test, log_preds), accuracy_score(y_test, tree_preds)],
    "F1": [f1_score(y_test, log_preds), f1_score(y_test, tree_preds)],
}).set_index("Model").round(4)
print("Model comparison:")
print(results)

# Task 3: persist winner, reload, confirm identical predictions
winner_name = results["F1"].idxmax()
print(f"\nWinner: {winner_name}")
winner_model = log_reg if winner_name == "LogisticRegression" else tree

joblib.dump(winner_model, "/tmp/winner_model.joblib")
reloaded = joblib.load("/tmp/winner_model.joblib")

original_preds = winner_model.predict(X_test)
reloaded_preds = reloaded.predict(X_test)
print("Reloaded predictions identical:", np.array_equal(original_preds, reloaded_preds))
```

</details>
