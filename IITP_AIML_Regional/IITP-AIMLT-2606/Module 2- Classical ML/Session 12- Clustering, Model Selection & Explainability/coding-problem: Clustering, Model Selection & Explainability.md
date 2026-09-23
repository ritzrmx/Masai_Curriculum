# Coding Problem: Clustering, Model Selection & Explainability
> **Session 12 — Module 2: Classical ML** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Run `KMeans` on scaled features:

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.DataFrame({
    "annual_spend_k": [12, 45, 15, 50, 10, 48, 14, 52, 11, 46],
    "purchase_frequency": [8, 2, 9, 1, 7, 2, 8, 1, 9, 2],
})
X = df[["annual_spend_k", "purchase_frequency"]]

X_scaled = ___().fit_transform(X)

kmeans = ___(n_clusters=___, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(___)
print(df)
```

**Task 2 — Basic**

Compute silhouette score and inertia across a k sweep:

```python
from sklearn.metrics import silhouette_score

for k in [2, 3, 4]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    print(k, km.inertia_, silhouette_score(X_scaled, labels))
```

**Task 3 — Mid**

Build a structured model comparison table for a small classification dataset:

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

clf_df = pd.DataFrame({
    "income_k": [25, 40, 60, 30, 80, 45, 90, 35, 70, 50],
    "credit_score": [590, 640, 720, 600, 780, 650, 800, 610, 750, 660],
    "approved": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
})
Xc = clf_df[["income_k", "credit_score"]]
yc = clf_df["approved"]
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=42, stratify=yc)

results = []
for name, model in [("Logistic Regression", LogisticRegression()), ("Decision Tree", DecisionTreeClassifier(max_depth=2, random_state=42))]:
    model.fit(Xtr, ytr)
    preds = model.predict(Xte)
    results.append({"Model": name, "Accuracy": accuracy_score(yte, preds), "F1": f1_score(yte, preds)})

print(pd.DataFrame(results))
```

---

## Expected Output

```
   annual_spend_k  purchase_frequency  cluster
0              12                   8        ...
...

2 ... ...
3 ... ...
4 ... ...

                Model  Accuracy   F1
0  Logistic Regression       ...  ...
1        Decision Tree       ...  ...
```

*(Exact numbers depend on the fitted model on this toy dataset — values will be printed, not fixed constants.)*

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

df = pd.DataFrame({
    "annual_spend_k": [12, 45, 15, 50, 10, 48, 14, 52, 11, 46],
    "purchase_frequency": [8, 2, 9, 1, 7, 2, 8, 1, 9, 2],
})
X = df[["annual_spend_k", "purchase_frequency"]]

X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)
print(df)

for k in [2, 3, 4]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    print(k, km.inertia_, silhouette_score(X_scaled, labels))

clf_df = pd.DataFrame({
    "income_k": [25, 40, 60, 30, 80, 45, 90, 35, 70, 50],
    "credit_score": [590, 640, 720, 600, 780, 650, 800, 610, 750, 660],
    "approved": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
})
Xc = clf_df[["income_k", "credit_score"]]
yc = clf_df["approved"]
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=42, stratify=yc)

results = []
for name, model in [("Logistic Regression", LogisticRegression()), ("Decision Tree", DecisionTreeClassifier(max_depth=2, random_state=42))]:
    model.fit(Xtr, ytr)
    preds = model.predict(Xte)
    results.append({"Model": name, "Accuracy": accuracy_score(yte, preds), "F1": f1_score(yte, preds)})

print(pd.DataFrame(results))
```
</details>
