# Coding Problem: Decision Trees
> **Session 9 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Train a `DecisionTreeClassifier`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.DataFrame({
    "income_k": [25, 40, 60, 30, 80, 45, 90, 35, 70, 50],
    "credit_score": [590, 640, 720, 600, 780, 650, 800, 610, 750, 660],
    "approved": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
})
X = df[["income_k", "credit_score"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = ___(max_depth=___, random_state=42)
model.fit(___, ___)
```

**Task 2 — Basic**

Evaluate accuracy and print the tree as text:

```python
from sklearn.tree import export_text

preds = model.predict(X_test)
accuracy = (preds == y_test).mean()
print(f"Test accuracy: {accuracy:.3f}")

print(export_text(model, feature_names=list(X.columns)))
```

**Task 3 — Mid**

Compare train vs. test accuracy across a depth sweep, and predict on a new applicant:

```python
for depth in [1, 2, 3, None]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    print(depth, m.score(X_train, y_train), m.score(X_test, y_test))

new_applicant = pd.DataFrame({"income_k": [55], "credit_score": [700]})
print("Prediction:", model.predict(new_applicant))
```

---

## Expected Output

```
Test accuracy: ...
|--- ...
...

1 ... ...
2 ... ...
3 ... ...
None ... ...
Prediction: [...]
```

*(Exact numbers depend on the fitted model on this toy dataset — values will be printed, not fixed constants.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

df = pd.DataFrame({
    "income_k": [25, 40, 60, 30, 80, 45, 90, 35, 70, 50],
    "credit_score": [590, 640, 720, 600, 780, 650, 800, 610, 750, 660],
    "approved": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
})
X = df[["income_k", "credit_score"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
accuracy = (preds == y_test).mean()
print(f"Test accuracy: {accuracy:.3f}")

print(export_text(model, feature_names=list(X.columns)))

for depth in [1, 2, 3, None]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    print(depth, m.score(X_train, y_train), m.score(X_test, y_test))

new_applicant = pd.DataFrame({"income_k": [55], "credit_score": [700]})
print("Prediction:", model.predict(new_applicant))
```
</details>
