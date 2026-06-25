# Control Flow & Decision Making
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI, ML and GenAI…<br/>Identify and declare variables using co…"]
    CURSES["<b>Current Session</b><br/><b>Control Flow & Decision Making</b><br/><i>Shift:</i> Turn business rules into executable log…<br/>Construct if/elif/else blocks to handle real de…<br/>evaluate boolean expressions combining multiple…"]
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
    C{score >= 60?}
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
