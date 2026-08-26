# TA Live Code -- Session 7.1: SQL with MySQL Workbench
# Duration: ~5 minutes
# Concept: The same WHERE/GROUP BY question, run via sqlite3 in Python

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (city TEXT, amount INTEGER)")
conn.executemany("INSERT INTO orders VALUES (?, ?)", [
    ("Hyderabad", 650), ("Mumbai", 300), ("Hyderabad", 900), ("Delhi", 450)
])

result = conn.execute(
    "SELECT city, SUM(amount) AS total FROM orders GROUP BY city HAVING total > 500"
)
for row in result:
    print(row)

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. This is a REAL SQL query, running inside Python via sqlite3 --
#    not a simulation.
# 2. Compare this GROUP BY/HAVING line directly to the groupby() line
#    from the Session 5.2 TA demo -- same question, two syntaxes.
# 3. Change HAVING total > 500 to > 1000 live and show Hyderabad drop out.
# ---------------------------------------------------------------------------
