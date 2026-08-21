# Mental Map — File Handling, JSON & APIs
> Academic Session 8 · Module 1: Foundations of Data

```mermaid
%%{init: {"theme": "default", "themeVariables": { "fontSize": "28px", "fontFamily": "sans-serif" }, "flowchart": {"useMaxWidth": false, "htmlLabels": true, "nodeSpacing": 100, "rankSpacing": 140, "wrappingWidth": 700, "padding": 40}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Foundations of Data</i><br/>&nbsp;<br/><b>Covered so far:</b> AI Landscape; Python Fundamentals; Control Flow; Loops; Master class: Numbers/Logic/Structure; Functions; Python Data Structures<br/>This is Session 8 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>File Handling, JSON & APIs</b><br/>&nbsp;<br/><i>The shift:</i> from <i>'my data lives only inside my code'</i> to <b>'I can read, save, and fetch real data from files and the internet'</b><br/>&nbsp;<br/>File I/O & context managers · JSON structure<br/>The requests library & APIs · Ethical key & rate-limit usage"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Read and write files safely, parse and generate JSON, make API calls with requests,<br/>and apply ethical usage of API keys and rate limits"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>This is the bridge from 'toy examples' to real data — every dataset and API you'll touch for the rest of the course arrives exactly this way"]
    RVAL["<b>Real-Life Value</b><br/>The same skill behind an app checking Swiggy's menu (GET) or placing your order (POST) behind the scenes"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>NumPy: Numerical Foundation<br/><i>Handle large numerical datasets efficiently, without slow loops</i>"]
    U1["<b>Later in Module 1</b><br/>Pandas (Loading & Aggregation), Master class: Tables & Relationships"]
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
