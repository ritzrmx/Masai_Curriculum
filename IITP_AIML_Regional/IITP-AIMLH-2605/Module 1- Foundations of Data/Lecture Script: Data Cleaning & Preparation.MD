# Lecture Script: Data Cleaning & Preparation (2 Hours)

## Session Overview
**Duration**: 2 hours (105 min teaching + 5 min break + 10 min quiz)
**Goal**: Students identify, handle, and prepare messy data using null treatment, duplicate removal, and column type management
**Audience**: Complete beginners — Session 1.5

---

## SEGMENT 1: Opening & Hook (8 min)

### Hook (3 min)

**Ask**: "Imagine you're analyzing customer data — 10,000 rows. You run your code and get a result. Would you trust it?"

**Ask**: "What if 800 of those rows had missing ages? What if 200 rows were exact duplicates entered twice by mistake?"

**Reveal**: "Real-world data is messy. Before any analysis or machine learning, data must be cleaned. In industry, data cleaning takes up to 80% of a data scientist's time. Today you learn how to do it systematically."

### Connect & Promise (5 min)

**Connect**: "Last session we loaded a CSV, inspected its shape, and selected columns. Today we go one level deeper — we look inside the data and fix what's broken."

**Say**: "There are four problems we tackle today, in this order:"

| Problem | Tool |
|---|---|
| Missing values — what are they? | `.isnull()`, `.sum()` |
| Drop or fill missing values | `.dropna()`, `.fillna()` |
| Duplicate rows | `.duplicated()`, `.drop_duplicates()` |
| Column types — numeric vs categorical | `.dtypes`, `pd.to_numeric()`, `.astype()` |

**Today's Promise**: "By the end, you will take a messy dataset and produce a clean, analysis-ready version of it."

---

## SEGMENT 2: Identifying Nulls (13 min)

### What is a Null? (4 min)

**Say**: "A **null** is a missing value — a cell in your table with no data. In Pandas, missing values appear as `NaN`, which stands for Not a Number."

**Show**:
```python
import pandas as pd
import numpy as np

data = {
    "name":  ["Ananya", "Rohan", None, "Priya"],
    "age":   [22, None, 25, 23],
    "score": [88, 91, 79, None]
}

df = pd.DataFrame(data)
print(df)
```
Output:
```
     name   age  score
0  Ananya  22.0   88.0
1   Rohan   NaN   91.0
2    None  25.0   79.0
3   Priya  23.0    NaN
```

**Break it down**:
- `None` in Python becomes `NaN` inside a Pandas DataFrame
- Pandas shows `NaN` wherever a value is missing
- Notice `age` became `float64` — because NaN forces numeric columns to float

### Detecting Nulls (5 min)

**Show**:
```python
print(df.isnull())
```
Output:
```
    name    age  score
0  False  False  False
1  False   True  False
2   True  False  False
3  False  False   True
```

**Say**: "`.isnull()` gives you a True/False map. But on a large dataset, this is hard to read. Use `.sum()` to count."

**Show**:
```python
print(df.isnull().sum())
```
Output:
```
name     1
age      1
score    1
dtype: int64
```

**Show** — percentage missing:
```python
print(df.isnull().sum() / len(df) * 100)
```
Output:
```
name     25.0
age      25.0
score    25.0
dtype: float64
```

**Say**: "This tells you what percentage of each column is missing. This number drives your next decision — drop or fill."

### Load the Real Dataset (4 min)

**Say**: "Let's switch to the Titanic dataset we used last session — it has real missing values."

**Show**:
```python
url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = pd.read_csv(url)

print(df.shape)
print(df.isnull().sum())
```
Output:
```
(891, 12)
PassengerId      0
Survived         0
Pclass           0
Name             0
Age            177
...
Cabin          687
Embarked         2
```

**Say**: "Age has 177 missing values. Cabin has 687 — that's 77% of the column missing. These two problems need different solutions."

**Student try**: Run `.isnull().sum()` on the Titanic dataset. Calculate what percentage of `Age` is missing. **(2 min)**

---

## SEGMENT 3: Drop vs Fill (13 min)

### Dropping Nulls (5 min)

**Say**: "`.dropna()` removes any row that contains at least one missing value."

**Show**:
```python
df_dropped = df.dropna()
print(df_dropped.shape)
```
Output:
```
(183, 12)
```

**Ask**: "We started with 891 rows. Why do we only have 183 now?" [Students think]

**Say**: "Because `Cabin` alone is missing in 687 rows. Dropping any row with any null wipes out most of our data. Dropping blindly is dangerous."

**Show** — drop only if a specific column is null:
```python
df_clean = df.dropna(subset=["Age"])
print(df_clean.shape)
```
Output:
```
(714, 12)
```

**Say**: "`subset=` lets you be specific. Now we only drop rows where `Age` is missing — we keep everything else."

**When to drop**: When very few rows are missing (under 5%) and removing them won't distort your data.

### Filling Nulls (5 min)

**Say**: "Sometimes dropping loses too much data. Instead, we fill missing values with a reasonable substitute."

**Show** — fill with mean:
```python
mean_age = df["Age"].mean()
print("Mean age:", round(mean_age, 1))

df["Age"] = df["Age"].fillna(mean_age)
print(df["Age"].isnull().sum())  # Should be 0
```
Output:
```
Mean age: 29.7
0
```

**Show** — fill with a fixed value:
```python
df["Embarked"] = df["Embarked"].fillna("Unknown")
print(df["Embarked"].value_counts())
```

**Break it down**:

| Strategy | Use when |
|---|---|
| `.fillna(mean)` | Numeric column, values are roughly symmetric |
| `.fillna(median)` | Numeric column, outliers present |
| `.fillna("Unknown")` | Text column, missing means no info |
| `.dropna(subset=["col"])` | Missing rows are few and droppable |

**Important**:
```python
# Wrong — result is not saved
df["Age"].fillna(29.7)
print(df["Age"].isnull().sum())   # Still has nulls

# Right — assign it back
df["Age"] = df["Age"].fillna(29.7)
```

**Student try**: Fill the `Age` column with the median (use `.median()`). Then confirm nulls are gone with `.isnull().sum()`. **(2 min)**

### Drop the Cabin Column (3 min)

**Say**: "When a column is mostly missing — like `Cabin` at 77% — filling it creates fake data. The right move is to drop the whole column."

**Show**:
```python
df = df.drop(columns=["Cabin"])
print(df.shape)
print(df.columns.tolist())
```

**Say**: "`drop(columns=[...])` removes one or more columns. Now we have 11 columns instead of 12."

---

## SEGMENT 4: Handling Duplicates (12 min)

### What is a Duplicate Row? (3 min)

**Say**: "A duplicate is a row that appears more than once — exact same data entered twice. This can happen from data entry errors, system glitches, or merging datasets."

**Show** — create a small example with duplicates:
```python
data = {
    "name":  ["Ananya", "Rohan", "Ananya", "Priya", "Rohan"],
    "age":   [22, 25, 22, 23, 25],
    "score": [88, 91, 88, 79, 91]
}

df_ex = pd.DataFrame(data)
print(df_ex)
```
Output:
```
     name  age  score
0  Ananya   22     88
1   Rohan   25     91
2  Ananya   22     88   ← duplicate of row 0
3   Priya   23     79
4   Rohan   25     91   ← duplicate of row 1
```

### Detecting Duplicates (4 min)

**Show**:
```python
print(df_ex.duplicated())
```
Output:
```
0    False
1    False
2     True
3    False
4     True
dtype: bool
```

**Show** — count them:
```python
print(df_ex.duplicated().sum())
```
Output:
```
2
```

**Say**: "`.duplicated()` marks every row that is an exact copy of an earlier row. `.sum()` counts how many."

### Removing Duplicates (5 min)

**Show**:
```python
df_clean = df_ex.drop_duplicates()
print(df_clean)
print(df_clean.shape)
```
Output:
```
     name  age  score
0  Ananya   22     88
1   Rohan   25     91
3   Priya   23     79
(3, 5)
```

**Say**: "`.drop_duplicates()` keeps the first occurrence and removes all later copies."

**Show** — check Titanic for duplicates:
```python
url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = pd.read_csv(url)
print(df.duplicated().sum())
```
Output:
```
0
```

**Say**: "Titanic has no duplicate rows — but always check. On merged or scraped datasets, duplicates are very common."

**Student try**: On the small `df_ex` example, use `.duplicated().sum()` to count duplicates, then `.drop_duplicates()` to remove them. Print the shape before and after. **(2 min)**

---

## — 5-MINUTE BREAK —

---

## SEGMENT 5: Categorical vs Numeric Columns (13 min)

### Understanding Column Types (4 min)

**Say**: "Every column in a DataFrame has a data type. The two most important categories are **numeric** and **categorical**."

**Show**:
```python
url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = pd.read_csv(url)
print(df.dtypes)
```
Output:
```
PassengerId      int64
Survived         int64
Pclass           int64
Name            object
Sex             object
Age            float64
SibSp            int64
Parch            int64
Ticket          object
Fare           float64
Cabin           object
Embarked        object
```

**Break it down**:

| Dtype | Meaning | Example |
|---|---|---|
| `int64` | Whole numbers | Age: 22, 35 |
| `float64` | Decimal numbers | Fare: 7.25 |
| `object` | Text / mixed | Name, Sex |

**Say**: "`object` columns are usually **categorical** — they represent groups or labels, not quantities. `int64` and `float64` are **numeric**."

### Separating Column Types (4 min)

**Show**:
```python
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
cat_cols = df.select_dtypes(include=["object"]).columns

print("Numeric:", numeric_cols.tolist())
print("Categorical:", cat_cols.tolist())
```
Output:
```
Numeric: ['PassengerId', 'Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
Categorical: ['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked']
```

**Say**: "`.select_dtypes()` filters columns by type. This is how you quickly separate your data before analysis."

### Fixing Wrong Types (5 min)

**Say**: "Sometimes a column that should be numeric is stored as text — often because of a bad entry like a dash or the word 'unknown' in one row."

**Show**:
```python
data = {
    "passenger": ["A", "B", "C", "D"],
    "fare":      ["7.25", "71.28", "unknown", "13.00"]
}
df_ex = pd.DataFrame(data)
print(df_ex.dtypes)
```
Output:
```
passenger    object
fare         object   ← should be float
```

**Show** — convert with `pd.to_numeric`:
```python
df_ex["fare"] = pd.to_numeric(df_ex["fare"], errors="coerce")
print(df_ex)
print(df_ex.dtypes)
```
Output:
```
  passenger   fare
0         A   7.25
1         B  71.28
2         C    NaN   ← "unknown" became NaN
3         D  13.00

fare    float64
```

**Break it down**:
- `errors="coerce"` = if a value can't be converted to a number, replace it with `NaN`
- Now you can fill that NaN using what you learned earlier

**Show** — convert with `.astype()` when you're sure all values are valid:
```python
df["Pclass"] = df["Pclass"].astype(str)   # Numeric → string (treat as category)
print(df["Pclass"].dtype)
```
Output: `object`

**Say**: "`Pclass` is 1, 2, 3 — but these are class labels, not quantities. Converting to string signals to your code: don't do math on this."

**Student try**: On the Titanic `df`, use `.select_dtypes()` to print only the numeric columns. Then print the unique values of `Sex` using `.unique()`. **(2 min)**

---

## SEGMENT 6: Building Real Programs (20 min)

### Program 1: Null Report (5 min)

**Say**: "A function that gives a clean summary of missing data in any DataFrame."

```python
import pandas as pd

def null_report(df):
    total = df.isnull().sum()
    percent = (df.isnull().sum() / len(df) * 100).round(1)
    
    report = pd.DataFrame({
        "missing_count": total,
        "missing_pct":   percent
    })
    
    # Show only columns that have at least one null
    report = report[report["missing_count"] > 0]
    print(report.sort_values("missing_pct", ascending=False))

url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = pd.read_csv(url)
null_report(df)
```
Output:
```
             missing_count  missing_pct
Cabin                  687         77.1
Age                    177         19.9
Embarked                 2          0.2
```

### Program 2: Duplicate Checker and Cleaner (7 min)

**Say**: "A function that reports duplicates and returns a clean dataset."

```python
import pandas as pd

def remove_duplicates(df, report=True):
    before = df.shape[0]
    df_clean = df.drop_duplicates()
    after = df_clean.shape[0]
    removed = before - after
    
    if report:
        print(f"Rows before : {before}")
        print(f"Rows after  : {after}")
        print(f"Duplicates removed: {removed}")
    
    return df_clean

url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = pd.read_csv(url)
df_clean = remove_duplicates(df)
```
Output:
```
Rows before : 891
Rows after  : 891
Duplicates removed: 0
```

### Program 3: Full Data Cleaner (8 min)

**Say**: "A function that runs all cleaning steps in sequence and returns a ready dataset."

```python
import pandas as pd

def clean_dataset(url, drop_cols=None, fill_strategy="mean"):
    df = pd.read_csv(url)
    print(f"Loaded: {df.shape}")
    
    # Step 1: Drop specified columns
    if drop_cols:
        df = df.drop(columns=drop_cols)
        print(f"After dropping columns: {df.shape}")
    
    # Step 2: Fill numeric nulls
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            fill_val = df[col].mean() if fill_strategy == "mean" else df[col].median()
            df[col] = df[col].fillna(round(fill_val, 2))
            print(f"Filled '{col}' with {fill_strategy}: {round(fill_val, 2)}")
    
    # Step 3: Fill categorical nulls
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna("Unknown")
            print(f"Filled '{col}' with 'Unknown'")
    
    # Step 4: Remove duplicates
    df = df.drop_duplicates()
    
    print(f"\nFinal shape: {df.shape}")
    print(f"Remaining nulls: {df.isnull().sum().sum()}")
    return df

url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df_ready = clean_dataset(url, drop_cols=["Cabin"], fill_strategy="median")
```
Output:
```
Loaded: (891, 12)
After dropping columns: (891, 11)
Filled 'Age' with median: 28.0
Filled 'Embarked' with 'Unknown'

Final shape: (891, 11)
Remaining nulls: 0
```

---

## SEGMENT 7: Common Mistakes & Wrap (10 min)

### Common Mistakes (7 min)

**Mistake 1 — Not saving fillna back**
```python
# Wrong — original df unchanged
df["Age"].fillna(29)
print(df["Age"].isnull().sum())   # Still has nulls

# Right
df["Age"] = df["Age"].fillna(29)
```

**Mistake 2 — Dropping all nulls blindly**
```python
# Wrong — loses most data if one column is mostly empty
df_clean = df.dropna()
print(df_clean.shape)   # (183, 12) — 708 rows gone

# Right — target specific columns
df_clean = df.dropna(subset=["Age", "Embarked"])
```

**Mistake 3 — Filling numeric column with "Unknown"**
```python
# Wrong — turns numeric column into object
df["Age"] = df["Age"].fillna("Unknown")

# Right — fill with a number
df["Age"] = df["Age"].fillna(df["Age"].median())
```

**Mistake 4 — Forgetting to check for duplicates on merged data**
```python
# Always check after any merge or concatenation
print(df.duplicated().sum())   # Must be 0 before analysis
```

**Mistake 5 — Treating a label column as numeric**
```python
# Wrong — Pclass is 1, 2, 3 but they are categories
df["Pclass"].mean()   # Meaningless

# Right — convert to string/category first
df["Pclass"] = df["Pclass"].astype(str)
```

### Session Recap (3 min)

| Task | Method |
|---|---|
| Count missing values | `df.isnull().sum()` |
| Percentage missing | `df.isnull().sum() / len(df) * 100` |
| Drop rows with nulls | `df.dropna(subset=["col"])` |
| Fill nulls | `df["col"].fillna(value)` |
| Drop a column | `df.drop(columns=["col"])` |
| Find duplicates | `df.duplicated().sum()` |
| Remove duplicates | `df.drop_duplicates()` |
| Check column types | `df.dtypes` |
| Select by type | `df.select_dtypes(include=["float64"])` |
| Fix wrong type | `pd.to_numeric(df["col"], errors="coerce")` |

