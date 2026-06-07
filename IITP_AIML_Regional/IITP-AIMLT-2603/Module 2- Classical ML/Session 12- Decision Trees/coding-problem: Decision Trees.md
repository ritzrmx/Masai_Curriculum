# Coding Problem: Decision Trees

> **Session 12** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

You're building a model to decide whether a bank should approve a loan. Decision Trees are interpretable — you can actually read the rules the model learned. You'll train, visualise, and control overfitting.

---

## Setup

```python
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

np.random.seed(42)
n = 150
df = pd.DataFrame({
    "income":       np.random.randint(20, 120, n),
    "credit_score": np.random.randint(400, 800, n),
    "loan_amount":  np.random.randint(5, 50, n),
    "employed":     np.random.randint(0, 2, n),
})
df["approved"] = ((df["credit_score"] > 600) & (df["income"] > 40)).astype(int)
```

---

## Tasks

**Task 1 — Split**

```python
X = df.drop(columns=["___"])                             # fill: approved
y = df["___"]                                             # fill: approved

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=___, random_state=42                  # fill: 0.2
)
```

---

**Task 2 — Train and Evaluate at Different Depths**

```python
for depth in [1, 3, 5, None]:
    dt = DecisionTreeClassifier(max_depth=___, random_state=42)   # fill: depth
    dt.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, dt.predict(X_train))
    test_acc  = accuracy_score(y_test,  dt.predict(X_test))
    print(f"depth={str(depth):4s} → Train: {train_acc:.3f}  Test: {test_acc:.3f}")
```

> At which depth does the model start to overfit? (Train accuracy >> Test accuracy)

---

**Task 3 — Visualise the Tree**

```python
best_tree = DecisionTreeClassifier(max_depth=___, random_state=42)   # fill: 3
best_tree.fit(X_train, y_train)

# Text representation (readable rules)
print(export_text(best_tree, feature_names=list(X.___)))   # fill: columns

# Plot
plt.figure(figsize=(12, 6))
plot_tree(best_tree, feature_names=X.___, class_names=["Denied","Approved"],
          filled=True, rounded=True, fontsize=10)          # fill: columns
plt.title("Loan Approval Decision Tree")
plt.show()
```

---

**Task 4 — Gini Impurity**

The tree splits on the feature that reduces **Gini impurity** the most.

```python
def gini(labels):
    n = len(labels)
    if n == 0:
        return 0
    p1 = sum(labels) / n         # proportion of class 1
    p0 = 1 - p1
    return 1 - (p0**2 + p1**2)  # Gini formula

# What's the Gini impurity of a perfectly pure node?
print("Pure node (all 1s):", gini([1,1,1,1]))
# What's the Gini impurity of a perfectly mixed node?
print("Mixed node (50/50):", gini([0,0,1,1]))
# Fill in what you expect before running:
# Pure node → ___   Mixed node → ___
```

---

## Key Takeaways

- Decision Trees learn **if/else rules** from data — fully interpretable
- **max_depth** controls overfitting — deeper trees memorise training data
- The tree splits on the feature that creates the **purest child nodes** (lowest Gini)
