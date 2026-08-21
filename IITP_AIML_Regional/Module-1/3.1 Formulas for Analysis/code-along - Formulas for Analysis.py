"""
CODE-ALONG (5-10 min) — Academic Session 6
Formulas for Analysis

PROBLEM
-------
Zappy Mart's Jaipur branch has 7 days of Units Sold and Sale Amount data.
Recreate SUM, AVERAGE, COUNT from scratch, then build a new calculated
column: average price per unit -- handling any day with 0 units sold
safely instead of crashing.
"""

units_sold = [40, 0, 38, 45, 41, 39, 44]
sale_amount = [8600, 0, 8100, 9700, 8900, 8400, 9500]


# --- SOLUTION -----------------------------------------------------------

def calculate_sum(numbers):
    return sum(numbers)


def calculate_average(numbers):
    return sum(numbers) / len(numbers)


def calculate_count(numbers):
    return len(numbers)


print(f"Total units sold:   {calculate_sum(units_sold)}")
print(f"Average units/day:  {calculate_average(units_sold):.1f}")
print(f"Days with data:     {calculate_count(units_sold)}")

print("\nCalculated column -- Avg Price per Unit:")
for day, (units, amount) in enumerate(zip(units_sold, sale_amount), start=1):
    if units == 0:
        price_per_unit = None  # avoid #DIV/0! -- flag it instead of guessing
    else:
        price_per_unit = amount / units
    print(f"  Day {day}: {price_per_unit if price_per_unit is None else round(price_per_unit, 2)}")
