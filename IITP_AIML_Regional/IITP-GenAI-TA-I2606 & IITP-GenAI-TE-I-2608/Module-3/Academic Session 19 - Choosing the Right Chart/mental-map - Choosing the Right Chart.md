# Mental Map — Choosing the Right Chart
> Academic Session 19 · Module 3: Tableau Dashboards + Storytelling

```mermaid
%%{init: {'themeVariables': {'fontSize': '16px'}, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 80, 'rankSpacing': 120, 'wrappingWidth': 620, 'padding': 20}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 3: Tableau Dashboards + Storytelling</i><br/>&nbsp;<br/><b>Covered so far:</b> Tableau Basics and First Charts · Statistics: Probability and Uncertainty<br/>This is Session 19 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Choosing the Right Chart</b><br/>&nbsp;<br/><i>The shift:</i> from <i>only knowing how to build a bar or a line chart</i> to <b>matching the chart type to the actual question being asked</b><br/>&nbsp;<br/>Chart type variety · Matching chart to data<br/>Comparing chart types · Labels &amp; formatting"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Look at a Kirana365 business question and pick the chart<br/>type that answers it clearly, then format it with labels<br/>and sorting so anyone can read it in seconds"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>A dashboard is only as good as the charts inside it — this is the judgement call every later Tableau session assumes you can make"]
    RVAL["<b>Real-Life Value</b><br/>Picking a chart a store manager actually understands in ten seconds, instead of a cluttered pie chart nobody can read"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Building a Dashboard<br/><i>Now we combine several well-chosen charts into one connected view</i>"]
    U1["<b>Later in Module 3</b><br/>KPIs and Trends on One View · Dashboard Design Basics<br/>Dashboards That Support Decisions"]
    U2["<b>Upcoming Modules</b><br/>Module 4: GenAI for Analytics Workflows + Basic Python<br/><i>You'll rebuild some of these same chart choices in matplotlib later</i>"]
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
