# =============================================================
# Session 24: Master Class - Probability & Counting
# TA Live Coding Demo — ~5 min typing, under 10 min total
# Scenario: Let's actually compute this Bayes' Theorem calculation
# in code, step by step, and then see the same effect show up in
# a churn-flagging scenario.
#
# Syntax scope check: pure arithmetic with plain Python variables -
# no libraries needed at all. This is deliberately a from-scratch
# conceptual demo, matching Session 19's hand-rolled approach,
# since the point is the reasoning, not any new syntax.
# =============================================================

# --- SETUP ---
# The exact disease-testing numbers from the board derivation:
# 1% of the population has the disease, the test is 90% accurate
# in both directions (sensitivity and specificity).
p_disease = 0.01                    # P(Disease)
p_positive_given_disease = 0.90     # P(Positive | Disease) - sensitivity
p_positive_given_no_disease = 0.10  # P(Positive | No Disease) - false positive rate
p_no_disease = 1 - p_disease        # P(No Disease)

print("Known probabilities:")
print(f"  P(Disease) = {p_disease}")
print(f"  P(Positive | Disease) = {p_positive_given_disease}")
print(f"  P(Positive | No Disease) = {p_positive_given_no_disease}")


# --- EXPLAIN ---
# Step 1 of Bayes' Theorem: find P(Positive) overall, by combining
# BOTH groups - the sick people who correctly test positive, and
# the healthy people who incorrectly test positive. This is exactly
# the board derivation from Concept Block 5.
# -------------------------------------------------------------

p_positive = (
    p_positive_given_disease * p_disease
    + p_positive_given_no_disease * p_no_disease
)

print(f"\nP(Positive) = ({p_positive_given_disease} x {p_disease}) + ({p_positive_given_no_disease} x {p_no_disease})")
print(f"P(Positive) = {p_positive:.4f}")


# --- EXPLAIN ---
# Step 2: apply Bayes' Theorem itself to find what we actually want -
# P(Disease | Positive), not P(Positive | Disease). These are NOT
# the same number, which is the entire point of today's session.
# -------------------------------------------------------------

p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

print(f"\nP(Disease | Positive) = ({p_positive_given_disease} x {p_disease}) / {p_positive:.4f}")
print(f"P(Disease | Positive) = {p_disease_given_positive:.4f} = {p_disease_given_positive:.1%}")
print("\nThis matches the board derivation: about 8.3%, NOT 90%.")


# --- EXPLAIN ---
# Now let's apply the exact same reasoning to a churn-flagging
# scenario, connecting straight back to Session 23's precision
# discussion. Suppose only 2% of partners actually churn in a
# given month, and our flagging system catches 95% of true
# churners but also incorrectly flags 5% of non-churners.
# -------------------------------------------------------------

p_churn = 0.02                     # P(Churn) - rare event
p_flag_given_churn = 0.95          # P(Flagged | Churn) - like recall
p_flag_given_no_churn = 0.05       # P(Flagged | No Churn) - false alarm rate
p_no_churn = 1 - p_churn

p_flag = (p_flag_given_churn * p_churn) + (p_flag_given_no_churn * p_no_churn)
p_churn_given_flag = (p_flag_given_churn * p_churn) / p_flag

print(f"\n--- Churn-flagging version ---")
print(f"P(Churn) = {p_churn}, P(Flagged|Churn) = {p_flag_given_churn}, P(Flagged|No Churn) = {p_flag_given_no_churn}")
print(f"P(Flagged) = {p_flag:.4f}")
print(f"P(Churn | Flagged) = {p_churn_given_flag:.4f} = {p_churn_given_flag:.1%}")


# --- EXPLAIN ---
# Notice: P(Churn | Flagged) here IS precision, in Session 23's
# vocabulary - "of everyone flagged, how many actually churned."
# Even with a strong 95% catch rate, because churn is rare, only
# about 28% of flagged partners are true churners. This is exactly
# why Session 23 insisted on checking precision directly rather
# than trusting a headline "95% catch rate" number alone.
#
# What this demo does NOT do yet: it doesn't connect this back to
# an actual trained model's real confusion matrix - that link (this
# theory explaining that practice) is exactly what Concept Block 6
# draws explicitly on the board.
# -------------------------------------------------------------
