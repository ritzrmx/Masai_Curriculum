# =============================================================
# Session 12.2: Clustering, Model Selection & Explainability
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Same Swiggy partner data one last time - let's find
# natural partner segments with KMeans, pick the best churn model
# from a fair comparison table, and explain its predictions in
# plain English for the ops team.
#
# Syntax scope check: Pandas/NumPy (Module 1), StandardScaler (Data
# Prep), LogisticRegression (Logistic Regression session),
# DecisionTreeClassifier (Decision Trees), RandomForestClassifier and
# feature_importances_ (Random Forests), StratifiedKFold and
# cross_validate (Model Validation & Leakage), DummyClassifier (ML
# Workflow), plus today's new tools: KMeans, inertia_ (elbow method)
# and silhouette_score.
#
# Install once:  pip install scikit-learn pandas numpy matplotlib
# NOTE: all partner data below is synthetic, for teaching.
# =============================================================

# --- SETUP ---
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
warnings.filterwarnings("ignore")   # hides the baseline's "precision is 0" notice


# --- EXPLAIN ---
# Synthetic partner data with three hidden "types" of partner, which
# the ops team has never labelled: full-timers, part-timers and new
# joiners. KMeans must discover them WITHOUT being told.
# -------------------------------------------------------------

def make_group(n, orders, rating, months):
    return pd.DataFrame({
        "orders_last_30_days": np.clip(np.random.normal(orders, 6, n), 0, None).round(),
        "avg_rating": np.clip(np.random.normal(rating, 0.2, n), 3.0, 5.0).round(2),
        "months_active": np.clip(np.random.normal(months, 3, n), 1, None).round(),
    })

df = pd.concat([make_group(120, 50, 4.6, 26),     # full-timers
                make_group(110, 27, 4.3, 13),     # part-timers
                make_group(70, 7, 4.0, 2)],       # new joiners
               ignore_index=True)

# Churn label: fewer orders, lower rating and shorter tenure raise the
# risk - plus ~15% label noise, so no model can be perfect.
risk = (-0.08 * df["orders_last_30_days"] - 2.0 * (df["avg_rating"] - 4.3)
        - 0.06 * df["months_active"] + 1.6)
df["churned"] = (risk + np.random.normal(0, 0.6, len(df)) > 0).astype(int)
flip = np.random.rand(len(df)) < 0.15
df.loc[flip, "churned"] = 1 - df.loc[flip, "churned"]

features = ["orders_last_30_days", "avg_rating", "months_active"]
print(df.head())
print("\nPartners:", len(df), "| churn rate:", round(df["churned"].mean(), 2))


# --- SETUP ---
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# --- EXPLAIN ---
# Concept Block 1: KMeans measures DISTANCE, so features must be on the
# same scale (orders run 0-60, ratings 3-5). Unlike trees, KMeans
# NEEDS scaling - StandardScaler from the Data Prep session.
# -------------------------------------------------------------

X_scaled = StandardScaler().fit_transform(df[features])


# --- EXPLAIN ---
# Concept Blocks 2-3: try k = 2..8. inertia_ = total squared distance
# from each partner to its cluster centre (always falls as k grows).
# silhouette_score = how well each partner fits its own cluster vs the
# nearest other one (-1 to 1, higher is better).
# -------------------------------------------------------------

rows = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled)
    rows.append({"k": k, "inertia": round(km.inertia_, 1),
                 "silhouette": round(silhouette_score(X_scaled, km.labels_), 3)})
k_table = pd.DataFrame(rows)
print("\n", k_table.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(k_table["k"], k_table["inertia"], "o-")
axes[0].set_title("Elbow method: inertia vs k"); axes[0].set_xlabel("k")
axes[1].plot(k_table["k"], k_table["silhouette"], "o-", color="tab:green")
axes[1].set_title("Silhouette score vs k"); axes[1].set_xlabel("k")
plt.tight_layout(); plt.show()


# --- EXPLAIN ---
# Read the table: inertia drops sharply until k = 3, then flattens -
# the "elbow". Silhouette is highest at k = 2, with k = 3 a close
# second. The two methods are guides, not verdicts: business sense
# breaks the tie, and 3 segments needing 3 different actions wins.
# Then fit the chosen k and DESCRIBE each cluster in business terms -
# the model only gives cluster numbers; naming them is our job.
# -------------------------------------------------------------

best_k = 3
km = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit(X_scaled)
df["segment"] = km.labels_
profile = df.groupby("segment")[features + ["churned"]].mean().round(2)
profile["partners"] = df["segment"].value_counts().sort_index()
print("\nSegment profiles:\n", profile)


# --- SETUP ---
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# --- EXPLAIN ---
# Concept Block 4: a FAIR comparison table. Same data, same 5
# stratified folds, same metrics for every model. The baseline
# (DummyClassifier from the ML Workflow session) shows what
# "no learning at all" scores. Scaling sits inside a pipeline so each
# fold is scaled only on its own training part (no leakage).
# -------------------------------------------------------------

X, y = df[features], df["churned"]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = {
    "Baseline (most frequent)": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression()),
    "Decision Tree (depth 3)": DecisionTreeClassifier(max_depth=3, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42),
}
metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]

table = []
for name, model in models.items():
    scores = cross_validate(model, X, y, cv=cv, scoring=metrics)
    table.append({"model": name, **{m: round(scores[f"test_{m}"].mean(), 3) for m in metrics}})
comparison = pd.DataFrame(table).set_index("model")
print("\nModel comparison (mean of 5 stratified folds):\n", comparison)


# --- EXPLAIN ---
# Concept Block 5: feature importance from the Random Forest - how much
# each feature reduced impurity across all its trees. It says WHICH
# features matter, not in WHICH DIRECTION, and not that they CAUSE churn.
# -------------------------------------------------------------

rf = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42).fit(X, y)
importance = pd.Series(rf.feature_importances_, index=features).sort_values()
print("\nFeature importances:\n", importance.round(3))

importance.plot.barh(color="tab:orange")
plt.title("What drives the churn prediction?"); plt.xlabel("importance")
plt.tight_layout(); plt.show()


# --- EXPLAIN ---
# Concept Block 6: explain ONE prediction to a non-technical manager.
# Template: what we predict, how sure, the top reasons in plain words
# (this partner vs a typical retained partner), and what to do next.
# -------------------------------------------------------------

partner = df.loc[[250], features]
prob = rf.predict_proba(partner)[0, 1]
typical = df.loc[df["churned"] == 0, features].median()

print(f"\nPartner #250: {prob:.0%} estimated chance of churning next month.")
for f in importance.sort_values(ascending=False).index:
    print(f"  - {f.replace('_', ' ')}: {partner[f].iloc[0]:g} (typical retained partner: {typical[f]:g})")
print("Suggested action: call within a week; offer peak-hour slots and a rating-coaching session.")


# --- EXPLAIN ---
# What this demo does NOT do: it doesn't prove WHY partners churn -
# importances and comparisons are correlations in historical data.
# A real decision (like an incentive) should be tested, e.g. with a
# small pilot. Next, Module 3 starts with LLM Fundamentals - and the
# same "explain it in plain words" skill returns for AI answers.
# -------------------------------------------------------------
