# Lecture Script: Unsupervised Learning: Clustering
> **Instructor Reference** — Module 2: Classical ML | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can explain why unsupervised learning has no `y`, implement and interpret K-Means clustering end-to-end (scale → fit → elbow → profile), and describe Hierarchical Clustering as an alternative that doesn't require picking `k` upfront.

**Student profile at this point:** Eight sessions deep into Classical ML — comfortable with `train_test_split`, fitting `sklearn` estimators, reading `.predict()` output, and evaluating models against a known label (`y`). Every algorithm so far has had a target column to check answers against.

**Key outcome:** By the end of class, every student has run a full clustering pipeline on a customer-segmentation-style dataset and can translate raw cluster numbers into a business-readable segment name.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Unsupervised Learning & The K-Means Algorithm | 10 min | 0:15 |
| **Practical 1:** Trace K-Means by Hand, Verify with sklearn | 15 min | 0:30 |
| **Concept 2:** Feature Scaling + The Elbow Method | 10 min | 0:40 |
| **Practical 2:** Fit KMeans on `make_blobs` + Elbow Sweep | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Customer Segmentation — Business Framing | 10 min | 1:15 |
| **Practical 3:** Segment Customers, Prove the Scaling Effect | 15 min | 1:30 |
| **Concept 4:** Hierarchical Clustering — No `k` Required Upfront | 10 min | 1:40 |
| **Practical 4:** Agglomerative Clustering vs. K-Means | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Put this on the board — no code yet, just a question:

```
customer_id, annual_spend, visit_frequency
1,            85000,        3
2,            90000,        2
3,            15000,        9
4,            20000,        8
...
```

Ask the class: *"If I asked you to put these customers into 3 or 4 meaningful groups — no instructions, no 'correct answer' column — how would you even start?"* Let a few students describe an approach out loud (most will say something like "group people who spend similarly and visit similarly"). Point out: *that instinct — grouping by similarity, with no target to check against — is exactly what we formalize today.*

**Context to set:** Every model in Sessions 1–8 had a `y`. Linear Regression predicted a price; Logistic Regression and Random Forest predicted a class. You could always ask *"was the prediction right?"* because the true answer existed in the data. Today that changes — there is no `y`, only `X`. The algorithm's job is not to predict a known answer but to **discover structure** that was never labeled. This is the majority of real-world data: most of what companies collect is unlabeled.

**Learning contract for today:**
- Understand what makes a problem "unsupervised" and how K-Means groups points
- Use the elbow method to choose a defensible number of clusters
- Run a full clustering pipeline on a customer-segmentation dataset and name the segments
- Know when Hierarchical Clustering is the better tool

---

## Concept Block 1: Unsupervised Learning & The K-Means Algorithm (10 min)

### Supervised vs. Unsupervised — What Actually Changes

| | Supervised (Sessions 1–8) | Unsupervised (today) |
|---|---|---|
| Input | `X` (features) + `y` (labels) | `X` only — no `y` |
| Goal | Predict `y` for new data | Discover structure / groups in `X` |
| "Correct answer" | Exists — compare prediction to true `y` | Does not exist — no ground truth to score against |
| Evaluation | Accuracy, F1, RMSE, etc. | Indirect measures (inertia, silhouette) + human judgment |
| Example today | — | Group customers by spend & visit behavior |

**Teaching point:** Because there's no `y`, you can never say a clustering result is "correct" the way you'd say a classifier's prediction is correct. You can only say it's *useful*, *stable*, and *interpretable*. This reframing — from "did I get the right answer" to "did I find a useful pattern" — is the single biggest mental shift of the day.

### The K-Means Algorithm — Four Steps on Repeat

```
1. CHOOSE k     → decide how many clusters you want (you pick this)
2. INITIALIZE   → place k centroids (cluster "centers"), usually smart-random
3. ASSIGN       → each point joins the nearest centroid (Euclidean distance)
4. UPDATE       → move each centroid to the mean of the points assigned to it
        │
        └──── repeat steps 3–4 until assignments stop changing (convergence)

   ASSIGN                    UPDATE
┌─────────────┐          ┌─────────────┐
│  · · C1     │          │   ·  ·      │
│      ·   ·  │   ──►    │     C1'     │   ──► repeat until
│    ·  ·   C2│          │   ·    C2'  │       centroids stop moving
│  ·      ·   │          │  ·   ·      │
└─────────────┘          └─────────────┘
```

**Key facts to state explicitly:**
- `k` (number of clusters) is chosen **by you**, before fitting — K-Means cannot tell you how many groups exist. (This is the gap the elbow method fills, coming up next.)
- The algorithm is sensitive to where centroids start. `sklearn`'s `KMeans` defaults to a smart initialization (`k-means++`) and runs multiple random starts (`n_init`), keeping the best result by lowest inertia — always set `n_init` explicitly in your code so results are reproducible across sklearn versions.
- "Convergence" means centroid positions stabilize — the loop stops when no point changes its assigned cluster.

**Teaching point:** K-Means literally cannot run without a distance calculation, and distance is dominated by whichever feature has the largest numeric range. Hold that thought — it becomes very concrete in Concept Block 2.

---

## Practical Block 1: Trace K-Means by Hand, Verify with sklearn (15 min)

### Step 1 — A Tiny Toy Dataset (do this by hand first, no code)

```
P1: (1.0, 2.0)     P4: (8.0, 8.0)
P2: (1.5, 1.8)     P5: (1.0, 0.6)
P3: (5.0, 8.0)     P6: (9.0, 11.0)
```

Draw these six points on the board. Pick `k=2`. Initialize the two centroids **at P1 and P3** (a deliberately simple choice so the arithmetic is easy to follow live).

**Walk the class through iteration 1 — ASSIGN step:**

```
Point   Coords        Dist->C1  Dist->C2  Assign
P1      (1.0, 2.0)    0.0       7.21      C1
P2      (1.5, 1.8)    0.54      7.12      C1
P3      (5.0, 8.0)    7.21      0.0       C2
P4      (8.0, 8.0)    9.22      3.0       C2
P5      (1.0, 0.6)    1.4       8.41      C1
P6      (9.0, 11.0)   12.04     5.0       C2
```

**UPDATE step — new centroid = mean of assigned points:**

```
New C1 = (1.2, 1.5)  <- mean of P1, P2, P5
New C2 = (7.3, 9.0)  <- mean of P3, P4, P6
```

Ask the class: *"Did any point's nearest centroid change compared to the original assignment?"* Have them check P4 and P5 by eye — they didn't move groups. That's the visual definition of convergence: the next ASSIGN pass produces the same groups.

### Step 2 — Verify with sklearn

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array([
    [1.0, 2.0],
    [1.5, 1.8],
    [5.0, 8.0],
    [8.0, 8.0],
    [1.0, 0.6],
    [9.0, 11.0],
])
point_names = ["P1", "P2", "P3", "P4", "P5", "P6"]

km = KMeans(n_clusters=2, random_state=42, n_init=10)
km.fit(X)

print("sklearn labels:  ", km.labels_)
print("sklearn centers: ", km.cluster_centers_.round(2))
print("sklearn inertia: ", round(km.inertia_, 2))
print("n_iter_ to converge:", km.n_iter_)

for name, lab in zip(point_names, km.labels_):
    print(f"{name}: cluster {lab}")
```

**Output:**
```
sklearn labels:   [1 1 0 0 1 0]
sklearn centers:  [[7.33 9.  ]
 [1.17 1.47]]
sklearn inertia:  15.98
n_iter_ to converge: 2

P1: cluster 1
P2: cluster 1
P3: cluster 0
P4: cluster 0
P5: cluster 1
P6: cluster 0
```

**Walk through this:** sklearn's `cluster 1` = {P1, P2, P5} with center `(1.17, 1.47)` — matches our by-hand `(1.2, 1.5)` (small rounding difference only). `cluster 0` = {P3, P4, P6} with center `(7.33, 9.0)` — matches exactly. The cluster *numbers* (0 vs 1) are arbitrary labels sklearn assigns — never assume cluster `0` means anything special.

**Discussion prompt:** *"What if we had initialized the centroids at P1 and P6 instead of P1 and P3? Would we get the same groups?"* → Usually yes on well-separated data like this, but not guaranteed on messier data — which is exactly why `n_init` (multiple random restarts) exists. Never set `n_init=1` in production code.

---

## Concept Block 2: Feature Scaling + The Elbow Method (10 min)

### Why Scaling Is Not Optional for K-Means

K-Means assigns points using **Euclidean distance**. If one feature ranges 0–100,000 (e.g. annual spend) and another ranges 0–10 (e.g. visits per month), the distance calculation is almost entirely driven by the large-range feature. The small-range feature effectively gets ignored — even if it's just as important for the segmentation.

```
distance² = (spend_a - spend_b)² + (visits_a - visits_b)²
             └── can be 10,000,000 ──┘   └── can be 4 ──┘
             completely dominates the sum
```

**Fix:** `StandardScaler` transforms every feature to mean 0, standard deviation 1, so no feature dominates just because of its units.

**Teaching point:** This is not a "nice to have" — skipping it silently produces clusters that are really just "high spend" vs. "low spend" groups, regardless of what the other features say. We'll see the exact before/after numbers in Practical Block 3.

### The Elbow Method — How to Choose `k`

**Inertia** (a.k.a. within-cluster sum of squares, WCSS) measures how tightly packed each cluster is — the sum of squared distances from every point to its own cluster's centroid. Lower is "tighter," but inertia **always decreases as `k` increases** (more clusters can only shrink each point's distance to its nearest centroid — at the extreme, `k = n` gives inertia `0`, one cluster per point, which is useless).

The **elbow method**: fit K-Means for a range of `k` values, plot `k` vs. inertia, and look for the point where adding another cluster stops giving a big payoff — the "elbow" in the curve.

```
Inertia
   │●
   │  ●
   │     ●
   │        ●___
   │            ●───●───●───●     ← flattens after the elbow
   └──────────────────────────── k
     1  2  3  4  5  6  7  8
              ↑
          elbow ≈ best k
```

**Teaching point:** The elbow method is a heuristic, not a formula — you're looking for the point of *diminishing returns*, not a mathematically unique answer. On real data the elbow is often fuzzy; that's normal, and business context should break the tie.

---

## Practical Block 2: Fit KMeans on `make_blobs` + Elbow Sweep (15 min)

### Step 1 — Generate a Clean Synthetic Dataset

`sklearn.datasets.make_blobs` creates data with known, visually separable groups — perfect for a first real K-Means fit before we bring in messier business data.

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np

X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.80, random_state=42)
print("X shape:", X.shape)
print("First 5 points:\n", X[:5].round(2))
```

**Output:**
```
X shape: (300, 2)
First 5 points:
 [[ -9.21   6.64]
 [ -9.53   7.02]
 [ -1.85   8.04]
 [ -7.05  -6.  ]
 [-10.47   6.52]]
```

**Note for the class:** `y_true` exists here only because `make_blobs` is a *synthetic generator* that secretly knows the true group each point came from — it's included for validation/teaching purposes only. In a real unsupervised problem, you would never have `y_true`. We deliberately do not pass it to `KMeans.fit()`.

### Step 2 — Fit KMeans and Inspect the Fitted Object

```python
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X)

print("First 10 predicted labels:", kmeans.labels_[:10])
print("\nCluster centers:\n", kmeans.cluster_centers_.round(2))
print("\nInertia (within-cluster sum of squares):", round(kmeans.inertia_, 2))

unique, counts = np.unique(kmeans.labels_, return_counts=True)
sizes = {int(u): int(c) for u, c in zip(unique, counts)}
print("\nCluster sizes:", sizes)
```

**Output:**
```
First 10 predicted labels: [3 3 0 1 3 1 2 1 0 2]

Cluster centers:
 [[-2.64  8.99]
 [-6.84 -6.84]
 [ 4.7   2.03]
 [-8.83  7.22]]

Inertia (within-cluster sum of squares): 362.47

Cluster sizes: {0: 75, 1: 75, 2: 75, 3: 75}
```

**Walk through the three attributes students will use constantly:**
- `.labels_` — which cluster each training point landed in (same order as `X`)
- `.cluster_centers_` — the final centroid coordinates, one row per cluster
- `.inertia_` — the single number summarizing how tight the clustering is; use it for the elbow method next

### Step 3 — Elbow Sweep

```python
inertias = []
k_range = range(1, 9)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(round(km.inertia_, 1))

print(f"{'k':<4}{'Inertia':<10}")
for k, i in zip(k_range, inertias):
    print(f"{k:<4}{i:<10}")
```

**Output:**
```
k   Inertia   
1   19780.3   
2   9211.2    
3   1919.4    
4   362.5     
5   329.3     
6   294.6     
7   261.6     
8   232.0     
```

**Read the drops out loud with the class:**

```
k=1 -> k=2: drop = 10569.1
k=2 -> k=3: drop = 7291.8
k=3 -> k=4: drop = 1556.9   ← last big drop
k=4 -> k=5: drop = 33.2     ← falls off a cliff
k=5 -> k=6: drop = 34.7
k=6 -> k=7: drop = 33.0
k=7 -> k=8: drop = 29.6
```

**Teaching point:** The drop from `k=3` to `k=4` is over 1500; every drop after `k=4` is under 35. That's the elbow — `k=4` — and it matches exactly how `make_blobs` was generated (`centers=4`). This is why synthetic data is a great first example: students can *verify* the elbow method actually found the right answer.

---

## BREAK (10 min)

*Suggested break prompt — ask students to jot down, on paper, two features from their own life/work/college context that they think would naturally form clusters (e.g. "study hours vs. exam score", "screen time vs. sleep hours"). They'll share one after the break — used to open Concept Block 3.*

---

## Concept Block 3: Customer Segmentation — Business Framing (10 min)

### Clustering Numbers Have No Names — You Give Them One

K-Means hands you cluster `0`, `1`, `2`, `3`. Those numbers carry zero business meaning by themselves. Your job as a practitioner is to look at each cluster's centroid (translated back to real units) and assign a human-readable label.

```
Raw output                          Business translation
────────────────────────────────    ──────────────────────────────
cluster 0: spend≈89k, visits≈2       →  "Big occasional spenders"
cluster 1: spend≈16k, visits≈2       →  "Low engagement / at risk"
cluster 2: spend≈88k, visits≈10      →  "High-value loyalists"
cluster 3: spend≈19k, visits≈9       →  "Frequent bargain hunters"
```

**Teaching point:** This translation step is where clustering actually creates business value. A marketing team doesn't act on "cluster 2" — they act on "high-value loyalists get a VIP early-access campaign; low-engagement customers get a win-back discount." The model finds the groups; the human names and activates them.

### A Word of Caution

- Clusters found are only as good as the features you gave the model. Missing an important feature (e.g. product category) can produce technically tight but practically useless groups.
- Always sanity-check cluster sizes — a "segment" of 2 customers out of 10,000 is probably noise, not a real market segment.
- Re-run clustering periodically — customer behavior drifts, and segments should be refreshed, not treated as permanent.

---

## Practical Block 3: Segment Customers, Prove the Scaling Effect (15 min)

### Step 1 — Prove Scaling Changes the Answer (small, concrete example)

```python
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Toy customer table: annual spend (Rs '000s) vs visit frequency (visits/month)
data = {
    "customer_id":    list(range(1, 13)),
    "annual_spend_k": [15, 18, 20, 90, 95, 88, 12, 16, 22, 92, 85, 91],
    "visit_freq":     [2, 3, 2, 3, 4, 2, 8, 9, 7, 9, 8, 10],
}
df = pd.DataFrame(data)

print(df[["annual_spend_k", "visit_freq"]].describe().round(2))

X = df[["annual_spend_k", "visit_freq"]].values

# WITHOUT scaling
labels_raw = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
print("\nLabels WITHOUT scaling:", labels_raw)

# WITH scaling
X_scaled = StandardScaler().fit_transform(X)
labels_scaled = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X_scaled)
print("Labels WITH scaling:   ", labels_scaled)

df["cluster_raw"] = labels_raw
df["cluster_scaled"] = labels_scaled
print("\n", df)
```

**Output:**
```
       annual_spend_k  visit_freq
count           12.00       12.00
mean            53.67        5.58
std             38.27        3.18
min             12.00        2.00
25%             17.50        2.75
50%             53.50        5.50
75%             90.25        8.25
max             95.00       10.00

Labels WITHOUT scaling: [2 2 2 0 0 0 1 1 2 0 0 0]
Labels WITH scaling:    [1 1 1 2 2 2 1 1 1 0 0 0]

     customer_id  annual_spend_k  visit_freq  cluster_raw  cluster_scaled
0             1              15           2            2               1
1             2              18           3            2               1
2             3              20           2            2               1
3             4              90           3            0               2
4             5              95           4            0               2
5             6              88           2            0               2
6             7              12           8            1               1
7             8              16           9            1               1
8             9              22           7            2               1
9            10              92           9            0               0
10           11              85           8            0               0
11           12              91          10            0               0
```

**Walk through it live:** Without scaling (`cluster_raw`), customers 4, 5, 6 (spend≈90k, low visits) and customers 10, 11, 12 (spend≈90k, high visits) are dumped into the **same cluster (0)** — the model only "sees" that they all spend a lot; it can't tell high-frequency VIPs from big one-time spenders because `visit_freq`'s range (2–10) is invisible next to `annual_spend_k`'s range (12–95). After scaling (`cluster_scaled`), customers 10–12 split into their own cluster (0) — the frequency signal now actually counts.

**Teaching point:** This is not a hypothetical — this is the *exact* failure mode you'll hit if you forget `StandardScaler` on any dataset with mixed-unit features. Always scale before K-Means.

### Step 2 — Full Segmentation: Elbow + Business Interpretation

```python
rng = np.random.default_rng(42)

def make_group(n, spend_mean, spend_std, freq_mean, freq_std):
    spend = rng.normal(spend_mean, spend_std, n).round(1)
    freq = rng.normal(freq_mean, freq_std, n).round(1)
    return spend, freq

# 4 realistic customer segments (annual spend in Rs '000s, visits/month)
spend_a, freq_a = make_group(10, 90, 5, 10, 1.2)   # High-value loyalists
spend_b, freq_b = make_group(10, 88, 6, 2, 0.7)    # Big occasional spenders
spend_c, freq_c = make_group(10, 18, 4, 9, 1.0)    # Frequent bargain hunters
spend_d, freq_d = make_group(10, 16, 3, 2, 0.6)    # Low engagement

df2 = pd.DataFrame({
    "customer_id": np.arange(1, 41),
    "annual_spend_k": np.concatenate([spend_a, spend_b, spend_c, spend_d]),
    "visit_freq": np.concatenate([freq_a, freq_b, freq_c, freq_d]),
})
print(df2.shape)

X2_scaled = StandardScaler().fit_transform(df2[["annual_spend_k", "visit_freq"]])

# Elbow sweep on this dataset
for k in range(1, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X2_scaled)
    print(f"k={k}: inertia={round(km.inertia_, 2)}")

# Fit final model at the elbow (k=4) and profile clusters in real units
kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=10)
df2["cluster"] = kmeans_final.fit_predict(X2_scaled)

profile = df2.groupby("cluster")[["annual_spend_k", "visit_freq"]].mean().round(1)
profile["count"] = df2.groupby("cluster").size()
print("\nCluster profile (mean, real units):")
print(profile)
```

**Output:**
```
(40, 3)
k=1: inertia=80.0
k=2: inertia=39.93
k=3: inertia=17.82
k=4: inertia=1.66
k=5: inertia=1.3
k=6: inertia=0.94
k=7: inertia=0.7

Cluster profile (mean, real units):
         annual_spend_k  visit_freq  count
cluster                                   
0                  88.7         2.1     10
1                  16.0         1.9     10
2                  88.3        10.3     10
3                  19.2         8.9     10
```

**Have the class name each cluster from the profile table before you reveal the answer:**

```
cluster 0: spend 88.7, visits 2.1   →  Big occasional spenders
cluster 1: spend 16.0, visits 1.9   →  Low engagement / at risk
cluster 2: spend 88.3, visits 10.3  →  High-value loyalists
cluster 3: spend 19.2, visits 8.9   →  Frequent bargain hunters
```

**Note:** the elbow here (`k=3→k=4` drop is 16.16, `k=4→k=5` drop is only 0.36) is unusually sharp because this synthetic data was built from four well-separated groups on purpose — real business data is rarely this clean, but the *procedure* (scale → sweep → elbow → profile → name) is exactly the same.

**Discussion prompt:** *"If your manager asks for exactly 6 segments regardless of what the elbow says, what do you do?"* → Business requirements can override the statistical elbow — but you should document that the extra clusters split naturally coherent groups, so stakeholders understand the trade-off.

---

## Concept Block 4: Hierarchical Clustering — No `k` Required Upfront (10 min)

### The Big Idea: Build a Tree of Merges, Not a Fixed Partition

**Agglomerative (bottom-up) Hierarchical Clustering:**

```
1. Start: every point is its own cluster
2. Repeat: merge the two closest clusters into one
3. Stop: when everything has merged into a single cluster
        → the merge history IS the output — a tree called a dendrogram
```

Unlike K-Means, you don't choose `k` before fitting. You build the *entire* merge tree once, then decide afterward where to "cut" it to get however many clusters you want.

**Trace on our 6-point toy dataset (`method='ward'`, minimizes variance at each merge):**

```
Merge 1: P1 + P2                    at distance 0.54  -> cluster6
Merge 2: P5 + (P1+P2)               at distance 1.53  -> cluster7
Merge 3: P3 + P4                    at distance 3.00  -> cluster8
Merge 4: P6 + (P3+P4)               at distance 4.51  -> cluster9
Merge 5: (P5+(P1+P2)) + (P6+(P3+P4)) at distance 16.86 -> cluster10
```

```
Distance
  16.86 ─┤                    ┌──────────┴──────────┐
         │                    │                      │
   4.51 ─┤              ┌─────┴─────┐                │
         │              │           │                │
   3.00 ─┤              │      ┌────┴────┐            │
   1.53 ─┤   ┌───────┐  │      │         │            │
   0.54 ─┤   │       │  │      │         │            │
         │  P1      P2  P5    P3        P4           P6
```

**Cut the tree** at any horizontal line to get that many clusters — cut low (near 0.54) for many small clusters, cut high (near 16.86) for few large ones. Cutting at distance ≈5 gives exactly the same two groups {P1,P2,P5} and {P3,P4,P6} we got from K-Means.

**Teaching point:** the dendrogram literally shows you the trade-off of every possible `k` in one picture — the tallest un-crossed vertical gap is often a good place to cut, similar in spirit to the K-Means elbow.

### K-Means vs. Hierarchical — When to Use Which

| | K-Means | Hierarchical (Agglomerative) |
|---|---|---|
| Choose `k` upfront? | Yes, required | No — cut the tree after building it |
| Speed on large data | Fast, scales well | Slower — naive implementation is O(n³) |
| Output | Flat partition | Full tree (dendrogram) — inspect any cut level |
| Sensitivity | Random init (mitigated by `n_init`) | Deterministic given the linkage method |
| Best for | Large datasets, fast iteration | Smaller datasets, exploring structure before committing to `k` |

---

## Practical Block 4: Agglomerative Clustering vs. K-Means (10 min)

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.optimize import linear_sum_assignment
import pandas as pd

# Reuse the make_blobs data from Practical 2
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels_km = kmeans.fit_predict(X)

agg = AgglomerativeClustering(n_clusters=4, linkage='ward')
labels_agg = agg.fit_predict(X)

print("KMeans first 15 labels: ", labels_km[:15])
print("Agglo   first 15 labels:", labels_agg[:15])

ct = pd.crosstab(labels_km, labels_agg, rownames=['KMeans'], colnames=['Agglomerative'])
print("\nContingency table:\n", ct)

# Best matching between the two label sets, then % agreement
row_ind, col_ind = linear_sum_assignment(-ct.values)
matched = ct.values[row_ind, col_ind].sum()
print(f"\nPoints in matching clusters: {matched}/300 ({matched/300*100:.1f}%)")
```

**Output:**
```
KMeans first 15 labels:  [3 3 0 1 3 1 2 1 0 2 0 2 0 0 3]
Agglo   first 15 labels: [0 0 3 1 0 1 2 1 3 2 3 2 3 3 0]

Contingency table:
 Agglomerative   0   1   2   3
KMeans                       
0               0   0   0  75
1               0  75   0   0
2               0   0  75   0
3              75   0   0   0

Points in matching clusters: 300/300 (100.0%)
```

**Walk through this:** the raw label numbers differ (KMeans calls one group `3`, Agglomerative calls the same group `0`) — that's expected, cluster IDs are arbitrary. But the contingency table shows a perfect one-to-one match: every group of 75 points that K-Means put together, Agglomerative also put together. **100% agreement.**

**Teaching point:** on well-separated data, K-Means and Hierarchical Clustering converge to the *same* answer — the algorithm you pick matters less than the structure already present in your data. The two methods tend to disagree more on messier, overlapping, or non-spherical (e.g. crescent-shaped) clusters, which is outside today's scope but worth naming if a student asks.

**Discussion prompt:** *"Given that K-Means is faster and gave the identical answer here, why would you ever choose Hierarchical Clustering for real work?"* → When you don't know `k` yet and want to *see* the range of reasonable options before committing (the dendrogram), or on smaller datasets where visual inspection of the tree adds real insight for stakeholders.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Unsupervised learning: `X` only, no `y` — the goal is discovering structure, not predicting a known answer
- The K-Means loop: assign → update → repeat until convergence, and why `k` must be chosen in advance
- Feature scaling is mandatory before K-Means — proved it with a concrete before/after cluster-assignment example
- The elbow method: sweep `k`, track inertia, find the point of diminishing returns
- Customer segmentation: translating raw cluster centroids into named, actionable business segments
- Hierarchical Clustering as an alternative that builds the full merge tree first and lets you cut `k` afterward

**Bridge to next session:** *"Everything we've done in Classical ML — regression, classification, clustering — quietly assumes you understand probability: how likely is an event, how do we count outcomes, what does 'confidence' really mean. Next session is a Master Class dedicated entirely to Probability & Counting — the mathematics of uncertainty that underlies every model we've built so far, and every model still to come."*

**Homework / self-practice:** Take any two numeric columns from a dataset of your choice (or reuse today's customer table with different numbers), run the full pipeline — `StandardScaler` → elbow sweep `k=1..8` → fit at the elbow → profile each cluster in real units — and write one sentence naming what each cluster represents.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: If there's no `y`, how do I know my clustering is actually good?**
→ You can't check against ground truth the way you would with accuracy or F1. Instead, use inertia (tightness), the elbow method (is `k` defensible), and — most importantly — human judgment: do the cluster profiles make business sense? A "good" clustering is one that's stable, interpretable, and useful, not one that's provably correct.

**Q: Inertia always goes down as k increases — so why not just pick a huge k?**
→ Because at the extreme (`k = n`), every point is its own cluster and inertia is exactly 0 — but that's useless, you've just relabeled your raw data. The elbow method exists specifically to stop you at the point where more clusters stop paying off.

**Q: What if the elbow isn't obvious — the curve just curves smoothly?**
→ This happens often on real data. Use a secondary check (silhouette score, which we haven't covered yet but you'll see referenced in later material), or fall back on business constraints (e.g., "marketing can only run 4 campaigns, so k=4").

**Q: Can K-Means handle categorical features, like a "region" column?**
→ Not directly — Euclidean distance on categories is meaningless. You'd need to encode them numerically first (and even then, one-hot-encoded categories interact awkwardly with Euclidean distance). K-Means is fundamentally a numeric-distance algorithm.

**Q: Do I always have to scale before clustering, even if features look similar?**
→ If features are already on comparable scales and units (e.g. two test scores both 0–100), scaling changes little. But it's cheap and safe to always scale before K-Means — the failure mode when you forget it (one feature silently dominating) is hard to detect after the fact.

**Q: Between K-Means and Hierarchical, which should I default to on the job?**
→ Start with K-Means for speed and scale, especially if the dataset is large. Reach for Hierarchical when the dataset is small-to-medium and you want to *see* the structure across many possible `k` values before committing — or when stakeholders want a visual dendrogram to reason about segment granularity themselves.

---

## Instructor Notes

- **Dataset choices:** `make_blobs(n_samples=300, centers=4, cluster_std=0.80, random_state=42)` gives clean, visually separable groups ideal for a first fit and for proving the elbow method actually recovers the true `k`. The hand-built customer dataframe (spend vs. visit frequency) carries the business narrative and is the vehicle for the scaling demonstration and final segmentation exercise. Both are fully self-contained — no file downloads, no internet access required.
- **Common student mistake #1:** Fitting `KMeans` directly on unscaled `annual_spend_k` and `visit_freq` and being confused why frequency seems to have no effect on the groups. Use the Practical 3 Step 1 before/after table to make this failure concrete and visible, not just theoretical.
- **Common student mistake #2:** Treating cluster label numbers as ordinal or meaningful (e.g. assuming cluster `0` is "worse" than cluster `3`). Emphasize repeatedly: label numbers are arbitrary and can flip between runs/algorithms — always profile the centroid before drawing conclusions.
- **Common student mistake #3:** Picking `k` from the elbow chart once and never re-validating against business constraints or re-running as data changes. Segments are not permanent.
- **Live coding tip:** Deliberately run K-Means on the unscaled customer data first, show the (wrong-looking) clusters, then add `StandardScaler` and re-run side by side. The visible label flip is more convincing live than reading it off a slide.
- **For advanced students:** Mention `silhouette_score` (from `sklearn.metrics`) as a more rigorous cluster-quality check than inertia alone, and `DBSCAN` as a density-based alternative that doesn't require choosing `k` and can find non-spherical clusters — both are natural "go explore" pointers, not required for today.
- **Time-check contingency:** If running behind after the break, compress Practical Block 4 to just the contingency-table comparison (skip re-deriving the toy dendrogram trace verbally — point to the ASCII diagram from Concept Block 4 instead) and assign the full walkthrough as homework.
