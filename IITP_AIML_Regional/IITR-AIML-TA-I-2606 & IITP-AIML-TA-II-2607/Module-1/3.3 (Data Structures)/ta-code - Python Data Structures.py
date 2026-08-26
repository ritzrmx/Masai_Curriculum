# TA Live Code -- Session 3.3: Python Data Structures
# Duration: ~5 minutes
# Concept: List vs tuple vs set -- same data, different rules

groceries_list = ["milk", "bread", "milk"]          # list: allows duplicates
groceries_set = set(groceries_list)                  # set: removes duplicates
home_coordinates = (17.385, 78.4867)                 # tuple: immutable

print(groceries_list)
print(groceries_set)
print(home_coordinates[0])

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. groceries_list keeps "milk" twice -- lists don't enforce uniqueness.
# 2. Converting to a set instantly drops the duplicate -- no loop needed.
# 3. Try home_coordinates[0] = 18.0 live -- show the TypeError, and tie
#    it back to "tuples are locked once created."
# ---------------------------------------------------------------------------
