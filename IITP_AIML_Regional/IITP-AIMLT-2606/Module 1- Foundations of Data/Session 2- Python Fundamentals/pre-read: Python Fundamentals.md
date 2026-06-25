# Python Fundamentals
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI, ML and GenAI…"]
    CURSES["<b>Current Session</b><br/><b>Python Fundamentals</b><br/><i>Shift:</i> Move from watching to a working dev lab<br/>Identify and declare variables using correct da…<br/>construct expressions using arithmetic and comp…"]
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
print(f"Hello {name}, you scored {score}%")
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
