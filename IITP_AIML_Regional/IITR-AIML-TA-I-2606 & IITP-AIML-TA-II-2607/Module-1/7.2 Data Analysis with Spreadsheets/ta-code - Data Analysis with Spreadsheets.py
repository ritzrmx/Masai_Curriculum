# TA Live Code -- Session 7.2: Data Analysis with Spreadsheets
# Duration: ~5 minutes
# Concept: A VLOOKUP-style lookup, done with pandas merge()

import pandas as pd

students = pd.DataFrame({"roll_no": [1, 2, 3], "name": ["Priya", "Rohan", "Meera"]})
marks = pd.DataFrame({"roll_no": [1, 2], "marks": [85, 76]})

result = pd.merge(students, marks, on="roll_no", how="left")
print(result)

# ---------------------------------------------------------------------------
# EXPLAIN:
# 1. This is conceptually what VLOOKUP/XLOOKUP does in Excel -- match on
#    roll_no, pull in the marks column.
# 2. Meera (roll_no 3) has no marks record -- her value shows as NaN,
#    the exact same "missing value" behavior as an Excel #N/A.
# 3. Point out: how="left" keeps her row anyway -- same deliberate-merge-
#    type lesson from Session 5.2, now visible in a lookup context.
# ---------------------------------------------------------------------------
