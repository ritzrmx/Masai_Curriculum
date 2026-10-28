# Mental Map — Master Class: Vectors & Linear Algebra — The Mathematics of Space and Direction
> Academic Session 14.2 · Module 3: GenAI & Agents

```mermaid
%%{init: {'themeVariables': {'fontSize': '32px', 'fontFamily': 'sans-serif'}, 'flowchart': {'htmlLabels': true, 'nodeSpacing': 50, 'rankSpacing': 80, 'wrappingWidth': 400, 'padding': 20}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 3: GenAI &amp; Agents</i><br/>&nbsp;<br/><b>Covered so far:</b> Module 1 (AI/ML Landscape through Spreadsheets), Module 2 (ML Workflow through Clustering, Model Selection &amp; Explainability), LLM Fundamentals (13.1), Calling LLMs with APIs (13.2), Prompt Engineering (14.1)<br/>This is Session 14.2 (4 of 14 in Module 3)"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Master Class: Vectors &amp; Linear Algebra — The Mathematics of Space and Direction</b><br/>&nbsp;<br/><i>The shift:</i> from numbers as single values <i>to</i> <b>numbers as arrows with size and direction</b><br/>&nbsp;<br/>Scalars vs vectors · Add, subtract, scale · Magnitude &amp; unit vectors<br/>Dot product · Angle between vectors"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Add, subtract and scale vectors as arrows and as numbers,<br/>find 2D and 3D magnitudes with Pythagoras, compute a dot<br/>product by hand, and use it to find the angle between two<br/>vectors"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Text embeddings (16.2), vector stores (16.3) and RAG (17.1)<br/>all search using today's dot product and angle"]
    RVAL["<b>Real-Life Value</b><br/>You can explain how a search engine knows 'refund' and<br/>'money back' mean nearly the same thing"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Structured Outputs with Pydantic<br/><i>Makes the LLM return clean, validated data instead of free<br/>text</i>"]
    U1["<b>Later in Module 3</b><br/>Getting Started with LangChain · AI Workflows in LangChain ·<br/>Master Class: Calculus · Embeddings &amp; Semantic Search ·<br/>Vector Stores &amp; Retrieval · RAG Pipeline · AI Agents ·<br/>Agentic RAG, Evaluation &amp; Guardrails · LangGraph<br/>Orchestration"]
    U2["<b>Upcoming Modules</b><br/>The next module, per your course calendar<br/><i>Vector maths powers search, recommendations and retrieval<br/>everywhere</i>"]
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
