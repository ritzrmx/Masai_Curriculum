# File Handling & JSON Processing
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>AI · Python · Git<br/>Loops · Logic · Math"]
    CURSES["<b>Current Session</b><br/><b>File Handling & JSON</b><br/><i>Shift:</i> Code meets real files<br/>File I/O · JSON<br/>Parsing · Nested data"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Core stack every AI engineer<br/>repeats daily"]
    RVAL["<b>Real-Life Value</b><br/>Load configs, datasets, and<br/>API responses in any project"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[scikit-learn · Statistics]</i><br/>Predictive models"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · Agents]</i><br/>Grounded AI products"]
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

- How Python reads and writes files — the mechanics behind every `open()` call
- What **JSON** is and why it is the universal language of data exchange
- How to **parse** a JSON string into Python dictionaries and lists
- How to navigate **nested JSON** — the kind every real API returns
- How file handling and JSON together power config files, logs, datasets, and API responses

---

## A. File I/O — Reading and Writing Files in Python

> 💡 **Analogy:** A book in a library sits on a shelf until someone borrows it, reads it, makes notes, and returns it. Python's file system works identically — a file sits on disk until your program **opens** it, does something with it, and **closes** it. Forgetting to close the book puts it in limbo.

**One-line definition:** **File I/O (Input/Output)** is the process of opening a file on disk, reading or writing its contents in memory, and closing it — using Python's built-in `open()` function.

```mermaid
flowchart LR
    DISK["File on disk\n(data.txt)"] -->|open()| MEM["Python reads into\nmemory (string/lines)"]
    MEM -->|process| CODE["Your code\nworks on the data"]
    CODE -->|write + close| DISK2["Updated file\non disk"]
```

**The three file modes:**

| Mode | Symbol | What it does | Use when |
|---|---|---|---|
| Read | `'r'` | Opens for reading (default) | Loading existing files |
| Write | `'w'` | Creates or overwrites the file | Saving new output |
| Append | `'a'` | Adds to the end of an existing file | Adding to logs |

**Two ways to open files — always prefer the second:**

```python
# Way 1: Manual open and close (risky — if code crashes, file stays open)
f = open('data.txt', 'r')
content = f.read()
f.close()

# Way 2: Context manager (always closes automatically, even on error)
with open('data.txt', 'r') as f:
    content = f.read()
# File is automatically closed here
print(content)
```

**The `with` statement is not optional in professional code.** It guarantees the file is closed no matter what happens — errors included.

**Three ways to read:**

```python
with open('data.txt', 'r') as f:
    entire_content = f.read()       # One big string

with open('data.txt', 'r') as f:
    all_lines = f.readlines()       # List of strings, one per line

with open('data.txt', 'r') as f:
    for line in f:                  # Memory-efficient: one line at a time
        print(line.strip())         # strip() removes the trailing \n
```

| Method | Returns | Best for |
|---|---|---|
| `f.read()` | One string with everything | Small files, full content needed |
| `f.readlines()` | List of strings | Iterating lines by index |
| `for line in f` | One line at a time | Large files, memory efficiency |

---

## B. Writing Files and File Paths

> 💡 **Analogy:** Writing to a file is like filling out a printed form — you are putting information into a permanent storage format that others (or your future self) can read later. Unlike a variable in memory, a file persists when the program closes.

**One-line definition:** Writing to a file means sending a string from Python's memory onto disk — `'w'` mode creates or overwrites, `'a'` mode appends to the end.

**Writing example:**

```python
# Writing a new file
results = ["Accuracy: 0.94\n", "Precision: 0.91\n", "Recall: 0.88\n"]

with open('model_results.txt', 'w') as f:
    f.writelines(results)  # Write all lines at once

# Or write line by line
with open('model_results.txt', 'w') as f:
    f.write("Accuracy: 0.94\n")
    f.write("Precision: 0.91\n")

# Appending to an existing log
with open('run_log.txt', 'a') as f:
    f.write("Run completed at 2025-03-01 14:32\n")
```

**File paths — absolute vs relative:**

| Type | Example | When to use |
|---|---|---|
| **Relative** | `'data/scores.txt'` | From the current working directory |
| **Absolute** | `'/Users/alice/project/data/scores.txt'` | Always works regardless of where script runs |

**Best practice for paths — use `pathlib`:**

```python
from pathlib import Path

# Portable, works on Windows, Mac, and Linux
data_path = Path('data') / 'scores.txt'
print(data_path)           # data/scores.txt

# Check if file exists before opening
if data_path.exists():
    with open(data_path, 'r') as f:
        print(f.read())
else:
    print("File not found!")
```

Never hardcode `'C:\\Users\\alice\\...'` — it breaks on every other machine.

---

## C. JSON — The Language of Data Exchange

> 💡 **Analogy:** When people from different countries need to communicate, they often use a common language (e.g., English). When programs on different machines — built in different languages — need to exchange data, they use **JSON**: a text format that every language can read and write.

**One-line definition:** **JSON (JavaScript Object Notation)** is a text format that represents structured data as key-value pairs and lists — readable by humans and parseable by virtually every programming language.

**JSON looks almost exactly like Python dictionaries and lists:**

```json
{
  "name": "Alice",
  "age": 28,
  "skills": ["Python", "SQL", "Pandas"],
  "address": {
    "city": "Mumbai",
    "pincode": "400001"
  },
  "is_active": true,
  "score": null
}
```

**Type mapping — JSON to Python:**

| JSON type | Python equivalent | Example |
|---|---|---|
| `string` | `str` | `"Alice"` |
| `number` | `int` or `float` | `28`, `3.14` |
| `array` | `list` | `["Python", "SQL"]` |
| `object` | `dict` | `{"city": "Mumbai"}` |
| `true` / `false` | `True` / `False` | `true` → `True` |
| `null` | `None` | `null` → `None` |

**The two core JSON operations in Python:**

```python
import json

# 1. json.loads() — parse a JSON STRING into Python objects
json_string = '{"name": "Alice", "age": 28, "skills": ["Python", "SQL"]}'
data = json.loads(json_string)
print(type(data))          # <class 'dict'>
print(data['name'])        # Alice
print(data['skills'][0])   # Python

# 2. json.dumps() — convert Python objects to a JSON STRING
student = {"name": "Bob", "score": 91.5, "passed": True}
json_output = json.dumps(student, indent=2)
print(json_output)
# {
#   "name": "Bob",
#   "score": 91.5,
#   "passed": true
# }
```

**Memory trick:** `loads` = Load from **S**tring. `dumps` = Dump to **S**tring.

---

## D. Reading and Writing JSON Files

> 💡 **Analogy:** `json.loads()` is like translating a letter written in French into English in your head. `json.load()` is like directly reading a French book — the translator (Python) reads the file and converts it all in one step.

**One-line definition:** `json.load()` reads a JSON file directly into Python objects; `json.dump()` writes Python objects directly to a JSON file — both handle the file + parsing in one combined step.

**The four JSON functions — a clear map:**

| Function | Operates on | Direction | Use |
|---|---|---|---|
| `json.loads(s)` | String | JSON → Python | Parse API response string |
| `json.dumps(obj)` | Python object | Python → JSON | Convert to JSON string |
| `json.load(f)` | File object | JSON file → Python | Read a `.json` file |
| `json.dump(obj, f)` | Python obj + file | Python → JSON file | Write to a `.json` file |

**File read/write examples:**

```python
import json

# --- Read a JSON file ---
with open('config.json', 'r') as f:
    config = json.load(f)          # Reads file + parses in one step

print(config['model_name'])        # Access like a normal dict

# --- Write a JSON file ---
results = {
    "experiment": "run_01",
    "accuracy": 0.94,
    "hyperparams": {"lr": 0.001, "epochs": 50}
}

with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)    # indent makes it human-readable
```

**Why save data as JSON instead of plain text?**

```mermaid
flowchart LR
    A["Plain text file\n'name: Alice, age: 28'"] -->|"custom parsing\n(fragile)"| B["Python dict"]
    C["JSON file\n{\"name\":\"Alice\",\"age\":28}"] -->|"json.load()\n(always works)"| D["Python dict"]
```

JSON gives you structure for free — no custom parsing required.

---

## E. Nested JSON — Navigating Real-World API Responses

> 💡 **Analogy:** A Russian nesting doll (matryoshka) has dolls inside dolls inside dolls. **Nested JSON** is the same — objects contain objects contain arrays contain objects. Knowing how to reach the innermost doll without getting confused is the core skill.

**One-line definition:** **Nested JSON** is JSON where values are themselves objects or arrays — requiring chained key and index access to reach deeply nested data, which is the standard format returned by real-world APIs.

**A realistic API response (weather API style):**

```python
response = {
    "city": "Mumbai",
    "country": "IN",
    "weather": [
        {
            "main": "Clouds",
            "description": "scattered clouds"
        }
    ],
    "main": {
        "temp": 305.15,
        "feels_like": 310.2,
        "humidity": 78
    },
    "wind": {
        "speed": 5.1,
        "deg": 240
    }
}
```

**Accessing nested values — layer by layer:**

```python
# Top level
print(response['city'])                    # "Mumbai"

# One level deep (dict inside dict)
print(response['main']['temp'])            # 305.15
print(response['wind']['speed'])           # 5.1

# Array inside top-level (list index + key)
print(response['weather'][0]['main'])      # "Clouds"
print(response['weather'][0]['description'])  # "scattered clouds"

# Convert temperature from Kelvin to Celsius
temp_c = response['main']['temp'] - 273.15
print(f"Temperature: {temp_c:.1f}°C")     # 32.0°C
```

**Safe access with `.get()` — prevents KeyError on missing keys:**

```python
# This crashes if 'rain' key doesn't exist
# rain = response['rain']['1h']  # KeyError!

# Safe approach: .get() returns None if key is absent
rain = response.get('rain', {}).get('1h', 0)
print(f"Rainfall: {rain} mm")    # 0 mm (no KeyError)
```

**Flattening a list of API records into a table:**

```python
# API returned a list of user records
users = [
    {"id": 1, "name": "Alice", "address": {"city": "Mumbai"}},
    {"id": 2, "name": "Bob",   "address": {"city": "Delhi"}},
    {"id": 3, "name": "Charlie", "address": {"city": "Bangalore"}}
]

# Extract specific fields into a flat list of dicts (ready for DataFrame)
flat_users = [
    {
        "id": u["id"],
        "name": u["name"],
        "city": u["address"]["city"]
    }
    for u in users
]

print(flat_users)
# [{'id': 1, 'name': 'Alice', 'city': 'Mumbai'}, ...]

# One step further — convert to Pandas DataFrame
import pandas as pd
df = pd.DataFrame(flat_users)
print(df)
```

This pattern — fetch JSON from an API, flatten the nested fields, load into a DataFrame — is one of the most frequently repeated patterns in all of data engineering and ML work.

---

## Practice Exercises

**1. Pattern Recognition**  
Given this JSON string: `'{"student": "Riya", "grades": {"math": 88, "science": 92, "english": 79}, "rank": 3}'`  
Write the Python code to: (a) parse it with `json.loads()`, (b) print Riya's science grade, (c) compute her average grade across all three subjects, (d) add a new key `"average"` with that value, and (e) write the updated dictionary to a file called `riya_report.json`.

**2. Concept Detective**  
A teammate runs the following code and gets an error: `KeyError: 'rainfall'`  
```python
data = {"temp": 32, "humidity": 70, "wind": {"speed": 12}}
print(data['rainfall'])
```  
Using section E, explain (a) why the error occurs, (b) how `.get()` would fix it, and (c) rewrite the line to safely return `0` if `'rainfall'` is missing.

**3. Real-Life Application**  
You receive a JSON file `orders.json` containing a list of orders:  
```json
[
  {"order_id": "O1", "customer": "Alice", "items": [{"product": "Laptop", "qty": 1, "price": 65000}]},
  {"order_id": "O2", "customer": "Bob",   "items": [{"product": "Chair",  "qty": 2, "price": 6000}]}
]
```  
Write the code to: (a) read the file with `json.load()`, (b) print each customer's name and total order value (qty × price per item), (c) save a summary `[{"order_id": ..., "total": ...}]` to a new file `order_totals.json`.

**4. Spot the Error**  
A student writes this code to log results to a file:  
```python
f = open('results.txt', 'w')
for score in [88, 92, 79]:
    f.write(f"Score: {score}\n")
# Program crashes here due to a different bug
f.close()  # This line never runs
```  
Using section A, identify (a) what happens to the file if `close()` is never reached, (b) how the `with` statement would prevent this, and (c) rewrite the code correctly.

**5. Planning Ahead**  
You are building a configuration system for an ML pipeline. The pipeline needs to store: model name, hyperparameters (learning rate, epochs, batch size), input data path, and output directory. Design the complete config as a Python dictionary, write it to `pipeline_config.json` with proper indentation, then write the code to load it back and print each setting using a loop over `config.items()`. Finally, add a safety check: if the `input_data_path` file does not exist, print a warning before the pipeline starts.

---

> ✅ **You're done!** You now know how to open, read, and write files safely using the `with` statement, and how to parse, navigate, and write JSON — the format that powers every config file, API response, and dataset export you will encounter. Next: **NumPy Foundations & Array Operations**, where you'll move from processing one value at a time to processing entire arrays of numbers in a single operation — the mathematical engine behind all of data science and ML.
