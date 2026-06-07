# Coding Problem: Model Selection and End-to-End Pipeline

> **Session 16** | ⏱ 15 mins | Module 2: Classical ML

---

## Scenario

You are wrapping up a classification project. You'll compare multiple models, tune the best one with Grid Search, and bundle everything into a single sklearn Pipeline — ready for production.

---

## Setup

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

---

## Tasks

**Task 1 — Compare Multiple Models**

```python
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree":       DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
}

results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=___, scoring="f1")  # fill: 5
    results[name] = {"Mean F1": round(scores.mean(), 3), "Std": round(scores.std(), 3)}

print(pd.DataFrame(results).T.sort_values("Mean F1", ascending=False))
# Which model has the best mean F1 with lowest variance?
```

---

**Task 2 — Grid Search on Best Model**

```python
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth":    [3, 5, None],
    "min_samples_split": [2, 5]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    rf,
    param_grid,
    cv=___,              # fill: 5
    scoring="f1",
    n_jobs=-1
)
grid_search.fit(___, ___)    # fill: X_train, y_train

print("Best params:", grid_search.___)        # fill: best_params_
print("Best CV F1:", round(grid_search.___, 3))  # fill: best_score_
```

---

**Task 3 — Build a Pipeline**

A Pipeline chains preprocessing and modelling into one object — no risk of fitting the scaler on test data.

```python
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42))
])

pipeline.fit(___, ___)              # fill: X_train, y_train
y_pred = pipeline.predict(___)      # fill: X_test

print(classification_report(y_test, y_pred, target_names=data.target_names))
```

---

**Task 4 — Grid Search on the Pipeline**

You can tune pipeline steps using `stepname__param` syntax.

```python
pipe_params = {
    "classifier__C":        [0.01, 0.1, 1.0, 10.0],   # Regularization strength
    "classifier__max_iter": [200, 500, 1000]
}

pipe_gs = GridSearchCV(pipeline, pipe_params, cv=5, scoring="f1")
pipe_gs.fit(___, ___)                   # fill: X_train, y_train

print("Best pipeline params:", pipe_gs.___)        # fill: best_params_
print("Best CV F1:", round(pipe_gs.___, 3))        # fill: best_score_
```

---

**Task 5 — Final Evaluation**

```python
best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)
y_final = best_model.predict(___)        # fill: X_test

print("=== Final Model Report ===")
print(classification_report(y_test, y_final, target_names=data.target_names))

# Simplicity vs performance decision:
# If Logistic Regression F1 = 0.96 and Random Forest F1 = 0.97
# Which would you choose for production? Why?
```

---

## Key Takeaways

- Compare models with **cross-validation** before committing — single split results can mislead
- **Grid Search** exhaustively tries all parameter combinations; always validate on held-out test data after
- **Pipelines** prevent data leakage and make deployment simple — fit once, predict anywhere
