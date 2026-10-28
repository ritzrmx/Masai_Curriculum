# Mental Map — Text Embeddings & Semantic Search
> Academic Session 16.2 · Module 3: GenAI & Agents

```mermaid
%%{init: {'themeVariables': {'fontSize': '32px', 'fontFamily': 'sans-serif'}, 'flowchart': {'htmlLabels': true, 'nodeSpacing': 50, 'rankSpacing': 80, 'wrappingWidth': 400, 'padding': 20}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 3: GenAI &amp; Agents</i><br/>&nbsp;<br/><b>Covered so far:</b> Module 1 (AI/ML Landscape through Spreadsheets), Module 2 (ML Workflow through Clustering, Model Selection &amp; Explainability), LLM Fundamentals (13.1), Calling LLMs with APIs (13.2), Prompt Engineering (14.1), Master Class: Vectors (14.2), Structured Outputs (14.3), Getting Started with LangChain (15.1), AI Workflows in LangChain (15.2), Master Class: Calculus (16.1)<br/>This is Session 16.2 (9 of 14 in Module 3)"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Text Embeddings &amp; Semantic Search</b><br/>&nbsp;<br/><i>The shift:</i> from matching exact words <i>to</i> <b>matching meaning, even across languages</b><br/>&nbsp;<br/>sentence-transformers · HuggingFaceEmbeddings · Cosine &amp; dot product<br/>Semantic vs keyword · Embedding visualisation"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Generate embeddings locally for free, compare them with<br/>cosine or dot product similarity, explain when semantic<br/>search beats keyword search (and when it doesn't), and plot<br/>embeddings in 2D"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Vector stores (16.3), RAG (17.1) and agentic RAG (18.1) all<br/>search with today's embeddings"]
    RVAL["<b>Real-Life Value</b><br/>You can build search that finds 'payout delayed' when<br/>someone types 'where is my money'"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Chunking, Vector Stores &amp; Retrieval<br/><i>Scales from a dozen sentences to a whole handbook, searched<br/>in milliseconds</i>"]
    U1["<b>Later in Module 3</b><br/>RAG Pipeline · AI Agents · Agentic RAG, Evaluation &amp;<br/>Guardrails · LangGraph Orchestration"]
    U2["<b>Upcoming Modules</b><br/>The next module, per your course calendar<br/><i>Embeddings power search and retrieval in almost every AI<br/>product</i>"]
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
