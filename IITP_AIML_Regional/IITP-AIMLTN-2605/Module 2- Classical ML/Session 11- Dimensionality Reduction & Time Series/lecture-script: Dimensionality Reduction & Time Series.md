# Lecture Script: Dimensionality Reduction & Time Series
> **Instructor Reference** — Module 2: Classical ML | Session 11 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can compress a high-dimensional numeric dataset into 2 principal components for visualization using PCA, and can identify trend and seasonality in a time series while understanding why it must be split chronologically, never randomly.

**Student profile at this point:** Comfortable with `train_test_split`, `StandardScaler`, and `fit`/`predict` from earlier sessions. Have built regression and classification models, ensembles, evaluated with classification metrics, run K-Means/hierarchical clustering, and just finished a masterclass on probability and Bayes. This is the first time they touch dimensionality reduction or sequential/time-indexed data.

**Key outcome:** By end of class, every student can (1) scale a dataset, fit `PCA(n_components=2)`, read `explained_variance_ratio_`, and decide how many components to keep; and (2) build and read a trend + seasonality decomposition, and correctly split a time series by time order instead of shuffling it.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Curse of Dimensionality & What "Variance" Means | 10 min | 0:15 |
| **Practical 1:** Load, Scale, and First PCA Fit | 15 min | 0:30 |
| **Concept 2:** Reading PCA Output — Ratio, Loadings, Cumulative Variance | 10 min | 0:40 |
| **Practical 2:** 2D Scatter, Cumulative Variance & Choosing k | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Time Series Building Blocks — Trend & Seasonality | 10 min | 1:15 |
| **Practical 3:** Build & Decompose a Synthetic Time Series | 15 min | 1:30 |
| **Concept 4:** Why Time Order Matters for Splitting | 10 min | 1:40 |
| **Practical 4:** Correct vs Wrong Split + Baseline Forecast | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Load the Wine dataset and show its shape on screen:

```
Shape: (178, 13)
```

Ask the class: *"Thirteen numeric features per wine sample. If I want to see, in ONE plot, whether the three wine cultivars form separable groups — how many scatter plots would I need to check every pair of features?"* Let them compute `13 choose 2 = 78`. Nobody wants to look at 78 scatter plots, and even then, a pair of features is only 2 out of 13 — the interesting structure might be spread across all of them at once.

**Second hook:** Show a simple monthly sales series climbing steadily with visible seasonal bumps. Ask: *"If I want to test whether my forecasting model works, can I just do `train_test_split(shuffle=True)` like we did all module?"* Let a few students guess. Hold the answer — we come back to this in the second half.

**Context to set:** Today has two halves that are more connected than they look. Both are about **structure hiding in numbers**: PCA finds the hidden directions where a dataset spreads out the most; time series decomposition finds the hidden trend and cycle inside a sequence of values. Both matter constantly in real ML work — PCA before clustering or visualization, time awareness before any forecasting or monitoring system.

**Learning contract for today:**
- Explain why PCA compresses correlated features into fewer components without losing much information
- Fit `PCA` in scikit-learn, read `explained_variance_ratio_`, and decide how many components to keep
- Build a synthetic time series and separate it into trend, seasonality, and noise
- Explain — and demonstrate — why time series must be split by time order, never shuffled

---

## Concept Block 1: Curse of Dimensionality & What "Variance" Means (10 min)

### The Curse of Dimensionality

As the number of features grows, three things get worse at once:

| Problem | What happens |
|---|---|
| **Visualization** | Humans can plot 2D or 3D. Beyond that, we're guessing. |
| **Sparsity** | Points spread thinly across a huge feature space — "nearest neighbor" becomes less meaningful. |
| **Redundancy** | Many features move together (correlated) — e.g. `total_phenols` and `flavanoids` in a wine dataset both measure related chemistry. Highly correlated features carry duplicate information. |

**Teaching point:** More features is not automatically more information. Correlated features often encode the *same* underlying signal multiple times. Dimensionality reduction tries to find a smaller number of new axes that keep the signal and drop the redundancy.

### Variance = Spread = Information

In PCA, **variance is our proxy for "how much information a direction carries."** A feature (or a direction in feature space) with high variance separates observations from each other; a feature with near-zero variance says almost the same thing about every row and isn't doing much work for us.

```
Low variance direction:  •  •  •  •  •   (barely spreads → little info)
High variance direction: •      •      •      •   (spreads a lot → informative)
```

**PCA's central idea:** Instead of keeping or dropping original columns, *rotate* the coordinate system to find new axes — called **principal components** — such that the first axis (PC1) captures the maximum possible variance, the second axis (PC2) captures the maximum variance *left over* after removing PC1, and so on. Each principal component is a weighted combination of ALL original features, not a single existing column.

```
Original correlated cloud (2 features):     After PCA rotation:

        y                                        PC2
        |    ● ●●                                 |
        |  ●●●●●●●                     ──────●●●●●●●●●●●●────── PC1
        | ●●●●●●●                                 |
        |●●●                                      |
        └────────── x               PC1 = direction of max spread
                                     PC2 = perpendicular, max remaining spread
```

**Critical prerequisite — scaling:** PCA is driven purely by variance, and variance is sensitive to units. A feature measured in the hundreds (e.g. `proline`, ranging 278–1680 in the Wine dataset) will dominate a feature measured in single digits (e.g. `hue`, ranging 0.48–1.71) purely because of scale, not because it's more informative. **Always `StandardScaler` before PCA.** This is the same scaling instinct from earlier sessions — just applied for a new reason.

---

## Practical Block 1: Load, Scale, and First PCA Fit (15 min)

### Dataset

We use `sklearn.datasets.load_wine()` — 178 wine samples, 13 numeric chemistry features (alcohol, acidity, phenols, color intensity, proline, etc.), 3 cultivar classes. It's fully self-contained (no internet needed) and has exactly the "too many features, wildly different scales" problem we just described.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

wine = load_wine(as_frame=True)
X = wine.data
y = wine.target
target_names = wine.target_names

print("Shape:", X.shape)
print("\nClass counts:")
print(pd.Series(y).value_counts().sort_index())
```

**Output:**
```
Shape: (178, 13)

Class counts:
target
0    59
1    71
2    48
Name: count, dtype: int64
```

### Show the scale problem directly

```python
print("Feature scales (min/max wildly different):")
print(X.describe().loc[['min', 'max']].T)
```

**Output (excerpt):**
```
                                 min      max
alcohol                        11.03    14.83
malic_acid                      0.74     5.80
ash                              1.36     3.23
alcalinity_of_ash               10.60    30.00
magnesium                       70.00   162.00
total_phenols                    0.98     3.88
flavanoids                       0.34     5.08
nonflavanoid_phenols             0.13     0.66
proanthocyanins                  0.41     3.58
color_intensity                  1.28    13.00
hue                              0.48     1.71
od280/od315_of_diluted_wines     1.27     4.00
proline                        278.00  1680.00
```

**Ask the class:** *"If I ran PCA on this right now, without scaling, which feature do you think would dominate PC1?"* → `proline`, purely because its numbers are hundreds of times larger, not because it's more chemically informative.

### Scale, then fit PCA

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Scaled mean (first 5, ~0):", np.round(X_scaled.mean(axis=0)[:5], 4))
print("Scaled std  (first 5, ~1):", np.round(X_scaled.std(axis=0)[:5], 4))

pca2 = PCA(n_components=2, random_state=42)
X_pca2 = pca2.fit_transform(X_scaled)

print("\nX_pca2 shape:", X_pca2.shape)
print("Explained variance ratio (2 comps):", np.round(pca2.explained_variance_ratio_, 4))
print("Total variance captured by 2 comps:", round(pca2.explained_variance_ratio_.sum(), 4))
```

**Output:**
```
Scaled mean (first 5, ~0): [ 0.  0. -0. -0. -0.]
Scaled std  (first 5, ~1): [1. 1. 1. 1. 1.]

X_pca2 shape: (178, 2)
Explained variance ratio (2 comps): [0.362  0.1921]
Total variance captured by 2 comps: 0.5541
```

**Walk through this together:** We went from 13 columns to 2, and those 2 new columns still capture 55.41% of the total variance in the original 13-dimensional space. PC1 alone captures 36.2%, PC2 an additional 19.21%.

**Discussion prompt:** *"Is 55% 'good enough'? What would you want to know before answering that?"* → depends on what we're using it for — quick visual EDA can tolerate losing 45% of variance; feeding into a downstream model usually wants more.

---

## Concept Block 2: Reading PCA Output — Ratio, Loadings, Cumulative Variance (10 min)

### `explained_variance_ratio_` — what the number actually means

Each entry is *"the fraction of total dataset variance captured by this one component,"* and the components are always ordered from most to least informative. They also sum to 1.0 across **all** components (no variance is ever lost if you keep all of them — PCA is just a rotation).

### Components are not original features — they're recipes

`pca.components_` gives the "recipe" (loadings) for each principal component: how much of each original (scaled) feature is mixed in. A student-friendly framing:

```
PC1 ≈ 0.14·alcohol − 0.24·malic_acid + 0.00·ash − 0.24·alcalinity_of_ash + ...
```

**Teaching point:** You cannot say "PC1 is the alcohol axis." PC1 is a *blend* of all 13 features, weighted by how much each contributes to the direction of maximum spread. This is the main interpretability trade-off of PCA — you gain a clean 2D plot, you lose the ability to say "this axis is simply feature X."

### Cumulative variance — deciding how many components to keep

Fit PCA with **no** `n_components` limit to see every component's contribution, then look at the running total:

| Concept | Formula |
|---|---|
| Individual ratio | `explained_variance_ratio_[i]` |
| Cumulative ratio | `np.cumsum(explained_variance_ratio_)` |
| Rule of thumb | keep enough components to cross 90–95% cumulative variance |

```
Variance kept
   1.0 ┤                                  ●───●───●───●
       │                          ●───●
   0.9 ┤                  ●───●                          ← typical cutoff line
       │              ●
   0.7 ┤          ●
       │      ●
   0.4 ┤  ●
       │●
   0.0 └──────────────────────────────────────────────────
        1   2   3   4   5   6   7   8   9  10  11  12  13
                      number of components kept
```

**Teaching point:** This "elbow"-style curve is the PCA equivalent of the elbow plot they saw in K-Means. Early components add a lot of variance quickly; later ones add very little. The bend is where you usually stop.

---

## Practical Block 2: 2D Scatter, Cumulative Variance & Choosing k (15 min)

### Visualize the 2D projection, colored by class

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 5))
scatter = plt.scatter(X_pca2[:, 0], X_pca2[:, 1], c=y, cmap='viridis', edgecolor='k', alpha=0.8)
plt.xlabel(f"PC1 ({pca2.explained_variance_ratio_[0]*100:.1f}% variance)")
plt.ylabel(f"PC2 ({pca2.explained_variance_ratio_[1]*100:.1f}% variance)")
plt.title("Wine dataset — 13 features compressed to 2 principal components")
plt.legend(handles=scatter.legend_elements()[0], labels=list(target_names))
plt.show()
```

Confirm the visual separation numerically by checking each class's average position:

```python
df_pca = pd.DataFrame(X_pca2, columns=['PC1', 'PC2'])
df_pca['class'] = [target_names[i] for i in y]
print(df_pca.groupby('class')[['PC1', 'PC2']].mean().round(2))
```

**Output:**
```
          PC1   PC2
class
class_0  2.28  0.97
class_1 -0.04 -1.64
class_2 -2.75  1.24
```

**Describe what the plot shows:** three visibly separated clouds along PC1 — `class_0` sits furthest right (PC1 ≈ 2.28), `class_2` furthest left (PC1 ≈ -2.75), and `class_1` in the middle but pulled downward on PC2 (-1.64). Even though PC1+PC2 only capture 55% of total variance, the dominant chemical differences between cultivars happen to align with those first two directions — that's why the plot still shows clean separation.

**Teaching point (important limit):** PCA is **unsupervised** — it never looks at `y` while fitting. The fact that classes separate nicely here is a (common but not guaranteed) side effect of class differences being the dominant source of variance in this dataset. On a noisier dataset, PC1/PC2 might capture variance that has nothing to do with the label you care about.

### Cumulative variance — how many components would you actually keep?

```python
pca_full = PCA(random_state=42)
pca_full.fit(X_scaled)
cum_var = np.cumsum(pca_full.explained_variance_ratio_)

print("Explained variance ratio per component:")
print(np.round(pca_full.explained_variance_ratio_, 4))
print("\nCumulative explained variance:")
print(np.round(cum_var, 4))

n_for_90 = np.argmax(cum_var >= 0.90) + 1
n_for_95 = np.argmax(cum_var >= 0.95) + 1
print(f"\nComponents needed for >=90% variance: {n_for_90}")
print(f"Components needed for >=95% variance: {n_for_95}")
```

**Output:**
```
Explained variance ratio per component:
[0.362  0.1921 0.1112 0.0707 0.0656 0.0494 0.0424 0.0268 0.0222 0.0193
 0.0174 0.013  0.008 ]

Cumulative explained variance:
[0.362  0.5541 0.6653 0.736  0.8016 0.851  0.8934 0.9202 0.9424 0.9617
 0.9791 0.992  1.    ]

Components needed for >=90% variance: 8
Components needed for >=95% variance: 10
```

**Discussion prompt:** *"We needed 8 of the 13 original components to hit 90% variance — is PCA still 'worth it' here?"* → For visualization, 2 components was clearly worth it. For feeding a downstream model, going from 13 to 8 features is a much smaller win — sometimes PCA isn't worth the interpretability cost if the dataset doesn't have much redundancy to begin with.

---

## BREAK (10 min)

*Suggested break prompt — ask students to think of one real sequence of numbers they've personally seen that goes up-and-down repeatedly over time (their monthly phone bill, a city's temperature, app downloads, cricket team's win rate per season). They'll share one after the break — this primes the "trend vs seasonality" framing.*

---

## Concept Block 3: Time Series Building Blocks — Trend & Seasonality (10 min)

### What makes a time series different from a normal dataset

Every row we've worked with this module (Titanic-style tables, wine samples) is **independent** — shuffling the rows changes nothing about what the data means. A **time series** is a sequence of values where **order carries information** — each point is related to its neighbors in time, and shuffling destroys the very thing we're trying to model.

### The Decomposition Idea

A time series can (approximately) be broken into three additive pieces:

```
  Observed Series  =  Trend  +  Seasonality  +  Noise/Residual

     ╱╲  ╱╲  ╱╲                                    small random
   ╱╲  ╲╱  ╲╱  ╲╱╲        ___________              wiggle left
  ╱                  ≈   ╱          + repeating  + over after
                        ╱  (long-run  wave pattern   removing
                        direction)   (fixed period)  trend+season
```

| Component | Meaning | Example |
|---|---|---|
| **Trend** | The long-run direction, ignoring short-term ups/downs | Sales steadily growing 3–4% a month over 4 years |
| **Seasonality** | A pattern that repeats at a **fixed period** | Ice cream sales spike every summer, every year |
| **Residual / Noise** | Whatever is left after removing trend and seasonality | Day-to-day randomness, one-off events |

**Teaching point:** "Seasonality" doesn't have to mean literal seasons — it means *any* fixed, repeating period: hourly patterns in web traffic (busy at 9am, quiet at 3am), weekly patterns in restaurant bookings (busy Friday, quiet Monday), or yearly patterns in retail sales. The key is that the period is **fixed and known** (e.g. 12 months, 7 days, 24 hours).

**A simple way to estimate trend:** a **rolling mean** (moving average) smooths out short-term noise and seasonal bumps, leaving the long-run direction behind. A simple way to estimate seasonality: after removing the trend, average what's left, grouped by the position in the cycle (e.g. average the "January leftovers" across every year in the data).

---

## Practical Block 3: Build & Decompose a Synthetic Time Series (15 min)

### Build a synthetic monthly series: trend + yearly seasonality + noise

We build this ourselves with `pd.date_range` and `numpy` — fully self-contained, no external data needed.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n_months = 48  # 4 years of monthly data
dates = pd.date_range(start="2022-01-01", periods=n_months, freq="MS")
t = np.arange(n_months)

trend = 200 + 3.5 * t                          # steady upward trend
seasonality = 40 * np.sin(2 * np.pi * t / 12)  # repeats every 12 months
noise = rng.normal(0, 8, n_months)              # random noise

sales = trend + seasonality + noise
ts = pd.Series(sales, index=dates, name="sales")

print(ts.head(6).round(2))
print("\nDescribe:")
print(ts.describe().round(2))
```

**Output:**
```
2022-01-01    202.44
2022-02-01    215.18
2022-03-01    247.64
2022-04-01    258.02
2022-05-01    233.03
2022-06-01    227.08
Freq: MS, Name: sales, dtype: float64

Describe:
count     48.00
mean     282.89
std       53.01
min      184.68
25%      240.37
50%      282.91
75%      326.29
max      381.70
Name: sales, dtype: float64
```

### Estimate trend with a rolling mean, then detrend

```python
trend_est = ts.rolling(window=12, center=True).mean()
print("Rolling trend (first 15):")
print(trend_est.head(15).round(2))

detrended = ts - trend_est
print("\nDetrended (first 15):")
print(detrended.head(15).round(2))
```

**Output:**
```
Rolling trend (first 15):
2022-01-01       NaN
2022-02-01       NaN
2022-03-01       NaN
2022-04-01       NaN
2022-05-01       NaN
2022-06-01       NaN
2022-07-01    218.12
2022-08-01    221.46
2022-09-01    226.40
2022-10-01    229.71
2022-11-01    232.01
2022-12-01    237.06
2023-01-01    240.79
2023-02-01    244.79
2023-03-01    248.47
Freq: MS, Name: sales, dtype: float64

Detrended (first 15):
2022-01-01      NaN
2022-02-01      NaN
2022-03-01      NaN
2022-04-01      NaN
2022-05-01      NaN
2022-06-01      NaN
2022-07-01     3.91
2022-08-01   -19.49
2022-09-01   -33.18
2022-10-01   -45.04
2022-11-01   -24.62
2022-12-01   -12.34
2023-01-01     1.74
2023-02-01    29.73
2023-03-01    38.91
Freq: MS, Name: sales, dtype: float64
```

**Explain the NaNs:** a `center=True` window of 12 needs 6 months on either side, so the first and last 6 months of the series have no trend estimate. This is a real trade-off of rolling-mean decomposition — you lose the edges.

### Extract seasonality by averaging the detrended residual per calendar month

```python
seasonal_by_month = detrended.groupby(detrended.index.month).mean()
print("Seasonal component by month:")
print(seasonal_by_month.round(2))

residual = ts - trend_est - ts.index.month.map(seasonal_by_month).values
print("\nResidual stats (should hover near 0):")
print(residual.describe().round(2))
```

**Output:**
```
Seasonal component by month:
1     -0.66
2     20.62
3     35.78
4     41.06
5     39.11
6     20.44
7      6.08
8    -20.81
9    -35.34
10   -44.70
11   -25.77
12   -14.30
Name: sales, dtype: float64

Residual stats (should hover near 0):
count    37.00
mean     -0.00
std       4.44
min     -10.42
25%      -2.98
50%       1.32
75%       2.29
max      10.73
dtype: float64
```

**Walk through it:** the seasonal component peaks around April (+41.06) and bottoms out around October (-44.70) — matching the `sin` wave we injected. After removing trend AND seasonality, what's left (`residual`) has mean ≈ 0 and a small spread (std ≈ 4.4) — that's the noise we added with `rng.normal(0, 8, ...)`, shrunk by averaging.

**Note for the class:** production libraries like `statsmodels.tsa.seasonal_decompose()` automate exactly this (rolling mean + per-period averaging). We built it by hand so the mechanics are transparent — once you understand this, the library call is just a shortcut.

---

## Concept Block 4: Why Time Order Matters for Splitting (10 min)

### The leakage problem, revisited

Back in Module 1 we discussed data leakage — information from outside the training data sneaking in and making validation scores look better than they really are. Time series has its own dedicated version of this problem.

```
CORRECT — chronological split:              WRONG — random shuffle split:

|-------- TRAIN --------|--- TEST ---|      TRAIN: ▓ ░ ▓ ▓ ░ ▓ ░ ░ ▓ ░ ▓ ░
Jan22 ............... Dec24 | Jan25...Dec25   TEST:  ░ ▓ ░ ░ ▓ ░ ▓ ▓ ░ ▓ ░ ▓
     (only past)         (only future)       (both scattered across all 4 years)
```

**Teaching point:** If you shuffle a time series before splitting, your "test" set ends up containing months from years the model already trained on. The model isn't being asked to *forecast the unseen future* anymore — it's just interpolating between points it has effectively already seen (an earlier and later month from the same year, same season). Validation metrics will look artificially good and will **not** reflect real forecasting performance.

**The correct approach:** split by time order — all of the earliest data in `train`, all of the most recent data in `test`. In production settings, teams often go further with **walk-forward validation** (retrain repeatedly, always testing on the next unseen chunk) — a concept worth naming here even though we'll only do a single chronological split today.

**Bridge back:** *"This is the exact same leakage principle from Module 1 — information from the 'future' (relative to a prediction point) must never touch training. Time series just makes the rule concrete and easy to violate accidentally with a single `shuffle=True`."*

---

## Practical Block 4: Correct vs Wrong Split + Baseline Forecast (10 min)

### Show the wrong way first

```python
shuffled = ts.sample(frac=1.0, random_state=42)
wrong_train_idx = shuffled.index[:36]
wrong_test_idx = shuffled.index[36:]

print("Random-split TRAIN years present:", sorted(set(wrong_train_idx.year)))
print("Random-split TEST years present :", sorted(set(wrong_test_idx.year)))
print("Test years already seen in training:",
      set(wrong_test_idx.year) <= set(wrong_train_idx.year))
```

**Output:**
```
Random-split TRAIN years present: [2022, 2023, 2024, 2025]
Random-split TEST years present : [2022, 2023, 2024, 2025]
Test years already seen in training: True
```

**Point at this directly:** every single year appears in both train AND test. The model has already "met" data from every season it's being tested on.

### Now the correct way — split by time, then build a simple baseline forecast

```python
split_point = 36  # first 36 months train, last 12 months test
train, test = ts.iloc[:split_point], ts.iloc[split_point:]

print("Train range:", train.index.min().date(), "to", train.index.max().date())
print("Test range :", test.index.min().date(), "to", test.index.max().date())

# Baseline forecast: fit a trend line on TRAIN only, add back the seasonal
# pattern learned from TRAIN only (never touch test data while "fitting")
train_t = np.arange(split_point)
slope, intercept = np.polyfit(train_t, train.values, 1)
print("\nTrend fit on TRAIN only -> slope:", round(slope, 3), "intercept:", round(intercept, 3))

test_t = np.arange(split_point, n_months)
trend_forecast = slope * test_t + intercept
seasonal_forecast = test.index.month.map(seasonal_by_month).values
forecast = trend_forecast + seasonal_forecast

mae = np.mean(np.abs(test.values - forecast))
print("\nTest actual   (first 6):", np.round(test.values[:6], 2))
print("Forecast      (first 6):", np.round(forecast[:6], 2))
print("MAE on chronological test set:", round(mae, 2))
```

**Output:**
```
Train range: 2022-01-01 to 2024-12-01
Test range : 2025-01-01 to 2025-12-01

Trend fit on TRAIN only -> slope: 2.946 intercept: 210.281

Test actual   (first 6): [325.09 342.78 361.05 381.7  380.59 367.85]
Forecast      (first 6): [315.69 339.91 358.02 366.24 367.24 351.52]
MAE on chronological test set: 11.68
```

**Discussion prompt:** *"An MAE of 11.68 on values averaging ~283 — is that a good forecast?"* → roughly a 4% average error, which is a reasonable baseline for a hand-built trend+seasonal model. The point isn't the exact number — it's that this MAE is **trustworthy** because the test months genuinely came after every training month, unlike the shuffled version.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- The curse of dimensionality: too many correlated features make visualization and distance-based reasoning unreliable
- Variance = information; PCA rotates the feature space to find directions (principal components) of maximum variance
- Always `StandardScaler` before PCA — unscaled large-magnitude features dominate for the wrong reasons
- `explained_variance_ratio_` and its cumulative sum tell you how many components to keep (90–95% is a common target)
- A 2D PCA scatter plot is a fast, honest way to check whether classes/clusters separate in a high-dimensional dataset
- Time series = Trend + Seasonality + Noise; rolling mean isolates trend, averaging the detrended residual by period isolates seasonality
- Time series must be split **chronologically**, never shuffled — shuffling leaks future information into training and produces misleadingly optimistic validation

**Bridge to next session:** *"Next class is the final session of Module 2 — Model Selection, Persistence & Module Review. We'll take everything built this module — regression, classification, ensembles, clustering, and today's PCA — and formalize how to properly select the best model, then learn to save and reload trained models with `joblib` so they survive beyond a single notebook session."*

**Homework / self-practice:**
1. Run the same PCA workflow on `sklearn.datasets.load_breast_cancer()`. Report the cumulative variance table and how many components are needed to reach 95%.
2. Build your own synthetic time series (pick a different trend slope, seasonal period, and noise level), decompose it into trend + seasonality, then perform a correct chronological train/test split and compute the baseline forecast MAE.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Do we lose interpretability when we use PCA?**
→ Yes — a principal component is a weighted blend of every original feature, not one recognizable column. You can inspect `pca.components_` to see the weights, but explaining "PC1" to a non-technical stakeholder is much harder than explaining "customer age."

**Q: Should I always scale before PCA?**
→ Almost always, unless every feature is already naturally on the same scale and unit (e.g. all percentages 0–100). When in doubt, scale — an unscaled PCA is usually dominated by whichever feature happens to have the largest numeric range.

**Q: How do I decide exactly how many components to keep?**
→ There's no universal number. Common approaches: target a cumulative variance threshold (90–95%), look for the "elbow" in the scree plot where returns drop off sharply, or simply keep however many a downstream model needs (2 for a plot, more for a model).

**Q: Can I feed PCA output straight into a classifier?**
→ Yes — PCA is often used exactly this way as a preprocessing step to reduce noise/redundancy before a supervised model. Just remember PCA itself never looks at the label; it only reduces the feature space.

**Q: What's actually different between "trend" and "seasonality" if both cause the values to go up and down?**
→ Trend is the smooth, long-run direction once you ignore short cycles — it doesn't repeat. Seasonality repeats at a **fixed, known period** (every 12 months, every 7 days). If you can name the period, it's seasonality; if it's a slow, one-directional drift, it's trend.

**Q: Why exactly does shuffling ruin a time series split — the math still runs fine?**
→ The code runs fine, that's the trap. The problem is what the numbers *mean*: a forecasting model is supposed to predict values it hasn't seen yet, using only the past. A shuffled split lets training data sit chronologically *after* some test points, so the "test" score reflects interpolation between known points, not genuine forecasting — it will not match real-world performance when deployed.

---

## Instructor Notes

- **Dataset choices:** `load_wine()` was chosen over `load_breast_cancer()` for the PCA half because 3 classes give a visibly richer scatter plot than 2, and 13 features (vs 30) keep printed output readable on a projector. The synthetic time series is fully generated with `numpy`/`pandas` — no internet access needed, and the trend/seasonal/noise parameters are visible in the code so students can tweak and re-run instantly.
- **Common student mistake (PCA):** fitting `PCA` before `StandardScaler`, or fitting the scaler on the whole dataset instead of train-only in a real pipeline. For today's EDA-style use this is fine (no leakage risk since there's no train/test split for the PCA half), but flag it explicitly: *"If this were feeding a model with train/test, you'd fit the scaler and PCA on train only, then `.transform()` test."*
- **Common student mistake (time series):** calling `.rolling(window=12)` without `center=True` and being confused why the trend line looks "shifted" relative to the data. Show both settings side by side if time allows.
- **Live-coding tip:** Deliberately skip `StandardScaler` once on the wine data, rerun PCA, and show `explained_variance_ratio_` change dramatically (PC1 will look almost entirely driven by `proline`). This lands the scaling lesson far better than just stating it.
- **For advanced students:** Have them inspect `pca.components_[0]` sorted by absolute weight to see which original features contribute most to PC1 — a light bridge into "loadings" without a full linear algebra detour. For time series, challenge them to implement `statsmodels.tsa.seasonal_decompose`-style output purely with `pandas`/`numpy` (which is exactly what Practical Block 3 already does) and compare against `statsmodels` if it happens to be installed on their machine.
- **Time check contingency:** If running behind after the break, compress Practical Block 4 to just the "wrong vs correct split" comparison and assign the baseline-forecast MAE calculation as part of the homework.
