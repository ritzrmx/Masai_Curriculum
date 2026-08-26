# Mental Map — NumPy: Numerical Foundation
> Academic Session 9 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape through File Handling, JSON & APIs<br/>This is Session 9 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>NumPy: Numerical Foundation</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'I loop through numbers one at a time'</i> to <b>'I operate on entire collections of numbers at once'</b><br/>&nbsp;<br/>Arrays & dtype · Shape, indexing & slicing<br/>Element-wise ops & broadcasting · Reshape & flatten"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Create and manipulate NumPy arrays with indexing and slicing, perform element-wise arithmetic and broadcasting without loops,<br/>and reshape or flatten arrays for downstream use"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>NumPy is the numerical engine underneath Pandas — every DataFrame column you'll use starting next module is secretly a NumPy array"]
    RVAL["<b>Real-Life Value</b><br/>The same idea behind applying a festival discount to an entire price list instantly, instead of updating each price by hand"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Pandas: Loading, Inspection & Filtering<br/><i>Put this numerical power inside labeled, spreadsheet-like tables</i>"]
    U1["<b>Later in Module 1</b><br/>Pandas: Aggregation & Merging, Master class: Tables & Relationships"]
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
