# Mental Map — Summarise, Compare and Report with GenAI
> Academic Session 27 · Module 4: GenAI for Analytics Workflows + Basic Python

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 4: GenAI for Analytics Workflows + Basic Python</i><br/>&nbsp;<br/><b>Covered so far:</b> Statistics: Relationships in Data<br/>This is Session 27 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Summarise, Compare and Report with GenAI</b><br/>&nbsp;<br/><i>The shift:</i> from <i>writing a single one-off GenAI prompt for one insight</i> to <b>deliberately prompting GenAI to summarise, compare, and build structured reports — then refining when the output falls short</b><br/>&nbsp;<br/>Prompting for summaries &amp; comparisons · Extracting key points from outputs<br/>Generating structured reports · Refining prompts to improve outputs"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Write a GenAI prompt that turns raw Kirana365 figures into<br/>a structured comparison table or summary report, then<br/>refine the prompt when the first output isn't good enough"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This exact skill becomes one step inside the multi-step GenAI workflows you build for the rest of this module"]
    RVAL["<b>Real-Life Value</b><br/>Generating a clean city-performance comparison table for a leadership meeting in minutes instead of manually formatting one"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Breaking Down the Workflow<br/><i>Now we learn to split a whole analysis problem into steps like this one</i>"]
    U1["<b>Later in Module 4</b><br/>Multi-Step GenAI Workflows · Python Fundamentals I, II, III<br/>Python for APIs and GenAI Integration"]
    U2["<b>Upcoming</b><br/>Capstone Project<br/><i>Prompting for structured, trustworthy output is a skill the capstone assumes you already have</i>"]
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
