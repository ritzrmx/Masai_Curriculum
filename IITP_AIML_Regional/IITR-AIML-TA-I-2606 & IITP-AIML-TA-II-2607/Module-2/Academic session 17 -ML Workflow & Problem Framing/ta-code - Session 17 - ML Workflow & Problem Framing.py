# =============================================================
# Session 17: ML Workflow & Problem Framing
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually see this in code - same Swiggy churn
# scenario, same numbers we've been talking about all session.
#
# Syntax scope check: only uses Pandas/NumPy (Sessions 9-11),
# plus today's new tools: train_test_split, cross_val_score,
# and DummyClassifier (used only as a placeholder baseline -
# NOT a real model; LinearRegression/LogisticRegression are
# earned in Sessions 20 and 22, not before).
# =============================================================

# --- SETUP ---
# Reusing Pandas/NumPy from Module 1 to build a small synthetic
# dataset of delivery partner activity.
import pandas as pd
import numpy as np

np.random.seed(42)

n_partners = 200

df = pd.DataFrame({
    "partner_id": range(1, n_partners + 1),
    "orders_last_30_days": np.random.randint(0, 60, n_partners),
    "avg_rating": np.round(np.random.uniform(3.0, 5.0, n_partners), 2),
    "months_active": np.random.randint(1, 36, n_partners),
})

# Simple rule to simulate a "churned" label (0 = stayed, 1 = churned):
# fewer recent orders and a lower rating roughly means higher churn risk
# (this is synthetic data for demo purposes only)
df["churned"] = (
    (df["orders_last_30_days"] < 10) & (df["avg_rating"] < 4.2)
).astype(int)

print(df.head())
print("\nChurn rate in this sample:", df["churned"].mean())


# --- EXPLAIN ---
# We now have a labeled dataset - "churned" is our known historical
# outcome. That means this is SUPERVISED learning, and since the
# outcome is a category (0 or 1) rather than a number, it's
# specifically CLASSIFICATION - exactly the box we placed this
# problem in during Concept Block 1.
#
# X = the features we'll use to predict
# y = the label we're trying to predict
# -------------------------------------------------------------

X = df[["orders_last_30_days", "avg_rating", "months_active"]]
y = df["churned"]

print("\nFeatures (X) shape:", X.shape)
print("Label (y) shape:", y.shape)


# --- SETUP ---
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.dummy import DummyClassifier

# --- EXPLAIN ---
# train_test_split holds out 20% of the data purely for honest
# evaluation later - the model will never see this during training.
# random_state=42 makes the split reproducible: same split every run.
# This is the "never grade your own homework" rule from Concept
# Block 3, in one line of code.
# -------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining set size:", X_train.shape[0])
print("Test set size:", X_test.shape[0])


# --- EXPLAIN ---
# We're using DummyClassifier here on purpose - it's a baseline
# that just predicts the most frequent class, with NO real learning
# involved. We use it today only to walk through the WORKFLOW
# mechanics. From Session 20 onward, we swap this for real models
# (LinearRegression, then LogisticRegression in Session 22).
# -------------------------------------------------------------

baseline_model = DummyClassifier(strategy="most_frequent")
baseline_model.fit(X_train, y_train)

test_accuracy = baseline_model.score(X_test, y_test)
print("\nBaseline test accuracy (single split):", round(test_accuracy, 3))


# --- EXPLAIN ---
# A single split can be lucky or unlucky - the cricket-selector
# problem from Concept Block 4. cross_val_score repeats the
# train/test process 5 times (cv=5), rotating which chunk of data
# is held out each time, then reports all 5 scores.
# -------------------------------------------------------------

cv_scores = cross_val_score(baseline_model, X, y, cv=5)

print("\nCross-validation scores across 5 folds:", np.round(cv_scores, 3))
print("Average CV accuracy:", round(cv_scores.mean(), 3))


# --- EXPLAIN ---
# Notice: this baseline just guesses the majority class every time,
# yet its accuracy looks deceptively high - because most partners in
# our sample don't churn. This is exactly the discomfort Concept
# Block 5 pointed at: a metric can look great and still tell you
# almost nothing useful.
#
# What this demo does NOT do yet: it doesn't tell us how many actual
# churners we'd miss (false negatives) versus how many false alarms
# we'd raise (false positives) - the precision/recall tools that
# unpack exactly that live in Session 23 (Classification Metrics).
# It also doesn't check this dataset for leakage or stratify the
# folds - that rigor is Session 27's job (Model Validation & Leakage).
# -------------------------------------------------------------
