# Python Data Structures
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI,… · Identify and…<br/>Construct if/elif/else bloc… · Write for an…<br/>Number Systems & Boolean Lo… · Define and c…"]
    CURSES["<b>Current Session</b><br/><b>Python Data Structures</b><br/><i>Shift:</i> Pick the right in-memory data shape<br/>Create and perform operations on lists, diction…<br/>differentiate between mutable and immutable str…"]
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
user = {"name": "Alex", "role": "analyst"}
tags = {"ml", "python", "ml"}
```

```mermaid
flowchart TD
    Q{Need key-value?}
    Q -->|Yes| D[dict]
    Q -->|No| L{Order matters?}
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

team = [{"name": "A", "score": 9}, {"name": "B", "score": 7}]
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
