# Lecture Script: File Handling, JSON & APIs
> **Instructor Reference** — Module 1: Foundations of Data | Session 8 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students read and write files safely with context managers, parse and produce JSON (including nested structures), and make HTTP requests to live APIs with proper error handling and ethical practice.

**Student profile at this point:** Comfortable with lists, dicts, and nesting from Session 7. Ready to connect in-memory structures to disk and the web.

**Key outcome:** Each student completes an end-to-end pipeline — load a JSON config from disk, call a public weather API, parse the nested JSON response, save results to a file, and handle at least one error case gracefully.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| **SEGMENT 1:** Opening & Hook | 8 min | 0:08 |
| **SEGMENT 2:** File I/O & Context Managers | 12 min | 0:20 |
| **SEGMENT 3:** File I/O Lab — Read, Write, Append | 18 min | 0:38 |
| **SEGMENT 4:** JSON Basics — loads/dumps/load/dump | 15 min | 0:53 |
| **SEGMENT 5:** Nested JSON & Flattening | 12 min | 1:05 |
| **BREAK** | 10 min | 1:15 |
| **SEGMENT 6:** HTTP, APIs & Live Open-Meteo Demo | 22 min | 1:37 |
| **SEGMENT 7:** Status Codes, Keys, safe_api_call & Pipeline | 23 min | 2:00 |
| **SEGMENT 8:** Quiz, Homework, FAQ & Instructor Notes | 15 min | 2:15 |

*Strict 2-hour slot: trim SEGMENT 8 quiz to take-home; keep live API demo (SEGMENT 6) protected.*

---


## SEGMENT 1: Opening & Hook (8 min)

### Hook (3 min)

**Say:** *"Yesterday you built a product catalog in memory. What happens when you close Colab? It's gone. What happens when a weather app shows tomorrow's forecast? It called an API and got JSON back. Today we solve both — persisting data to disk and fetching it from the web."*

**Ask:** *"Who tried the `with open(...)` example from the pre-read?"* [Show of hands]

**Ask:** *"Name one app on your phone that must load data from the internet every time you open it."* [Weather, maps, social feeds — all JSON over HTTP]

### Three Skills, One Session (3 min)

| Skill | Tool | Real-world use |
|---|---|---|
| Files | `open()`, `with`, `pathlib` | Configs, logs, datasets |
| JSON | `json.load`, `json.dump` | API responses, settings |
| APIs | `requests.get`, `requests.post` | Live weather, payments, LLMs |

**Say:** *"Every CSV you will load in Pandas and every ChatGPT call in Module 3 follows today's pattern: open → read → structure → process."*

### Learning Contract (2 min)

By the end of this session, every student will:

1. Read and write text files using context managers
2. Parse and write JSON files with all four `json` functions
3. Navigate nested API-style JSON safely with `.get()`
4. Make a live GET request to Open-Meteo and save the forecast
5. Use `safe_api_call` with retry logic and never hardcode API keys

**Say:** *"You cannot break Colab. Run cells, read errors, fix, rerun. File and network errors are normal — handling them is the job."*

---


## SEGMENT 2: File I/O & Context Managers (12 min)

### The Mental Model (3 min)

**Draw on board:**

```
Disk (file)  ──open()──►  Memory (Python string/list)  ──process──►  Disk (updated file)
```

**Say:** *"A file on disk is permanent. A variable in RAM disappears when the program ends. File I/O is the bridge."*

### File Modes (3 min)

| Mode | Symbol | Behaviour |
|---|---|---|
| Read | `'r'` | Read existing file (default) |
| Write | `'w'` | Create or **overwrite** |
| Append | `'a'` | Add to end of existing file |

**Ask:** *"If I open `results.txt` with `'w'` when I meant to read it, what happens?"* → File is truncated to zero bytes immediately.

### Why `with` Beats Manual open/close (3 min)


### Manual open/close vs context manager

```python
# BAD — if an error occurs before close(), file may stay locked
f = open('data.txt', 'r')
content = f.read()
# ... bug here ...
f.close()   # may never run

# GOOD — context manager closes automatically
with open('data.txt', 'r') as f:
    content = f.read()
# file is closed here, even if an error occurred inside the block
```

**Output:**
```
Alice
Bob
Charlie
(same content either way if no crash — but only `with` closes on error)
```

**Break it down:**
- `open(path, mode)` returns a file object tied to the OS
- `f.read()` loads the entire file into one string
- `with` calls `f.close()` automatically when the block exits — success or crash
- In professional code, `with open(...) as f` is the standard

**Ask:** *"In professional code, is manual `f.close()` acceptable?"* → Only in tiny scripts; `with` is expected everywhere.

**Common mistake:** Opening with `'w'` by mistake when you meant `'r'` — the file is wiped before you read anything. Always double-check the mode letter.

### Three Ways to Read (3 min)

| Method | Returns | Best for |
|---|---|---|
| `f.read()` | One string with everything | Small files |
| `f.readlines()` | List of strings (with `\n`) | Index-based line access |
| `for line in f` | One line at a time | Large files, memory efficient |


### Three read methods compared

```python
with open('data.txt', 'r') as f:
  entire = f.read()

with open('data.txt', 'r') as f:
  lines = f.readlines()

with open('data.txt', 'r') as f:
  for line in f:
    print(line.strip())
```

**Output:**
```
Line one
Line two
Line three
(one line per iteration, no trailing newline after strip)
```

**Break it down:**
- `read()` — one big string, including `\n` characters
- `readlines()` — list where each element is one line
- `for line in f` — lazy iteration; best for large log files
- `strip()` removes leading/trailing whitespace and the newline

**Ask:** *"Which method would you use on a 2 GB log file?"* → `for line in f` — never load 2 GB into one string.

**Common mistake:** Using `read()` on a huge file and running out of memory — always iterate line by line for large files.

### File Paths — `pathlib` (3 min)

**Say:** *"Never hardcode `C:\\Users\\...` — it breaks on Mac and Linux. Use `pathlib.Path`."*


### Portable paths with pathlib

```python
from pathlib import Path

data_dir = Path('data')
data_dir.mkdir(exist_ok=True)
file_path = data_dir / 'scores.txt'

print(file_path)
print(file_path.exists())
```

**Output:**
```
data/scores.txt
False
```

**Break it down:**
- `Path('data')` creates a path object — portable across OS
- `mkdir(exist_ok=True)` creates the folder if missing
- `/` operator joins path parts — cleaner than string concatenation
- `.exists()` checks whether the file is on disk before opening

**Ask:** *"Why is `Path` better than `'data' + '/' + 'scores.txt'`?"* → Correct separators on Windows vs Mac automatically.

**Common mistake:** Forgetting `mkdir` before writing — `FileNotFoundError` when parent folder does not exist. Call `path.parent.mkdir(parents=True, exist_ok=True)`.


---


## SEGMENT 3: File I/O Lab — Read, Write, Append (18 min)

**Say:** *"We build a mini data folder from scratch — the same pattern every ML project uses for inputs and outputs."*

### Setup — Create Sample Data (4 min)


### Create sample CSV on disk

```python
from pathlib import Path

Path('data').mkdir(exist_ok=True)

sample_lines = [
    "Product,Price,Category\n",
    "Laptop,65000,Tech\n",
    "Mouse,899,Tech\n",
    "Desk,12000,Furniture\n",
]

with open('data/products.csv', 'w') as f:
    f.writelines(sample_lines)

print("Created data/products.csv")
```

**Output:**
```
Created data/products.csv
```

**Break it down:**
- `Path('data').mkdir(exist_ok=True)` ensures the folder exists
- Each string in the list ends with `\n` — CSV row per line
- `'w'` mode creates the file or overwrites if it already exists
- `writelines()` writes every string in the list without adding extra newlines

**Ask:** "What mode would you use to add one more product without deleting the file?" → append mode ('a').

**Common mistake:** Forgetting `\n` at the end of each line — all rows run together on one line. CSV needs newline separators.

### Read Entire File (3 min)


### Read entire file with read()

```python
with open('data/products.csv', 'r') as f:
    content = f.read()

print(content)
print(f"Characters read: {len(content)}")
```

**Output:**
```
Product,Price,Category
Laptop,65000,Tech
Mouse,899,Tech
Desk,12000,Furniture

Characters read: 72
```

**Break it down:**
- `'r'` mode opens for reading — default if omitted
- `read()` returns the full file as one string
- `len(content)` counts characters including newlines

**Ask:** *"How many lines are in this file?"* → Four — header plus three products (count `\n`).

**Common mistake:** Opening `products.csv` with `'w'` before reading — file becomes empty. Read first, write later.

### Read Line by Line — Memory Efficient (4 min)


### Iterate lines with enumerate

```python
with open('data/products.csv', 'r') as f:
    for i, line in enumerate(f):
        clean = line.strip()
        if i == 0:
            print(f"Header: {clean}")
        else:
            print(f"Row {i}: {clean}")
```

**Output:**
```
Header: Product,Price,Category
Row 1: Laptop,65000,Tech
Row 2: Mouse,899,Tech
Row 3: Desk,12000,Furniture
```

**Break it down:**
- `enumerate(f)` gives index `i` and line content together
- `strip()` removes the trailing `\n` for clean printing
- `i == 0` treats the first line as a header — common CSV pattern

**Ask:** *"Why is `enumerate` useful here instead of a manual counter?"* → Cleaner; index starts at 0 automatically.

**Common mistake:** Not calling `strip()` — output has blank lines or trailing `\n` characters that break string comparisons.

### Write Results to a New File (3 min)


### Write summary text file

```python
summary = [
    "Session 8 Lab Results\n",
    "Products loaded: 3\n",
    "Status: success\n",
]

with open('data/run_summary.txt', 'w') as f:
    f.writelines(summary)

print("Wrote data/run_summary.txt")
```

**Output:**
```
Wrote data/run_summary.txt
```

**Break it down:**
- A list of strings is a simple report format
- `'w'` creates `run_summary.txt` or overwrites an old version
- Check the file in Colab: folder icon → `data` → `run_summary.txt`

**Ask:** "If you run this cell twice, does the file grow or get replaced?" → Replaced — write mode ('w') overwrites.

**Common mistake:** Using `'a'` when you meant to start fresh — old content remains at the top. Use `'w'` for a clean report.

### Append to a Log File (4 min)


### Append timestamped log entry

```python
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open('data/run_log.txt', 'a') as f:
    f.write(f"[{timestamp}] Lab completed successfully\n")

with open('data/run_log.txt', 'r') as f:
    print(f.read())
```

**Output:**
```
[2026-06-25 14:32:01] Lab completed successfully
(run again → second line appended below)
```

**Break it down:**
- `'a'` append mode adds to the end without deleting existing lines
- `datetime.now().strftime(...)` formats the current time as text
- Logs grow over time — append is the correct mode for audit trails

**Ask:** *"When would you use append instead of write?"* → Logs, journals, anything that must keep history.

**Common mistake:** Using `'w'` for a log — every run erases previous entries. Logs almost always use `'a'`.

### Live Exercise — Student Log (3 min)

**Student try (3 min):** Write your name to `data/my_log.txt` in append mode, then read the file back.


### Student personal log exercise

```python
name = "Your Name Here"

with open('data/my_log.txt', 'a') as f:
    f.write(f"Student: {name}\n")

with open('data/my_log.txt', 'r') as f:
    print(f.read())
```

**Output:**
```
Student: Your Name Here
```

**Break it down:**
- Replace the name string with your actual name
- Append mode lets multiple students add lines without overwriting

**Ask:** "What file mode letter means append?" → 'a'.

**Common mistake:** Forgetting the newline `\n` — multiple entries run together on one line.

### FileNotFoundError Demo (2 min)


### Safe file open with exists check

```python
path = Path('data/products.csv')
if path.exists():
    with open(path, 'r') as f:
        print(f.read()[:100])
else:
    print(f"File not found: {path}")
```

**Output:**
```
Product,Price,Category
Laptop,65000,Tech
Mouse,899,Tech
Desk,12000,Furniture
(first 100 characters)
```

**Break it down:**
- Always check `path.exists()` before opening when the file might be missing
- `[:100]` slices the string to the first 100 characters for preview
- The `else` branch gives a friendly message instead of a crash

**Ask:** *"What error do you get if you skip the exists check and the path is wrong?"* → `FileNotFoundError`.

**Common mistake:** Typos in path — `data/product.csv` vs `data/products.csv`. Use `print(path.resolve())` to debug.


---


## SEGMENT 4: JSON Basics — loads/dumps/load/dump (15 min)

### Why JSON? (3 min)

**Say:** *"JSON looks almost exactly like Python dicts and lists. Every API, config system, and modern data export uses it."*

| JSON | Python |
|---|---|
| `"string"` | `str` |
| `number` | `int` or `float` |
| `array` | `list` |
| `object` | `dict` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### The Four JSON Functions (3 min)

| Function | Operates on | Direction |
|---|---|---|
| `json.loads(s)` | String | JSON string → Python |
| `json.dumps(obj)` | Python object | Python → JSON string |
| `json.load(f)` | File object | JSON file → Python |
| `json.dump(obj, f)` | Python + file | Python → JSON file |

**Memory trick:** `loads` = load from **s**tring. `dumps` = dump to **s**tring. `load`/`dump` work on **f**iles.

### Parse a JSON String (3 min)


### json.loads — string to dict

```python
import json

json_string = '{"name": "Riya", "score": 91, "passed": true}'
data = json.loads(json_string)
print(type(data))
print(data["name"])
print(data["passed"])
```

**Output:**
```
<class 'dict'>
Riya
True
```

**Break it down:**
- `json.loads()` parses a JSON **string** into a Python dict
- JSON `true` becomes Python `True` automatically
- Access values with dict syntax: `data['name']`

**Ask:** *"What function parses a string — `load` or `loads`?"* → `loads` — the **s** is for string.

**Common mistake:** Passing a Python dict to `json.loads()` — `TypeError`. Use `json.dumps()` to go the other way.

### Convert Python to JSON String (3 min)


### json.dumps — dict to string

```python
student = {"name": "Bob", "score": 88.5, "courses": ["Python", "SQL"]}
json_output = json.dumps(student, indent=2)
print(json_output)
```

**Output:**
```
{
  "name": "Bob",
  "score": 88.5,
  "courses": [
    "Python",
    "SQL"
  ]
}
```

**Break it down:**
- `json.dumps()` converts a Python object to a JSON **string**
- `indent=2` pretty-prints with 2-space indentation
- Python `True`/`False` become JSON `true`/`false` in the output

**Ask:** *"What does `indent=2` do?"* → Makes the JSON human-readable with line breaks.

**Common mistake:** Forgetting `import json` — `NameError: name json is not defined`. Always import at the top.

### JSON File Lab — Write Config (3 min)


### Write pipeline config JSON file

```python
import json
from pathlib import Path

config = {
    "project": "weather_pipeline",
    "version": "1.0",
    "cities": ["Mumbai", "Delhi", "Bangalore"],
    "settings": {
        "forecast_days": 7,
        "units": "celsius",
        "save_to_file": True
    },
    "output_path": "data/forecast_results.json"
}

Path('data').mkdir(exist_ok=True)
with open('data/config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Config written to data/config.json")
```

**Output:**
```
Config written to data/config.json
```

**Break it down:**
- `json.dump(obj, f)` writes Python objects directly to an open file
- Nested dicts (`settings`) serialize perfectly to nested JSON
- This mirrors real ML pipeline config files in production

**Ask:** *"Which function writes to a file — `dumps` or `dump`?"* → `dump` — needs a file object `f`.

**Common mistake:** Opening the file in `'w'` text mode but passing binary — rare issue; stick to `'w'` and `'r'` for JSON text files.

### Read Config Back (3 min)


### Read and inspect config JSON

```python
with open('data/config.json', 'r') as f:
    loaded_config = json.load(f)

print("Project:", loaded_config["project"])
print("Cities:", loaded_config["cities"])
print("Forecast days:", loaded_config["settings"]["forecast_days"])

for key, value in loaded_config.items():
    print(f"  {key}: {value}")
```

**Output:**
```
Project: weather_pipeline
Cities: ['Mumbai', 'Delhi', 'Bangalore']
Forecast days: 7
  project: weather_pipeline
  version: 1.0
  cities: ['Mumbai', 'Delhi', 'Bangalore']
  settings: {'forecast_days': 7, 'units': 'celsius', 'save_to_file': True}
  output_path: data/forecast_results.json
```

**Break it down:**
- `json.load(f)` reads and parses a JSON file in one step
- Nested access: `loaded_config['settings']['forecast_days']`
- `.items()` loops over all top-level key-value pairs

**Ask:** *"After `json.load`, what type is `loaded_config`?"* → `dict`.

**Common mistake:** Using `json.loads(f)` instead of `json.load(f)` — `loads` expects a string, not a file object.

### Session 7 Catalog as JSON (3 min)


### Catalog JSON round-trip

```python
catalog = [
    {"id": 1, "name": "Laptop", "price": 65000, "tags": ["tech", "sale"]},
    {"id": 2, "name": "Mouse",  "price": 899,   "tags": ["tech"]},
    {"id": 3, "name": "Desk",   "price": 12000, "tags": ["furniture"]},
]

with open('data/catalog.json', 'w') as f:
    json.dump(catalog, f, indent=2)

with open('data/catalog.json', 'r') as f:
    restored = json.load(f)

print(f"Loaded {len(restored)} products")
print(restored[0]["name"])
```

**Output:**
```
Loaded 3 products
Laptop
```

**Break it down:**
- A list of dicts round-trips perfectly through JSON
- Same structure as Session 7 in-memory catalog — now persistent
- `restored[0]['name']` proves nested list-of-dicts survived the save

**Ask:** *"Why save as JSON instead of a plain text file?"* → Structure preserved; no custom parsing.

**Common mistake:** Saving with `json.dump` but trying to read with `f.read()` — you get a raw string, not a dict. Use `json.load`.


---


## SEGMENT 5: Nested JSON & Flattening (12 min)

**Say:** *"Real API responses are deeply nested — objects inside lists inside objects. Session 7 nesting skills apply directly."*

### API-Style Weather Response (3 min)


### Nested weather API response structure

```python
weather_response = {
    "city": "Mumbai",
    "country": "IN",
    "weather": [
        {"main": "Clouds", "description": "scattered clouds"}
    ],
    "main": {
        "temp": 305.15,
        "feels_like": 310.2,
        "humidity": 78
    },
    "wind": {"speed": 5.1, "deg": 240}
}
```

**Output:**
```
(dict created in memory — no printed output yet)
```

**Break it down:**
- Top-level keys: `city`, `weather`, `main`, `wind`
- `weather` is a **list** containing one **dict**
- `main` is a **dict** inside the top-level dict — classic nesting

**Ask:** *"Is `weather` a list or a dict?"* → List — square brackets `[{...}]`.

**Common mistake:** Confusing `weather` (list) with `main` (dict) — `weather['main']` crashes; use `weather[0]['main']`.

### Layer-by-Layer Access (4 min)


### Navigate nested weather JSON

```python
print(weather_response["city"])
print(weather_response["main"]["temp"])
print(weather_response["weather"][0]["main"])

temp_c = weather_response["main"]["temp"] - 273.15
print(f"Temperature: {temp_c:.1f}°C")
```

**Output:**
```
Mumbai
305.15
Clouds
Temperature: 32.0°C
```

**Break it down:**
- `response['city']` — one level, simple key
- `response['main']['temp']` — two levels, chained keys
- `response['weather'][0]['main']` — list index then dict key
- Kelvin to Celsius: subtract 273.15 from API temperature

**Ask:** "What is the difference between top-level main dict vs weather[0][main]?" → Different keys at different nesting levels.

**Common mistake:** Using `weather['main']` instead of `weather[0]['main']` — `TypeError` because the list has no key `'main'`.

### Safe Access with `.get()` (3 min)


### Safe nested get with defaults

```python
# rain = weather_response['rain']['1h']   # KeyError if 'rain' missing!

rain = weather_response.get("rain", {}).get("1h", 0)
print(f"Rainfall: {rain} mm")
```

**Output:**
```
Rainfall: 0 mm
```

**Break it down:**
- `.get('rain', {})` returns `{}` if `'rain'` key is absent — no crash
- Chaining `.get('1h', 0)` on the empty dict returns default `0`
- Always assume API keys may be missing — weather varies by location

**Ask:** "Why not just use bracket access for rain?" → Crashes the whole pipeline if the key is missing.

**Common mistake:** `.get('rain', 0).get('1h', 0)` — if `rain` is missing you get int `0`, and `0.get()` crashes. Default must be `{}` for nested dict access.

### Flatten Nested Records (5 min)


### Flatten users and save JSON

```python
users = [
    {"id": 1, "name": "Alice", "address": {"city": "Mumbai",    "pin": "400001"}},
    {"id": 2, "name": "Bob",   "address": {"city": "Delhi",      "pin": "110001"}},
    {"id": 3, "name": "Cy",    "address": {"city": "Bangalore",  "pin": "560001"}},
]

flat_users = [
    {
        "id": u["id"],
        "name": u["name"],
        "city": u["address"]["city"],
        "pin": u["address"]["pin"],
    }
    for u in users
]

print(flat_users)

with open('data/users_flat.json', 'w') as f:
    json.dump(flat_users, f, indent=2)
```

**Output:**
```
[{'id': 1, 'name': 'Alice', 'city': 'Mumbai', 'pin': '400001'}, ...]
(file saved to data/users_flat.json)
```

**Break it down:**
- List comprehension loops over each user record
- Pull nested `address.city` up to the top level — **flattening**
- Flat list-of-dicts is ready for `pd.DataFrame(flat_users)` in Pandas
- Save flattened output to disk for the next pipeline stage

**Ask:** *"Why flatten before making a DataFrame?"* → Pandas wants flat columns, not nested dicts per cell.

**Common mistake:** Forgetting to flatten — `pd.DataFrame(users)` puts entire `address` dicts in one column. Flatten first.


**Pattern to memorise:** Fetch JSON → navigate/flatten nested fields → save or analyse.

---

## — 10-MINUTE BREAK —

*Prompt: "Think of one public API you use daily — weather, maps, payments. What data does it return? We'll call a real one after the break."*

---


## SEGMENT 6: HTTP, APIs & Live Open-Meteo Demo (22 min)

### The Request-Response Model (4 min)

**Draw on board:**

```
Your Python code                    Server
     │                                 │
     │── HTTP Request ────────────────►│
     │   GET /forecast?city=Mumbai     │
     │                                 │ (server looks up data)
     │◄── HTTP Response ───────────────│
         200 OK, JSON body
```

| Concept | Meaning | Example |
|---|---|---|
| URL / Endpoint | Address of the resource | `https://api.open-meteo.com/v1/forecast` |
| Method | What action to perform | `GET` (read), `POST` (send/create) |
| Status code | Did it work? | `200` OK, `404` Not Found |
| Params | Query string on GET URL | `?latitude=19.076&longitude=72.877` |

**Install check:** `pip install requests` — run before class if needed.

### First GET Request (4 min)


### Basic GET request to GitHub API

```python
import requests

response = requests.get(
    "https://api.github.com",
    timeout=10
)
print(response.status_code)
print(type(response.json()))
```

**Output:**
```
200
<class 'dict'>
```

**Break it down:**
- `requests.get(url, timeout=10)` sends an HTTP GET request
- `timeout=10` aborts if the server does not respond within 10 seconds
- `response.status_code` is an integer — 200 means success
- `response.json()` parses the response body as JSON into a dict

**Ask:** *"What type does `.json()` return?"* → Usually `dict`, sometimes `list`.

**Common mistake:** Calling `.json()` without checking status first — if the server returns HTML error page, parsing fails.

### GET vs POST (3 min)

| | GET | POST |
|---|---|---|
| Purpose | Read/fetch data | Send data to create or process |
| Data location | URL parameters | Request body (JSON) |
| Example | Weather forecast | Submit a form, call ChatGPT |
| Idempotent | Yes (safe to repeat) | No (may create duplicates) |


### POST demo with httpbin.org

```python
import requests

payload = {
    "city": "Mumbai",
    "query": "7-day forecast",
    "units": "celsius"
}

response = requests.post(
    "https://httpbin.org/post",
    json=payload,
    timeout=10
)

print(response.status_code)
print(response.json()["json"])
```

**Output:**
```
200
{'city': 'Mumbai', 'query': '7-day forecast', 'units': 'celsius'}
```

**Break it down:**
- `requests.post(url, json=payload)` sends JSON in the request body
- `json=payload` auto-sets `Content-Type: application/json`
- httpbin.org echoes back what you sent — perfect for classroom demos

**Ask:** *"Where does GET put data vs POST?"* → GET: URL params; POST: body.

**Common mistake:** Using `data=payload` instead of `json=payload` — sends form-encoded data, not JSON. Use `json=` for APIs.

### Live Demo — Open-Meteo Weather API (11 min)

**Say:** *"Open-Meteo is free, needs no API key, and returns nested JSON — perfect for class."*


### Open-Meteo GET request setup

```python
import requests

lat, lon = 19.076, 72.877  # Mumbai

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Asia/Kolkata",
    "forecast_days": 7
}

response = requests.get(url, params=params, timeout=10)
print("Status code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
```

**Output:**
```
Status code: 200
Content-Type: application/json; charset=utf-8
```

**Break it down:**
- `params` dict becomes the query string — requests encodes it safely
- No API key needed for Open-Meteo — zero setup friction
- Check `status_code` and `Content-Type` before parsing

**Ask:** *"What two parameters would change for Delhi?"* → latitude and longitude.

**Common mistake:** Hardcoding the full URL with `?lat=...&lon=...` manually — error-prone. Use the `params` dict.

### Parse Open-Meteo response structure

```python
if response.status_code == 200:
    data = response.json()
    print("Top-level keys:", list(data.keys()))
    print("Daily keys:", list(data["daily"].keys()))
else:
    print("Request failed:", response.status_code, response.text[:200])
```

**Output:**
```
Top-level keys: ['latitude', 'longitude', 'generationtime_ms', 'timezone', 'timezone_abbreviation', 'elevation', 'daily_units', 'daily']
Daily keys: ['time', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum']
```

**Break it down:**
- Always guard `.json()` with a status check
- `data['daily']` is a nested dict — parallel arrays for each field
- `response.text[:200]` shows error HTML/text if status is not 200

**Ask:** *"What shape is `data['daily']['time']`?"* → A list of date strings.

**Common mistake:** Assuming keys exist — always inspect `list(data.keys())` on a new API first.

### Flatten daily forecast loop

```python
daily = data["daily"]

forecast = []
for i in range(len(daily["time"])):
    forecast.append({
        "date": daily["time"][i],
        "max_temp_c": daily["temperature_2m_max"][i],
        "min_temp_c": daily["temperature_2m_min"][i],
        "rain_mm": daily["precipitation_sum"][i],
    })

for day in forecast:
    print(f"{day['date']}: {day['min_temp_c']:.0f}°C – {day['max_temp_c']:.0f}°C, rain {day['rain_mm']:.1f}mm")
```

**Output:**
```
2026-06-25: 28°C – 33°C, rain 2.4mm
2026-06-26: 27°C – 32°C, rain 0.0mm
... (7 days total)
```

**Break it down:**
- Parallel arrays share the same index `i` — classic API pattern
- Loop builds a flat list of dicts — same flattening skill from SEGMENT 5
- f-string formats temperature and rain for human-readable output

**Ask:** *"Why loop by index instead of zip?"* → Both work; index loop is explicit for beginners.

**Common mistake:** Mismatched array lengths — rare but would cause index errors. Always use `len(daily['time'])` as the loop bound.

### Save forecast JSON to disk

```python
output = {
    "city": "Mumbai",
    "lat": lat,
    "lon": lon,
    "fetched_at": "2026-06-25",
    "forecast": forecast
}

with open('data/mumbai_forecast.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Saved data/mumbai_forecast.json")
```

**Output:**
```
Saved data/mumbai_forecast.json
```

**Break it down:**
- Combine metadata (`city`, `lat`) with processed `forecast` list
- Write to disk — pipeline step: network → memory → disk
- Open the JSON file in Colab to verify pretty-printed output

**Ask:** *"What are the three storage locations we used today?"* → Disk, memory, network.

**Common mistake:** Forgetting `import json` at the top of the notebook — NameError when saving.


---


## SEGMENT 7: Status Codes, API Keys, safe_api_call & Pipeline Lab (23 min)

### Status Codes Students Must Know (4 min)

| Code | Meaning | What to do |
|---|---|---|
| 200 | OK — success | Parse `response.json()` |
| 401 | Unauthorised — bad/missing key | Check API key and headers |
| 404 | Not found — wrong URL | Check endpoint documentation |
| 429 | Rate limited — too many requests | Wait and retry with backoff |
| 500 | Server error | Retry; report to API provider |

**Say:** *"An API key is a password. Treat it like your bank PIN."*

### Never Hardcode API Keys (4 min)


### Load API key from environment

```python
# WRONG — this key lives in git history forever
# api_key = "sk-abc123secret"

# RIGHT — load from environment variable
import os
api_key = os.environ.get("MY_API_KEY")
print("Key loaded:", bool(api_key))
```

**Output:**
```
Key loaded: False
(False until you set the variable or use .env)
```

**Break it down:**
- Never paste real keys into notebook cells
- `os.environ.get()` returns `None` if the variable is unset — safe default
- In production: secrets managers, GitHub Actions secrets, Colab secrets

**Ask:** *"Where should API keys live?"* → Environment variables or `.env` — never source code.

**Common mistake:** Committing a notebook with a key cell to GitHub — key is public forever. Revoke and rotate immediately.

### Using `.env` with python-dotenv (3 min)


### dotenv load pattern

```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()   # reads .env file into environment
api_key = os.environ.get("MY_API_KEY", "not-set")
print("Key status:", "loaded" if api_key != "not-set" else "missing")
```

**Output:**
```
Key status: missing
(or 'loaded' if .env file exists with MY_API_KEY=...)
```

**Break it down:**
- `.env` file sits next to your script — `MY_API_KEY=your_key_here`
- Add `.env` to `.gitignore` **before** writing any key
- `load_dotenv()` loads variables into `os.environ` at runtime

**Ask:** "What file must never be pushed to GitHub?" → .env

**Common mistake:** Forgetting `.gitignore` — one `git push` exposes every key in the repo.

### POST with Authorization Header (3 min)


### POST with Bearer token pattern

```python
import requests
import os

api_key = os.environ.get("MY_API_KEY", "demo-key")
headers = {"Authorization": f"Bearer {api_key}"}
payload = {"model": "gpt-demo", "prompt": "Hello"}

# Pattern for real LLM APIs — demo URL only
# response = requests.post(url, headers=headers, json=payload, timeout=30)
print("Headers ready:", list(headers.keys()))
```

**Output:**
```
Headers ready: ['Authorization']
```

**Break it down:**
- Bearer token goes in the `Authorization` header — not the URL
- `json=payload` sends the prompt/body as JSON
- Module 3 GenAI uses this exact pattern for OpenAI and similar APIs

**Ask:** *"For ChatGPT-style APIs, is the call GET or POST?"* → POST.

**Common mistake:** Putting the API key in the URL query string — visible in logs and browser history. Use headers.

### safe_api_call with Retry Logic (6 min)


### safe_api_call helper function

```python
import requests
import time

def safe_api_call(url, params=None, headers=None, method="GET", json_body=None, retries=3):
    """Call an API with retry logic, timeout, and error handling."""
    for attempt in range(retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=10)
            else:
                response = requests.post(url, params=params, headers=headers,
                                         json=json_body, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait}s (attempt {attempt + 1}/{retries})...")
                time.sleep(wait)
            elif response.status_code == 401:
                print("Authentication failed. Check your API key.")
                return None
            else:
                print(f"HTTP {response.status_code}: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            time.sleep(2 ** attempt)
        except requests.exceptions.ConnectionError:
            print(f"Connection error on attempt {attempt + 1}")
            time.sleep(2)

    print(f"Failed after {retries} attempts.")
    return None
```

**Output:**
```
(function defined — no output until called)
```

**Break it down:**
- Loop up to `retries` times — handles flaky networks
- `2 ** attempt` is exponential backoff: 1s, 2s, 4s on rate limits
- Returns parsed JSON on 200, `None` on failure — caller checks before using
- Catches `Timeout` and `ConnectionError` separately from HTTP errors

**Ask:** *"Why return `None` instead of raising an exception?"* → Caller decides whether to log, retry, or exit gracefully.

**Common mistake:** Retrying forever on 401 — authentication will never succeed. Return `None` immediately on 401.

### Good call with safe_api_call

```python
result = safe_api_call(
    "https://api.open-meteo.com/v1/forecast",
    params={"latitude": 19.076, "longitude": 72.877,
            "daily": "temperature_2m_max", "forecast_days": 3,
            "timezone": "Asia/Kolkata"}
)
if result:
    print("Success! Max temps:", result["daily"]["temperature_2m_max"])
```

**Output:**
```
Success! Max temps: [33.2, 32.1, 31.5]
(values vary by date)
```

**Break it down:**
- Always check `if result:` before accessing nested keys
- Same Open-Meteo endpoint — now wrapped in retry-safe helper
- Three-day forecast — shorter response for quick demos

**Ask:** *"What happens if all retries fail?"* → Function prints message and returns `None`.

**Common mistake:** Using `result['daily']` without checking `if result` — `TypeError` on `None`.

### Bad endpoint demo — 404 handling

```python
bad = safe_api_call(
    "https://api.open-meteo.com/v1/WRONG_ENDPOINT",
    params={"latitude": 19.076, "longitude": 72.877}
)
print("Bad call result:", bad)
```

**Output:**
```
HTTP 404: ...
Bad call result: None
```

**Break it down:**
- Wrong endpoint returns 404 — function prints status and returns `None`
- Demonstrates graceful failure — program does not crash
- Students see the difference between good and bad URLs live

**Ask:** *"What status code means wrong URL?"* → 404.

**Common mistake:** Letting a 404 crash the notebook — always wrap API calls in error handling.

### End-to-End Pipeline Lab (6 min)

**Say:** *"This is the session payoff: disk → config → network → JSON → disk."*


### Full end-to-end pipeline lab

```python
import json
import requests
from pathlib import Path

# 1. Load config
with open('data/config.json', 'r') as f:
    config = json.load(f)

# 2. City coordinate lookup
CITY_COORDS = {
    "Mumbai":    (19.076, 72.877),
    "Delhi":     (28.704, 77.102),
    "Bangalore": (12.972, 77.594),
}

city = config["cities"][0]
lat, lon = CITY_COORDS[city]

# 3. Fetch forecast
result = safe_api_call(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "forecast_days": config["settings"]["forecast_days"],
        "timezone": "Asia/Kolkata"
    }
)

# 4. Save if configured
if result and config["settings"]["save_to_file"]:
    output = {"city": city, "forecast": result["daily"]}
    Path('data').mkdir(exist_ok=True)
    with open(config["output_path"], 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Pipeline complete. Saved to {config['output_path']}")
else:
    print("Pipeline skipped — no result or save_to_file is False")
```

**Output:**
```
Pipeline complete. Saved to data/forecast_results.json
```

**Break it down:**
- Step 1: `json.load` reads config written in SEGMENT 4
- Step 2: lookup dict maps city name → coordinates
- Step 3: `safe_api_call` fetches live data with retry
- Step 4: `json.dump` writes results to path from config

**Ask:** *"How many of the four JSON functions did this pipeline use?"* → Two: `json.load` and `json.dump`.

**Common mistake:** Hardcoding city coordinates inside the API call instead of reading from config — breaks reproducibility.


**Student extension (if time):** Loop over all cities in `config["cities"]` and write a combined summary JSON.

---


## SEGMENT 8: Quiz, Homework, FAQ & Instructor Notes (15 min)

### Session Recap Table (2 min)

| Skill | Tool | Output |
|---|---|---|
| Read/write text files | `with open(...)`, `pathlib` | `data/products.csv`, logs |
| Parse and write JSON | `json.load`, `json.dump`, `.get()` | `data/config.json`, `catalog.json` |
| Navigate nested JSON | chained keys and indexes | flattened user records |
| Call a live API | `requests.get`, params, status codes | 7-day Mumbai forecast |
| Handle errors ethically | `safe_api_call`, `.env`, retry | robust pipeline |

**Say:** *"Next session: NumPy — numeric arrays at scale. But every CSV and API response follows today's open → read → structure → process pattern."*

---

### 10-Question Quiz (8 min)

**Instructions:** Answer individually (2 min each for first 5, then review as class). Instructor reads aloud or displays on slide.

**Q1.** What file mode would you use to add a line to a log without deleting existing content?
→ `'a'` (append)

**Q2.** What is the output type of `json.loads('{"a": 1}')`?
→ `dict`

**Q3.** Which function reads JSON from an open file object — `json.loads` or `json.load`?
→ `json.load`

**Q4.** How do you safely access a key that might be missing in a dictionary?
→ `.get('key', default)`

**Q5.** What HTTP method is typically used to **fetch** read-only data from an API?
→ GET

**Q6.** What status code means the request succeeded?
→ 200

**Q7.** What status code means the URL or endpoint was not found?
→ 404

**Q8.** Why should API keys never be hardcoded in source code?
→ They get committed to git and exposed publicly; use environment variables instead

**Q9.** In nested JSON `data["daily"]["time"][0]`, what does `[0]` access?
→ The first element of the `time` list

**Q10.** What does the `with` statement guarantee when opening a file?
→ The file is closed automatically when the block exits, even if an error occurs

**Scoring guide:** 8–10 = ready for NumPy; 5–7 = review JSON functions and file modes; below 5 = redo pre-read sections A–D before next session.

---

### Homework (2 min)

**Assignment:** Multi-City Weather Pipeline

1. Using `safe_api_call`, fetch a **3-day** forecast for **Delhi** and **Bangalore** (not just Mumbai).
2. Save all three cities to **one** JSON file: `data/all_cities_forecast.json`.
3. Structure:
```json
{
  "fetched_at": "2026-06-25",
  "cities": [
    {"name": "Mumbai", "forecast": [...]},
    {"name": "Delhi", "forecast": [...]},
    {"name": "Bangalore", "forecast": [...]}
  ]
}
```
4. Add a check: if the API returns non-200, write an error entry to `data/run_log.txt` (append mode) instead of crashing.
5. **Bonus:** Load cities from `data/config.json` instead of hardcoding names.

**Due:** Before Session 9 (NumPy). Submit notebook link or `data/` folder screenshot.

**Exit ticket (1 min):** Write the four JSON functions and what each does in one phrase each.

| Function | One-phrase answer |
|---|---|
| `json.loads` | Parse JSON string → Python |
| `json.dumps` | Python → JSON string |
| `json.load` | Read JSON file → Python |
| `json.dump` | Python → JSON file |

---

### FAQ — 12 Common Questions (3 min — assign as reference)

**Q1: What's the difference between `json.loads()` and `json.load()`?**
→ `loads` parses a JSON **string** already in memory. `load` reads from an open **file** object. Same for `dumps` vs `dump`.

**Q2: Can I use `requests` for POST APIs like OpenAI?**
→ Yes. `requests.post(url, headers={"Authorization": f"Bearer {key}"}, json={...})`. The OpenAI SDK wraps the same HTTP call.

**Q3: What happens if I open a file with `'w'` by mistake when I meant to read?**
→ The file is immediately truncated to zero bytes. Always double-check the mode.

**Q4: Why did we use Open-Meteo instead of OpenWeatherMap?**
→ No API key required — zero setup friction in a classroom. OpenWeatherMap is a good homework extension with a free tier key.

**Q5: Is it safe to put API keys in Colab secrets?**
→ Colab secrets are acceptable for personal notebooks. For team projects, use `.env` locally and a secrets manager in production.

**Q6: What's the difference between `response.text` and `response.json()`?**
→ `.text` is the raw string body. `.json()` parses that string into Python dict/list — only works if the body is valid JSON.

**Q7: Why use `pathlib` instead of string paths?**
→ `Path` handles Windows vs Mac separators, provides `.exists()`, `.mkdir()`, and `/` joining — fewer path bugs.

**Q8: What is exponential backoff?**
→ Waiting longer after each failed retry: 1s, 2s, 4s… Used when APIs return 429 (rate limited).

**Q9: Can JSON store Python tuples?**
→ No — `json.dump` converts tuples to JSON arrays (lists). Load them back as lists.

**Q10: What does `timeout=10` do in `requests.get`?**
→ Aborts the request if the server does not respond within 10 seconds — prevents your program hanging forever.

**Q11: How do I pretty-print JSON in the terminal?**
→ `print(json.dumps(data, indent=2))` or save with `json.dump(..., indent=2)`.

**Q12: What's the bridge to Module 3 (GenAI)?**
→ Every LLM API call is POST + JSON body + Bearer token — the same pattern as today's POST demo.

---

### Instructor Notes

**Pre-read alignment:**
- Session 8 pre-read covers sections A–H (files, JSON, APIs, ethics, pipeline). Open with *"What did you try from the pre-read?"* — do not re-teach every section verbatim.
- Focus live time on labs, live API demo, and `safe_api_call`.

**Network contingency:**
- If classroom Wi-Fi blocks external APIs, pre-cache an Open-Meteo response in `data/cached_forecast.json` and load from file while showing the live call in code.
- Test `requests.get("https://api.open-meteo.com/v1/forecast", ...)` from the room network before class.

**Timing protection:**
- SEGMENT 6 live API demo is the emotional high point — protect it even if SEGMENT 3 file lab runs long.
- SEGMENT 8 quiz can be shortened to 5 questions or assigned as take-home if strictly 2 hours.

**API keys:**
- Do not share personal keys in class. Demonstrate authenticated POST pattern with httpbin.org or a class-specific limited key.
- If a student accidentally commits a key, walk through revoke + `.gitignore` + `.env` setup immediately.

**Common student errors (watch for these live):**
- Forgetting `import json` or `import requests`
- Using `json.load(f)` without opening file in `'r'` mode
- Not checking `status_code` before `.json()`
- Hardcoding API keys in Colab cells
- `json.loads` vs `json.load` confusion — stop and draw the four-function table
- Using `weather['main']` when `weather` is a list — draw the nesting diagram

**Differentiation:**
- **Fast finishers:** Loop all cities in `config["cities"]`; add CSV export with manual `csv` module or Pandas preview; try OpenWeatherMap with a personal key.
- **Struggling students:** Pair with partner for file lab; provide pre-filled `data/config.json`; use cached JSON for API segment.

**Connection to upcoming sessions:**
- **Session 9 (NumPy):** Numeric arrays loaded from files — today's file I/O is the on-ramp.
- **Session 10–11 (Pandas):** `pd.read_csv()` and `pd.read_json()` wrap today's patterns.
- **Module 3 (GenAI):** LLM APIs = POST + JSON + Bearer token + error handling.

**Materials checklist:**
- [ ] Colab notebook template with `pip install requests python-dotenv`
- [ ] Pre-created `data/` folder structure in template
- [ ] Cached `data/cached_forecast.json` backup
- [ ] Slide or board diagram: request-response model
- [ ] Four JSON functions reference card
- [ ] HTTP status code cheat sheet (200, 401, 404, 429, 500)

**Assessment rubric for homework:**

| Criterion | Points |
|---|---|
| All 3 cities fetched with `safe_api_call` | 3 |
| Combined JSON structure correct | 2 |
| Error logged to `run_log.txt` on failure | 2 |
| Uses config file (bonus) | 1 |
| Code uses `with` and no hardcoded keys | 2 |

---

> **End of Session 8 Lecture Script** — File Handling, JSON & APIs
