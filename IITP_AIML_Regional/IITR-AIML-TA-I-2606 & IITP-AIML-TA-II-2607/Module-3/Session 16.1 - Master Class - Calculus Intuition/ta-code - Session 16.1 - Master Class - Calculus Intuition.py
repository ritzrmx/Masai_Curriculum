# =============================================================
# Session 16.1: Master Class - Calculus Intuition: Change, Slope
# & Optimisation
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Watch the secant slope settle into a derivative, find
# the bottom of a curve, then walk downhill step by step - the
# same move every model makes while it learns.
#
# Syntax scope check: NumPy and Matplotlib only (Module 1). Every
# derivative is checked two ways: by the rules from Concept Block 3
# and by shrinking the gap between two points. No API key needed.
#
# Install once:  pip install numpy matplotlib
# =============================================================

# --- SETUP ---
import numpy as np
import matplotlib.pyplot as plt


# --- EXPLAIN ---
# Concept Block 1: a function is a rule, input -> one output.
# Plot y = x^2 and y = x^3 to see their shapes.
# -------------------------------------------------------------

x = np.linspace(-3, 3, 200)
plt.figure(figsize=(9, 4))
plt.subplot(1, 2, 1); plt.plot(x, x ** 2); plt.title("y = x^2"); plt.grid(True)
plt.subplot(1, 2, 2); plt.plot(x, x ** 3); plt.title("y = x^3"); plt.grid(True)
plt.tight_layout(); plt.show()


# --- EXPLAIN ---
# Concept Blocks 1-2: average rate of change = (f(b) - f(a)) / (b - a).
# The partner's distance d(t) = t^2. Slide b towards a = 1 and
# watch the average rate settle on 2 - the derivative at t = 1.
# -------------------------------------------------------------

def d(t):
    return t ** 2


a = 1
for b in [3, 2, 1.1, 1.01, 1.001, 1.0001]:
    rate = (d(b) - d(a)) / (b - a)
    print(f"from t=1 to t={b:<7} average rate = {rate:.4f}")


# --- EXPLAIN ---
# Concept Block 2: secant (two points) vs tangent (one point).
# As the second point slides in, the secant line rotates into
# the tangent, whose slope is the derivative 2t = 2 at t = 1.
# -------------------------------------------------------------

t = np.linspace(0, 3.2, 200)
plt.figure(figsize=(5, 4))
plt.plot(t, d(t), color="black", label="d(t) = t^2")
for b, colour in [(3, "tab:red"), (2, "tab:orange"), (1.3, "tab:olive")]:
    slope = (d(b) - d(a)) / (b - a)
    plt.plot(t, d(a) + slope * (t - a), "--", color=colour, label=f"secant to t={b}, slope {slope:.1f}")
plt.plot(t, d(a) + 2 * (t - a), color="tab:green", linewidth=2, label="tangent at t=1, slope 2")
plt.ylim(-1, 10); plt.grid(True); plt.legend(fontsize=7)
plt.title("Secants rotating into the tangent"); plt.show()


# --- EXPLAIN ---
# Concept Block 3: the power, constant and sum rules.
# f(x) = 3x^2 + 2x + 1  ->  f'(x) = 6x + 2 (the "+1" vanishes).
# Check the rule against a tiny-gap estimate at a few points.
# -------------------------------------------------------------

def f(x):
    return 3 * x ** 2 + 2 * x + 1


def f_prime_rule(x):
    return 6 * x + 2


def slope_estimate(func, x, gap=1e-5):
    return (func(x + gap) - func(x)) / gap


for point in [-2, 0, 1, 3]:
    print(f"x={point:>2}: rule says {f_prime_rule(point):>5}, tiny-gap estimate {slope_estimate(f, point):.3f}")


# --- EXPLAIN ---
# Concept Block 4: set the derivative to zero to find the bottom.
# 6x + 2 = 0  ->  x = -1/3. Check the slope on both sides.
# -------------------------------------------------------------

x_min = -2 / 6
print(f"\nf'(x) = 0 at x = {x_min:.4f}, f(x) there = {f(x_min):.4f}  (expected 2/3 = {2/3:.4f})")
print("slope just left :", round(f_prime_rule(x_min - 0.1), 2), "(negative = going down)")
print("slope just right:", round(f_prime_rule(x_min + 0.1), 2), "(positive = going up) -> a MINIMUM")

# y = x^3 - 3x has a hilltop and a valley where 3x^2 - 3 = 0
for xc in [-1, 1]:
    print(f"y = x^3 - 3x at x = {xc}: y = {xc ** 3 - 3 * xc}")


# --- EXPLAIN ---
# Concept Block 5: walking downhill on f(x) = x^2.
#   new x = old x - step_size * slope,  with slope = 2x
# Start at x = 4 with step 0.1, exactly like the pre-read table.
# -------------------------------------------------------------

def walk_downhill(start, step_size, n_steps=15):
    xs = [start]
    for _ in range(n_steps):
        slope = 2 * xs[-1]
        xs.append(xs[-1] - step_size * slope)
    return xs


good = walk_downhill(4, 0.1)
print("\nStep size 0.1:", [round(v, 3) for v in good[:6]], "...", round(good[-1], 4))

too_big = walk_downhill(4, 1.1, n_steps=6)
print("Step size 1.1:", [round(v, 2) for v in too_big], " <- bouncing further away!")

xx = np.linspace(-6, 6, 200)
plt.figure(figsize=(5, 4))
plt.plot(xx, xx ** 2, color="black")
plt.plot(good, [v ** 2 for v in good], "o-", color="tab:green", label="step 0.1 (walks down)")
plt.plot(too_big[:4], [v ** 2 for v in too_big[:4]], "o--", color="tab:red", label="step 1.1 (overshoots)")
plt.ylim(-1, 40); plt.grid(True); plt.legend(); plt.title("Walking downhill on x^2"); plt.show()


# --- EXPLAIN ---
# Practical Block 4 preview: the hub manager's incentive.
# N(b) = 40b - b^2  ->  N'(b) = 40 - 2b = 0  ->  b = 20 (Rs 2,000).
# Here we MAXIMISE, so we walk UPHILL: add the slope instead.
# -------------------------------------------------------------

b = 5.0
for _ in range(50):
    b = b + 0.1 * (40 - 2 * b)
print(f"\nWalking uphill on N(b) lands at b = {b:.2f} -> N = {40 * b - b ** 2:.1f}")


# --- EXPLAIN ---
# What this demo does NOT do: here "x" is ONE number. In a real model
# it's thousands to billions of numbers, and the chain rule (concept
# only today) links the error to every one of them. The libraries do
# that automatically - you've already used it inside .fit() in Module 2.
# Next session uses models trained this way to turn text into vectors.
# -------------------------------------------------------------
