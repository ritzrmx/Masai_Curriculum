# Mental Map — GenAI for Analytics: Prompt, Check, Improve
> Academic Session 3 · Module 1: Analytics Foundations + GenAI + Spreadsheets

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '28px', 'fontFamily': 'sans-serif' }, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 100, 'rankSpacing': 140, 'wrappingWidth': 700, 'padding': 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Analytics Foundations + GenAI + Spreadsheets</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data and Averages (mean/median/mode/range) · Analytics Workflow, Metrics & KPIs<br/>This is Session 3 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>GenAI for Analytics: Prompt, Check, Improve</b><br/>&nbsp;<br/><i>The shift:</i> from <i>doing every workflow step by hand</i> to <b>using GenAI to speed up steps of the workflow — while personally validating everything it produces</b><br/>&nbsp;<br/>What GenAI is in analytics · Prompting patterns<br/>Structured outputs · Validating GenAI outputs"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Write a clear prompt for a simple analytics task, generate a structured table or<br/>list from GenAI, and catch an incorrect or low-quality GenAI output before trusting it"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This 'prompt → check → improve' loop reappears constantly — GenAI for SQL,<br/>GenAI insight writing, GenAI workflows, and Python + the OpenAI API later in the course"]
    RVAL["<b>Real-Life Value</b><br/>Using ChatGPT to summarize event feedback or draft a report —<br/>and knowing exactly how to catch it when it quietly makes up a number"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Clean Up the Data<br/><i>Moving from Excel/Sheets basics into spotting and fixing messy real-world data</i>"]
    U1["<b>Later in Module 1</b><br/>Make Data Ready for Analysis · Formulas for Analysis<br/>Pivot Tables and Quick Insights"]
    U2["<b>Upcoming Modules</b><br/>Module 2: SQL for Data Analysis · Module 3: Tableau Dashboards + Storytelling · Module 4: GenAI Workflows + Python<br/><i>GenAI keeps reappearing as a helper across every tool — SQL query generation, insight writing, and full Python-API integration</i>"]
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
