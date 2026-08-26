# TA Live Code -- Session 5.2: Pandas -- Aggregation, Groupby & Merging
# Duration: ~5 minutes
# Concept: groupby, summarizing sales by city

import pandas as pd

df = pd.DataFrame({
    "city": ["Hyderabad", "Mumbai", "Hyderabad", "Delhi"],
    "amount": [650, 300, 900, 450]
})

city_sales = df.groupby("city")["amount"].sum()
print(city_sales)

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. One line replaces manually filtering and summing per city.
# 2. Point out Hyderabad's two rows (650 + 900) combine into one total --
#    that's the "pile sorting" from the receipts analogy, done instantly.
# 3. Ask: "what would happen if I called .sum() with no column specified?"
#    -- run df.groupby("city").sum() live and discuss the extra output.
# ---------------------------------------------------------------------------
