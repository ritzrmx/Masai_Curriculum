# Mental Map — Clean Up the Data
> Academic Session 4 · Module 1: Analytics Foundations + GenAI + Spreadsheets

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '28px', 'fontFamily': 'sans-serif' }, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 100, 'rankSpacing': 140, 'wrappingWidth': 700, 'padding': 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Analytics Foundations + GenAI + Spreadsheets</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data and Averages · Analytics Workflow, Metrics & KPIs · GenAI for Analytics<br/>This is Session 4 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Clean Up the Data</b><br/>&nbsp;<br/><i>The shift:</i> from <i>discussing analytics ideas conceptually</i> to <b>getting hands-on in a spreadsheet with real, messy data</b><br/>&nbsp;<br/>Loading data into spreadsheets · Spotting missing values, duplicates, formatting issues<br/>Removing duplicates & fixing formats · Sort and filter to inspect"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Load a raw dataset into Excel/Sheets, spot missing values, duplicates, and formatting<br/>issues by eye, and clean the obvious problems using sort and filter"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Every formula, pivot table, SQL query, and dashboard ahead assumes the data<br/>underneath it is clean — this is the session where that assumption starts being true"]
    RVAL["<b>Real-Life Value</b><br/>Cleaning up a messy contact list or expense sheet before you can<br/>actually trust any total or summary calculated from it"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Make Data Ready for Analysis<br/><i>Going one level deeper — consistent formats, data types, and validating that cleaning actually worked</i>"]
    U1["<b>Later in Module 1</b><br/>Formulas for Analysis · Pivot Tables and Quick Insights"]
    U2["<b>Upcoming Modules</b><br/>Module 2: SQL for Data Analysis · Module 3: Tableau Dashboards + Storytelling · Module 4: GenAI Workflows + Python<br/><i>Clean data is the prerequisite every one of these tools silently assumes you've already handled</i>"]
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
