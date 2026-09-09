# Mental Map — Reading Dashboards for Insight
> Academic Session 24 · Module 3: Tableau Dashboards + Storytelling

```mermaid
%%{init: {'themeVariables': {'fontSize': '16px'}, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 80, 'rankSpacing': 120, 'wrappingWidth': 620, 'padding': 20}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction LR
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 3: Tableau Dashboards + Storytelling</i><br/>&nbsp;<br/><b>Covered so far:</b> Tableau Basics and First Charts · Statistics: Probability and Uncertainty · Choosing the Right Chart · Building a Dashboard · KPIs and Trends on One View · Dashboard Design Basics · Dashboards That Support Decisions<br/>This is Session 24 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Reading Dashboards for Insight</b><br/>&nbsp;<br/><i>The shift:</i> from <i>building dashboards for others to read</i> to <b>reading someone else's dashboard and pulling out the real insight it's arguing for</b><br/>&nbsp;<br/>Reading dashboard outputs · Spotting trends &amp; patterns<br/>Converting charts into insight statements"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction LR
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Open an unfamiliar Kirana365-style dashboard you didn't<br/>build, correctly spot the trends and patterns in it, and<br/>write the one-sentence insight it's actually arguing for"]
end

subgraph value[" WHY IT MATTERS "]
direction LR
    CVAL["<b>Course Value</b><br/>This exact reading skill is what you'll hand to GenAI to draft into a full written insight next session"]
    RVAL["<b>Real-Life Value</b><br/>Correctly summarizing a colleague's dashboard from another city without needing a call to explain it to you"]
end

subgraph future[" WHAT COMES NEXT "]
direction LR
    U0["<b>Next Session</b><br/>Insight Writing with GenAI<br/><i>Now we turn the insight you just learned to spot into a clearly written narrative</i>"]
    U1["<b>Later in Module 3</b><br/>Module 3 Evaluation"]
    U2["<b>Upcoming Modules</b><br/>Module 4: GenAI for Analytics Workflows + Basic Python<br/><i>Reading patterns in a chart is the same instinct you'll apply to distributions and correlations there</i>"]
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
