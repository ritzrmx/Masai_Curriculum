# Loops, Iteration & Repetitive Logic
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI, ML and GenAI…<br/>Identify and declare variables using co…<br/>Construct if/elif/else blocks to handle…"]
    CURSES["<b>Current Session</b><br/><b>Loops, Iteration & Repetitive L…</b><br/><i>Shift:</i> Strengthen data foundations around Writ…<br/>Write for and while loops with correct terminat…<br/>apply break and continue to control loop flow"]
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
