# Coding Problem: Fundamentals of AI Agents and Tool Usage

> **Session 3** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a simple FAQ agent that can answer questions about a product using a `search_faq` tool. The agent should decide when to call the tool and when to answer directly.

---

## Setup

```python
import openai, json, os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Simulated FAQ database (no real DB needed)
FAQ_DB = {
    "return policy":   "You can return products within 30 days of purchase.",
    "shipping time":   "Standard shipping takes 5–7 business days.",
    "warranty":        "All products come with a 1-year manufacturer warranty.",
    "payment methods": "We accept credit cards, UPI, and net banking.",
}

def search_faq(query: str) -> str:
    """Search the FAQ database for an answer."""
    query = query.lower()
    for key, answer in FAQ_DB.items():
        if key in query:
            return answer
    return "Sorry, I couldn't find an answer for that."
```

---

## Tasks

**Task 1 — Define the Tool Schema**

Fill in the JSON schema so the LLM knows when and how to call `search_faq`.

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_faq",
            "description": "___",   # fill: describe what this tool does
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "___",        # fill: data type (string)
                        "description": "The user's question to search in the FAQ"
                    }
                },
                "required": ["___"]           # fill: required parameter name
            }
        }
    }
]
```

---

**Task 2 — Agent Loop (single turn)**

Send the user message to the LLM. If it calls a tool, execute it and send the result back.

```python
def run_agent(user_message: str):
    messages = [
        {"role": "system", "content": "You are a helpful support agent. Use the search_faq tool to answer product questions."},
        {"role": "user",   "content": user_message}
    ]

    # Step 1: first LLM call
    response = client.chat.completions.create(
        model=MODEL,
        messages=___,         # fill: pass messages
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    # Step 2: check if LLM wants to call a tool
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        args      = json.loads(tool_call.function.___)   # fill: arguments attribute
        result    = search_faq(args["query"])

        print(f"Tool called: {tool_call.function.name}({args})")
        print(f"Tool result: {result}")

        # Step 3: send tool result back to LLM
        messages.append(msg)
        messages.append({
            "role":         "tool",
            "tool_call_id": tool_call.___,               # fill: id attribute
            "content":      result
        })

        final = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return final.choices[0].message.content

    return msg.content
```

---

**Task 3 — Test the Agent**

Run the agent on the following queries. Note which ones trigger the tool and which don't.

```python
queries = [
    "What is your return policy?",
    "How long does shipping take?",
    "What is the capital of France?"   # should NOT trigger the tool
]

for q in queries:
    print(f"\nQ: {q}")
    print(f"A: {run_agent(q)}")
    print("-" * 40)
```

---

## Key Takeaways

- Agents use tool schemas to decide **when** to call a function — the LLM doesn't run code itself
- `tool_choice="auto"` lets the model decide; you can also force a tool with `tool_choice={"type": "function", ...}`
- Always send tool results back to the LLM so it can formulate a final response
