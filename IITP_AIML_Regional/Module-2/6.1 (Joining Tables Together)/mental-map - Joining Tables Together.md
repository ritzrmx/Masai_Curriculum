# Mental Map - Joining Tables Together
> Academic Session 13 - Module 2: SQL for Data Analysis

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 2: SQL for Data Analysis</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data &amp; Averages - Analytics Workflow &amp; KPIs - GenAI for Analytics - Clean Up the Data - Make Data Ready for Analysis - Formulas - Pivot Tables - Spread &amp; Variability - SQL Query Basics - Sorting &amp; Filtering - Aggregation Essentials - Grouping for KPIs<br/>This is Session 13 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Joining Tables Together</b><br/>&nbsp;<br/><i>The shift:</i> from one table answering everything <i>to</i> <b>combining two related tables into one richer answer</b><br/>&nbsp;<br/>Why data lives in 2 tables - INNER JOIN<br/>LEFT JOIN - JOIN + WHERE/GROUP BY"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can...</b><br/>&nbsp;<br/>Explain why real data lives in separate related tables, write an<br/>INNER JOIN to combine matching rows, write a LEFT JOIN to keep<br/>unmatched rows too, and combine a JOIN with WHERE/GROUP BY"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Almost no real business question is answerable from a single<br/>table - JOIN is the single most-used clause in professional SQL"]
    RVAL["<b>Real-Life Value</b><br/>'Revenue by loyalty tier' or 'customers who never ordered' need<br/>two tables talking to each other - this is exactly how"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Insights from Combined Data<br/><i>Turning a joined, grouped table into an actual business insight</i>"]
    U1["<b>Later in Module 2</b><br/>Subqueries in Action - CTEs and GenAI for SQL"]
    U2["<b>Upcoming Modules</b><br/>Module 3: Tableau Dashboards + Storytelling - Module 4: GenAI Workflows + Basic Python<br/><i>Tableau's data-relationships/blending and pandas' .merge() are JOIN under a different name</i>"]
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
