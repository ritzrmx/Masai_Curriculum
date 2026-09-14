# =============================================================
# Session 25: Decision Trees
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually watch a tree overfit and then find its
# sweet spot in code - same Swiggy churn scenario, now with a
# decision tree instead of logistic regression.
#
# Syntax scope check: reuses train_test_split (Session 17),
# Pipeline + ColumnTransformer (Session 18), plus today's new
# tools: DecisionTreeClassifier and plot_tree from sklearn.tree.
# matplotlib is already earned from Session 13 (Data Visualization).
# =============================================================

# --- SETUP ---
# Same Swiggy partner dataset as Sessions 17-23, now with a smaller
# sample and a touch of realistic label noise deliberately added -
# without noise, even a very deep tree could perfectly generalize,
# hiding today's overfitting lesson entirely.
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
flip_mask = np.random.rand(n_partners) < 0.15  # 15% label noise
df["churned"] = np.where(flip_mask, 1 - base_churn, base_churn)

print(f"Churn rate: {df['churned'].mean():.2%}")


# --- SETUP ---
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

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
# First, an UNLIMITED depth tree - no max_depth set at all. Watch
# it hit perfect training accuracy while test accuracy lags well
# behind - the exact overfitting gap from Session 21, now caused
# by tree depth instead of too many features.
# -------------------------------------------------------------

unlimited_pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", DecisionTreeClassifier(random_state=42)),
])
unlimited_pipeline.fit(X_train, y_train)

train_acc = accuracy_score(y_train, unlimited_pipeline.predict(X_train))
test_acc = accuracy_score(y_test, unlimited_pipeline.predict(X_test))
tree_depth = unlimited_pipeline.named_steps["classifier"].get_depth()

print(f"\nUnlimited depth tree (actual depth reached: {tree_depth}):")
print(f"  Train accuracy: {train_acc:.3f}")
print(f"  Test accuracy:  {test_acc:.3f}")
print(f"  Gap: {train_acc - test_acc:.3f}")


# --- EXPLAIN ---
# Now let's sweep max_depth from 1 to 10 and watch the train/test
# gap open up as depth increases - this is this session's version
# of Session 21's alpha sweep.
# -------------------------------------------------------------

print("\nDepth sweep:")
results = []
for depth in range(1, 11):
    pipeline = Pipeline(steps=[
        ("preprocessing", preprocessor),
        ("classifier", DecisionTreeClassifier(max_depth=depth, random_state=42)),
    ])
    pipeline.fit(X_train, y_train)
    tr = accuracy_score(y_train, pipeline.predict(X_train))
    te = accuracy_score(y_test, pipeline.predict(X_test))
    results.append((depth, tr, te))
    print(f"  depth={depth:2d}  train={tr:.3f}  test={te:.3f}  gap={tr - te:.3f}")

best_depth = max(results, key=lambda r: r[2])[0]
print(f"\nBest test accuracy found at max_depth={best_depth} - this is our sweet spot.")


# --- EXPLAIN ---
# Let's train the sweet-spot tree and actually look at it with
# plot_tree - small enough to read, unlike the unlimited-depth
# version from earlier.
# -------------------------------------------------------------

best_pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", DecisionTreeClassifier(max_depth=best_depth, random_state=42)),
])
best_pipeline.fit(X_train, y_train)

feature_names = best_pipeline.named_steps["preprocessing"].get_feature_names_out()

plt.figure(figsize=(14, 8))
plot_tree(
    best_pipeline.named_steps["classifier"],
    feature_names=feature_names,
    class_names=["No Churn", "Churn"],
    filled=True,
    fontsize=8,
)
plt.title(f"Decision Tree (max_depth={best_depth})")
plt.tight_layout()
plt.savefig("decision_tree_visualization.png", dpi=100)
print(f"\nTree diagram saved as decision_tree_visualization.png")


# --- EXPLAIN ---
# Finally, let's trace one specific prediction root-to-leaf in
# plain language, exactly like Concept Block 4 - this is what
# makes a single tree's reasoning genuinely explainable.
# -------------------------------------------------------------

sample_partner = X_test.iloc[[0]]
sample_prediction = best_pipeline.predict(sample_partner)[0]

print("\nSample partner:")
print(sample_partner.to_string(index=False))
print(f"\nPredicted: {'Churn' if sample_prediction == 1 else 'No Churn'}")
print("(See the saved tree diagram to trace this partner's exact root-to-leaf path.)")


# --- EXPLAIN ---
# What this demo does NOT do yet: it doesn't combine multiple
# trees together to reduce the instability we saw in how much a
# tree's structure can shift with the data - that's exactly
# Session 26 (Random Forests & Ensemble Methods), where many trees
# vote together instead of relying on one.
# -------------------------------------------------------------
