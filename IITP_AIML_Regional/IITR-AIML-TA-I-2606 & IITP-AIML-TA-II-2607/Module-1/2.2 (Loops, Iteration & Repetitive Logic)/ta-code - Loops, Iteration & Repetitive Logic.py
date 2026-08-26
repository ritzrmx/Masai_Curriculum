# TA Live Code -- Session 2.2: Loops, Iteration & Repetitive Logic
# Duration: ~5 minutes
# Concept: for loop with break/continue, skipping over-budget items

prices = [200, 150, 0, 300, 450]

for price in prices:
    if price == 0:
        continue
    if price > 400:
        break
    print(f"Item within budget: Rs.{price}")

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. Trace it together before running -- ask the room what will print.
# 2. `continue` skips the Rs.0 item silently, loop keeps going.
# 3. `break` stops completely at Rs.450 -- the item never even prints,
#    and nothing after it (even if the list continued) would run either.
# 4. Change 450 to 500 live and show one more item now prints -- proves
#    the loop is genuinely evaluating each item, not just guessing.
# ---------------------------------------------------------------------------
