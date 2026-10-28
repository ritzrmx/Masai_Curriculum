# Lecture Script: Generative AI — Building an AI Agent with LangChain
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 17.2 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can define custom LangChain tools with descriptions that drive correct selection, explain and trace the ReAct Thought → Action → Observation loop, build an agent with `create_react_agent` + `AgentExecutor` (and recognise `initialize_agent`), control it with `max_iterations` and `handle_parsing_errors`, and complete a mini-build: an FAQ Helpdesk agent with handbook search, partner stats and a payout calculator.

**Student profile at this point:** They built a RAG chain (17.1), the CSV copilot and FAQ bot (15.2), and know chain-of-thought (14.1) and "LLMs aren't calculators" (15.2). They've only built fixed-step pipelines. Likely wrong assumptions: "agents are smarter chains, so always use them," "the Thought lines are the model's real reasoning," and "more iterations means more reliable." Boredom risk: low — the ₹600 question finally gets answered end to end — but live agent runs can be slow or erratic, so keep the TA's recorded trace as a backup.

**Key outcome:** Students should leave asking, before building anything: "Are the steps fixed — chain — or does the question decide them — agent? If agent: what are my tools, how are they described, and what stops it running away?"

> 🎯 **The one sentence this session must land:** *An agent is an LLM that chooses its own next step from tools you describe — so the descriptions decide how smart it looks, and the limits you set decide how safe it is.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The ₹600 Question Needs Three Things" | 8 min | 8 min |
| Concept Block 1: LangChain Tools | 12 min | 20 min |
| Practical Block 1: Write the Tool Descriptions | 8 min | 28 min |
| Concept Block 2: The ReAct Pattern | 12 min | 40 min |
| Practical Block 2: Be the Agent — Paper ReAct | 8 min | 48 min |
| **BREAK** | 10 min | 58 min |
| Concept Block 3: AgentExecutor, create_react_agent & initialize_agent | 10 min | 68 min |
| Concept Block 4: Tool Selection & Multi-Step Loops | 8 min | 76 min |
| Concept Block 5: max_iterations & handle_parsing_errors | 8 min | 84 min |
| Practical Block 3: Mini-Build — FAQ Helpdesk Agent (TA Code) | 16 min | 100 min |
| Practical Block 4: Design a CSV Analyst Agent | 12 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "The ₹600 Question Needs Three Things" (8 min)

Open with this, verbatim-ish, with the partner's message from 13.2 and 14.1 on the board — "Why is my payout ₹600 less this week? My ID is P-20417.":

> "Our RAG bot from last session reads the handbook beautifully. Ask it this question. What happens?"

Pause. Ask the room:

> "What does the helpdesk actually need to answer this properly?"

(Steer to three things: P-20417's numbers, exact payout maths for both weeks, and the policy behind each part — three different tools.)

> "We could build a fixed chain — stats, calculate, handbook. But then 'How do I change my bank account?' also runs the calculator. What we really want is for the LLM to decide which tools to use. That's an agent."

**Pivot line:** "Up to now, you decided every step. Today, the LLM decides — and you decide what it's allowed to touch."

**Context for sessions ahead:** "18.1 makes the retriever a first-class agent tool and measures the agent's answers. 18.2 redraws this hidden loop as an explicit flowchart in LangGraph."

---

## Concept Block 1: LangChain Tools (12 min)

> "A new support agent can talk well, but she needs access to the payout system, the partner database and the policy binder. Each access is a **tool** — and each needs a label saying what it's for. A chain is a fixed thali; an agent is a waiter who decides what to bring."

```python
@tool
def calculate_weekly_payout(partner_id: str) -> str:
    """Calculate EXACT payout amounts for this week and last week with a breakdown.
    Use for any question about how much a partner earned or why a payout changed.
    Input: a partner ID like P-20417."""
    ...
```

> "Three ingredients: the name (the function name), the description (the docstring) and the input (the argument). `@tool` turns any Python function into a tool; `Tool(name=..., func=..., description=...)` does the same without the decorator. The curriculum calls this 'create_tool' — in LangChain, there's no single function by that name. Our three tools: `search_handbook` (the 17.1 retriever), `get_partner_stats` (a lookup) and `calculate_weekly_payout` (plain Python, because 15.2 taught us LLMs aren't calculators)."

### 🔴 The trap / highest-value moment
> "The LLM never sees your code — only the name and the description. Write this down: *a tool's description is its entire job interview — say what it does, what input it wants, and when to use it.*"

---

## Practical Block 1: Write the Tool Descriptions (8 min)

Give pairs three bad descriptions — "searches stuff", "gets data" and "payout tool" — and five minutes to rewrite them for `search_handbook`, `get_partner_stats` and `calculate_weekly_payout`. Show model answers: "Search the official partner handbook for policy and rules (payout schedule, bonuses, deductions, disputes, insurance, safety). Input: a short question."; "Look up a partner's raw numbers for this week and last week: orders, peak orders, cancellations, rain orders. Input: a partner ID like P-20417."; and "Calculate exact payout amounts with a full breakdown for both weeks; use for any question about how much was earned or why it changed. Input: a partner ID." Point out that the second and third now clearly differ — raw numbers vs calculated amounts — because overlapping descriptions are the top cause of wrong tool choices. Tool descriptions are prompts, so everything from 14.1 applies.

---

## Concept Block 2: The ReAct Pattern (12 min)

> "A detective doesn't solve a case in one leap. She thinks, acts, observes and thinks again."

Write the full ₹600 trace on the board:

```
Thought: I need his weekly payout breakdown.
Action: calculate_weekly_payout   Action Input: P-20417
Observation: Last week Rs 2,860 ... This week Rs 2,260 ...
Thought: Peak bonus fell Rs 300, deductions rose Rs 300. Check the deduction policy.
Action: search_handbook   Action Input: cancellation deduction policy
Observation: [1.3] Rs 100 deducted per verified cancellation...
Final Answer: Rs 600 lower: 20 fewer peak orders (Rs 300) + 3 cancellations (Rs 300, 1.3)...
```

> "**ReAct** — Reason plus Act. The Thought lines are 14.1's chain-of-thought; the difference is that each step can now do something and see a real result."

### 🔴 The trap / highest-value moment
> "The Thoughts read like reasoning, but they're generated text, like everything in 13.1. A model can write a sensible Thought and then pick the wrong tool. Write this down: *Thoughts are a debugging window, not a guarantee.*"

---

## Practical Block 2: Be the Agent — Paper ReAct (8 min)

In pairs, one student is the "agent" and the other the "tools", holding printouts of the handbook sections and P-33150's stats. The question: "I'm P-33150. Did I get my rain bonus this week, and how is it calculated?" The agent writes each Thought, Action and Action Input; the tools partner reads back only what the tool would return. A model trace: `get_partner_stats` (P-33150) → 12 rain orders this week; `search_handbook` (rain bonus) → [2.2] ₹10 per order during an active rain alert; Final Answer: "Yes — 12 rain-alert orders × ₹10 = ₹120 rain bonus this week (Section 2.2)." Some pairs will go to the calculator first; that's also valid, since its breakdown shows the rain line — agents can take different paths to the same right answer. If someone asks whether the agent should multiply 12 × 10 itself, say tiny sums usually come out right, but the safer design pushes maths into tools whenever it matters.

---

## BREAK (10 min)

---

## Concept Block 3: AgentExecutor, create_react_agent & initialize_agent (10 min)

> "The agent is the decision-maker. The **AgentExecutor** is the shift supervisor who runs the loop: she sends each decision to the right tool, brings back the result, enforces the rules and ends the shift."

```python
agent = create_react_agent(llm, tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                         max_iterations=6, handle_parsing_errors=True)
executor.invoke({"input": "Why is P-20417's payout Rs 600 less this week?"})
```

> "The ReAct prompt has four blanks: `{tools}`, `{tool_names}`, `{input}` and `{agent_scratchpad}` — every Thought, Action and Observation so far, the agent's working memory for this one question. Older code does it in one line: `initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)`. It's deprecated but everywhere, so recognise it; we prefer `create_react_agent` because you can see and edit the prompt."

### 🔴 The trap / highest-value moment
> "Turning `verbose` off while learning is debugging with your eyes closed. Write this down: *keep verbose=True until the agent behaves — the trace is how you see why it did something strange.*"

---

## Concept Block 4: Tool Selection & Multi-Step Loops (8 min)

> "A good waiter doesn't bring every dish in the kitchen. He brings what the order needs, in a sensible order."

Write on the board:

> "Change bank account?" → search_handbook
> "My payout this week? P-33150" → calculate_weekly_payout
> "My rain orders?" → get_partner_stats
> "Why ₹600 less? P-20417" → calculator → handbook
> "Tell me a joke" → no tool

> "The agent compares the question with the tool descriptions, then uses each observation to decide the next action. Good selection comes from distinct descriptions, a prompt saying when to use tools, and few tools — three well-described tools beat fifteen vague ones."

### 🔴 The trap / highest-value moment
> "A 'do everything' tool like `run_python(code)` gets used for everything — including things it shouldn't, the same danger as 15.2's CSV copilot debate. Write this down: *narrow tools are safer, easier to describe and easier to test.*"

---

## Concept Block 5: max_iterations & handle_parsing_errors (8 min)

> "A delivery app caps how many times an order can be reassigned. Without a cap, one confused order bounces around for a long time."

Write on the board:

> `max_iterations=6` → caps long loops (the default cap is 15 rounds) — each round is a paid LLM call
> `handle_parsing_errors=True` → a badly formatted reply goes back as an error to fix, instead of crashing

> "Ask 'What will P-20417 earn next month?' — no tool can answer the future, so a confused agent may call the calculator again and again. The cap stops it, and the helpdesk falls back to a human. And if the model writes 'I think the answer is...' without 'Final Answer:', the flag sends the error back and the model fixes its format."

### 🔴 The trap / highest-value moment
> "'Let's set max_iterations=50 so it never gives up.' At 50,000 questions a day and one paid call per step — 13.1's cost formula — a looping agent becomes your biggest bill. Write this down: *most good answers take 1–4 steps; cap it at 4–8 and fall back to a human.*"

---

## Practical Block 3: Mini-Build — FAQ Helpdesk Agent (TA Code) (16 min)

**Handoff line (must match TA code file's opening comment):** "Mini-build — an FAQ Helpdesk agent that can search the handbook, look up a partner's stats and calculate payouts, and finally answers the ₹600 question by itself."

Hand off to `ta-code - Session 17.2 - Building an AI Agent with LangChain.py` (with `partner_handbook.txt` alongside), narrating each `# --- EXPLAIN ---` block aloud:

1. Show the three tools — read each description aloud, and call the calculator directly once to show its output
2. Show the ReAct prompt — point at the four blanks
3. Run three questions with `verbose=True` — for each, ask the class to predict the tools before running
4. Follow the ₹600 question's trace step by step, and compare it with the paper trace from Practical Block 2
5. Run the capped executor on "next month" — show the iteration-limit stop
6. Run the classic `initialize_agent` one-liner

💬 Expect a comment: "It took a different path from the one on the board!" Welcome it. Say: "As long as the final answer is right and grounded, different paths are fine. If a path is wasteful — calling the same tool twice — that's a description or prompt problem to fix."

---

## Practical Block 4: Design a CSV Analyst Agent (12 min)

In pairs, students spend six minutes designing the alternative mini-build: a CSV Analyst agent for partner-ops over 15.2's 200-partner table (orders, rating, months active, zone, churned). They specify two or three tools with one-line descriptions and input formats, one question that needs two tools, and a `max_iterations` value with a reason. A model answer: `describe_columns` ("lists the table's columns, their meaning and allowed values"), `run_query_plan` ("computes a metric with an aggregation, optionally grouped by zone or churned, using Pandas; input: a JSON QueryPlan" — 15.2's copilot as a tool) and `search_handbook`; a two-tool question such as "Which zone has the most churned partners, and what's their average rating?" (`run_query_plan` twice); and `max_iterations=5`. Point out that the CSV copilot became a tool — chains don't disappear when you build agents, they become the agent's hands. If someone proposes a `run_pandas_code` tool instead, revisit the 15.2 debate: narrow tools are safer.

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| Tools | `@tool` or `Tool(...)`; the description is all the LLM sees |
| ReAct | Thought → Action → Observation, repeat → Final Answer |
| AgentExecutor | Runs the loop; `create_react_agent` preferred; `initialize_agent` is classic |
| Tool selection | Matches the question to descriptions — keep them distinct and few |
| Safety controls | `max_iterations` 4–8, `handle_parsing_errors=True`, `verbose` while learning |

Close on the thesis line: "An agent is an LLM that chooses its own next step from tools you describe — so the descriptions decide how smart it looks, and the limits you set decide how safe it is."

**Bridge to next session:** "Our agent answered the ₹600 question. But how often is it right? Did it stick to the handbook or add details? And what stops a partner asking for someone else's payout? Session 18.1 — Agentic RAG, Evaluation & Guardrails — turns the retriever into a proper agent tool, measures the system with RAGAS, and adds guardrails for hallucination, privacy and reliability."

---

## Q&A & Doubt Solving (4 min)

**Q: Can an agent call two tools at once?**
→ Text-based ReAct agents call one tool per step. Newer tool-calling agents can request several in one step; the loop idea is the same.

**Q: How does the agent remember earlier tool results?**
→ Through `{agent_scratchpad}` — every Thought, Action and Observation is pasted back into the prompt on the next step, which is also why long agent runs get expensive.

**Q: Why does each tool take just one string?**
→ The classic ReAct format passes one "Action Input" string. Multi-argument tools need a structured-tool agent; one ID or one question per tool is simplest for now.

**Q: What if the model invents a tool name?**
→ The executor reports it as an invalid tool in the next observation, and the model usually corrects itself.

**Q: Isn't it risky to let an AI choose actions?**
→ Yes — which is why tools should be narrow (read-only lookups, safe calculations), loops capped, and anything with real consequences, like refunds or account changes, gated behind a human. That's 18.1's guardrails.

---

## Instructor Notes
- **Words not yet earned:** agentic RAG and `create_retriever_tool` (18.1 — today we hand-wrap the retriever), RAGAS and guardrails (18.1), StateGraph, nodes and edges (18.2), multi-agent systems.
- **Biggest risk in this session:** a live agent run going sideways. Keep the TA's recorded verbose trace of the ₹600 question as a backup; if a run fails, treat it as a teaching moment and diagnose it from the trace.
- **Board management:** keep the three tool descriptions and the ₹600 ReAct trace on the board all session; add the safety settings in Concept Block 5.
- **Common confusions, numbered:**
  1. Using agents where a fixed chain would do
  2. Vague or overlapping tool descriptions
  3. Treating Thoughts as guaranteed reasoning
  4. Letting the LLM do maths instead of a tool
  5. Very high `max_iterations`
  6. Turning off `verbose` while debugging
  7. Expecting a LangChain function literally named "create_tool"
- **Cross-references:** Session 14.1's chain-of-thought becomes ReAct Thoughts; Session 15.2's CSV copilot becomes a tool; Session 17.1's retriever becomes `search_handbook`; Session 18.1 formalises it with `create_retriever_tool` and evaluates it; Session 18.2 rebuilds the loop in LangGraph.
- **Local/cultural context notes:** the ₹600 story has threaded from 13.2 through 14.1 and 14.3 — this is where it's finally answered end to end, so make a moment of it. The detective and waiter analogies land well; the partner stats in the TA code are synthetic.
