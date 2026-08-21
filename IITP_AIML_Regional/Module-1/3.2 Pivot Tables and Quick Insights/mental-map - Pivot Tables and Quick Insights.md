# Mental Map — Pivot Tables and Quick Insights
> Academic Session 7 · Module 1: Analytics Foundations + GenAI + Spreadsheets

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '28px', 'fontFamily': 'sans-serif' }, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 100, 'rankSpacing': 140, 'wrappingWidth': 700, 'padding': 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Analytics Foundations + GenAI + Spreadsheets</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data and Averages · Analytics Workflow, Metrics & KPIs · GenAI for Analytics · Clean Up the Data · Make Data Ready for Analysis · Formulas for Analysis<br/>This is Session 7 of 41 — final session of Module 1"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Pivot Tables and Quick Insights</b><br/>&nbsp;<br/><i>The shift:</i> from <i>dragging formulas manually for each summary</i> to <b>letting a pivot table instantly summarize and compare across categories</b><br/>&nbsp;<br/>What a pivot table is · Summarizing data<br/>Comparing categories · Extracting insights from pivot outputs"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Build a pivot table from a clean dataset, summarize totals/averages/counts by category,<br/>compare categories side by side, and pull a clear insight out of the result"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This closes out Module 1's entire arc — clean data (Sessions 4-5) → formulas (Session 6) → pivot<br/>summaries (this session) — the exact same arc SQL's GROUP BY and Tableau will repeat next"]
    RVAL["<b>Real-Life Value</b><br/>Instantly comparing total spend by category on a shared trip or event<br/>budget, without manually adding up each category by hand"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Module 2: SQL for Data Analysis begins<br/><i>Statistics: Spread, Variability and Outliers — going deeper than range into variance and standard deviation</i>"]
    U1["<b>Later in Module 1</b><br/>Module 1 complete — every foundational spreadsheet and analytics skill is now in place"]
    U2["<b>Upcoming Modules</b><br/>Module 2: SQL for Data Analysis · Module 3: Tableau Dashboards + Storytelling · Module 4: GenAI Workflows + Python<br/><i>SQL's GROUP BY and Tableau's drag-and-drop fields are pivot tables in a new form — the logic carries forward directly</i>"]
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
