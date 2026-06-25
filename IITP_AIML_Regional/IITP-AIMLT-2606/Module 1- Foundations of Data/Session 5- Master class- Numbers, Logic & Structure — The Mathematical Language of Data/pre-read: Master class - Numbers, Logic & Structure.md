# Master Class: Numbers, Logic & Structure — The Mathematical Language of Data
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI,… · Identify and…<br/>Construct if/elif/else bloc… · Write for an…"]
    CURSES["<b>Current Session</b><br/><b>Master class: Numbers, Logic &…</b><br/><i>Shift:</i> Turn business rules into executable log…<br/>Number Systems & Boolean Logic"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Math intuition behind<br/>algorithms you will run"]
    RVAL["<b>Real-Life Value</b><br/>Read formulas and charts<br/>without fear in interviews"]
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

In Python, `def greet(name): return f"Hi {name}"` is the same idea: one input name → one output string.

---

## Practice Exercises

**1. Pattern Recognition** — Truth table: A=True, B=False. What is A OR B? A AND B?

**2. Concept Detective** — Why is a Python `set` better than a list for "unique user IDs"?

**3. Real-Life Application** — Give one example each of union and intersection in daily life.

**4. Spot the Error** — "A dict can have two identical keys with different values." True or false?

**5. Planning Ahead** — If domain is exam scores 0–100 and range is grades A–F, is one score → two grades allowed in a function?

---

> ✅ **You're done!** You see the math under Python's logic and collections. Next session: **functions** in code for reusable blocks.
