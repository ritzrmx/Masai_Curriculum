# TA Live Code -- Session 6.2: Data Visualization
# Duration: ~5 minutes
# Concept: One labeled bar chart, built live

import matplotlib.pyplot as plt

branches = ["Hyderabad", "Mumbai", "Delhi"]
sales = [45000, 62000, 38000]

plt.bar(branches, sales)
plt.title("Branch-wise Sales")
plt.xlabel("Branch")
plt.ylabel("Sales (Rs.)")
plt.show()

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. Build it WITHOUT the title/labels first, ask "what does this show?"
#    -- then add title/xlabel/ylabel live and watch it become readable.
# 2. Point out: these are unordered categories, so bar (not line) is
#    correct -- ties back to the line-vs-bar trap from this session.
# ---------------------------------------------------------------------------
