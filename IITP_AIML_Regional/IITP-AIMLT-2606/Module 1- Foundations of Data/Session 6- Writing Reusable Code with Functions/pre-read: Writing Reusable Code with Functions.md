# Writing Reusable Code with Functions
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI,… · Identify and…<br/>Construct if/elif/else bloc… · Write for an…<br/>Number Systems & Boolean Lo…"]
    CURSES["<b>Current Session</b><br/><b>Writing Reusable Code with Func…</b><br/><i>Shift:</i> Strengthen data foundations around Defi…<br/>Define and call functions with parameters and r…<br/>explain how scope affects variable access"]
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
    return f"Hello, {name}"

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
