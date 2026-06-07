# Coding Problem: Orchestration and Agent Workflow Design

> **Session 8** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a simple two-node research agent using LangGraph. The agent:
1. **Researches** a topic (calls an LLM to generate a summary)
2. **Reviews** the summary (calls the LLM again to critique it)

This simulates the pattern used in multi-step agentic workflows.

---

## Setup

```bash
pip install langgraph openai
```

```python
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm(prompt: str) -> str:
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return res.choices[0].message.content.strip()
```

---

## Tasks

**Task 1 — Define the State**

The state is the shared data that flows between nodes. Fill in the TypedDict.

```python
class AgentState(TypedDict):
    topic:   str       # input topic
    summary: ___       # fill: data type — research output
    review:  ___       # fill: data type — critique output
```

---

**Task 2 — Define the Nodes**

Each node is a function that receives the state and returns updated state fields.

```python
def research_node(state: AgentState) -> dict:
    topic   = state["___"]          # fill: get the topic
    prompt  = f"Write a concise 3-sentence summary about: {topic}"
    summary = llm(___)              # fill: pass prompt
    print(f"[Research] Done for: {topic}")
    return {"summary": ___}         # fill: return summary

def review_node(state: AgentState) -> dict:
    summary = state["___"]          # fill: get the summary
    prompt  = f"Review this summary. Point out 1 strength and 1 weakness:\n\n{summary}"
    review  = llm(___)              # fill: pass prompt
    print(f"[Review] Done.")
    return {"review": ___}          # fill: return review
```

---

**Task 3 — Build the Graph**

Wire the nodes together with transitions. Research runs first, then Review, then END.

```python
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("research", ___)    # fill: research_node
workflow.add_node("review",   ___)    # fill: review_node

# Set entry point
workflow.set_entry_point("___")       # fill: first node name

# Add edges
workflow.add_edge("research", "___")  # fill: next node
workflow.add_edge("review",   ___)    # fill: END

app = workflow.compile()
```

---

**Task 4 — Run the Workflow**

Invoke the compiled graph with an initial state and print the results.

```python
result = app.invoke({
    "topic":   "Large Language Models in Healthcare",
    "summary": "",
    "review":  ""
})

print("\n=== RESEARCH SUMMARY ===")
print(result["___"])        # fill: summary key

print("\n=== REVIEW ===")
print(result["___"])        # fill: review key
```

---

**Task 5 — Add Retry Handling**

Wrap the `research_node` LLM call in a simple retry loop (max 3 attempts) in case of an API error.

```python
import time

def research_node_with_retry(state: AgentState) -> dict:
    topic = state["topic"]
    prompt = f"Write a concise 3-sentence summary about: {topic}"

    for attempt in range(___):                          # fill: max attempts
        try:
            summary = llm(prompt)
            return {"summary": summary}
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(___)                             # fill: wait in seconds (e.g. 2)

    return {"summary": "Research failed after retries."}
```

---

## Key Takeaways

- LangGraph uses a **state machine model** — nodes transform state, edges control flow
- The shared `State` dict is the contract between all nodes — design it first
- Retry handling at the node level keeps the workflow resilient without cluttering the graph
