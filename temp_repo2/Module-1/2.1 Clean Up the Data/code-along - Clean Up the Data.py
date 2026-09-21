"""
CODE-ALONG (5-10 min) — Academic Session 4
Clean Up the Data

PROBLEM
-------
Zappy Mart's raw transaction log has a duplicate row (rows 2 and 4 are the
same sale entered twice) and one row with a missing sale amount.

Write code that (1) removes true duplicates and (2) flags rows with
missing values, without silently deleting them.
"""

transactions = [
    {"date": "2026-06-01", "store": "Jaipur", "amount": 8600},
    {"date": "2026-06-02", "store": "Jaipur", "amount": 7200},
    {"date": "2026-06-03", "store": "Jaipur", "amount": None},
    {"date": "2026-06-02", "store": "Jaipur", "amount": 7200},  # duplicate of row 2
]


# --- SOLUTION -----------------------------------------------------------

def remove_duplicates(rows):
    seen = set()
    unique_rows = []
    for row in rows:
        key = (row["date"], row["store"], row["amount"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)
    return unique_rows


def flag_missing_values(rows):
    return [row for row in rows if row["amount"] is None]


cleaned = remove_duplicates(transactions)
missing = flag_missing_values(cleaned)

print(f"Before cleaning: {len(transactions)} rows")
print(f"After removing duplicates: {len(cleaned)} rows")
print(f"Rows with missing amount (needs follow-up, not guessing): {missing}")
