# Lecture Script: Building an AI Agent with LangChain
> **Instructor Reference** — Module 3: GenAI & Agents | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students define custom tools and connect them to a LangChain `AgentExecutor` using the ReAct (Reason + Act) pattern, build a multi-step agent that selects and calls tools based on input, and construct a working mini-agent — an FAQ Helpdesk — while controlling its execution safely.

**Student profile at this point:** Students have the full prompting and structured-output toolkit (Sessions 2-5), LangChain fundamentals (Sessions 6-7), embeddings/retrieval (Sessions 8-9), calculus Master Class (Session 10), and just built a complete RAG pipeline last session (Session 11). Everything up to now has been a FIXED pipeline: the code always runs the same steps in the same order. Today introduces the first genuinely NEW idea of the agents arc: letting the LLM itself decide WHICH action to take next, and in what order, based on the input.

**Key outcome:** Every student can write a custom tool using LangChain's `@tool` decorator, assemble a list of tools into a ReAct-style `AgentExecutor`, trace through an agent's Thought/Action/Observation loop in raw verbose output, and build a working FAQ Helpdesk mini-agent that safely selects between multiple tools, with `max_iterations` and `handle_parsing_errors` controlling its execution safely.

**Dataset for this session:** None required from disk — a small inline FAQ dictionary and a couple of simple inline tool functions (a calculator and an FAQ lookup) serve as this session's working material. No new dataset file is created.

**API note for this script:** All `@tool` decorator syntax, `create_react_agent`, and `AgentExecutor` usage in this script reflects LangChain's current, documented public API for building ReAct-pattern agents. The STRUCTURAL/mechanical behavior of these APIs (what gets called, what an `AgentExecutor` returns, how `verbose=True` formats its trace) is stated as documented fact. The actual CONTENT of an agent's reasoning trace — its Thought text, which tool it picks for a given input, and its final answer wording — is inherently non-deterministic LLM output and is marked **"Example output (illustrative — actual LLM output will vary run to run)"** throughout, since this script is not executed against a live paid API key.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — From Fixed Pipelines to Decisions | 10 min | 0:10 |
| SEGMENT 2: Defining Custom Tools | 20 min | 0:30 |
| SEGMENT 3: The ReAct Pattern & `AgentExecutor` | 25 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Tracing a Multi-Step Agent Run | 20 min | 1:25 |
| SEGMENT 5: Controlling Execution Safely | 15 min | 1:40 |
| SEGMENT 6: Lab — An FAQ Helpdesk Mini-Agent | 15 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — From Fixed Pipelines to Decisions (10 min)

### The Hook (5 min)

**Say:** *"Last session, our RAG pipeline always did the exact same thing, in the exact same order: retrieve, then generate. Every single time, no matter the question. But think about a real support bot — one user asks a factual question that needs retrieval. Another asks 'what's 15% of my $340 invoice' — that's a MATH question, not a retrieval question. A fixed pipeline can't tell the difference; it just always does the same steps. What we actually want is something that looks at the input FIRST and decides what kind of action is even needed."*

**Say:** *"That decision-making capability — 'look at the situation, decide what to do, do it, look at the result, decide what to do next' — is exactly what an AGENT is. Today we build our first one."*

### Why This Session Matters (5 min)

**Say:** *"LangChain's agent framework gives the LLM a list of TOOLS — plain Python functions it's allowed to call — and a loop that lets it reason about which tool to use, call it, observe the result, and decide whether it's done or needs another step. The specific reasoning pattern we'll use is called ReAct, short for 'Reason + Act': at each step the model THINKS out loud about what to do, takes an ACTION (calls a tool), OBSERVES the result, and repeats until it has enough to give a final answer. This loop is what turns a static pipeline into something that behaves like it's actually solving a problem."*

**Learning contract for today — write on board:**

- Define custom tools using LangChain's `@tool` decorator
- Understand the ReAct Thought → Action → Observation loop
- Assemble tools into a working `AgentExecutor`
- Build a multi-step agent that correctly selects between tools
- Control agent execution safely (iteration limits, parsing-error handling)

---

## SEGMENT 2: Defining Custom Tools (20 min)

### What a Tool Actually Is (5 min)

**Say:** *"A LangChain tool is just a Python function — plus some metadata the LLM can read: a NAME, a DESCRIPTION of what it does, and its expected INPUT. The description is doing more work than it looks like: it's the ONLY information the model has to decide whether this tool is the right one for a given situation. A vague or misleading description leads directly to the model picking the wrong tool."*

### Building Your First Tool (8 min)

**Live-code:**

```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """Evaluates a basic arithmetic expression, e.g. '15 * 0.2' or '340 - 51'.
    Use this for any math the user asks about, such as percentages, totals, or differences."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

print(calculate.name)
print(calculate.description)
print(calculate.invoke("15 * 0.2"))
```

**Example output (actual — deterministic behavior of the `@tool` decorator and this exact function):**
```
calculate
Evaluates a basic arithmetic expression, e.g. '15 * 0.2' or '340 - 51'.
    Use this for any math the user asks about, such as percentages, totals, or differences.
calculate
Evaluates a basic arithmetic expression, e.g. '15 * 0.2' or '340 - 51'.
    Use this for any math the user asks about, such as percentages, totals, or differences.
3.0
```

**Say:** *"Three things the `@tool` decorator automatically extracts from a plain function. The NAME comes from the function's name, `calculate`. The DESCRIPTION comes directly from the function's docstring — which is why writing a clear, specific docstring isn't optional documentation here, it's the actual instruction the agent reads to decide when to use this tool. And `.invoke(...)` is how you call a tool directly, the same uniform interface LangChain uses everywhere, from Session 6's chains to today's tools."*

**Say, flagging a safety note explicitly:** *"Quick, important aside: `eval()` is normally something you should be very cautious with in real production code, since it can execute arbitrary code. I restricted its builtins to an empty dict above specifically to reduce (not eliminate) that risk for this teaching example. A production calculator tool would typically use a dedicated, safe math-expression parser library instead of raw `eval()` — worth flagging explicitly so students don't copy this pattern into a real system without that caveat."*

### A Second Tool — FAQ Lookup (7 min)

**Live-code:**

```python
FAQ_DATABASE = {
    "refund policy": "Refunds are available within 30 days of purchase with a valid receipt.",
    "shipping time": "Standard shipping takes 5-7 business days; express shipping takes 1-2 business days.",
    "warranty": "All products include a 1-year limited warranty covering manufacturing defects.",
}

@tool
def search_faq(query: str) -> str:
    """Searches the company FAQ database for a topic like 'refund policy',
    'shipping time', or 'warranty'. Use this for any question about company
    policies. Returns the matching FAQ answer, or a not-found message."""
    query_lower = query.lower()
    for topic, answer in FAQ_DATABASE.items():
        if topic in query_lower or any(word in query_lower for word in topic.split()):
            return answer
    return "No matching FAQ entry found for that topic."

print(search_faq.invoke("What's your refund policy?"))
```

**Example output (actual — deterministic for this exact function and FAQ_DATABASE; matching here is simple keyword overlap, not semantic search):**
```
Refunds are available within 30 days of purchase with a valid receipt.
```

**Say:** *"Notice this tool's 'search' is deliberately simple keyword matching, not the embeddings-based semantic search from Sessions 8-9 — intentional today, to keep focus on tool-calling mechanics rather than retrieval quality. SEGMENT 6's lab, and next session's agentic RAG, is exactly where we'll upgrade this to real semantic retrieval as a tool. For now, two simple, clearly-described tools are enough to demonstrate an agent genuinely CHOOSING between them."*

### Comprehension Check (5 min)

1. *"Where does a tool's description, which the agent reads to decide when to use it, actually come from?"* (The function's docstring, automatically extracted by the `@tool` decorator.)
2. *"Why would a vague tool description like 'does stuff with numbers' be a problem, even if the underlying function works correctly?"* (The agent only has the description to decide WHEN to call a tool; a vague description makes it likely to pick the wrong tool, or the right tool at the wrong time, since it can't inspect the function's actual code.)

---

## SEGMENT 3: The ReAct Pattern & `AgentExecutor` (25 min)

### The Thought → Action → Observation Loop (8 min)

**Say:** *"ReAct prompts the model to produce, in a structured text format, a THOUGHT (reasoning about what to do next), an ACTION (which tool to call and with what input), and then the framework inserts an OBSERVATION (the tool's actual return value) before asking the model to continue. This repeats until the model decides it has enough information, at which point it produces a FINAL ANSWER instead of another action. Let's see the exact pattern before we build it, so the mechanics are clear before the API."*

**Write on board (a representative, illustrative ReAct trace — not a guaranteed exact transcript):**
```
Thought: The user is asking about a refund policy, so I should search the FAQ.
Action: search_faq
Action Input: refund policy
Observation: Refunds are available within 30 days of purchase with a valid receipt.
Thought: I now have the answer and don't need another tool call.
Final Answer: Refunds are available within 30 days of purchase with a valid receipt.
```

### Assembling the LLM, Tools, and Prompt (9 min)

**Say:** *"LangChain's standard way to build a ReAct agent is `create_react_agent`, which takes an LLM, a list of tools, and a ReAct-style prompt template, and returns an agent 'runnable.' We then wrap that in an `AgentExecutor`, which is the actual LOOP that repeatedly runs the agent, executes whichever tool it picks, feeds back the observation, and repeats."*

**Live-code:**

```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    temperature=0,
)

tools = [calculate, search_faq]

react_prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
```

**Say:** *"`hub.pull("hwchase17/react")` fetches LangChain's well-known, community-standard ReAct prompt template from LangChain Hub — it already contains the exact Thought/Action/Action Input/Observation formatting instructions the model needs to follow, so we don't have to hand-write that boilerplate ourselves. `create_react_agent` combines our LLM, our tool list, and that prompt into the reasoning agent itself. `AgentExecutor` is the piece that actually RUNS it — repeatedly invoking the agent, executing whichever tool name and input it outputs, and feeding the result back in, until a final answer appears. `verbose=True` is what will print the full Thought/Action/Observation trace for us to see, which SEGMENT 4 relies on directly."*

### Your First Agent Run (4 min)

**Live-code:**

```python
response = agent_executor.invoke({"input": "What is your refund policy?"})
print(response["output"])
```

**Example output (illustrative — actual LLM output will vary run to run in exact Thought phrasing, but given the clear FAQ-topic input and `search_faq`'s matching description, selecting `search_faq` and returning its exact matched answer is the expected and realistic outcome):**
```
Refunds are available within 30 days of purchase with a valid receipt.
```

**Say:** *"`agent_executor.invoke({"input": ...})` is the call that kicks off the whole Thought/Action/Observation loop. `response["output"]` is the FINAL answer string once the loop completes — with `verbose=True` set, you'd also see every intermediate Thought, Action, and Observation printed along the way, which is exactly what SEGMENT 4 examines closely."*

### Comprehension Check (4 min)

1. *"What is the actual difference between `agent` (from `create_react_agent`) and `agent_executor` (from `AgentExecutor`)?"* (`agent` is the reasoning component that decides what to do next; `AgentExecutor` is the loop that actually runs it repeatedly, executes the chosen tools, and feeds results back in until a final answer.)
2. *"Why does `hub.pull("hwchase17/react")` save us meaningful work?"* (It provides the exact, already-tested Thought/Action/Action Input/Observation prompt formatting the ReAct pattern needs, rather than requiring us to hand-write and debug that prompt structure ourselves.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict what would happen if a user's question needed BOTH tools — for example, "what's 20% of my refund if my order was $150, and what's your refund policy?" Would the agent call one tool, or both, and in what order? Come back ready to see it happen.

---

## SEGMENT 4: Tracing a Multi-Step Agent Run (20 min)

### A Question That Needs Two Tools (10 min)

**Say:** *"Let's test exactly the scenario from the break prompt — a question genuinely requiring BOTH tools, in sequence."*

**Live-code:**

```python
response = agent_executor.invoke({
    "input": "My order was $150. What's 20% of that as a refund, and what is your refund policy?"
})
print(response["output"])
```

**Example output (illustrative — actual LLM output will vary run to run in exact Thought wording and the precise order of tool calls, but given the input genuinely requires both a calculation and a policy lookup, and `verbose=True` is set, a multi-step trace calling BOTH `calculate` and `search_faq` — in some order — before a combined final answer is the expected and realistic outcome; this is a representative illustrative trace, not a guaranteed exact transcript):**
```
> Entering new AgentExecutor chain...
Thought: The user wants two things: a calculation (20% of $150) and the refund policy. I'll start with the calculation.
Action: calculate
Action Input: 150 * 0.20
Observation: 30.0
Thought: Now I need the refund policy.
Action: search_faq
Action Input: refund policy
Observation: Refunds are available within 30 days of purchase with a valid receipt.
Thought: I now have both pieces of information needed for a complete answer.
Final Answer: 20% of your $150 order is $30.00. Our refund policy allows refunds within 30 days of purchase with a valid receipt.

> Finished chain.
20% of your $150 order is $30.00. Our refund policy allows refunds within 30 days of purchase with a valid receipt.
```

**Say:** *"This is the genuinely new capability today's session introduces: the agent decided, on its OWN, that this question needed two separate tool calls, chose a sensible order, and combined both observations into one coherent final answer. Nothing in our code explicitly told it 'call calculate, then call search_faq' — that sequencing came entirely from the model's own reasoning inside the ReAct loop, guided only by the tool descriptions and the user's actual input."*

### Reading the Trace Structure Carefully (6 min)

**Say:** *"Walking through the trace's STRUCTURE, which is NOT model-generated and IS something you can rely on: `> Entering new AgentExecutor chain...` and `> Finished chain.` are fixed framework markers `verbose=True` always prints, bracketing the whole run. Inside, each Thought/Action/Action Input/Observation block is one ITERATION of the loop — the agent reasons, acts, and the framework inserts the real tool's return value as the Observation, which the model then reads before its NEXT thought. The loop only stops once the model outputs 'Final Answer:' instead of another 'Action:' — that's the actual stopping SIGNAL the `AgentExecutor` looks for."*

### What Happens If a Tool Fails or Returns Nothing Useful (4 min)

**Live-code:**

```python
response = agent_executor.invoke({"input": "What is your pet adoption policy?"})
print(response["output"])
```

**Example output (illustrative — actual LLM output will vary run to run, but given that `search_faq` will genuinely return "No matching FAQ entry found for that topic." for this query — an input not present in `FAQ_DATABASE` — a final answer that honestly reports no matching policy was found, rather than inventing one, is the expected and realistic outcome of a correctly functioning search_faq tool and a reasonably instructed model):**
```
I don't have information about a pet adoption policy in our FAQ database.
```

**Say:** *"This connects directly back to Session 11's grounding discussion: the TOOL'S OWN return value — 'No matching FAQ entry found' — is itself grounding information the agent reads and (ideally) reports honestly, rather than fabricating a policy. The quality of your tool's OWN failure messages directly shapes how gracefully the agent handles a miss — a vague tool failure message risks a vague or even fabricated final answer."*

---

## SEGMENT 5: Controlling Execution Safely (15 min)

### Why Unbounded Loops Are a Real Risk (5 min)

**Say:** *"Here's a real production risk worth naming explicitly: nothing inherently stops an agent from looping Thought → Action → Observation forever, if the model keeps deciding it needs 'just one more' tool call, or gets stuck re-trying the same failing action. Left unchecked, that's wasted API calls, wasted money, and a hung application. `AgentExecutor` gives us real controls for exactly this."*

### `max_iterations` and `max_execution_time` (6 min)

**Live-code:**

```python
safe_agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=4,
    max_execution_time=30,  # seconds
    handle_parsing_errors=True,
)
```

**Say:** *"`max_iterations=4` caps the Thought/Action/Observation loop at 4 rounds — after that, the executor stops and returns whatever it has, rather than looping indefinitely. `max_execution_time=30` is a second, independent safety net based on wall-clock time, useful if a single tool call itself hangs or runs unexpectedly slowly. And `handle_parsing_errors=True` addresses a DIFFERENT failure mode entirely: sometimes the model's raw text output doesn't perfectly match the expected Thought/Action/Action-Input format the ReAct prompt expects, and without this flag, that malformed output would raise an uncaught exception and crash the whole run. With it set, the executor instead feeds the parsing error back to the model as an observation, essentially saying 'that wasn't formatted correctly, try again' — giving the model a chance to self-correct within the remaining iteration budget."*

**Say:** *"These three settings are today's direct parallel to Session 5's `try/except` around `instructor`'s validation retries, and Session 2's exponential backoff for rate limits — different failure modes (infinite reasoning loops, slow tool calls, malformed agent output), same engineering instinct: external, probabilistic processes need explicit bounds, every time, in production code."*

### Comprehension Check (4 min)

1. *"What specific failure mode does `max_iterations` protect against that `handle_parsing_errors` does not?"* (`max_iterations` caps how many Thought/Action/Observation rounds can run, protecting against a genuinely unbounded reasoning loop; `handle_parsing_errors` instead recovers from the model producing text that doesn't match the expected ReAct format, which is a formatting problem, not a looping problem.)
2. *"If `max_iterations` is reached before the agent produces a Final Answer, does the program crash?"* (No — `AgentExecutor` stops the loop and returns its best available result rather than raising an exception, which is exactly why this is a SAFE control rather than just an error condition.)

---

## SEGMENT 6: Lab — An FAQ Helpdesk Mini-Agent (15 min)

### Instructions (read aloud, step by step)

1. Add a third tool, `check_order_status`, that takes an `order_id: str` and looks up a status from an inline dictionary of 3-4 fake order IDs and statuses (e.g., `{"A1001": "Shipped, arriving in 2 days", "A1002": "Processing"}`), returning a clear "order not found" message for unknown IDs.
2. Assemble all three tools (`calculate`, `search_faq`, `check_order_status`) into a new `AgentExecutor`, with `max_iterations=5` and `handle_parsing_errors=True` set.
3. Test it against three inputs: one that needs only `search_faq`, one that needs only `check_order_status`, and one that needs `calculate` combined with either of the other two.
4. For one test, print the full `verbose=True` trace and identify, in a comment, which tool(s) were called and in what order.

### Starter Code

```python
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

ORDER_STATUS_DB = {
    "A1001": "Shipped, arriving in 2 days",
    "A1002": "Processing",
    "A1003": "Delivered on March 3rd",
}

@tool
def check_order_status(order_id: str) -> str:
    """___"""
    return ORDER_STATUS_DB.get(order_id, ___)

helpdesk_tools = [calculate, search_faq, ___]

helpdesk_agent = create_react_agent(llm=llm, tools=___, prompt=react_prompt)

helpdesk_executor = AgentExecutor(
    agent=___,
    tools=___,
    verbose=True,
    max_iterations=___,
    handle_parsing_errors=___,
)

print(helpdesk_executor.invoke({"input": "What's the status of order A1002?"})["output"])
print(helpdesk_executor.invoke({"input": "What's your shipping time policy?"})["output"])
print(helpdesk_executor.invoke({"input": "My order A1001 cost $80 -- what's 15% of that as a potential restocking fee, and is it shipped yet?"})["output"])
```

### Reference Solution

```python
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

ORDER_STATUS_DB = {
    "A1001": "Shipped, arriving in 2 days",
    "A1002": "Processing",
    "A1003": "Delivered on March 3rd",
}

@tool
def check_order_status(order_id: str) -> str:
    """Looks up the shipping status of an order given its order ID, e.g. 'A1001'.
    Use this for any question about where an order is or whether it has shipped."""
    return ORDER_STATUS_DB.get(order_id, f"No order found with ID {order_id}.")

helpdesk_tools = [calculate, search_faq, check_order_status]

helpdesk_agent = create_react_agent(llm=llm, tools=helpdesk_tools, prompt=react_prompt)

helpdesk_executor = AgentExecutor(
    agent=helpdesk_agent,
    tools=helpdesk_tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)

print(helpdesk_executor.invoke({"input": "What's the status of order A1002?"})["output"])
print(helpdesk_executor.invoke({"input": "What's your shipping time policy?"})["output"])
print(helpdesk_executor.invoke({
    "input": "My order A1001 cost $80 -- what's 15% of that as a potential restocking fee, and is it shipped yet?"
})["output"])
# Trace for the third call is expected to show calculate (150 * 0.15, i.e. "80 * 0.15")
# followed by check_order_status("A1001"), in that order, based on the order the
# question poses the two sub-requests -- though exact ordering may vary run to run.
```

**Example output (illustrative — actual LLM output will vary run to run; outcomes are expected to be a correct status lookup, a correct FAQ answer, and a correct combined calculation-plus-status answer respectively, since each test input clearly matches one or more tool descriptions):**
```
Your order A1002 is currently: Processing.
Standard shipping takes 5-7 business days; express shipping takes 1-2 business days.
15% of $80 is $12.00, and order A1001 has shipped -- arriving in 2 days.
```

**Instructor circulates**, checking specifically that the new tool's docstring is clear and specific (not just `"""Checks order status."""`, which under-specifies the expected input format), that all three tools are present in BOTH the `create_react_agent` call AND the `AgentExecutor` call (a common slip is updating one list but not the other), and that `max_iterations` and `handle_parsing_errors` are both actually set rather than left as the `AgentExecutor` defaults.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Defined custom LangChain tools with the `@tool` decorator, and saw how a tool's docstring becomes its description for the agent
- Learned the ReAct Thought → Action → Observation loop and assembled an agent with `create_react_agent` and `AgentExecutor`
- Traced a genuinely multi-step agent run where the model decided, on its own, to call two different tools in sequence
- Controlled agent execution safely using `max_iterations`, `max_execution_time`, and `handle_parsing_errors`
- Built a working FAQ Helpdesk mini-agent combining calculation, FAQ lookup, and order-status tools

**Bridge to what comes next:** *"Today's agent chose between a calculator and a keyword-matching FAQ lookup. Next session, we swap that simple keyword lookup for a REAL ChromaDB retriever, wrapped as its own tool — giving the agent genuine semantic-search-powered retrieval as one option among several, which is called agentic RAG. We'll also learn how to actually MEASURE whether a RAG pipeline is doing a good job, using RAGAS metrics, and talk seriously about guardrails and responsible AI."*

**Homework / self-practice:**
1. Add a fourth tool of your own design (e.g., a `convert_currency` tool with a small hardcoded exchange-rate dictionary) to the helpdesk agent, and test a question that requires it.
2. Deliberately lower `max_iterations` to `1` on a question that genuinely needs two tool calls, run it, and write 2-3 sentences on what you observe happening instead of a complete answer.
3. Rewrite `check_order_status`'s docstring to be deliberately VAGUE (e.g., `"""Does order stuff."""`), re-run a clear order-status question, and note whether the agent still reliably picks the right tool — then restore the clear docstring.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Is `AgentExecutor` the only way to build an agent in LangChain, or is it considered "old" now?**
→ `AgentExecutor` with `create_react_agent` is the classic, well-documented, and still fully supported way to build a ReAct-pattern tool-calling agent, and it's the right starting point for understanding the core Thought/Action/Observation mechanics clearly. LangGraph, which we cover in Session 14, offers a more flexible, graph-based way to build agent-like systems, including multi-agent workflows with explicit control over branching and retries — we'll directly compare the two approaches then.

**Q: Why did the agent in SEGMENT 4 choose to do the calculation BEFORE the FAQ lookup — is that order fixed?**
→ Not fixed — the ORDER of tool calls is itself a reasoning decision the model makes based on how it parses the user's question, not something hardcoded in our code. A different phrasing of the same underlying question, or even just model-to-model variation, can produce a different but equally valid call order.

**Q: What happens if two of our tools have genuinely overlapping, ambiguous descriptions?**
→ The agent can become unreliable at picking the "right" one, occasionally calling the wrong tool or needlessly calling both. This is a real, practical argument for keeping tool descriptions clearly distinct and non-overlapping — good tool design is itself a form of prompt engineering, echoing Session 5's point about well-designed schemas reducing `instructor` retries.

**Q: Can a tool call another tool, or call the LLM itself, internally?**
→ Yes, nothing prevents a tool function from containing arbitrary Python logic, including calling an LLM internally or even invoking another chain — but keep in mind the AGENT itself doesn't see or reason about what happens INSIDE a tool call; it only sees whatever string the tool ultimately returns as the Observation.

**Q: Does `handle_parsing_errors=True` fix every possible malformed-output situation?**
→ No — it specifically recovers from the model's raw text output not matching the ReAct prompt's expected Thought/Action/Action-Input structure, by feeding the parsing error back as a correction opportunity. It does not fix a tool THROWING an exception internally (your tool's own code should still handle its own errors gracefully, as our `calculate` tool's `try/except` does) or guarantee the model's retry attempt will actually succeed.

---

## Instructor Notes

- **Prerequisite check:** Confirm `pip install langchain langchain-openai langchainhub` all succeed before class, and that `hub.pull("hwchase17/react")` successfully fetches the prompt on the demo machine (requires outbound network access to LangChain Hub specifically, separate from the OpenRouter API itself).
- **Common mistake:** Writing a vague or missing tool docstring, then being confused when the agent picks the wrong tool or never calls a clearly-relevant one. Point directly to the docstring as the root cause whenever this surfaces.
- **Common mistake:** Updating the `tools` list passed to `create_react_agent` but forgetting to ALSO update the `tools` list passed to `AgentExecutor` (they must match) — a frequent slip in SEGMENT 6's lab specifically.
- **Another common mistake:** Leaving `max_iterations` unset entirely in a "real" build, risking runaway loops/cost on an unexpected input. Reinforce SEGMENT 5's framing explicitly as a production habit, not an optional afterthought.
- **Engagement tip:** SEGMENT 4's two-tool trace is the strongest "aha" moment of the session — pause immediately after revealing it and ask the class to point out, in the trace itself, the exact line where the model decided it was done with one tool and moved to the next.
- **Time check:** If running behind before the break, shorten SEGMENT 2's `search_faq` build to presenting the finished function rather than building it incrementally.
- **If running long after the break:** Compress SEGMENT 4's "tool failure" demo to a quick verbal description rather than a live run, and move directly to SEGMENT 5.
- **Materials to prepare:** `langchain`, `langchain-openai`, and `langchainhub` installed and verified; confirm `hub.pull` works on the classroom network ahead of time; a backup pre-captured verbose trace transcript of SEGMENT 4's two-tool run, in case of API/network issues.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Vague or missing tool docstring | Agent picks the wrong tool, or never calls a clearly relevant one | Write a specific docstring naming exactly when to use the tool and what input it expects |
| Mismatched `tools` list between `create_react_agent` and `AgentExecutor` | Agent references a tool name the executor doesn't recognize, raising an error | Keep one single `tools` list variable and pass the SAME list to both calls |
| No `max_iterations` set | Agent can loop far longer (and cost far more) than intended on an ambiguous input | Always set a reasonable `max_iterations` (and often `max_execution_time`) in any real build |
| `handle_parsing_errors` left as default/unset | A single malformed model output crashes the entire run with an uncaught exception | Set `handle_parsing_errors=True` so the executor can feed the parsing issue back for self-correction |
| Using raw unsandboxed `eval()` in a tool without restricting builtins | Security risk — a tool can be tricked into executing unintended code | Restrict `eval()`'s builtins as shown, or better, use a dedicated safe math-expression parser library in production |

---

## Appendix: Inspecting Intermediate Steps Programmatically (Optional, If Time Allows)

```python
response = agent_executor.invoke(
    {"input": "What's your warranty policy, and what's 10% of $200?"},
    return_intermediate_steps=True,
)

for action, observation in response["intermediate_steps"]:
    print(f"Tool called: {action.tool}, Input: {action.tool_input}")
    print(f"Observation: {observation}")
```

**Example output (illustrative — actual LLM output will vary run to run in exact Thought phrasing and tool-call order, but the STRUCTURE — a list of (action, observation) pairs, one per tool call actually made, accessible via `return_intermediate_steps=True` — reflects documented `AgentExecutor` behavior):**
```
Tool called: search_faq, Input: warranty policy
Observation: All products include a 1-year limited warranty covering manufacturing defects.
Tool called: calculate, Input: 200 * 0.10
Observation: 20.0
```

**Say (if running this appendix):** *"`return_intermediate_steps=True` gives you PROGRAMMATIC access to every (action, observation) pair from the run, not just the pretty-printed `verbose=True` text — genuinely useful for logging, debugging, or building your own custom trace UI in a real application, rather than relying on parsing printed console text."*

---

## FAQ — Additional Questions

**Q: Do tools always have to return a string?**
→ In the standard LangChain tool-calling convention, yes — a tool's return value becomes the Observation text the agent reads, so it needs to be a string (or something that stringifies cleanly). If your underlying logic naturally returns a number or object, convert it to a clear string representation before returning, as our `calculate` tool does with `str(result)`.

**Q: Can an agent decide to call the SAME tool more than once in one run?**
→ Yes, absolutely — for example, asking two separate calculations in one question could lead to two separate `calculate` calls in the same run, each its own Thought/Action/Observation round, well within a reasonable `max_iterations` budget.

**Q: What's the actual difference between a "chain" from Sessions 6-7 and an "agent" from today?**
→ A chain executes a FIXED sequence of steps you define in code — the same steps, same order, every time. An agent uses the LLM itself to decide, dynamically, WHICH steps (tool calls) to take and in what order, based on the specific input — the decision-making is genuinely data-dependent, not hardcoded.

---

## Materials Checklist

- [ ] `langchain`, `langchain-openai`, `langchainhub` installed and verified
- [ ] `hub.pull("hwchase17/react")` confirmed working on the classroom network ahead of time
- [ ] Scratch notebook with SEGMENT 2's tool definitions pre-typed
- [ ] Backup pre-captured verbose trace transcript of a two-tool agent run
- [ ] Whiteboard space for the ReAct Thought/Action/Observation diagram
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 2's `search_faq` build to presenting the finished function directly |
| Running long after break | Compress SEGMENT 4's tool-failure demo to a brief verbal description, skip the live run |
| Low energy after lunch/break | Run SEGMENT 4's two-tool trace as a group "predict the next Action" guessing game, line by line |
| Advanced group finishes lab early | Have them add the Appendix's `return_intermediate_steps=True` inspection to their own helpdesk agent |
| No shared screen / projector issue | Walk through the ReAct trace structure on the whiteboard using this script's exact illustrative examples |
| OpenRouter outage / no internet | Use the backup pre-captured trace transcript for SEGMENTS 3-6; focus live work on SEGMENT 2's tool definitions, which require no LLM calls |

---

## End-of-Session Quiz (5 Questions)

1. In the ReAct pattern, what are the three repeating parts of each loop iteration, and what signals the loop to stop?
2. Where does a LangChain tool's description, read by the agent to decide when to use it, actually come from?
3. What is the structural difference between `create_react_agent`'s return value and `AgentExecutor`?
4. Name two distinct safety controls `AgentExecutor` offers, and the distinct failure mode each one protects against.
5. Why might two tools with overlapping, ambiguous descriptions cause unreliable agent behavior?

**Answer key (instructor):**
1. Thought, Action, Observation, repeating until the model outputs a Final Answer instead of another Action.
2. The tool function's docstring, automatically extracted by the `@tool` decorator.
3. `create_react_agent` returns the reasoning component that decides what to do next; `AgentExecutor` is the loop that actually runs it, executes chosen tools, and feeds results back in until a final answer.
4. Any two of: `max_iterations` (caps the number of reasoning rounds, protecting against unbounded loops), `max_execution_time` (caps wall-clock time, protecting against a hanging tool call), `handle_parsing_errors` (recovers from malformed model output not matching the expected ReAct format, rather than crashing).
5. The agent only has each tool's description to decide which one fits a given situation; overlapping or ambiguous descriptions make it genuinely harder to tell them apart, increasing the chance of picking the wrong tool or needlessly calling both.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Fourth custom tool added + tested | Clear docstring, correctly integrated into both tool lists, tested successfully on a relevant question | Tool added and mostly working, minor description or integration issue | Tool added but not correctly integrated or tested | Not attempted |
| `max_iterations=1` observation write-up | Clear, specific description of the incomplete/truncated behavior observed | Reasonable description, somewhat generic | Vague or superficial observation | Not attempted |
| Vague-docstring experiment + restoration | Clearly tested both vague and clear docstring versions, reported the difference, restored the clear version | Tested one version clearly, other less clearly documented | Attempted without a clear before/after comparison | Not attempted |

**Total:** /12 — Pass threshold: 8/12
