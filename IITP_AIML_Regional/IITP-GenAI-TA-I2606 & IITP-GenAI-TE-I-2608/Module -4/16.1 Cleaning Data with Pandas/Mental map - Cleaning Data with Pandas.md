# Mental Map — Cleaning Data with Pandas
> Academic Session 35 · Module 4: GenAI for Analytics Workflows + Basic Python

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 4: GenAI for Analytics Workflows + Basic Python</i><br/>&nbsp;<br/><b>Covered so far:</b> Python Fundamentals III · Python for APIs and GenAI Integration · Getting Started with Python Data<br/>plus 6 earlier Module 4 sessions<br/>This is Session 35 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Cleaning Data with Pandas</b><br/>&nbsp;<br/><i>The shift:</i> from <i>analysing data exactly as it arrives</i> to <b>cleaning it first: fixing duplicates, missing values and messy entries so the results can be trusted</b><br/>&nbsp;<br/>Cleaning data with pandas · Modifying columns and values<br/>Handling missing values and duplicates<br/>Simple transformations on datasets"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Take a messy Kirana365 orders file and produce a clean table,<br/>recording what you removed, filled or changed, and why"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Clean data is the input to the charts, workflow and conclusions in the sessions ahead"]
    RVAL["<b>Real-Life Value</b><br/>Preventing a leadership dashboard from showing wrong totals because of duplicate or mistyped rows"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Visualizing Data with Python<br/><i>Now we turn the clean table into charts</i>"]
    U1["<b>Later in Module 4</b><br/>Connecting the Tools · End-to-End Analytics Workflow<br/>Statistics: Distributions; Insights and Drawing Conclusions"]
    U2["<b>Upcoming</b><br/>Capstone Project<br/><i>Documented, defensible cleaning is expected in the capstone</i>"]
end

START ==>|" begin "| CURMOD
CURMOD ==>|" progress "| CURSES
CURSES ==>|" you get "| OUT
OUT ==>|" course "| CVAL
OUT ==>|" real life "| RVAL
CURSES ==>|" next up "| U0
U0 -.->|" then "| U1
U1 -.->|" ahead "| U2

classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef outBox fill:#FEF2F2,stroke:#DC2626,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C

class START startBox
class CURMOD curModBox
class CURSES curSessBox
class OUT outBox
class CVAL,RVAL valueBox
class U0,U1,U2 futureBox

linkStyle default stroke-width:2px
```
