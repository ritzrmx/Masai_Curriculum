# Mental Map — Tableau Basics and First Charts
> Academic Session 17 · Module 3: Tableau Dashboards + Storytelling

```mermaid
%%{init: {'themeVariables': {'fontSize': '16px'}, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 80, 'rankSpacing': 120, 'wrappingWidth': 620, 'padding': 20}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction LR
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 3: Tableau Dashboards + Storytelling</i><br/>&nbsp;<br/><b>Covered so far:</b> nothing yet — this is the module's first session<br/>This is Session 17 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Tableau Basics and First Charts</b><br/>&nbsp;<br/><i>The shift:</i> from <i>scrolling through raw SQL output tables</i> to <b>seeing the same data as an instant, readable chart</b><br/>&nbsp;<br/>Tableau interface · Loading data<br/>Basic bar &amp; line charts · Mapping fields to axes"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction LR
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Load a Kirana365 orders dataset into Tableau and build<br/>your first bar and line charts by dragging the right<br/>fields onto Rows, Columns, and Marks"]
end

subgraph value[" WHY IT MATTERS "]
direction LR
    CVAL["<b>Course Value</b><br/>Every dashboard you build for the rest of Module 3 is made of charts exactly like these"]
    RVAL["<b>Real-Life Value</b><br/>An ops manager can glance at one chart on their phone instead of scrolling 5,000 rows of Excel before a Monday review"]
end

subgraph future[" WHAT COMES NEXT "]
direction LR
    U0["<b>Next Session</b><br/>Statistics: Probability and Uncertainty<br/><i>How sure can you really be that a customer will buy?</i>"]
    U1["<b>Later in Module 3</b><br/>Choosing the Right Chart · Building a Dashboard<br/>KPIs and Trends on One View"]
    U2["<b>Upcoming Modules</b><br/>Module 4: GenAI for Analytics Workflows + Basic Python<br/><i>These same charts later get rebuilt in Python and stitched into full workflows</i>"]
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
