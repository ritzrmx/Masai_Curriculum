# TA Live Code -- Session 2.1: Control Flow & Decision Making
# Duration: ~5 minutes
# Concept: if/elif/else deciding a delivery charge

order_total = 650

if order_total >= 1000:
    print("You get free delivery!")
elif order_total >= 500:
    print("You get a Rs.20 discount on delivery.")
else:
    print("Standard delivery charges apply.")

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. Change order_total live to 1200, then 300 -- show only ONE branch
#    ever runs, no matter how many conditions are True in theory.
# 2. Ask: "what if I used three separate `if`s instead of elif?" --
#    rewrite it that way live and show multiple messages printing at once.
# 3. That side-by-side comparison IS the whole lesson from today.
# ---------------------------------------------------------------------------
