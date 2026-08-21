# Mental Map — Data Analysis with Spreadsheets
> Academic Session 16 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape through SQL with MySQL Workbench<br/>This is Session 16 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Data Analysis with Spreadsheets</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'I answer these questions in code'</i> to <b>'I can answer them in the tool most business teams already use daily'</b><br/>&nbsp;<br/>VLOOKUP & XLOOKUP · Pivot tables<br/>Filters, sorting & conditional formatting · SUM/AVERAGE/COUNTIF & named ranges"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Use VLOOKUP and XLOOKUP to retrieve values across sheets, build pivot tables to summarize data,<br/>and apply COUNTIF and conditional formatting to surface quick insights"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This closes Module 1 by showing that every skill you've built — filtering, grouping, joining — exists in spreadsheets too, the tool most non-technical stakeholders will actually open"]
    RVAL["<b>Real-Life Value</b><br/>The same skill behind instantly summarizing a huge sales sheet into 'total sales per city,' or highlighting overdue accounts in red automatically"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Module</b><br/>Module 1: Foundations of Data is now complete<br/><i>The course continues into its next module — details as the curriculum unfolds</i>"]
    U1["<b>Skills carried forward</b><br/>Every Pandas, SQL, and spreadsheet skill from this module becomes the foundation for deeper analysis and modeling ahead"]
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
