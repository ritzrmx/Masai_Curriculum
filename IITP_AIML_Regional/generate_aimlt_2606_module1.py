#!/usr/bin/env python3
"""Generate Module 1 session folders and content for IITP-AIMLT-2606."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCH = ROOT / "IITP-AIMLT-2606"
MODULE = BATCH / "Module 1- Foundations of Data"

SESSIONS = [
    {
        "num": 1,
        "folder": "Session 1- AI, ML & GenAI Landscape",
        "label": "AI, ML & GenAI Landscape",
    },
    {
        "num": 2,
        "folder": "Session 2- Python Fundamentals",
        "label": "Python Fundamentals",
    },
    {
        "num": 3,
        "folder": "Session 3- Control Flow & Decision Making",
        "label": "Control Flow & Decision Making",
    },
    {
        "num": 4,
        "folder": "Session 4- Loops, Iteration & Repetitive Logic",
        "label": "Loops, Iteration & Repetitive Logic",
    },
    {
        "num": 5,
        "folder": "Session 5- Master class- Numbers, Logic & Structure — The Mathematical Language of Data",
        "label": "Master class - Numbers, Logic & Structure",
    },
    {
        "num": 6,
        "folder": "Session 6- Writing Reusable Code with Functions",
        "label": "Writing Reusable Code with Functions",
    },
    {
        "num": 7,
        "folder": "Session 7- Python Data Structures",
        "label": "Python Data Structures",
    },
    {
        "num": 8,
        "folder": "Session 8- File Handling, JSON & APIs",
        "label": "File Handling, JSON & APIs",
    },
    {
        "num": 9,
        "folder": "Session 9- NumPy- Numerical Foundation",
        "label": "NumPy - Numerical Foundation",
        "copy_from": ROOT / "IITP-AIMLH-2605/Module 1- Foundations of Data/Session 8- NumPy Foundations & Array Operations",
        "copy_map": {
            "NumPy Foundations & Array Operations": "NumPy - Numerical Foundation",
            "Session 8": "Session 9",
            "NumPy & Array Operations": "NumPy: Numerical Foundation",
        },
    },
    {
        "num": 10,
        "folder": "Session 10- Pandas- Loading, Inspection & Filtering",
        "label": "Pandas - Loading, Inspection & Filtering",
        "copy_from": ROOT / "IITP-AIMLH-2605/Module 1- Foundations of Data/Session 9- Pandas- Data Loading & Selection",
        "copy_map": {
            "Pandas: Data Loading & Selection": "Pandas - Loading, Inspection & Filtering",
            "Pandas: Data Loading": "Pandas: Loading, Inspection & Filtering",
            "Session 9": "Session 10",
        },
    },
    {
        "num": 11,
        "folder": "Session 11- Pandas- Aggregation, Groupby & Merging",
        "label": "Pandas - Aggregation, Groupby & Merging",
        "copy_from": ROOT / "IITP-AIMLH-2605/Module 1- Foundations of Data/Session 10- Pandas- Cleaning & Aggregation",
        "copy_map": {
            "Pandas: Cleaning & Aggregation": "Pandas - Aggregation, Groupby & Merging",
            "Pandas: Cleaning": "Pandas: Aggregation, Groupby & Merging",
            "Session 10": "Session 11",
        },
    },
    {
        "num": 12,
        "folder": "Session 12- Data Visualization",
        "label": "Data Visualization",
    },
    {
        "num": 13,
        "folder": "Session 13- EDA & Business Thinking",
        "label": "EDA & Business Thinking",
        "copy_from": ROOT / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 13- EDA & Visual Storytelling",
        "copy_map": {
            "EDA & Visual Storytelling": "EDA & Business Thinking",
            "Visual Storytelling": "Business Thinking",
            "Session 13": "Session 13",
        },
    },
    {
        "num": 14,
        "folder": "Session 14- Master class- From Tables to Relationships - The Mathematics of Data Organisation",
        "label": "Master class - From Tables to Relationships",
        "copy_from": ROOT / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 11- Master class-From Tables to Relationships - The Mathematics of Data Organisation",
        "copy_map": {
            "Session 11": "Session 14",
        },
    },
    {
        "num": 15,
        "folder": "Session 15- SQL with MySQL Workbench",
        "label": "SQL with MySQL Workbench",
        "copy_from": ROOT / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 12- SQL for Analysis & Data Retrieval",
        "copy_map": {
            "SQL for Analysis & Data Retrieval": "SQL with MySQL Workbench",
            "Session 12": "Session 15",
        },
    },
    {
        "num": 16,
        "folder": "Session 16- Data Analysis with Spreadsheets",
        "label": "Data Analysis with Spreadsheets",
        "copy_from": ROOT / "IITP-AIMLH-2605/Module 1- Foundations of Data/Session 11- Excel Analysis & SQL Fundamentals",
        "copy_map": {
            "Excel Analysis & SQL Fundamentals": "Data Analysis with Spreadsheets",
            "Excel Analysis": "Data Analysis with Spreadsheets",
            "Session 11": "Session 16",
        },
    },
]


def adapt_text(text: str, mapping: dict[str, str]) -> str:
    for old, new in sorted(mapping.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return text


def copy_session_files(session: dict) -> None:
    src = session["copy_from"]
    dst = MODULE / session["folder"]
    dst.mkdir(parents=True, exist_ok=True)
    mapping = session.get("copy_map", {})
    label = session["label"]

    patterns = [
        ("pre-read: ", f"pre-read: {label}.md"),
        ("lecture-script: ", f"lecture-script: {label}.md"),
        ("coding-problem: ", f"coding-problem: {label}.md"),
    ]

    for prefix, out_name in patterns:
        matches = list(src.glob(f"{prefix}*"))
        if not matches:
            continue
        content = matches[0].read_text(encoding="utf-8")
        content = adapt_text(content, mapping)
        (dst / out_name).write_text(content, encoding="utf-8")


def write_file(folder: Path, kind: str, label: str, content: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{kind}: {label}.md").write_text(content.strip() + "\n", encoding="utf-8")


# --- Generated content for sessions without copy_from ---

def content_session_1() -> dict[str, str]:
    label = "AI, ML & GenAI Landscape"
    pre_read = f"""# AI, ML & GenAI Landscape
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- What **AI**, **ML**, and **GenAI** mean — in plain language, not buzzwords
- Real **industry examples** that show where each term applies
- The main **types of ML problems** (prediction, grouping, generation)
- How the **AI/ML ecosystem** fits together — data, models, apps, and people
- How to **map a business use case** to the right category before writing code

---

## A. Artificial Intelligence — The Big Umbrella

> 💡 **Analogy:** AI is like the entire **transport industry** — cars, buses, trains, and planes all move people, but they work in different ways. ML and GenAI are specific vehicles inside that industry.

**One-line definition:** **Artificial Intelligence (AI)** is any computer system designed to perform tasks that normally require human intelligence — like understanding language, recognising images, or making decisions.

```mermaid
flowchart TD
    AI["Artificial Intelligence<br/>Broad field"]
    ML["Machine Learning<br/>Learns from data"]
    GenAI["Generative AI<br/>Creates new content"]
    Rules["Rule-based systems<br/>If-then logic"]
    AI --> ML
    AI --> Rules
    ML --> GenAI
```

| Term | What it does | Example |
|---|---|---|
| AI | Mimics intelligent behaviour | Voice assistant, chess engine |
| ML | Learns patterns from data | Spam filter, price prediction |
| GenAI | Generates text, images, code | ChatGPT, image generators |

---

## B. Machine Learning — Learning From Data

> 💡 **Analogy:** Teaching a child to recognise fruits by showing hundreds of photos works better than listing rules like "if red and round, it's an apple." **ML** learns from examples instead of hand-written rules.

**One-line definition:** **Machine Learning (ML)** is a branch of AI where systems improve at a task by finding patterns in data — without being explicitly programmed for every case.

```mermaid
flowchart LR
    D[Historical data] --> T[Train model]
    T --> M[Trained model]
    N[New input] --> M
    M --> P[Prediction or insight]
```

| ML type | Has labels? | Goal | Example |
|---|---|---|---|
| Supervised | Yes | Predict known outcomes | Will customer churn? |
| Unsupervised | No | Find hidden structure | Customer segments |
| Reinforcement | Rewards | Learn best actions | Game-playing bots |

---

## C. Generative AI — Creating New Content

> 💡 **Analogy:** A **photocopier** copies what exists. A **GenAI** tool is more like a skilled writer who has read millions of books and can draft a new paragraph in your style — original output, trained on existing data.

**One-line definition:** **Generative AI (GenAI)** uses large models trained on vast text or media to **create** new content — answers, summaries, code, images — from a prompt.

| Traditional ML | GenAI |
|---|---|
| Predicts a number or category | Generates open-ended text or media |
| Needs structured training data | Trained on language or multimodal data |
| Output is fixed (0/1, price) | Output is flexible (paragraphs, code) |

---

## D. Mapping Use Cases to the Right Category

> 💡 **Analogy:** Before ordering food, you decide: dine-in, takeaway, or cook at home. Picking **AI vs ML vs GenAI** is the same — match the tool to the job.

**One-line definition:** **Problem framing** means naming what you want the system to do so you choose the right approach — rules, ML model, or GenAI assistant.

| Use case | Best fit | Why |
|---|---|---|
| Sort emails into folders with fixed rules | Rules / classic AI | Logic is known upfront |
| Predict next month's sales | ML (regression) | Pattern in historical numbers |
| Draft a customer support reply | GenAI | Open-ended language generation |
| Group shoppers by behaviour | ML (clustering) | No pre-defined labels |

```mermaid
flowchart TD
    Q{{What is the output?}}
    Q -->|Fixed rules| R[Rule-based system]
    Q -->|Number or category| M[Machine Learning]
    Q -->|New text or content| G[Generative AI]
```

---

## Practice Exercises

**1. Pattern Recognition** — For each item, label it AI, ML, or GenAI: (a) Netflix recommending shows, (b) a chatbot writing an email draft, (c) a thermostat following "if temp > 25, turn on AC."

**2. Concept Detective** — A startup wants to "use AI" to detect fraudulent credit card transactions. Which category fits best? What kind of ML problem is it?

**3. Real-Life Application** — List three jobs in your city that touch AI, ML, or GenAI. For each, say which term applies and one task they might do.

**4. Spot the Error** — Someone says: "We don't need ML — we'll just use ChatGPT to predict whether a loan should be approved." What is wrong with this plan?

**5. Planning Ahead** — Pick one app you use daily. Sketch whether it likely uses rules, ML, GenAI, or a mix — and what data it might need.

---

> ✅ **You're done!** You can now tell AI, ML, and GenAI apart and place real products in the right bucket. Next session you will write your first Python programs in Colab — the language everything else builds on.
"""
    lecture = f"""# Lecture Script: AI, ML & GenAI Landscape
> **Instructor Reference** — Module 1: Foundations of Data | Session 1 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students leave with a clear mental map of AI, ML, and GenAI — and can classify real use cases without jargon.

**Student profile:** Beginners; may have used ChatGPT but no formal CS background.

**Key outcome:** Every student can explain the three terms to a friend and pick the right approach for two business scenarios.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Icebreaker | 10 min | 0:10 |
| **Concept 1:** AI as the umbrella | 15 min | 0:25 |
| **Activity 1:** Sort the headlines — AI, ML, or GenAI? | 15 min | 0:40 |
| **Concept 2:** ML problem types | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** GenAI vs traditional ML | 15 min | 1:20 |
| **Activity 2:** Map use cases in pairs | 20 min | 1:40 |
| **Concept 4:** Roles and ecosystem | 10 min | 1:50 |
| Summary & course roadmap | 10 min | 2:00 |

---

## Opening (10 min)

**Hook:** Show three headlines (Netflix recommendations, ChatGPT essay, traffic light timing). Ask: *"Which is AI? Which is ML? Which is GenAI?"*

**Set context:** This course goes from Python basics → data → classical ML → GenAI agents. Today is the map of the territory.

---

## Concept Block 1: AI as the Umbrella (15 min)

Draw three nested circles on the board: AI ⊃ ML ⊃ Deep Learning / GenAI.

Emphasise: **AI is not one product** — it is a field. ML is the main path for data-driven prediction; GenAI is the newest wave for language and content.

---

## Activity 1: Sort the Headlines (15 min)

Hand out 8 cards: face unlock, fraud alert, DALL·E image, Excel formula, Spotify Discover Weekly, Siri weather, K-means customer segments, GitHub Copilot.

Pairs sort into: Rules / ML / GenAI. Debrief with reasoning.

---

## Concept Block 2: ML Problem Types (15 min)

| Type | Question | Output |
|---|---|---|
| Regression | How much? | Number |
| Classification | Which category? | Label |
| Clustering | What groups exist? | Segments |
| Generation | What should we create? | Text/media |

Use e-commerce examples: churn (classification), revenue (regression), segments (clustering).

---

## Concept Block 3: GenAI vs Traditional ML (15 min)

**Key line:** ML *scores* or *labels*; GenAI *composes*.

Discuss limits: GenAI can hallucinate; ML needs clean labelled data.

---

## Activity 2: Map Use Cases (20 min)

Scenarios: (1) HR resume screening, (2) inventory forecast, (3) FAQ chatbot, (4) anomaly detection.

Groups fill: Problem → AI/ML/GenAI → Supervised or not → What data is needed.

---

## Wrap-Up (10 min)

Show Module 1–3 roadmap on one slide. Preview Session 2: Python in Colab.

**Exit ticket:** One sentence each for AI, ML, GenAI.
"""
    coding = f"""# Coding Problem: AI, ML & GenAI Landscape
> **Session 1 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Scenario

You are onboarding as a junior analyst. Classify each project and ML problem type before any code is written.

---

## Tasks

**Task 1 — Basic**

Fill in the category for each (`AI`, `ML`, or `GenAI`):

```python
projects = {{
    "Email spam filter trained on labelled emails": "___",
    "Chatbot that drafts support replies from a prompt": "___",
    "Thermostat: if temp > 30, turn on AC": "___",
    "Recommend products based on purchase history": "___",
}}
for name, cat in projects.items():
    print(f"{{name}}: {{cat}}")
```

**Task 2 — Basic**

Mark each as `regression`, `classification`, or `unsupervised`:

```python
problems = {{
    "Predict house price": "___",
    "Detect fraud (yes/no)": "___",
    "Group customers by behaviour": "___",
    "Forecast daily sales": "___",
}}
for task, ptype in problems.items():
    print(f"{{task}}: {{ptype}}")
```

**Task 3 — Mid**

Write comments explaining your choice:

```python
# Scenario: A bank wants to predict loan default (yes/no) from applicant data.
# Best approach: ___ (ML / GenAI / Rules)
# ML problem type: ___
# Why not GenAI for the final decision? ___
```

---

## Expected Output

```
Email spam filter trained on labelled emails: ML
Chatbot that drafts support replies from a prompt: GenAI
Thermostat: if temp > 30, turn on AC: AI
Recommend products based on purchase history: ML

Predict house price: regression
Detect fraud (yes/no): classification
Group customers by behaviour: unsupervised
Forecast daily sales: regression
```

---

<details>
<summary>Solution</summary>

```python
projects = {{
    "Email spam filter trained on labelled emails": "ML",
    "Chatbot that drafts support replies from a prompt": "GenAI",
    "Thermostat: if temp > 30, turn on AC": "AI",
    "Recommend products based on purchase history": "ML",
}}
for name, cat in projects.items():
    print(f"{{name}}: {{cat}}")

problems = {{
    "Predict house price": "regression",
    "Detect fraud (yes/no)": "classification",
    "Group customers by behaviour": "unsupervised",
    "Forecast daily sales": "regression",
}}
for task, ptype in problems.items():
    print(f"{{task}}: {{ptype}}")

# Scenario: loan default prediction
# Best approach: ML
# ML problem type: classification
# Why not GenAI: need consistent, auditable yes/no from structured features;
# GenAI is not trained for regulated scoring on tabular applicant data.
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_2() -> dict[str, str]:
    label = "Python Fundamentals"
    pre_read = f"""# Python Fundamentals
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- How to **declare variables** and pick the right **data types**
- How **operators** let you compute and compare values
- How **input and output** connect your program to the user
- How **f-strings** format readable messages
- Good **Colab notebook habits** so your work stays organised

---

## A. Variables — Named Storage Boxes

> 💡 **Analogy:** A **variable** is like a labelled lunch box. You put food in, close the lid, and next time you open "Monday lunch," the same contents are there — unless you swap them.

**One-line definition:** A **variable** is a name that points to a value stored in memory.

```python
age = 25          # int
price = 19.99     # float
name = "Priya"    # str
is_student = True # bool
```

| Type | Example | Use when |
|---|---|---|
| int | 42 | Whole numbers |
| float | 3.14 | Decimals |
| str | "hello" | Text |
| bool | True, False | Yes/no flags |

---

## B. Operators — Doing Math and Comparisons

> 💡 **Analogy:** Operators are kitchen tools: **+** is a mixer, **>** is a taste test ("is this spicier than that?").

**One-line definition:** **Operators** are symbols that perform calculations or comparisons on values.

| Arithmetic | Comparison | Result type |
|---|---|---|
| + − * / | == != | number or bool |
| // % ** | < > <= >= | |

```mermaid
flowchart LR
    A[5 + 3] --> R1[8]
    B[10 > 7] --> R2[True]
```

---

## C. Input, Output, and f-strings

> 💡 **Analogy:** **print()** is announcing your order number. **input()** is the cashier asking your name. **f-strings** are name tags that auto-fill the details.

**One-line definition:** **Input/output** lets programs talk to users; **f-strings** embed variables inside text.

```python
name = input("Your name: ")
score = 87
print(f"Hello {{name}}, you scored {{score}}%")
```

---

## D. Colab Notebook Discipline

> 💡 **Analogy:** A notebook is a lab journal — one idea per cell, run in order, note what each experiment showed.

**Rules:**
- One logical step per cell
- Run cells top to bottom after changes
- Add a short markdown note above tricky cells
- Restart kernel if variables behave oddly

---

## Practice Exercises

**1. Pattern Recognition** — What type is each value: `3.0`, `"3.0"`, `3`, `True`?

**2. Concept Detective** — `print(10 / 4)` vs `print(10 // 4)` — why are the outputs different?

**3. Real-Life Application** — Name three values you'd store for a food delivery app order.

**4. Spot the Error** — `age = input("Age: ")` then `print(age + 1)` crashes. Why?

**5. Planning Ahead** — Write pseudocode for a tip calculator: ask bill amount, compute 15% tip, print total with f-string.

---

> ✅ **You're done!** Variables, types, and I/O are the atoms of every Python program. Next you will add **decisions** with if/elif/else.
"""
    lecture = f"""# Lecture Script: Python Fundamentals
> **Instructor Reference** — Module 1: Foundations of Data | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write and run Python in Colab using variables, types, operators, input/output, and f-strings.

**Key outcome:** Each student completes a mini "profile card" program that asks for name, age, and city and prints a formatted greeting.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Colab setup & first cell | 15 min | 0:15 |
| Variables & types live demo | 20 min | 0:35 |
| Operators & type inspection | 15 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| input(), print(), f-strings | 25 min | 1:25 |
| Lab: Profile card + tip calculator | 25 min | 1:50 |
| Summary & homework | 10 min | 2:00 |

---

## Live Demo Highlights

```python
x = 10
print(type(x))
print(f"Double is {{x * 2}}")

name = input("Name: ")
print(f"Welcome, {{name}}!")
```

Discuss: `input()` always returns a **string** — cast with `int()` when needed.

---

## Lab: Profile Card

Requirements: ask name, age, favourite language; print two lines using f-strings; show age in 5 years.

---

## Common Errors to Address

- NameError (typo in variable)
- TypeError (str + int)
- Forgetting quotes on strings
"""
    coding = f"""# Coding Problem: Python Fundamentals
> **Session 2 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Create variables and print their types:

```python
item = "Notebook"
qty = 3
price = 249.50
in_stock = True
# Print each value and its type
```

**Task 2 — Basic**

Compute and print (use f-strings):

```python
qty = 4
price = 125.0
# subtotal, 18% tax, grand total
```

**Task 3 — Mid**

Ask the user for item name and quantity; print a one-line order summary.

```python
item = input("Item: ")
qty = int(input("Quantity: "))
# Print: "Order: <qty>x <item>"
```

---

## Expected Output

```
Notebook <class 'str'>
3 <class 'int'>
249.5 <class 'float'>
True <class 'bool'>

Subtotal: 500.0
Tax: 90.0
Total: 590.0
```

*(Task 3 output depends on user input.)*

---

<details>
<summary>Solution</summary>

```python
item = "Notebook"
qty = 3
price = 249.50
in_stock = True
for v in [item, qty, price, in_stock]:
    print(v, type(v))

qty = 4
price = 125.0
sub = qty * price
tax = sub * 0.18
print(f"Subtotal: {{sub}}")
print(f"Tax: {{tax}}")
print(f"Total: {{sub + tax}}")

item = input("Item: ")
qty = int(input("Quantity: "))
print(f"Order: {{qty}}x {{item}}")
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_3() -> dict[str, str]:
    label = "Control Flow & Decision Making"
    pre_read = f"""# Control Flow & Decision Making
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- How **if / elif / else** run different code paths
- How **boolean logic** combines multiple conditions
- How **comparison operators** test values
- How to **trace nested conditions** and predict output
- How real apps use decisions (login, discounts, eligibility)

---

## A. The if Statement — One Fork in the Road

> 💡 **Analogy:** At a junction, if the light is green you go; otherwise you stop. **if** is that traffic decision for your code.

**One-line definition:** An **if statement** runs a block of code only when a condition is **True**.

```python
score = 72
if score >= 60:
    print("Pass")
else:
    print("Retake")
```

```mermaid
flowchart TD
    C{{score >= 60?}}
    C -->|Yes| P[Print Pass]
    C -->|No| F[Print Retake]
```

---

## B. elif and else — Multiple Branches

> 💡 **Analogy:** A menu with Veg / Non-veg / Dessert — pick **one** path. **elif** is the middle options.

```python
temp = 38
if temp > 40:
    print("Heatwave")
elif temp > 30:
    print("Hot")
else:
    print("Comfortable")
```

---

## C. Boolean Logic — AND, OR, NOT

> 💡 **Analogy:** Entering a club needs ID **and** age 18+. A sale applies if member **or** coupon. **NOT** flips yes to no.

| Operator | True when |
|---|---|
| A and B | Both true |
| A or B | At least one true |
| not A | A is false |

```python
age = 20
has_id = True
if age >= 18 and has_id:
    print("Entry allowed")
```

---

## D. Nested Conditions

> 💡 **Analogy:** Outer gate: ticket check. Inner gate: seat assignment. Each **nest** is another decision inside the previous one.

Trace carefully: only the inner block runs if the outer condition already passed.

---

## Practice Exercises

**1. Pattern Recognition** — What prints? `x=5` then `if x>3: print("A")` else `print("B")`

**2. Concept Detective** — Login needs email **and** password length ≥ 8. Write the condition in English, then Python.

**3. Real-Life Application** — List three apps that use if/else on your phone today.

**4. Spot the Error** — `if age = 18:` — why is this invalid?

**5. Planning Ahead** — Design grade bands: A ≥90, B ≥75, C ≥60, else F. Write pseudocode only.

---

> ✅ **You're done!** You can branch code like real products do. Next: **loops** for repeating actions without copy-paste.
"""
    lecture = f"""# Lecture Script: Control Flow & Decision Making
> **Instructor Reference** — Module 1: Foundations of Data | Session 3 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write if/elif/else with combined boolean conditions and trace nested logic.

**Key outcome:** Working "eligibility checker" (age, documents, income) and "grade calculator."

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Opening: why decisions matter | 10 min |
| if/else live coding | 25 min |
| elif chains + truth tables | 20 min |
| BREAK | 10 min |
| and/or/not + nested if | 25 min |
| Lab: loan eligibility | 25 min |
| Trace-the-output quiz + wrap | 5 min |

---

## Labs

1. **Grade bands** — elif chain
2. **Discount rules** — member OR coupon, not both stacked incorrectly
3. **Nested:** if country == "IN" and amount > 1000 → GST logic (simplified)

---

## Teaching tip

Use physical "true/false" cards for `and` vs `or` — students hold up hands.
"""
    coding = f"""# Coding Problem: Control Flow & Decision Making
> **Session 3 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Print ticket price: child (<12) = 100, adult = 200.

```python
age = 10
# your if/else here
```

**Task 2 — Basic**

```python
score = 78
# Print A if >=90, B if >=75, C if >=60, else F
```

**Task 3 — Mid**

Free shipping if `total >= 500` **and** `is_member`. Set variables and print message.

```python
total = 650
is_member = True
```

---

## Expected Output

```
100
B
Free shipping applied
```

---

<details>
<summary>Solution</summary>

```python
age = 10
print(100 if age < 12 else 200)

score = 78
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")

total = 650
is_member = True
if total >= 500 and is_member:
    print("Free shipping applied")
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_4() -> dict[str, str]:
    label = "Loops, Iteration & Repetitive Logic"
    pre_read = f"""# Loops, Iteration & Repetitive Logic
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- How **for loops** repeat over sequences
- How **while loops** repeat until a condition fails
- How **range()** generates number sequences
- When to use **break** and **continue**
- How to loop over **lists and strings** by index or item

---

## A. for Loops — Repeat for Each Item

> 💡 **Analogy:** Checking every bag on a conveyor belt — the loop **visits each bag once** without you naming them one by one.

```python
fruits = ["apple", "banana", "cherry"]
for f in fruits:
    print(f)
```

```mermaid
flowchart LR
    S[Start loop] --> I[Next item]
    I --> B[Do work]
    B --> I
    I --> E[End]
```

---

## B. while Loops — Repeat Until Done

> 💡 **Analogy:** Keep filling glasses while the jug has water. **while** checks the condition before each round.

```python
count = 3
while count > 0:
    print(count)
    count -= 1
```

---

## C. range(), break, continue

| Tool | Purpose |
|---|---|
| range(5) | 0,1,2,3,4 |
| break | Exit loop early |
| continue | Skip to next iteration |

```python
for i in range(5):
    if i == 3:
        continue
    print(i)
```

---

## D. Index vs Value

```python
names = ["Ana", "Bo", "Cy"]
for i in range(len(names)):
    print(i, names[i])
```

---

## Practice Exercises

**1. Pattern Recognition** — How many times does `for i in range(4): print(i)` print?

**2. Concept Detective** — You need to retry API calls until success or 5 failures. for or while?

**3. Real-Life Application** — Three daily tasks you repeat that map to loops.

**4. Spot the Error** — `while True: print("hi")` with no break — what happens?

**5. Planning Ahead** — Sum numbers 1 to 10 using a loop (pseudocode).

---

> ✅ **You're done!** Loops remove repetition from code. Next: a **master class** on the math behind logic and data structures.
"""
    lecture = f"""# Lecture Script: Loops, Iteration & Repetitive Logic
> **Instructor Reference** — Module 1: Foundations of Data | Session 4 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students use for/while, range, break/continue, and iterate lists/strings confidently.

**Key outcome:** Sum/average of a list, FizzBuzz-style exercise, password retry with while + break.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Why loops beat copy-paste | 10 min |
| for + range demos | 25 min |
| BREAK | 10 min |
| while + break/continue | 25 min |
| Nested loops intro | 15 min |
| Lab: stats on a list | 30 min |
| Wrap | 5 min |

---

## Lab highlights

- Print multiplication table for one number
- Sum only even numbers in a list
- Guess-the-number with while and break
"""
    coding = f"""# Coding Problem: Loops, Iteration & Repetitive Logic
> **Session 4 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Print squares of 1 through 5 using `for` and `range`.

**Task 2 — Basic**

```python
nums = [4, 7, 2, 9, 1]
# Print sum using a loop
```

**Task 3 — Mid**

Print only values > 5 from `nums`; stop early if sum exceeds 15 (use break).

---

## Expected Output

```
1 1
2 4
3 9
4 16
5 25

23
7
9
```

*(Task 3: prints 7, then 9, then breaks when running sum > 15.)*

---

<details>
<summary>Solution</summary>

```python
for i in range(1, 6):
    print(i, i * i)

nums = [4, 7, 2, 9, 1]
s = 0
for n in nums:
    s += n
print(s)

s = 0
for n in nums:
    if n > 5:
        print(n)
    s += n
    if s > 15:
        break
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_5() -> dict[str, str]:
    label = "Master class - Numbers, Logic & Structure"
    pre_read = f"""# Master Class: Numbers, Logic & Structure — The Mathematical Language of Data
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- Why computers use **0 and 1** to represent every decision
- How **AND, OR, NOT** and truth tables mirror Python conditions
- What **sets** are and how lists, dicts, and JSON relate to set ideas
- How **functions** in math (domain → range) differ from but inform code functions
- Why this math sits underneath every data type you will use

---

## A. Binary and Boolean Logic

> 💡 **Analogy:** A light switch is only **on** or **off**. Every complex computer decision is built from millions of such switches.

**One-line definition:** **Boolean logic** uses True/False values combined with AND, OR, NOT to represent decisions.

| A | B | A AND B | A OR B |
|---|---|---|---|
| T | T | T | T |
| T | F | F | T |
| F | T | F | T |
| F | F | F | F |

**De Morgan's laws (intuition):** NOT (A AND B) = (NOT A) OR (NOT B) — flip each part and swap AND/OR.

```mermaid
flowchart LR
    B[Binary 0/1] --> BL[Boolean True/False]
    BL --> PY[Python if/while]
    BL --> DT[Data type flags]
```

---

## B. Set Theory — Lists, Dicts, JSON

> 💡 **Analogy:** A **set** is a bag of unique marbles — no duplicates. A **list** is marbles in order. A **dict** labels each marble with a name tag.

| Math idea | Python structure |
|---|---|
| Set membership | `x in my_list` |
| Union | combine unique items |
| Intersection | items in both |
| Mapping (function) | dict key → value |

```mermaid
flowchart TD
    S[Mathematical set] --> L[List ordered]
    S --> T[Tuple fixed]
    S --> D[Dict key-value map]
    D --> J[JSON on the wire]
```

---

## C. Functions in Math vs Code

> 💡 **Analogy:** A vending machine: you input coins (**domain**), it outputs a snack (**range**). Every input maps to **at most one** output.

**One-line definition:** A **function** maps each input from a **domain** to exactly one output in the **range**.

In Python, `def greet(name): return f"Hi {{name}}"` is the same idea: one input name → one output string.

---

## Practice Exercises

**1. Pattern Recognition** — Truth table: A=True, B=False. What is A OR B? A AND B?

**2. Concept Detective** — Why is a Python `set` better than a list for "unique user IDs"?

**3. Real-Life Application** — Give one example each of union and intersection in daily life.

**4. Spot the Error** — "A dict can have two identical keys with different values." True or false?

**5. Planning Ahead** — If domain is exam scores 0–100 and range is grades A–F, is one score → two grades allowed in a function?

---

> ✅ **You're done!** You see the math under Python's logic and collections. Next session: **functions** in code for reusable blocks.
"""
    lecture = f"""# Lecture Script: Master Class — Numbers, Logic & Structure
> **Instructor Reference** — Module 1: Foundations of Data | Session 5 | Duration: 2 Hours

---

## Session Overview

**Goal:** Build intuition for boolean logic, sets, and mathematical functions — connecting to Python data structures.

**Tone:** Conceptual, board-heavy, minimal coding. Draw truth tables and Venn diagrams.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Opening: why math matters for data | 10 min |
| Binary & boolean + truth tables | 25 min |
| De Morgan + link to if/and/or | 15 min |
| BREAK | 10 min |
| Sets, Venn diagrams, Python mapping | 25 min |
| Math functions → Python def | 20 min |
| Discussion + wrap | 15 min |

---

## Activities

- Build truth table for `(A or B) and not C` on paper
- Venn diagram: users who bought A, B, both
- Whiteboard: domain/range for `score → grade`
"""
    coding = f"""# Coding Problem: Master class - Numbers, Logic & Structure
> **Session 5 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Evaluate and print boolean results:

```python
a, b = True, False
print(a and b)
print(a or b)
print(not a)
```

**Task 2 — Basic**

De Morgan check — should match:

```python
a, b = True, False
print(not (a and b))
print((not a) or (not b))
```

**Task 3 — Mid**

Use a set to print unique tags from a list:

```python
tags = ["ml", "ai", "ml", "data", "ai", "python"]
# unique tags, sorted
```

---

## Expected Output

```
False
True
False
True
True
['ai', 'data', 'ml', 'python']
```

---

<details>
<summary>Solution</summary>

```python
a, b = True, False
print(a and b)
print(a or b)
print(not a)
print(not (a and b))
print((not a) or (not b))

tags = ["ml", "ai", "ml", "data", "ai", "python"]
print(sorted(set(tags)))
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_6() -> dict[str, str]:
    label = "Writing Reusable Code with Functions"
    pre_read = f"""# Writing Reusable Code with Functions
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- How to **define and call** functions with `def`
- How **parameters and arguments** pass data in
- How **return values** send results back
- How **scope** controls which variables exist where
- How **default arguments** make functions flexible

---

## A. Why Functions?

> 💡 **Analogy:** A **function** is a recipe card. Write it once; cook the dish whenever you need it — same steps, maybe different serving size (arguments).

**One-line definition:** A **function** is a named, reusable block of code that runs when called.

```python
def greet(name):
    return f"Hello, {{name}}"

print(greet("Sam"))
```

---

## B. Parameters, Return, and Scope

| Concept | Meaning |
|---|---|
| Parameter | Name in `def` |
| Argument | Value you pass in |
| return | Sends value back; ends function |
| Local scope | Variables inside function |

```mermaid
flowchart LR
    C[Call greet Sam] --> F[Function body]
    F --> R[Return string]
    R --> O[Caller receives result]
```

---

## C. Default Arguments and Modularity

```python
def power(base, exp=2):
    return base ** exp

power(5)      # 25
power(5, 3)   # 125
```

Refactor repeated blocks into one function — **DRY**: Don't Repeat Yourself.

---

## Practice Exercises

**1. Pattern Recognition** — What does `def f(): pass` do when called?

**2. Concept Detective** — A variable `x` is set inside a function but not returned. Can the caller use it?

**3. Real-Life Application** — Name three "functions" in real life (microwave preset, etc.).

**4. Spot the Error** — Function uses `total` but `total` was never passed or defined inside. Name the error type.

**5. Planning Ahead** — Design `celsius_to_fahrenheit(c)` with formula F = C × 9/5 + 32.

---

> ✅ **You're done!** Functions are your first modular design tool. Next: **data structures** for storing many values.
"""
    lecture = f"""# Lecture Script: Writing Reusable Code with Functions
> **Instructor Reference** — Module 1: Foundations of Data | Session 6 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students define functions with parameters, returns, defaults, and understand scope.

**Key outcome:** Refactor a repetitive script into 3–4 functions; unit-style tests with print.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Why modularity | 10 min |
| def, call, return live | 25 min |
| Scope demo (local vs global) | 15 min |
| BREAK | 10 min |
| Default args + refactor lab | 40 min |
| Docstrings intro | 10 min |
| Wrap | 10 min |

---

## Lab

Start with 40-line script computing order totals with copy-paste; end with `calc_subtotal`, `calc_tax`, `calc_total`.
"""
    coding = f"""# Coding Problem: Writing Reusable Code with Functions
> **Session 6 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Write `double(n)` returning n×2. Print `double(7)`.

**Task 2 — Basic**

Write `discounted(price, pct=10)` returning price after pct% off. Test with default and `pct=25`.

**Task 3 — Mid**

Write `summary(name, scores)` returning average of list `scores`; print one f-string line for `summary("Ria", [80, 90, 70])`.

---

## Expected Output

```
14
90.0
75.0
Ria avg: 80.0
```

---

<details>
<summary>Solution</summary>

```python
def double(n):
    return n * 2
print(double(7))

def discounted(price, pct=10):
    return price * (1 - pct / 100)
print(discounted(100))
print(discounted(100, 25))

def summary(name, scores):
    avg = sum(scores) / len(scores)
    return avg

name, scores = "Ria", [80, 90, 70]
print(f"{{name}} avg: {{summary(name, scores)}}")
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_7() -> dict[str, str]:
    label = "Python Data Structures"
    pre_read = f"""# Python Data Structures
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- How **lists, dicts, tuples, and sets** store data differently
- **Indexing and slicing** on sequences
- **Mutable vs immutable** — what you can change in place
- **Nesting** structures for real records
- How to **pick the right structure** for a problem

---

## A. Lists and Tuples

> 💡 **Analogy:** A **list** is a shopping list you can edit. A **tuple** is a printed receipt — fixed once created.

| | list | tuple |
|---|---|---|
| Syntax | `[1,2]` | `(1,2)` |
| Mutable | Yes | No |
| Use | Changing collections | Fixed records |

```python
items = ["pen", "book"]
items.append("bag")
coords = (12.9, 77.6)
```

---

## B. Dictionaries and Sets

> 💡 **Analogy:** A **dict** is a contact book: name → number. A **set** is a unique guest list — no duplicates.

```python
user = {{"name": "Alex", "role": "analyst"}}
tags = {{"ml", "python", "ml"}}
```

```mermaid
flowchart TD
    Q{{Need key-value?}}
    Q -->|Yes| D[dict]
    Q -->|No| L{{Order matters?}}
    L -->|Yes| LI[list or tuple]
    L -->|No| S[set]
```

---

## C. Indexing, Slicing, Nesting

```python
nums = [10, 20, 30, 40]
nums[0]    # 10
nums[-1]   # 40
nums[1:3]  # [20, 30]

team = [{{"name": "A", "score": 9}}, {{"name": "B", "score": 7}}]
```

---

## Practice Exercises

**1. Pattern Recognition** — Which types are mutable: list, tuple, dict, set?

**2. Concept Detective** — Store 50 student IDs with no duplicates — list or set?

**3. Real-Life Application** — Model a movie ticket: title, seat, price — which structures?

**4. Spot the Error** — `t = (1, 2); t[0] = 5` — what happens?

**5. Planning Ahead** — Nested dict for two users with name and email lists.

---

> ✅ **You're done!** You can choose and manipulate core Python containers. Next: **files, JSON, and APIs**.
"""
    lecture = f"""# Lecture Script: Python Data Structures
> **Instructor Reference** — Module 1: Foundations of Data | Session 7 | Duration: 2 Hours

---

## Session Overview

**Goal:** Fluency with list/dict/tuple/set operations, slicing, nesting, and structure selection.

**Key outcome:** Build an in-memory "mini database" of products as list of dicts with CRUD-style operations.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Four structures overview | 15 min |
| Lists + tuples hands-on | 25 min |
| BREAK | 10 min |
| Dicts + sets | 25 min |
| Nesting + choice guide | 15 min |
| Lab: product catalog | 25 min |
| Wrap | 5 min |
"""
    coding = f"""# Coding Problem: Python Data Structures
> **Session 7 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Given list, print first, last, and slice middle two:

```python
nums = [5, 10, 15, 20, 25]
```

**Task 2 — Basic**

Count unique words using a set:

```python
words = ["data", "ml", "data", "ai", "ml", "ai"]
```

**Task 3 — Mid**

Build dict `inventory` with keys `"apple"`, `"banana"` and counts; print total items.

```python
inventory = {{"apple": 3, "banana": 5}}
```

---

## Expected Output

```
5
25
[10, 15]
3
8
```

---

<details>
<summary>Solution</summary>

```python
nums = [5, 10, 15, 20, 25]
print(nums[0])
print(nums[-1])
print(nums[1:3])

words = ["data", "ml", "data", "ai", "ml", "ai"]
print(len(set(words)))

inventory = {{"apple": 3, "banana": 5}}
print(sum(inventory.values()))
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_8() -> dict[str, str]:
    label = "File Handling, JSON & APIs"
    src = ROOT / "IITP-AIMLH-2605/Module 1- Foundations of Data/Session 7- File Handling & JSON Processing"
    api_src = ROOT / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 14- APIs & Building AI Interfaces"
    pre_read = ""
    if src.exists():
        pre = list(src.glob("pre-read: *"))[0].read_text(encoding="utf-8")
        pre = pre.replace("File Handling & JSON Processing", "File Handling, JSON & APIs")
        pre = pre.replace("File Handling & JSON", "File Handling, JSON & APIs")
        pre_read = pre + """

---

## E. APIs — Talking to Services Over the Web

> 💡 **Analogy:** An **API** is a restaurant menu with a fixed list of dishes. You order by name (endpoint); the kitchen (server) sends back your meal (JSON response).

**One-line definition:** An **API** lets your program request data or actions from another service over the internet using HTTP.

| Method | Typical use |
|---|---|
| GET | Read data |
| POST | Send data to create/update |

```python
import requests
r = requests.get("https://api.github.com")
print(r.status_code)
print(r.json()["current_user_url"])
```

**Ethics:** Never commit API keys; respect rate limits and Terms of Service.

---

## Practice Exercises (API)

**5. Planning Ahead** — Name one public API you could call for a weather dashboard.

> ✅ **Extended pre-read** now covers files, JSON, and API basics for Session 8.
"""
    else:
        pre_read = "# File Handling, JSON & APIs\n\n*(See lecture script.)*\n"

    lecture_file = list(src.glob("lecture-script: *")) if src.exists() else []
    lecture = lecture_file[0].read_text(encoding="utf-8") if lecture_file else "# Lecture Script\n"
    lecture = lecture.replace("Session 7", "Session 8").replace("File Handling & JSON Processing", "File Handling, JSON & APIs")

    if api_src.exists():
        api_lecture = list(api_src.glob("lecture-script: *"))[0].read_text(encoding="utf-8")
        lecture += "\n\n---\n\n## API Segment (from course outline)\n\nIntegrate GET requests, status codes, API keys via `.env`, and ethical rate limiting. See Session 14 API script in AIMLTN-2605 for full demo flow — adapted here for 45 min segment after JSON lab.\n"

    coding = f"""# Coding Problem: File Handling, JSON & APIs
> **Session 8 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Parse JSON string and print city:

```python
import json
raw = '{{"user": "Maya", "city": "Pune", "score": 88}}'
data = json.loads(raw)
print(data["city"])
```

**Task 2 — Basic**

Write dict to JSON string with `ensure_ascii=False`:

```python
record = {{"product": "Notebook", "qty": 2}}
# json.dumps → print
```

**Task 3 — Mid**

Simulate API response — print status and title:

```python
response = {{"status_code": 200, "body": {{"title": "Intro to ML"}}}}
# Print: OK: Intro to ML if status 200 else Error
```

---

## Expected Output

```
Pune
{{"product": "Notebook", "qty": 2}}
OK: Intro to ML
```

---

<details>
<summary>Solution</summary>

```python
import json
raw = '{{"user": "Maya", "city": "Pune", "score": 88}}'
data = json.loads(raw)
print(data["city"])

record = {{"product": "Notebook", "qty": 2}}
print(json.dumps(record))

response = {{"status_code": 200, "body": {{"title": "Intro to ML"}}}}
if response["status_code"] == 200:
    print("OK:", response["body"]["title"])
else:
    print("Error")
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


def content_session_12() -> dict[str, str]:
    label = "Data Visualization"
    pre_read = f"""# Data Visualization
---

## Mental Map

*(Generated by mental-map script — see mental Map file in this folder.)*

## What You'll Learn

In this pre-read, you'll discover:

- When to use **line, bar, scatter, and histogram** charts
- How to add **titles, labels, and legends** in Matplotlib
- How **Plotly** makes interactive charts
- How chart choice depends on **variable type and goal**
- How good visuals support decisions, not decoration

---

## A. Choosing the Right Chart

> 💡 **Analogy:** You wouldn't use a pie chart to show temperature every hour — like using a photo when you need a timeline. **Chart type** must match the question.

| Question | Chart | X | Y |
|---|---|---|---|
| Trend over time | Line | Time | Metric |
| Compare categories | Bar | Category | Value |
| Relationship | Scatter | Var A | Var B |
| Distribution | Histogram | Bins | Count |

```mermaid
flowchart TD
    Q{{What are you showing?}}
    Q -->|Over time| L[Line]
    Q -->|Compare groups| B[Bar]
    Q -->|Two variables| S[Scatter]
    Q -->|Spread of one| H[Histogram]
```

---

## B. Matplotlib Basics

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar"]
sales = [120, 150, 130]
plt.bar(months, sales)
plt.title("Monthly Sales")
plt.ylabel("Units")
plt.show()
```

Always label axes and title — your future self (and your manager) will thank you.

---

## C. Plotly for Interactivity

Plotly charts zoom, hover, and filter — useful in dashboards and notebooks shared with non-coders.

---

## Practice Exercises

**1. Pattern Recognition** — Show exam scores for 30 students' distribution — histogram or line?

**2. Concept Detective** — Revenue by product category — which chart?

**3. Real-Life Application** — One misleading chart you have seen (truncated axis, etc.).

**4. Spot the Error** — Scatter plot with 2 categories on x-axis only — better alternative?

**5. Planning Ahead** — Sketch axes for website visits per day for one month.

---

> ✅ **You're done!** You can match charts to questions. Next: **EDA and business thinking** on real datasets.
"""
    lecture = f"""# Lecture Script: Data Visualization
> **Instructor Reference** — Module 1: Foundations of Data | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students create Matplotlib line/bar/scatter/histogram and one Plotly interactive chart with proper labels.

**Key outcome:** Single-page "sales dashboard" from a CSV snippet — 4 chart types, one insight slide.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Chart choice framework | 15 min |
| Matplotlib line + bar | 25 min |
| BREAK | 10 min |
| Scatter + histogram | 25 min |
| Plotly demo | 20 min |
| Lab + critique bad charts | 20 min |
| Wrap | 5 min |
"""
    coding = f"""# Coding Problem: Data Visualization
> **Session 12 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
visits = [120, 135, 128, 150, 142]
```

---

## Tasks

**Task 1 — Basic**

Create a bar chart of visits by day with title "Daily Visits".

**Task 2 — Basic**

On same data, print max visits and which day (no plot).

**Task 3 — Mid**

Add `plt.ylabel("Visits")` and save figure as `visits.png` (use `plt.savefig` before show/close).

---

## Expected Output

```
150 Thu
Saved visits.png
```

*(Plus bar chart displayed or saved.)*

---

<details>
<summary>Solution</summary>

```python
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
visits = [120, 135, 128, 150, 142]

plt.bar(days, visits)
plt.title("Daily Visits")
plt.ylabel("Visits")
plt.savefig("visits.png")
plt.close()

print(max(visits), days[visits.index(max(visits))])
print("Saved visits.png")
```
</details>
"""
    return {"pre_read": pre_read, "lecture_script": lecture, "coding_problem": coding}


GENERATORS = {
    1: content_session_1,
    2: content_session_2,
    3: content_session_3,
    4: content_session_4,
    5: content_session_5,
    6: content_session_6,
    7: content_session_7,
    8: content_session_8,
    12: content_session_12,
}


def main() -> None:
    MODULE.mkdir(parents=True, exist_ok=True)
    created = 0
    copied = 0

    for session in SESSIONS:
        folder = MODULE / session["folder"]
        label = session["label"]

        if "copy_from" in session and session["copy_from"].exists():
            copy_session_files(session)
            copied += 1
            print(f"Copied: {session['folder']}")
            continue

        gen = GENERATORS.get(session["num"])
        if gen:
            content = gen()
            write_file(folder, "pre-read", label, content["pre_read"])
            write_file(folder, "lecture-script", label, content["lecture_script"])
            write_file(folder, "coding-problem", label, content["coding_problem"])
            created += 1
            print(f"Generated: {session['folder']}")
        else:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"PENDING manual content: {session['folder']}")

    print(f"\nGenerated: {created}, Copied: {copied}, Pending: {len(SESSIONS) - created - copied}")


if __name__ == "__main__":
    main()
