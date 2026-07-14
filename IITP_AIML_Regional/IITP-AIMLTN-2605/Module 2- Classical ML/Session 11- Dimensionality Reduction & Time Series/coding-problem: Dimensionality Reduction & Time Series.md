# Coding Problem: Dimensionality Reduction & Time Series
> **Session 11 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

# --- Part A: a 10-column dataset for PCA ---
X, y = make_classification(n_samples=200, n_features=10, n_informative=3,
                           n_redundant=5, n_classes=2, random_state=42)

# --- Part B: 60 days of daily shop sales (trend + weekly cycle + noise) ---
np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=60, freq="D")
t = np.arange(60)
sales = 100 + 2 * t + 15 * np.sin(2 * np.pi * t / 7) + np.random.normal(0, 5, 60)

ts = pd.DataFrame({"sales": sales.round(1)}, index=dates)
ts.index.name = "date"
```

---

## Tasks

**Task 1 — Basic**
Standardise `X`, then fit `PCA(n_components=2)`. Print the `explained_variance_ratio_` (rounded to 3 decimals) and the **total** variance those 2 components capture.

**Task 2 — Basic**
Add two new columns to `ts`:
- `lag_1` — yesterday's sales
- `roll_7` — the mean of the **7 days ending yesterday** (shift *before* you roll)

Print the first 9 rows.

**Task 3 — Mid**
Drop the `NaN` rows, then split `ts` **chronologically** 80/20 (first 80% of dates train, last 20% test — no shuffling).
Print the MAE of the **naive persistence baseline** (`lag_1` used directly as the prediction), then fit a `LinearRegression` on `[lag_1, roll_7]` and print its test MAE. State whether the model beat the baseline.

---

## Expected Output

```
Explained variance ratio: [0.487 0.2  ]
Total variance captured by 2 components: 0.687

            sales  lag_1  roll_7
date
2023-01-01  102.5    NaN     NaN
2023-01-02  113.0  102.5     NaN
2023-01-03  121.9  113.0     NaN
2023-01-04  120.1  121.9     NaN
2023-01-05  100.3  120.1     NaN
2023-01-06   94.2  100.3     NaN
2023-01-07  108.2   94.2     NaN
2023-01-08  117.8  108.2  108.60
2023-01-09  125.4  117.8  110.79

train: 2023-01-08 -> 2023-02-18 (42 rows)
test : 2023-02-19 -> 2023-03-01 (11 rows)
Naive persistence MAE: 7.42
LinearRegression  MAE: 6.59
Beat the baseline? YES
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

X, y = make_classification(n_samples=200, n_features=10, n_informative=3,
                           n_redundant=5, n_classes=2, random_state=42)

np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=60, freq="D")
t = np.arange(60)
sales = 100 + 2 * t + 15 * np.sin(2 * np.pi * t / 7) + np.random.normal(0, 5, 60)
ts = pd.DataFrame({"sales": sales.round(1)}, index=dates)
ts.index.name = "date"

# --- Task 1: PCA (standardise FIRST — never skip this) ---
X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=2, random_state=42).fit(X_scaled)
print("Explained variance ratio:", pca.explained_variance_ratio_.round(3))
print(f"Total variance captured by 2 components: {pca.explained_variance_ratio_.sum():.3f}")

# --- Task 2: lag + rolling features (shift BEFORE rolling, or you leak today) ---
ts["lag_1"] = ts["sales"].shift(1)
ts["roll_7"] = ts["sales"].shift(1).rolling(7).mean()
print()
print(ts.head(9).round(2))

# --- Task 3: chronological split, baseline first, then the model ---
d = ts.dropna()
split = int(len(d) * 0.8)
train, test = d.iloc[:split], d.iloc[split:]      # NO shuffle — order is the data

print()
print("train:", train.index[0].date(), "->", train.index[-1].date(), f"({len(train)} rows)")
print("test :", test.index[0].date(), "->", test.index[-1].date(), f"({len(test)} rows)")

naive_mae = mean_absolute_error(test["sales"], test["lag_1"])   # "tomorrow = today"
print(f"Naive persistence MAE: {naive_mae:.2f}")

cols = ["lag_1", "roll_7"]
lr = LinearRegression().fit(train[cols], train["sales"])
model_mae = mean_absolute_error(test["sales"], lr.predict(test[cols]))
print(f"LinearRegression  MAE: {model_mae:.2f}")
print("Beat the baseline?", "YES" if model_mae < naive_mae else "NO")
```

</details>
