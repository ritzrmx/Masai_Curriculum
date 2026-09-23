# Coding Problem: Random Forests & Ensemble Methods
> **Session 10 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Train a `RandomForestClassifier`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.DataFrame({
    "income_k": [25, 40, 60, 30, 80, 45, 90, 35, 70, 50],
    "credit_score": [590, 640, 720, 600, 780, 650, 800, 610, 750, 660],
    "approved": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
})
X = df[["income_k", "credit_score"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = ___(n_estimators=___, max_depth=___, random_state=42)
model.fit(___, ___)
```

**Task 2 — Basic**

Report accuracy and print feature importances:

```python
accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.3f}")

for name, score in sorted(zip(X.columns, model.feature_importances_), key=lambda t: -t[1]):
    print(f"{name}: {score:.4f}")
```

**Task 3 — Mid**

Compare against a single tree, then save and reload the model with `joblib`:

```python
from sklearn.tree import DecisionTreeClassifier
import joblib

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
print("Tree test accuracy:", tree.score(X_test, y_test))
print("Forest test accuracy:", model.score(X_test, y_test))

joblib.dump(model, "loan_rf_model.joblib")
loaded = joblib.load("loan_rf_model.joblib")
print("Predictions match:", (model.predict(X_test) == loaded.predict(X_test)).all())
```

---

## Expected Output

```
Test accuracy: ...
income_k: ...
credit_score: ...
Tree test accuracy: ...
Forest test accuracy: ...
Predictions match: True
```

*(Exact numbers depend on the fitted model on this toy dataset — values will be printed, not fixed constants.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.DataFrame({
    "income_k": [25, 40, 60, 30, 80, 45, 90, 35, 70, 50],
    "credit_score": [590, 640, 720, 600, 780, 650, 800, 610, 750, 660],
    "approved": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
})
X = df[["income_k", "credit_score"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.3f}")

for name, score in sorted(zip(X.columns, model.feature_importances_), key=lambda t: -t[1]):
    print(f"{name}: {score:.4f}")

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
print("Tree test accuracy:", tree.score(X_test, y_test))
print("Forest test accuracy:", model.score(X_test, y_test))

joblib.dump(model, "loan_rf_model.joblib")
loaded = joblib.load("loan_rf_model.joblib")
print("Predictions match:", (model.predict(X_test) == loaded.predict(X_test)).all())
```
</details>
