# TA Live Code -- Session 5.1: Pandas -- Loading, Inspection & Filtering
# Duration: ~5 minutes
# Concept: Inspecting a small DataFrame, then filtering it

import pandas as pd

df = pd.DataFrame({
    "city": ["Hyderabad", "Mumbai", "Hyderabad", "Delhi"],
    "amount": [650, 300, 900, 450]
})

print(df.head())
print(df.shape)

big_orders = df[df["amount"] > 500]
print(big_orders)

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. head() and shape give a quick first look -- same habit as a real CSV.
# 2. df["amount"] > 500 builds a True/False column, one row per order.
# 3. Wrapping that in df[...] keeps only the True rows -- boolean indexing,
#    the exact same logic as if/elif/else from Session 2.1.
# ---------------------------------------------------------------------------
