# Coding Problem: Data Preparation for ML
> **Session 2 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Build a `ColumnTransformer` for numeric and categorical columns:

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

df = pd.DataFrame({
    "age": [25, 40, 35, 50],
    "city": ["Pune", "Delhi", "Pune", "Mumbai"],
    "bought": [0, 1, 0, 1],
})
X = df.drop(columns=["bought"])
y = df["bought"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), ["___"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["___"]),
])
```

**Task 2 — Basic**

Wrap it in a `Pipeline` with a `LogisticRegression` and fit it:

```python
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipe = Pipeline(steps=[
    ("preprocessor", ___),
    ("model", ___()),
])
pipe.fit(X, y)
print("Fitted:", pipe.named_steps.keys())
```

**Task 3 — Mid**

Correctly split first, then evaluate with cross-validation on the *training* portion only (no leakage):

```python
from sklearn.model_selection import train_test_split, cross_val_score

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42
)
scores = cross_val_score(pipe, ___, ___, cv=2)
print(scores)
```

---

## Expected Output

```
dict_keys(['preprocessor', 'model'])
[... two CV scores ...]
```

*(Exact scores depend on the tiny toy dataset.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score

df = pd.DataFrame({
    "age": [25, 40, 35, 50],
    "city": ["Pune", "Delhi", "Pune", "Mumbai"],
    "bought": [0, 1, 0, 1],
})
X = df.drop(columns=["bought"])
y = df["bought"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), ["age"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])

pipe = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression()),
])
pipe.fit(X, y)
print("Fitted:", pipe.named_steps.keys())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42
)
scores = cross_val_score(pipe, X_train, y_train, cv=2)
print(scores)
```
</details>
