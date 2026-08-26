# Mental Map — Pandas: Loading, Inspection & Filtering
> Academic Session 10 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape through NumPy: Numerical Foundation<br/>This is Session 10 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Pandas: Loading, Inspection & Filtering</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'numbers in an array'</i> to <b>'labeled, real-world tables I can load, inspect, and filter'</b><br/>&nbsp;<br/>pd.read_csv() · head/info/describe/shape<br/>Boolean indexing · loc vs iloc & sorting"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Load a CSV into a DataFrame, inspect it with head/info/describe, filter rows with boolean conditions and loc/iloc,<br/>and spot data quality issues from inspection output"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This is the tool you'll use in almost every remaining session — EDA, visualization, and SQL all assume you can load and filter a DataFrame first"]
    RVAL["<b>Real-Life Value</b><br/>The same skill behind a shop owner scanning through a sales ledger to find only the ₹500+ transactions from last week"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Pandas: Aggregation, Groupby & Merging<br/><i>Summarize this data and combine it with other tables</i>"]
    U1["<b>Later in Module 1</b><br/>Master class: Tables & Relationships, Data Visualization, EDA"]
    U2["<b>Upcoming Modules</b><br/>Course continues beyond Foundations of Data<br/><i>Details as the curriculum unfolds</i>"]
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
```
