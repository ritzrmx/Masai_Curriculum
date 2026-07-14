# Coding Problem: Unsupervised Learning: Clustering
> **Session 9 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

Ten customers of a Bengaluru fashion store. Notice what is missing: **there is no `y`.** Nobody has told you what kind of customer anyone is. That is your job.

```python
import pandas as pd

data = {
    "customer":      ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
    "age":           [22, 25, 24, 23, 26, 48, 52, 50, 47, 55],
    "annual_income": [250000, 300000, 280000, 260000, 310000,
                      1800000, 2200000, 2000000, 1900000, 2400000],   # ₹
    "spend_score":   [78, 85, 80, 76, 88, 30, 25, 28, 33, 22],        # 0–100
}
df = pd.DataFrame(data)
features = ["age", "annual_income", "spend_score"]
```

---

## Tasks

**Task 1 — Basic**
Scale the three feature columns with `StandardScaler`. Print the scaled array rounded to 2 decimals. Look at the numbers and say in one line why this step was not optional here.

**Task 2 — Basic**
Fit `KMeans` with `n_clusters=2`, `n_init=10`, `random_state=42` on the **scaled** data. Add the labels to `df` as a `cluster` column, then print `customer` and `cluster` side by side, plus the model's **inertia**.

**Task 3 — Mid**
Two parts:
1. Profile the clusters: `groupby("cluster")` on the **unscaled** feature columns and print the mean of each, rounded to 0 decimals.
2. Read that profile table and print a **business-language name** for each cluster. Also print the **silhouette score** to check the two groups are genuinely separated.

---

## Expected Output

```
Scaled features:
[[-1.13 -1.02  0.86]
 ...                    <- every column now sits in roughly -1.4 to +1.4
 [ 1.33  1.36 -1.19]]

customer  cluster
      C1        0
      ...
     C10        1

Inertia: 0.81

Cluster profile (unscaled):
          age  annual_income  spend_score
cluster
0        24.0       280000.0         81.0
1        50.0      2060000.0         28.0

Cluster 0 -> "Young Low-Income High-Spenders"
Cluster 1 -> "Older High-Income Low-Spenders"

Silhouette score: 0.89   (well above 0.5 — two clearly separate groups)
```

> ⚠️ Cluster numbers are arbitrary labels, not ranks. If your run swaps `0` and `1`, that is not a bug — read your own profile table before naming.

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

data = {
    "customer":      ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
    "age":           [22, 25, 24, 23, 26, 48, 52, 50, 47, 55],
    "annual_income": [250000, 300000, 280000, 260000, 310000,
                      1800000, 2200000, 2000000, 1900000, 2400000],
    "spend_score":   [78, 85, 80, 76, 88, 30, 25, 28, 33, 22],
}
df = pd.DataFrame(data)
features = ["age", "annual_income", "spend_score"]

# --- Task 1: scale ---
# Mandatory: K-Means measures Euclidean distance. Unscaled, annual_income runs in the
# millions while spend_score maxes out at 100 — income would decide every cluster alone.
X_scaled = StandardScaler().fit_transform(df[features])
print("Scaled features:")
print(X_scaled.round(2))

# --- Task 2: fit K-Means (note: no y anywhere) ---
km = KMeans(n_clusters=2, n_init=10, random_state=42)
df["cluster"] = km.fit_predict(X_scaled)

print("\n" + df[["customer", "cluster"]].to_string(index=False))
print(f"\nInertia: {km.inertia_:.2f}")

# --- Task 3a: profile the clusters on the UNSCALED values (readable ₹ and years) ---
profile = df.groupby("cluster")[features].mean().round(0)
print("\nCluster profile (unscaled):")
print(profile)

# --- Task 3b: name the segments — this is the real deliverable ---
for c in profile.index:
    row = profile.loc[c]
    age_word    = "Young"  if row["age"] < 40            else "Older"
    income_word = "Low-Income"  if row["annual_income"] < 1_000_000 else "High-Income"
    spend_word  = "High-Spenders" if row["spend_score"] > 50 else "Low-Spenders"
    print(f'Cluster {c} -> "{age_word} {income_word} {spend_word}"')

# --- Task 3b: sanity-check the separation ---
sil = silhouette_score(X_scaled, df["cluster"])
print(f"\nSilhouette score: {sil:.2f}   (above 0.5 means clearly separate groups)")
```

**The takeaway:** the model handed you the integers `0` and `1`. The names are what a marketing team can actually act on — and only you could write those.

</details>
