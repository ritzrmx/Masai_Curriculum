# Coding Problem: Unsupervised Learning: Clustering
> **Session 9 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A small customer table — annual spend (Rs '000s) and visit frequency (visits/month), with no label column:

```python
import pandas as pd

data = {
    "customer_id":    [1, 2, 3, 4, 5, 6, 7, 8],
    "annual_spend_k": [85, 90, 88, 15, 20, 18, 92, 12],
    "visit_freq":     [3, 2, 4, 9, 8, 10, 3, 9],
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Scale `annual_spend_k` and `visit_freq` using `StandardScaler`. Print the scaled features, rounded to 2 decimals.

**Task 2 — Basic**
Fit `KMeans` with `n_clusters=2`, `random_state=42`, `n_init=10` on the scaled features. Print the resulting cluster labels and the cluster centers (scaled space, rounded to 2 decimals).

**Task 3 — Mid**
Sweep `k` from 1 to 4 on the same scaled features (same `random_state`/`n_init`) and print the inertia for each `k` to identify the elbow.

---

## Expected Output

```
Scaled features (rounded):
[[ 0.89 -0.97]
 [ 1.03 -1.3 ]
 [ 0.98 -0.65]
 [-1.03  0.97]
 [-0.89  0.65]
 [-0.95  1.3 ]
 [ 1.09 -0.97]
 [-1.11  0.97]]

Cluster labels: [0, 0, 0, 1, 1, 1, 0, 1]

Cluster centers (scaled space, rounded):
[[ 1.   -0.97]
 [-1.    0.97]]

Inertia by k:
k=1: inertia=16.0
k=2: inertia=0.47
k=3: inertia=0.31
k=4: inertia=0.17
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

data = {
    "customer_id":    [1, 2, 3, 4, 5, 6, 7, 8],
    "annual_spend_k": [85, 90, 88, 15, 20, 18, 92, 12],
    "visit_freq":     [3, 2, 4, 9, 8, 10, 3, 9],
}
df = pd.DataFrame(data)

# Task 1: scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[["annual_spend_k", "visit_freq"]])
print("Scaled features (rounded):")
print(X_scaled.round(2))

# Task 2: fit KMeans with k=2, print labels and centers
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)
print("\nCluster labels:", df["cluster"].tolist())
print("\nCluster centers (scaled space, rounded):")
print(kmeans.cluster_centers_.round(2))

# Task 3: inertia across k=1..4 to find the elbow
print("\nInertia by k:")
for k in range(1, 5):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    print(f"k={k}: inertia={round(km.inertia_, 2)}")
```

</details>
