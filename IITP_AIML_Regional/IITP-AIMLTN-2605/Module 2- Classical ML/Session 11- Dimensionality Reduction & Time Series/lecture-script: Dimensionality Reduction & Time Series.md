# Lecture Script: Dimensionality Reduction & Time Series
> **Instructor Reference** — Module 2: Classical ML | Session 11 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students compress a 64-column dataset down to a handful of principal components (and *see* their classes separate in 2-D), then take a raw daily sales series, engineer lag and rolling features from it, split it chronologically, and build a model that beats the persistence baseline.

**Student profile at this point:** They have trained regression (S3–S4), classification (S6–S8), ensembles (S7), and K-Means clustering (S9). They know `train_test_split`, cross-validation, `StandardScaler`, pipelines, and leakage (S2). They have **never** met PCA, and they have never modelled anything time-ordered. Every dataset they have seen so far had interchangeable rows.

**Key outcome:** One notebook with two halves — a PCA scree/cumulative plot plus a 2-D class-coloured scatter of `load_digits`, and a lag-featured sales model whose MAE is compared honestly against a naive baseline under a chronological split.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The 500-Column Trap | 5 min | 0:05 |
| **Concept 1:** The Curse of Dimensionality | 10 min | 0:15 |
| **Practical 1:** Watch distance die; watch KNN die | 15 min | 0:30 |
| **Concept 2:** PCA — Best Camera Angle on Your Data | 10 min | 0:40 |
| **Practical 2:** PCA on digits — scree, 2-D map, speed-up | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Time Series — The Rows Are Not Independent | 10 min | 1:15 |
| **Practical 3:** Build the series, shuffle it, get caught | 15 min | 1:30 |
| **Concept 4:** Lag Features and the Baseline You Must Beat | 10 min | 1:40 |
| **Practical 4:** Lags, rolling windows, beat persistence | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — do this live, no slides.** Write two lines on the board:

```
Breast-cancer data, 30 real features   → KNN accuracy ≈ 0.96
Same data + 500 columns of pure noise  → KNN accuracy ≈ 0.88
```

Then say: *"I did not delete a single real feature. Every one of the 30 good columns is still there. I only ADDED information — random, meaningless numbers. And the model got dramatically worse. How can adding columns make a model worse?"*

Let them argue for sixty seconds. Someone will say "the noise confused it." Push back: KNN does not have weights to confuse. Something more fundamental has broken.

**What dimensionality reduction is NOT:**
- Dropping columns you personally find boring
- A magic accuracy booster you bolt on to every model
- Something you do *after* fitting, to tidy up the output

**What dimensionality reduction IS:**
- A rescue operation for the *distance* that KNN and K-Means are built on
- A way to draw a picture of data that has more than 3 columns
- A trade: you buy speed and clarity, and you pay for them with interpretability

*"And in the second half we will meet a dataset where the rows are not allowed to be shuffled — where `train_test_split` as you know it is a bug."*

---

## Concept Block 1: The Curse of Dimensionality (10 min)

### Board content

```
1 feature   → 10 tiles to search
2 features  → 100 tiles
3 features  → 1,000 tiles
d features  → 10^d

Data does not grow to fill this space. It just gets LONELIER.
```

The volume of the space explodes exponentially with each column. Your row count does not. So the points spread thinner and thinner, and every point ends up roughly the same distance from every other point.

### Why this specifically kills what they already built

| Model (session) | What it relies on | What breaks in high dimensions |
|---|---|---|
| KNN (S6) | "Who is nearest to me?" | Nearest and farthest neighbours are equally far |
| K-Means (S9) | Distance to a centroid | All centroids look equally close; clusters are arbitrary |
| Linear/Logistic (S3, S6) | Weighted sums, not distances | Survives better, but overfits — more columns than it needs |
| Tree ensembles (S7) | Threshold splits per feature | Most robust, but slow and wasteful with junk columns |

**Say this out loud:** *"Distance is a comparison. In 500 dimensions, everything is far from everything, so the comparison carries no signal. KNN's 'nearest neighbour' is a coin flip wearing a lab coat."*

**Three responses to too many columns:** *feature selection* (drop original columns — keeps names), *feature extraction* (build a few new columns that summarise the old — this is PCA, and it loses the names), or *regularisation* (Session 3 — only helps linear models). Today is the middle one.

---

## Practical Block 1: Watch Distance Die (15 min)

```python
import numpy as np
from scipy.spatial.distance import pdist

np.random.seed(42)

print(f"{'dims':>6} | {'min dist':>9} | {'max dist':>9} | {'contrast':>9}")
print("-" * 45)
for d in [2, 5, 20, 100, 500]:
    X = np.random.rand(300, d)          # 300 random points in d dimensions
    dists = pdist(X)                    # every pairwise distance
    contrast = (dists.max() - dists.min()) / dists.min()
    print(f"{d:>6} | {dists.min():>9.3f} | {dists.max():>9.3f} | {contrast:>9.2f}")
```

**Expected output shape:** `contrast` starts in the hundreds at 2 dimensions and collapses towards ~0.2 by 500 dimensions. The min distance climbs, the max distance climbs, and the *gap between them* — the only thing KNN can actually use — vanishes.

**Live walk-through:** Point at the `contrast` column and read it downwards. *"In 2-D, the farthest point is hundreds of times farther away than the nearest one. In 500-D, the farthest point is only 20% farther than the nearest. If your nearest neighbour is essentially as far away as your worst enemy — what exactly is KNN voting on?"*

Now prove the consequence on real data:

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))

print(f"Real features only ({X.shape[1]} cols): "
      f"{cross_val_score(knn, X, y, cv=5).mean():.3f}")

rng = np.random.RandomState(42)
for n_junk in [50, 200, 500]:
    X_junk = np.hstack([X, rng.normal(size=(X.shape[0], n_junk))])
    score = cross_val_score(knn, X_junk, y, cv=5).mean()
    print(f"+ {n_junk:>3} junk cols ({X_junk.shape[1]:>3} cols): {score:.3f}")
```

**Expected output:** accuracy starts around 0.96 with the 30 real features and slides down through the high-0.80s as the noise columns pile up — losing roughly 8 accuracy points to columns that contain literally nothing.

**Ask the room:** *"The 30 real columns never left. Why can't KNN just ignore the noise?"* → Because KNN has no concept of "ignoring" a column. Every column contributes equally to the distance. 500 junk columns simply drown out 30 good ones in the sum.

---

## Concept Block 2: PCA — The Best Camera Angle (10 min)

### The shadow demo (do it physically)

Hold up any 3-D object — a water bottle, a chalk duster. Switch on your phone torch behind it and cast a shadow on the whiteboard.

- Point the torch down the bottle's long axis → the shadow is a boring circle. Useless.
- Turn it side-on → the shadow shows the neck, the body, the cap. Instantly recognisable.

*"Same object. Same 2-D shadow. But one angle preserved the shape and the other destroyed it. **PCA is the algorithm that finds the good angle** — automatically, in 64 dimensions, where you cannot use your eyes."*

### Board content

```
PC1 = the direction along which the data spreads out the MOST
PC2 = next-most-spread direction, at 90° to PC1
PC3 = next-most-spread, at 90° to both
...

VARIANCE = INFORMATION.
A direction where all points look identical tells you nothing → drop it first.
```

### The non-negotiable prerequisite

| Column | Unit | Spread |
|---|---|---|
| `monthly_spend` | ₹ | ~40,000 |
| `age` | years | ~15 |
| `visits` | count | ~5 |

Without scaling, PCA looks at these and declares `monthly_spend` to be *the* dominant direction — not because it matters, but because rupees are bigger numbers than years. **`StandardScaler()` before `PCA()`. Always.** Write it on the board and underline it twice.

### And the price

`PC1` is not a column you can name. It is `0.41 × f1 + 0.29 × f2 − 0.18 × f3 + ...` across every original feature. You can no longer tell a doctor "the tumour radius was the deciding factor." You can only say "PC1 was high," which means nothing to anyone.

| Use PCA for | Do NOT use PCA for |
|---|---|
| Plotting >3-D data in 2-D | Any model whose reasoning must be explained |
| Speeding up training on wide data | Data with only 5–10 columns — no gain |
| Denoising (dropping low-variance directions) | Before you have standardised |

**Name-drop only:** t-SNE and UMAP also squash data to 2-D and handle curved structure better. They are for *pictures only* — you do not feed their output into a model.

---

## Practical Block 2: PCA on `load_digits` (15 min)

```python
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

digits = load_digits()
X, y = digits.data, digits.target
print("Original shape:", X.shape)      # (1797, 64) — an 8x8 image flattened

X_scaled = StandardScaler().fit_transform(X)   # NEVER skip this line

pca_full = PCA(random_state=42).fit(X_scaled)
evr = pca_full.explained_variance_ratio_
cum = evr.cumsum()

print("Variance held by first 5 PCs:", evr[:5].round(3))
for t in [0.80, 0.90, 0.95]:
    k = (cum < t).sum() + 1
    print(f"Components needed for {int(t*100)}% of the variance: {k}")
```

**Expected output:** PC1 holds roughly 12% of the variance, and it takes somewhere around 20 components to reach 80% and around 30 to reach 90% — down from 64. No single component dominates, which is itself worth pointing out.

### The scree + cumulative plot

```python
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].bar(range(1, 21), evr[:20], color="steelblue")
ax[0].set(title="Scree plot — variance per component",
          xlabel="Principal component", ylabel="Explained variance ratio")

ax[1].plot(range(1, 65), cum, marker=".", color="coral")
ax[1].axhline(0.90, color="red", ls="--", label="90% threshold")
ax[1].set(title="Cumulative explained variance",
          xlabel="Number of components kept", ylabel="Cumulative variance")
ax[1].legend()

plt.tight_layout(); plt.show()
```

The scree plot shows a steep drop then a long flat tail — that flattening is the "elbow". The cumulative plot is the one you actually make decisions from.

### PCA for visualisation — the payoff

```python
X_2d = PCA(n_components=2, random_state=42).fit_transform(X_scaled)

plt.figure(figsize=(7, 6))
sc = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap="tab10", s=12, alpha=0.7)
plt.colorbar(sc, label="True digit")
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.title("64 dimensions squashed into 2 — do the digits separate?")
plt.show()
```

**Live walk-through:** These two components hold only about a fifth of the total variance — and yet distinct digit blobs are clearly visible. Ask: *"Which digits overlap?"* (3, 5 and 8 typically smear into each other; 0 and 6 sit well apart.) *"That overlap is exactly where your classifier will make its mistakes — and you found it before training anything."*

### PCA for speed

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

Xtr, Xte, ytr, yte = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42, stratify=y)

full = LogisticRegression(max_iter=2000, random_state=42).fit(Xtr, ytr)
print(f"All 64 features  → accuracy {full.score(Xte, yte):.3f}")

pca = PCA(n_components=0.90, random_state=42).fit(Xtr)   # keep 90% of variance
Xtr_p, Xte_p = pca.transform(Xtr), pca.transform(Xte)
small = LogisticRegression(max_iter=2000, random_state=42).fit(Xtr_p, ytr)
print(f"{pca.n_components_} PCA comps → accuracy {small.score(Xte_p, yte):.3f}")
```

**Call out:** `n_components=0.90` is a float, not an int — sklearn reads it as "keep however many components I need for 90% of the variance." Accuracy drops a little; the feature count drops by half. *"Was that trade worth it here? Probably not — 64 columns is small. On 5,000 columns it absolutely is. PCA is a tool for wide data, not for every dataset."*

> ⚠️ **Fit the PCA on the training set only, then `transform` the test set.** Calling `fit_transform` on the full data before splitting is leakage — the test rows helped choose the axes. (For today's visualisation-only plot we fit on everything, which is fine because we are not scoring anything.)

---

## BREAK (10 min)

*Mull this over: you have 1,000 days of shop sales. You shuffle the rows and take a random 20% as your test set. Your R² comes out at 0.96. What, exactly, have you just proved?*

---

## Concept Block 3: Time Series — The Rows Are Not Independent (10 min)

### The one assumption that just broke

Everything in Sessions 1–10 assumed rows were **interchangeable**. Row 4 tells you nothing about row 5. That is why shuffling was harmless.

A time series violates this at its core: today's sales depend on yesterday's. **The order IS the data.**

### The cardinal sin — write it on the board and box it

```
      ┌──────────────────────────────────────────────┐
      │  NEVER: train_test_split(X, y, shuffle=True) │
      │         on time-ordered data                 │
      └──────────────────────────────────────────────┘

Shuffle → future rows land in TRAIN → model learns from tomorrow
        → test score is beautiful → deployment is a disaster
```

This is leakage (Session 2) in its purest, most seductive form. It does not look like a bug. It looks like a great model.

### The correct split

| | Ordinary data | Time series |
|---|---|---|
| Split | `train_test_split(shuffle=True)` | Slice by date: `df.iloc[:split]`, `df.iloc[split:]` |
| Cross-validation | `KFold` | `TimeSeriesSplit` |
| Test set is | a random sample | always the **most recent** stretch |

`TimeSeriesSplit(n_splits=5)` walks forward through time. Fold 1 trains on days 0–180 and tests on 181–360. Fold 2 trains on 0–360 and tests on 361–540. Training data only ever grows, and it always sits *before* the test window.

### The anatomy of a series

```
observed  =  trend  +  seasonality  +  noise

trend        the slow drift            sales grow 4% a year
seasonality  a fixed-length cycle      every Saturday; every monsoon
cyclical     a wave with no fixed length   multi-year booms
noise        whatever is left
```

**Stationarity, intuitively:** *the rules of the game are not changing.* Mean and variance stay put over time. A growing sales series is **not** stationary — its 2024 average is nowhere near its 2021 average. The standard fix is **differencing**: model the *change* (`df['sales'].diff()`) instead of the level. The level climbs forever; the day-to-day change hovers around a constant.

---

## Practical Block 3: Build the Series, Then Get Caught Cheating (15 min)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

dates = pd.date_range("2021-01-01", periods=1095, freq="D")   # 3 years, daily
t = np.arange(len(dates))

trend       = 500 + 0.4 * t                       # slow growth
seasonality =  80 * np.sin(2 * np.pi * t / 365.25)  # yearly wave
weekly      =  25 * np.sin(2 * np.pi * t / 7)       # weekly wave
noise       = np.random.normal(0, 20, len(dates))

df = pd.DataFrame(
    {"sales": (trend + seasonality + weekly + noise).round(2)},
    index=dates)
df.index.name = "date"

print(df.head())
df["sales"].plot(figsize=(12, 4), lw=0.8,
                 title="Daily sales — trend + yearly season + weekly season + noise")
plt.ylabel("Sales (₹ thousand)")
plt.show()
```

### Decomposition by hand — no extra library needed

```python
d = df.copy()
d["trend"]     = d["sales"].rolling(30, center=True).mean()   # smooth away the wiggles
d["detrended"] = d["sales"] - d["trend"]
d["seasonal"]  = d.groupby(d.index.dayofweek)["detrended"].transform("mean")
d["residual"]  = d["detrended"] - d["seasonal"]

fig, ax = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
for i, col in enumerate(["sales", "trend", "seasonal", "residual"]):
    ax[i].plot(d.index, d[col], lw=0.8)
    ax[i].set_ylabel(col)
ax[0].set_title("Decomposition: observed = trend + seasonal + residual")
plt.tight_layout(); plt.show()

print("Average weekday effect (0 = Monday):")
print(d.groupby(d.index.dayofweek)["detrended"].mean().round(2))
```

**Expected output:** the weekday-effect table shows clearly negative values midweek and clearly positive ones at the weekend — we have *rediscovered* the weekly sine wave we planted, using nothing but a rolling mean and a groupby.

### Now the trap

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

X = pd.DataFrame({"t": t,
                  "dayofweek": df.index.dayofweek,
                  "month": df.index.month}, index=df.index)
y = df["sales"]

# ---------- THE WRONG WAY ----------
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)
bad = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xtr, ytr)
p_bad = bad.predict(Xte)
print(f"SHUFFLED split  → MAE {mean_absolute_error(yte, p_bad):.2f}   R² {r2_score(yte, p_bad):.3f}")

# ---------- THE RIGHT WAY ----------
split = int(len(df) * 0.8)
good = RandomForestRegressor(n_estimators=100, random_state=42).fit(X.iloc[:split], y.iloc[:split])
p_good = good.predict(X.iloc[split:])
print(f"CHRONO   split  → MAE {mean_absolute_error(y.iloc[split:], p_good):.2f}   "
      f"R² {r2_score(y.iloc[split:], p_good):.3f}")
```

**Expected output:** the shuffled split reports an R² up around 0.96 and looks superb. The chronological split reports a **negative** R² — worse than just predicting the average. Same data, same model, same seed.

**Live walk-through — spend real time here.** *"The shuffled model was tested on 15 March using rows from 14 March and 16 March that it had already memorised. It never had to forecast anything. The moment we force it to face a genuinely unseen future, it collapses."*

Then push further: *"Why does the tree fail so badly on the honest split?"* → Because a Random Forest predicts by averaging training values. It **cannot extrapolate** past the largest value it has ever seen. The sales trend keeps climbing into the test period, and the forest is stuck predicting the past. This is a second, deeper lesson: on a trending series, tree models need the trend removed or a lag feature to lean on.

---

## Concept Block 4: Lag Features and the Baseline You Must Beat (10 min)

### Turning a series into a table

A raw series has no `X`. You build one, by pasting the past in as columns.

| Feature | Code | Meaning |
|---|---|---|
| `lag_1` | `df['sales'].shift(1)` | Yesterday |
| `lag_7` | `df['sales'].shift(7)` | Same weekday last week |
| `roll7_mean` | `df['sales'].shift(1).rolling(7).mean()` | Average of the last 7 days |
| `roll7_std` | `df['sales'].shift(1).rolling(7).std()` | How jumpy the last 7 days were |
| `dayofweek` | `df.index.dayofweek` | Calendar context |

Once those exist, `X` = the lag columns and `y` = `sales`, and every model from Sessions 3 and 7 works unchanged. **This is the single most useful practical skill in the session.**

> ⚠️ **`.shift(1)` BEFORE `.rolling()`.** A bare `df['sales'].rolling(7).mean()` includes *today's* value — the very thing you are predicting. Leakage, dressed up as a helpful feature.

The first few rows will be `NaN` (there is no "yesterday" for day one). `.dropna()` and move on.

### The persistence baseline

```
Prediction: tomorrow = today.
In code:    y_pred = X_test['lag_1']
```

Score it first, before you train anything. *That number is the bar.* An MAE of 18 means nothing on its own — it only means something once you know the do-nothing baseline scores 24. Many published forecasting models, in the real world, quietly fail to clear this bar.

**Where to go next (name-drop only):** **ARIMA** models the series directly using its own lags and differences. **Prophet** (from Meta) fits trend + seasonality + holidays with almost no configuration. Both are excellent, both are for another day — and neither will save you if you split your data wrong.

---

## Practical Block 4: Lags, Rolling Windows, Beat the Baseline (10 min)

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

feat = df[["sales"]].copy()

# --- lag features ---
for lag in [1, 2, 3, 7, 14]:
    feat[f"lag_{lag}"] = feat["sales"].shift(lag)

# --- rolling features (shift FIRST, then roll) ---
feat["roll7_mean"] = feat["sales"].shift(1).rolling(7).mean()
feat["roll7_std"]  = feat["sales"].shift(1).rolling(7).std()

# --- calendar features ---
feat["dayofweek"] = feat.index.dayofweek
feat["month"]     = feat.index.month

feat = feat.dropna()          # first 14 rows have no history
print(feat.shape)

X = feat.drop(columns="sales")
y = feat["sales"]

split = int(len(feat) * 0.8)                       # CHRONOLOGICAL — never shuffle
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]
print("train ends:", X_train.index[-1].date(), "| test starts:", X_test.index[0].date())
```

```python
# --- STEP 1: the baseline. Always first. ---
naive = X_test["lag_1"]                            # "tomorrow = today"
print(f"Naive persistence  MAE: {mean_absolute_error(y_test, naive):.2f}")

# --- STEP 2: now try to beat it ---
lr = LinearRegression().fit(X_train, y_train)
print(f"LinearRegression   MAE: {mean_absolute_error(y_test, lr.predict(X_test)):.2f}")

rf = RandomForestRegressor(n_estimators=200, random_state=42).fit(X_train, y_train)
print(f"RandomForest       MAE: {mean_absolute_error(y_test, rf.predict(X_test)):.2f}")
```

**Expected output:** the naive baseline lands in the mid-20s. Linear Regression comfortably beats it (high teens). The Random Forest also beats the baseline but — surprisingly — loses to plain Linear Regression, because it still cannot extrapolate the upward trend beyond its training range.

### Proper cross-validation for a series

```python
tscv = TimeSeriesSplit(n_splits=5)

for i, (tr, te) in enumerate(tscv.split(X)):
    print(f"fold {i}: train rows 0–{tr[-1]:>4} ({len(tr):>4}) | "
          f"test rows {te[0]:>4}–{te[-1]:>4} ({len(te)})")

scores = -cross_val_score(LinearRegression(), X, y, cv=tscv,
                          scoring="neg_mean_absolute_error")
print("MAE per fold:", scores.round(2))
print(f"Mean MAE: {scores.mean():.2f}")
```

**Live walk-through:** Print the fold boundaries and read them aloud. *"Look — the training window only ever grows, and the test window is always strictly after it. No fold ever peeks at the future. That is the whole idea."* Note that the first fold usually has the worst MAE — it has the least history to learn from, which is exactly what you would expect and exactly what a random `KFold` would have hidden from you.

**Closing question:** *"The Random Forest lost to a straight line. When would you actually want the forest?"* → When the relationship between lags and target is non-linear, and when the series is not dominated by a simple trend. The lesson is not "trees are bad" — it is "always run the baseline, and always let the honest split decide."

---

## Summary & Wrap-Up (5 min)

1. **The curse of dimensionality** — as columns grow, all distances converge, and distance-based models (KNN, K-Means) quietly stop working.
2. **PCA** finds the directions of maximum variance and keeps the first few. It **demands standardised features**, and it **costs you interpretability** — `PC1` is a blend, not a column you can name.
3. **`explained_variance_ratio_` + the cumulative plot** tell you how many components to keep. Two components for a picture; ~90–95% of variance for speed.
4. **In a time series, the rows are not independent.** `shuffle=True` leaks the future into the past and produces a beautiful, worthless score. Split chronologically; cross-validate with `TimeSeriesSplit`.
5. **Lag and rolling features** turn a series into an ordinary supervised table (`.shift()` then `.rolling()`), and **the persistence baseline** — tomorrow = today — is the bar every model must clear.

**Bridge:** *"You now have a shelf full of models and a lot of ways to prepare data for them. Next session — **Model Selection, Persistence & Module Review** — you'll learn how to systematically choose between them with GridSearchCV, and then how to `joblib.dump` the winner so it survives outside your notebook. That is the last step before a model becomes a product."*

---

## Q&A & Doubt Solving (5 min)

**Q: If PCA loses interpretability, why not just drop the columns with low variance and keep the names?**
→ You can, and that is called feature selection — it is a legitimate alternative. But low-variance columns are not necessarily useless columns, and PCA captures information that lives *across* columns (two features that always move together are one direction, not two). PCA finds structure that column-by-column selection cannot see.

**Q: How many components should I keep?**
→ There is no universal answer. Two if you are drawing a picture. Enough for 90–95% of the variance if you want speed with minimal loss. Or find the "elbow" on the scree plot where the bars flatten. In practice, treat `n_components` as a hyperparameter and tune it — which is exactly what next session's GridSearchCV is for.

**Q: My time-series model gets a great score. How do I know it isn't leaking?**
→ Three checks. (1) Did anything in your feature pipeline see the whole dataset before splitting — a scaler, a rolling mean without `.shift(1)`? (2) Is your test set strictly the *last* chunk by date? (3) Does it beat the persistence baseline by a *believable* margin? A model that beats "tomorrow = today" by 60% on real, noisy data is almost always leaking.

**Q: Can I use PCA and then KNN together?**
→ Yes — that is one of PCA's best uses. `make_pipeline(StandardScaler(), PCA(n_components=0.95), KNeighborsClassifier())`. The PCA step restores meaning to the distances KNN depends on. Just remember the pipeline fits PCA on the training fold only, which is precisely why you use a pipeline.

**Q: What about time series where I have several shops, each with its own sales column?**
→ Build lag features *per shop* (a `groupby('shop_id')` before the `.shift()`), then stack them into one long table with `shop_id` as a feature. The chronological-split rule still applies, and the split date must be the same for every shop.

---

## Instructor Notes

- **No downloads, no extra installs.** `load_digits` and `load_breast_cancer` ship with sklearn; the sales series is generated inline with `np.random.seed(42)`. `scipy.spatial.distance.pdist` (Practical 1) comes with scipy, which sklearn already depends on. **Do not** use `statsmodels.seasonal_decompose` — it is often not installed. The hand-rolled `rolling().mean()` decomposition in Practical 3 avoids the dependency entirely and teaches more.
- **Pacing:** Practical 3's shuffle-vs-chronological demo is the emotional centre of the session. If you are running behind, cut the scree plot's cosmetics or trim Practical 4's `TimeSeriesSplit` loop — but never cut the leakage demo.
- **The physical shadow demo in Concept 2 is worth the 60 seconds.** Students who see the bottle's shadow change never forget what a principal component is.
- **Expect a fight about the Random Forest losing to Linear Regression** in Practical 4. Lean into it. "Trees cannot extrapolate" is one of the most useful facts in applied ML and this is a rare chance to show it, not just assert it.
- **The single most common student mistake:** forgetting `StandardScaler` before `PCA`. It fails *silently* — you still get components, they are just wrong, dominated by whichever column happens to have the largest units. Pre-empt it by running PCA once *without* scaling on a dataset with mixed units and showing them a first component that explains 99% of the variance and means nothing at all.
- **Runner-up mistake:** `df['sales'].rolling(7).mean()` with no `.shift(1)`. It looks correct, produces a fantastic score, and is pure leakage. Make them say the rule out loud: *shift first, then roll.*
