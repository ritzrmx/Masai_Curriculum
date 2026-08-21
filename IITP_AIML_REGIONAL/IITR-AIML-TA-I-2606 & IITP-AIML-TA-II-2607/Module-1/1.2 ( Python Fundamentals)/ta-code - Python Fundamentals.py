# TA Live Code -- Session 1.2: Python Fundamentals
# Duration: ~5 minutes
# Concept: Variables, data types, and f-strings working together

name = input("What's your name? ")
item_count = int(input("How many items? "))
price = 49.5
total = item_count * price

print(f"Hi {name}, your total for {item_count} items is Rs.{total}")

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. `name` is a str, `item_count` is an int (converted from input's text),
#    `price` is a float -- three different data types, one line of output.
# 2. Point out: input() ALWAYS returns text -- that's why int() wraps it.
# 3. Try removing int() live and show the crash -- ties directly back
#    to today's "int vs str" trap.
# 4. The f-string weaves three variables into one readable sentence --
#    that's the whole point of today's session, in five lines.
# ---------------------------------------------------------------------------
