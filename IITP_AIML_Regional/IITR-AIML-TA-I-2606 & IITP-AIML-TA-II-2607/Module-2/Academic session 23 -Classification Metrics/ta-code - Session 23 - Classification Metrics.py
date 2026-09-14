# =============================================================
# Session 23: Classification Metrics
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually compute all of this in code - same
# Swiggy churn pipeline from Session 22, and finally, the
# DummyClassifier reveal from Session 17.
#
# Syntax scope check: reuses the full Session 22 pipeline
# (ColumnTransformer + LogisticRegression) and Session 17's
# DummyClassifier, plus today's new tools from sklearn.metrics:
# confusion_matrix, precision_score, recall_score, f1_score.
# =============================================================

# --- SETUP ---
# Same Session 22 Swiggy partner dataset and pipeline.
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

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

X = df.drop(columns="churned")
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

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
probabilities = pipeline.predict_proba(X_test)[:, 1]
predictions_at_05 = (probabilities >= 0.5).astype(int)


# --- EXPLAIN ---
# confusion_matrix gives us the exact four-way breakdown from
# Concept Block 1: rows are actual class, columns are predicted
# class. Let's see how our real trained model performs.
# -------------------------------------------------------------

cm = confusion_matrix(y_test, predictions_at_05)
print("LogisticRegression confusion matrix (rows=actual, cols=predicted):")
print("             Pred: No Churn   Pred: Churn")
print(f"Actual: No Churn     {cm[0][0]:>6}          {cm[0][1]:>6}")
print(f"Actual: Churn        {cm[1][0]:>6}          {cm[1][1]:>6}")

model_accuracy = accuracy_score(y_test, predictions_at_05)
model_precision = precision_score(y_test, predictions_at_05)
model_recall = recall_score(y_test, predictions_at_05)
model_f1 = f1_score(y_test, predictions_at_05)

print(f"\nAccuracy:  {model_accuracy:.2f}")
print(f"Precision: {model_precision:.2f}")
print(f"Recall:    {model_recall:.2f}")
print(f"F1:        {model_f1:.2f}")


# --- EXPLAIN ---
# Now the moment we've been building toward since Session 17:
# rebuild that exact DummyClassifier baseline on THIS SAME test
# set, and look at its confusion matrix and metrics side by side.
# -------------------------------------------------------------

dummy_model = DummyClassifier(strategy="most_frequent")
dummy_model.fit(X_train, y_train)
dummy_predictions = dummy_model.predict(X_test)

dummy_cm = confusion_matrix(y_test, dummy_predictions)
dummy_accuracy = accuracy_score(y_test, dummy_predictions)
dummy_precision = precision_score(y_test, dummy_predictions, zero_division=0)
dummy_recall = recall_score(y_test, dummy_predictions, zero_division=0)

print("\n--- Session 17's DummyClassifier baseline, revisited ---")
print("             Pred: No Churn   Pred: Churn")
print(f"Actual: No Churn     {dummy_cm[0][0]:>6}          {dummy_cm[0][1]:>6}")
print(f"Actual: Churn        {dummy_cm[1][0]:>6}          {dummy_cm[1][1]:>6}")
print(f"\nAccuracy:  {dummy_accuracy:.2f}  <- looks fine at a glance!")
print(f"Precision: {dummy_precision:.2f}  <- but this reveals the truth")
print(f"Recall:    {dummy_recall:.2f}  <- it caught ZERO real churners")


# --- EXPLAIN ---
# Side-by-side comparison table - this is the payoff moment.
# The DummyClassifier's accuracy looks almost as good as the real
# model's, but its precision and recall expose that it's completely
# useless for actually catching churners.
# -------------------------------------------------------------

comparison = pd.DataFrame({
    "Model": ["DummyClassifier (Session 17)", "LogisticRegression (Session 22)"],
    "Accuracy": [dummy_accuracy, model_accuracy],
    "Precision": [dummy_precision, model_precision],
    "Recall": [dummy_recall, model_recall],
})
print("\n", comparison.round(3).to_string(index=False))


# --- EXPLAIN ---
# Finally, let's confirm the precision-recall tradeoff table from
# Concept Block 5 with live numbers - same threshold sweep as
# Session 22, now measured properly instead of just counting
# flagged partners.
# -------------------------------------------------------------

print("\nPrecision-recall tradeoff across thresholds:")
for threshold in [0.3, 0.5, 0.7]:
    preds = (probabilities >= threshold).astype(int)
    p = precision_score(y_test, preds, zero_division=0)
    r = recall_score(y_test, preds, zero_division=0)
    print(f"  threshold={threshold} -> precision={p:.2f}, recall={r:.2f}")


# --- EXPLAIN ---
# Notice how threshold=0.7 buys higher precision at the cost of
# recall - exactly the tradeoff Concept Block 5 described, now
# backed by real numbers instead of just intuition.
#
# What this demo does NOT do yet: it doesn't use k-fold or
# stratified cross-validation to get more reliable metric
# estimates, and it doesn't systematically search for the best
# threshold - both of those, plus GridSearchCV, are Session 27's
# job (Model Validation & Leakage).
# -------------------------------------------------------------
