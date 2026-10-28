# Lecture Script: Generative AI — Agent Orchestration with LangGraph
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 18.2 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can design a multi-step agent workflow as a LangGraph `StateGraph` with typed state, nodes and edges; implement conditional edges for branching and a counter-controlled retry loop; compile and run the graph and read its final state; and compare LangGraph with LangChain's `AgentExecutor`, justifying when to use each.

**Student profile at this point:** They have the full Module 3 toolkit: API calls, prompts, structured outputs, chains, embeddings, vector stores, RAG, a ReAct agent, RAGAS evaluation and code-level guardrails (18.1). They've felt AgentExecutor's limits: a hidden loop, and rules that exist only as prompt requests. Likely wrong assumptions: "LangGraph is just a fancier agent," "graphs replace LLMs," and "newer is always better." Boredom risk: end-of-module fatigue — frame today as the finale, the whole module in one flowchart.

**Key outcome:** Students should leave asking, for any AI system: "Which rules must be guaranteed — and are they edges in a graph, or just sentences in a prompt?"

> 🎯 **The one sentence this session must land:** *LangGraph turns your AI system into a flowchart you control — the LLM still does the thinking inside each box, but the arrows, branches and retries are yours, so the rules that matter are guaranteed rather than requested.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Rule the Agent Forgot" | 8 min | 8 min |
| Concept Block 1: StateGraph & State Management | 12 min | 20 min |
| Concept Block 2: Nodes, Edges, add_node, add_edge & compile() | 14 min | 34 min |
| Practical Block 1: Draw the Helpdesk Graph | 8 min | 42 min |
| Concept Block 3: Conditional Edges | 10 min | 52 min |
| **BREAK** | 10 min | 62 min |
| Concept Block 4: Retry Handling Across Nodes | 10 min | 72 min |
| Practical Block 2: Live Coding Demo (TA Code) | 16 min | 88 min |
| Concept Block 5: LangGraph vs AgentExecutor | 9 min | 97 min |
| Practical Block 3: Choose the Orchestrator | 8 min | 105 min |
| Practical Block 4: Module 3 in One Trace | 7 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "The Rule the Agent Forgot" (8 min)

Open with this, verbatim-ish, with a realistic AgentExecutor trace on screen:

```
Question: customer ne gate pe dhamki di, mera payout bhi kam hai. P-20417
Thought: The partner mentions a payout issue. Let me calculate.
Action: calculate_weekly_payout
...
Final Answer: Your payout is Rs 600 lower because...
```

> "Read it carefully. A partner says a customer is threatening him at the gate — and our agent helpfully calculates his payout."

Pause. Ask the room:

> "We wrote 'safety issues must go to a human' in the system prompt. Why didn't it happen?"

(Answers: the model focused on the payout; prompts are requests, not guarantees; it chose its own steps.)

> "In 18.1 we said critical rules belong in code. But inside AgentExecutor the loop is hidden — where would that code even go? Today we take the loop out of the black box and draw it as a flowchart we control."

**Pivot line:** "Module 3's final step: from an agent that decides everything, to a system where you decide the flow and the LLM does the thinking inside each box."

**Context for sessions ahead:** "This graph is the finished shape of the helpdesk for this module — and the pattern most production AI systems use."

---

## Concept Block 1: StateGraph & State Management (12 min)

> "A hospital patient file travels from reception to the nurse, the doctor and the pharmacy. Each person reads what they need and adds their part; nobody re-asks the patient's name."

Write on the board:

```python
class HelpdeskState(TypedDict):
    partner_id: str
    question: str
    route: str
    context: List[str]
    answer: str
    check_passed: bool
    attempts: int

graph = StateGraph(HelpdeskState)
```

> "That's the patient file — the **state**: one typed dictionary every step can read and update. `TypedDict` is a lighter cousin of 14.3's Pydantic models. Data used to move between steps by matching variable names (15.1) or in the agent's text scratchpad (17.2); now it's one typed state you can inspect after every step."

### 🔴 The trap / highest-value moment
> "Stuffing everything into the state 'just in case' makes it unreadable when you're debugging. Write this down: *the state holds only what later nodes need.*"

---

## Concept Block 2: Nodes, Edges, add_node, add_edge & compile() (14 min)

> "Each desk in the hospital is a **node** — a plain Python function: state in, changes out. The arrows painted on the floor are **edges** — fixed directions."

```python
def retrieve(state):
    docs = retriever.invoke(state["question"])
    return {"context": [d.page_content for d in docs]}     # only what changed

graph.add_node("retrieve", retrieve)
graph.add_edge(START, "guard")
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", "check")
app = graph.compile()
final_state = app.invoke({...})
```

> "Our seven nodes call things you've already built: `guard` (18.1's guardrails), `refuse`, `human`, `retrieve` (16.3), `answer` (17.1's RAG prompt), `check` (18.1's number check) and `fallback`. `START` and `END` mark the entry and exit, `compile()` validates and builds the graph, and `invoke()` returns the whole final state, not just the answer. Bonus: `app.get_graph().draw_mermaid()` prints your graph as mermaid — the same format as every mental map in this course."

### 🔴 The trap / highest-value moment
> "A node returns only the keys it changed — return nothing, or forget a key, and the next node reads stale data. And every node needs a way out. Write this down: *nodes return changes; every path must reach END.*"

---

## Practical Block 1: Draw the Helpdesk Graph (8 min)

Read out the requirements and give pairs five minutes to draw the graph on paper, labelling which arrows are decisions: always run the guardrails first; refuse blocked messages and send safety issues to the human team; otherwise retrieve, then answer; check the answer, retry once if it fails, and fall back to a human if it fails again. Reveal the graph — START → guard → (ok → retrieve → answer → check → done, retry or give up) / (block → refuse) / (escalate → human) → END — and count the decision points: two, after `guard` and after `check`. Those are exactly the two conditional edges we write next; everything else is a plain arrow. If someone suggests a second safety check after answering, say that's one more node and one more conditional edge — graphs make adding rules like that easy and visible.

---

## Concept Block 3: Conditional Edges (10 min)

> "At hospital triage, the nurse looks at the patient and decides: emergency room, ward or home. Same desk, different next stop."

```python
def route_after_guard(state):
    return state["route"]                   # "ok" / "block" / "escalate"

graph.add_conditional_edges("guard", route_after_guard,
                            {"ok": "retrieve", "block": "refuse", "escalate": "human"})
```

> "A tiny routing function reads the state and returns a name; the mapping says which node that name means. Now replay the opening: 'customer ne gate pe dhamki di'. `guard` sees a safety word, sets `route = 'escalate'`, and the flow goes to `human`, then END. The LLM never even runs. That's not a request in a prompt — it's an arrow, and it can't be skipped."

### 🔴 The trap / highest-value moment
> "Don't put real work in routing functions — no LLM calls, no database lookups. Write this down: *routers only read the state and return a name; work happens in nodes.*"

---

## BREAK (10 min)

---

## Concept Block 4: Retry Handling Across Nodes (10 min)

> "A factory quality inspector sends a faulty part back to the machine once, with adjusted settings. If it's still faulty, it goes to a human technician. It doesn't loop forever."

```python
def route_after_check(state):
    if state["check_passed"]:
        return "done"
    return "retry" if state["attempts"] < 2 else "give_up"

graph.add_conditional_edges("check", route_after_check,
                            {"done": END, "retry": "answer", "give_up": "fallback"})
```

Walk the retry story on the board:

> 1. `answer`: "Accident cover is ₹5,00,000" → attempts = 1
> 2. `check`: 500000 isn't in the sources → fail
> 3. route: retry → back to `answer`, which sees attempts > 0 and adds "quote amounts exactly"
> 4. `answer`: "₹2,00,000 on active orders (4.2)" → attempts = 2 → `check` passes → END

> "This is **state across nodes**: `answer` knows it's a retry because `attempts` travelled through the state. In 13.2 we retried the same request after a 429; here we retry with a changed instruction after a quality failure."

### 🔴 The trap / highest-value moment
> "A retry edge with no counter is 17.2's runaway agent all over again. LangGraph has a built-in recursion limit, but hitting it ends in an error, not a polite fallback. Write this down: *every loop gets a counter in the state and a give-up path to a human.*"

---

## Practical Block 2: Live Coding Demo (TA Code) (16 min)

**Handoff line (must match TA code file's opening comment):** "All of Module 3 in one flowchart — guardrails, handbook retrieval, the answer, the number check, one retry, and a human fallback — built as an explicit LangGraph flow."

Hand off to `ta-code - Session 18.2 - Agent Orchestration with LangGraph.py` (with `partner_handbook.txt` alongside), narrating each `# --- EXPLAIN ---` block aloud:

1. Show the `HelpdeskState` TypedDict — the patient file
2. Show the seven node functions — name the session each one comes from (guardrails 18.1, retrieval 16.3, RAG prompt 17.1, number check 18.1)
3. Build the graph — `add_node`, `add_edge`, two `add_conditional_edges` calls and `compile()`
4. Print `draw_mermaid()` and paste it into a mermaid viewer on screen — it looks like our mental maps
5. Run four journeys, reading the final state each time: the happy path, a privacy block, a safety escalation, and the forced-hallucination retry (attempts = 2)

💬 Expect a question: "In 18.1 'accident' triggered the safety escalation, but here the insurance question went through. Why?" Welcome it. Say: "Sharp eyes. We dropped 'accident' from the safety words because it was escalating ordinary policy questions — 18.1's false-positive lesson. In a graph, that rule lives in one node you can see and tune; a real system would use a smarter classifier node."

---

## Concept Block 5: LangGraph vs AgentExecutor (9 min)

> "A freelancer with a goal versus an employee following a documented process. Both are useful — for different jobs."

Write on the board:

> AgentExecutor: the LLM picks every step · rules are prompt requests · retries = `max_iterations` · text scratchpad · little setup → prototypes, open-ended tool use
> LangGraph: you design the steps (LLMs work inside nodes) · rules guaranteed by edges · custom retry loops with counters · typed state · more setup → production flows with rules and hand-offs

> "And they combine: put the 17.2 agent inside an `answer` node, and the graph guarantees the guardrails before and the checks after."

### 🔴 The trap / highest-value moment
> "'LangGraph is newer, so always use it.' For a quick prototype with three tools and no hard rules, a graph is overhead. Write this down: *reach for a graph when you need guarantees — branches, retries, hand-offs — not by default.*"

---

## Practical Block 3: Choose the Orchestrator (8 min)

Rapid fire — chain, AgentExecutor or LangGraph, with a one-line reason: extract a ticket from every message (chain — same steps every time); a weekend prototype that answers anything with three tools (AgentExecutor — fast and flexible); the production helpdesk where safety must always reach a human (LangGraph — guaranteed routing); draft a reply, check it, retry once, then escalate (LangGraph — a retry loop with a counter); a CSV analyst for one manager's ad-hoc questions (AgentExecutor — open-ended and low risk); a refund flow that needs human approval above ₹500 (LangGraph — a conditional hand-off). Sum it up: anything involving money, safety or approvals, think graph; anything exploratory and low-risk, an agent is fine. If someone asks whether a graph can hold several agents, yes — each node can be its own agent, which is multi-agent orchestration, a natural next step beyond this module.

---

## Practical Block 4: Module 3 in One Trace (7 min)

Put the happy-path final state on screen and go round the room: for each node, a student names the session that taught the idea inside it. `guard` — 18.1's guardrails, with the injection idea from 14.3. `retrieve` — 16.2's embeddings and 16.3's chunking and Chroma. `answer` — 13.1's temperature, 13.2's API call, 14.1's prompt design and 17.1's RAG prompt. `check` — 18.1's hallucination detection. `fallback` — 15.2's FAQ fallback line and 17.1's "I couldn't find this". The retry — 13.2's retries and 17.2's iteration limits, now an explicit loop. Close quietly: "Fourteen sessions, one flowchart, and every box is something you built. That's what 'GenAI engineer' means — knowing which piece goes in which box."

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| StateGraph & state | One typed dictionary; keep only what later nodes need |
| Nodes & edges | Nodes return changes; fixed edges for fixed paths; every path reaches END |
| compile() & invoke() | Validate, run, read the whole final state; `draw_mermaid()` to see it |
| Conditional edges | Tiny routers return a name; branches are guarantees, not requests |
| Retry handling | A counter in the state + a loop edge + a give-up path |
| LangGraph vs AgentExecutor | Guarantees and hand-offs → graph; open-ended prototypes → agent |

Close on the thesis line: "LangGraph turns your AI system into a flowchart you control — the LLM still does the thinking inside each box, but the arrows, branches and retries are yours, so the rules that matter are guaranteed rather than requested."

**Bridge to next session:** "That completes Module 3. You started with 'what is a token?' and you're finishing with a guarded, evaluated, orchestrated helpdesk built from real components. Whatever the course calendar brings next, this graph is the skeleton you'll keep reusing."

---

## Q&A & Doubt Solving (4 min)

**Q: Can LangGraph pause for a human and then continue?**
→ Yes — LangGraph supports checkpoints and human-in-the-loop interrupts: the graph saves its state, waits for approval, then resumes. It's a natural extension of today's `human` node.

**Q: How is this different from SequentialChain in 15.1?**
→ SequentialChain only runs steps in a straight line. LangGraph adds branches, loops and a shared typed state, which retries and escalations need.

**Q: Does LangGraph make the system slower?**
→ The graph itself adds almost no time — the LLM calls inside nodes dominate. It's often faster, because routes like `refuse` and `human` skip the LLM entirely.

**Q: Where does conversation history live in a graph?**
→ In the state — for example a `messages` list that nodes append to. LangGraph has helpers for exactly this.

**Q: Should the number check be its own node or inside `answer`?**
→ Its own node. Then you can see in the final state whether it passed, change it independently, and route on its result.

---

## Instructor Notes
- **Words not yet earned / beyond scope:** checkpointers and persistence in depth, interrupts, subgraphs, multi-agent supervisors, streaming, reducers on state keys.
- **Biggest risk in this session:** end-of-module fatigue. Use the opening's forgotten safety rule for energy and the Module-3-in-one-trace exercise as the emotional close.
- **Board management:** keep the full helpdesk graph drawn large on the board all session, with the state TypedDict beside it; add the AgentExecutor-vs-LangGraph comparison in Concept Block 5.
- **Common confusions, numbered:**
  1. Thinking LangGraph replaces LLMs or LangChain
  2. Returning the whole state, or nothing, from a node
  3. Nodes with no path to END
  4. Heavy work inside routing functions
  5. Retry loops without a counter
  6. Choosing LangGraph by default for simple prototypes
- **Cross-references:** every node maps to a prior session — 13.2 (retries), 15.1 (SequentialChain), 16.3 (retriever), 17.1 (RAG prompt), 17.2 (AgentExecutor and iteration limits), 18.1 (guardrails and the number check) — and the mental-map mermaid format returns in `draw_mermaid()`.
- **Local/cultural context notes:** the Gachibowli safety message from 14.1 makes a strong opening callback, and the hospital-file and triage analogies land well. Close by naming the 11:40 pm partner from 13.1 — he now has a helpdesk that's grounded, measured and safe.
