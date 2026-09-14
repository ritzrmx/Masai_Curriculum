# Mental Map - CTEs and GenAI for SQL
> Academic Session 16 - Module 2: SQL for Data Analysis

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 2: SQL for Data Analysis</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data &amp; Averages - Analytics Workflow &amp; KPIs - GenAI for Analytics - Clean Up the Data - Make Data Ready - Formulas - Pivot Tables - Spread &amp; Variability - SQL Basics - Sorting &amp; Filtering - Aggregation - Grouping for KPIs - Joining Tables - Insights from Combined Data - Subqueries in Action<br/>This is Session 16 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>CTEs and GenAI for SQL</b><br/>&nbsp;<br/><i>The shift:</i> from nested, hard-to-read subqueries <i>to</i> <b>clean, named, step-by-step queries - and safely using GenAI to help write them</b><br/>&nbsp;<br/>WITH clause (CTEs) - Chaining CTEs<br/>Prompt-Check-Improve for SQL - Verifying AI output"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can...</b><br/>&nbsp;<br/>Rewrite a subquery as a clean, readable CTE using WITH, chain<br/>multiple CTEs into a step-by-step query, and use GenAI to draft<br/>SQL safely - always verifying it against the real schema and data"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This closes out Module 2 by tying every SQL skill so far into one<br/>readable, professional query style - and previews the GenAI<br/>workflows used throughout the rest of this course"]
    RVAL["<b>Real-Life Value</b><br/>On the job, most analysts DO use GenAI to draft SQL - knowing<br/>exactly how to check its output is what makes that safe to do"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Statistics: Probability and Uncertainty<br/><i>Module 3 begins - Tableau Dashboards + Storytelling</i>"]
    U1["<b>Later in Module 2</b><br/>Module 2 concludes with this session"]
    U2["<b>Upcoming Modules</b><br/>Module 3: Tableau Dashboards + Storytelling - Module 4: GenAI Workflows + Basic Python<br/><i>Tableau's calculated fields and pandas' method-chaining both echo today's 'name each step clearly' habit</i>"]
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
