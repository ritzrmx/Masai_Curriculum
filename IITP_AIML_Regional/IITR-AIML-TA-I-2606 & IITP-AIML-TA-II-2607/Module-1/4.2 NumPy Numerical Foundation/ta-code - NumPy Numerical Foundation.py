# TA Live Code -- Session 4.2: NumPy: Numerical Foundation
# Duration: ~5 minutes
# Concept: Broadcasting -- one operation, whole array, no loop

import numpy as np

prices = np.array([49.5, 20, 15, 99.9])
discounted = prices * 0.9
print(discounted)

plain_list = [49.5, 20, 15, 99.9]
print(plain_list * 2)   # NOT the same operation -- repeats the list

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. `prices * 0.9` applies 10% off to EVERY element, instantly, no loop.
# 2. Now show plain_list * 2 -- it repeats the list, doesn't multiply
#    each value. Same symbol, completely different meaning.
# 3. One-line takeaway: "numerical math needs a NumPy array, not a list."
# ---------------------------------------------------------------------------
