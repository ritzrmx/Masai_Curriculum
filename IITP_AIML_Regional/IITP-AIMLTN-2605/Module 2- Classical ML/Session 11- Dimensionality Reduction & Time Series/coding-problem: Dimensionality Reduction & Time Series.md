# Coding Problem: Dimensionality Reduction & Time Series
> **Session 11 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A small product-quality dataset (4 numeric features, 8 samples) for PCA, plus a 12-month synthetic sales series for the trend check:

```python
import pandas as pd

data = {
    "weight_g":   [120, 135, 118, 250, 260, 245, 130, 255],
    "sugar_pct":  [2.1, 2.4, 1.9, 8.5, 9.1, 8.8, 2.2, 8.9],
    "acidity_ph": [3.4, 3.3, 3.5, 3.9, 4.0, 3.8, 3.4, 3.9],
    "shelf_days": [14, 15, 13, 30, 32, 29, 14, 31],
}
df = pd.DataFrame(data)

months = pd.date_range("2024-01-01", periods=12, freq="MS")
values = pd.Series(
    [100, 104, 108, 115, 121, 128, 133, 140, 146, 151, 158, 165],
    index=months
)
```

---

## Tasks

**Task 1 — Basic**
Print the **shape** of `df` and the **mean of every column**, rounded to 2 decimals.

**Task 2 — Basic**
Scale `df` with `StandardScaler`, fit `PCA(n_components=2, random_state=42)` on the scaled data, and print the **explained variance ratio** (rounded to 4 decimals) and the **total variance captured** by the 2 components (rounded to 4 decimals).

**Task 3 — Mid**
Compute a **3-month rolling mean** of `values` to identify the trend, and print it rounded to 2 decimals.

---

## Expected Output

```
Shape: (8, 4)

Column means:
weight_g      189.12
sugar_pct       5.49
acidity_ph      3.65
shelf_days     22.25
dtype: float64

Explained variance ratio: [0.9837 0.0153]
Total variance captured: 0.999

3-month rolling mean (trend):
2024-01-01       NaN
2024-02-01       NaN
2024-03-01    104.00
2024-04-01    109.00
2024-05-01    114.67
2024-06-01    121.33
2024-07-01    127.33
2024-08-01    133.67
2024-09-01    139.67
2024-10-01    145.67
2024-11-01    151.67
2024-12-01    158.00
Freq: MS, dtype: float64
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

data = {
    "weight_g":   [120, 135, 118, 250, 260, 245, 130, 255],
    "sugar_pct":  [2.1, 2.4, 1.9, 8.5, 9.1, 8.8, 2.2, 8.9],
    "acidity_ph": [3.4, 3.3, 3.5, 3.9, 4.0, 3.8, 3.4, 3.9],
    "shelf_days": [14, 15, 13, 30, 32, 29, 14, 31],
}
df = pd.DataFrame(data)

months = pd.date_range("2024-01-01", periods=12, freq="MS")
values = pd.Series(
    [100, 104, 108, 115, 121, 128, 133, 140, 146, 151, 158, 165],
    index=months
)

# Task 1
print("Shape:", df.shape)
print("\nColumn means:")
print(df.mean().round(2))

# Task 2
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)
pca = PCA(n_components=2, random_state=42)
pca.fit(X_scaled)
print("\nExplained variance ratio:", np.round(pca.explained_variance_ratio_, 4))
print("Total variance captured:", round(pca.explained_variance_ratio_.sum(), 4))

# Task 3
rolling_trend = values.rolling(window=3).mean()
print("\n3-month rolling mean (trend):")
print(rolling_trend.round(2))
```

</details>
