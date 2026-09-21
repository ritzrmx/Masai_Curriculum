"""
CODE-ALONG (5-10 min) — Academic Session 2
Analytics Workflow, Metrics & KPIs

PROBLEM
-------
Zappy Mart's goal this quarter: "grow revenue per branch by 10%."
You have last quarter's and this quarter's revenue (Rs) for each branch.

Convert the vague goal into an actual KPI: revenue growth % per branch,
and flag which branches actually hit the 10% target.
"""

revenue_last_quarter = {"Jaipur": 120000, "Udaipur": 90000, "Kanpur": 95000}
revenue_this_quarter = {"Jaipur": 138000, "Udaipur": 93000, "Kanpur": 106000}


# --- SOLUTION -----------------------------------------------------------

TARGET_GROWTH_PERCENT = 10

def growth_percent(old_value, new_value):
    return (new_value - old_value) / old_value * 100


print(f"{'Branch':10s} {'Growth %':>10s}  Hit target?")
for branch in revenue_last_quarter:
    old = revenue_last_quarter[branch]
    new = revenue_this_quarter[branch]
    growth = growth_percent(old, new)
    hit_target = growth >= TARGET_GROWTH_PERCENT
    print(f"{branch:10s} {growth:9.1f}%  {'YES' if hit_target else 'no'}")
