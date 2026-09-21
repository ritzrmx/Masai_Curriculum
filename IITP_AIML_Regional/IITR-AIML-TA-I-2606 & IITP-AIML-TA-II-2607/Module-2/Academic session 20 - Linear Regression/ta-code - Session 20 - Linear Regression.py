# =============================================================
# Session 20: Linear Regression
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually train, predict, and evaluate a real
# model in code - same Swiggy distance and item-count data from
# the last two sessions.
#
# Syntax scope check: reuses train_test_split (Session 17), plus
# today's new tools: sklearn.linear_model.LinearRegression and
# sklearn.metrics (mean_absolute_error, mean_squared_error,
# r2_score). No Ridge/Lasso yet - those are earned in Session 21.
# =============================================================

# --- SETUP ---
# Same true relationship as Session 19's gradient descent demo,
# now with a second feature (num_items) added so we have more than
# one coefficient to interpret.
import numpy as np
import pandas as pd

np.random.seed(42)

n_deliveries = 200
distance_km = np.random.uniform(1, 10, n_deliveries)
num_items = np.random.randint(1, 8, n_deliveries)

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

df = pd.DataFrame({
    "distance_km": distance_km,
    "num_items": num_items,
    "delivery_time_min": delivery_time_min,
})

print(df.head())


# --- SETUP ---
from sklearn.model_selection import train_test_split

X = df[["distance_km", "num_items"]]
y = df["delivery_time_min"]

# --- EXPLAIN ---
# Same Session 17 habit: split first, before fitting anything.
# -------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# --- SETUP ---
from sklearn.linear_model import LinearRegression

# --- EXPLAIN ---
# This is the "expert hiker" from the opening - two lines replace
# Session 19's entire 500-epoch gradient descent loop. fit() is
# called ONLY on the training data, exactly like every model from
# here forward.
# -------------------------------------------------------------

model = LinearRegression()
model.fit(X_train, y_train)

print("\nModel trained.")


# --- EXPLAIN ---
# predict() applies the already-learned line to new data - it
# never changes the model itself. Let's look at a few predictions
# next to their actual values.
# -------------------------------------------------------------

train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

comparison = pd.DataFrame({
    "actual": y_test.values[:5],
    "predicted": np.round(test_predictions[:5], 2),
})
print("\nSample predictions vs actuals (test set):")
print(comparison)


# --- SETUP ---
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- EXPLAIN ---
# We evaluate on BOTH train and test - not just test - because
# comparing the two is exactly how we diagnose overfitting
# (Concept Block 5). Watch whether these numbers stay close.
# -------------------------------------------------------------

train_mae = mean_absolute_error(y_train, train_predictions)
train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
train_r2 = r2_score(y_train, train_predictions)

test_mae = mean_absolute_error(y_test, test_predictions)
test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
test_r2 = r2_score(y_test, test_predictions)

print(f"\n{'Metric':<10}{'Train':>10}{'Test':>10}")
print(f"{'MAE':<10}{train_mae:>10.2f}{test_mae:>10.2f}")
print(f"{'RMSE':<10}{train_rmse:>10.2f}{test_rmse:>10.2f}")
print(f"{'R2':<10}{train_r2:>10.2f}{test_r2:>10.2f}")


# --- EXPLAIN ---
# Now let's read the coefficients the model actually learned, and
# compare them to the true values we used to generate the data.
# -------------------------------------------------------------

print(f"\nLearned distance_km coefficient: {model.coef_[0]:.2f} (true value: {true_distance_coef})")
print(f"Learned num_items coefficient:   {model.coef_[1]:.2f} (true value: {true_items_coef})")
print(f"Learned intercept:               {model.intercept_:.2f} (true value: {true_intercept})")

print(
    f"\nInterpretation: each extra km adds about {model.coef_[0]:.1f} minutes; "
    f"each extra item adds about {model.coef_[1]:.1f} minutes; "
    f"baseline handling time is about {model.intercept_:.1f} minutes."
)


# --- EXPLAIN ---
# Notice train and test MAE/RMSE/R2 stay close - a healthy sign
# this model generalizes rather than having memorized the training
# set. This is a deliberately well-behaved dataset; real-world data
# is often messier.
#
# What this demo does NOT do yet: it doesn't do anything about
# overfitting when it DOES show up - that's Session 21
# (Regularization), where Ridge and Lasso pull an overfitting
# model back toward simplicity, and we explore the bias-variance
# tradeoff behind why that works.
# -------------------------------------------------------------
