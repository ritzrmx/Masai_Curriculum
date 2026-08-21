"""
CODE-ALONG (5-10 min) — Academic Session 5
Make Data Ready for Analysis

PROBLEM
-------
Zappy Mart's Store City column has inconsistent entries, and the Sale
Amount column mixes plain numbers with text like "Rs1,200".

Write code that standardizes both columns so they're ready for analysis.
"""

raw_rows = [
    {"store": "jaipur", "amount": "8600"},
    {"store": "JAIPUR ", "amount": "Rs7,200"},
    {"store": "Udaipur", "amount": "9100"},
]


# --- SOLUTION -----------------------------------------------------------

def standardize_city(name):
    return name.strip().title()


def standardize_amount(value):
    cleaned = value.replace("Rs", "").replace(",", "").strip()
    return float(cleaned)


ready_rows = []
for row in raw_rows:
    ready_rows.append({
        "store": standardize_city(row["store"]),
        "amount": standardize_amount(row["amount"]),
    })

print("Before:", raw_rows)
print("After: ", ready_rows)

unique_cities = {row["store"] for row in ready_rows}
print(f"\nUnique store names after standardizing: {unique_cities}")
print("-> Down from 3 messy variants to the real number of branches.")
