# Lecture Script: Unsupervised Learning: Clustering
> **Instructor Reference** — Module 2: Classical ML | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students make the pivot from supervised to unsupervised learning — they run K-Means end to end on unlabelled data, prove to themselves why feature scaling is mandatory, choose `k` with the elbow method and silhouette score, profile the resulting clusters into named business segments, and then watch K-Means fail on crescent-shaped data while DBSCAN succeeds.

**Student profile at this point:** Eight sessions of supervised learning — regression, classification, ensembles, and metrics. They are fluent in `fit`, `predict`, `train_test_split`, and `StandardScaler`. They have never once trained a model without a `y`. That is the mental shift this session forces.

**Key outcome:** A notebook in which students segment a customer dataset with no labels, justify their choice of `k` with two diagnostics, and hand over a `groupby('cluster').mean()` table with a plain-English name written next to each row.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The Day the `y` Column Disappeared | 5 min | 0:05 |
| **Concept 1:** No Labels, No Accuracy — and Distance as Similarity | 10 min | 0:15 |
| **Practical 1:** Scaling or nonsense — the ₹ salary vs age demo | 15 min | 0:30 |
| **Concept 2:** K-Means — Four Steps, Inertia, and `k-means++` | 10 min | 0:40 |
| **Practical 2:** K-Means on `make_blobs` — fit, plot, read the centroids | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Choosing k — the Elbow and the Silhouette | 10 min | 1:15 |
| **Practical 3:** Elbow + silhouette, then profile and NAME the segments | 15 min | 1:30 |
| **Concept 4:** Where K-Means Breaks — DBSCAN and Hierarchical | 10 min | 1:40 |
| **Practical 4:** `make_moons` — K-Means fails, DBSCAN wins | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — do this live, on screen, with no explanation first.**

Put up a scatter plot of `make_blobs` data with four obvious blobs, all points in one grey colour. Say nothing for five seconds. Then ask the room to shout out a number.

*"How many groups do you see? … Everyone said four. Nobody had a label. Nobody had an answer key. Nobody was trained. You just did unsupervised learning in half a second. Today we teach a machine to do the same thing — and, more importantly, we work out how you would ever know it got the answer right, when there is no right answer to check against."*

Now write two words on the board and box them: **NO `y`.**

**What clustering is NOT:**
- Classification without the labels handy — there is no hidden truth you are trying to recover
- Something you can score with accuracy, precision, recall, or F1
- A thing that has one correct answer that a smarter algorithm would find

**What clustering IS:**
- Discovering structure that was always sitting in the data, unnoticed
- Grouping rows by *similarity*, where "similar" means "close together in distance"
- A tool whose output is judged by whether a human can act on it — not by a metric
- The engine behind customer segmentation, anomaly detection, and document grouping

*"For eight sessions you have been graded. Today, for the first time, you are the grader."*

---

## Concept Block 1: No Labels, No Accuracy — and Distance as Similarity (10 min)

### Board content — the split

```
SUPERVISED (Sessions 1-8)        UNSUPERVISED (Session 9)
-------------------------        ------------------------
model.fit(X, y)                  model.fit(X)
predict a known target           discover unknown structure
accuracy / F1 / R2 / RMSE        no such score exists
train_test_split is essential    usually fit on everything
"Is this right?"                 "Is this useful?"
```

Drive this home: **there is no `y` in the `fit` call.** Watch for students who type `kmeans.fit(X, y)` out of muscle memory. It will not error — sklearn ignores the second argument — and that silence is exactly why it is dangerous.

### Similarity = distance

Clustering has one core idea: **similar means close**. Closeness is **Euclidean distance** — the straight line between two rows treated as points.

For two features:

```
distance = sqrt( (x1 - x2)^2 + (y1 - y2)^2 )
```

Write this on the board with real numbers next to it:

| | Customer A | Customer B | Gap | Gap squared |
|---|---|---|---|---|
| Age (years) | 25 | 45 | 20 | 400 |
| Monthly salary (₹) | 30,000 | 1,20,000 | 90,000 | 8,100,000,000 |

*"Add those two squared gaps. Now tell me — what percentage of the total came from age?"*

The answer is effectively zero. Age contributes 400 out of 8.1 billion. **The distance is salary, and salary alone.** Age is in the dataframe but it is not in the model.

### Therefore: scaling is not optional

| Algorithm | Uses distance? | Scaling |
|---|---|---|
| Linear / Ridge regression | No | Helpful for regularisation |
| Decision tree / Random Forest | No | Not needed |
| **K-Means** | **Yes** | **Mandatory** |
| **DBSCAN** | **Yes** | **Mandatory** |

`StandardScaler` rewrites every column to mean 0, standard deviation 1. Every feature then gets an equal vote in the distance. Say it as a rule they should write down: **if the algorithm measures distance, scale first — always.**

---

## Practical Block 1: Scaling or Nonsense (15 min)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 10 customers. The REAL structure here is AGE: five in their twenties,
# five in their fifties. Salary is deliberately spread wide INSIDE each
# age group, so salary carries no group information at all.
cust = pd.DataFrame({
    "age":            [22, 24, 25, 23, 26,   52, 54, 55, 53, 56],
    "monthly_salary": [40000,  70000, 100000, 130000, 160000,
                       45000,  75000, 105000, 135000, 165000],
})
print(cust)
print("\nColumn ranges:")
print(cust.max() - cust.min())   # age spans 34, salary spans 1,25,000 — ~3700x bigger
```

```python
# --- Fit WITHOUT scaling ---
cust["raw"] = KMeans(n_clusters=2, n_init=10,
                     random_state=42).fit_predict(cust[["age", "monthly_salary"]])

# --- Fit WITH scaling ---
X_scaled = StandardScaler().fit_transform(cust[["age", "monthly_salary"]])
cust["scaled"] = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_scaled)

print(cust)

print("\n--- What did the RAW clustering group on? ---")
print(cust.groupby("raw")[["age", "monthly_salary"]].mean().round(0))

print("\n--- What did the SCALED clustering group on? ---")
print(cust.groupby("scaled")[["age", "monthly_salary"]].mean().round(0))
```

**Read the two profile tables out loud — this is the whole point of the block.**

- The **raw** clusters have almost **identical age means** (both around 38–40) and wildly different salary means (roughly ₹57,000 vs ₹1,32,000). K-Means split the data purely on salary. Age was in the dataframe but it never got a vote.
- The **scaled** clusters have **identical salary means** (both around ₹1,00,000) and cleanly separated age means (24 vs 54). It found the structure that was actually there.

```python
# Show the scaler's arithmetic so they see WHY it fixed things
print(pd.DataFrame(X_scaled, columns=["age_z", "salary_z"]).round(2))
# Both columns now sit in roughly the -1.7 to +1.7 range — an equal vote each.
```

**Live walk-through:** Put the two `groupby` outputs side by side on screen. Then ask: *"Suppose a colleague ran only the raw version and reported back: 'we segmented our customers, and age turned out not to matter — the groups are purely income bands.' What is wrong with that conclusion?"*

Let them answer. The point to land: **age was never tested.** It was drowned out by a column with numbers 3,700 times larger. The model never saw it. The colleague did not discover that age is unimportant — they discovered that they forgot to scale.

Finish with the rule on the board: **distance-based model → `StandardScaler` first. Every single time.**

---

## Concept Block 2: K-Means — Four Steps, Inertia, and `k-means++` (10 min)

### The algorithm — draw it, do not just say it

Draw a scatter of dots on the board. Then walk the loop, redrawing the centroids each pass.

```
STEP 0 — CHOOSE k.        You decide. The algorithm cannot.
STEP 1 — PLACE k centroids.   (k-means++ spreads them out sensibly)
STEP 2 — ASSIGN.          Every point joins its nearest centroid.
STEP 3 — MOVE.            Every centroid slides to the MEAN of its own points.
STEP 4 — REPEAT 2 and 3   until no point changes cluster. Then stop.
```

A **centroid** is not a data point. It is an invented point sitting at the average position of its cluster. It is the "middle" of the group.

### Inertia (WCSS) — how K-Means scores itself

```
inertia = sum over all points of (distance from point to its own centroid)^2
```

Also called **WCSS** — within-cluster sum of squares. Lower is tighter. Every pass of the loop reduces it. When it stops falling, the algorithm has converged.

**Warn them now, before the elbow section:** inertia *always* drops as `k` rises. At `k` = number of rows, every point is its own centroid and inertia is exactly zero. So you can never pick `k` by "minimise inertia." That would give you one cluster per customer.

### The two arguments that matter

| Argument | Default | Why you care |
|---|---|---|
| `init='k-means++'` | on | Spreads initial centroids apart. Random init can land two centroids in the same blob and produce a genuinely bad answer. Never turn it off. |
| `n_init=10` | 10 (or `'auto'`) | Reruns the entire algorithm 10 times from different starts and keeps the lowest-inertia result. |
| `random_state=42` | none | Starting positions are random. Without this, your notebook gives different clusters every run. Set it every time. |

### What K-Means assumes (the fine print)

- Clusters are roughly **round** (spherical)
- Clusters are roughly **the same size**
- Clusters are **separated blobs**
- Every point **must** belong to a cluster — there is no "none of the above"

*"Remember these four. In eighty minutes we are going to break every one of them."*

---

## Practical Block 2: K-Means on `make_blobs` (15 min)

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 300 points, 4 true blobs. We will PRETEND we don't know it's 4.
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=1.0, random_state=42)
X_scaled = StandardScaler().fit_transform(X)

# Fit K-Means with k=4
km = KMeans(n_clusters=4, init="k-means++", n_init=10, random_state=42)
labels = km.fit_predict(X_scaled)     # NOTE: no y anywhere in this line

print("Cluster labels for the first 10 points:", labels[:10])
print("Points per cluster:", np.bincount(labels))
print("Inertia (WCSS):", round(km.inertia_, 2))
print("Centroid coordinates:\n", km.cluster_centers_.round(2))

# Plot the clusters with the centroids marked on top
plt.figure(figsize=(6, 5))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="viridis", s=25, alpha=0.8)
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
            c="red", marker="X", s=250, edgecolors="black", label="Centroids")
plt.title(f"K-Means, k=4 — inertia {km.inertia_:.1f}")
plt.xlabel("Feature 1 (scaled)"); plt.ylabel("Feature 2 (scaled)")
plt.legend()
plt.show()
```

Expect four clusters of roughly 75 points each, an inertia in the high teens, and a 4-row × 2-column centroid array. Have students read their own numbers rather than quoting figures at them.

```python
# Prove that k is a CHOICE, not a discovery: force a wrong k.
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, k in zip(axes, [2, 4, 7]):
    m = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled)
    ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=m.labels_, cmap="viridis", s=18)
    ax.scatter(m.cluster_centers_[:, 0], m.cluster_centers_[:, 1],
               c="red", marker="X", s=140, edgecolors="black")
    ax.set_title(f"k = {k}  |  inertia = {m.inertia_:.1f}")
plt.tight_layout()
plt.show()
```

**Live walk-through:** Point at the three panels in turn. At `k=2`, two real blobs have been welded together. At `k=7`, real blobs have been sliced in half. Both ran without a single error and both returned confident-looking labels.

Now the key question for the room: *"Look at the inertia printed on each panel. It is lowest at k=7. Does that mean k=7 is the best clustering?"* Let them sit with it. Then: *"No — and that is exactly why we need the next concept."*

---

## BREAK (10 min)

*Something to chew on: inertia keeps falling as k goes up, and hits zero when every customer is their own cluster. So a number that always improves cannot tell you when to stop. What would you look at instead?*

---

## Concept Block 3: Choosing k — the Elbow and the Silhouette (10 min)

### Method 1 — the elbow

Fit K-Means for `k = 1, 2, 3 ... 10`. Plot inertia on the y-axis, `k` on the x-axis. Sketch this curve on the board:

```
inertia
  |  *
  |    *
  |      *
  |        *          <- steep: each new cluster genuinely helps
  |          *
  |            * _ _ _ _ _ _ _ _   <- flat: new clusters just split real groups
  |              ^
  |            ELBOW = your k
  +--------------------------------- k
```

Before the elbow, adding a cluster buys you a big drop in inertia. After it, you are paying for almost nothing. The bend is the answer.

**Be honest with them:** the elbow is often a judgement call. On clean data it is obvious. On real customer data it is a gentle curve and three people will point at three different places. That is why you never rely on it alone.

### Method 2 — the silhouette score

For a single point:

```
a = average distance to the other points IN its own cluster
b = average distance to the points in the NEAREST OTHER cluster
silhouette = (b - a) / max(a, b)
```

Read it in plain words: *how much better off am I in my cluster than in the next-best one?* Average this over every point to score the whole clustering.

| Score | Reading |
|---|---|
| `+0.7` to `+1.0` | Strong, clearly separated clusters |
| `+0.5` to `+0.7` | Reasonable structure |
| `+0.25` to `+0.5` | Weak — the structure may be imaginary |
| Below `0.25` | No real cluster structure. Say so out loud. |
| Negative | Points are on average closer to a *different* cluster. Something is wrong. |

Unlike inertia, the silhouette does **not** just keep improving with `k`. It peaks. That peak is a real recommendation.

### The rule for the room

Run both. If the elbow and the silhouette peak agree, take that `k` with confidence. If they disagree, look at the cluster profiles for each candidate `k` and choose the one you can *explain* — a `k` you cannot describe in business language is a `k` you cannot ship.

---

## Practical Block 3: Elbow, Silhouette, and Naming the Segments (15 min)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# A synthetic customer base — 3 hidden segments, but WE ACT AS IF WE DO NOT KNOW THAT.
# Features: age (years), monthly_spend (₹), visits_per_month
centres = [[24, 12000, 11], [38, 65000, 3], [55, 30000, 6]]
spreads = [[3, 2500, 1.5], [5, 7000, 1.0], [4, 4000, 1.2]]
X, _ = make_blobs(n_samples=300, centers=centres, cluster_std=spreads, random_state=42)

customers = pd.DataFrame(X, columns=["age", "monthly_spend", "visits_per_month"])
print(customers.describe().round(0))

# MANDATORY: scale before any distance-based model.
X_scaled = StandardScaler().fit_transform(customers)
```

```python
# --- Elbow curve and silhouette curve, side by side ---
ks = range(1, 11)
inertias, sils = [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled)
    inertias.append(km.inertia_)
    sils.append(silhouette_score(X_scaled, km.labels_) if k > 1 else np.nan)  # needs 2+ clusters
    if k > 1:
        print(f"k={k}  inertia={km.inertia_:8.1f}   silhouette={sils[-1]:.3f}")

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(list(ks), inertias, "o-", color="steelblue", lw=2)
ax[0].set_title("Elbow — where does it bend?"); ax[0].set_xlabel("k"); ax[0].set_ylabel("Inertia (WCSS)")
ax[1].plot(list(ks), sils, "o-", color="coral", lw=2)
ax[1].set_title("Silhouette — where does it peak?"); ax[1].set_xlabel("k"); ax[1].set_ylabel("Avg silhouette")
plt.tight_layout()
plt.show()
```

Inertia falls very steeply to `k=3` and then flattens; the silhouette peaks at `k=3`. Both diagnostics agree. Let students read their own printed values.

```python
# --- Fit the chosen k, then PROFILE the clusters ---
final = KMeans(n_clusters=3, n_init=10, random_state=42)

# Attach labels to the UNSCALED dataframe — we want readable ₹ and years, not z-scores.
customers["cluster"] = final.fit_predict(X_scaled)

profile = customers.groupby("cluster").mean().round(0)
profile["n_customers"] = customers["cluster"].value_counts().sort_index()
print(profile)

# --- The actual deliverable: NAMES. Read YOUR table and fill these in;
# cluster numbers are arbitrary and can differ between runs. ---
names = {0: "…", 1: "…", 2: "…"}
customers["segment"] = customers["cluster"].map(names)
feats = ["age", "monthly_spend", "visits_per_month"]
print(customers.groupby("segment")[feats].mean().round(0))
```

**Live walk-through:** The profile gives three clearly different rows — a young, low-spend, very-frequent group; a middle-aged, high-spend, rare-visit group; and an older, mid-spend, mid-frequency group. Put it on screen and run the naming as a room activity, taking suggestions out loud: *"Young Frequent Small-Basket Shoppers"*, *"Big-Ticket Occasional Buyers"*, *"Steady Mid-Value Regulars"*.

Then land the point of the whole session: *"A marketing team cannot send an offer to 'Cluster 1'. They can absolutely send an offer to 'Big-Ticket Occasional Buyers'. The model produced integers. You produced the deliverable."*

Stress the ordering trap too: cluster numbers are arbitrary labels, not ranks. Cluster 2 is not "better" than cluster 0, and the numbering shuffles if someone reruns with a different `random_state`.

---

## Concept Block 4: Where K-Means Breaks — DBSCAN and Hierarchical (10 min)

### The three failure modes

Sketch each on the board as a quick scatter with the K-Means answer drawn over it:

1. **Non-round shapes.** Two interlocking crescents. K-Means, which can only cut with straight boundaries, slices straight through both and hands you two halves that each contain part of both crescents.
2. **Very different cluster sizes.** A huge sparse blob next to a tiny dense one. K-Means tends to steal points from the big one.
3. **Outliers.** Every point *must* join a cluster. One extreme point drags its centroid towards it and distorts the whole group.

### DBSCAN — density instead of centroids

**DBSCAN** = Density-Based Spatial Clustering of Applications with Noise. The idea in one line: *a cluster is a region where points are packed close together; everything else is noise.*

| Parameter | Meaning | If too small | If too large |
|---|---|---|---|
| `eps` | Radius of a point's neighbourhood | Everything becomes noise | Everything merges into one cluster |
| `min_samples` | Neighbours needed inside `eps` to count as "dense" | Noise gets clustered | Real clusters get called noise |

What it buys you:

- **No `k`.** DBSCAN decides the number of clusters itself.
- **Any shape.** Crescents, rings, snakes — all fine.
- **Honest about outliers.** Points in no dense region get label **`-1`** = **noise**. This is a feature, not a bug. Those `-1` rows are often the most interesting rows in the dataset — fraud, sensor faults, VIP customers.

What it costs you: `eps` is genuinely fiddly, and it struggles when different clusters have very different densities.

### Hierarchical clustering — the tree

Start with every point as its own cluster. Repeatedly merge the two closest clusters. Keep going until one cluster remains. Plot that merge history as a tree — a **dendrogram** — and cut across it at whatever height you like. Where you cut determines `k`, and you can decide *after* seeing the tree.

In sklearn: `AgglomerativeClustering(n_clusters=3)`. It is slow on large data (it compares all pairs), but the dendrogram is the best picture of nested structure you will ever get.

| | K-Means | DBSCAN | Hierarchical |
|---|---|---|---|
| Choose `k` up front | Yes | No | No — cut later |
| Arbitrary shapes | No | Yes | Yes |
| Outliers | Absorbed | Labelled `-1` | Absorbed |
| Scales to 1M rows | Yes | Moderately | No |
| Default choice when | Blobby data, big data | Odd shapes, outliers matter | You want to *see* the structure |

---

## Practical Block 4: `make_moons` — K-Means Fails, DBSCAN Wins (10 min)

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# Two interlocking crescents. Any human sees two groups instantly.
X, _ = make_moons(n_samples=300, noise=0.08, random_state=42)
X_scaled = StandardScaler().fit_transform(X)

km_labels = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_scaled)
db = DBSCAN(eps=0.25, min_samples=5)
db_labels = db.fit_predict(X_scaled)

n_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
n_noise = int((db_labels == -1).sum())
print(f"DBSCAN found {n_clusters} clusters and {n_noise} noise points (label -1)")
print("K-Means silhouette on the moons:", round(silhouette_score(X_scaled, km_labels), 3))
```

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], c="grey", s=22)
axes[0].set_title("The raw data — you see 2 crescents")

axes[1].scatter(X_scaled[:, 0], X_scaled[:, 1], c=km_labels, cmap="viridis", s=22)
axes[1].set_title("K-Means, k=2 — WRONG\nit cuts a straight line through both")

# DBSCAN: draw noise points (-1) as black crosses
noise_mask = db_labels == -1
axes[2].scatter(X_scaled[~noise_mask, 0], X_scaled[~noise_mask, 1],
                c=db_labels[~noise_mask], cmap="viridis", s=22)
axes[2].scatter(X_scaled[noise_mask, 0], X_scaled[noise_mask, 1],
                c="black", marker="x", s=70, label="noise (-1)")
axes[2].set_title(f"DBSCAN — RIGHT\n{n_clusters} clusters, {n_noise} noise points")
axes[2].legend()

plt.tight_layout()
plt.show()
```

**Live walk-through:** The middle panel is the money shot. K-Means splits the moons left/right — it can only draw straight boundaries between centroids, and no straight line separates two crescents that wrap around each other. It reports a respectable-looking silhouette while being completely wrong.

*"K-Means did not crash. It did not warn you. It gave you a clean, confident, plausible answer — and it was nonsense. What is the only reason you know that?"* (Answer: because you plotted it. Always plot your clusters.)

Then point at the black crosses in panel three: *"Those are the `-1` points. DBSCAN is telling you 'I decline to guess about these.' No other algorithm today has the humility to do that."*

```python
# Optional if time allows: eps sensitivity — the one thing they must feel
for eps in [0.10, 0.25, 0.60]:
    lab = DBSCAN(eps=eps, min_samples=5).fit_predict(X_scaled)
    n_c = len(set(lab)) - (1 if -1 in lab else 0)
    print(f"eps={eps}: {n_c} clusters, {(lab == -1).sum()} noise points")
```

Tiny `eps` fragments the data into many clusters and huge noise. Large `eps` merges the two moons into one. There is a right range and you find it by trying.

---

## Summary & Wrap-Up (5 min)

**The spine of today:**

1. **No `y`.** Unsupervised learning finds structure in `X` alone. There is no accuracy score because there is no right answer.
2. **Similar = close.** Clustering measures similarity as Euclidean distance — which makes **feature scaling mandatory**, or the biggest-numbered column (₹ salary) silently decides everything.
3. **K-Means** = place `k` centroids → assign each point to the nearest → move each centroid to the mean of its points → repeat until stable. It minimises **inertia** and assumes round, similar-sized blobs.
4. **Choose `k`** with the **elbow** on inertia and the **silhouette score** (−1 to +1). Never by minimising inertia — that always picks the largest `k`.
5. **DBSCAN** when the shapes are strange: no `k` needed, any shape, and it labels outliers as noise (`-1`). **Hierarchical** when you want to see the whole tree.
6. **The deliverable is the name.** `groupby('cluster').mean()`, read the profile, and write a business-language segment name next to each row. "Cluster 1" is not an insight.

**Bridge:** *"Every model in this module so far has quietly rested on ideas about likelihood, chance, and counting — the probability a classifier assigns, the randomness in a train-test split, the random starts inside K-Means. Next session is the Master Class: Probability & Counting — The Mathematics of Uncertainty, where we go underneath all of it and build the maths properly."*

---

## Q&A & Doubt Solving (5 min)

**Q: If there is no right answer, how do I know my clustering is any good?**
→ Three checks. (1) Silhouette — is it above roughly 0.5? (2) Stability — do you get broadly the same segments with a different `random_state`, or on a random 80% of the rows? If the segments dissolve, they were never real. (3) The one that actually decides it: can a stakeholder look at your profile table and recognise those groups as real people? A clustering that scores 0.7 but that nobody can name is worthless. One that scores 0.45 but reveals a segment marketing instantly recognises is gold.

**Q: Why can't I just pick the `k` with the lowest inertia?**
→ Because inertia is mathematically guaranteed to fall as `k` rises, all the way to exactly zero when every row is its own cluster. "Minimise inertia" therefore always answers "give each customer their own segment" — which is the same as having no segments at all. The elbow works precisely because it ignores the *level* of inertia and looks at where the *rate of improvement* collapses.

**Q: My cluster numbers changed when I reran the notebook. Is my model broken?**
→ No, and this catches almost everyone. The labels `0`, `1`, `2` are arbitrary names, not rankings — K-Means starts from random centroid positions, so the group called `0` last time might be `2` this time. The *groupings* are stable; only the *names* shuffle. That is why you set `random_state=42`, and why you must never write logic that assumes cluster `0` means anything. Always re-derive meaning from the profile table.

**Q: Should I use `train_test_split` for clustering?**
→ Generally no. There is no target to hold out and no prediction to score, so a test set has nothing to measure — you fit on all the data you have. (One exception: if you intend to *assign new customers* to existing segments, you fit the scaler and K-Means once on historical data and then call `.predict()` on new arrivals — so the scaler is reused, never refitted on the new rows.)

**Q: DBSCAN gave me almost all `-1`. What did I do wrong?**
→ Your `eps` is too small: no point has `min_samples` neighbours inside that radius, so everything is noise. Check two things. First, did you scale? On raw data with ₹ salary in the tens of thousands, an `eps` of 0.5 is microscopic and *everything* will be noise. Second, sweep `eps` and print the cluster count and noise count for each — you want the range where the cluster count is stable and the noise fraction is small.

---

## Instructor Notes

- **No installs beyond the usual** — `scikit-learn`, `pandas`, `numpy`, `matplotlib`. Every dataset is generated in memory with `make_blobs` / `make_moons`, so a flaky classroom network cannot derail the session.
- **`n_init` warning:** on scikit-learn 1.4+ the default changed to `'auto'`. Every snippet here passes `n_init=10` explicitly, which silences the `FutureWarning` and keeps results identical across student machines.
- **The single most common student mistake:** clustering on unscaled data. It never errors, it always returns confident-looking labels, and those labels are just the largest-magnitude column in disguise. Pre-empt it in Practical 1 — make them *print the age means per cluster* and *see* that age had no vote. Repeat the rule until it is boring: **distance-based model → scale first.**
- **The second most common mistake:** stopping at `fit_predict` and treating cluster integers as the answer. Protect time in Practical 3 for the naming activity. If the notebook ends with a `groupby` table and no names written on it, the session did not land.
- **Watch for `kmeans.fit(X, y)`.** Eight sessions of supervised muscle memory will produce it. sklearn silently ignores the `y`, so it never errors. Call it out on the board in Concept 1.
- **Pacing:** if you are running late, cut the optional `eps` sweep at the end of Practical 4 and shorten the elbow discussion. Do not cut Practical 1 or the naming activity.
- **Always plot.** The moons demo only lands because the failure is *visible*. A silhouette score cannot tell you your boundaries are shaped wrong — only your eyes can.
