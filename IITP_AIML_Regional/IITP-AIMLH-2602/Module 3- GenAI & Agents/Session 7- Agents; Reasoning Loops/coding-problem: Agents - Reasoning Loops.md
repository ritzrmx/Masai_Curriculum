# Coding Problem: Agents — Reasoning Loops

> **Session 7** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

Implement a simple ReAct-style loop: the agent **thinks**, **acts** (calls a tool), and **observes** the result before answering.

---

## Setup

```python
import openai, json, os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

INVENTORY = {"SKU101": 45, "SKU202": 0, "SKU303": 12}

def check_stock(sku: str) -> str:
  qty = INVENTORY.get(sku.upper(), None)
  return f"{sku}: {qty} units" if qty is not None else f"{sku}: not found"
```

---

## Tasks

**Task 1 — Tool Schema**

```python
tools = [{
    "type": "function",
    "function": {
        "name": "check_stock",
        "description": "Check warehouse stock for a SKU",
        "parameters": {
            "type": "object",
            "properties": {"sku": {"type": "string"}},
            "required": ["___"]              # fill: sku
        }
    }
}]
```

---

**Task 2 — ReAct Loop**

```python
def run_agent(question: str, max_steps: int = 3):
    messages = [
        {"role": "system", "content": "You are a warehouse assistant. Use check_stock when needed."},
        {"role": "user", "content": question}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools, tool_choice="auto"
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content   # final answer

        # Act: execute tool
        call = msg.tool_calls[0]
        args = json.loads(call.function.___)       # fill: arguments
        result = check_stock(args["sku"])
        print(f"[Step {step+1}] Tool: {call.function.name}({args}) → {result}")

        # Observe: feed result back
        messages.append(msg)
        messages.append({
            "role": "tool",
            "tool_call_id": call.___,              # fill: id
            "content": result
        })

    return "Max steps reached."
```

---

**Task 3 — Run**

```python
print(run_agent("Can we ship 5 units of SKU202 today?"))
print(run_agent("How many SKU101 units do we have?"))
```

---

## Key Takeaways

- ReAct = Reason → Act → Observe in a loop
- The LLM decides when to call tools via `tool_choice="auto"`
- Always return tool results to the model for the final answer
