# =============================================================
# Session 19: Master Class - Lines, Curves & Errors
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually watch a machine "learn" a line in code
# - no sklearn yet, just the loop we just drew on the board,
# built from scratch.
#
# Syntax scope check: only uses functions, loops, and NumPy
# (Sessions 6, 9) - deliberately NO sklearn.linear_model here.
# LinearRegression is earned in Session 20; today we hand-roll
# the exact gradient descent loop from the board so students see
# what that future one-liner is actually doing underneath.
# =============================================================

# --- SETUP ---
# Synthetic distance -> delivery-time data, same Swiggy scenario
# as the pre-read/lecture script, generated from a KNOWN true line
# (time = 3 * distance + 5) plus a little random noise - so we can
# check whether gradient descent finds something close to it.
import numpy as np

np.random.seed(42)

n_deliveries = 50
distance_km = np.random.uniform(1, 10, n_deliveries)
true_slope = 3
true_intercept = 5
noise = np.random.normal(0, 1.5, n_deliveries)

delivery_time_min = true_slope * distance_km + true_intercept + noise

print("Sample of the data (distance, delivery_time):")
for i in range(5):
    print(f"  {distance_km[i]:.2f} km -> {delivery_time_min[i]:.2f} min")


# --- EXPLAIN ---
# We start with a deliberately bad guess: slope = 0, intercept = 0.
# This is the hiker standing at a random spot on the hill, blindfolded,
# with no idea yet which way is downhill.
# -------------------------------------------------------------

slope = 0.0
intercept = 0.0
learning_rate = 0.01
n_epochs = 500
n = len(distance_km)


def compute_ssr(distance, actual_time, slope, intercept):
    predicted = slope * distance + intercept
    residuals = actual_time - predicted
    return np.sum(residuals ** 2)


# --- EXPLAIN ---
# Each loop iteration is one "epoch" from the board diagram:
# 1. Measure how wrong the current guess is (SSR)
# 2. Use the derivative (the gradient) to find the downhill direction
# 3. Take a small step in that direction, sized by the learning rate
# We print the SSR every 100 epochs so we can watch it fall - that
# falling number IS the hiker walking downhill toward the valley floor.
# -------------------------------------------------------------

for epoch in range(n_epochs):
    predicted = slope * distance_km + intercept
    residuals = delivery_time_min - predicted

    # Gradients: how SSR changes as we nudge slope and intercept
    # (this is the "feeling the steepness" step - no calculus by
    # hand needed to follow the demo, just watch it work)
    slope_gradient = -2 * np.sum(distance_km * residuals) / n
    intercept_gradient = -2 * np.sum(residuals) / n

    # Take a small step downhill
    slope -= learning_rate * slope_gradient
    intercept -= learning_rate * intercept_gradient

    if epoch % 100 == 0:
        ssr = compute_ssr(distance_km, delivery_time_min, slope, intercept)
        print(f"Epoch {epoch:4d} | SSR = {ssr:8.2f} | slope = {slope:.3f} | intercept = {intercept:.3f}")

final_ssr = compute_ssr(distance_km, delivery_time_min, slope, intercept)
print(f"\nFinal (epoch {n_epochs}) | SSR = {final_ssr:.2f} | slope = {slope:.3f} | intercept = {intercept:.3f}")
print(f"\nTrue relationship used to generate the data: time = {true_slope} * distance + {true_intercept}")
print(f"What gradient descent learned:                time = {slope:.2f} * distance + {intercept:.2f}")


# --- EXPLAIN ---
# Notice the learned slope and intercept land close to the true
# 3 and 5 we used to generate the data - gradient descent found its
# way to (approximately) the bottom of the SSR bowl using nothing
# but repeated small downhill steps.
#
# What this demo does NOT do yet: it doesn't use sklearn at all,
# it doesn't split into train/test (Session 17's habit still
# applies once we're doing this "for real"), and it doesn't
# evaluate with MAE, RMSE, or R² - all of that is Session 20
# (Linear Regression), where this exact hand-rolled loop gets
# replaced by one line: LinearRegression().fit(X, y).
# -------------------------------------------------------------
