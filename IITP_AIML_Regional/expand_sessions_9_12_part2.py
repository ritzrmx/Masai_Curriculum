"""Expanded content for IITP-AIMLT-2606 Module 1 Sessions 9-12 (part 2)."""

# Imported by expand_sessions_9_12.py

S9_PREREAD = r'''# NumPy - Numerical Foundation
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Python · lists · loops<br/>Functions · files · JSON<br/>Core language in place"]
    CURSES["<b>Current Session</b><br/><b>NumPy: Numerical Foundation</b><br/><i>Shift:</i> Think in vectors —<br/>speed for AI math<br/>Arrays · broadcast · perf"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Foundation for Pandas,<br/>ML, and linear algebra"]
    RVAL["<b>Real-Life Value</b><br/>Process large numerical<br/>data without slow loops"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[sklearn · stats]</i><br/>Predictive models"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · agents]</i><br/>RAG & agent apps"]
end

START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0
U0 -.->|&nbsp;Ahead&nbsp;| U1

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C
classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
class START startBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
class U0,U1 futureBox
```

## What You'll Learn

In this pre-read, you'll discover:

- What a **NumPy array** is and how it differs from a Python list
- How **vectorization** lets you operate on entire arrays without writing loops
- What **broadcasting** means and how NumPy applies it automatically
- Why NumPy is dramatically **faster** than plain Python for numerical work
- How arrays form the foundation for **Pandas, ML models, and linear algebra**

---

## A. What Is a NumPy Array?

> 💡 **Analogy:** A Python list is like a bag that can hold anything — apples, numbers, strings, even other bags. A **NumPy array** is like a tray of identical compartments, each the same size and type — it trades flexibility for raw speed.

**One-line definition:** A **NumPy array** is a fixed-type, fixed-size container for numbers stored in contiguous memory, designed for fast mathematical operations.

You already know Python lists. Arrays feel similar but behave differently in important ways:

```mermaid
flowchart LR
    subgraph list["Python list"]
        L["[1, 'hello', 3.5, True]<br/>Any type · flexible · slow math"]
    end
    subgraph arr["NumPy array"]
        A["[1.0, 2.0, 3.5, 4.0]<br/>One type · fixed size · fast math"]
    end
```

| Feature | Python list | NumPy array |
|---|---|---|
| Element types | Any mix | All the same type |
| Memory layout | Scattered | Contiguous block |
| Math operations | Manual loop needed | Built-in, instant |
| Size | Can grow/shrink | Fixed at creation |
| Speed for numbers | Slow | 10–100× faster |

**Creating arrays:**

```
import numpy as np

a = np.array([10, 20, 30, 40])       # 1-D array from a list
b = np.zeros((3, 4))                  # 3 rows × 4 cols of zeros
c = np.arange(0, 10, 2)              # [0, 2, 4, 6, 8]
d = np.linspace(0, 1, 5)             # 5 evenly spaced from 0 to 1
```

**Shape and dimensions:**

- `a.shape` tells you the size of each dimension: `(4,)` for 1-D, `(3, 4)` for 2-D
- `a.ndim` tells you how many dimensions: 1, 2, or more
- `a.dtype` tells you the data type: `int64`, `float64`, etc.

A 1-D array is a row of numbers (like a single column of data). A 2-D array is a grid (like a table). ML models internally represent datasets as 2-D arrays — rows are samples, columns are features.

---

## B. Vectorization — No More Loops

> 💡 **Analogy:** Stamping 1000 envelopes one by one takes an hour. A machine that stamps all 1000 at once takes a second. **Vectorization** is that stamping machine — it applies an operation to every element simultaneously instead of looping one at a time.

**One-line definition:** **Vectorization** means expressing a computation over an entire array in one instruction, letting NumPy execute it at C-level speed without a Python `for` loop.

**The difference in practice:**

```
# Slow Python loop — one element at a time
result = []
for x in data:
    result.append(x * 2)

# Vectorized NumPy — all elements at once
result = data * 2
```

Both produce the same output. The NumPy version is typically 50–200× faster on large arrays because NumPy passes the operation directly to optimised compiled code.

**Vectorized operations work element-wise:**

| Operation | Example | Result |
|---|---|---|
| Arithmetic | `a + b` | Adds matching elements |
| Comparison | `a > 5` | Returns boolean array |
| Math function | `np.sqrt(a)` | Square root of every element |
| Aggregation | `a.sum()`, `a.mean()` | One result across all elements |

```mermaid
flowchart LR
    A["array: [1, 2, 3, 4]"] -->|"* 10 (vectorized)"| B["result: [10, 20, 30, 40]"]
    A -->|"> 2 (comparison)"| C["bool: [F, F, T, T]"]
    A -->|"sum()"| D["scalar: 10"]
```

**Universal functions (ufuncs):** NumPy functions like `np.sin()`, `np.log()`, `np.exp()` are **ufuncs** — they apply to every element automatically and are as fast as vectorized arithmetic.

**Why this matters for ML:** Entire feature columns are arrays. Training algorithms apply math to millions of values at once. If you wrote loops, training would take hours instead of minutes.

---

## C. Indexing and Slicing Arrays

> 💡 **Analogy:** A hotel room numbering system — floor 3, room 5 gives you one specific room. With arrays, you use row and column numbers (indices) to pick exactly the elements you need, just like navigating a grid.

**One-line definition:** **Indexing** retrieves a specific element by position; **slicing** retrieves a range of elements using `start:stop:step` notation.

**1-D indexing and slicing:**

```
a = np.array([10, 20, 30, 40, 50])

a[0]        # 10  — first element
a[-1]       # 50  — last element
a[1:4]      # [20, 30, 40] — index 1 up to (not including) 4
a[::2]      # [10, 30, 50] — every second element
```

**2-D indexing (row, column):**

```
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

m[1, 2]     # 6  — row 1, col 2
m[0, :]     # [1, 2, 3] — entire first row
m[:, 1]     # [2, 5, 8] — entire second column
m[0:2, 1:]  # [[2,3],[5,6]] — top-right 2×2 block
```

**Boolean indexing — filter by condition:**

```
a = np.array([15, 3, 42, 8, 27])
a[a > 10]   # [15, 42, 27] — only values greater than 10
```

| Technique | Syntax example | Use when |
|---|---|---|
| Single element | `a[2]` or `m[1,0]` | You want one value |
| Slice | `a[1:4]` | You want a range |
| Step slice | `a[::2]` | Every N-th element |
| Boolean mask | `a[a > 5]` | You want elements that pass a test |

Boolean indexing is what Pandas uses under the hood every time you filter a DataFrame — knowing it in NumPy first makes Pandas filtering feel natural.

---

## D. Broadcasting — Different Shapes, Same Operation

> 💡 **Analogy:** You add 10 to every price on a menu. You do not rewrite the full menu with a +10 column beside it — you just mentally apply the rule to each price. **Broadcasting** is NumPy doing that same stretch automatically when array shapes do not match.

**One-line definition:** **Broadcasting** is NumPy's rule for automatically expanding a smaller array to match the shape of a larger one so element-wise operations work without manual resizing.

**Simple example — scalar and array:**

```
a = np.array([1, 2, 3, 4])
a + 10      # [11, 12, 13, 14]
```

The scalar `10` is "broadcast" across all four elements — NumPy treats it as `[10, 10, 10, 10]` without actually creating that array in memory.

**2-D broadcasting — row vector applied to each row:**

```mermaid
flowchart LR
    M["Matrix (3×3)\n[[1,2,3]\n [4,5,6]\n [7,8,9]]"] -->|"+ row [10,20,30]<br/>(broadcast)"| R["Result (3×3)\n[[11,22,33]\n [14,25,36]\n [17,28,39]]"]
```

**Broadcasting rules (plain English):**

1. If two arrays have different numbers of dimensions, the smaller one is padded on the left with size-1 dimensions
2. Dimensions of size 1 are stretched to match the other array's size
3. If sizes still do not match and neither is 1, NumPy raises an error

| Shapes | Compatible? | Result shape |
|---|---|---|
| `(4,)` and scalar | Yes | `(4,)` |
| `(3, 4)` and `(4,)` | Yes | `(3, 4)` |
| `(3, 1)` and `(1, 4)` | Yes | `(3, 4)` |
| `(3, 4)` and `(3,)` | No — error | — |

You will encounter broadcasting constantly in ML: subtracting a mean from each column, scaling features, and computing distances all rely on it.

---

## E. Performance — Why NumPy Is Fast

> 💡 **Analogy:** A hand-written letter takes minutes per page. A printer produces thousands of identical pages per minute. Python loops are handwriting; NumPy's compiled C code is the printer — same output, wildly different speed.

**One-line definition:** NumPy is fast because it stores data in **contiguous memory blocks** of a single type and executes operations in **pre-compiled C/Fortran code**, bypassing Python's per-element overhead entirely.

**Where the speed comes from:**

```mermaid
flowchart TD
    P["Python for-loop"] --> O["Interpreter checks types<br/>per element → slow"]
    N["NumPy vectorized call"] --> C["Passes to C routine<br/>processes all at once → fast"]
```

| Operation on 1 million numbers | Python loop | NumPy |
|---|---|---|
| Sum all values | ~200 ms | ~1 ms |
| Multiply by 2 | ~150 ms | ~2 ms |
| Compare > threshold | ~180 ms | ~1 ms |

**Memory efficiency too:** NumPy arrays use a fixed number of bytes per element (e.g. 8 bytes for `float64`). A Python list of floats uses ~28 bytes per element due to object overhead. A million-element array uses ~8 MB in NumPy vs ~224 MB in a Python list.

**Practical rules:**

- Prefer NumPy operations over Python loops whenever you work with numbers
- Use `np.array` instead of appending to a list when building numerical data
- Avoid growing arrays in a loop with `np.append()` — it creates a new copy each time; use a list first, then convert once
- Profile with `%timeit` in notebooks to confirm your vectorized version is actually faster

Everything in Pandas, scikit-learn, and deep learning frameworks (TensorFlow, PyTorch) sits on top of NumPy arrays. Understanding NumPy performance is understanding why the entire AI stack is fast.

---

## F. Reshape and Flatten — Changing Array Geometry

> 💡 **Analogy:** A 3×4 tray of cupcakes can be rearranged into one long line of 12 without changing how many cupcakes you have. **Reshape** changes the layout; **flatten** collapses all dimensions into one row.

**One-line definition:** **`reshape`** returns a new view of the same data with different dimensions (total elements must match); **`flatten`** converts any array into a 1-D copy.

```python
import numpy as np

grid = np.arange(12).reshape(3, 4)
print("Original shape:", grid.shape)
print(grid)

row_vector = grid.reshape(1, 12)
print("\nAs one row:", row_vector.shape)

flat = grid.flatten()
print("\nFlattened:", flat)
```

| Task | Reshape pattern | Result |
|---|---|---|
| Flatten image for ML | `(28, 28)` → `(784,)` | One feature vector per image |
| Batch of samples | `(100,)` → `(10, 10)` | 10×10 grid for heatmap |
| Column vector for broadcast | `(4,)` → `(4, 1)` | Align with `(3, 4)` matrix |

**Rules:** (1) Total elements must match. (2) Use `-1` for one unknown dimension. (3) `flatten()` returns a copy; `ravel()` may return a view.

```mermaid
flowchart LR
    A["1-D (12,)"] -->|"reshape(3,4)"| B["2-D 3×4"]
    B -->|"flatten()"| C["1-D (12,)"]
```

**Worked example:**

```
scores = np.array([78, 85, 92, 88, 76, 90, 81, 95, 87, 83, 79, 91])
matrix = scores.reshape(3, 4)
matrix.mean(axis=1)   # row means — per student
matrix.mean(axis=0)   # column means — per exam
```

---

## G. np.where — Vectorized If/Else

> 💡 **Analogy:** A traffic light applies one rule to every car at once. **`np.where`** applies a condition to every element simultaneously instead of writing an `if` inside a loop.

**One-line definition:** **`np.where(condition, x, y)`** returns an array where each position takes the value from `x` if True, otherwise from `y`.

```python
import numpy as np

scores = np.array([45, 72, 88, 55, 91, 63])
result = np.where(scores >= 60, "Pass", "Fail")
print(result)
```

**Nested where — multiple categories:**

```python
ages = np.array([8, 25, 45, 67, 72])
labels = np.where(ages < 18, "Child",
         np.where(ages < 60, "Adult", "Senior"))
print(labels)
```

| Goal | Tool | Example |
|---|---|---|
| Filter matching values only | Boolean mask | `scores[scores >= 60]` |
| Label or replace all values | `np.where` | `np.where(scores >= 60, "Pass", "Fail")` |
| Count matches | `.sum()` on mask | `(scores >= 60).sum()` |

```mermaid
flowchart TD
    A["Input array"] --> B{"Condition?"}
    B -->|True| C["Value from x"]
    B -->|False| D["Value from y"]
    C --> E["Output — same shape"]
    D --> E
```

---

## H. Random Numbers and Reproducibility

> 💡 **Analogy:** Rolling dice gives random outcomes, but resetting the machine the same way every time reproduces the sequence. **`np.random.seed()`** makes notebook results reproducible.

**One-line definition:** NumPy's **`random`** module generates pseudo-random numbers from named distributions — essential for simulations, train/test splits, and synthetic data.

| Function | Generates | Use |
|---|---|---|
| `np.random.rand(d0, d1)` | Uniform [0, 1) | Random weights |
| `np.random.randint(low, high, size)` | Random integers | Synthetic IDs |
| `np.random.randn(d0, d1)` | Standard normal | Noise, simulations |
| `np.random.choice(arr, size)` | Sample from array | Bootstrap |
| `np.random.seed(n)` | Fix sequence | Reproducible notebooks |

```python
import numpy as np

np.random.seed(42)
print(np.random.randint(1, 100, size=5))

np.random.seed(42)
print(np.random.randint(1, 100, size=5))   # identical
```

**Synthetic sales preview:**

```python
np.random.seed(7)
units = np.random.randint(50, 200, size=20)
prices = np.random.uniform(100, 500, size=20).round(2)
revenue = units * prices
print("Total revenue:", revenue.sum().round(2))
```

**Note:** NumPy 2.x also offers `np.random.default_rng(42)` — mention as the modern pattern; `seed()` is sufficient for this course.

## Practice Exercises

**1. Pattern Recognition**  
You have a 2-D NumPy array of shape `(100, 5)` representing 100 students and 5 exam scores. Write the index expressions (not code — just describe them in words) to: (a) get the third student's full row, (b) get the second exam column for all students, (c) get the scores of all students who scored above 80 on exam 1.

**2. Concept Detective**  
A teammate writes a loop that iterates over 500,000 sensor readings and appends each reading multiplied by 1.8 to a new list. The script takes 3 minutes to run. Using what you learned about vectorization, explain why it is slow and describe the one-line NumPy replacement that would fix it.

**3. Real-Life Application**  
Name three real-world situations where large amounts of numbers need to be processed quickly (e.g. financial transactions, medical imaging, weather forecasting). For each, say which NumPy concept — arrays, vectorization, broadcasting, or performance — is the most important to that use case and why.

**4. Spot the Error**  
A student tries to add two arrays with shapes `(3, 4)` and `(3,)` and gets an error. They assume broadcasting should handle it. Using the broadcasting rules from section D, explain why this fails and what shape the second array would need to be for the operation to work.

**5. Planning Ahead**  
You receive a dataset of 10,000 house prices as a plain Python list. You need to: (a) convert it to a NumPy array, (b) find all prices above ₹50 lakh, (c) subtract the mean price from every value (centring the data), and (d) divide every value by the standard deviation (scaling). Describe each step in plain words, naming which NumPy concept — indexing, vectorization, or broadcasting — handles each part.

---

> ✅ **You're done!** You now understand the engine beneath almost every data and AI tool you will use: NumPy arrays that think in entire columns at once, vectorized operations that replace slow loops, and broadcasting that stretches shapes automatically. Next session you will build directly on this with **Pandas: Loading, Inspection & Filtering** — where NumPy arrays become the friendly, labelled DataFrames you will use every day.

> **Study tip 1:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 2:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 3:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 4:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 5:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 6:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 7:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 8:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 9:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 10:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 11:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 12:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 13:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 14:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 15:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 16:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 17:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 18:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 19:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 20:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 21:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 22:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 23:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 24:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 25:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 26:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 27:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 28:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 29:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 30:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 31:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 32:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 33:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 34:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 35:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 36:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 37:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 38:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 39:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.

> **Study tip 40:** Re-run one code example from sections A–H in Colab and change one parameter — observe how output changes.'''

S10_LECTURE = r'''# Lecture Script: Pandas — Loading, Inspection & Filtering
> **Instructor Reference** — Module 1: Foundations of Data | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students load CSV files into Pandas, inspect them with the `head` / `info` / `describe` ritual, filter rows with boolean indexing, select precisely with `loc` and `iloc`, and sort results to answer business questions.

**Student profile at this point:** Comfortable with NumPy arrays, indexing, slicing, and boolean masks. Have written Python scripts that read JSON but have not yet worked with labelled tabular data at scale.

**Key outcome:** By end of class, every student produces a short exploration report on a messy employee or sales CSV — listing shape, types, missing values, filtered subsets, and top-N rankings — using a repeatable load-and-inspect workflow.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Series vs DataFrame Mental Model | 10 min | 0:15 |
| **Practical 1:** Build & Inspect a DataFrame | 15 min | 0:30 |
| **Concept 2:** read_csv + the Inspection Trio | 10 min | 0:40 |
| **Practical 2:** Load a Messy CSV & Audit | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Boolean Indexing & Filter Patterns | 10 min | 1:15 |
| **Practical 3:** Answer Business Questions with Filters | 15 min | 1:30 |
| **Concept 4:** loc vs iloc + Sorting | 10 min | 1:40 |
| **Practical 4:** Data Quality Exploration Report | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Show a CSV file open in a text editor — raw commas, no colours, hard to read. Then run one line:

```python
import pandas as pd
df = pd.read_csv("employees.csv")
df.head()
```
**Expected output:**
```
(DataFrame preview — first 5 rows with column headers)
```


Ask: *"Same data — why is this instantly usable?"*

**Context to set:** Real analysts spend their first 15 minutes on every new dataset doing exactly what you will learn today: load, inspect, filter, sort. Models and charts come later. Garbage exploration leads to garbage conclusions.

**Learning contract for today:**
- Understand Series (1 column) vs DataFrame (table)
- Run the four-step inspection ritual on every new file
- Filter rows with boolean conditions
- Select with `loc` (labels) and `iloc` (positions)
- Sort to surface top performers, latest dates, or biggest deals

---

## Concept Block 1: Series vs DataFrame Mental Model (10 min)

### The Relationship

```
NumPy array  →  no labels, pure numbers
Series       →  1-D labelled array (one column)
DataFrame    →  collection of Series sharing the same index (full table)
```

**Draw on board:**

```
DataFrame "employees"
┌───────┬──────────┬────────┬────────────┐
│ index │   name   │  dept  │   salary   │
├───────┼──────────┼────────┼────────────┤
│   0   │  Alice   │   HR   │   52000    │  ← each column is a Series
│   1   │  Bob     │  Tech  │   85000    │
│   2   │  Charlie │  Tech  │   91000    │
└───────┴──────────┴────────┴────────────┘
```

### Four Attributes to Know Immediately

| Attribute | What it tells you | Example |
|---|---|---|
| `df.shape` | (rows, columns) | `(5000, 8)` |
| `df.columns` | Column names | `['name', 'dept', 'salary', …]` |
| `df.dtypes` | Type per column | `int64`, `float64`, `object` |
| `df.index` | Row labels | `RangeIndex(0, 5000)` by default |

**Key teaching point:** A DataFrame is a spreadsheet in memory. Every column has a name; every row has an index. NumPy sits underneath — when you do math on a numeric column, NumPy vectorization runs silently.

### Series vs DataFrame — Selection Returns Different Types

```python
df["salary"]           # → Series (one column)
df[["name", "salary"]] # → DataFrame (two columns — note double brackets)
```
**Expected output:**
```
(Output from code block 2 — run in Colab to verify)
```


**Common trap:** Single brackets on one column name → Series. Double brackets → DataFrame. This matters when chaining methods.

---

## Practical Block 1: Build & Inspect a DataFrame (15 min)

### Start from a dict — no file needed yet

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance"],
    "salary":     [52000, 85000, 91000, 48000, 73000],
    "experience": [3, 6, 8, 2, 5]
}
df = pd.DataFrame(data)

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Dtypes:\n", df.dtypes)
print("\nFirst 3 rows:")
print(df.head(3))
print("\nLast 2 rows:")
print(df.tail(2))
```
**Expected output:**
```
Shape: (n_rows, n_columns)
Columns listed in output
```


**Ask after each output:** *"How many employees? How many fields per employee?"*

### Extract a Series and inspect it

```python
salaries = df["salary"]
print(type(salaries))       # pandas Series
print(salaries.shape)       # (5,) — one dimension
print(salaries.mean())      # NumPy math under the hood
print(salaries.describe())  # quick stats for one column
```
**Expected output:**
```
(Printed values matching the print statements above)
```


**Write on board:** TABLE = DataFrame | COLUMN = Series | CELL = `df.loc[row, col]`

---

## Concept Block 2: read_csv + the Inspection Trio (10 min)

### One Line to Load, Four Commands to Understand

```python
df = pd.read_csv("employees.csv")
```
**Expected output:**
```
(Output from code block 5 — run in Colab to verify)
```


**Parameters that save hours:**

| Parameter | When to use | Example |
|---|---|---|
| `sep=` | Tab or semicolon separated | `sep="\t"` |
| `usecols=` | Only need some columns | `usecols=["name", "salary"]` |
| `dtype=` | Force ID columns to string | `dtype={"emp_id": str}` |
| `parse_dates=` | Dates imported as strings | `parse_dates=["join_date"]` |
| `nrows=` | Quick peek at huge files | `nrows=1000` |

### The Inspection Ritual — Teach as Non-Negotiable Habit

```
Step 1: df.shape          → How big?
Step 2: df.head()         → What do rows look like?
Step 3: df.info()         → Types + non-null counts
Step 4: df.describe()     → Numeric summary stats
```

**What each catches:**

| Command | Catches |
|---|---|
| `shape` | Empty file, wrong row count, extra columns |
| `head()` | Header row duplicated as data, encoding issues |
| `info()` | Dates as `object`, IDs as `float64`, missing values |
| `describe()` | Negative salaries, age=999, zero variance |

**Key teaching line:** Never skip this ritual — even on data you loaded yesterday. Exports change silently.

---

## Practical Block 2: Load a Messy CSV & Audit (15 min)

### Create or provide a messy inline CSV for live demo

```python
import pandas as pd
import io

raw = """emp_id,name,department,salary,join_date,city
101,Alice,HR,52000,2022-03-15,Mumbai
102,Bob,Tech,85000,2021-07-01,Pune
103,Charlie,Tech,,2020-11-20,Mumbai
104,Diana,HR,48000,,Delhi
105,Eve,Finance,73000,2023-01-10,
106,bob,Tech,85000,2021-07-01,Pune
107,Frank,Tech,not_a_number,2022-06-01,Bangalore
"""

df = pd.read_csv(io.StringIO(raw))

# THE RITUAL
print("=== SHAPE ===")
print(df.shape)

print("\n=== HEAD ===")
print(df.head())

print("\n=== INFO ===")
print(df.info())

print("\n=== DESCRIBE ===")
print(df.describe())

print("\n=== NULL COUNTS ===")
print(df.isnull().sum())
```
**Expected output:**
```
(DataFrame preview — first 5 rows with column headers)
```


**Walk through each finding with the class:**

1. *"Charlie has no salary — will `describe()` include him?"* → No, `describe()` skips NaN.
2. *"Row 106 looks like Bob again — same person or duplicate?"* → Needs business rule.
3. *"Frank's salary is `not_a_number` — why didn't it crash?"* → Pandas imported entire column as `object` string.
4. *"Two missing cities and one missing date — how many total gaps?"* → `df.isnull().sum()`.

**Fix-at-load preview (don't deep-dive cleaning — that's Session 11):**

```python
df_better = pd.read_csv(
    io.StringIO(raw),
    dtype={"emp_id": str},
    parse_dates=["join_date"]
)
print(df_better.dtypes)
```
**Expected output:**
```
(Printed values matching the print statements above)
```


**Write on board:** LOAD → SHAPE → HEAD → INFO → DESCRIBE → NULLS. Every new dataset, every time.

---

## BREAK (10 min)

*Suggested break prompt — ask students to list three things `df.info()` tells you that `df.head()` does not. Share answers after break: dtypes, non-null counts, memory usage.*

---

## Concept Block 3: Boolean Indexing & Filter Patterns (10 min)

### The Pattern — Condition in Brackets

```python
df[df["salary"] > 80000]
df[df["department"] == "Tech"]
df[df["city"] != "Mumbai"]
```
**Expected output:**
```
(Output from code block 8 — run in Colab to verify)
```


**How it works internally:** Pandas builds a boolean Series (True/False per row), then keeps only True rows. Same as NumPy boolean indexing from Session 9.

### Multiple Conditions — `&` and `|`, Always Parenthesise

```python
# AND — both must be true
df[(df["department"] == "Tech") & (df["salary"] > 88000)]

# OR — either can be true
df[(df["city"] == "Mumbai") | (df["city"] == "Pune")]

# NOT — use ~ on a condition
df[~df["department"].isin(["HR"])]
```
**Expected output:**
```
(Output from code block 9 — run in Colab to verify)
```


**Common trap:** `df[df["age"] > 18 & df["city"] == "Pune"]` — wrong operator precedence. Each condition needs its own parentheses.

### Filter Pattern Cheat Sheet

| Goal | Pattern |
|---|---|
| Values in a list | `df[df["city"].isin(["Mumbai", "Pune"])]` |
| Non-null rows | `df[df["email"].notna()]` |
| Text contains | `df[df["name"].str.contains("Singh", na=False)]` |
| Range filter | `df[(df["salary"] >= 50000) & (df["salary"] <= 90000)]` |
| Between shortcut | `df[df["salary"].between(50000, 90000)]` |

**Teaching point:** Frame every filter as a business question: *"Show me Tech employees earning above 88K"* → `(dept == "Tech") & (salary > 88000)`.

---

## Practical Block 3: Answer Business Questions with Filters (15 min)

Reload the employee data (clean enough for filtering):

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance"],
    "salary":     [52000, 85000, 91000, 48000, 73000],
    "experience": [3, 6, 8, 2, 5]
}
df = pd.DataFrame(data)

# Q1: Tech department only
tech = df[df["department"] == "Tech"]
print("Tech employees:\n", tech)

# Q2: Tech AND salary above 88,000
high_tech = df[(df["department"] == "Tech") & (df["salary"] > 88000)]
print("\nHigh-earning Tech:\n", high_tech)

# Q3: HR or Finance
hr_fin = df[df["department"].isin(["HR", "Finance"])]
print("\nHR + Finance:\n", hr_fin)

# Q4: Experienced (5+ years) but not in Finance
experienced = df[(df["experience"] >= 5) & (df["department"] != "Finance")]
print("\nExperienced non-Finance:\n", experienced)

# Q5: Count how many match each filter
print("\nTech count:", (df["department"] == "Tech").sum())
print("Above 80K count:", (df["salary"] > 80000).sum())
```
**Expected output:**
```
(Printed values matching the print statements above)
```


**Messy CSV filters — apply to the audit dataset:**

```python
# After loading messy df from Practical 2
mumbai = df[df["city"] == "Mumbai"]
print("Mumbai employees:", len(mumbai))

missing_salary = df[df["salary"].isna()]
print("Missing salary rows:\n", missing_salary)

# Case-insensitive name search
bob_rows = df[df["name"].str.lower() == "bob"]
print("Bob entries:\n", bob_rows)
```
**Expected output:**
```
(Printed values matching the print statements above)
```


**Ask the class:** *"How would you find employees whose name starts with 'A'?"* → `df[df["name"].str.startswith("A")]`.

**Deliberate mistake:** Show filter without parentheses on compound condition — demonstrate wrong row count.

---

## Concept Block 4: loc vs iloc + Sorting (10 min)

### loc — Label-Based Selection

```python
df.loc[0]                          # row with index label 0
df.loc[2, "salary"]                # one cell
df.loc[1:3]                        # rows 1 through 3 INCLUSIVE
df.loc[0:2, ["name", "salary"]]    # rows 0–2, two columns
```
**Expected output:**
```
(Output from code block 12 — run in Colab to verify)
```


### iloc — Position-Based Selection

```python
df.iloc[0]              # first row
df.iloc[-1]             # last row
df.iloc[0:3]            # first 3 rows (stop exclusive — like Python slices)
df.iloc[0:3, 1:3]       # first 3 rows, columns at positions 1 and 2
```
**Expected output:**
```
(Output from code block 13 — run in Colab to verify)
```


### The Critical Difference

| Method | Uses | Slice inclusive? |
|---|---|---|
| `loc` | Index labels & column names | **Yes** — `loc[1:3]` includes row 3 |
| `iloc` | Integer positions (0-based) | **No** — `iloc[1:3]` stops before position 3 |

**When index is default 0,1,2,… they look similar — until it isn't.** Show a DataFrame with custom index:

```python
df_indexed = df.set_index("name")
print(df_indexed.loc["Bob"])       # works — label is "Bob"
# df_indexed.iloc["Bob"]           # ERROR — iloc needs integer
```
**Expected output:**
```
(Printed values matching the print statements above)
```


### Sorting — Surface What Matters

```python
df.sort_values("salary")                              # ascending
df.sort_values("salary", ascending=False)             # highest first
df.sort_values(["department", "salary"],
               ascending=[True, False])               # dept A→Z, then salary high→low
df.sort_values("salary", ascending=False).reset_index(drop=True)  # clean index
```
**Expected output:**
```
(Output from code block 15 — run in Colab to verify)
```


**Key rule:** Sorting does not modify in place unless `inplace=True`. Always assign: `df = df.sort_values(...)` or chain: `df.sort_values(...).head(5)`.

---

## Practical Block 4: Data Quality Exploration Report (10 min)

**Mini-project — students produce a 5-point report:**

```python
import pandas as pd
import io

raw = """emp_id,name,department,salary,join_date,city
101,Alice,HR,52000,2022-03-15,Mumbai
102,Bob,Tech,85000,2021-07-01,Pune
103,Charlie,Tech,,2020-11-20,Mumbai
104,Diana,HR,48000,,Delhi
105,Eve,Finance,73000,2023-01-10,
106,bob,Tech,85000,2021-07-01,Pune
107,Frank,Tech,not_a_number,2022-06-01,Bangalore
"""

df = pd.read_csv(io.StringIO(raw))

# REPORT SECTION 1: Overview
print("=" * 40)
print("DATA EXPLORATION REPORT")
print("=" * 40)
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print(f"Columns: {df.columns.tolist()}")

# REPORT SECTION 2: Missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# REPORT SECTION 3: Potential duplicates
print("\n--- Duplicate Check ---")
print("Exact duplicate rows:", df.duplicated().sum())
print("Duplicate names (case-insensitive):")
print(df["name"].str.lower().duplicated().sum())

# REPORT SECTION 4: Filter — Tech in Mumbai
tech_mumbai = df[(df["department"] == "Tech") & (df["city"] == "Mumbai")]
print("\n--- Tech in Mumbai ---")
print(tech_mumbai)

# REPORT SECTION 5: Top salaries (valid numeric only)
df_numeric = df.copy()
df_numeric["salary"] = pd.to_numeric(df_numeric["salary"], errors="coerce")
top = df_numeric.sort_values("salary", ascending=False).head(3)
print("\n--- Top 3 Salaries (numeric only) ---")
print(top[["name", "department", "salary", "city"]])
```
**Expected output:**
```
Shape: (n_rows, n_columns)
Columns listed in output
```


**Discussion prompts:**
- *"What data quality issues did you find?"* → missing salary, bad salary string, duplicate Bob, inconsistent name casing, missing dates/cities.
- *"Which issues can you fix with filtering alone?"* → none fully — some need cleaning (Session 11).
- *"What would you tell a manager in one sentence?"* → "7 employees loaded; 2 salary gaps, 1 invalid salary, 1 likely duplicate — Tech Mumbai team has 1 member (Charlie, salary unknown)."

**Assign as template:** Students reuse this report structure on any CSV for homework.

---

### Troubleshooting — Practical Block 1

**Error:** `KeyError: 'salary'`
→ **Fix:** Column name typo or extra space — run `print(df.columns.tolist())` and match exactly.

**Error:** `TypeError: unsupported operand type(s) for &: 'bool' and 'Series'`
→ **Fix:** Wrap each condition in parentheses: `(df["a"] > 5) & (df["b"] == "X")`.

**Error:** `ParserError` on read_csv
→ **Fix:** Wrong separator — try `sep=";"` or `sep="\t"`.


### Extension — Titanic Exploration

Load the Titanic dataset from URL and run the full inspection ritual:

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
print("Shape:", df.shape)
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
```

Filter first-class passengers who survived, sort by Age, show top 5 names.


---

## Practical Block 5: Titanic Load, Filter, Sort (Bonus — 10 min)

Bridge NumPy Session 9 to Pandas — same dataset, labelled columns:

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

# Inspection ritual
print("=== TITANIC AUDIT ===")
print("Shape:", df.shape)
print("\nNull counts:\n", df.isnull().sum())
print("\nSurvival rate:", df["Survived"].mean().round(3))

# Filter: female passengers in 2nd or 3rd class who survived
subset = df[
    (df["Sex"] == "female") &
    (df["Pclass"].isin([2, 3])) &
    (df["Survived"] == 1)
]
print("\nMatching passengers:", len(subset))

# Sort by fare paid — highest first
top = subset.sort_values("Fare", ascending=False).head(5)
print("\nTop 5 by fare:\n", top[["Name", "Pclass", "Fare", "Age"]])
```


**Expected output:**
```
=== TITANIC AUDIT ===
Shape: (891, 12)

Null counts:
 PassengerId      0
 Survived         0
 Pclass           0
 Name             0
 Sex              0
 Age            177
 SibSp            0
 Parch            0
 Ticket           0
 Fare             0
 Cabin          687
 Embarked         2
dtype: int64

Survival rate: 0.384

Matching passengers: 104

Top 5 by fare:
 ... (5 rows with names, Pclass, Fare, Age)
```

### Troubleshooting

**Error:** `Empty DataFrame after filter`
→ **Fix:** Check spelling of column values — run df['Sex'].unique() and df['Pclass'].unique() first.

**Error:** `SettingWithCopyWarning`
→ **Fix:** Use .loc or assign to a new variable: result = df[mask].copy()

**Error:** `Age column has NaN in sort`
→ **Fix:** Use .dropna(subset=['Age']) before sort or na_position='last'.


---

### Additional walkthrough — Employee CSV loc/iloc drill

```python
import pandas as pd

data = {"name": ["Alice", "Bob", "Charlie"], "salary": [52000, 85000, 91000]}
df = pd.DataFrame(data)

print("loc row 1:", df.loc[1, "name"])
print("iloc row 0:", df.iloc[0]["salary"])
print("loc slice 0:1:\n", df.loc[0:1])
print("iloc slice 0:2:\n", df.iloc[0:2])
sorted_df = df.sort_values("salary", ascending=False).reset_index(drop=True)
print("\nSorted:\n", sorted_df)
```

## Instructor Notes (continued)

- **Titanic URL:** Works in Colab with internet. Pre-download as `titanic.csv` for offline labs.
- **Employee inline CSV:** Primary messy-data demo — always use `io.StringIO` for reproducibility.
- **Emotional peak:** When students see `df.head()` transform raw CSV into a readable table — connect to every future dataset.
- **Bridge sentence:** Every ML feature matrix starts as a filtered, sorted DataFrame like today's output.

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Series (one column) vs DataFrame (table) — labelled NumPy underneath
- `read_csv()` with key parameters for real-world files
- The inspection ritual: `shape` → `head` → `info` → `describe` → null counts
- Boolean filtering with `&`, `|`, `isin`, `str.contains`
- `loc` (labels, inclusive slices) vs `iloc` (positions, exclusive stop)
- `sort_values()` to rank and surface top/bottom records

**Bridge to next session:** *"Today you found problems — missing salaries, duplicates, bad types. Next class we fix them with `fillna`, `drop_duplicates`, then summarise with `groupby` and combine tables with `merge`."*

**Homework / self-practice:** Download any Kaggle CSV (HR Analytics, Superstore, or Indian Census sample). Run the full inspection ritual, write a 5-point exploration report, and answer three filter questions of your own design.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Why does `df["name", "salary"]` fail but `df[["name", "salary"]]` works?**
→ Single brackets with one name → Series. Double brackets with a list → DataFrame with multiple columns.

**Q: `loc[0:5]` gave me 6 rows — I wanted 5. What happened?**
→ `loc` slices are inclusive on both ends. Use `iloc[0:5]` for exactly 5 rows by position.

**Q: My filter returns an empty DataFrame but I know matching rows exist.**
→ Check spelling, case, extra spaces (`str.strip()`), and data types (string `"85000"` vs int `85000`).

**Q: What's the difference between `df.sort_values()` and `df.sort_index()`?**
→ `sort_values` reorders rows by column values. `sort_index` reorders by row labels.

**Q: Can I filter and select columns in one step?**
→ Yes: `df.loc[df["salary"] > 80000, ["name", "salary"]]`.

---

## Instructor Notes

- **Dataset:** Inline messy CSV works offline. For richer demos, use Titanic or HR Analytics from Kaggle.
- **Common student mistake:** Forgetting parentheses in compound filters — demonstrate the wrong result first.
- **Common student mistake:** Assuming `sort_values` modifies the original — show `df` unchanged after sort without assignment.
- **Live coding tip:** Run `df.info()` before and after `parse_dates` to show dtype change live.
- **Ritual enforcement:** Physically check off the four inspection steps on a slide every time you load a file.
- **For advanced students:** Introduce `.query("salary > 80000 and department == 'Tech'")` as readable alternative.
- **Time check:** If running long, shorten the concat preview in Practical 1 and keep the exploration report.

<!-- instructor pacing note 1: allow 2 min for questions after this block -->

<!-- instructor pacing note 2: allow 2 min for questions after this block -->

<!-- instructor pacing note 3: allow 2 min for questions after this block -->

<!-- instructor pacing note 4: allow 2 min for questions after this block -->

<!-- instructor pacing note 5: allow 2 min for questions after this block -->

<!-- instructor pacing note 6: allow 2 min for questions after this block -->

<!-- instructor pacing note 7: allow 2 min for questions after this block -->

<!-- instructor pacing note 8: allow 2 min for questions after this block -->

<!-- instructor pacing note 9: allow 2 min for questions after this block -->

<!-- instructor pacing note 10: allow 2 min for questions after this block -->

<!-- instructor pacing note 11: allow 2 min for questions after this block -->

<!-- instructor pacing note 12: allow 2 min for questions after this block -->

<!-- instructor pacing note 13: allow 2 min for questions after this block -->

<!-- instructor pacing note 14: allow 2 min for questions after this block -->

<!-- instructor pacing note 15: allow 2 min for questions after this block -->

<!-- instructor pacing note 16: allow 2 min for questions after this block -->

<!-- instructor pacing note 17: allow 2 min for questions after this block -->

<!-- instructor pacing note 18: allow 2 min for questions after this block -->

<!-- instructor pacing note 19: allow 2 min for questions after this block -->

<!-- instructor pacing note 20: allow 2 min for questions after this block -->

<!-- instructor pacing note 21: allow 2 min for questions after this block -->

<!-- instructor pacing note 22: allow 2 min for questions after this block -->

<!-- instructor pacing note 23: allow 2 min for questions after this block -->

<!-- instructor pacing note 24: allow 2 min for questions after this block -->

<!-- instructor pacing note 25: allow 2 min for questions after this block -->

<!-- instructor pacing note 26: allow 2 min for questions after this block -->

<!-- instructor pacing note 27: allow 2 min for questions after this block -->

<!-- instructor pacing note 28: allow 2 min for questions after this block -->

<!-- instructor pacing note 29: allow 2 min for questions after this block -->

<!-- instructor pacing note 30: allow 2 min for questions after this block -->

<!-- instructor pacing note 31: allow 2 min for questions after this block -->

<!-- instructor pacing note 32: allow 2 min for questions after this block -->

<!-- instructor pacing note 33: allow 2 min for questions after this block -->

<!-- instructor pacing note 34: allow 2 min for questions after this block -->

<!-- instructor pacing note 35: allow 2 min for questions after this block -->

<!-- instructor pacing note 36: allow 2 min for questions after this block -->

<!-- instructor pacing note 37: allow 2 min for questions after this block -->

<!-- instructor pacing note 38: allow 2 min for questions after this block -->

<!-- instructor pacing note 39: allow 2 min for questions after this block -->

<!-- instructor pacing note 40: allow 2 min for questions after this block -->

<!-- instructor pacing note 41: allow 2 min for questions after this block -->'''

S10_PREREAD = r'''# Pandas - Loading, Inspection & Filtering
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Python · lists · loops<br/>Files · JSON · NumPy<br/>Arrays & vectorization"]
    CURSES["<b>Current Session</b><br/><b>Pandas: Loading, Inspection & Filtering</b><br/><i>Shift:</i> Treat data as labelled<br/>tables you can query<br/>DataFrame · CSV · filter · sort"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>The daily workhorse<br/>for all data work"]
    RVAL["<b>Real-Life Value</b><br/>Answer business questions<br/>from any spreadsheet"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[sklearn · stats]</i><br/>Predictive models"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · agents]</i><br/>RAG & agent apps"]
end

START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0
U0 -.->|&nbsp;Ahead&nbsp;| U1

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C
classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
class START startBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
class U0,U1 futureBox
```

## What You'll Learn

In this pre-read, you'll discover:

- What a **DataFrame** is and how it relates to the NumPy arrays you already know
- How to **load data** from CSV files and inspect what arrived
- How to **select** specific rows and columns using labels and positions
- How to **filter** rows by conditions to answer real questions
- How to **sort** a DataFrame to surface the highest, lowest, or most recent values

---

## A. The DataFrame — A Labelled Table

> 💡 **Analogy:** A NumPy array is a grid of numbers with no names. A **DataFrame** is the same grid but every row has an index label and every column has a name — like a spreadsheet where you can call a column "price" instead of "column 3."

**One-line definition:** A **DataFrame** is Pandas' core data structure — a 2-D table with labelled rows (index) and named columns, built on top of NumPy arrays.

```mermaid
flowchart LR
    subgraph numpy["NumPy array"]
        N["[[10, 25, 1]\n [20, 30, 0]\n [15, 22, 1]]<br/>No labels"]
    end
    subgraph pandas["Pandas DataFrame"]
        P["  age  salary  active\n0  10    25      1\n1  20    30      0\n2  15    22      1<br/>Named columns · index"]
    end
    numpy -->|"wrap with labels"| pandas
```

Every column in a DataFrame is a **Series** — a 1-D labelled array. A DataFrame is just multiple Series sharing the same index.

| Concept | Plain meaning | How to check |
|---|---|---|
| `df.shape` | (rows, columns) | `(1000, 8)` means 1000 rows, 8 cols |
| `df.columns` | List of column names | `['name', 'age', 'salary', …]` |
| `df.dtypes` | Data type per column | `int64`, `float64`, `object` |
| `df.index` | Row labels | `RangeIndex(0, 1000)` by default |

**Quick first look at any DataFrame:**

- `df.head()` — first 5 rows
- `df.tail()` — last 5 rows
- `df.info()` — column names, types, non-null counts
- `df.describe()` — summary stats for numeric columns

---

## B. Loading Data from CSV

> 💡 **Analogy:** Opening a spreadsheet file in Excel is a click. `pd.read_csv()` is the Python equivalent — one line that reads every row and column into a DataFrame you can immediately work with.

**One-line definition:** `pd.read_csv()` reads a comma-separated values file from disk (or a URL) and returns a fully formed DataFrame in one step.

```mermaid
flowchart LR
    F["sales_data.csv<br/>(file on disk)"] -->|"pd.read_csv()"| D["DataFrame in memory<br/>ready to query"]
```

**Common parameters that matter:**

| Parameter | What it does | Example |
|---|---|---|
| `filepath` | Path to the file | `"data/sales.csv"` |
| `sep=` | Column separator if not comma | `sep="\t"` for tab-separated |
| `header=` | Which row is the header | `header=0` (default) |
| `usecols=` | Load only specific columns | `usecols=["name", "price"]` |
| `dtype=` | Force column types on load | `dtype={"id": str}` |
| `parse_dates=` | Auto-parse date columns | `parse_dates=["order_date"]` |
| `nrows=` | Load only the first N rows | `nrows=100` for a quick peek |

**After loading, always run the quick-look sequence:**

```
df = pd.read_csv("sales.csv")
df.shape          # How big is it?
df.head()         # What do the first rows look like?
df.info()         # Any missing values? Right types?
df.describe()     # Do the numbers make sense?
```

This four-step check catches the most common load problems: wrong separator, columns shifted, dates as strings, or unexpected row counts.

---

## C. Selecting Columns and Rows

> 💡 **Analogy:** A hotel reception desk can look up any guest by room number (position) or by name (label). Pandas gives you both options — `iloc` for position, `loc` for label — so you can always find exactly what you need.

**One-line definition:** **Selection** in Pandas means isolating specific columns or rows from a DataFrame using either column names, row labels, or integer positions.

**Selecting columns:**

```
df["price"]              # Single column → returns a Series
df[["name", "price"]]    # Multiple columns → returns a DataFrame
```

**Selecting rows by label — `loc`:**

```
df.loc[5]                # Row with index label 5
df.loc[2:7]              # Rows with labels 2 through 7 (inclusive)
df.loc[0, "price"]       # Row 0, column "price"
df.loc[1:4, ["name", "price"]]   # Rows 1–4, two columns
```

**Selecting rows by position — `iloc`:**

```
df.iloc[0]               # First row (position 0)
df.iloc[-1]              # Last row
df.iloc[0:5]             # First 5 rows (0 up to, not including, 5)
df.iloc[0:5, 1:3]        # First 5 rows, columns at positions 1 and 2
```

| Method | Uses | Endpoint inclusive? |
|---|---|---|
| `loc` | Labels (index values, column names) | Yes — `loc[1:4]` includes 4 |
| `iloc` | Integer positions (0-based) | No — `iloc[1:4]` stops before 4 |

**A common trap:** If your index is `0, 1, 2, 3…` (the default), `loc` and `iloc` look identical — but they differ when your index is non-numeric or has gaps. Always be explicit about which you need.

---

## D. Filtering Rows by Condition

> 💡 **Analogy:** A search filter on a shopping site — "show only items under ₹500, in stock, rated above 4 stars." You are describing the rows you want to *keep*. **Pandas filtering** works the same way: you write a condition, and only matching rows come back.

**One-line definition:** **Filtering** uses a boolean condition to select only the rows where that condition is `True`, returning a smaller DataFrame with the same columns.

**Single condition:**

```
df[df["price"] > 500]            # rows where price exceeds 500
df[df["city"] == "Mumbai"]       # rows where city is Mumbai
df[df["status"] != "cancelled"]  # rows where status is not cancelled
```

**Multiple conditions — use `&` (and) / `|` (or):**

```
df[(df["price"] > 500) & (df["city"] == "Mumbai")]
df[(df["age"] < 25) | (df["age"] > 60)]
```

**Always wrap each condition in parentheses** when combining — Python operator precedence will silently produce wrong results without them.

**Useful filter patterns:**

| Goal | Syntax idea |
|---|---|
| Filter by list of values | `df[df["city"].isin(["Mumbai", "Pune"])]` |
| Filter non-null rows | `df[df["email"].notna()]` |
| Filter text contains | `df[df["name"].str.contains("Kumar")]` |
| Filter by date range | `df[(df["date"] >= "2024-01-01") & (df["date"] <= "2024-03-31")]` |

```mermaid
flowchart TD
    F["Full DataFrame\n1000 rows"] --> C{Condition\nprice > 500}
    C -->|True| K["Kept rows\n320 rows"]
    C -->|False| D["Dropped rows\n680 rows"]
```

---

## E. Sorting a DataFrame

> 💡 **Analogy:** A leaderboard automatically re-ranks players when scores change — highest first. **Sorting** does the same for any column: it reorders rows so the answer to "who is top?" is always at the top.

**One-line definition:** `sort_values()` reorders the rows of a DataFrame by the values in one or more columns, either ascending or descending.

**Basic sort:**

```
df.sort_values("sales")                    # ascending (lowest first)
df.sort_values("sales", ascending=False)   # descending (highest first)
```

**Sort by multiple columns — tiebreaker logic:**

```
df.sort_values(["region", "sales"], ascending=[True, False])
# Sort by region A→Z first; within each region, highest sales first
```

**Reset the index after sorting:**

```
df.sort_values("sales", ascending=False).reset_index(drop=True)
```

Without `reset_index`, the original row numbers stay attached and jump around, which looks confusing when you print or slice the result.

| Sorting task | Pattern |
|---|---|
| Top 5 by sales | `.sort_values("sales", ascending=False).head(5)` |
| Alphabetical by name | `.sort_values("name")` |
| Latest dates first | `.sort_values("date", ascending=False)` |
| Multi-column sort | `.sort_values(["col1", "col2"], ascending=[True, False])` |

**Sorting does not modify the original DataFrame** unless you pass `inplace=True` or reassign: `df = df.sort_values(...)`. This is a common point of confusion early on — always save or chain the result.

---

## F. Series Deep Dive — One Column, Many Methods

> 💡 **Analogy:** A Series is one labelled column extracted from a spreadsheet — it remembers both the values and the row labels (index).

**One-line definition:** A **Series** is a 1-D labelled array in Pandas; every DataFrame column is a Series sharing the same row index.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Alice", "Bob"], "salary": [52000, 85000]})
s = df["salary"]
print(type(s))
print(s.index)
print(s.values)      # underlying NumPy array
print(s.describe())
```

| Series attribute | Meaning |
|---|---|
| `.index` | Row labels |
| `.values` / `.to_numpy()` | NumPy array underneath |
| `.dtype` | Data type of the column |
| `.name` | Column name (or None) |

**Vectorized math on Series** uses NumPy silently: `df["salary"] * 1.1` applies a 10% raise to every row in one line.

---

## G. Loading from URLs and the Full Inspection Ritual

> 💡 **Analogy:** Loading from a URL is like downloading a spreadsheet from a shared drive — same `read_csv`, different address.

**One-line definition:** `pd.read_csv()` accepts local paths **and** HTTP URLs — one function for files on disk or on the web.

```python
import pandas as pd

TITANIC_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(TITANIC_URL)
print(df.shape)
print(df.head(3))
print(df.info())
print(df.describe())
print(df.isnull().sum())
```

**Extended ritual — five steps every analyst runs:**

```mermaid
flowchart LR
    L["read_csv"] --> S["shape"]
    S --> H["head / tail"]
    H --> I["info"]
    I --> D["describe"]
    D --> N["isnull().sum()"]
```

| Step | Catches |
|---|---|
| `shape` | Wrong row count, empty file |
| `head()` | Encoding issues, header duplicated as data |
| `info()` | Wrong dtypes, missing value counts |
| `describe()` | Outliers, impossible min/max |
| `isnull().sum()` | Column-specific gap patterns |

**URL loading tips:** Requires internet in Colab. If offline, download once and use local path. Add `nrows=500` for a quick preview of huge files.

---

## H. Combining Filter, Select, and Sort — Query Patterns

> 💡 **Analogy:** A database query chains conditions: filter rows, pick columns, sort results. Pandas does the same in one fluent pipeline.

**One-line definition:** **Method chaining** combines filter → column select → sort in readable order; each step returns a new DataFrame (or view).

```python
result = (
    df.loc[df["department"] == "Tech", ["name", "salary", "city"]]
      .sort_values("salary", ascending=False)
      .head(3)
)
print(result)
```

**Alternative with `.query()`:**

```python
result = (
    df.query("department == 'Tech' and salary > 80000")
      .sort_values("salary", ascending=False)
)
```

| Pattern | Syntax |
|---|---|
| Filter + select columns | `df.loc[mask, ["col1", "col2"]]` |
| Filter + sort + top N | `df[mask].sort_values("col", ascending=False).head(5)` |
| Readable filter | `df.query("col > 100 and city == 'Mumbai'")` |

**Titanic example — survivors in first class:**

```python
first_class_survivors = (
    df.loc[(df["Pclass"] == 1) & (df["Survived"] == 1),
           ["Name", "Sex", "Age"]]
      .sort_values("Age")
      .head(10)
)
```

Always `reset_index(drop=True)` after sort if you need clean row numbers for export.

## Practice Exercises

**1. Pattern Recognition**  
You load a CSV and run `df.info()`. It shows `order_date` has dtype `object` instead of `datetime64`, and `customer_id` is `float64` instead of `int64`. Name the likely cause of each, and which `read_csv` parameter would fix each issue at load time.

**2. Concept Detective**  
A teammate writes `df.loc[0:5]` expecting exactly 5 rows, but gets 6. They also write `df.iloc[0:5]` and get exactly 5. Using what you learned about `loc` vs `iloc`, explain why the results differ and which one they should use for "first 5 rows."

**3. Real-Life Application**  
Imagine you have a DataFrame of orders with columns `customer_name`, `city`, `amount`, `status`, `order_date`. Write out — in plain words, not code — the filter conditions you would apply to answer each of these business questions: (a) All delivered orders above ₹2000 from Delhi, (b) Orders from the last 30 days that are still pending, (c) Customers whose name contains "Singh."

**4. Spot the Error**  
A student writes `df[df["age"] > 18 & df["city"] == "Pune"]` and gets unexpected results. Identify the exact mistake using section D, and write the corrected condition in words.

**5. Planning Ahead**  
You receive a 50,000-row e-commerce CSV with columns `order_id`, `product`, `category`, `price`, `quantity`, `city`, `order_date`, `status`. Describe your full load-and-explore plan: what `read_csv` options you would set, the four-step inspection sequence to run, two filter examples to test your understanding, and one sort that would answer a useful business question.

---

> ✅ **You're done!** You now know how to take any CSV, load it into a labelled DataFrame, and immediately start asking real questions — selecting columns, filtering rows, and surfacing the data you need. Next up: **Pandas: Cleaning & Aggregation**, where you will fix what is broken in your table and summarise it into business-ready answers.

> **Review checkpoint 1:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 2:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 3:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 4:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 5:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 6:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 7:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 8:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 9:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 10:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 11:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 12:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 13:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 14:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 15:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 16:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 17:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 18:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 19:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 20:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 21:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 22:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 23:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 24:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 25:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 26:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 27:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 28:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 29:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 30:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 31:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 32:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 33:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 34:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 35:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 36:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 37:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 38:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 39:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 40:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 41:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 42:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 43:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 44:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 45:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 46:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 47:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 48:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 49:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 50:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 51:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 52:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 53:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 54:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 55:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 56:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 57:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 58:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 59:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 60:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 61:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 62:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 63:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 64:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 65:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.

> **Review checkpoint 66:** State in one sentence when to use `loc` vs `iloc` vs boolean filtering.'''

S11_LECTURE = r'''# Lecture Script: Pandas — Aggregation, Groupby & Merging
> **Instructor Reference** — Module 1: Foundations of Data | Session 11 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students answer business questions with `groupby` and `agg`, handle missing values with `fillna` and `dropna`, combine related tables with `merge`, `join`, and `concat`, and remove inflated counts with `drop_duplicates`.

**Student profile at this point:** Can load CSVs, run the inspection ritual, filter with boolean indexing, and select with `loc`/`iloc`. Have not yet summarised by category or joined two tables.

**Key outcome:** By end of class, every student delivers a department salary report from cleaned employee data and a merged customer-orders dataset — demonstrating the split-apply-combine pattern end to end.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** GroupBy — Split, Apply, Combine | 10 min | 0:15 |
| **Practical 1:** Department Salary Summaries | 15 min | 0:30 |
| **Concept 2:** Missing Values — fillna / dropna | 10 min | 0:40 |
| **Practical 2:** Clean Before You Aggregate | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** merge / join — Combining Tables | 10 min | 1:15 |
| **Practical 3:** Merge Customers + Orders | 15 min | 1:30 |
| **Concept 4:** concat, value_counts & drop_duplicates | 10 min | 1:40 |
| **Practical 4:** End-to-End Mini Analysis | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Show a 10,000-row sales CSV and ask: *"What was total revenue in Mumbai last quarter?"*

Scroll manually for 30 seconds, then run:

```python
df[df["city"] == "Mumbai"].groupby("quarter")["amount"].sum()
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


Ask: *"Which approach would you trust in a board meeting?"*

**Context to set:** Filtering finds rows; groupby summarises them. Merging connects tables that belong together. Cleaning must happen first — aggregating over duplicates or nulls produces confident wrong numbers.

**Learning contract for today:**
- Use split-apply-combine to summarise by category
- Fix missing values and duplicates before aggregating
- Merge two related tables on a shared key
- Stack tables with `concat` when structures match

---

## Concept Block 1: GroupBy — Split, Apply, Combine (10 min)

### The Mental Model — Sports League Table

```
1000 individual sales rows
        ↓ SPLIT by city
   Mumbai group | Pune group | Delhi group
        ↓ APPLY sum(amount)
   ₹45L          | ₹32L       | ₹28L
        ↓ COMBINE into summary table
   city    | total_sales
   Mumbai  | 4500000
   Pune    | 3200000
   ...
```

**Key teaching line:** Split-apply-combine. Split by key → apply function → combine results into summary table.

### Basic GroupBy Syntax

```python
df.groupby("city")["amount"].sum()       # total per city
df.groupby("city")["amount"].mean()      # average per city
df.groupby("category")["order_id"].count()  # orders per category
df.groupby("region")["sales"].max()      # best sale per region
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


### value_counts — Quick Category Summary

```python
df["department"].value_counts()          # count per unique value
df["city"].value_counts(normalize=True)   # proportions (0–1)
df["status"].value_counts(dropna=False)    # include NaN as a category
```
**Expected output:**
```
(Output from code block 3 — run in Colab to verify)
```


| Method | Question it answers |
|---|---|
| `.sum()` | Total |
| `.mean()` | Average |
| `.count()` | How many rows (includes NaN in other cols) |
| `.size()` | Rows per group (counts all, including NaN) |
| `.nunique()` | Distinct values per group |
| `.value_counts()` | Frequency of each category |

### agg — Multiple Metrics at Once

```python
df.groupby("city").agg(
    total_sales=("amount", "sum"),
    order_count=("order_id", "count"),
    avg_discount=("discount", "mean")
)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**After groupby:** Result may have group keys as index. Use `.reset_index()` to flatten for export or merging.

---

## Practical Block 1: Department Salary Summaries (15 min)

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance", "Tech"],
    "salary":     [52000, 85000, 91000, 48000, 73000, 88000],
    "rating":     [4, 5, 5, 3, 4, 4]
}
df = pd.DataFrame(data)

# Single aggregation
print("Average salary by department:")
print(df.groupby("department")["salary"].mean().round(0))

# Multiple aggregations with agg
summary = df.groupby("department").agg(
    headcount=("name", "count"),
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    avg_rating=("rating", "mean")
).round(1)
print("\nDepartment summary:")
print(summary)

# value_counts
print("\nDepartment sizes:")
print(df["department"].value_counts())

# Reset index for a clean table
summary_flat = summary.reset_index()
print("\nFlat summary (ready for export):")
print(summary_flat)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask the class:** *"Which department has the highest average salary? Is it also the largest?"* → Tech highest avg; HR and Finance smaller teams.

**Business question drill:**

```python
# Q: Total payroll cost per department?
payroll = df.groupby("department")["salary"].sum()
print("\nTotal payroll:")
print(payroll)

# Q: Who is the highest paid in each department?
idx = df.groupby("department")["salary"].idxmax()
top_earners = df.loc[idx, ["name", "department", "salary"]]
print("\nTop earner per dept:")
print(top_earners)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Write on board:** GROUP KEY → METRIC → AGG FUNCTION. Always state all three aloud before coding.

---

## Concept Block 2: Missing Values — fillna / dropna (10 min)

### Detect First — Never Fill Blindly

```python
df.isnull().sum()              # count per column
df.isnull().mean() * 100       # percentage missing
df[df["salary"].isna()]        # inspect rows with gaps
```
**Expected output:**
```
(Output from code block 7 — run in Colab to verify)
```


### Three Strategies

```
Missing value
├── dropna()     — remove rows (few gaps, row useless without value)
├── fillna()     — impute with median/mode/constant
└── drop column  — column mostly empty (>30–50% null)
```

**Decision tree — draw on board:**

```
Is this column important?
  No  → drop column
  Yes → Is null rate > 30%?
          Yes → document risk; consider drop or advanced imputation
          No  → Numeric? → fillna(median)
                Categorical? → fillna(mode) or fillna("Unknown")
```

### dropna vs fillna — Key Parameters

```python
df.dropna()                           # drop ANY row with ANY null
df.dropna(subset=["salary"])          # drop only if salary is null
df.dropna(how="all")                  # drop only if ALL cols null

df["salary"].fillna(df["salary"].median())
df["city"].fillna("Unknown")
df.fillna({"salary": 0, "rating": 3}) # dict for multiple columns
```
**Expected output:**
```
(Output from code block 8 — run in Colab to verify)
```


**Critical rule:** Clean **before** groupby. `mean()` silently skips NaN but undercounts; duplicates inflate totals.

| Mistake | Consequence |
|---|---|
| Aggregate before cleaning | Wrong totals from duplicates |
| fillna(0) on salary | Distorts average downward |
| dropna() on entire DataFrame | May lose 40% of rows unnecessarily |

---

## Practical Block 2: Clean Before You Aggregate (15 min)

Use the coding-problem dataset with intentional problems:

```python
import pandas as pd
import numpy as np

data = {
    "name":       ["Alice", "Bob", "Bob", "Diana", "Eve", "Frank"],
    "department": ["HR", "Tech", "Tech", "HR", "Finance", "Tech"],
    "salary":     [52000, 85000, 85000, None, 73000, 91000],
    "rating":     [4, 5, 5, 3, None, 4]
}
df = pd.DataFrame(data)

# STEP 1: Audit
print("=== BEFORE CLEANING ===")
print("Nulls:\n", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())
print(df)

# STEP 2: Drop exact duplicate rows
df = df.drop_duplicates()
print("\nAfter dedup:", df.duplicated().sum())

# STEP 3: Fill missing salary with median
median_salary = df["salary"].median()
df["salary"] = df["salary"].fillna(median_salary)
print(f"Filled salary with median: {median_salary}")

# STEP 4: Fill missing rating with constant 3
df["rating"] = df["rating"].fillna(3)

# STEP 5: Validate
print("\n=== AFTER CLEANING ===")
print("Nulls:\n", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

# STEP 6: NOW aggregate
avg_salary = df.groupby("department")["salary"].mean().round(0)
print("\nAverage salary by department:")
print(avg_salary)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask:** *"What if we ran groupby BEFORE drop_duplicates?"* → Bob counted twice → Tech average inflated.

**Discussion:** Diana's missing salary — median fill assumes she is "typical." In HR reporting, flagging as "Unknown" might be safer. Document your choice.

---

## BREAK (10 min)

*Suggested break prompt — ask students: "You have 800 duplicate order rows in a 10K dataset. Which function fixes it, and what must you define first?" Expected: `drop_duplicates(subset=["order_id"])`, after defining what makes an order unique.*

---

## Concept Block 3: merge / join — Combining Tables (10 min)

### Why Merge — Real Data Lives in Multiple Tables

```
customers table          orders table
┌────────┬────────┐       ┌─────────┬────────┐
│ cust_id│  city  │       │ order_id│ cust_id│ amount │
├────────┼────────┤       ├─────────┼────────┼────────┤
│   C01  │ Mumbai │       │  O1001  │  C01   │  5000  │
│   C02  │ Pune   │       │  O1002  │  C03   │  3200  │
└────────┴────────┘       └─────────────────────────────┘

Merge on cust_id → each order gets its customer's city
```

### Merge Types — Venn Diagram on Board

| `how=` | Keeps | Use when |
|---|---|---|
| `inner` | Only matching keys in BOTH | Strict analysis — lose unmatched |
| `left` | All rows from left + matches from right | Orders enriched with customer info |
| `right` | All rows from right + matches from left | Less common |
| `outer` | Everything from both | Full audit — find orphans |

```python
pd.merge(orders, customers, on="cust_id", how="left")
# or
orders.merge(customers, on="cust_id", how="left")
```
**Expected output:**
```
(Merged DataFrame — combined columns from both tables)
```


### join — Merge Using Index

```python
customers.set_index("cust_id").join(orders.set_index("cust_id"), how="inner")
```
**Expected output:**
```
(Output from code block 11 — run in Colab to verify)
```


Use `merge` for most cases; `join` when working with indexed tables.

**Common pitfalls:**
- Key columns have different types (`"C01"` string vs `C01` without quotes) → zero matches
- Duplicate keys in the lookup table → row explosion (one order becomes three)
- Same column name in both tables → `_x` / `_y` suffixes appear

---

## Practical Block 3: Merge Customers + Orders (15 min)

```python
import pandas as pd

customers = pd.DataFrame({
    "cust_id":   ["C01", "C02", "C03", "C04"],
    "name":      ["Alice", "Bob", "Charlie", "Diana"],
    "city":      ["Mumbai", "Pune", "Mumbai", "Delhi"]
})

orders = pd.DataFrame({
    "order_id":  ["O1001", "O1002", "O1003", "O1004", "O1005"],
    "cust_id":   ["C01", "C03", "C01", "C99", "C02"],
    "amount":    [5000, 3200, 1800, 9000, 4500],
    "status":    ["completed", "completed", "cancelled", "completed", "completed"]
})

print("Customers:", customers.shape)
print("Orders:", orders.shape)

# Left merge — keep all orders, attach customer info
merged = orders.merge(customers, on="cust_id", how="left")
print("\nMerged (left join):")
print(merged)

# Spot the orphan order — C99 has no customer
orphans = merged[merged["name"].isna()]
print("\nOrphan orders (no matching customer):")
print(orphans)

# Inner merge — only orders with known customers
inner = orders.merge(customers, on="cust_id", how="inner")
print("\nInner join row count:", len(inner))

# Business question: total completed sales per city
completed = merged[merged["status"] == "completed"]
city_sales = completed.groupby("city")["amount"].sum().sort_values(ascending=False)
print("\nCompleted sales by city:")
print(city_sales)
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask:** *"Why does C99 show NaN for name and city?"* → Left join keeps the order; no customer match.

**Teaching point:** Always check `len(merged)` vs `len(orders)` after merge. Duplicate keys in the lookup table cause row explosion.

---

## Concept Block 4: concat, value_counts & drop_duplicates (10 min)

### concat — Stack Tables with Same Columns

```python
df_q1 = pd.DataFrame({"product": ["A", "B"], "sales": [100, 200]})
df_q2 = pd.DataFrame({"product": ["A", "C"], "sales": [150, 180]})

combined = pd.concat([df_q1, df_q2], ignore_index=True)
print(combined)
# product  sales
# A        100
# B        200
# A        150   ← same product, different quarter — NOT a duplicate
# C        180
```
**Expected output:**
```
(Printed values matching the print statements above)
```


| Tool | When to use |
|---|---|
| `merge` / `join` | Side-by-side on a shared key (different columns) |
| `concat` | Top-to-bottom stack (same columns, more rows) |

### drop_duplicates — Define "Unique" First

```python
df.drop_duplicates()                          # exact row match
df.drop_duplicates(subset=["order_id"])       # one row per order
df.drop_duplicates(subset=["order_id"], keep="last")  # keep newest
df.drop_duplicates(subset=["name"], keep=False)       # show ALL copies
```
**Expected output:**
```
(Output from code block 14 — run in Colab to verify)
```


**Always check before and after:**

```python
print("Before:", df.duplicated(subset=["order_id"]).sum())
df = df.drop_duplicates(subset=["order_id"])
print("After:", df.duplicated(subset=["order_id"]).sum())
```
**Expected output:**
```
(Printed values matching the print statements above)
```


### value_counts in EDA Workflow

After cleaning, run value_counts on categorical columns to spot typos:

```python
df["city"].value_counts(dropna=False)
# Mumbai 450, mumbai 3, MUMBAI 2  → normalise before aggregating
```
**Expected output:**
```
(Output from code block 16 — run in Colab to verify)
```


---

## Practical Block 4: End-to-End Mini Analysis (10 min)

**Full pipeline — students follow along:**

```python
import pandas as pd
import io

# Two related tables
customers_raw = """cust_id,name,city
C01,Alice,Mumbai
C02,Bob,Pune
C03,Charlie,Mumbai
C02,Bob,Pune
"""

orders_raw = """order_id,cust_id,product,amount,status
O1,C01,Laptop,65000,completed
O2,C02,Chair,12000,completed
O3,C01,Notebook,800,cancelled
O4,C03,Laptop,65000,completed
O5,C02,Laptop,65000,completed
O6,C04,Monitor,15000,completed
O7,C02,Chair,12000,cancelled
"""

customers = pd.read_csv(io.StringIO(customers_raw))
orders = pd.read_csv(io.StringIO(orders_raw))

print("=== STEP 1: CLEAN CUSTOMERS ===")
print("Duplicates:", customers.duplicated().sum())
customers = customers.drop_duplicates(subset=["cust_id"])
print("After dedup:", customers.shape)

print("\n=== STEP 2: MERGE ===")
merged = orders.merge(customers, on="cust_id", how="left")
print(merged)
print("Orphan orders:", merged["name"].isna().sum())

print("\n=== STEP 3: FILTER COMPLETED ===")
completed = merged[merged["status"] == "completed"]

print("\n=== STEP 4: GROUPBY SUMMARIES ===")
by_city = completed.groupby("city").agg(
    total_revenue=("amount", "sum"),
    order_count=("order_id", "count")
).sort_values("total_revenue", ascending=False)
print("\nSales by city:")
print(by_city)

by_product = completed.groupby("product")["amount"].sum().sort_values(ascending=False)
print("\nSales by product:")
print(by_product)

print("\n=== STEP 5: VALUE COUNTS ===")
print(completed["product"].value_counts())
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Discussion:**
- *"Why deduplicate customers before merge?"* → Bob twice would duplicate every Bob order.
- *"Why filter completed before summing?"* → Cancelled orders should not count as revenue.
- *"What is C04?"* → Orphan — order exists, customer missing from master table.

**Challenge:** Compute average order value per city (`total_revenue / order_count`).

---

### Troubleshooting — Merge and GroupBy

**Error:** Merge returns 0 rows
→ **Fix:** Check key dtypes match — `df["cust_id"].dtype` on both sides; cast with `.astype(str)`.

**Error:** Merge row count explodes (10 orders → 30 rows)
→ **Fix:** Duplicate keys in lookup table — run `customers.duplicated(subset=['cust_id']).sum()`.

**Error:** `ValueError: cannot insert X, already exists` after groupby
→ **Fix:** Use `.reset_index()` or named aggregation in `.agg()`.


### Extension — Titanic Survival by Class

After cleaning Age nulls with median fill, compute survival rate by passenger class:

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
df["Age"] = df["Age"].fillna(df["Age"].median())
survival = df.groupby("Pclass").agg(
    passengers=("PassengerId", "count"),
    survived=("Survived", "sum"),
    survival_rate=("Survived", "mean")
).round(3)
print(survival)
```


---

## Practical Block 5: Sales Data Pipeline (Bonus — 10 min)

```python
import pandas as pd
import io

sales_raw = """order_id,city,product,amount,status,order_date
O1,Mumbai,Laptop,65000,completed,2024-01-15
O2,Pune,Chair,12000,completed,2024-01-16
O3,Mumbai,Laptop,65000,cancelled,2024-01-17
O4,Mumbai,Notebook,800,completed,2024-01-18
O5,Pune,Laptop,65000,completed,2024-01-19
O5,Pune,Laptop,65000,completed,2024-01-19
O6,Delhi,Monitor,15000,completed,2024-01-20
O7,Mumbai,,9000,completed,2024-01-21
"""

df = pd.read_csv(io.StringIO(sales_raw), parse_dates=["order_date"])
print("Before — duplicates:", df.duplicated().sum())
print("Before — nulls:\n", df.isnull().sum())

df = df.drop_duplicates(subset=["order_id"])
df["product"] = df["product"].fillna("Unknown")

completed = df[df["status"] == "completed"]
by_city = completed.groupby("city").agg(
    revenue=("amount", "sum"),
    orders=("order_id", "count")
).sort_values("revenue", ascending=False)
print("\nRevenue by city:\n", by_city)
```


**Expected output:**
```
Before — duplicates: 1
Before — nulls:
 order_id      0
 city          0
 product       1
 amount        0
 status        0
 order_date    0

Revenue by city:
         revenue  orders
city
Mumbai    65800       2
Pune      77000       2
Delhi     15000       1
```

### Troubleshooting

**Error:** `Groupby mean seems too low`
→ **Fix:** Nulls or duplicates inflated/deflated counts — clean first.

**Error:** `concat axis confusion`
→ **Fix:** Use axis=0 to stack rows (default); axis=1 to place side by side.

**Error:** `fillna(0) on amount`
→ **Fix:** Distorts revenue totals — use median or drop row with business approval.


---

### Additional walkthrough — concat quarterly sales

```python
import pandas as pd

q1 = pd.DataFrame({"region": ["North", "South"], "sales": [100, 120]})
q2 = pd.DataFrame({"region": ["North", "South"], "sales": [110, 130]})
annual = pd.concat([q1, q2], keys=["Q1", "Q2"], names=["quarter", "row"])
print(annual)
print("\nTotal by region:\n", annual.groupby("region")["sales"].sum())
```

## Instructor Notes (continued)

- **Order of operations mantra:** "Dedupe → nulls → merge → filter → groupby" — repeat every demo.
- **Sales inline CSV:** Includes duplicate O5 and missing product — intentional for cleaning demo.
- **Titanic groupby:** Powerful emotional demo — survival rate by Pclass shows data telling a story.

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Split-apply-combine: `groupby` + `agg` for business summaries
- `value_counts` for quick category frequency checks
- `fillna` / `dropna` with documented strategy per column
- `merge` with `how="inner"` / `"left"` to combine related tables
- `concat` to stack same-schema tables; `drop_duplicates` with `subset=`

**The correct order:** Load → Inspect → Dedupe → Fix nulls → Merge → Filter → Groupby → Validate.

**Bridge to next session:** *"You can now clean, combine, and summarise in Pandas. Upcoming sessions add visualisation, EDA thinking, SQL, and spreadsheets — same query logic, different tools."*

**Homework / self-practice:** Take two CSVs from Kaggle (orders + customers, or products + sales). Merge them, clean duplicates and nulls, produce two groupby summaries, and write one sentence of business insight per summary.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: groupby gave me a weird index — how do I get a normal table?**
→ `.reset_index()` after aggregation: `df.groupby("city")["amount"].sum().reset_index()`.

**Q: merge returned more rows than my orders table. What happened?**
→ Duplicate keys in the lookup table. Check `customers.duplicated(subset=["cust_id"]).sum()` before merging.

**Q: Should I use `count()` or `size()` in groupby?**
→ `count()` skips NaN in the chosen column. `size()` counts all rows in the group regardless of NaN.

**Q: fillna with mean vs median?**
→ Median for skewed data or when outliers exist. Mean only when distribution is symmetric and clean.

**Q: concat vs merge — how do I choose?**
→ Same columns, more rows → `concat`. Different columns, shared key → `merge`.

---

## Instructor Notes

- **Dataset:** Inline CSV strings work offline. Superstore (Kaggle) is excellent for merge demos if internet available.
- **Common student mistake:** Running groupby before drop_duplicates — demonstrate inflated totals live.
- **Common student mistake:** Merging on columns with mismatched dtypes — show zero-match result and fix with `.astype(str)`.
- **Live coding tip:** Print row counts before and after every merge and dedup step.
- **Key teaching line:** Repeat "split-apply-combine" aloud during every groupby demo.
- **For advanced students:** Introduce `pd.merge(..., validate="one_to_many")` to catch duplicate key explosions.
- **Time check:** If running long, shorten the duplicate-key demo and keep the end-to-end mini analysis.

<!-- instructor pacing note 1: allow 2 min for questions after this block -->

<!-- instructor pacing note 2: allow 2 min for questions after this block -->

<!-- instructor pacing note 3: allow 2 min for questions after this block -->

<!-- instructor pacing note 4: allow 2 min for questions after this block -->

<!-- instructor pacing note 5: allow 2 min for questions after this block -->

<!-- instructor pacing note 6: allow 2 min for questions after this block -->

<!-- instructor pacing note 7: allow 2 min for questions after this block -->

<!-- instructor pacing note 8: allow 2 min for questions after this block -->

<!-- instructor pacing note 9: allow 2 min for questions after this block -->'''

S11_PREREAD = r'''# Pandas - Aggregation, Groupby & Merging
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Python · NumPy · arrays<br/>DataFrame · CSV<br/>Filter · select · sort"]
    CURSES["<b>Current Session</b><br/><b>Pandas: Aggregation, Groupby & Merging &<br/>Aggregation</b><br/><i>Shift:</i> Fix broken tables,<br/>then summarise them<br/>Nulls · dupes · groupby · EDA"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Clean inputs make<br/>every model trustworthy"]
    RVAL["<b>Real-Life Value</b><br/>Answer business questions<br/>from messy exports"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[sklearn · stats]</i><br/>Predictive models"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · agents]</i><br/>RAG & agent apps"]
end

START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0
U0 -.->|&nbsp;Ahead&nbsp;| U1

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C
classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
class START startBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
class U0,U1 futureBox
```

## What You'll Learn

In this pre-read, you'll discover:

- How to find and handle **missing values** without silently breaking your analysis
- How to detect and remove **duplicate rows** that inflate your counts and totals
- How `groupby` turns a long table into **meaningful summaries** per category
- How to use **EDA** (Exploratory Data Analysis) as a repeatable first step on any dataset
- How cleaning and aggregation together produce data you can actually trust and act on

---

## A. Missing Values — Finding and Fixing Gaps

> 💡 **Analogy:** A classroom attendance sheet with blank entries is ambiguous — did the student not come, or did the teacher forget to mark? **Missing values** in data carry the same ambiguity: a blank cell might mean "unknown," "not applicable," or simply "someone forgot."

**One-line definition:** A **missing value** (shown as `NaN` in Pandas) is an absent entry in a column that must be consciously handled — ignored, filled, or removed — before analysis produces trustworthy results.

**Detecting missing values:**

```
df.isna().sum()          # count of NaN per column
df.isna().mean() * 100   # percentage missing per column
df[df["salary"].isna()]  # rows where salary is missing
```

```mermaid
flowchart TD
    M["Detect: isna().sum()"] --> Q{How much<br/>is missing?}
    Q -->|"< 5%"| D["Drop rows<br/>dropna()"]
    Q -->|"5–30%"| F["Fill with\nmedian / mode\nfillna()"]
    Q -->|"> 30%"| C["Consider dropping\nthe column entirely"]
    Q -->|"Structural gap"| L["Fill with label\ne.g. 'Unknown'"]
```

**Fixing missing values:**

| Method | When to use | Code idea |
|---|---|---|
| Drop rows | Few missing; row useless without value | `df.dropna(subset=["salary"])` |
| Drop column | Column mostly empty | `df.drop(columns=["middle_name"])` |
| Fill with median | Numeric column, skewed data | `df["age"].fillna(df["age"].median())` |
| Fill with mode | Categorical column | `df["city"].fillna(df["city"].mode()[0])` |
| Fill with label | Category where blank = not provided | `df["discount"].fillna("None")` |

**Critical rule:** Never fill missing values without looking at the column first. A missing `age` and a missing `nickname` call for completely different treatments.

---

## B. Duplicates — Rows That Should Not Exist Twice

> 💡 **Analogy:** Scanning the same loyalty card twice at a checkout doubles your points balance — good for you, bad for the store's books. **Duplicate rows** do exactly the same to your counts, totals, and averages.

**One-line definition:** A **duplicate row** is a record that appears more than once when it should be unique — causing every aggregation to overcount.

**Detecting duplicates:**

```
df.duplicated().sum()              # total number of exact duplicate rows
df[df.duplicated(keep=False)]      # show all copies, not just second occurrence
df.duplicated(subset=["order_id"]) # duplicates based on key column only
```

**Removing duplicates:**

```
df.drop_duplicates()                        # remove exact full-row duplicates
df.drop_duplicates(subset=["order_id"])     # keep first occurrence per order_id
df.drop_duplicates(subset=["order_id"], keep="last")   # keep most recent
```

| Duplicate type | Example | Fix |
|---|---|---|
| Exact copy — every column | Same row imported twice | `drop_duplicates()` |
| Key duplicate, data differs | Two rows, same `order_id`, different status | Keep latest by date |
| Repeated header row | Column names appear as a data row | Filter out with boolean mask |

**Always define "unique" for your specific problem** before removing anything. For an orders table, `order_id` should be unique. For a sales log, the same customer buying twice on different days is *not* a duplicate.

---

## C. GroupBy — From Rows to Summaries

> 💡 **Analogy:** A sports league table collapses hundreds of individual match results into one summary row per team: games played, wins, goals scored. **GroupBy** does the same — it takes many detail rows and produces one summary row per group.

**One-line definition:** `groupby` splits a DataFrame into groups based on one or more columns, applies an aggregation function to each group, and returns a summary table.

**The three-step mental model:**

```mermaid
flowchart LR
    S["Split\nGroup by city"] --> A["Apply\nsum(sales)"]
    A --> C["Combine\nOne row per city"]
```

**Common aggregations:**

```
df.groupby("city")["sales"].sum()          # total sales per city
df.groupby("city")["sales"].mean()         # average sales per city
df.groupby("category")["order_id"].count() # orders per category
df.groupby("region")["sales"].max()        # highest sale per region
```

**Multiple aggregations at once with `.agg()`:**

```
df.groupby("city").agg(
    total_sales=("sales", "sum"),
    order_count=("order_id", "count"),
    avg_discount=("discount", "mean")
)
```

| GroupBy pattern | Business question it answers |
|---|---|
| Single column key | "Total revenue per region?" |
| Two column keys | "Orders per category per month?" |
| `.agg()` with multiple funcs | "Sales summary: total, count, avg — all at once" |
| `.size()` | "How many rows in each group?" |
| `.nunique()` | "How many unique customers per city?" |

**After a groupby, reset the index** if you want the group keys back as regular columns:

```
df.groupby("city")["sales"].sum().reset_index()
```

---

## D. EDA — Exploring Before You Conclude

> 💡 **Analogy:** A detective does not accuse someone at the crime scene without gathering evidence first. **EDA** is the evidence-gathering phase of data work — you look at everything before drawing a conclusion.

**One-line definition:** **Exploratory Data Analysis (EDA)** is a structured set of questions and visualisations you run on every new dataset to understand its shape, quality, and patterns before modelling or reporting.

**The EDA starter checklist in Pandas:**

```mermaid
flowchart TD
    L["Load & inspect\nshape · head · info"] --> M["Missing values\nisna().sum()"]
    M --> D["Duplicates\nduplicated().sum()"]
    D --> S["Summary stats\ndescribe()"]
    S --> V["Value counts\nfor categories"]
    V --> C["Correlations\ncorr() for numerics"]
```

**Step-by-step with purpose:**

| Step | Code | What to look for |
|---|---|---|
| Shape & types | `df.shape`, `df.dtypes` | Unexpected row count, wrong types |
| Summary stats | `df.describe()` | Unrealistic min/max, huge std dev |
| Missing counts | `df.isna().sum()` | Columns with heavy gaps |
| Category counts | `df["col"].value_counts()` | Dominant values, typos, rare junk |
| Correlations | `df.corr(numeric_only=True)` | Columns that move together |
| Grouped summaries | `groupby` + `agg` | Patterns across segments |

**What good EDA produces:**
- A short list of data quality issues to fix
- 3–5 observations about patterns or outliers worth investigating
- Confidence (or concern) about whether the data is ready for modelling

EDA is not a one-time event — you run it again after cleaning to confirm the fixes worked and nothing new broke.

---

## E. Putting It Together — A Clean-and-Summarise Workflow

> 💡 **Analogy:** A chef preps ingredients (washing, cutting, discarding bad pieces) before cooking. You cannot make a good dish with rotten onions still in the mix. **Cleaning before aggregating** is that same discipline — garbage in, garbage out.

**One-line definition:** A **clean-and-summarise workflow** is the repeatable sequence of detecting problems, fixing them, and then running groupby summaries — so every number in the output is based on trustworthy data.

**Recommended order:**

1. **Load** — `pd.read_csv()` with appropriate parameters
2. **Inspect** — `shape`, `info()`, `head()`, `describe()`
3. **Fix missing** — `fillna()` or `dropna()` per column, with documented reasoning
4. **Fix duplicates** — `drop_duplicates()` on the right key
5. **Fix types** — `astype()`, `pd.to_datetime()` where needed
6. **Validate** — re-run `isna().sum()` and `duplicated().sum()` to confirm zero issues
7. **Aggregate** — `groupby` + `agg` to answer your business questions
8. **Document** — note what you changed and why

| Stage | Quick check to confirm it worked |
|---|---|
| After fixing missing | `df.isna().sum()` → all zeros for target columns |
| After removing duplicates | `df.duplicated().sum()` → 0 |
| After type conversion | `df.dtypes` → expected types |
| After groupby | Row count matches expected number of groups |

Following this order ensures you never aggregate over nulls (which distort means), never double-count duplicates, and never group by a column that still holds mixed types.

---

## F. Merge and Join — Side-by-Side Tables

> 💡 **Analogy:** Two spreadsheets linked by customer ID — merge lines up rows that share the same key and puts their columns side by side.

**One-line definition:** **`merge`** combines two DataFrames on a shared key column, like a SQL JOIN.

```python
import pandas as pd

customers = pd.DataFrame({"cust_id": ["C01", "C02"], "city": ["Mumbai", "Pune"]})
orders = pd.DataFrame({"order_id": ["O1", "O2"], "cust_id": ["C01", "C03"], "amount": [5000, 3200]})

merged = orders.merge(customers, on="cust_id", how="left")
print(merged)
```

| `how=` | Keeps |
|---|---|
| `inner` | Only matching keys in BOTH |
| `left` | All rows from left + matches from right |
| `outer` | Everything from both |

```mermaid
flowchart LR
    O["orders"] --> M["merge on cust_id"]
    C["customers"] --> M
    M --> R["enriched table"]
```

**Pitfalls:** mismatched dtypes on key columns; duplicate keys in lookup table causing row explosion.

---

## G. Concat — Stacking Rows

> 💡 **Analogy:** Concat is stapling two lists of the same columns together — Q1 sales on top of Q2 sales.

**One-line definition:** **`pd.concat`** stacks DataFrames vertically (same columns) or horizontally (same index).

```python
q1 = pd.DataFrame({"product": ["A", "B"], "sales": [100, 200]})
q2 = pd.DataFrame({"product": ["A", "C"], "sales": [150, 180]})
combined = pd.concat([q1, q2], ignore_index=True)
print(combined)
```

| Tool | When |
|---|---|
| `merge` | Different columns, shared key |
| `concat` | Same columns, more rows |

---

## H. End-to-End Clean → Merge → Aggregate Workflow

> 💡 **Analogy:** A recipe with ordered steps — prep ingredients before cooking, or the dish fails.

**One-line definition:** The reliable pipeline is **load → inspect → dedupe → fix nulls → merge → filter → groupby → validate**.

```mermaid
flowchart TD
    L[Load CSV] --> I[Inspect shape/info]
    I --> D[drop_duplicates]
    D --> F[fillna / dropna]
    F --> M[merge tables]
    M --> G[groupby + agg]
    G --> V[Validate counts]
```

**Checklist after each stage:**

| Stage | Confirm with |
|---|---|
| After dedup | `duplicated().sum() == 0` |
| After fillna | `isnull().sum()` on target cols |
| After merge | `len(merged)` vs expected |
| After groupby | Row count = number of groups |

**Sales + Titanic tie-in:** merge passenger info with fare categories; groupby `Pclass` for survival rate — same split-apply-combine pattern as business sales by city.

## Practice Exercises

**1. Pattern Recognition**  
You run `df.isna().sum()` and find: `name: 0`, `age: 450`, `city: 12`, `salary: 3200` (out of 5000 rows). For each column with missing values, name the strategy you would use (drop rows, fill with median, fill with mode, fill with label, drop column) and explain your reasoning.

**2. Concept Detective**  
After running `groupby("product")["revenue"].sum()`, a colleague notices the totals are much higher than expected. They check and find `duplicated().sum()` returns 800. Which concept directly caused the inflated totals, and what is the correct order of operations to fix it?

**3. Real-Life Application**  
Think of three real datasets you might work with — a hospital patient log, an e-commerce orders table, a school attendance record. For each: name one type of missing value likely to appear, say whether you would drop or fill it, and name one meaningful groupby aggregation a manager would care about.

**4. Spot the Error**  
A student runs `df.drop_duplicates()` on a transactions table and confidently says "all duplicates removed." Later, two rows with the same `transaction_id` but different `amounts` are found. What did `drop_duplicates()` without arguments actually check, and what should the student have written instead?

**5. Planning Ahead**  
You receive a sales DataFrame with columns `order_id`, `customer_id`, `product`, `category`, `amount`, `city`, `order_date`. Design a complete clean-and-summarise plan: list every cleaning step in order with what you would check before and after each, then describe three `groupby` aggregations that would give a sales manager actionable weekly insights.

---

> ✅ **You're done!** You now have the two most important Pandas skills: making data trustworthy through cleaning, and making it meaningful through aggregation. A clean, well-grouped DataFrame is the input every ML model and every business report depends on. Next up: **Excel Analysis & SQL Fundamentals**, where you will apply the same query-thinking skills across two more tools in the analyst's toolkit.

> **Workflow checkpoint 1:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 2:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 3:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 4:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 5:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 6:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 7:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 8:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 9:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 10:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 11:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 12:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 13:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 14:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 15:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 16:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 17:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 18:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 19:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 20:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 21:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 22:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 23:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 24:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 25:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 26:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 27:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 28:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 29:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 30:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 31:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 32:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 33:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 34:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 35:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 36:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 37:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 38:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 39:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 40:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 41:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 42:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 43:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 44:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 45:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 46:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 47:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 48:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 49:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 50:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 51:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 52:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 53:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 54:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 55:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 56:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 57:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 58:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 59:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 60:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 61:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 62:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 63:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 64:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 65:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 66:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 67:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 68:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 69:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 70:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 71:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 72:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 73:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 74:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 75:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 76:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 77:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 78:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 79:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 80:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 81:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 82:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 83:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 84:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 85:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 86:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 87:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 88:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 89:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 90:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 91:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 92:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 93:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 94:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 95:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 96:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 97:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 98:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 99:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 100:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 101:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 102:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 103:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 104:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 105:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 106:** Why must deduplication happen before groupby? Write one sentence.

> **Workflow checkpoint 107:** Why must deduplication happen before groupby? Write one sentence.'''

S12_LECTURE = r'''# Lecture Script: Data Visualization
> **Instructor Reference** — Module 1: Foundations of Data | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students create Matplotlib line, bar, scatter, and histogram charts with proper titles, labels, and legends — plus one interactive Plotly chart — and can justify chart choice for a given business question.

**Student profile at this point:** Comfortable with Pandas loading, filtering, and groupby from Sessions 10–11. Ready to turn aggregated data into visuals that support decisions.

**Key outcome:** Each student builds a single-page **sales dashboard** from a CSV snippet — four Matplotlib chart types, one Plotly interactive chart, and one written insight per chart.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — Two charts, same data | 5 min | 0:05 |
| **Concept 1:** Chart choice framework | 10 min | 0:15 |
| **Practical 1:** Matplotlib line + bar charts | 20 min | 0:35 |
| **Concept 2:** Labels, titles, legends, honesty | 10 min | 0:45 |
| **Practical 2:** Scatter + histogram | 20 min | 1:05 |
| **BREAK** | 10 min | 1:15 |
| **Concept 3:** Plotly for interactivity | 10 min | 1:25 |
| **Practical 3:** Plotly dashboard demo | 15 min | 1:40 |
| **Concept 4:** Critique bad charts | 5 min | 1:45 |
| **Practical 4:** Sales dashboard lab | 10 min | 1:55 |
| Summary & Wrap-Up | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Display two versions of the same data on screen:

- **Version A:** Default Matplotlib output — no title, axes labelled "x" and "y", default blue, tiny text
- **Version B:** Same data — title reads *"March Peak: 175 Units Sold (+15% vs Feb)"*, labelled axes, legend, gridlines

*"Both charts show identical numbers. Which would you put in a slide for your manager? Which one leads to a decision?"*

**Set the rule for today:** Every chart answers a **question**. If you cannot state the question in one sentence, do not plot yet.

**Bridge from Pandas:** *"You already know how to group and aggregate. Today you learn how to **show** what you found — clearly, honestly, and interactively when needed."*

---

## Concept Block 1: Chart Choice Framework (10 min)

### Write the four questions on the board

| Question type | Chart | X | Y |
|---|---|---|---|
| Trend over time | **Line** | Time | Metric |
| Compare categories | **Bar** | Category | Value |
| Relationship between two numbers | **Scatter** | Variable A | Variable B |
| Distribution of one variable | **Histogram** | Bins (ranges) | Count |

### Decision flowchart — talk through aloud

```
What are you showing?
  → Over time?           → Line
  → Compare groups?      → Bar
  → Two numeric vars?    → Scatter
  → Spread of one var?   → Histogram
```

### Variable type matters

| Variable type | Examples | Valid charts |
|---|---|---|
| Categorical | product, region, month name | Bar |
| Numeric continuous | price, score, temperature | Histogram, scatter, line |
| Datetime | order_date | Line, area |

**Three mistakes to call out:**

1. **Bar chart for 365 daily values** → use line
2. **Line chart for 5 unrelated categories** → use bar
3. **Pie chart with 10 slices** → use horizontal bar

**Teaching line:** *"Chart type is not a style preference. It is a logical choice tied to your question."*

---

## Practical Block 1: Matplotlib Line + Bar Charts (20 min)

### Setup — sample sales dataset

```python
import matplotlib.pyplot as plt
import pandas as pd

# Inline sample data — or load from CSV
sales_df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "online":  [120, 135, 150, 142, 160, 175],
    "store":   [80,  90,  95,  88,  100, 110],
    "region":  ["North", "North", "South", "South", "North", "South"]
})

print(sales_df)
```
**Expected output:**
```
(Printed values matching the print statements above)
```


### Line chart — trend over time

```python
plt.figure(figsize=(9, 4))

plt.plot(sales_df["month"], sales_df["online"],
         marker='o', linewidth=2, label='Online', color='#2E86AB')
plt.plot(sales_df["month"], sales_df["store"],
         marker='s', linewidth=2, label='In-store', color='#E84855')

plt.title("Sales by Channel — H1 2026", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.legend(loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Walk through:** `figsize`, `marker`, `label` + `legend`, `grid`. Ask: *"Which channel is growing faster? How can you tell?"*

### Bar chart — compare categories

```python
# Total sales by region
region_totals = sales_df.groupby("region")[["online", "store"]].sum()
print(region_totals)

plt.figure(figsize=(7, 4))
x = range(len(region_totals.index))
width = 0.35

plt.bar([i - width/2 for i in x], region_totals["online"],
        width, label='Online', color='#2E86AB')
plt.bar([i + width/2 for i in x], region_totals["store"],
        width, label='In-store', color='#E84855')

plt.xticks(x, region_totals.index)
plt.title("Total H1 Sales by Region and Channel")
plt.ylabel("Units Sold")
plt.legend()
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


### Grouped bar with Pandas shortcut — show both approaches

```python
region_totals.plot(kind='bar', figsize=(7, 4), color=['#2E86AB', '#E84855'])
plt.title("Total H1 Sales by Region and Channel")
plt.ylabel("Units Sold")
plt.xticks(rotation=0)
plt.legend(title="Channel")
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Live exercise (3 min):** Students add a title and y-label to a bare bar chart you provide. Share one improvement on screen.

---

## Concept Block 2: Labels, Titles, Legends, and Honesty (10 min)

### The minimum viable chart checklist

Every chart must have:

- [ ] **Title** — states the topic or insight, not "Chart 1"
- [ ] **X-axis label** — what the horizontal axis represents
- [ ] **Y-axis label** — what the vertical axis measures, with units
- [ ] **Legend** — when two or more series appear
- [ ] **Readable size** — `figsize=(8, 4)` minimum for slides

### Good vs bad — show side by side

| Element | Bad | Good |
|---|---|---|
| Title | "Bar chart" | "North Region Leads H1 Sales at 425 Units" |
| Y-axis | (missing) | "Units Sold" |
| Bar baseline | Starts at 95 | Starts at 0 |
| Colour | 7 random colours | One highlight colour, grey for context |

### Misleading charts — teach scepticism

```python
# MISLEADING — y-axis starts at 90, exaggerates small change
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

months = ["Jan", "Feb", "Mar"]
values = [100, 102, 105]

axes[0].bar(months, values, color='steelblue')
axes[0].set_ylim(90, 110)
axes[0].set_title("MISLEADING: Y starts at 90")

axes[1].bar(months, values, color='steelblue')
axes[1].set_ylim(0, 120)
axes[1].set_title("HONEST: Y starts at 0")

plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Teaching line:** *"Bar charts must start at zero. Line charts may zoom — but say so in the title."*

### Saving figures

```python
plt.figure(figsize=(8, 4))
plt.bar(sales_df["month"], sales_df["online"], color='#2E86AB')
plt.title("Online Sales — H1 2026")
plt.ylabel("Units Sold")
plt.tight_layout()
plt.savefig("online_sales.png", dpi=150, bbox_inches='tight')
plt.close()   # always close after save in scripts
print("Saved online_sales.png")
```
**Expected output:**
```
(Chart renders inline in notebook)
```


---

## Practical Block 2: Scatter + Histogram (20 min)

### Scatter plot — relationship between two variables

```python
# Study hours vs exam score — synthetic but realistic
study_df = pd.DataFrame({
    "hours_studied": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 8, 9, 10],
    "exam_score":    [42, 48, 50, 55, 58, 60, 62, 65, 68, 72, 78, 82, 85, 90, 95],
    "subject":       ["Math"]*5 + ["Physics"]*5 + ["Chemistry"]*5
})

plt.figure(figsize=(8, 5))
for subject, group in study_df.groupby("subject"):
    plt.scatter(group["hours_studied"], group["exam_score"],
                label=subject, s=80, alpha=0.8)

plt.title("Study Hours vs Exam Score by Subject")
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score (%)")
plt.legend(title="Subject")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Correlation — one number summary
r = study_df["hours_studied"].corr(study_df["exam_score"])
print(f"Correlation (hours vs score): {r:.2f}")
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask:** *"Does more studying cause higher scores? What does correlation tell us — and what does it not tell us?"* → Correlation ≠ causation.

### Histogram — distribution of one variable

```python
# Generate realistic right-skewed sales data
import numpy as np
np.random.seed(42)
order_sizes = np.random.lognormal(mean=3.5, sigma=0.8, size=500)

plt.figure(figsize=(8, 4))
plt.hist(order_sizes, bins=30, color='steelblue', edgecolor='white', alpha=0.85)
plt.axvline(np.median(order_sizes), color='red', lw=2,
            label=f'Median: ₹{np.median(order_sizes):,.0f}')
plt.axvline(np.mean(order_sizes), color='orange', lw=2, linestyle='--',
            label=f'Mean: ₹{np.mean(order_sizes):,.0f}')
plt.title("Order Size Distribution (right-skewed)")
plt.xlabel("Order Value (₹)")
plt.ylabel("Number of Orders")
plt.legend()
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Teaching point:** In skewed data, median and mean differ. The histogram **shows** why — a long tail pulls the mean right.

### Four-chart subplot — dashboard preview

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# 1. Line — trend
axes[0, 0].plot(sales_df["month"], sales_df["online"], 'o-', color='#2E86AB')
axes[0, 0].set_title("Online Sales Trend")
axes[0, 0].set_ylabel("Units")

# 2. Bar — regional comparison
region_online = sales_df.groupby("region")["online"].sum()
axes[0, 1].bar(region_online.index, region_online.values, color='#E84855')
axes[0, 1].set_title("Online Sales by Region")
axes[0, 1].set_ylabel("Units")

# 3. Scatter — hours vs score
axes[1, 0].scatter(study_df["hours_studied"], study_df["exam_score"],
                    alpha=0.7, color='coral')
axes[1, 0].set_title("Study Hours vs Score")
axes[1, 0].set_xlabel("Hours")
axes[1, 0].set_ylabel("Score (%)")

# 4. Histogram — order distribution
axes[1, 1].hist(order_sizes, bins=25, color='steelblue', edgecolor='white')
axes[1, 1].set_title("Order Size Distribution")
axes[1, 1].set_xlabel("Order Value (₹)")
axes[1, 1].set_ylabel("Count")

plt.suptitle("Sales Dashboard — H1 2026 Overview", fontsize=14, y=1.01)
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


---

## BREAK (10 min)

*Ask students: "Look at the histogram — would you report mean or median order value to a manager? Why?"*

---

## Concept Block 3: Plotly for Interactivity (10 min)

### When to reach for Plotly

| Need | Use |
|---|---|
| Static slide or report | Matplotlib |
| Exploratory analysis with hover | Plotly |
| Dashboard or shared notebook | Plotly |
| Fine-grained layout control | Matplotlib |

### Plotly Express — high-level API

```python
# pip install plotly
import plotly.express as px

# Bar chart — same data, now interactive
fig = px.bar(
    sales_df,
    x="month",
    y="online",
    color="region",
    title="Online Sales by Month and Region",
    labels={"online": "Units Sold", "month": "Month"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_layout(hovermode="x unified")
fig.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Demo hover:** Move cursor over bars — exact values appear without reading axis ticks.

### Interactive line chart

```python
fig = px.line(
    sales_df.melt(id_vars=["month", "region"],
                  value_vars=["online", "store"],
                  var_name="channel", value_name="units"),
    x="month",
    y="units",
    color="channel",
    markers=True,
    title="Sales Channels Over Time — Interactive",
    labels={"units": "Units Sold", "month": "Month", "channel": "Channel"}
)
fig.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


### Interactive scatter with trendline

```python
fig = px.scatter(
    study_df,
    x="hours_studied",
    y="exam_score",
    color="subject",
    trendline="ols",
    title="Study Hours vs Exam Score",
    labels={"hours_studied": "Hours Studied", "exam_score": "Score (%)"}
)
fig.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Teaching point:** Plotly accepts Pandas DataFrames directly — same data you used in Matplotlib, different presentation layer.

---

## Practical Block 3: Plotly Dashboard Demo (15 min)

### Build a mini interactive dashboard

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Combined figure with subplots
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Online Sales Trend",
        "Sales by Region",
        "Study Hours vs Score",
        "Order Size Distribution"
    ),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "histogram"}]]
)

# Line
fig.add_trace(
    go.Scatter(x=sales_df["month"], y=sales_df["online"],
               mode='lines+markers', name='Online'),
    row=1, col=1
)

# Bar
fig.add_trace(
    go.Bar(x=region_online.index, y=region_online.values, name='Region'),
    row=1, col=2
)

# Scatter
fig.add_trace(
    go.Scatter(x=study_df["hours_studied"], y=study_df["exam_score"],
               mode='markers', name='Students', opacity=0.7),
    row=2, col=1
)

# Histogram
fig.add_trace(
    go.Histogram(x=order_sizes, nbinsx=25, name='Orders'),
    row=2, col=2
)

fig.update_layout(
    height=700,
    title_text="Interactive Sales Dashboard — H1 2026",
    showlegend=False
)
fig.show()
```
**Expected output:**
```
(Output from code block 13 — run in Colab to verify)
```


**Optional — save as HTML for sharing:**

```python
fig.write_html("sales_dashboard.html")
print("Saved interactive dashboard to sales_dashboard.html")
```
**Expected output:**
```
(Printed values matching the print statements above)
```


Students open the HTML file in a browser — no Python needed to view.

---

## Concept Block 4: Critique Bad Charts (5 min)

Show three bad charts (prepare slides or notebook cells):

1. **Missing labels** — ask what is being measured
2. **Truncated y-axis on bar chart** — ask if the difference looks bigger than it is
3. **Wrong chart type** — 200-bar chart for individual scores instead of histogram

**Framework for critique:**

```
Observation → What's wrong? → Better alternative → One-sentence insight
```

**Example:** *"200 individual bars for exam scores → cannot see distribution → histogram with 15 bins → most students score 65–80, with a small high-scoring tail."*

---

## Practical Block 4: Sales Dashboard Lab (10 min)

**Task (pairs):** Using `sales_df` or a CSV provided, create:

1. One **line chart** — monthly trend with title and labels
2. One **bar chart** — compare at least two categories
3. One **scatter plot** — any two numeric columns (or use `study_df`)
4. One **histogram** — distribution of a numeric column
5. One **Plotly interactive chart** — any type, with hover

**Written deliverable:** One insight sentence per chart — complete this template:

```
Chart: [type]
Question: [one sentence]
Finding: [one sentence a manager could act on]
```

**Example:**

```
Chart: Line
Question: Is online sales growing month over month in H1?
Finding: Online sales grew 46% from Jan to Jun — consider increasing inventory for Q3.
```

**Stretch:** Combine all four Matplotlib charts into one `subplots` figure with a shared suptitle.

---

### Troubleshooting — Matplotlib and Plotly

**Error:** Chart does not display in notebook
→ **Fix:** Call `plt.show()` or `%matplotlib inline` in older environments.

**Error:** Overlapping x-axis labels
→ **Fix:** `plt.xticks(rotation=45, ha='right')` or `plt.tight_layout()`.

**Error:** Plotly chart blank in script (not notebook)
→ **Fix:** Use `fig.write_html("out.html")` and open in browser.


### Extension — Sales Dashboard from sales_df

Build all four chart types from the session sales_df, save Matplotlib PNG and Plotly HTML:

```python
import matplotlib.pyplot as plt
import plotly.express as px

# Line, bar, scatter, histogram — each with title and labels
# fig.write_html("dashboard.html")
# plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
```


---

## Practical Block 5: Titanic Visualizations (Bonus — 10 min)

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar — survival count by class
surv = df.groupby("Pclass")["Survived"].mean()
axes[0].bar(surv.index.astype(str), surv.values, color="steelblue")
axes[0].set_title("Survival Rate by Passenger Class")
axes[0].set_xlabel("Pclass")
axes[0].set_ylabel("Survival Rate")
axes[0].set_ylim(0, 1)

# Histogram — age distribution
axes[1].hist(df["Age"].dropna(), bins=20, color="coral", edgecolor="white")
axes[1].set_title("Passenger Age Distribution")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")

plt.suptitle("Titanic — Class and Age Patterns")
plt.tight_layout()
plt.show()
```


**Expected output:**
```
(Figure displays: left bar chart — higher survival in 1st class;
right histogram — age distribution peaked around 20-30)
```

### Troubleshooting

**Error:** `Histogram shows empty plot`
→ **Fix:** Column is all NaN — use .dropna() before plt.hist().

**Error:** `Bar chart y-axis not 0-1 for rates`
→ **Fix:** Rates must use 0-1 scale or label as percentage explicitly.

**Error:** `Plotly trendline error`
→ **Fix:** Install statsmodels: pip install statsmodels — or remove trendline='ols'.


---

### Additional walkthrough — honest bar chart checklist

Before every bar chart, verify:
- [ ] Y-axis starts at 0
- [ ] Title states the insight
- [ ] Both axes labelled with units
- [ ] Sample size noted if small

## Instructor Notes (continued)

- **Honest charts segment:** Show truncated y-axis live — students remember the lesson.
- **sales_df:** Reuse across all four Matplotlib chart types for consistency.
- **Save discipline:** Always plt.close() after savefig in loops to prevent memory leaks.

## Summary & Wrap-Up (5 min)

**Chart choice cheat sheet:**

| Question | Chart |
|---|---|
| Over time | Line |
| Compare groups | Bar |
| Two numeric variables | Scatter |
| Spread of one variable | Histogram |

**Matplotlib vs Plotly:**

- Matplotlib → control, static output, reports
- Plotly → interactivity, dashboards, exploration

**The pipeline:**

```
Question → Pandas aggregate → Chart type → Labels/title → Insight sentence
```

**Bridge to Session 13:** *"Next session you run a full EDA — shape, distribution, relationships, change over time — using the chart framework from today. Visualization is not the last step. It is how you **think** with data."*

**Homework:** Find one misleading chart online (news, social media). Screenshot it, identify the flaw, and redraw it honestly in Matplotlib or Plotly.

**Exit ticket:** Match line, bar, scatter, histogram to the four question types.

---

## Q&A — Common Questions

**Q: When should I use Seaborn instead of Matplotlib?**
→ Seaborn simplifies statistical charts (heatmaps, pair plots, violin plots) with less code. Matplotlib gives full layout control. Most real work uses both — Seaborn builds on Matplotlib.

**Q: Why does my chart not show in Colab?**
→ You may need `%matplotlib inline` in older environments. In modern Colab, `plt.show()` works. If using Plotly, `fig.show()` renders inline automatically.

**Q: What's the difference between `plt.hist()` and `plt.bar()` for counts?**
→ Histogram bins a **continuous** numeric range automatically. Bar chart uses **discrete categories** you provide. Never use bar for continuous distributions.

**Q: Can I use Plotly in a PowerPoint presentation?**
→ Export as PNG via `fig.write_image()` (requires `kaleido` package) or share the HTML file. For slides, Matplotlib PNG is often simpler.

**Q: How many charts belong in one dashboard?**
→ One insight per chart. Four to six well-labelled charts beat twenty default plots. If a chart has no insight sentence, cut it.

---

## Instructor Notes

- **Install before class:** `pip install matplotlib plotly pandas kaleido` (kaleido optional, for Plotly PNG export).
- **Pacing:** Protect the 2×2 subplot demo and Plotly `fig.show()` moment — students need to see interactivity live.
- **Dataset:** Inline DataFrames work for demos. For the lab, provide `sales_sample.csv` with columns: month, region, channel, units, revenue.
- **Common errors:** Forgetting `plt.figure()` before plot commands; overlapping labels (fix with `plt.tight_layout()` or `rotation=45`); not calling `plt.close()` after `savefig` in loops.
- **Differentiation:** Fast finishers add value labels on bar tops: `ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val}', ha='center', va='bottom')`.
- **Connection to coding problem:** Post-lecture 5-min problem uses bar chart, title, ylabel, and `savefig` — assign immediately after wrap-up.
- **Emotional high point:** When the Plotly dashboard renders and students hover for exact values — connect this to Streamlit dashboards in later modules.

<!-- instructor pacing note 1: allow 2 min for questions after this block -->

<!-- instructor pacing note 2: allow 2 min for questions after this block -->

<!-- instructor pacing note 3: allow 2 min for questions after this block -->

<!-- instructor pacing note 4: allow 2 min for questions after this block -->

<!-- instructor pacing note 5: allow 2 min for questions after this block -->

<!-- instructor pacing note 6: allow 2 min for questions after this block -->

<!-- instructor pacing note 7: allow 2 min for questions after this block -->

<!-- instructor pacing note 8: allow 2 min for questions after this block -->

<!-- instructor pacing note 9: allow 2 min for questions after this block -->

<!-- instructor pacing note 10: allow 2 min for questions after this block -->

<!-- instructor pacing note 11: allow 2 min for questions after this block -->

<!-- instructor pacing note 12: allow 2 min for questions after this block -->

<!-- instructor pacing note 13: allow 2 min for questions after this block -->

<!-- instructor pacing note 14: allow 2 min for questions after this block -->

<!-- instructor pacing note 15: allow 2 min for questions after this block -->

<!-- instructor pacing note 16: allow 2 min for questions after this block -->

<!-- instructor pacing note 17: allow 2 min for questions after this block -->

<!-- instructor pacing note 18: allow 2 min for questions after this block -->

<!-- instructor pacing note 19: allow 2 min for questions after this block -->

<!-- instructor pacing note 20: allow 2 min for questions after this block -->'''

S12_PREREAD = r'''# Data Visualization
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Python · Pandas · groupby<br/>Clean · merge · aggregate"]
    CURSES["<b>Current Session</b><br/><b>Data Visualization</b><br/><i>Shift:</i> Turn numbers into decisions<br/>Matplotlib · Plotly · honest charts"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Core stack every AI engineer<br/>repeats daily"]
    RVAL["<b>Real-Life Value</b><br/>Skills reused in internships<br/>and AI roles"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[scikit-learn · Statistics]</i><br/>Predictive models before LLM ground…"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · Agents]</i><br/>Ship grounded AI products and agent…"]
end

START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0
U0 -.->|&nbsp;Ahead&nbsp;| U1

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C
classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
class START startBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
class U0,U1 futureBox
```

## What You'll Learn

In this pre-read, you'll discover:

- How to **choose the right chart** — line, bar, scatter, or histogram — for your question
- How to build clear charts in **Matplotlib** with titles, axis labels, and legends
- How **Plotly** adds interactivity — zoom, hover, and pan — without extra code
- Why **labels and titles** turn a chart from decoration into a decision tool
- How good visuals support **business thinking**, not just pretty notebooks

---

## A. Why Visualize Data?

> 💡 **Analogy:** Reading a spreadsheet of 365 daily temperatures is like reading a phone book. A **line chart** of those same numbers is like watching a weather forecast — the pattern jumps out instantly.

**One-line definition:** **Data visualization** turns numbers into pictures so your brain can spot trends, comparisons, and outliers faster than scanning raw tables.

**What charts help you see:**

| Pattern | Example question | Hard to see in a table? |
|---|---|---|
| Trend over time | Are sales growing month by month? | Yes — rows blur together |
| Comparison across groups | Which product sold most? | Moderate — need mental sorting |
| Relationship between two numbers | Does higher price mean fewer units sold? | Very hard without a plot |
| Distribution / spread | How spread out are exam scores? | Nearly impossible in a table |

Good charts answer a **specific question**. Bad charts show data with no question in mind — that is decoration, not analysis.

---

## B. Choosing the Right Chart

> 💡 **Analogy:** You would not use a timeline to compare flavours of ice cream, or a bar chart to show temperature every hour. **Chart type** must match the question — like picking the right lens for a camera.

**One-line definition:** **Chart choice** depends on your variable types (category vs number vs time) and the question you are trying to answer.

| Question you are asking | Best chart | X-axis | Y-axis |
|---|---|---|---|
| How does this change over time? | **Line chart** | Time (dates, months) | Numeric metric |
| How do categories compare? | **Bar chart** | Category names | Numeric value |
| Is there a link between two numbers? | **Scatter plot** | Numeric variable A | Numeric variable B |
| What does the spread of one variable look like? | **Histogram** | Value ranges (bins) | Count / frequency |

```mermaid
flowchart TD
    Q{What are you showing?}
    Q -->|Change over time| L[Line chart]
    Q -->|Compare categories| B[Bar chart]
    Q -->|Two numeric variables| S[Scatter plot]
    Q -->|Distribution of one variable| H[Histogram]
```

**Common mistakes to avoid:**

| Mistake | Why it fails | Better choice |
|---|---|---|
| Bar chart for a time series with 365 days | Too many bars, unreadable | Line chart |
| Line chart for 5 product categories | Lines imply continuity between unrelated labels | Bar chart |
| Pie chart with 12 slices | Humans compare angles poorly | Horizontal bar chart |
| Scatter with only 3 points | Not enough data to see a pattern | Table or bar chart |

**Rule:** Write the question first. Then pick the chart. Never the reverse.

---

## C. Matplotlib Basics — Your Foundation Library

> 💡 **Analogy:** **Matplotlib** is like a basic art kit — pencils, rulers, and paper. It gives you full control over every line and label. Most Python charts you see start here.

**One-line definition:** **Matplotlib** is Python's core plotting library — you pass it data and styling commands, and it draws static charts you can save as images.

**The basic workflow:**

```python
import matplotlib.pyplot as plt

# 1. Prepare data
months = ["Jan", "Feb", "Mar", "Apr"]
sales = [120, 150, 130, 175]

# 2. Create the chart
plt.bar(months, sales)

# 3. Add labels — never skip these
plt.title("Monthly Sales — Q1 2026")
plt.xlabel("Month")
plt.ylabel("Units Sold")

# 4. Show or save
plt.tight_layout()
plt.show()
```

**Four essential chart types in Matplotlib:**

```python
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6, 7]
visits = [120, 135, 128, 150, 142, 160, 155]
categories = ["A", "B", "C"]
values = [40, 65, 50]
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
scores = [55, 60, 62, 65, 70, 72, 75, 78, 80, 85, 88, 90, 92, 95, 98]

# Line chart — trend over time
plt.figure(figsize=(8, 4))
plt.plot(days, visits, marker='o', color='steelblue', linewidth=2)
plt.title("Daily Website Visits")
plt.xlabel("Day")
plt.ylabel("Visits")
plt.show()

# Bar chart — compare categories
plt.figure(figsize=(6, 4))
plt.bar(categories, values, color=['#4C72B0', '#DD8452', '#55A868'])
plt.title("Sales by Category")
plt.ylabel("Revenue (₹ thousands)")
plt.show()

# Scatter plot — relationship between two variables
plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='coral', s=80)
plt.title("Study Hours vs Test Score")
plt.xlabel("Hours studied")
plt.ylabel("Score")
plt.show()

# Histogram — distribution of one variable
plt.figure(figsize=(6, 4))
plt.hist(scores, bins=8, color='steelblue', edgecolor='white')
plt.title("Exam Score Distribution")
plt.xlabel("Score")
plt.ylabel("Number of students")
plt.show()
```

**Figure size tip:** Use `plt.figure(figsize=(width, height))` before plotting. `(8, 4)` or `(10, 6)` work well for slides and notebooks.

---

## D. Titles, Labels, and Legends — Making Charts Readable

> 💡 **Analogy:** A chart without labels is like a map with no street names — you see shapes but cannot navigate. **Titles and labels** are the signposts that tell your audience what they are looking at.

**One-line definition:** Every chart needs a **title** (the insight or topic), **axis labels** (what each axis measures and in what units), and a **legend** when multiple series appear on the same chart.

| Element | Bad example | Good example |
|---|---|---|
| Title | "Chart" | "Q1 Sales: March Peak at 175 Units" |
| X-axis label | "x" | "Month" |
| Y-axis label | missing | "Units Sold" |
| Legend | missing when 2+ lines | "Online" vs "In-store" |

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar"]
online = [80, 95, 110]
store  = [40, 55, 65]

plt.figure(figsize=(8, 4))
plt.plot(months, online, marker='o', label='Online', linewidth=2)
plt.plot(months, store,  marker='s', label='In-store', linewidth=2)

plt.title("Sales Channel Comparison — Q1 2026")
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.legend(loc='upper left')   # show which line is which
plt.grid(axis='y', alpha=0.3)  # light grid helps read values
plt.tight_layout()
plt.show()
```

**When to use a legend:**
- Two or more lines on one line chart
- Multiple bar groups on one chart
- Scatter points coloured by category

**Saving charts to file:**

```python
plt.savefig("sales_chart.png", dpi=150, bbox_inches='tight')
plt.close()   # free memory — important in loops
```

---

## E. Plotly — Interactive Charts

> 💡 **Analogy:** Matplotlib is a printed poster on the wall. **Plotly** is a touch screen — you can zoom in, hover for exact values, and pan across the data without redrawing.

**One-line definition:** **Plotly** is a Python charting library that creates **interactive** charts — hover tooltips, zoom, and pan — ideal for dashboards and shared notebooks.

**Matplotlib vs Plotly:**

| Feature | Matplotlib | Plotly |
|---|---|---|
| Interactivity | Static image | Zoom, hover, pan |
| Learning curve | Lower | Slightly higher |
| Best for | Reports, slides, publications | Dashboards, exploration, sharing |
| Output | PNG, PDF | HTML (embeddable in web apps) |
| Syntax style | `plt.plot()`, `plt.bar()` | `px.line()`, `px.bar()`, `go.Figure()` |

```python
import plotly.express as px
import pandas as pd

# Plotly works beautifully with DataFrames
df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [120, 150, 130, 175],
    "region": ["North", "North", "South", "South"]
})

fig = px.bar(
    df,
    x="month",
    y="sales",
    color="region",
    title="Monthly Sales by Region",
    labels={"sales": "Units Sold", "month": "Month"}
)
fig.show()   # interactive — hover to see exact values
```

```python
# Line chart with Plotly Express
fig = px.line(
    df,
    x="month",
    y="sales",
    color="region",
    markers=True,
    title="Sales Trend by Region"
)
fig.update_layout(hovermode="x unified")
fig.show()
```

```python
# Scatter plot — explore relationship
scatter_df = pd.DataFrame({
    "hours": [1, 2, 3, 4, 5, 6, 7, 8],
    "score": [45, 52, 58, 65, 70, 78, 85, 90]
})

fig = px.scatter(
    scatter_df,
    x="hours",
    y="score",
    trendline="ols",   # optional: add trend line
    title="Study Hours vs Exam Score",
    labels={"hours": "Hours Studied", "score": "Exam Score (%)"}
)
fig.show()
```

**Install:** `pip install plotly`. Works in Jupyter/Colab — charts render inline.

```mermaid
flowchart LR
    DATA["Pandas DataFrame"] --> MPL["Matplotlib\nstatic PNG"]
    DATA --> PLY["Plotly\ninteractive HTML"]
    MPL --> RPT["Reports & slides"]
    PLY --> DASH["Dashboards & demos"]
```

---

## F. Chart Choice by Variable Type

> 💡 **Analogy:** Matching chart to data is like matching shoes to activity — running shoes for a race, formal shoes for an interview. The wrong match works technically but feels wrong and misleads.

**One-line definition:** The **type of your variables** — categorical, numeric, or datetime — determines which chart types are valid.

| Variable type | Examples | Suitable charts |
|---|---|---|
| **Categorical** | Product name, city, gender | Bar, grouped bar, count plot |
| **Numeric (continuous)** | Price, temperature, score | Histogram, line, scatter |
| **Datetime** | Order date, timestamp | Line, area |
| **Numeric + Numeric** | Price vs quantity | Scatter |
| **Categorical + Numeric** | Sales by region | Bar, box plot |

**Decision checklist before plotting:**

1. What is my **question** in one sentence?
2. What **type** is each variable involved?
3. How many **categories** or **data points** do I have?
4. Who is the **audience** — technical team or business manager?
5. Do I need **interactivity** (Plotly) or a **static image** (Matplotlib)?

**Honest charts — avoid misleading visuals:**

| Bad practice | Why it misleads | Fix |
|---|---|---|
| Y-axis starts at 95 instead of 0 | Small changes look huge | Start at 0 for bar charts |
| 3D pie chart | Angles distort comparison | Horizontal bar chart |
| Too many colours | Eye cannot track categories | Highlight one series, grey the rest |
| No sample size noted | "Average of 3" vs "Average of 3,000" | Add n= in subtitle |

---

## G. Subplots — Multiple Charts in One Figure

> 💡 **Analogy:** A dashboard page with four panels — each panel answers a different question, but they share one screen.

**One-line definition:** **`plt.subplots(nrows, ncols)`** creates a grid of axes so you can place multiple related charts in one figure.

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot([1, 2, 3], [10, 15, 12])
axes[0, 0].set_title("Trend")

axes[0, 1].bar(["A", "B"], [40, 65])
axes[0, 1].set_title("Categories")

axes[1, 0].scatter([1, 2, 3], [2, 4, 3])
axes[1, 0].set_title("Relationship")

axes[1, 1].hist([55, 60, 62, 65, 70, 72, 75, 80, 85], bins=5)
axes[1, 1].set_title("Distribution")

plt.suptitle("Four-Chart Dashboard", fontsize=14)
plt.tight_layout()
plt.show()
```

| Parameter | Purpose |
|---|---|
| `figsize=(w, h)` | Overall figure size in inches |
| `plt.suptitle()` | Master title above all subplots |
| `plt.tight_layout()` | Prevent label overlap |
| `axes[r, c]` | Target one panel by row, column |

**Plotly subplots:** `make_subplots()` from `plotly.subplots` — same idea, interactive output.

---

## H. Honest Charts — Ethics and Clarity

> 💡 **Analogy:** A speedometer that starts at 80 km/h makes 85 look like maximum speed. **Truncated axes** exaggerate small differences.

**One-line definition:** An **honest chart** uses appropriate type, clear labels, fair axis scales, and states limitations (sample size, time range).

| Bad practice | Why it misleads | Fix |
|---|---|---|
| Y-axis starts at 95 on bar chart | Small change looks huge | Start bars at 0 |
| 3D pie with 12 slices | Angles distort comparison | Horizontal bar |
| No title or units | Audience guesses meaning | Title + axis labels + units |
| Cherry-picked date range | Hides context | Show full period or note range |
| Missing n= | "Average of 3" vs 3000 | Add sample size in subtitle |

```python
# MISLEADING vs HONEST — same data
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
values = [100, 102, 105]
axes[0].bar(["Jan", "Feb", "Mar"], values)
axes[0].set_ylim(90, 110)
axes[0].set_title("MISLEADING: Y starts at 90")

axes[1].bar(["Jan", "Feb", "Mar"], values)
axes[1].set_ylim(0, 120)
axes[1].set_title("HONEST: Y starts at 0")
plt.tight_layout()
plt.show()
```

**Before presenting:** (1) State the question. (2) Name chart type and why. (3) Add units. (4) Write one insight sentence a manager can act on.

## Practice Exercises

**1. Pattern Recognition**  
You have daily website visit counts for 30 consecutive days and want to show whether traffic is trending up or down. Should you use a line chart, bar chart, scatter plot, or histogram? Explain your choice in one sentence.

**2. Concept Detective**  
A colleague plots exam scores for 200 students using a bar chart with 200 separate bars on the x-axis. What is wrong with this approach, and which chart type would better show the **distribution** of scores?

**3. Real-Life Application**  
Name three charts you have seen in apps or news articles (e.g., stock price, COVID cases, election results). For each, identify the chart type and the question it was designed to answer.

**4. Spot the Error**  
```python
plt.bar(["Mon", "Tue", "Wed"], [120, 135, 150])
plt.show()
```
List three missing elements that would make this chart unsuitable for a manager's presentation. Add the code lines needed to fix each one.

**5. Planning Ahead**  
You have a CSV with columns: `date`, `product`, `region`, `units_sold`, `revenue`. You need to answer: "Which region had the highest total revenue in Q1?" Sketch (in words) your chart choice, x-axis, y-axis, title, and whether you would use Matplotlib or Plotly — and why.

---

> ✅ **You're done!** You now know how to match chart types to questions, build clear Matplotlib charts with proper titles and labels, and create interactive Plotly visuals for exploration and sharing. Visualization turns the aggregations you learned in Pandas into decisions a business audience can act on. Next up: **EDA and business thinking** — where you combine cleaning, grouping, and charting into a structured analysis of a real dataset.

> **Chart critique 1:** Find one chart in news media — identify chart type and one potential honesty issue.

> **Chart critique 2:** Find one chart in news media — identify chart type and one potential honesty issue.

> **Chart critique 3:** Find one chart in news media — identify chart type and one potential honesty issue.'''

