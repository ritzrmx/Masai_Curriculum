# =============================================================
# Session 22: Logistic Regression
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually attach a real classifier to the
# Session 18 pipeline skeleton and watch the threshold change
# our decisions in real time.
#
# Syntax scope check: reuses train_test_split (Session 17),
# Pipeline + ColumnTransformer + OneHotEncoder + StandardScaler
# (Session 18), plus today's new tool: LogisticRegression and
# predict_proba(). No precision/recall/confusion matrix yet -
# those are earned in Session 23.
# =============================================================

# --- SETUP ---
# Rebuilding the exact Session 18 Swiggy partner dataset: city and
# vehicle_type (categorical) plus orders/rating/months (numeric),
# predicting churned (0/1) - same scenario as Sessions 17-18.
import numpy as np
import pandas as pd

np.random.seed(42)

n_partners = 300

df = pd.DataFrame({
    "city": np.random.choice(["Hyderabad", "Pune", "Chennai"], n_partners),
    "vehicle_type": np.random.choice(["Bike", "Scooter", "Bicycle"], n_partners),
    "orders_last_30_days": np.random.randint(0, 60, n_partners),
    "avg_rating": np.round(np.random.uniform(3.0, 5.0, n_partners), 2),
    "months_active": np.random.randint(1, 36, n_partners),
})

df["churned"] = (
    (df["orders_last_30_days"] < 15) & (df["avg_rating"] < 4.3)
).astype(int)

print(f"Churn rate in this sample: {df['churned'].mean():.2%}")


# --- SETUP ---
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

X = df.drop(columns="churned")
y = df["churned"]

# --- EXPLAIN ---
# Same Session 17 habit: split first. stratify=y keeps the churn
# rate balanced between train and test, since churners are a
# minority class here.
# -------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# --- EXPLAIN ---
# This is the EXACT Session 18 pipeline skeleton - ColumnTransformer
# routing categorical columns to OneHotEncoder and numeric columns
# to StandardScaler - now finally complete with a real estimator
# as the last step: LogisticRegression.
# -------------------------------------------------------------

categorical_columns = ["city", "vehicle_type"]
numeric_columns = ["orders_last_30_days", "avg_rating", "months_active"]

preprocessor = ColumnTransformer(transformers=[
    ("categorical", OneHotEncoder(), categorical_columns),
    ("numeric", StandardScaler(), numeric_columns),
])

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", LogisticRegression()),
])

pipeline.fit(X_train, y_train)
print("\nPipeline trained (preprocessing + LogisticRegression).")


# --- EXPLAIN ---
# predict_proba() gives us the real output of a classification
# model - a probability, not a hard label. Column 0 is "no churn",
# column 1 is "churn" - the two always add up to 1 per row.
# -------------------------------------------------------------

probabilities = pipeline.predict_proba(X_test)
churn_probabilities = probabilities[:, 1]

sample = pd.DataFrame({
    "actual": y_test.values[:8],
    "churn_probability": np.round(churn_probabilities[:8], 3),
})
print("\nSample predicted probabilities vs actual outcome:")
print(sample)


# --- EXPLAIN ---
# Now let's sweep three different thresholds and watch how many
# partners get flagged as "will churn" at each one. The model
# hasn't changed at all between these three lines - only where
# we've drawn the decision line has changed.
# -------------------------------------------------------------

print("\nThreshold sweep (same probabilities, different decision lines):")
for threshold in [0.3, 0.5, 0.7]:
    flagged = (churn_probabilities >= threshold).astype(int)
    print(f"  threshold={threshold} -> {flagged.sum()} of {len(flagged)} partners flagged as 'will churn'")


# --- EXPLAIN ---
# Quick multiclass illustration: predict_proba() isn't limited to
# two columns. Here's a tiny synthetic 3-category example
# (engagement level: low/medium/high) just to show the same
# LogisticRegression class handling more than two outcomes.
# -------------------------------------------------------------

np.random.seed(1)
n_demo = 60
demo_X = pd.DataFrame({"orders_last_30_days": np.random.randint(0, 60, n_demo)})
demo_y = pd.cut(
    demo_X["orders_last_30_days"], bins=[-1, 15, 35, 60], labels=["low", "medium", "high"]
)

multiclass_model = LogisticRegression()
multiclass_model.fit(demo_X, demo_y)
multiclass_probs = multiclass_model.predict_proba(demo_X.iloc[:3])

print("\nMulticlass example - predict_proba() now returns one column per category:")
print("Categories:", multiclass_model.classes_)
print(np.round(multiclass_probs, 3))


# --- EXPLAIN ---
# Notice each multiclass row still sums to 1 across three columns
# instead of two - same underlying idea, more categories to read.
#
# What this demo does NOT do yet: it doesn't measure whether any
# of these thresholds are actually GOOD choices - it only shows
# that they change the flagged count. Precision, recall, and the
# confusion matrix (Session 23: Classification Metrics) give us
# the real numbers to judge that properly.
# -------------------------------------------------------------
