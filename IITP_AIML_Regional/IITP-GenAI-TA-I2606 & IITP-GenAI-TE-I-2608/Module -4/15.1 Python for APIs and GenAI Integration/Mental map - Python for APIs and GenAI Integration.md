# Mental Map — Python for APIs and GenAI Integration
> Academic Session 33 · Module 4: GenAI for Analytics Workflows + Basic Python

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 4: GenAI for Analytics Workflows + Basic Python</i><br/>&nbsp;<br/><b>Covered so far:</b> Python Fundamentals I · Python Fundamentals II · Python Fundamentals III<br/>plus 4 earlier Module 4 sessions<br/>This is Session 33 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Python for APIs and GenAI Integration</b><br/>&nbsp;<br/><i>The shift:</i> from <i>using GenAI by typing into a chat window</i> to <b>calling GenAI from code through an API, as one step inside your own script</b><br/>&nbsp;<br/>HTTP requests with the requests library · API structure: endpoints, headers, JSON<br/>Calling the OpenAI API from Python<br/>A script combining file reading, functions and API calls"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Run a Python script that reads Kirana365 figures from a file,<br/>sends them to GenAI through an API, and saves the summary it returns,<br/>checking the response before using it"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This is how the GenAI step of an automated workflow runs with nobody typing"]
    RVAL["<b>Real-Life Value</b><br/>Generating a weekly summary automatically instead of copying data into a chat window each time"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Getting Started with Python Data<br/><i>Now we load and inspect whole tables with pandas instead of reading files by hand</i>"]
    U1["<b>Later in Module 4</b><br/>Cleaning Data with Pandas · Visualizing Data with Python<br/>Connecting the Tools"]
    U2["<b>Upcoming</b><br/>Capstone Project<br/><i>Putting GenAI inside a workflow is a pattern the capstone can build on</i>"]
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
