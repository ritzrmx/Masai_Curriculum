# Mental Map — EDA & Business Thinking
> Academic Session 14 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape through Data Visualization<br/>This is Session 14 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>EDA & Business Thinking</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'I can build a chart or a statistic'</i> to <b>'I can investigate a dataset systematically and connect findings to business questions'</b><br/>&nbsp;<br/>EDA checklist · Distributions, outliers & skewness<br/>Correlation · Funnels, conversion & retention"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Run a structured EDA on a raw dataset, interpret distributions, outliers and correlations,<br/>and connect data findings to real business questions like funnel drop-off and retention"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This session ties together every Pandas, statistics, and visualization skill from this module into one repeatable investigation process"]
    RVAL["<b>Real-Life Value</b><br/>The same thinking behind a business asking 'why do so many app users add to cart but never checkout?'"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>SQL with MySQL Workbench<br/><i>Ask these exact same questions directly against a database, not just a DataFrame</i>"]
    U1["<b>Later in Module 1</b><br/>Data Analysis with Spreadsheets"]
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
