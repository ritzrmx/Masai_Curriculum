# Mental Map — Connecting the Tools
> Academic Session 37 · Module 4: GenAI for Analytics Workflows + Basic Python

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 4: GenAI for Analytics Workflows + Basic Python</i><br/>&nbsp;<br/><b>Covered so far:</b> Getting Started with Python Data · Cleaning Data with Pandas · Visualizing Data with Python<br/>plus 8 earlier Module 4 sessions<br/>This is Session 37 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Connecting the Tools</b><br/>&nbsp;<br/><i>The shift:</i> from <i>using each tool on its own</i> to <b>connecting spreadsheets, SQL, Tableau and Python into one organised workflow with a check at every hand-off</b><br/>&nbsp;<br/>Combining outputs from spreadsheets, SQL, Tableau and Python<br/>Connecting different tools into one workflow<br/>Organising analysis steps end to end"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Combine a SQL export and a spreadsheet of Kirana365 figures in Python,<br/>hand the result to a dashboard, and document the workflow<br/>with a check at every hand-off"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This is the structure the end-to-end session follows from raw data to final insight"]
    RVAL["<b>Real-Life Value</b><br/>Replacing copy-and-paste between tools with a hand-off you can repeat and trust"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>End-to-End Analytics Workflow<br/><i>Now we run one complete analysis from question to communicated insight</i>"]
    U1["<b>Later in Module 4</b><br/>Statistics: Distributions; Insights and Drawing Conclusions"]
    U2["<b>Upcoming</b><br/>Capstone Project<br/><i>Joining tools into one workflow is exactly how the capstone is assembled</i>"]
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
