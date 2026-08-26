# TA Live Code -- Session 4.1: File Handling, JSON & APIs
# Duration: ~5 minutes
# Concept: Writing/reading a file safely, and parsing JSON

import json

with open("order.txt", "w") as f:
    f.write("Order: Chai, Rs.20\n")

with open("order.txt", "r") as f:
    print(f.read())

json_text = '{"name": "Priya", "orders": ["Chai", "Samosa"]}'
data = json.loads(json_text)
print(data["orders"][0])

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. `with` opens, writes, and auto-closes the file -- no .close() needed.
# 2. Reading it back proves the write actually persisted to disk.
# 3. json.loads turns TEXT into a real Python dict -- point out
#    data["orders"][0] works only AFTER loads(), not on the raw string.
# ---------------------------------------------------------------------------
