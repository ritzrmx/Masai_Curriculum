# Coding Problem: The ML Workflow, Data Prep & Reliability
> **Session 1 — Module 2: Classical ML** | ⏱ 5 mins

---

## Dataset

A small house-price dataset with one categorical column (`city`) and two numeric features:

```python
import pandas as pd

data = {
    "city":        ["Delhi", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune", "Delhi"],
    "area_sqft":   [850, 1200, 950, 1100, 1600, 800, 1400, 2000, 1000, 1250],
    "age_years":   [5, 2, 10, 8, 1, 15, 3, 0, 12, 6],
    "price_lakhs": [65, 110, 58, 82, 165, 48, 105, 210, 55, 92]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Separate the DataFrame into features `X` (everything except `price_lakhs`) and label `y` (`price_lakhs`). Print the shape of each and the list of feature column names.

**Task 2 — Basic**
One-hot encode the `city` column using `pd.get_dummies(..., drop_first=True)`. Print the resulting column names and the encoded DataFrame.

**Task 3 — Mid**
Split the encoded features into train/test sets (`test_size=0.2, random_state=42`). Fit a `StandardScaler` on `area_sqft` and `age_years` using **train only**, then transform both train and test. Print the train shape, test shape, the scaled train mean (rounded to 2 decimals), and the scaled test values (rounded to 2 decimals).

---

## Expected Output

```
X shape: (10, 3)
y shape: (10,)
Feature columns: ['city', 'area_sqft', 'age_years']

Encoded columns: ['area_sqft', 'age_years', 'city_Mumbai', 'city_Pune']
   area_sqft  age_years  city_Mumbai  city_Pune
0        850          5        False      False
1       1200          2         True      False
2        950         10        False       True
3       1100          8        False      False
4       1600          1         True      False
5        800         15        False       True
6       1400          3        False      False
7       2000          0         True      False
8       1000         12        False       True
9       1250          6        False      False

Train shape: (8, 4) Test shape: (2, 4)

Scaled train mean (should be ~0):
area_sqft    0.0
age_years    0.0
dtype: float64

Scaled test values:
   area_sqft  age_years
8      -0.63       1.29
1      -0.11      -0.86
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = {
    "city":        ["Delhi", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune", "Delhi"],
    "area_sqft":   [850, 1200, 950, 1100, 1600, 800, 1400, 2000, 1000, 1250],
    "age_years":   [5, 2, 10, 8, 1, 15, 3, 0, 12, 6],
    "price_lakhs": [65, 110, 58, 82, 165, 48, 105, 210, 55, 92]
}
df = pd.DataFrame(data)

# Task 1
X = df.drop(columns=["price_lakhs"])
y = df["price_lakhs"]
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Feature columns:", list(X.columns))

# Task 2
X_encoded = pd.get_dummies(X, columns=["city"], drop_first=True)
print("\nEncoded columns:", list(X_encoded.columns))
print(X_encoded)

# Task 3
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)
print("\nTrain shape:", X_train.shape, "Test shape:", X_test.shape)

num_cols = ["area_sqft", "age_years"]
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

print("\nScaled train mean (should be ~0):")
print(X_train_scaled[num_cols].mean().round(2) + 0.0)
print("\nScaled test values:")
print(X_test_scaled[num_cols].round(2))
```

</details>
