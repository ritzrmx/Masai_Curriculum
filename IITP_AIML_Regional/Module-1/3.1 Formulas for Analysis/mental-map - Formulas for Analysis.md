# Mental Map — Formulas for Analysis
> Academic Session 6 · Module 1: Analytics Foundations + GenAI + Spreadsheets

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '28px', 'fontFamily': 'sans-serif' }, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 100, 'rankSpacing': 140, 'wrappingWidth': 700, 'padding': 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Analytics Foundations + GenAI + Spreadsheets</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data and Averages · Analytics Workflow, Metrics & KPIs · GenAI for Analytics · Clean Up the Data · Make Data Ready for Analysis<br/>This is Session 6 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Formulas for Analysis</b><br/>&nbsp;<br/><i>The shift:</i> from <i>preparing and validating data</i> to <b>actually calculating business numbers you can trust, using formulas</b><br/>&nbsp;<br/>SUM, AVERAGE, COUNT · Applying formulas across rows/columns<br/>Creating new calculated columns · Simple descriptive analysis"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Apply SUM, AVERAGE, and COUNT correctly across a validated dataset, build new<br/>calculated columns, and use formulas to answer simple descriptive business questions"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>These are the exact same operations behind SQL's SUM()/AVG()/COUNT(),<br/>Tableau's aggregations, and pandas' .sum()/.mean() — learn the logic once, reuse it everywhere"]
    RVAL["<b>Real-Life Value</b><br/>Quickly calculating total spend, average cost per person, and item<br/>counts when splitting a group trip or event budget"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Pivot Tables and Quick Insights<br/><i>Summarizing and comparing the same numbers across categories, without writing repeated formulas</i>"]
    U1["<b>Later in Module 1</b><br/>Module 1 wraps up after the next session"]
    U2["<b>Upcoming Modules</b><br/>Module 2: SQL for Data Analysis · Module 3: Tableau Dashboards + Storytelling · Module 4: GenAI Workflows + Python<br/><i>SUM/AVERAGE/COUNT reappear immediately as SQL's aggregation functions in Module 2</i>"]
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
