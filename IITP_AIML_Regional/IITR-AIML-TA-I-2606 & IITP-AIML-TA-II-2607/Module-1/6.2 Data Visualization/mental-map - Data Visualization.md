# Mental Map — Data Visualization
> Academic Session 13 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape through Master class: From Tables to Relationships<br/>This is Session 13 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Data Visualization</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'I understand the math behind a chart'</i> to <b>'I can build the right chart for the right question'</b><br/>&nbsp;<br/>Line & bar charts · Scatter & histogram<br/>Labels, titles & legends · Plotly & choosing the right chart"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Build line, bar, scatter and histogram plots with Matplotlib, create basic interactive Plotly charts,<br/>and choose the right chart type for a given variable and question"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Every EDA finding and business insight from here on needs to be SHOWN, not just calculated — this session is how you show it"]
    RVAL["<b>Real-Life Value</b><br/>The same skill behind the interactive stock charts on money-control apps, or the bar charts comparing sales across branches in a business review"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>EDA & Business Thinking<br/><i>Use these charts as tools inside a structured, business-focused investigation of data</i>"]
    U1["<b>Later in Module 1</b><br/>SQL with MySQL Workbench, Data Analysis with Spreadsheets"]
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
