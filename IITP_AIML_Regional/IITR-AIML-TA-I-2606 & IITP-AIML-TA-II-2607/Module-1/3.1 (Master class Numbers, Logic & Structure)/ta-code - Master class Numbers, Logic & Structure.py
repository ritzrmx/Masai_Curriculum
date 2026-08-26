# TA Live Code -- Session 3.1 Master class: Numbers, Logic & Structure
# Duration: ~5 minutes
# Concept: Binary numbers and De Morgan's law, verified in code

print(bin(5))     # binary representation of 5
print(bin(13))    # binary representation of 13

A, B = True, False
print(not (A and B))          # De Morgan's law -- left side
print((not A) or (not B))     # De Morgan's law -- right side (should match)

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. bin(5) prints '0b101' -- read it right to left: 1+0+4 = 5, exactly
#    like we did by hand on the board.
# 2. Both De Morgan lines print True -- proving the "operator flips" rule
#    (and -> or) holds, not just on the board but in actual code.
# 3. Try (not A) and (not B) instead -- show it gives a DIFFERENT (wrong)
#    answer, reinforcing why the flip specifically matters.
# ---------------------------------------------------------------------------
