# Coding Problem: Clustering and Unsupervised Learning

> **Session 15** | ⏱ 12 mins | Module 2: Classical ML

---

## Scenario

A retail company wants to group their customers into segments based on spending behaviour — without any predefined labels. You'll use K-Means clustering, find the right number of clusters using the Elbow Method, and interpret what each cluster means.

---

## Setup

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 120
df = pd.DataFrame({
    "annual_spend":   np.concatenate([
        np.random.normal(5000,  500, 40),   # low spenders
        np.random.normal(15000, 1000, 40),  # mid spenders
        np.random.normal(30000, 2000, 40),  # high spenders
    ]),
    "visit_frequency": np.concatenate([
        np.random.normal(2, 0.5, 40),
        np.random.normal(6, 1.0, 40),
        np.random.normal(12, 2.0, 40),
    ])
})
```

---

## Tasks

**Task 1 — Scale the Features**

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[["annual_spend", "___"]])   # fill: visit_frequency
```

---

**Task 2 — Elbow Method**

Try k = 1 to 8. Plot inertia (total within-cluster variance) to find the "elbow".

```python
inertias = []

for k in range(1, ___):                                     # fill: 9
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(___)                                             # fill: X_scaled
    inertias.append(km.___)                                 # fill: inertia_

plt.plot(range(1, 9), inertias, marker="o")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()

# At which k does the curve bend (the elbow)?
```

---

**Task 3 — Fit Final Model**

```python
best_k = ___                                               # fill: 3 (based on elbow)

km_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["cluster"] = km_final.fit_predict(___)                  # fill: X_scaled

print(df.groupby("cluster")[["annual_spend","visit_frequency"]].mean().round(0))
```

---

**Task 4 — Visualise Clusters**

```python
colors = ["steelblue", "orange", "green"]

for cluster_id in range(best_k):
    mask = df["cluster"] == ___                            # fill: cluster_id
    plt.scatter(
        df.loc[mask, "annual_spend"],
        df.loc[mask, "visit_frequency"],
        label=f"Cluster {cluster_id}",
        color=colors[cluster_id],
        alpha=0.7
    )

plt.xlabel("Annual Spend (₹)")
plt.ylabel("Visit Frequency / month")
plt.title("Customer Segments")
plt.legend()
plt.show()
```

---

**Task 5 — Business Interpretation**

```python
cluster_summary = df.groupby("cluster")[["annual_spend","visit_frequency"]].mean()
cluster_summary.columns = ["Avg Spend", "Avg Visits"]

# Give each cluster a business label based on spend and frequency
labels = {0: "___", 1: "___", 2: "___"}   # fill: e.g. "Casual", "Regular", "VIP"
cluster_summary["Segment"] = cluster_summary.index.map(labels)
print(cluster_summary)
```

---

## Key Takeaways

- K-Means assigns each point to the nearest **centroid** — repeat until centroids stop moving
- The **Elbow Method** helps choose k: look for where adding more clusters gives diminishing returns
- Always scale features before clustering — K-Means is distance-based and sensitive to scale
