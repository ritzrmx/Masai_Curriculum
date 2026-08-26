# TA Live Code -- Session 1.1: The AI Landscape & Programming Foundations
# Duration: ~5 minutes
# Concept: What does "AI" logic actually look like, at its simplest?

# ---------------------------------------------------------------------------
# SETUP (say this while typing):
# "We just spent this session talking about AI vs ML vs GenAI conceptually.
#  Let's actually SEE the simplest possible form of 'AI' -- a rule a human
#  wrote, that a computer follows to make a decision."
# ---------------------------------------------------------------------------

order_amount = 650

if order_amount >= 500:
    print(f"Order amount: Rs.{order_amount} -> Free delivery!")
else:
    print(f"Order amount: Rs.{order_amount} -> Delivery charges apply.")

# ---------------------------------------------------------------------------
# EXPLAIN (say this after running it):
#
# 1. This IS "AI" by our session's definition -- a machine making a decision
#    that normally needs a human ("should this order get free delivery?").
#
# 2. But notice: nobody "learned" this rule from data. *I* typed it.
#    That's the key giveaway this is NOT Machine Learning.
#
# 3. Change the number live -- try order_amount = 300, then 1000 -- and show
#    the decision flips. The RULE didn't change. Only the input did.
#
# 4. Bridge line: "If instead of me writing '>= 500', a computer looked at
#    10,000 past orders and FIGURED OUT that 500 was the right cutoff on
#    its own -- THAT would be Machine Learning. We're not there yet -- but
#    this simple if/else is the conceptual seed everything else builds on."
# ---------------------------------------------------------------------------
