# Lecture Script: Numerical & Tabular Data Foundations (2 Hours)

## Session Overview
**Duration**: 2 hours (105 min teaching + 5 min break + 10 min quiz)

---

## SEGMENT 1: Opening & Hook (8 min)

### Hook (3 min)

**Ask**: "How many of you have used Excel or Google Sheets?" [Hands go up]

**Ask**: "What if Python could load that spreadsheet in one line and run calculations on thousands of rows instantly — faster than Excel?"

**Reveal**: "That's exactly what we're doing today. Two libraries — NumPy and Pandas — are what every data scientist uses daily. By the end of this session, you will load a real dataset, inspect it, and pull out exactly the rows and columns you need."

### Why This Matters (5 min)

**Connect**: "Last session we wrote Python functions and worked with lists. Today we upgrade those tools for real data work."

| Library | What it does |
|---|---|
| NumPy | Fast numerical arrays — math on large data |
| Pandas | Labeled tables — load, inspect, filter CSVs |

**Today's Promise**: "By the end, you will load a real CSV, understand its shape, and select specific data from it."

---

## SEGMENT 2: NumPy Arrays (13 min)

### What is an Array? (4 min)

**Say**: "A NumPy array is like a Python list — but built only for numbers, and much faster."

**Show**:
```python
import numpy as np

scores = np.array([85, 92, 78, 95, 88])
print(scores)
print(type(scores))
```
Output:
```
[85 92 78 95 88]
<class 'numpy.ndarray'>
```

**Break it down**:
- `import numpy as np` = load the library, nickname it `np`
- `np.array([...])` = convert a list into a NumPy array

### Vectorized Operations (5 min)

**Ask**: "With a Python list, how would you add 10 to every element?" [Students say: a for loop]

**Show — list way**:
```python
scores_list = [85, 92, 78]
result = [s + 10 for s in scores_list]
```

**Show — NumPy way**:
```python
scores = np.array([85, 92, 78])
print(scores + 10)
print(np.mean(scores))
```
Output:
```
[95 102 88]
85.0
```

**Say**: "One operation, whole array. No loop. This is called a **vectorized operation**. On a million numbers, this is 100x faster than a list."

**Important**:
```python
# Right
nums = np.array([1, 2, 3])

# Watch out — mixing types
mixed = np.array([1, 2, "three"])
print(mixed)   # ['1' '2' 'three'] — everything became a string
```

**Student try**: Create an array of 5 temperatures in Celsius. Multiply by 1.8 to convert to Fahrenheit. Print the result. **(2 min)**

### 2D Arrays and Shape (4 min)

**Say**: "Arrays can have rows and columns — like a table."

**Show**:
```python
grades = np.array([
    [85, 92],
    [90, 88],
    [70, 75]
])

print(grades.shape)
print(grades.reshape(2, 3))
```
Output:
```
(3, 2)
[[85 92 90]
 [88 70 75]]
```

**Break it down**:
- `.shape` = (rows, columns)
- `.reshape(r, c)` = rearrange — total elements must stay the same (3×2 = 2×3 = 6)

---

## SEGMENT 3: Pandas Series and DataFrame (13 min)

### Series — One Column (4 min)

**Say**: "Pandas is built on top of NumPy. It adds labels — column names and row indices — so data looks and behaves like a spreadsheet."

**Say**: "A **Series** is one labeled column of data."

**Show**:
```python
import pandas as pd

city_temps = pd.Series(
    [28, 32, 25],
    index=["Bangalore", "Chennai", "Mumbai"]
)
print(city_temps)
print(city_temps["Chennai"])
```
Output:
```
Bangalore    28
Chennai      32
Mumbai       25
dtype: int64
32
```

### DataFrame — Full Table (5 min)

**Say**: "A **DataFrame** is multiple Series side by side — one per column. This is your spreadsheet in Python."

**Show**:
```python
data = {
    "name":  ["Ananya", "Rohan", "Priya"],
    "age":   [22, 25, 23],
    "score": [88, 91, 79]
}

df = pd.DataFrame(data)
print(df)
```
Output:
```
     name  age  score
0  Ananya   22     88
1   Rohan   25     91
2   Priya   23     79
```

**Break it down**:
- Dictionary keys → column names
- Lists → column values
- Pandas assigns a numeric index (0, 1, 2) automatically

### Series vs DataFrame (4 min)

**Show**:
```python
print(type(df["score"]))   # Series  — one column
print(type(df))            # DataFrame — whole table
```

**Say**: "Selecting one column gives you a Series. The full table is a DataFrame. You'll use both constantly."

**Student try**: Build a DataFrame with 3 rows and columns `city`, `population`, `avg_temp`. Print it. **(2 min)**

---

## SEGMENT 4: Loading a CSV (12 min)

### Read CSV (5 min)

**Say**: "In real work, data comes as files — most commonly CSV (comma-separated values). Pandas loads the whole thing in one line."

**Show**:
```python
import pandas as pd

url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = pd.read_csv(url)

print(df.shape)
```
Output:
```
(891, 12)
```

**Break it down**:
- `pd.read_csv()` = reads a CSV from a file path or URL
- `.shape` = (891 rows, 12 columns)

### Head and Tail (4 min)

**Say**: "Never print a full large dataset. Peek at it instead."

**Show**:
```python
print(df.head())     # First 5 rows
print(df.tail(3))    # Last 3 rows
```

**Say**: "Pass a number to control how many rows you see. Default is 5."

### Info (3 min)

**Show**:
```python
df.info()
```
Output (abbreviated):
```
RangeIndex: 891 entries
 #   Column       Non-Null Count  Dtype
 0   PassengerId  891 non-null    int64
 1   Survived     891 non-null    int64
 4   Age          714 non-null    float64  ← missing values
```

**Say**: "`.info()` tells you column names, data types, and which columns have missing data — `Age` has only 714 of 891 filled. This is always your first check on a new dataset."

**Student try**: Load the CSV. Print `.shape`. Run `.info()` and identify one column with missing values. **(2 min)**

---

## — 5-MINUTE BREAK —

---

## SEGMENT 5: Selecting Columns and Rows (13 min)

### Selecting Columns (5 min)

**Say**: "Most of the time you don't want the whole table — just specific columns."

**Show**:
```python
# Single column — returns a Series
ages = df["Age"]
print(ages.head())

# Multiple columns — returns a DataFrame
subset = df[["Name", "Age", "Survived"]]
print(subset.head())
```

**Important**:
```python
df["Age"]              # Single brackets → Series
df[["Age", "Pclass"]]  # Double brackets → DataFrame
```

**Say**: "One pair of brackets for one column. Two pairs for multiple. This trips up beginners — remember: more columns need the inner list."

### Selecting Rows with .iloc (5 min)

**Say**: "`.iloc` selects rows and columns by position — like list indexing."

**Show**:
```python
print(df.iloc[0])        # First row
print(df.iloc[0:3])      # Rows 0, 1, 2
print(df.iloc[0:3, 0:3]) # Rows 0-2, Columns 0-2
```

**Break it down**:
- `iloc[row, column]` — both use position numbers
- Omit the column part to get all columns

### Selecting Rows with .loc (3 min)

**Say**: "`.loc` selects by label — column name instead of position number."

**Show**:
```python
print(df.loc[0:2, ["Name", "Age", "Survived"]])
```
Output:
```
                          Name   Age  Survived
0  Braund, Mr. Owen Harris   22.0         0
1  Cumings, Mrs. John...    38.0         1
2  Heikkinen, Miss. Laina   26.0         1
```

**Student try**: Select columns `Name` and `Pclass` using double brackets. Then use `.iloc` to get the first 5 rows of those columns. **(2 min)**

---

## SEGMENT 6: Building Real Programs (20 min)

### Program 1: Array Statistics Report (5 min)

**Say**: "A function that takes any list of numbers and prints a clean summary."

```python
import numpy as np

def array_summary(data):
    arr = np.array(data)
    print("Values :", arr)
    print("Shape  :", arr.shape)
    print("Mean   :", np.mean(arr))
    print("Max    :", np.max(arr))
    print("Min    :", np.min(arr))

exam_scores = [72, 88, 95, 60, 81, 77, 90]
array_summary(exam_scores)
```
Output:
```
Values : [72 88 95 60 81 77 90]
Shape  : (7,)
Mean   : 80.43
Max    : 95
Min    : 60
```

### Program 2: CSV Quick Inspector (7 min)

**Say**: "A function you can point at any CSV to immediately understand what's in it."

```python
import pandas as pd

def inspect_csv(url):
    df = pd.read_csv(url)
    
    print("Shape:", df.shape)
    print("\nFirst 3 rows:")
    print(df.head(3))
    print("\nColumn info:")
    df.info()
    print("\nMissing values per column:")
    print(df.isnull().sum())
    
    return df

url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
df = inspect_csv(url)
```

**Note**: `df.isnull().sum()` counts missing values per column — one new line, worth knowing now.

### Program 3: Column Selector and Slicer (8 min)

**Say**: "A function that loads a CSV, selects specific columns, and returns a clean slice."

```python
import pandas as pd

def slice_dataset(url, columns, n_rows=10):
    df = pd.read_csv(url)
    
    print(f"Full dataset: {df.shape}")
    
    selected = df[columns]
    sliced = selected.iloc[0:n_rows]
    
    print(f"Selected {len(columns)} columns, {n_rows} rows")
    print(sliced)
    
    return sliced

url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/titanic_train.csv"
result = slice_dataset(url, ["Name", "Age", "Pclass", "Survived"], n_rows=5)
```
Output:
```
Full dataset: (891, 12)
Selected 4 columns, 5 rows
                          Name   Age  Pclass  Survived
0  Braund, Mr. Owen Harris   22.0       3         0
1  Cumings, Mrs. John...    38.0       1         1
...
```

---

## SEGMENT 7: Common Mistakes & Wrap (10 min)

### Common Mistakes (7 min)

**Mistake 1 — Single brackets for multiple columns**
```python
# Wrong
df["Name", "Age"]        # KeyError

# Right
df[["Name", "Age"]]      # Double brackets
```

**Mistake 2 — Reshape with wrong total**
```python
# Wrong
np.array([1,2,3,4,5]).reshape(2,3)  # 5 ≠ 2×3 — ValueError

# Right
np.array([1,2,3,4,5,6]).reshape(2,3)  # 6 = 2×3
```

**Mistake 3 — Mixing types in an array**
```python
# Watch out
np.array([1, 2, "three"])   # All become strings silently

# Right
np.array([1, 2, 3])         # Keep one type
```

**Mistake 4 — Forgetting .head() on large data**
```python
# Wrong — prints 891 rows to screen
print(df)

# Right — see a clean preview
print(df.head())
```

**Mistake 5 — Confusing .iloc and .loc**
```python
# .iloc — position numbers
df.iloc[0:3, 0:2]

# .loc — labels
df.loc[0:2, ["Name", "Age"]]
# Note: .loc includes the end index (0:2 gives rows 0, 1, 2)
# .iloc excludes the end index (0:3 gives rows 0, 1, 2)
```

### Session Recap (3 min)

| Topic | Key Tool | Key Syntax |
|---|---|---|
| Create array | NumPy | `np.array([...])` |
| Array math | Vectorized ops | `arr + 10`, `np.mean(arr)` |
| Array shape | Shape/Reshape | `.shape`, `.reshape(r,c)` |
| One column | Pandas Series | `pd.Series([...])` |
| Full table | Pandas DataFrame | `pd.DataFrame({...})` |
| Load file | Read CSV | `pd.read_csv(url)` |
| Inspect data | Head/Info | `.head()`, `.info()` |
| Select columns | Bracket notation | `df[["col1","col2"]]` |
| Select rows | iloc / loc | `.iloc[0:5]`, `.loc[0:2, ["col"]]` |