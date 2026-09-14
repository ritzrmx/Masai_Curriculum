# =============================================================
# Session 18: Data Preparation for ML
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually build this pipeline in code - same
# Swiggy partner dataset, now with city and vehicle type columns
# added.
#
# Syntax scope check: only uses Pandas/NumPy (Sessions 9-11) and
# train_test_split (Session 17), plus today's new tools: Pipeline,
# ColumnTransformer, OneHotEncoder, StandardScaler. Still no real
# estimator (LinearRegression/LogisticRegression are earned in
# Sessions 20 and 22, not before) - this pipeline intentionally
# ends at preprocessing.
# =============================================================

# --- SETUP ---
# Reusing the Session 17 Swiggy partner dataset pattern, now
# extended with two raw categorical columns: city and vehicle_type.
import pandas as pd
import numpy as np

np.random.seed(42)

n_partners = 200

df = pd.DataFrame({
    "partner_id": range(1, n_partners + 1),
    "city": np.random.choice(["Hyderabad", "Pune", "Chennai"], n_partners),
    "vehicle_type": np.random.choice(["Bike", "Scooter", "Bicycle"], n_partners),
    "orders_last_30_days": np.random.randint(0, 60, n_partners),
    "avg_rating": np.round(np.random.uniform(3.0, 5.0, n_partners), 2),
    "months_active": np.random.randint(1, 36, n_partners),
})

df["churned"] = (
    (df["orders_last_30_days"] < 10) & (df["avg_rating"] < 4.2)
).astype(int)

print(df.head())


# --- EXPLAIN ---
# Two of these columns are text with no meaningful order: city and
# vehicle_type. A model can't do math on words, so these need
# one-hot encoding (Concept Block 2). The numeric columns sit on
# very different ranges - orders up to 60, rating only 3.0 to 5.0 -
# so they'll need scaling (Concept Block 3).
# -------------------------------------------------------------

X = df[["city", "vehicle_type", "orders_last_30_days", "avg_rating", "months_active"]]
y = df["churned"]


# --- SETUP ---
from sklearn.model_selection import train_test_split

# --- EXPLAIN ---
# Notice we split BEFORE touching any preprocessing at all. This
# is not an accident - it's the whole point of today's closing
# concept (data leakage). Nothing downstream is allowed to see
# the test set until evaluation time.
# -------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining rows:", X_train.shape[0], "| Test rows:", X_test.shape[0])


# --- SETUP ---
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# --- EXPLAIN ---
# ColumnTransformer routes each column to the right treatment:
# categorical columns go to OneHotEncoder, numeric columns go to
# StandardScaler. Every raw column gets an explicit destination -
# leave one out and it silently disappears from the output.
# -------------------------------------------------------------

categorical_columns = ["city", "vehicle_type"]
numeric_columns = ["orders_last_30_days", "avg_rating", "months_active"]

preprocessor = ColumnTransformer(transformers=[
    ("categorical", OneHotEncoder(), categorical_columns),
    ("numeric", StandardScaler(), numeric_columns),
])

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
])


# --- EXPLAIN ---
# fit_transform on TRAIN teaches the encoder which categories exist
# and teaches the scaler the train-only mean/std. We then only
# transform() the test set - reusing what was learned from training,
# never re-fitting on test. This is the "split first, fit only on
# train, transform everywhere else" rule from Concept Block 5.
# -------------------------------------------------------------

X_train_prepared = pipeline.fit_transform(X_train)
X_test_prepared = pipeline.transform(X_test)

print("\nRaw training columns:", X_train.shape[1])
print("Prepared training columns (after one-hot expansion):", X_train_prepared.shape[1])
print("\nFirst prepared training row:\n", X_train_prepared[0])


# --- EXPLAIN ---
# Notice the column count grew - one-hot encoding expanded city (3
# categories) and vehicle_type (3 categories) into separate 0/1
# columns, while the numeric columns were rescaled in place. Every
# value here is now a plain number, ready for a model.
#
# What this demo does NOT do yet: it doesn't attach an actual
# estimator to this pipeline - that's Session 20 (Linear Regression),
# where we add exactly one more step to this same pipeline object.
# It also doesn't handle categories that might appear in production
# but never appeared during training - a real concern, but out of
# scope for today's fixed dataset.
# -------------------------------------------------------------
