# =============================================================
# Session 26: Random Forests & Ensemble Methods
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually train a forest, compare it against
# Session 25's tree, and save the whole pipeline with joblib.
#
# Syntax scope check: reuses the Session 25 pipeline and
# DecisionTreeClassifier, plus today's new tools: sklearn.ensemble
# .RandomForestClassifier and joblib. No GridSearchCV yet -
# that's earned in Session 27.
# =============================================================

# --- SETUP ---
# Same noisy Swiggy churn dataset as Session 25, for a direct
# apples-to-apples comparison.
import numpy as np
import pandas as pd

np.random.seed(42)

n_partners = 150

df = pd.DataFrame({
    "city": np.random.choice(["Hyderabad", "Pune", "Chennai"], n_partners),
    "vehicle_type": np.random.choice(["Bike", "Scooter", "Bicycle"], n_partners),
    "orders_last_30_days": np.random.randint(0, 60, n_partners),
    "avg_rating": np.round(np.random.uniform(3.0, 5.0, n_partners), 2),
    "months_active": np.random.randint(1, 36, n_partners),
})

base_churn = ((df["orders_last_30_days"] < 15) & (df["avg_rating"] < 4.3)).astype(int)
flip_mask = np.random.rand(n_partners) < 0.15
df["churned"] = np.where(flip_mask, 1 - base_churn, base_churn)


# --- SETUP ---
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X = df.drop(columns="churned")
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

categorical_columns = ["city", "vehicle_type"]
numeric_columns = ["orders_last_30_days", "avg_rating", "months_active"]

preprocessor = ColumnTransformer(transformers=[
    ("categorical", OneHotEncoder(), categorical_columns),
    ("numeric", StandardScaler(), numeric_columns),
])


# --- EXPLAIN ---
# First, Session 25's best single tree (max_depth=3) as our
# baseline for comparison.
# -------------------------------------------------------------

tree_pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", DecisionTreeClassifier(max_depth=3, random_state=42)),
])
tree_pipeline.fit(X_train, y_train)

tree_train_acc = accuracy_score(y_train, tree_pipeline.predict(X_train))
tree_test_acc = accuracy_score(y_test, tree_pipeline.predict(X_test))

print(f"Single tree (max_depth=3): train={tree_train_acc:.3f}  test={tree_test_acc:.3f}")


# --- EXPLAIN ---
# Now a Random Forest with 200 trees - notice we're not hand-tuning
# max_depth at all here, unlike Session 25's careful depth sweep.
# -------------------------------------------------------------

forest_pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
])
forest_pipeline.fit(X_train, y_train)

forest_train_acc = accuracy_score(y_train, forest_pipeline.predict(X_train))
forest_test_acc = accuracy_score(y_test, forest_pipeline.predict(X_test))

print(f"Random Forest (200 trees): train={forest_train_acc:.3f}  test={forest_test_acc:.3f}")
print(f"\nTest accuracy improvement over single tree: {forest_test_acc - tree_test_acc:+.3f}")


# --- EXPLAIN ---
# Now let's directly demonstrate the stability difference from
# Concept Block 1. We retrain the single tree on 5 different
# bootstrap resamples of the SAME training data and watch its root
# split threshold shift each time - then do the same for the
# forest's top-3 feature importance ranking, which stays identical.
# -------------------------------------------------------------

print("\nSingle tree root-split THRESHOLD across 5 bootstrap resamples:")
for seed in range(5):
    X_boot = X_train.sample(frac=1.0, replace=True, random_state=seed)
    y_boot = y_train.loc[X_boot.index]
    boot_pipeline = Pipeline(steps=[
        ("preprocessing", preprocessor),
        ("classifier", DecisionTreeClassifier(max_depth=3, random_state=42)),
    ])
    boot_pipeline.fit(X_boot, y_boot)
    root_threshold = boot_pipeline.named_steps["classifier"].tree_.threshold[0]
    print(f"  resample {seed}: root threshold = {root_threshold:.3f}")

print("\nRandom Forest top-3 feature importance ranking across the SAME 5 resamples:")
for seed in range(5):
    X_boot = X_train.sample(frac=1.0, replace=True, random_state=seed)
    y_boot = y_train.loc[X_boot.index]
    boot_forest = Pipeline(steps=[
        ("preprocessing", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
    ])
    boot_forest.fit(X_boot, y_boot)
    importances = boot_forest.named_steps["classifier"].feature_importances_
    feat_names = boot_forest.named_steps["preprocessing"].get_feature_names_out()
    top3 = pd.Series(importances, index=feat_names).sort_values(ascending=False).head(3)
    print(f"  resample {seed}: {list(top3.index)}")


# --- EXPLAIN ---
# Notice: the single tree's exact threshold moves noticeably each
# time (Session 25's instability, confirmed again), while the
# forest's top-3 important features stay identical across all 5
# resamples - direct proof of the stability the crowd-wisdom
# analogy promised in Concept Block 1.
# -------------------------------------------------------------

full_importances = forest_pipeline.named_steps["classifier"].feature_importances_
full_feat_names = forest_pipeline.named_steps["preprocessing"].get_feature_names_out()
importance_table = pd.Series(full_importances, index=full_feat_names).sort_values(ascending=False)

print("\nFull feature importance ranking (final forest):")
print(importance_table.round(3).to_string())


# --- SETUP ---
import joblib

# --- EXPLAIN ---
# Finally, save the ENTIRE pipeline - preprocessing and model
# together - so it can be reused later without retraining, and
# without needing to remember the preprocessing steps separately.
# -------------------------------------------------------------

joblib.dump(forest_pipeline, "churn_forest_pipeline.joblib")
print("\nSaved trained pipeline to churn_forest_pipeline.joblib")

loaded_pipeline = joblib.load("churn_forest_pipeline.joblib")
original_predictions = forest_pipeline.predict(X_test)
loaded_predictions = loaded_pipeline.predict(X_test)

predictions_match = np.array_equal(original_predictions, loaded_predictions)
print(f"Loaded pipeline produces identical predictions: {predictions_match}")


# --- EXPLAIN ---
# What this demo does NOT do yet: it doesn't systematically search
# for the best n_estimators or other hyperparameters - we used
# n_estimators=200 by convention rather than a proper search.
# Session 27 (Model Validation & Leakage) introduces GridSearchCV,
# which automates exactly this kind of hyperparameter search using
# proper cross-validation.
# -------------------------------------------------------------
