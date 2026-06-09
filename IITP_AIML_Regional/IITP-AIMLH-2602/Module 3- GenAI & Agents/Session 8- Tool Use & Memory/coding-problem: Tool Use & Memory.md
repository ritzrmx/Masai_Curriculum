# Coding Problem: Tool Use & Memory

> **Session 8** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

Build an agent with **function calling** and a simple **conversation memory** list so follow-up questions work across turns.

---

## Setup

```python
import openai, json, os
from datetime import datetime

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

tools = [{
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Returns the current date and time",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
}]
```

---

## Tasks

**Task 1 — Memory List**

```python
memory = [
    {"role": "system", "content": "You are a helpful assistant with access to get_current_time."}
]

def add_to_memory(role: str, content: str):
    memory.append({"role": ___, "content": ___})   # fill both blanks
```

---

**Task 2 — Tool Execution**

```python
def handle_tool_call(tool_call):
    if tool_call.function.name == "get_current_time":
        return get_current_time()
    return "Unknown tool"

def chat(user_message: str) -> str:
    add_to_memory("user", ___)                      # fill: user_message

    response = client.chat.completions.create(
        model=MODEL, messages=memory, tools=tools, tool_choice="auto"
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        call = msg.tool_calls[0]
        result = handle_tool_call(___)              # fill: call
        memory.append(msg)
        memory.append({
            "role": "tool",
            "tool_call_id": call.___,              # fill: id
            "content": result
        })
        final = client.chat.completions.create(model=MODEL, messages=memory)
        reply = final.choices[0].message.content
    else:
        reply = msg.content

    add_to_memory("assistant", reply)
    return reply
```

---

**Task 3 — Multi-Turn with Memory**

```python
print(chat("What time is it right now?"))
print(chat("What did I just ask you?"))   # memory should recall the prior question
print(f"Memory has {len(memory)} messages")
```

---

## Key Takeaways

- **Memory** = the full `messages` list passed to each API call
- Tool results must be appended before the model can answer
- Function calling lets the LLM invoke Python functions safely
