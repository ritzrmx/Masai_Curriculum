# TA Live Code -- Session 6.1 Master class: From Tables to Relationships
# Duration: ~5 minutes
# Concept: Mean vs median on skewed data

incomes = [25000, 28000, 30000, 32000, 5000000]

mean_income = sum(incomes) / len(incomes)
sorted_incomes = sorted(incomes)
median_income = sorted_incomes[len(incomes) // 2]

print(f"Mean:   Rs.{mean_income:,.0f}")
print(f"Median: Rs.{median_income:,.0f}")

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. Run it -- the mean shoots past Rs.10,00,000, the median stays at
#    Rs.30,000. Same five numbers, two very different "typical" values.
# 2. This is the crorepati uncle example from the board, now in code.
# 3. Ask: "which one would you trust to describe a TYPICAL family member?"
# ---------------------------------------------------------------------------
