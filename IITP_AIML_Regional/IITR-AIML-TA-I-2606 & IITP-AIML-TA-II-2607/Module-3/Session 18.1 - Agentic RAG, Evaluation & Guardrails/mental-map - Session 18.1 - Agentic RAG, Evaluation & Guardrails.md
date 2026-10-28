# Mental Map — Agentic RAG, Evaluation & Guardrails
> Academic Session 18.1 · Module 3: GenAI & Agents

```mermaid
%%{init: {'themeVariables': {'fontSize': '32px', 'fontFamily': 'sans-serif'}, 'flowchart': {'htmlLabels': true, 'nodeSpacing': 50, 'rankSpacing': 80, 'wrappingWidth': 400, 'padding': 20}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 3: GenAI &amp; Agents</i><br/>&nbsp;<br/><b>Covered so far:</b> Module 1 (AI/ML Landscape through Spreadsheets), Module 2 (ML Workflow through Clustering, Model Selection &amp; Explainability), LLM Fundamentals (13.1), Calling LLMs with APIs (13.2), Prompt Engineering (14.1), Master Class: Vectors (14.2), Structured Outputs (14.3), Getting Started with LangChain (15.1), AI Workflows in LangChain (15.2), Master Class: Calculus (16.1), Embeddings &amp; Semantic Search (16.2), Vector Stores &amp; Retrieval (16.3), RAG Pipeline (17.1), AI Agents (17.2)<br/>This is Session 18.1 (13 of 14 in Module 3)"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Agentic RAG, Evaluation &amp; Guardrails</b><br/>&nbsp;<br/><i>The shift:</i> from a demo that seems to work <i>to</i> <b>a system you can measure and trust</b><br/>&nbsp;<br/>Retriever as a tool · Agentic RAG · RAGAS metrics<br/>Hallucination detection · Guardrails · Responsible AI"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Wrap a retriever as an agent tool, score a RAG system with<br/>RAGAS (answer correctness, context recall, faithfulness),<br/>catch hallucinations before they reach users, and design<br/>guardrails for privacy and reliability"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Brings Module 2's 'never grade your own homework' discipline<br/>to LLM systems"]
    RVAL["<b>Real-Life Value</b><br/>You can tell a manager how often the bot is right and<br/>grounded — with numbers, not vibes"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Agent Orchestration with LangGraph<br/><i>Turns the agent's hidden loop into an explicit flow you<br/>design</i>"]
    U1["<b>Later in Module 3</b><br/>Module 3 wrap-up"]
    U2["<b>Upcoming Modules</b><br/>The next module, per your course calendar<br/><i>Measuring and guarding AI applies to everything you build<br/>next</i>"]
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
