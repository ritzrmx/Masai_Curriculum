# Mental Map — SQL with MySQL Workbench
> Academic Session 15 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape through EDA & Business Thinking<br/>This is Session 15 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>SQL with MySQL Workbench</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'I ask these questions in Pandas'</i> to <b>'I can ask the exact same questions directly against a database'</b><br/>&nbsp;<br/>SELECT & WHERE · ORDER BY, LIMIT & DISTINCT<br/>GROUP BY & HAVING · JOINs & aliases"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Write SQL queries to filter, sort and group data, join two or more tables with INNER/LEFT/RIGHT JOIN,<br/>and choose the correct join type for a given multi-table scenario"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Most real company data lives in databases, not CSVs — SQL is how you'll actually retrieve it in most real analyst jobs"]
    RVAL["<b>Real-Life Value</b><br/>The same skill behind matching a student roster to their exam results, or asking a system for 'only Hyderabad orders above ₹500, sorted by date'"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Data Analysis with Spreadsheets<br/><i>Answer these same kinds of questions in the tool most business teams already use daily</i>"]
    U1["<b>Later in Module 1</b><br/>Module 1 concludes with Spreadsheets"]
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
