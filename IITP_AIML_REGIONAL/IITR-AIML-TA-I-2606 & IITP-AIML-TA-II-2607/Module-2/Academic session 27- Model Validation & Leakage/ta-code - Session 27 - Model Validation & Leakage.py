# =============================================================
# Session 27: Model Validation & Leakage
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually see that broken fold happen, fix it
# with stratification, then run a real GridSearchCV search.
#
# Syntax scope check: reuses the Session 26 pipeline and
# RandomForestClassifier, plus today's new tools: KFold,
# StratifiedKFold, and GridSearchCV from sklearn.model_selection.
# =============================================================

# --- SETUP ---
# Same noisy Swiggy churn dataset as Sessions 25-26.
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

print(f"Overall churn rate: {df['churned'].mean():.1%}")


# --- EXPLAIN ---
# Now let's simulate a very common real-world scenario: data
# exported from a database, sorted by the outcome column itself.
# This is NOT a contrived setup - sorting by status/date is common.
# -------------------------------------------------------------

df_sorted = df.sort_values("churned").reset_index(drop=True)
X_sorted = df_sorted.drop(columns="churned")
y_sorted = df_sorted["churned"]


# --- SETUP ---
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# --- EXPLAIN ---
# Plain KFold, with NO shuffling, on this sorted data. Watch what
# happens to the churn count in each test fold.
# -------------------------------------------------------------

kf_no_shuffle = KFold(n_splits=5, shuffle=False)

print("\nPlain KFold, NO shuffle, on SORTED data:")
for i, (train_idx, test_idx) in enumerate(kf_no_shuffle.split(X_sorted, y_sorted)):
    fold_churn_count = y_sorted.iloc[test_idx].sum()
    print(f"  fold {i}: {fold_churn_count} churners out of {len(test_idx)} in this test fold")


# --- EXPLAIN ---
# Now the fix: StratifiedKFold on the EXACT SAME sorted data.
# Every fold should now reflect the true ~25% churn rate,
# regardless of how the data happened to be ordered.
# -------------------------------------------------------------

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)

print("\nStratifiedKFold on the SAME sorted data:")
for i, (train_idx, test_idx) in enumerate(skf.split(X_sorted, y_sorted)):
    fold_churn_count = y_sorted.iloc[test_idx].sum()
    print(f"  fold {i}: {fold_churn_count} churners out of {len(test_idx)} in this test fold")


# --- EXPLAIN ---
# Now let's use GridSearchCV to systematically search for the best
# RandomForest hyperparameters, replacing the hand-tuning we did
# by eye in Sessions 21, 25, and 26. Note the full pipeline
# (preprocessing + classifier) goes INSIDE the grid search, so
# each fold's preprocessing stays leakage-free automatically.
# -------------------------------------------------------------

categorical_columns = ["city", "vehicle_type"]
numeric_columns = ["orders_last_30_days", "avg_rating", "months_active"]

preprocessor = ColumnTransformer(transformers=[
    ("categorical", OneHotEncoder(), categorical_columns),
    ("numeric", StandardScaler(), numeric_columns),
])

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42)),
])

param_grid = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__max_depth": [3, 5, None],
}

X = df.drop(columns="churned")
y = df["churned"]

grid_search = GridSearchCV(pipeline, param_grid, cv=skf, scoring="accuracy")
grid_search.fit(X, y)

print(f"\nGridSearchCV best params: {grid_search.best_params_}")
print(f"GridSearchCV best CV score: {grid_search.best_score_:.3f}")


# --- EXPLAIN ---
# Finally, the leakage demonstration. We add a proxy feature that
# closely tracks the churn outcome (with a little noise) - exactly
# the kind of feature that might sneak into a real dataset if it
# was set by a process that already "knew" the customer was at risk.
# -------------------------------------------------------------

df_leaky = df.copy()
proxy_noise = np.random.rand(n_partners) < 0.05
df_leaky["flagged_for_retention_call"] = np.where(
    proxy_noise, 1 - df_leaky["churned"], df_leaky["churned"]
)

X_leaky = df_leaky.drop(columns="churned")
y_leaky = df_leaky["churned"]

numeric_columns_leaky = numeric_columns + ["flagged_for_retention_call"]
preprocessor_leaky = ColumnTransformer(transformers=[
    ("categorical", OneHotEncoder(), categorical_columns),
    ("numeric", StandardScaler(), numeric_columns_leaky),
])
pipeline_leaky = Pipeline(steps=[
    ("preprocessing", preprocessor_leaky),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
])

scores_leaky = cross_val_score(pipeline_leaky, X_leaky, y_leaky, cv=skf)
scores_clean = cross_val_score(pipeline, X, y, cv=skf)

print(f"\nWith leaky 'flagged_for_retention_call' feature: mean CV accuracy = {scores_leaky.mean():.3f}")
print(f"Without that feature (clean):                     mean CV accuracy = {scores_clean.mean():.3f}")
print(f"\nSuspicious jump of {scores_leaky.mean() - scores_clean.mean():+.3f} - this is a leakage red flag,")
print("not a genuine improvement. 'flagged_for_retention_call' is almost certainly")
print("set by a process that already knows the customer is at risk - it would not")
print("be available before the outcome we're trying to predict.")


# --- EXPLAIN ---
# What this demo does NOT do yet: it doesn't use nested cross-
# validation, which would be needed if we wanted to both tune
# hyperparameters AND get a fully unbiased final performance
# estimate at the same time - a more advanced technique beyond
# today's scope, but good to know exists for rigorous production
# evaluation pipelines.
# -------------------------------------------------------------
