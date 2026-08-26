# TA Live Code -- Session 6.3: EDA & Business Thinking
# Duration: ~5 minutes
# Concept: A tiny funnel -- conversion rate at each stage

app_opens = 1000
add_to_cart = 400
checkouts = 150

cart_conversion = add_to_cart / app_opens
checkout_conversion = checkouts / add_to_cart

print(f"Open to cart:     {cart_conversion:.1%}")
print(f"Cart to checkout: {checkout_conversion:.1%}")

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. Run it -- two percentages appear instantly.
# 2. Ask: "where's the bigger drop-off -- and what would YOU investigate
#    next as a business analyst?"
# 3. This is the exact funnel math from the board, now runnable and
#    editable -- change the numbers live and watch the story shift.
# ---------------------------------------------------------------------------
