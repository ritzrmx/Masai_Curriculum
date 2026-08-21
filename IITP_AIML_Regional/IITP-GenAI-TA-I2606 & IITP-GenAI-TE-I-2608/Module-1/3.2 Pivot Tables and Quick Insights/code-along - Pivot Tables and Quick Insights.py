"""
CODE-ALONG (5-10 min) — Academic Session 7
Pivot Tables and Quick Insights

PROBLEM
-------
Zappy Mart's raw transactions span 5 branches. Build a "pivot table"
from scratch -- group by Store City and sum the Sale Amount for each --
then identify the leader and the laggard.
"""

transactions = [
    {"store": "Jaipur", "amount": 8600},
    {"store": "Udaipur", "amount": 9100},
    {"store": "Jaipur", "amount": 7200},
    {"store": "Kanpur", "amount": 6100},
    {"store": "Udaipur", "amount": 5300},
    {"store": "Kanpur", "amount": 7000},
]


# --- SOLUTION -----------------------------------------------------------

def pivot_sum_by_category(rows, category_key, value_key):
    totals = {}
    for row in rows:
        category = row[category_key]
        totals[category] = totals.get(category, 0) + row[value_key]
    return totals


totals_by_store = pivot_sum_by_category(transactions, "store", "amount")

print("Sum of Sale Amount by Store City:")
for store, total in totals_by_store.items():
    print(f"  {store:10s} Rs {total}")

leader = max(totals_by_store, key=totals_by_store.get)
laggard = min(totals_by_store, key=totals_by_store.get)
gap = totals_by_store[leader] - totals_by_store[laggard]

print(f"\nInsight: {leader} leads, {laggard} lags by Rs {gap} --")
print("worth checking why before deciding next steps.")
