# Lecture Script: Pandas — Loading, Inspection & Filtering
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

<!-- instructor pacing note 41: allow 2 min for questions after this block -->
