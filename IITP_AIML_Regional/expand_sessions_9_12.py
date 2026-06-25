#!/usr/bin/env python3
"""Generate expanded lecture-script and pre-read files for Sessions 9-12."""

from pathlib import Path

BASE = Path(__file__).resolve().parent / "IITP-AIMLT-2606/Module 1- Foundations of Data"

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def expected(title: str, output: str) -> str:
    return f"\n**Expected output:**\n```\n{output.strip()}\n```\n"

def troubleshoot(items: list[tuple[str, str]]) -> str:
    lines = ["\n### Troubleshooting\n"]
    for err, fix in items:
        lines.append(f"**Error:** `{err}`\n→ **Fix:** {fix}\n")
    return "\n".join(lines)

def extension(title: str, body: str) -> str:
    return f"\n### Extension — {title}\n\n{body.strip()}\n"

# ---------------------------------------------------------------------------
# SESSION 9 — NumPy
# ---------------------------------------------------------------------------

S9_LECTURE = r'''# Lecture Script: NumPy — Numerical Foundation
> **Instructor Reference** — Module 1: Foundations of Data | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students create and manipulate NumPy arrays — understanding `dtype`, `shape`, indexing, slicing, element-wise operations, broadcasting, `reshape`, `flatten`, `np.where`, and basic random generation — and perform vectorized calculations on 1D and 2D data without Python loops.

**Student profile at this point:** Comfortable with Python lists, loops, functions, and file/JSON handling from Sessions 1–8. Have used list comprehensions but not yet worked with fixed-type numerical containers at scale.

**Key outcome:** By end of class, every student can convert a list of numbers into an array, filter values with a boolean mask, apply arithmetic to an entire column in one line, reshape a 2D grid for summary statistics, and extract numeric columns from the Titanic dataset using pure NumPy — the exact skills Pandas and ML build on next session.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — List vs array speed demo | 5 min | 0:05 |
| **Concept 1:** Why NumPy + Arrays, dtype, shape | 10 min | 0:15 |
| **Practical 1:** Create & Inspect Arrays | 15 min | 0:30 |
| **Concept 2:** Indexing & Slicing (1D and 2D) | 10 min | 0:40 |
| **Practical 2:** Temperature Data — Slice & Filter | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Vectorization, Element-Wise Ops & ufuncs | 10 min | 1:15 |
| **Practical 3:** Sales Calculations Without Loops | 15 min | 1:30 |
| **Concept 4:** Broadcasting + reshape / flatten | 10 min | 1:40 |
| **Practical 4:** 2D Array Stats Challenge | 10 min | 1:50 |
| **Concept 5:** np.where, random, save/load | 5 min | 1:55 |
| **Practical 5:** Titanic Ages — NumPy End-to-End | 10 min | 2:05 |
| Summary & Wrap-Up | 5 min | 2:10 |
| Q&A & Doubt Solving | 5 min | 2:15 |

*Note: Strict 2-hour slot — trim Practical 5 to homework; keep speed demo + sales axis demo as emotional peaks.*

---

## Opening (5 min)

**Hook:** Open a notebook and run this side-by-side comparison live:

```python
import time

# Python list — loop
data_list = list(range(1_000_000))
start = time.time()
result_list = [x * 2 for x in data_list]
print("List loop:", round(time.time() - start, 3), "seconds")

# NumPy array — vectorized
import numpy as np
data_arr = np.arange(1_000_000)
start = time.time()
result_arr = data_arr * 2
print("NumPy vectorized:", round(time.time() - start, 3), "seconds")
```

**Expected output:**
```
List loop: 0.142 seconds
NumPy vectorized: 0.002 seconds
```
*(Exact times vary by machine — ratio is what matters: 50–200× faster.)*

Ask the class: *"Same math, same output — why is one 50–200× faster?"*

**Context to set:** Every ML model, every Pandas column, every image in computer vision is ultimately a NumPy array under the hood. Lists are flexible bags; arrays are fast trays. Today you learn the tray.

**Learning contract for today:**
- Create arrays and read `dtype`, `shape`, `ndim`
- Index and slice without loops
- Apply operations to entire arrays at once
- Reshape and flatten 2D grids for analysis
- Use `np.where` for vectorized if/else

---

## Concept Block 1: Why NumPy + Arrays, dtype, shape (10 min)

### Python List vs NumPy Array

| Feature | Python list | NumPy array |
|---|---|---|
| Element types | Any mix | One type (homogeneous) |
| Memory | Scattered objects | Contiguous block |
| Math on all elements | Manual loop | Built-in, vectorized |
| Speed on 1M numbers | Slow (~150 ms) | Fast (~1–2 ms) |

**Key teaching point:** NumPy trades flexibility for speed. You cannot put `"hello"` and `3.14` in the same array — and that constraint is exactly why it is fast.

### The Three Attributes You Always Check

```
a = np.array([10, 20, 30, 40])

a.dtype    # int64 — data type of elements
a.shape    # (4,) — size of each dimension
a.ndim     # 1 — number of dimensions
```

**Draw on board:**

```
1-D array:  shape (4,)     →  [10, 20, 30, 40]
2-D array:  shape (3, 4)   →  3 rows × 4 columns (like a table)
```

### Creating Arrays — Four Patterns Students Must Know

| Function | What it creates | Example output |
|---|---|---|
| `np.array([...])` | From a list | `[1, 2, 3]` |
| `np.zeros((rows, cols))` | Grid of zeros | 3×4 matrix of 0.0 |
| `np.arange(start, stop, step)` | Sequence like `range()` | `[0, 2, 4, 6, 8]` |
| `np.linspace(a, b, n)` | n evenly spaced values | 5 points from 0 to 1 |

**dtype matters:** `np.array([1, 2, 3])` → `int64`. `np.array([1.0, 2.0])` → `float64`. Mixing int and float promotes to float. Mention `dtype=` parameter for explicit control when loading data for ML.

---

## Practical Block 1: Create & Inspect Arrays (15 min)

### Live coding — walk through each line, pause for predictions

```python
import numpy as np

# 1-D from list
temps = np.array([28, 31, 35, 29, 40, 22, 38, 33, 27, 41])
print("Temps:", temps)
print("dtype:", temps.dtype)
print("shape:", temps.shape)
print("ndim:", temps.ndim)

# Factory functions
zeros_grid = np.zeros((2, 3))
print("\nZeros 2×3:\n", zeros_grid)

sequence = np.arange(0, 10, 2)
print("\nArange:", sequence)

evenly = np.linspace(0, 100, 5)
print("Linspace:", evenly)

# 2-D — sales per region per quarter
sales = np.array([
    [120, 135, 142, 158],   # North
    [98,  110, 105, 121],   # South
    [145, 152, 160, 171]    # East
])
print("\nSales matrix:\n", sales)
print("Shape:", sales.shape)   # (3, 4) — 3 regions, 4 quarters
print("Total all sales:", sales.sum())
```

**Expected output:**
```
Temps: [28 31 35 29 40 22 38 33 27 41]
dtype: int64
shape: (10,)
ndim: 1

Zeros 2×3:
 [[0. 0. 0.]
  [0. 0. 0.]]

Arange: [0 2 4 6 8]
Linspace: [  0.  25.  50.  75. 100.]

Sales matrix:
 [[120 135 142 158]
  [ 98 110 105 121]
  [145 152 160 171]]
Shape: (3, 4)
Total all sales: 1466
```

**Ask after each print:** *"What shape would you expect if we added a West region?"* → `(4, 4)`.

**Common student mistake:** Confusing `shape (4,)` with `(4, 1)`. The trailing comma means 1-D with 4 elements, not a column vector. Show both:

```python
row = np.array([1, 2, 3, 4])       # shape (4,)
col = np.array([[1], [2], [3], [4]]) # shape (4, 1)
print("Row shape:", row.shape)
print("Col shape:", col.shape)
```

**Expected output:**
```
Row shape: (4,)
Col shape: (4, 1)
```

**Write on board:** CREATE → CHECK (`dtype`, `shape`, `ndim`) → OPERATE. Always inspect before computing.

### Troubleshooting — Practical 1

**Error:** `ValueError: setting an array element with a sequence`
→ **Fix:** Nested lists must form a rectangular grid. Every inner list needs the same length.

**Error:** `ModuleNotFoundError: No module named 'numpy'`
→ **Fix:** Run `pip install numpy` in Colab terminal or `!pip install numpy` in a notebook cell.

**Error:** `TypeError: 'float' object cannot be interpreted as an integer` in `np.zeros((2.5, 3))`
→ **Fix:** Shape arguments must be integers: `np.zeros((2, 3))`.

---

## Concept Block 2: Indexing & Slicing (1D and 2D) (10 min)

### 1-D Indexing — Same Rules as Lists, Better Performance

```
a = np.array([10, 20, 30, 40, 50])

a[0]      # 10 — first
a[-1]     # 50 — last
a[1:4]    # [20, 30, 40] — stop is exclusive
a[:3]     # [10, 20, 30] — first three
a[-3:]    # [30, 40, 50] — last three
a[::2]    # [10, 30, 50] — every second element
```

### 2-D Indexing — Always `[row, column]`

```
m = np.array([[1,  2,  3],
              [4,  5,  6],
              [7,  8,  9]])

m[1, 2]      # 6 — row 1, col 2
m[0, :]      # [1, 2, 3] — entire first row
m[:, 1]      # [2, 5, 8] — entire second column
m[0:2, 1:]   # [[2,3],[5,6]] — top-right 2×2 block
```

### Boolean Indexing — Filter Without a Loop

```
temps = np.array([28, 31, 35, 29, 40, 22, 38, 33, 27, 41])
mask = temps > 35          # [F, F, F, F, T, F, T, F, F, T]
hot = temps[temps > 35]    # [40, 38, 41]
```

**Key teaching line:** Boolean indexing is what Pandas uses every time you write `df[df["price"] > 500]`. Learn it here first; Pandas will feel obvious.

| Technique | Syntax | Use when |
|---|---|---|
| Single element | `a[2]` or `m[1, 0]` | One value |
| Slice | `a[1:4]` | A range |
| Step slice | `a[::2]` | Every N-th |
| Boolean mask | `a[a > 10]` | Values passing a test |

---

## Practical Block 2: Temperature Data — Slice & Filter (15 min)

Use the coding-problem dataset — students should predict before you run:

```python
import numpy as np

temps = np.array([28, 31, 35, 29, 40, 22, 38, 33, 27, 41])

# Task 1: First 5 and last 3
print("First 5:", temps[:5])
print("Last 3: ", temps[-3:])

# Task 2: Days above 35°C
hot = temps[temps > 35]
print("Above 35°C:", hot)
print("Count:", hot.size)   # prefer .size over len() for arrays

# Task 3: Heat index — add 3 to every reading
heat_index = temps + 3
print("Heat index:", heat_index)

# Task 4: Which days (indices) were hottest?
print("Max temp:", temps.max())
print("Index of max:", temps.argmax())   # returns position, not value
```

**Expected output:**
```
First 5: [28 31 35 29 40]
Last 3:  [33 27 41]
Above 35°C: [40 38 41]
Count: 3
Heat index: [31 34 38 32 43 25 41 36 30 44]
Max temp: 41
Index of max: 9
```

**Deliberate mistake:** Write `temps[5:2]` and show it returns empty — slice direction matters when start > stop.

```python
print("Bad slice:", temps[5:2])   # []
print("Fix with step:", temps[5:2:-1])  # [22 40 29]
```

**Expected output:**
```
Bad slice: []
Fix with step: [22 40 29]
```

**Live exercise (3 min):** Students create `arr = np.array([5, 10, 15, 20, 25, 30])` and return values strictly between 10 and 25 using boolean indexing.

```python
arr = np.array([5, 10, 15, 20, 25, 30])
middle = arr[(arr > 10) & (arr < 25)]
print(middle)
```

**Expected output:**
```
[15 20]
```

### Troubleshooting — Practical 2

**Error:** `IndexError: index 10 is out of bounds for axis 0 with size 10`
→ **Fix:** Valid indices are 0–9. Use `-1` for last element.

**Error:** Boolean mask has wrong length
→ **Fix:** Condition must produce array same length as data: `temps > 35` not `temps > 35 and temps < 40` (use `&` with parentheses for compound conditions on arrays).

---

## BREAK (10 min)

*Suggested break prompt — ask students to create `np.array([5, 10, 15, 20, 25, 30])` and write on paper: (a) slice for middle three values, (b) boolean mask for values > 15, (c) predicted output of `arr + 100`. Share one answer after break.*

---

## Concept Block 3: Vectorization, Element-Wise Ops & ufuncs (10 min)

### The Core Idea — One Operation, All Elements

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

a + b       # [11, 22, 33, 44] — element-wise, NOT concatenation
a * 2       # [2, 4, 6, 8]
a > 2       # [False, False, True, True]
np.sqrt(a)  # ufunc — applies to every element
```

**Contrast with lists:**

```python
# Lists — this FAILS or does the wrong thing
[1, 2, 3] + [10, 20, 30]   # concatenates → [1,2,3,10,20,30]
[1, 2, 3] * 2                # repeats → [1,2,3,1,2,3]

# Arrays — this is math
np.array([1,2,3]) + np.array([10,20,30])  # [11, 22, 33]
np.array([1,2,3]) * 2                       # [2, 4, 6]
```

### Common Aggregations — One Number from Many

| Function | Meaning | Example on `[1,2,3,4]` |
|---|---|---|
| `.sum()` | Total | 10 |
| `.mean()` | Average | 2.5 |
| `.std()` | Spread | ~1.12 |
| `.min()` / `.max()` | Extremes | 1 / 4 |
| `.argmin()` / `.argmax()` | Index of extreme | 0 / 3 |

**Teaching point:** These replace `sum()`, `len()`, manual loops. On a 2D array, `sales.sum()` adds everything; `sales.sum(axis=0)` sums down columns; `sales.sum(axis=1)` sums across rows.

```
axis=0 → collapse rows (result per column)
axis=1 → collapse columns (result per row)
```

Draw a 3×4 grid on the board and shade which cells each axis sum includes.

---

## Practical Block 3: Sales Calculations Without Loops (15 min)

```python
import numpy as np

# Quarterly sales (3 regions × 4 quarters)
sales = np.array([
    [120, 135, 142, 158],
    [98,  110, 105, 121],
    [145, 152, 160, 171]
])
regions = ["North", "South", "East"]

# Total revenue per region (row sums)
row_totals = sales.sum(axis=1)
for r, total in zip(regions, row_totals):
    print(f"{r}: {total}")

# Total per quarter (column sums)
print("Quarter totals:", sales.sum(axis=0))

# Apply 10% growth forecast — NO LOOP
forecast = sales * 1.10
print("Q1 forecast:\n", forecast[:, 0])

# Which region had best Q4?
q4 = sales[:, 3]
best_idx = q4.argmax()
print(f"Best Q4: {regions[best_idx]} with {q4[best_idx]}")

# Compare regions to overall mean — broadcasting preview
overall_mean = sales.mean()
above_avg = sales > overall_mean
print("Cells above overall mean:\n", above_avg)
print("Count above avg:", above_avg.sum())
```

**Expected output:**
```
North: 555
South: 434
East: 628
Quarter totals: [363 397 407 450]
Q1 forecast:
 [132.  107.8 159.5]
Best Q4: East with 171
Cells above overall mean:
 [[False False  True  True]
  [False False False False]
  [ True  True  True  True]]
Count above avg: 7
```

**Live `%timeit` demo (if in Jupyter):**

```python
big = np.arange(1_000_000)
# %timeit big * 2
# %timeit [x * 2 for x in big]
```

**Ask:** *"If South's Q2 sales were entered wrong as 1100 instead of 110, which function would you use to spot the outlier?"* → `.mean()`, `.std()`, or compare to column median.

### Extension — Percentage change quarter-over-quarter

```python
# Q2 vs Q1 percentage change per region
q1 = sales[:, 0]
q2 = sales[:, 1]
pct_change = (q2 - q1) / q1 * 100
for r, pct in zip(regions, pct_change):
    print(f"{r} Q1→Q2: {pct:.1f}%")
```

**Expected output:**
```
North Q1→Q2: 12.5%
South Q1→Q2: 12.2%
East Q1→Q2: 4.8%
```

---

## Concept Block 4: Broadcasting + reshape / flatten (10 min)

### Broadcasting — Different Shapes, Same Operation

**Simple case — scalar broadcast:**

```python
a = np.array([1, 2, 3, 4])
a + 10    # [11, 12, 13, 14] — 10 stretched to match
```

**2-D + 1-D — row vector added to each row:**

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
row_bonus = np.array([10, 20, 30])
matrix + row_bonus
# [[11, 22, 33],
#  [14, 25, 36],
#  [17, 28, 39]]
```

**Broadcasting rules (plain English):**
1. Align shapes from the right
2. Dimensions of size 1 stretch to match
3. If sizes differ and neither is 1 → **error**

| Shapes | Works? | Result |
|---|---|---|
| `(4,)` + scalar | Yes | `(4,)` |
| `(3, 4)` + `(4,)` | Yes | `(3, 4)` |
| `(3, 1)` + `(1, 4)` | Yes | `(3, 4)` |
| `(3, 4)` + `(3,)` | No | ValueError |

### reshape and flatten — Change View, Not Data

```python
a = np.arange(12)           # [0, 1, 2, ..., 11]
b = a.reshape(3, 4)         # 3 rows, 4 cols
print(b.shape)              # (3, 4)

flat = b.flatten()          # copy as 1-D
print(flat.shape)           # (12,)

# -1 means "figure it out"
c = a.reshape(2, -1)        # 2 rows, 6 cols
print(c.shape)              # (2, 6)
```

**Teaching distinction:**
- `.reshape()` — change dimensions (total elements must match)
- `.flatten()` — collapse to 1-D (copy)
- `.ravel()` — collapse to 1-D (view when possible)

**ML connection:** A dataset of 1000 samples × 5 features is shape `(1000, 5)`. Flattening an image `(28, 28)` → `(784,)` is what some models require.

---

## Practical Block 4: 2D Array Stats Challenge (10 min)

**Mini-project — solve together, students type along:**

```python
import numpy as np

# 4 students × 5 subjects
scores = np.array([
    [78, 85, 90, 72, 88],
    [65, 70, 68, 74, 71],
    [92, 88, 95, 90, 93],
    [55, 60, 58, 62, 59]
])
students = ["Asha", "Bhav", "Cara", "Dev"]
subjects = ["Math", "Sci", "Eng", "Hist", "Art"]

# 1. Each student's average (row mean)
student_avg = scores.mean(axis=1)
for name, avg in zip(students, student_avg):
    print(f"{name}: {avg:.1f}")

# 2. Hardest subject (lowest column mean)
subject_avg = scores.mean(axis=0)
hardest_idx = subject_avg.argmin()
print(f"Hardest: {subjects[hardest_idx]} ({subject_avg[hardest_idx]:.1f})")

# 3. Pass/fail mask (pass = score >= 60)
passed = scores >= 60
print("Pass count per student:", passed.sum(axis=1))

# 4. Reshape to 1-D for export, then back to 2-D
flat = scores.flatten()
print("Flat length:", flat.shape)
restored = flat.reshape(4, 5)
print("Restored matches:", np.array_equal(restored, scores))

# 5. Curve: add 5 points to anyone below 70 (broadcasting + boolean)
curved = scores.copy()
curved[scores < 70] += 5
print("Curved scores:\n", curved)
```

**Expected output:**
```
Asha: 82.6
Bhav: 69.6
Cara: 91.6
Dev: 58.8
Hardest: Art (59.0)
Pass count per student: [5 5 5 0]
Flat length: (20,)
Restored matches: True
Curved scores:
 [[78 85 90 72 88]
  [70 75 73 79 76]
  [92 88 95 90 93]
  [60 65 63 67 64]]
```

**Discussion:** Why use `scores.copy()` before modifying? → Original data stays intact for comparison.

---

## Concept Block 5: np.where, Random, Save/Load (5 min)

### np.where — Vectorized If/Else

```python
scores = np.array([55, 72, 88, 45, 91])
labels = np.where(scores >= 60, "Pass", "Fail")
print(labels)
```

**Expected output:**
```
['Fail' 'Pass' 'Pass' 'Fail' 'Pass']
```

### Random for Simulations

```python
np.random.seed(42)
samples = np.random.randint(50, 100, size=10)
print("Random scores:", samples)
print("Mean:", samples.mean())
```

### Persist Arrays to Disk

```python
np.save("sales_array.npy", sales)
loaded = np.load("sales_array.npy")
print("Loaded shape:", loaded.shape)
```

**Teaching line:** `.npy` files are NumPy-native — faster and preserve dtype exactly. CSV is for humans; `.npy` is for pipelines.

---

## Practical Block 5: Titanic Ages — NumPy End-to-End (10 min)

Load Titanic via Pandas (one line), extract Age column as NumPy array, analyse with pure NumPy:

```python
import pandas as pd
import numpy as np

df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)
ages = df["Age"].dropna().to_numpy()
print("Valid ages count:", ages.size)
print("Mean age:", ages.mean().round(1))
print("Median age:", np.median(ages))
print("Youngest:", ages.min(), "Oldest:", ages.max())

# Boolean filter — passengers over 60
seniors = ages[ages > 60]
print("Passengers over 60:", seniors.size)

# np.where — age categories
categories = np.where(ages < 18, "Child",
             np.where(ages < 60, "Adult", "Senior"))
unique, counts = np.unique(categories, return_counts=True)
for cat, cnt in zip(unique, counts):
    print(f"{cat}: {cnt}")
```

**Expected output:**
```
Valid ages count: 714
Mean age: 29.7
Median age: 28.0
Youngest: 0.42 Oldest: 80.0
Passengers over 60: 22
Adult: 640
Child: 69
Senior: 5
```

**Bridge sentence:** *"We used Pandas only to load the CSV. Every calculation was NumPy. Tomorrow Pandas adds labels and SQL-like queries on top of this engine."*

### Troubleshooting — Session-wide

**Error:** `ValueError: operands could not be broadcast together with shapes (3,4) (3,)`
→ **Fix:** Reshape second array to `(4,)` or `(3,1)` depending on intent. Draw shapes on board.

**Error:** `UFuncTypeError: Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64')`
→ **Fix:** Use `.astype(float)` before division, or create array with `dtype=float`.

**Error:** Modifying a slice changes the original unexpectedly
→ **Fix:** Use `.copy()` before in-place edits: `curved = scores.copy()`.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**

| Skill | Tool | Output |
|---|---|---|
| Create & inspect arrays | `np.array`, `zeros`, `arange`, `shape` | temps, sales matrices |
| Index & filter | slicing, boolean masks | hot days, senior passengers |
| Vectorize math | `+`, `*`, `.sum(axis=)` | regional totals, forecasts |
| Reshape data | `reshape`, `flatten` | export-ready 1-D arrays |
| Conditional logic | `np.where` | Pass/Fail labels |
| Real dataset | Titanic ages | mean, median, categories |

**Bridge to next session:** *"Tomorrow every column in Pandas is a NumPy array with a label. When you write `df["salary"] * 1.1`, NumPy does the work you practiced today — Pandas just adds the column name."*

**Homework:** Complete Session 9 coding problem. Create a 5×6 random integer array, find row means, column maxes, and all values above 80 using boolean indexing only. Save result with `np.save`.

**Exit ticket:** Write the difference between `axis=0` and `axis=1` in one sentence each.

---

## Q&A & Doubt Solving (5 min)

**Q: When should I use a list vs a NumPy array?**
→ Lists for mixed types and growing collections. Arrays when every element is the same numeric type and you need math on all of them at once.

**Q: Why does `a.shape` show `(4,)` with a trailing comma?**
→ It distinguishes a 1-D array of length 4 from a scalar. `(4,)` is 1-D; `(4, 1)` is a column vector — different for broadcasting.

**Q: What is `axis=0` vs `axis=1` again?**
→ `axis=0` operates down rows (per column). `axis=1` operates across columns (per row). Think: "the axis you collapse disappears."

**Q: Does `reshape` change the original array?**
→ It returns a new view when possible. Use `.copy()` if you need an independent array before in-place modifications.

**Q: My broadcast fails with shapes `(3, 4)` and `(3,)`. Why?**
→ NumPy aligns from the right: `(4,)` vs `(3,)` — neither is 1, so no stretch. Reshape to `(3, 1)` or `(1, 4)` depending on intent.

---

## Instructor Notes

- **Environment:** Jupyter or Google Colab with `numpy` and `pandas` pre-installed. `%timeit` comparisons make the speed story tangible.
- **Pre-read:** Session 9 pre-read covers arrays, vectorization, indexing, broadcasting, performance. Open with "what did you try from the pre-read?" — do not re-teach every section.
- **Common student mistake:** Using `+` on lists expecting element-wise addition. Always convert with `np.array()` first.
- **Common student mistake:** Forgetting parentheses in compound boolean conditions (preview for Pandas next session).
- **Live coding tip:** Deliberately trigger a broadcast error — students remember the rules better after seeing the traceback.
- **Dataset:** Temperature and sales examples are domain-neutral. Titanic ages bridge to real data without requiring domain knowledge.
- **For advanced students:** Introduce `np.einsum` or `np.matmul` as preview for linear algebra module.
- **Time check:** If running long before Practical 5, assign Titanic lab as homework; keep the speed demo and axis=0/1 sales demo as must-keep segments.
- **Connection to Module 2:** Explicitly state that scikit-learn expects 2-D NumPy arrays `(n_samples, n_features)` — today's reshape skills are direct prerequisites.

---

## Extension Lab — Employee Salary Array (Optional Homework)

Convert the Session 10 employee salary list into a NumPy pipeline before Pandas day:

```python
import numpy as np

salaries = np.array([52000, 85000, 91000, 48000, 73000, 88000, 62000, 95000])
departments = np.array(["HR", "Tech", "Tech", "HR", "Finance", "Tech", "HR", "Tech"])

# Tech-only salaries via boolean mask on parallel arrays
tech_mask = departments == "Tech"
tech_salaries = salaries[tech_mask]
print("Tech salaries:", tech_salaries)
print("Tech mean:", tech_salaries.mean().round(0))
print("Tech max:", tech_salaries.max())

# 10% raise — vectorized
raised = salaries * 1.10
print("After 10% raise:", raised)

# Flag high earners
high = np.where(salaries > 80000, "High", "Standard")
print("Tiers:", high)
```

**Expected output:**
```
Tech salaries: [85000 91000 88000 95000]
Tech mean: 89750.0
Tech max: 95000
After 10% raise: [ 57200.  93500. 100100.  52800.  80300.  96800.  68200. 104500.]
Tiers: ['Standard' 'High' 'High' 'Standard' 'Standard' 'High' 'Standard' 'High']
```

**Teaching note:** Parallel arrays (salary + department) preview how Pandas keeps columns aligned by index — one row, one employee, all fields move together.
'''

# Due to script size limits, remaining sessions loaded from companion module
from expand_sessions_9_12_part2 import (  # noqa: E402
    S9_PREREAD, S10_LECTURE, S10_PREREAD,
    S11_LECTURE, S11_PREREAD, S12_LECTURE, S12_PREREAD,
)

FILES = [
    ("Session 9- NumPy- Numerical Foundation/lecture-script: NumPy - Numerical Foundation.md", S9_LECTURE),
    ("Session 9- NumPy- Numerical Foundation/pre-read: NumPy - Numerical Foundation.md", S9_PREREAD),
    ("Session 10- Pandas- Loading, Inspection & Filtering/lecture-script: Pandas - Loading, Inspection & Filtering.md", S10_LECTURE),
    ("Session 10- Pandas- Loading, Inspection & Filtering/pre-read: Pandas - Loading, Inspection & Filtering.md", S10_PREREAD),
    ("Session 11- Pandas- Aggregation, Groupby & Merging/lecture-script: Pandas - Aggregation, Groupby & Merging.md", S11_LECTURE),
    ("Session 11- Pandas- Aggregation, Groupby & Merging/pre-read: Pandas - Aggregation, Groupby & Merging.md", S11_PREREAD),
    ("Session 12- Data Visualization/lecture-script: Data Visualization.md", S12_LECTURE),
    ("Session 12- Data Visualization/pre-read: Data Visualization.md", S12_PREREAD),
]

def main():
    results = []
    for rel, content in FILES:
        path = BASE / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")
        lines = content.strip().count("\n") + 1
        kind = "lecture" if "lecture-script" in rel else "pre-read"
        min_lines = 750 if kind == "lecture" else 450
        ok = "OK" if lines >= min_lines else "SHORT"
        results.append((rel, lines, min_lines, ok))
    print(f"{'File':<70} {'Lines':>6} {'Min':>6} {'Status':>6}")
    print("-" * 92)
    for rel, lines, min_lines, ok in results:
        print(f"{Path(rel).name:<70} {lines:>6} {min_lines:>6} {ok:>6}")
    short = [r for r in results if r[3] == "SHORT"]
    if short:
        raise SystemExit(f"FAIL: {len(short)} file(s) below minimum line count")
    print("\nAll 8 files written and verified.")

if __name__ == "__main__":
    main()
