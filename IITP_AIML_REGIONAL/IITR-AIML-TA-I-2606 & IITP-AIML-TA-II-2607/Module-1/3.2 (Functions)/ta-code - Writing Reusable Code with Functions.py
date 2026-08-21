# TA Live Code -- Session 3.2: Writing Reusable Code with Functions
# Duration: ~5 minutes
# Concept: def, return, and default arguments together

def calculate_total(item_count, price=49.5):
    return item_count * price

order1 = calculate_total(3)
order2 = calculate_total(5, 60)
print(f"Order 1 total: Rs.{order1}")
print(f"Order 2 total: Rs.{order2}")

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. `price=49.5` is a default -- order1 uses it automatically.
# 2. order2 overrides BOTH parameters explicitly.
# 3. Point at `return` -- ask "what if this said print() instead?" --
#    live-edit it to print() and show order1 becomes None.
# 4. One function, reused twice, two different results -- that's the
#    entire pitch of today's session in four lines.
# ---------------------------------------------------------------------------
