# =============================================================
# Session 21: Regularization
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually watch this overfitting-and-fix cycle
# happen in code - same delivery-time scenario, now with a stack
# of random noise features added on purpose.
#
# Syntax scope check: reuses train_test_split (Session 17) and
# LinearRegression (Session 20), plus today's new tools: Ridge
# and Lasso from sklearn.linear_model. No GridSearchCV yet -
# that's earned in Session 27; today we tune alpha by hand.
# =============================================================

# --- SETUP ---
# Same true relationship as Sessions 19-20, now deliberately
# padded with 15 random noise columns and a SMALL training set -
# both choices designed to make plain LinearRegression overfit.
import numpy as np
import pandas as pd

np.random.seed(42)

n_deliveries = 40
distance_km = np.random.uniform(1, 10, n_deliveries)
num_items = np.random.randint(1, 8, n_deliveries)
n_noise_features = 15
noise_features = np.random.normal(0, 1, (n_deliveries, n_noise_features))

true_distance_coef = 3
true_items_coef = 1.5
true_intercept = 5
noise = np.random.normal(0, 1.5, n_deliveries)

delivery_time_min = (
    true_distance_coef * distance_km
    + true_items_coef * num_items
    + true_intercept
    + noise
)

df = pd.DataFrame({"distance_km": distance_km, "num_items": num_items})
for i in range(n_noise_features):
    df[f"random_signal_{i+1}"] = noise_features[:, i]
df["delivery_time_min"] = delivery_time_min

print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]-1} features (2 real + {n_noise_features} random noise)")


# --- SETUP ---
from sklearn.model_selection import train_test_split

X = df.drop(columns="delivery_time_min")
y = df["delivery_time_min"]

# --- EXPLAIN ---
# Same Session 17 habit: split first. Notice we're using very few
# training rows relative to the number of features - that's exactly
# the recipe for overfitting we discussed in Concept Block 1.
# -------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"\nTraining rows: {X_train.shape[0]} | Features: {X_train.shape[1]}")


# --- SETUP ---
from sklearn.linear_model import LinearRegression, Ridge, Lasso

# --- EXPLAIN ---
# First, the plain LinearRegression baseline from Session 20 -
# no regularization at all. Watch the train/test R2 gap.
# -------------------------------------------------------------

plain_model = LinearRegression()
plain_model.fit(X_train, y_train)

plain_train_r2 = plain_model.score(X_train, y_train)
plain_test_r2 = plain_model.score(X_test, y_test)

print(f"\nPlain LinearRegression: train R2 = {plain_train_r2:.3f} | test R2 = {plain_test_r2:.3f}")
print("Sample noise-feature coefficients (should be near zero, but aren't):")
print(np.round(plain_model.coef_[2:7], 2))


# --- EXPLAIN ---
# Now Ridge - same data, but with a penalty that shrinks every
# coefficient toward zero. Watch the train/test gap narrow and
# the noise coefficients shrink, without any going to exactly zero.
# -------------------------------------------------------------

ridge_model = Ridge(alpha=10)
ridge_model.fit(X_train, y_train)

ridge_train_r2 = ridge_model.score(X_train, y_train)
ridge_test_r2 = ridge_model.score(X_test, y_test)

print(f"\nRidge (alpha=10): train R2 = {ridge_train_r2:.3f} | test R2 = {ridge_test_r2:.3f}")
print("Same noise-feature coefficients, now shrunk:")
print(np.round(ridge_model.coef_[2:7], 2))


# --- EXPLAIN ---
# Now Lasso - watch some noise coefficients get pushed all the
# way to exactly zero, effectively removing those features, while
# distance_km and num_items stay strong because they carry real signal.
# -------------------------------------------------------------

lasso_model = Lasso(alpha=0.3, max_iter=10000)
lasso_model.fit(X_train, y_train)

lasso_train_r2 = lasso_model.score(X_train, y_train)
lasso_test_r2 = lasso_model.score(X_test, y_test)

print(f"\nLasso (alpha=0.3): train R2 = {lasso_train_r2:.3f} | test R2 = {lasso_test_r2:.3f}")
print("Same noise-feature coefficients, several now at/near zero:")
print(np.round(lasso_model.coef_[2:7], 2))

n_zeroed = np.sum(np.abs(lasso_model.coef_[2:]) < 0.01)
print(f"\nLasso zeroed out {n_zeroed} of {n_noise_features} noise coefficients entirely.")


# --- EXPLAIN ---
# Side-by-side summary: notice the train/test gap shrinks as we
# move from plain regression to Ridge to Lasso, while the real
# feature coefficients (distance_km, num_items) stay close to
# their true values (3 and 1.5) across all three models.
# -------------------------------------------------------------

summary = pd.DataFrame({
    "Model": ["Plain LinearRegression", "Ridge (alpha=10)", "Lasso (alpha=0.3)"],
    "Train R2": [plain_train_r2, ridge_train_r2, lasso_train_r2],
    "Test R2": [plain_test_r2, ridge_test_r2, lasso_test_r2],
    "Train-Test Gap": [
        plain_train_r2 - plain_test_r2,
        ridge_train_r2 - ridge_test_r2,
        lasso_train_r2 - lasso_test_r2,
    ],
    "distance_km coef (true=3.0)": [
        round(plain_model.coef_[0], 2),
        round(ridge_model.coef_[0], 2),
        round(lasso_model.coef_[0], 2),
    ],
})
print("\n", summary.round(3).to_string(index=False))


# --- EXPLAIN ---
# What this demo does NOT do yet: it doesn't search across many
# alpha values systematically - we picked alpha=10 and alpha=0.3
# by hand today. Session 27 (Model Validation & Leakage) introduces
# GridSearchCV, which automates exactly this search properly using
# cross-validation instead of a single train/test split.
# -------------------------------------------------------------
