# Lecture Script: Agent Orchestration with LangGraph
> **Instructor Reference** — Module 3: GenAI & Agents | Session 14 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students design a multi-step agent workflow using LangGraph's `StateGraph` with explicitly defined nodes and transitions, implement conditional edges to handle branching logic and retry handling across agent steps, and compare LangGraph orchestration with LangChain's `AgentExecutor`, justifying when to use each. This is the final session of Module 3 — and of the entire course — so it closes with a deliberate look back across everything Module 3 built.

**Student profile at this point:** Students have built chains (Sessions 6-7), RAG pipelines (Session 11), ReAct agents with `AgentExecutor` (Session 12), and agentic RAG with evaluation and guardrails (Session 13). Every agent so far has used the SAME underlying loop structure: a flat Thought/Action/Observation cycle, with safety controls (`max_iterations`, `handle_parsing_errors`) bolted on as settings. Today introduces a fundamentally different way to structure multi-step AI systems: an explicit graph of named steps and transitions, where branching and retry logic are first-class parts of the workflow's DESIGN, not just safety limits on an otherwise-opaque loop.

**Key outcome:** Every student can define a `StateGraph` with a typed state, add nodes representing discrete workflow steps, wire them together with `add_edge` and `add_conditional_edges` to implement real branching logic, build in explicit retry handling for a step that can fail, compile and run the graph, and give a clear, reasoned answer to "when would I reach for LangGraph instead of `AgentExecutor`, and why."

**Dataset for this session:** None required from disk — a small inline customer-request classification and routing workflow (route to "refund," "technical," or "general" handling) serves as this session's running example, built entirely from inline functions and dictionaries.

**API note for this script:** All `StateGraph`, `add_node`, `add_edge`, `add_conditional_edges`, and `compile()` usage in this script reflects LangGraph's current, documented public API. The STRUCTURAL/mechanical behavior of these APIs (how nodes execute, how conditional edges route execution, what `.invoke()` returns) is stated as documented fact. Any LLM-generated classification decision, reasoning text, or final response is inherently non-deterministic and is marked **"Example output (illustrative — actual LLM output will vary run to run)"** throughout, since this script is not executed against a live paid API key. Deterministic routing/retry behavior driven by plain Python conditions (not an LLM call) is stated as fact, since it follows fixed code logic.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Why a Graph, Not Just a Loop | 10 min | 0:10 |
| SEGMENT 2: `StateGraph` Fundamentals — State, Nodes, Edges | 25 min | 0:35 |
| SEGMENT 3: Conditional Edges — Real Branching Logic | 20 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Retry Handling as a First-Class Graph Pattern | 20 min | 1:25 |
| SEGMENT 5: LangGraph vs. `AgentExecutor` — When to Use Each | 15 min | 1:40 |
| SEGMENT 6: Lab — A Branching, Retrying Support-Routing Graph | 15 min | 1:55 |
| SEGMENT 7: Course Wrap-Up & Final Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Why a Graph, Not Just a Loop (10 min)

### The Hook (5 min)

**Say:** *"Every agent we've built so far — Session 12's helpdesk, Session 13's agentic RAG — follows the exact same internal shape: a loop that keeps going Thought, Action, Observation, Thought, Action, Observation, until the model decides to stop. That's powerful, but notice what you DON'T have visibility into from the outside: you can't easily say 'always validate the input FIRST, no matter what the model decides,' or 'if step 3 fails, retry it up to 2 times before giving up, THEN fall back to a human,' or 'if the request is a refund, go this way; if it's technical, go that way' — as an explicit, inspectable part of the workflow's structure, rather than hoping the model's own reasoning happens to do the right thing."*

**Say:** *"Today introduces LangGraph, a library built specifically to let you draw that structure explicitly — as an actual directed graph of named steps and the rules for moving between them — then let an LLM fill in the SMART parts within that structure, rather than owning the entire control flow itself."*

### Why This Session Matters (5 min)

**Say:** *"Think of the shift this way: `AgentExecutor` is like handing someone a toolbox and a goal and trusting their judgment on what order to use tools in. LangGraph is like handing someone a flowchart with clearly marked decision points — SOME of which the LLM fills in with judgment, but the overall shape, the branches, and the retry logic are things YOU designed and can verify, test, and reason about independently of what the model decides at runtime. Neither approach is strictly 'better' — today's final segment makes that comparison explicit — but they solve genuinely different problems."*

**Learning contract for today — write on board:**

- Define a `StateGraph` with typed state, nodes, and edges
- Implement conditional edges for real branching logic
- Build explicit retry handling as part of a graph's own structure
- Compare LangGraph and `AgentExecutor`, and justify when each is the better choice

---

## SEGMENT 2: `StateGraph` Fundamentals — State, Nodes, Edges (25 min)

### Defining the State (7 min)

**Say:** *"Everything in a LangGraph workflow revolves around a shared STATE — a single typed object every node reads from and writes updates to as execution moves through the graph. Think of it as the 'shared notebook' every step in the workflow can read and add notes to."*

**Live-code:**

```python
from typing import TypedDict, Optional

class SupportState(TypedDict):
    request_text: str
    category: Optional[str]
    response: Optional[str]
    attempts: int

initial_state: SupportState = {
    "request_text": "I was charged twice for my CloudNest subscription this month.",
    "category": None,
    "response": None,
    "attempts": 0,
}
print(initial_state)
```

**Example output (actual — deterministic, since this is a plain Python dict literal with no LLM call involved):**
```
{'request_text': 'I was charged twice for my CloudNest subscription this month.', 'category': None, 'response': None, 'attempts': 0}
```

**Say:** *"`TypedDict` gives us a clear, typed CONTRACT for what fields exist in state and what types they hold — `request_text` is set from the start, while `category`, `response`, and `attempts` start empty or at zero and get filled in as the workflow runs. Every single node we write next will take this state in, and return updates to merge back into it."*

### Defining Nodes (10 min)

**Say:** *"A NODE is just a Python function: it takes the current state, does some work — which might be an LLM call, might be plain logic, might be another tool entirely — and returns a dict of the fields it wants to UPDATE in state. Let's build our first node: classifying the incoming request."*

**Live-code:**

```python
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    temperature=0,
)

def classify_request(state: SupportState) -> dict:
    prompt = f"""Classify this customer request into exactly one category:
REFUND, TECHNICAL, or GENERAL. Reply with only the category word.

Request: {state['request_text']}"""
    result = llm.invoke(prompt)
    category = result.content.strip().upper()
    return {"category": category}

update = classify_request(initial_state)
print(update)
```

**Example output (illustrative — actual LLM output will vary run to run in exact phrasing, but given this request explicitly describes a double billing charge, "REFUND" is the expected and realistic classification outcome):**
```
{'category': 'REFUND'}
```

**Say:** *"Notice the function's RETURN value is just the fields it's updating — `{'category': 'REFUND'}` — not the entire state object. LangGraph merges this update into the full state automatically once this node runs inside the actual graph; we're testing the function standalone here first, before wiring it in, exactly the same instinct as Session 12's testing a tool with `.invoke()` before assembling the full agent."*

### Building the Graph — Nodes and Edges (8 min)

**Say:** *"Now let's actually build the graph: register nodes, then define the EDGES — the fixed paths execution follows between them."*

**Live-code:**

```python
from langgraph.graph import StateGraph, END

def respond_general(state: SupportState) -> dict:
    return {"response": f"Thanks for reaching out. A general support agent will follow up on: {state['request_text']}"}

graph_builder = StateGraph(SupportState)
graph_builder.add_node("classify", classify_request)
graph_builder.add_node("respond", respond_general)

graph_builder.set_entry_point("classify")
graph_builder.add_edge("classify", "respond")
graph_builder.add_edge("respond", END)

graph = graph_builder.compile()

result = graph.invoke(initial_state)
print(result)
```

**Example output (illustrative — actual LLM output will vary run to run for the `category` field classified by the LLM-backed `classify` node, but the overall STRUCTURE — a final state dict containing all four `SupportState` fields, with `response` set by the `respond` node after `classify` runs — reflects documented, deterministic `StateGraph` execution behavior):**
```
{'request_text': 'I was charged twice for my CloudNest subscription this month.', 'category': 'REFUND', 'response': 'Thanks for reaching out. A general support agent will follow up on: I was charged twice for my CloudNest subscription this month.', 'attempts': 0}
```

**Say:** *"`set_entry_point("classify")` says execution starts at the `classify` node. `add_edge("classify", "respond")` is a FIXED, unconditional transition: once `classify` finishes, ALWAYS go to `respond` next, no model judgment involved in that transition itself. `add_edge("respond", END)` says the graph finishes after `respond`. `.compile()` turns this definition into an actually-runnable graph object, and `.invoke(initial_state)` runs it start to finish, returning the final merged state. Notice this graph, as built so far, doesn't actually USE the `category` it classified — every request gets the same generic `respond_general` handling. SEGMENT 3 fixes exactly that, with real branching."*

### Comprehension Check (included via quick verbal check) 

---

## SEGMENT 3: Conditional Edges — Real Branching Logic (20 min)

### Building Category-Specific Response Nodes (6 min)

**Live-code:**

```python
def respond_refund(state: SupportState) -> dict:
    return {"response": f"Refund request received: '{state['request_text']}'. Routed to billing team, response within 24 hours."}

def respond_technical(state: SupportState) -> dict:
    return {"response": f"Technical issue received: '{state['request_text']}'. Routed to technical support queue."}

def respond_general_v2(state: SupportState) -> dict:
    return {"response": f"General inquiry received: '{state['request_text']}'. A support agent will follow up shortly."}
```

### Writing the Routing Function (8 min)

**Say:** *"A CONDITIONAL edge is a function that reads the current state and returns the NAME of whichever node should run next — this is where real branching logic lives, as actual Python code we can read, test, and reason about, not something buried inside an LLM's own freeform reasoning."*

**Live-code:**

```python
def route_by_category(state: SupportState) -> str:
    category = state.get("category", "GENERAL")
    if category == "REFUND":
        return "respond_refund"
    elif category == "TECHNICAL":
        return "respond_technical"
    else:
        return "respond_general"

branching_builder = StateGraph(SupportState)
branching_builder.add_node("classify", classify_request)
branching_builder.add_node("respond_refund", respond_refund)
branching_builder.add_node("respond_technical", respond_technical)
branching_builder.add_node("respond_general", respond_general_v2)

branching_builder.set_entry_point("classify")
branching_builder.add_conditional_edges(
    "classify",
    route_by_category,
    {
        "respond_refund": "respond_refund",
        "respond_technical": "respond_technical",
        "respond_general": "respond_general",
    },
)
branching_builder.add_edge("respond_refund", END)
branching_builder.add_edge("respond_technical", END)
branching_builder.add_edge("respond_general", END)

branching_graph = branching_builder.compile()

result = branching_graph.invoke(initial_state)
print(result["category"])
print(result["response"])
```

**Example output (illustrative for `category`, since it's classified by the LLM-backed `classify` node — actual LLM output will vary run to run, but given this request's clear double-billing description, "REFUND" is the expected and realistic classification; GIVEN that classification, routing to `respond_refund` and producing its exact templated response is deterministic, documented `add_conditional_edges` behavior, not LLM-generated):**
```
REFUND
Refund request received: 'I was charged twice for my CloudNest subscription this month.'. Routed to billing team, response within 24 hours.
```

**Say:** *"Walk through the mechanism carefully: `add_conditional_edges("classify", route_by_category, {...})` says 'after the `classify` node runs, call `route_by_category` with the current state, and whatever STRING it returns, look that string up in this mapping dict to decide which node runs next.' The mapping dict's keys are `route_by_category`'s possible return values; its values are the actual node names to jump to. This is the real branching power today's session is about: the LLM decides the CONTENT of the classification, but the actual ROUTING DECISION — which path the workflow takes — is governed by our own explicit, testable Python function, not buried inside the model's own internal reasoning the way it was in Session 12's `AgentExecutor`."*

### Comprehension Check (6 min)

1. *"What's the difference between `add_edge` and `add_conditional_edges`?"* (`add_edge` is a fixed, unconditional transition — always go from node A to node B; `add_conditional_edges` calls a routing function against the current state and uses its return value to decide which of several possible next nodes to go to.)
2. *"In `route_by_category`, what would happen if `state['category']` came back as something unexpected, like `'BILLING'` instead of one of our three expected categories?"* (It falls through to the `else` branch, routing to `respond_general` — a deliberate, explicit default rather than an undefined/crashing case, an important defensive-coding habit.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to sketch, on paper, a simple box-and-arrow diagram of the branching graph just built — `classify` branching into three possible response nodes. Come back ready to extend it with a RETRY path for a step that might fail.

---

## SEGMENT 4: Retry Handling as a First-Class Graph Pattern (20 min)

### A Step That Can Genuinely Fail (6 min)

**Say:** *"Let's make this realistic: imagine `classify_request` occasionally returns something that ISN'T one of our three expected categories — a malformed or unexpected LLM response, similar in spirit to Session 5's `ValidationError` discussion. Instead of silently routing to a default, let's build EXPLICIT retry logic as part of the graph itself."*

**Live-code:**

```python
class RetryableState(TypedDict):
    request_text: str
    category: Optional[str]
    response: Optional[str]
    attempts: int

VALID_CATEGORIES = {"REFUND", "TECHNICAL", "GENERAL"}

def classify_with_tracking(state: RetryableState) -> dict:
    prompt = f"""Classify this customer request into exactly one category:
REFUND, TECHNICAL, or GENERAL. Reply with only the category word.

Request: {state['request_text']}"""
    result = llm.invoke(prompt)
    category = result.content.strip().upper()
    return {"category": category, "attempts": state["attempts"] + 1}
```

### Writing the Retry-or-Proceed Conditional Edge (8 min)

**Live-code:**

```python
def check_classification(state: RetryableState) -> str:
    if state["category"] in VALID_CATEGORIES:
        return "valid"
    elif state["attempts"] < 3:
        return "retry"
    else:
        return "give_up"

def give_up_node(state: RetryableState) -> dict:
    return {"response": "Unable to classify this request automatically after 3 attempts -- routing to a human agent for manual triage."}

retry_builder = StateGraph(RetryableState)
retry_builder.add_node("classify", classify_with_tracking)
retry_builder.add_node("respond_refund", respond_refund)
retry_builder.add_node("respond_technical", respond_technical)
retry_builder.add_node("respond_general", respond_general_v2)
retry_builder.add_node("give_up", give_up_node)

retry_builder.set_entry_point("classify")
retry_builder.add_conditional_edges(
    "classify",
    check_classification,
    {
        "valid": "classify",   # placeholder -- replaced by a second-level route below
        "retry": "classify",
        "give_up": "give_up",
    },
)
```

**Say, pausing on this intermediate step:** *"Wait — I want to flag something real here, not paper over it: 'valid' needs to go to the RIGHT response node based on category, not back to `classify`. A single conditional edge can only branch to one of its mapped destinations, so handling BOTH 'is classification valid or should we retry' AND 'if valid, which specific category' in one function would make `check_classification` do two jobs at once. The cleaner graph design is to chain two decisions: one conditional edge decides retry vs. proceed; if it proceeds, we reuse SEGMENT 3's `route_by_category` as a SECOND conditional edge from a small pass-through step. Let's fix this properly."*

**Live-code, the corrected graph:**

```python
def route_after_classification(state: RetryableState) -> str:
    if state["category"] not in VALID_CATEGORIES:
        if state["attempts"] < 3:
            return "retry"
        return "give_up"
    if state["category"] == "REFUND":
        return "respond_refund"
    elif state["category"] == "TECHNICAL":
        return "respond_technical"
    else:
        return "respond_general"

retry_builder = StateGraph(RetryableState)
retry_builder.add_node("classify", classify_with_tracking)
retry_builder.add_node("respond_refund", respond_refund)
retry_builder.add_node("respond_technical", respond_technical)
retry_builder.add_node("respond_general", respond_general_v2)
retry_builder.add_node("give_up", give_up_node)

retry_builder.set_entry_point("classify")
retry_builder.add_conditional_edges(
    "classify",
    route_after_classification,
    {
        "retry": "classify",
        "give_up": "give_up",
        "respond_refund": "respond_refund",
        "respond_technical": "respond_technical",
        "respond_general": "respond_general",
    },
)
retry_builder.add_edge("respond_refund", END)
retry_builder.add_edge("respond_technical", END)
retry_builder.add_edge("respond_general", END)
retry_builder.add_edge("give_up", END)

retry_graph = retry_builder.compile()

retry_initial_state: RetryableState = {
    "request_text": "I was charged twice for my CloudNest subscription this month.",
    "category": None,
    "response": None,
    "attempts": 0,
}
result = retry_graph.invoke(retry_initial_state)
print(result["category"], result["attempts"])
print(result["response"])
```

**Example output (illustrative for `category`, since it's LLM-classified — actual LLM output will vary run to run, but given this request's clear content, "REFUND" on the first attempt, i.e. `attempts: 1`, with no retries needed, is the expected and realistic outcome; the routing to `respond_refund` and its exact templated response, GIVEN that classification, is deterministic graph behavior):**
```
REFUND 1
Refund request received: 'I was charged twice for my CloudNest subscription this month.'. Routed to billing team, response within 24 hours.
```

**Say:** *"The single most important structural fact in this graph: `retry` maps back to `"classify"` itself — the SAME node the edge originated from. That's what makes this a real RETRY LOOP: if classification comes back invalid, the graph genuinely re-enters `classify_with_tracking`, which increments `attempts` each time, until either a valid category appears or `attempts` hits 3 and `check_classification`-style logic routes to `give_up` instead. This is explicit, bounded, inspectable retry logic — directly comparable to Session 12's `max_iterations`, but here it's a designed PART of the graph's shape, not a global safety cap applied uniformly to the whole run."*

### Comprehension Check (6 min)

1. *"What specifically makes `route_after_classification`'s `'retry'` branch a genuine RETRY loop rather than just another branch?"* (Its mapped destination is `"classify"` — the SAME node the edge started from — so execution genuinely re-enters that node again, rather than moving forward to a new step.)
2. *"Why does `classify_with_tracking` need to increment and return `attempts` on every call, not just the first one?"* (Without an incrementing counter in state, the retry condition `state["attempts"] < 3` could never become false, risking an infinite retry loop with no bound.)

---

## SEGMENT 5: LangGraph vs. `AgentExecutor` — When to Use Each (15 min)

### A Direct, Honest Comparison (10 min)

**Say:** *"Both tools solve 'let an LLM make some decisions across multiple steps' — but they make genuinely different tradeoffs, worth naming explicitly rather than treating one as simply 'the upgraded version' of the other."*

**Write on board:**

| | `AgentExecutor` (Sessions 12-13) | LangGraph (today) |
|---|---|---|
| Control flow | Implicit — the LLM's own ReAct reasoning decides what happens next, every step | Explicit — you define nodes and edges; the LLM fills in SOME decisions within that fixed shape |
| Branching logic | Emerges from the model's reasoning; hard to guarantee a specific path is always taken | Defined in code via `add_conditional_edges`; a specific business rule can be guaranteed to route a specific way |
| Retry handling | Global settings (`max_iterations`, `handle_parsing_errors`) applied uniformly across the whole run | Can be scoped PER STEP, with different retry logic for different parts of the workflow |
| Best suited for | Open-ended tasks where the right sequence of tool calls genuinely isn't known in advance | Workflows with known structure/stages, where some steps must reliably happen in a guaranteed order or under specific conditions |
| Debuggability | Read a Thought/Action/Observation text trace after the fact | Inspect the graph's defined structure directly, independent of any specific run's trace |

**Say:** *"A genuinely useful rule of thumb: if you find yourself wanting to say 'but ALWAYS do X before Y' or 'if condition Z, guarantee this specific path' about your agent, and you're fighting the model's own reasoning to try to force that — that's the signal LangGraph's explicit structure is probably the better fit. If the task is genuinely open-ended, where the right NUMBER and ORDER of steps really can't be known ahead of time and should be left to the model's judgment, `AgentExecutor`'s flexibility is the better fit. Many real production systems, honestly, use BOTH — a LangGraph workflow with known stages, where one or more of those STAGES internally contains a full `AgentExecutor` agent handling a sub-task that genuinely needs open-ended tool use."*

### Comprehension Check (5 min)

1. *"If a business requirement says 'every refund request must go through a fraud-check step before any response is sent, no exceptions,' which approach more naturally guarantees that?"* (LangGraph — an explicit edge/node structure can guarantee a specific node always executes under a specific condition, rather than relying on the model's own reasoning to remember and follow that rule every time.)
2. *"Is it accurate to say LangGraph 'replaces' `AgentExecutor', making it obsolete?"* (No — they solve different problems with different tradeoffs; many real systems combine both, and the open-ended, judgment-heavy tool-selection `AgentExecutor` is good at remains genuinely useful within a larger LangGraph-structured workflow.)

---

## SEGMENT 6: Lab — A Branching, Retrying Support-Routing Graph (15 min)

### Instructions (read aloud, step by step)

1. Add a FOURTH category, `"URGENT"`, to `VALID_CATEGORIES` and `route_after_classification`, with its own `respond_urgent` node that returns a response indicating immediate escalation.
2. Update `classify_with_tracking`'s prompt to include `URGENT` as a fourth classification option, reserved for requests mentioning words like "immediately," "urgent," or "emergency."
3. Wire the new node and conditional-edge branch into a new graph, keeping the existing retry-to-`"classify"` logic intact.
4. Test the graph against two requests: one that should classify as `URGENT`, and one that should classify as one of the other three categories, and print each one's final `category` and `response`.

### Starter Code

```python
VALID_CATEGORIES_V2 = {"REFUND", "TECHNICAL", "GENERAL", "URGENT"}

def respond_urgent(state: RetryableState) -> dict:
    return {"response": f"URGENT request flagged: '{state['request_text']}'. Escalated immediately to on-call support."}

def classify_with_tracking_v2(state: RetryableState) -> dict:
    prompt = f"""Classify this customer request into exactly one category:
REFUND, TECHNICAL, GENERAL, or URGENT (use URGENT only for requests signaling
an emergency or needing immediate attention). Reply with only the category word.

Request: {state['request_text']}"""
    result = llm.invoke(prompt)
    category = result.content.strip().upper()
    return {"category": category, "attempts": state["attempts"] + 1}

def route_after_classification_v2(state: RetryableState) -> str:
    if state["category"] not in ___:
        if state["attempts"] < 3:
            return "retry"
        return "give_up"
    if state["category"] == "REFUND":
        return "respond_refund"
    elif state["category"] == "TECHNICAL":
        return "respond_technical"
    elif state["category"] == ___:
        return ___
    else:
        return "respond_general"

lab_builder = StateGraph(RetryableState)
# ... register all nodes, set entry point, wire conditional edges and END edges ...
```

### Reference Solution

```python
VALID_CATEGORIES_V2 = {"REFUND", "TECHNICAL", "GENERAL", "URGENT"}

def respond_urgent(state: RetryableState) -> dict:
    return {"response": f"URGENT request flagged: '{state['request_text']}'. Escalated immediately to on-call support."}

def classify_with_tracking_v2(state: RetryableState) -> dict:
    prompt = f"""Classify this customer request into exactly one category:
REFUND, TECHNICAL, GENERAL, or URGENT (use URGENT only for requests signaling
an emergency or needing immediate attention). Reply with only the category word.

Request: {state['request_text']}"""
    result = llm.invoke(prompt)
    category = result.content.strip().upper()
    return {"category": category, "attempts": state["attempts"] + 1}

def route_after_classification_v2(state: RetryableState) -> str:
    if state["category"] not in VALID_CATEGORIES_V2:
        if state["attempts"] < 3:
            return "retry"
        return "give_up"
    if state["category"] == "REFUND":
        return "respond_refund"
    elif state["category"] == "TECHNICAL":
        return "respond_technical"
    elif state["category"] == "URGENT":
        return "respond_urgent"
    else:
        return "respond_general"

lab_builder = StateGraph(RetryableState)
lab_builder.add_node("classify", classify_with_tracking_v2)
lab_builder.add_node("respond_refund", respond_refund)
lab_builder.add_node("respond_technical", respond_technical)
lab_builder.add_node("respond_general", respond_general_v2)
lab_builder.add_node("respond_urgent", respond_urgent)
lab_builder.add_node("give_up", give_up_node)

lab_builder.set_entry_point("classify")
lab_builder.add_conditional_edges(
    "classify",
    route_after_classification_v2,
    {
        "retry": "classify",
        "give_up": "give_up",
        "respond_refund": "respond_refund",
        "respond_technical": "respond_technical",
        "respond_general": "respond_general",
        "respond_urgent": "respond_urgent",
    },
)
lab_builder.add_edge("respond_refund", END)
lab_builder.add_edge("respond_technical", END)
lab_builder.add_edge("respond_general", END)
lab_builder.add_edge("respond_urgent", END)
lab_builder.add_edge("give_up", END)

lab_graph = lab_builder.compile()

urgent_state: RetryableState = {
    "request_text": "This is urgent -- our whole team is locked out of CloudNest right before a client deadline!",
    "category": None, "response": None, "attempts": 0,
}
general_state: RetryableState = {
    "request_text": "Just wondering if CloudNest has a referral program.",
    "category": None, "response": None, "attempts": 0,
}

for s in (urgent_state, general_state):
    result = lab_graph.invoke(s)
    print(result["category"], "->", result["response"])
```

**Example output (illustrative — actual LLM output will vary run to run in exact classification and phrasing, but given the first request's explicit "urgent," "locked out," and deadline language, "URGENT" is the expected and realistic classification; given the second request's casual, non-urgent inquiry tone, "GENERAL" is the expected and realistic classification):**
```
URGENT -> URGENT request flagged: 'This is urgent -- our whole team is locked out of CloudNest right before a client deadline!'. Escalated immediately to on-call support.
GENERAL -> General inquiry received: 'Just wondering if CloudNest has a referral program.'. A support agent will follow up shortly.
```

**Instructor circulates**, checking specifically that `respond_urgent` is both registered with `add_node` AND included in the conditional-edges mapping dict (a common slip is adding the node but forgetting to add its corresponding routing entry), and that the retry branch (`"retry": "classify"`) is still intact and correctly bounded by `attempts < 3` after the new category is added.

---

## SEGMENT 7: Course Wrap-Up & Final Q&A (5 min)

**What we covered today:**
- Defined a `StateGraph` with typed state, registered nodes, and wired them with `add_edge` for fixed transitions
- Built real branching logic with `add_conditional_edges`, where a Python routing function — not the model's own reasoning — decides which path execution takes
- Implemented explicit, bounded retry handling as a designed part of the graph's own structure, looping a node back to itself under a tracked condition
- Directly compared LangGraph and `AgentExecutor`, and articulated when each is the better-suited tool

**Looking back across Module 3 — walk through this list on the board, one line per session:**

- **Sessions 1-2:** Learned how LLMs actually generate text, and made our first raw API calls to one, by hand, with no framework at all
- **Session 3 (Master Class):** Built the vector and dot-product foundation that every embedding and every similarity search since has rested on
- **Sessions 4-5:** Learned to deliberately shape what a model produces — through prompting, then through Pydantic schemas and `instructor` for guaranteed structure
- **Sessions 6-7:** Picked up LangChain itself — prompt templates, chains, and our first real multi-step AI workflows
- **Sessions 8-9:** Learned to represent meaning as vectors with embeddings, then chunk, index, and retrieve real documents with ChromaDB and FAISS
- **Session 10 (Master Class):** Built the calculus intuition — rate of change, optimization — underlying how these models are trained in the first place
- **Session 11:** Combined retrieval and generation into a complete RAG pipeline, and watched grounding directly cut hallucination
- **Session 12:** Gave an LLM real tools and a ReAct reasoning loop, building our first genuine decision-making agent
- **Session 13:** Made retrieval itself just one tool among several, then learned to actually MEASURE quality with RAGAS and protect the system with guardrails
- **Session 14 (today):** Stepped beyond the flat agent loop entirely, into explicit, designed workflows with real branching and retry logic as first-class citizens

**Say:** *"Notice the throughline across all fourteen sessions: every single piece — raw API calls, vectors, prompting, structured output, chains, embeddings, retrieval, agents, evaluation, guardrails, and now orchestration — is a layer that makes the layer below it more RELIABLE, more CONTROLLABLE, or more CAPABLE, never a replacement for what came before. A production GenAI system you build after this course will very likely use ALL of these ideas together: an OpenRouter-backed LLM call, wrapped in structured output where the result needs to be reliable data, grounded in retrieved context where it needs to be factually accurate, given tools where it needs to take real action, evaluated so you actually know it's working, protected by guardrails so it fails safely, and orchestrated — by `AgentExecutor`, by LangGraph, or by both together — so its control flow is exactly as structured, or exactly as flexible, as the problem genuinely requires."*

**Final homework / self-practice:**
1. Add a genuinely new node to today's lab graph representing a "confirmation" step that runs AFTER any response node and always ends the graph — wire it in with `add_edge` from each response node (replacing their direct `END` edges) to this shared confirmation node, then to `END`.
2. Write a 5-6 sentence reflection: pick ONE concept from ANY earlier Module 3 session (your choice) and explain, concretely, how you would combine it with TODAY'S LangGraph orchestration in a single hypothetical real system — be specific about which node would use it and why.
3. Sketch (on paper or digitally) the full box-and-arrow diagram of today's lab graph, including the retry loop back to `classify` — this is the kind of diagram you'd actually use to explain a real workflow's design to a non-technical stakeholder.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Can a single LangGraph node itself contain a full `AgentExecutor` agent inside it?**
→ Yes — a node is just a Python function; nothing stops that function from internally building and invoking a complete `AgentExecutor` agent to handle its specific sub-task, then returning the result as that node's state update. This is exactly the "use both together" pattern SEGMENT 5 described as common in real systems.

**Q: In the retry loop, does LangGraph guarantee the retry will eventually succeed?**
→ No — LangGraph guarantees the LOOP MECHANICS (re-entering the node, tracking state across attempts) work correctly and are bounded by whatever condition you define; it cannot guarantee the underlying LLM call will actually produce a valid result on any given attempt. That's exactly why a bounded `give_up` fallback path, not an unbounded retry, is the responsible design — the same lesson as Session 12's `max_iterations`.

**Q: Does every node in a graph have to call an LLM?**
→ No — today's `give_up_node` and the response nodes are entirely plain Python logic with zero LLM calls. A graph can freely mix LLM-backed nodes (like classification) with pure-logic nodes (like formatting a final response), which is itself a meaningful advantage: you only pay for and risk an LLM call at the specific steps that genuinely need one.

**Q: Is there a limit to how complex a LangGraph workflow can get — more branches, more retry loops, nested graphs?**
→ No hard technical limit, but the same practical caution from Session 5's nested-schema discussion applies: a workflow that's needlessly complex becomes harder to reason about, test, and debug. Keep the graph's shape as simple as the real business process genuinely requires, adding branches and retries only where there's a real, specific need for that exact control.

---

## Instructor Notes

- **Prerequisite check:** Confirm `pip install langgraph langchain-openai` all succeed before class; `langgraph` is today's one new dependency beyond what's already been used throughout Module 3.
- **Common mistake:** Confusing a node's RETURN VALUE (a partial dict of just the fields it's updating) with the full state object — reinforce explicitly that LangGraph merges the returned dict into state automatically; a node should not try to return the entire state manually.
- **Common mistake:** In a conditional edge's mapping dict, forgetting to include an entry for every string the routing function can actually return — causing a runtime error when an unmapped value is produced. Walk through SEGMENT 4's "wait, let me fix this" moment explicitly if students hit this same class of bug.
- **Another common mistake:** Writing a retry condition without an incrementing, tracked counter in state, risking a genuinely unbounded loop. Point to `attempts` explicitly as the pattern to copy.
- **Engagement tip:** SEGMENT 4's live "wait, that's not quite right, let me fix it" moment — catching the single-conditional-edge limitation and correcting it to a combined routing function — is a valuable, honest teaching moment; consider narrating it explicitly as modeling real iterative design rather than treating it as an error to skip past quickly.
- **Time check:** If running behind before the break, shorten SEGMENT 2's standalone node-testing step (testing `classify_request` by itself before wiring the graph) and move directly to building the full graph.
- **If running long after the break:** Compress SEGMENT 5's comparison table discussion to presenting the table directly on the board rather than deriving each row through class discussion.
- **Materials to prepare:** `langgraph` and `langchain-openai` installed and verified; whiteboard space for the course-wide Module 3 review list in SEGMENT 7; a backup pre-captured transcript of the SEGMENT 6 lab's two test runs, in case of API/network issues; consider printing or projecting the SEGMENT 5 comparison table in advance.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Returning the full state dict from a node instead of just updated fields | Unexpected overwrites of unrelated state fields, or confusing merge behavior | Return only the fields the node is actually updating; let LangGraph merge them into the existing state |
| Missing a mapping entry for a possible routing-function return value | Runtime error: unrecognized/unmapped routing key | Ensure every string the routing function can return has a corresponding entry in the conditional-edges mapping dict |
| Retry condition with no incrementing counter in state | Potential unbounded retry loop | Track and increment an `attempts`-style field in state, and check it explicitly in the routing function |
| Forgetting to register a new node with `add_node` even though it's referenced in a conditional-edges mapping | Runtime error referencing an unregistered node | Always add a node with `add_node` BEFORE referencing its name anywhere in edges or conditional-edges mappings |
| Forgetting `add_edge(..., END)` for a terminal node | Graph never signals it has finished that branch | Explicitly wire every terminal node's edge to `END` |

---

## Appendix: Visualizing the Compiled Graph (Optional, If Time Allows)

```python
print(retry_graph.get_graph().draw_mermaid())
```

**Example output (actual — deterministic structural output reflecting exactly the nodes and edges registered in `retry_builder`, in LangGraph's Mermaid diagram syntax; the EXACT formatting/syntax details may vary slightly across LangGraph versions, but the underlying node/edge structure shown is a direct, accurate reflection of this exact graph's defined structure):**
```
graph TD
    __start__ --> classify
    classify -. retry .-> classify
    classify -. give_up .-> give_up
    classify -. respond_refund .-> respond_refund
    classify -. respond_technical .-> respond_technical
    classify -. respond_general .-> respond_general
    respond_refund --> __end__
    respond_technical --> __end__
    respond_general --> __end__
    give_up --> __end__
```

**Say (if running this appendix):** *"This is a genuinely useful debugging and documentation habit: a graph's STRUCTURE can be inspected and even rendered as a diagram directly from the compiled object, independent of any specific run — you can hand this Mermaid output to a non-technical stakeholder, or paste it into a Mermaid renderer, to visually confirm the workflow's shape matches what was actually intended, entirely separate from reading a runtime trace."*

---

## FAQ — Additional Questions

**Q: Does LangGraph require the state to be a `TypedDict` specifically, or could it be a different structure?**
→ `TypedDict` is the simplest, most common choice and what we used today for clarity, but LangGraph also supports Pydantic models as state — directly connecting back to Session 5's `BaseModel` work, for cases where you want state itself to carry validation rules.

**Q: Can a LangGraph workflow call another, separately-compiled LangGraph graph as one of its nodes?**
→ Yes — a compiled graph can be used as a node within a larger graph, enabling genuinely modular, nested workflow design for complex systems, similar in spirit to how a chain can be composed of smaller chains.

**Q: Is LangGraph only useful for agent-like systems with LLM calls, or could it orchestrate a workflow with no LLM involved at all?**
→ It can orchestrate ANY multi-step Python workflow with state, branching, and retries — LLM calls are a common and natural fit for the DECISION-MAKING parts of a node or routing function, but nothing about `StateGraph` itself requires an LLM to be involved at all.

---

## Materials Checklist

- [ ] `langgraph` and `langchain-openai` installed and verified
- [ ] Scratch notebook with SEGMENT 2's `SupportState` and `classify_request` pre-typed
- [ ] Backup pre-captured transcript of SEGMENT 6's two lab test runs
- [ ] Whiteboard space for the branching/retry graph diagram and the full Module 3 review list
- [ ] Printed or projected copy of the SEGMENT 5 LangGraph vs. `AgentExecutor` comparison table
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 2's standalone node-testing step, move directly to building the full graph |
| Running long after break | Compress SEGMENT 5 to presenting the comparison table directly rather than deriving it through discussion |
| Low energy after lunch/break | Run SEGMENT 6's two lab test cases as a group "predict the classification and route" guessing game before revealing |
| Advanced group finishes lab early | Have them implement final homework item 1 (shared confirmation node) live, and render it with the Appendix's `draw_mermaid()` |
| No shared screen / projector issue | Walk through the graph structure and routing logic on the whiteboard using this script's exact examples and the Appendix's Mermaid diagram text |
| OpenRouter outage / no internet | Use the backup pre-captured transcripts for SEGMENTS 2-4 and 6; focus live work on SEGMENT 5's comparison discussion and the Appendix's structural graph inspection, neither of which requires a live LLM call |

---

## End-of-Session Quiz (5 Questions)

1. What does a LangGraph node's function actually return, and how does LangGraph use that return value?
2. What is the structural difference between `add_edge` and `add_conditional_edges`?
3. What specific structural feature makes a conditional edge's branch a genuine RETRY loop rather than just another branch?
4. Give one concrete signal that LangGraph's explicit structure is likely the better fit for a given workflow than `AgentExecutor`'s flexibility.
5. Name one way a LangGraph node and an `AgentExecutor` agent could be combined in the same real system, rather than treating them as mutually exclusive choices.

**Answer key (instructor):**
1. A dict of just the state fields that node is updating; LangGraph automatically merges that dict into the full shared state.
2. `add_edge` is a fixed, unconditional transition between two named nodes; `add_conditional_edges` calls a routing function against the current state and uses its returned string, looked up in a mapping dict, to decide which of several possible nodes to go to next.
3. The conditional edge's mapped destination for the retry case is the SAME node the edge originated from, so execution genuinely re-enters that node again rather than moving forward.
4. Any reasonable answer naming a requirement for guaranteed, explicit branching or ordering (e.g., "a specific step must always run under a specific condition, with no exceptions") that would be hard to enforce reliably through an LLM's own freeform reasoning alone.
5. A LangGraph node's function can internally construct and invoke a full `AgentExecutor` agent to handle an open-ended sub-task, returning its result as that node's state update — combining LangGraph's explicit outer structure with `AgentExecutor`'s flexible inner reasoning.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Shared confirmation node added and correctly wired | All response nodes correctly rerouted through the new node to `END`, graph compiles and runs correctly | Node added and mostly working, minor wiring issue | Node added but not correctly wired for all response paths | Not attempted |
| Cross-session integration reflection | Specific, concrete node-level integration described for a clearly named earlier-session concept | Reasonable integration idea, somewhat generic | Vague or superficial connection made | Not attempted |
| Full graph diagram sketch (including retry loop) | Clear, accurate box-and-arrow diagram including the retry loop back to `classify` and all branches | Mostly accurate diagram, minor omission (e.g., retry loop unclear) | Diagram attempted but missing significant structure | Not attempted |

**Total:** /12 — Pass threshold: 8/12

---

*This session closes Module 3: GenAI & Agents — and this course. From raw API calls to orchestrated, evaluated, guarded agent workflows: every piece built across these fourteen sessions is now yours to combine into real systems.*
