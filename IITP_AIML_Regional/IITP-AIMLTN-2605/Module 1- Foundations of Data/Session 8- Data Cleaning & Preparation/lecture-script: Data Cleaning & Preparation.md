# Lecture Script: Data Cleaning & Preparation
> **Instructor Reference** — Module 1: Foundations of Data | Session 8 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can identify and fix the five most common data quality problems in a real CSV using Pandas — and explain *why* each step matters before any analysis or model.

**Student profile at this point:** Comfortable with Python basics, Pandas DataFrame creation, and basic indexing. Have seen `read_csv()`, `head()`, and `shape`.

**Key outcome:** By end of class, every student has a repeatable cleaning checklist they can apply to any new dataset.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** The Cleaning Mindset + Common Problems | 10 min | 0:15 |
| **Practical 1:** Explore + Audit a Messy Dataset | 15 min | 0:30 |
| **Concept 2:** Missing Values — 3 Strategies | 10 min | 0:40 |
| **Practical 2:** Handle Nulls — Drop, Fill, Impute | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Duplicates + Data Type Fixes | 10 min | 1:15 |
| **Practical 3:** Fix Duplicates, Types, and String Columns | 15 min | 1:30 |
| **Concept 4:** The Cleaning Workflow + Validation | 10 min | 1:40 |
| **Practical 4:** Live Mini-Project — Clean a Dataset End-to-End | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Open a spreadsheet of raw export data (or show this inline):

```
Name,Age,Email,Revenue,Date
Alice,28,alice@co.com,5000,01-03-2025
Bob,,bob@co.com,5000,01-03-2025
Alice,28,alice@co.com,5000,01-03-2025
Charlie,twenty-two,charlie@co.com,,15/03/2025
,35,dave@co.com,8000,2025-03-20
```

Ask the class: *"If I run `df.mean()` on this, what would happen? Would you trust the output?"*

**Context to set:** In real projects, 60–80% of data work is cleaning. Machine learning models trained on dirty data produce wrong predictions with high confidence — which is worse than no model at all. Today we learn to fix data before it misleads us.

**Learning contract for today:**
- Spot all five common problems in a dataset
- Fix each one systematically
- Validate the cleaned data before moving on

---

## Concept Block 1: The Cleaning Mindset & Common Problems (10 min)

### The Five Problems Every Dataset Has

| # | Problem | Example | Danger |
|---|---|---|---|
| 1 | Missing values | Age is NaN | Crashes calculations, wrong statistics |
| 2 | Duplicates | Same order appears twice | Revenue double-counted |
| 3 | Wrong data types | Revenue stored as string `"5,000"` | Math operations fail |
| 4 | Inconsistent formats | Dates as `01-03-25`, `March 1`, `2025/03/01` | Can't sort or filter |
| 5 | Outliers / impossible values | Age = 999, Revenue = -50000 | Distort averages, break models |

**Key teaching point:** These are not programming bugs. They are data entry, system migration, and export problems. Your job as a data professional is to handle them — not complain about them.

**The cleaning mindset — always ask three questions:**
1. *Why is this value missing / wrong?* (understanding → better fix)
2. *What will I do with this column downstream?* (context → right strategy)
3. *Have I validated the fix didn't introduce new problems?* (trust but verify)

---

## Practical Block 1: Explore + Audit a Messy Dataset (15 min)

### Dataset
Use the classic **Titanic dataset** (or provide a custom messy CSV). Titanic is ideal — it has nulls in Age, Cabin, Embarked; it has object/int type issues; it is familiar enough not to require domain explanation.

```python
import pandas as pd

# Load
df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
# Alternatively: df = pd.read_csv('titanic.csv')

print("Shape:", df.shape)
print("\n--- First look ---")
df.head()
```

### The Audit Checklist — show each command and its output meaning

```python
# 1. Shape — how many rows/columns?
print("Shape:", df.shape)

# 2. Column names and types
print(df.dtypes)

# 3. Missing value count per column
print(df.isnull().sum())
print("\nMissing %:")
print(df.isnull().mean().round(3) * 100)

# 4. Duplicates
print("\nDuplicate rows:", df.duplicated().sum())

# 5. Value distribution for key columns
print(df['Sex'].value_counts())
print(df['Pclass'].value_counts())
print(df['Age'].describe())
```

**Walk through each output.** Ask students: *"Age has 177 missing. What percentage is that? Should we drop or fill?"* Let them estimate before you show `isnull().mean()`.

**Write on board:** AUDIT → DECIDE → FIX → VALIDATE. This is the loop.

---

## Concept Block 2: Missing Values — 3 Strategies (10 min)

### The Three Strategies

```
Missing Value
├── Drop rows: when null rate > 50% OR column is critical
├── Fill with a constant: when "no value" has a meaning (e.g. 0, "Unknown")
└── Impute: fill with mean/median/mode when the column is numeric and needed
```

**Teaching decision tree — draw on board:**

```
Is this column important for analysis?
  ├── No → drop the entire column (Cabin in Titanic: 77% missing)
  └── Yes →
        Is null rate > 30%?
          ├── Yes → think carefully; imputing high-null columns adds noise
          └── No →
                Is it numeric?
                  ├── Yes → fill with median (robust to outliers) or mean
                  └── No → fill with mode, "Unknown", or most frequent
```

**Important distinction:** `dropna()` drops **rows**. `drop(columns=[...])` drops **columns**. Students constantly confuse these.

**What NOT to do:** Drop every row with any null — this can remove 40% of your data and bias the sample toward complete records.

---

## Practical Block 2: Handle Nulls — Drop, Fill, Impute (15 min)

```python
# --- Before: check nulls ---
print(df.isnull().sum())

# Strategy 1: Drop entire column (Cabin - 77% missing, not worth keeping)
df = df.drop(columns=['Cabin'])
print("After dropping Cabin:", df.isnull().sum())

# Strategy 2: Fill with mode (Embarked - only 2 missing)
mode_embarked = df['Embarked'].mode()[0]
print("Most common port:", mode_embarked)
df['Embarked'] = df['Embarked'].fillna(mode_embarked)

# Strategy 3: Impute with median (Age - 20% missing, numeric, important)
median_age = df['Age'].median()
print("Median age:", median_age)
df['Age'] = df['Age'].fillna(median_age)

# Validate
print("\nAfter cleaning nulls:")
print(df.isnull().sum())
```

**Live demonstration tip:** Run `df.isnull().sum()` before and after each step. The visible drop in null counts makes the impact concrete.

**Ask the class:** *"If we imputed Age with the mean instead of median, and there were 10 passengers with Age=2000 from a data entry error, what would happen?"* → Shows why median is safer.

**Extension for faster students:**
```python
# Conditional impute: fill age with median of same Pclass
df['Age'] = df.groupby('Pclass')['Age'].transform(lambda x: x.fillna(x.median()))
```

---

## BREAK (10 min)

*Suggested break prompt — ask them to open their own data (a CSV from a previous assignment or personal project) and run just the audit commands. They will share one finding after the break.*

---

## Concept Block 3: Duplicates + Data Type Fixes (10 min)

### Duplicates — Three Levels

| Level | What it means | Fix |
|---|---|---|
| Exact duplicate | Every column identical | `df.drop_duplicates()` |
| Key duplicate | Same order ID, different timestamp | `df.drop_duplicates(subset=['order_id'], keep='last')` |
| Near-duplicate | Same name, different capitalisation | Normalise first, then deduplicate |

**Teaching point:** Always define what "duplicate" means for your data. In Titanic, two people could have the same name — that's not a duplicate. In a sales table, the same order ID appearing twice is absolutely a duplicate.

### Data Type Fixes — Common Patterns

```
Wrong type → right fix:
"5,000.00" (string)      → pd.to_numeric(..., errors='coerce')
"2025-03-01" (string)    → pd.to_datetime(...)
"True"/"False" (string)  → df.astype(bool)
Integer 0/1              → can stay as int, or .astype(bool)
```

**Why types matter:** Pandas won't let you sort a "date" column stored as a string — it sorts alphabetically (`"2025-12-01"` before `"2025-02-01"` because `'1' > '0'`). Numeric operations on string columns raise a `TypeError`.

---

## Practical Block 3: Fix Duplicates, Types, and String Columns (15 min)

```python
# --- Duplicates ---
print("Duplicate rows before:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate rows after:", df.duplicated().sum())

# --- Type issues: create a demo example ---
# Imagine 'Fare' got imported as string in a dirty file
df_demo = df.copy()
df_demo['Fare'] = df_demo['Fare'].astype(str)  # simulate the problem
print("\nFare type (broken):", df_demo['Fare'].dtype)
# Try math on it — will fail or give wrong result
# print(df_demo['Fare'].mean())  # This now silently fails or errors

# Fix it
df_demo['Fare'] = pd.to_numeric(df_demo['Fare'], errors='coerce')
print("Fare type (fixed):", df_demo['Fare'].dtype)
print("Fare mean (now works):", df_demo['Fare'].mean())

# --- String normalisation ---
# Simulate inconsistent capitalisations
df_demo['Sex'] = df_demo['Sex'].str.strip().str.lower()
print("\nSex values:", df_demo['Sex'].value_counts())

# --- Date parsing ---
# Show with a date string column
import pandas as pd
date_strings = pd.Series(['01-03-2025', '15/03/2025', '2025-03-20'])
dates_fixed = pd.to_datetime(date_strings, dayfirst=True, errors='coerce')
print("\nParsed dates:")
print(dates_fixed)
print("Sorted:", dates_fixed.sort_values().values)
```

**Walk through the errors='coerce' behaviour** — unparseable values become NaT/NaN instead of crashing. Show a deliberately bad value: `pd.to_numeric(pd.Series(['100', 'twenty', '300']), errors='coerce')`.

---

## Concept Block 4: The Cleaning Workflow + Validation (10 min)

### The Repeatable 7-Step Workflow

```
Step 1: LOAD — read_csv, check shape
Step 2: AUDIT — dtypes, isnull().sum(), duplicated().sum(), describe()
Step 3: DECIDE — document each column's fate (keep/fix/drop)
Step 4: DROP — columns and rows with excessive nulls or true duplicates
Step 5: FIX TYPES — to_numeric, to_datetime, astype
Step 6: HANDLE NULLS — fill or impute remaining nulls
Step 7: VALIDATE — re-run audit; check describe() again; compare shape before/after
```

### Validation — What to Check After Cleaning

```python
# Shape should have changed predictably
print(f"Before: {original_shape}, After: {df.shape}")

# No remaining nulls in important columns
assert df['Age'].isnull().sum() == 0
assert df['Embarked'].isnull().sum() == 0

# No duplicates
assert df.duplicated().sum() == 0

# Types are correct
assert df['Age'].dtype in ['float64', 'int64']

# Ranges are sensible
print(df['Age'].describe())  # Min > 0, Max < 120
print(df['Fare'].describe())  # No negative fares
```

**Key message:** Assertions are your safety net. Write them after every clean. A future collaborator (or future you) will thank you.

---

## Practical Block 4: Mini-Project — Clean End-to-End (10 min)

**Give students a new messy CSV** (2-3 minutes to read and audit alone, then solve together):

```python
# Messy mini dataset — paste and load
import io
raw = """
order_id,customer,amount,order_date,status
1001,Alice,5000.00,01-03-2025,completed
1002,bob ,,"15/03/2025",pending
1001,Alice,5000.00,01-03-2025,completed
1003,Charlie,-500,2025-03-20,
1004,Dave,8000,March 25 2025,Completed
1005,,6000,01-04-2025,completed
"""

df_mini = pd.read_csv(io.StringIO(raw))
print(df_mini)
print("\n--- Audit ---")
print(df_mini.dtypes)
print(df_mini.isnull().sum())
print("Duplicates:", df_mini.duplicated().sum())
```

**Walk through solutions together:**

```python
# Step 1: Remove duplicate
df_mini = df_mini.drop_duplicates()

# Step 2: Fix types
df_mini['amount'] = pd.to_numeric(df_mini['amount'], errors='coerce')
df_mini['order_date'] = pd.to_datetime(df_mini['order_date'],
                                        dayfirst=True, errors='coerce')

# Step 3: Normalise strings
df_mini['customer'] = df_mini['customer'].str.strip().str.title()
df_mini['status'] = df_mini['status'].str.strip().str.lower()

# Step 4: Handle nulls
df_mini['status'] = df_mini['status'].fillna('unknown')
df_mini['customer'] = df_mini['customer'].fillna('Unknown Customer')
# Flag negative amounts as suspect rather than dropping
df_mini['amount_flag'] = df_mini['amount'] < 0

print("\n--- Cleaned ---")
print(df_mini)
```

**Discussion:** For the missing `customer` row — should we drop it or flag it? This is a business decision. Always document it.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- The 5-problem audit before any analysis begins
- 3 strategies for missing values (drop column / fill constant / impute)
- Deduplication at the exact and key level
- Type fixing: `to_numeric`, `to_datetime`, `astype`, `str.lower()`
- The 7-step repeatable workflow with validation assertions

**Bridge to next session:** *"Now that our data is clean, next class we learn Query Thinking — how to filter, group, and slice data efficiently, and how that logic carries from Pandas directly into SQL."*

**Homework / self-practice:** Apply the 7-step workflow to any CSV from Kaggle (Superstore, HR Analytics, or Indian Census datasets work well). Write down 3 problems you found and how you fixed them.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Should I always impute with median? What about mean?**
→ Use median for skewed distributions or when outliers are possible. Use mean only when data is symmetric and clean. A single extreme outlier makes the mean unreliable as a fill value.

**Q: What if a column has 40% missing — is that too much to impute?**
→ It depends on the use case. For ML features, imputing 40% adds significant noise. For reporting, it may be acceptable with documentation. There is no universal threshold — 20-30% is where most practitioners start questioning imputation.

**Q: Can `drop_duplicates()` accidentally drop real rows?**
→ Yes, if two legitimate records happen to be identical (same product bought twice). Use `subset=` to define which columns define uniqueness, and document your decision.

**Q: What does `errors='coerce'` do exactly?**
→ Instead of crashing on a value it cannot convert (like the string "twenty"), it silently replaces it with `NaN`. Always follow with a null check to see how many values coerced.

---

## Instructor Notes

- **Dataset:** Titanic CSV is freely available and well-known. Alternatively, use a custom "orders" dataset for a business context.
- **Common student mistake:** Using `df.fillna(df.mean())` on the whole DataFrame — this fills string columns with NaN (no effect) and numeric columns all at once, which is usually too aggressive. Show column-specific fills.
- **Live coding tip:** Deliberately make a mistake (e.g., use `fillna(df['Age'].mean())` and show how outliers affect the mean) to demonstrate why median is preferred.
- **For advanced students:** Introduce `df.pipe()` for chaining cleaning steps into a reusable pipeline function.
- **Time check:** If running long after the break, skip the mini-project live coding and give it as homework with the solution.
