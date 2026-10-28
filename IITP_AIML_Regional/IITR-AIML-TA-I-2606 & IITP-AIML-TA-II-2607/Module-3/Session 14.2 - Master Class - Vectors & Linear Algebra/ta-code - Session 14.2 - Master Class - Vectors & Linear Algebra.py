# =============================================================
# Session 14.2: Master Class - Vectors & Linear Algebra
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Our delivery partner rides around Hyderabad - let's
# turn his trips into arrows, then measure how similar two
# partner messages are using the very same maths.
#
# Syntax scope check: NumPy and Matplotlib only (Module 1).
# Everything is computed by hand first, then checked with NumPy.
# No API key or internet needed.
#
# Install once:  pip install numpy matplotlib
# =============================================================

# --- SETUP ---
import numpy as np
import matplotlib.pyplot as plt


# --- EXPLAIN ---
# Concept Block 1: a vector is just a list of numbers with a
# direction. (3, 4) = 3 km east, 4 km north of the hub.
# A NumPy array is the natural way to store one.
# -------------------------------------------------------------

a = np.array([3, 4])     # hub -> restaurant
b = np.array([2, -1])    # restaurant -> customer

print("a =", a, "| b =", b)


# --- EXPLAIN ---
# Concept Block 2: add, subtract, scale - component by component.
# NumPy does exactly the "add matching positions" rule for us.
# -------------------------------------------------------------

print("\na + b  =", a + b, "  (hub -> customer)")
print("a - b  =", a - b)
print("2 * a  =", 2 * a, "  (same direction, twice as long)")
print("-1 * a =", -1 * a, " (same length, flipped)")


# --- EXPLAIN ---
# Concept Block 3: magnitude = Pythagoras. First by hand, then
# with np.linalg.norm to check. Works in 3D (and 384D) too.
# -------------------------------------------------------------

by_hand = np.sqrt(a[0] ** 2 + a[1] ** 2)
print("\n|a| by hand :", by_hand)
print("|a| by NumPy:", np.linalg.norm(a))
print("|(2, 3, 6)| :", np.linalg.norm(np.array([2, 3, 6])))

print("Is |a + b| equal to |a| + |b|?",
      round(np.linalg.norm(a + b), 2), "vs", round(np.linalg.norm(a) + np.linalg.norm(b), 2))

unit_a = a / np.linalg.norm(a)
print("\nUnit vector of a:", unit_a, "-> length", np.linalg.norm(unit_a))
print("Unit vector of (30, 40):", np.array([30, 40]) / np.linalg.norm([30, 40]),
      "-> same direction as a")


# --- EXPLAIN ---
# Draw the tip-to-tail picture. quiver() draws arrows: start x,
# start y, change in x, change in y.
# -------------------------------------------------------------

plt.figure(figsize=(5, 5))
plt.quiver(0, 0, a[0], a[1], angles="xy", scale_units="xy", scale=1, color="tab:blue", label="a = (3,4)")
plt.quiver(a[0], a[1], b[0], b[1], angles="xy", scale_units="xy", scale=1, color="tab:orange", label="b = (2,-1)")
plt.quiver(0, 0, (a + b)[0], (a + b)[1], angles="xy", scale_units="xy", scale=1, color="tab:green", label="a + b = (5,3)")
plt.xlim(-1, 7); plt.ylim(-1, 7); plt.grid(True)
plt.xlabel("km east"); plt.ylabel("km north")
plt.title("Tip-to-tail: hub -> restaurant -> customer")
plt.legend(); plt.show()


# --- EXPLAIN ---
# Concept Block 4: dot product = multiply matching parts, add up.
# Watch the SIGN: positive = same way, zero = perpendicular,
# negative = opposite.
# -------------------------------------------------------------

for other in [np.array([4, 3]), np.array([-4, 3]), np.array([-3, -4])]:
    by_hand = a[0] * other[0] + a[1] * other[1]
    print(f"\na . {other} = {by_hand}  (NumPy says {np.dot(a, other)})")


# --- EXPLAIN ---
# Concept Block 5: cos(theta) = (a . b) / (|a| |b|).
# np.arccos gives RADIANS - convert with np.degrees before reading.
# -------------------------------------------------------------

def angle_between(u, v):
    cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return cos_theta, np.degrees(np.arccos(np.clip(cos_theta, -1, 1)))


for other in [np.array([4, 3]), np.array([-4, 3]), np.array([-3, -4])]:
    c, deg = angle_between(a, other)
    print(f"a vs {other}: cos = {c:.2f}, angle = {deg:.1f} degrees")


# --- EXPLAIN ---
# The payoff: messages as arrows on two made-up axes,
# (about money, about the app). Same formula, now measuring
# MEANING. This number is "cosine similarity" (Session 16.2).
# -------------------------------------------------------------

messages = {
    "Payout not credited since Friday": np.array([0.9, 0.1]),
    "kal ka paisa nahi aaya": np.array([0.8, 0.2]),
    "App keeps crashing": np.array([0.1, 0.9]),
}

names = list(messages)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        c, deg = angle_between(messages[names[i]], messages[names[j]])
        print(f"\n'{names[i]}' vs '{names[j]}'\n   cosine = {c:.2f}, angle = {deg:.0f} degrees")


# --- EXPLAIN ---
# What this demo does NOT do yet: we INVENTED the two axes and
# typed the scores ourselves. In Session 16.2, a model called
# sentence-transformers produces 384 numbers per sentence
# automatically - and the cosine formula above works unchanged.
# -------------------------------------------------------------
