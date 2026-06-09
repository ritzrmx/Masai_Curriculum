# Coding Problem: LLM APIs & JSON Handling

> **Session 3** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

You are calling an LLM API and parsing the JSON response from a mock weather API — combining HTTP-style data handling with LLM calls.

---

## Setup

```python
import openai, json, os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Simulated API response (as you'd get from requests.get().json())
weather_json = """
{
  "city": "Mumbai",
  "temp_c": 32,
  "humidity": 78,
  "conditions": "Partly cloudy"
}
"""
```

---

## Tasks

**Task 1 — Parse JSON**

```python
data = json.loads(___)                    # fill: weather_json
print("City:", data["___"])               # fill: city
print("Temp:", data["___"])              # fill: temp_c
```

---

**Task 2 — API Call with Auth**

```python
# Never hardcode keys — use environment variables
api_key = os.getenv("___")                # fill: OPENROUTER_API_KEY

response = client.chat.completions.create(
    model=___,
    messages=[
        {"role": "system", "content": "You summarise weather in one friendly sentence."},
        {"role": "user", "content": f"Weather data: {weather_json}"}
    ],
    max_tokens=60
)

reply = response.choices[0].message.___   # fill: content
print(reply)
```

---

**Task 3 — Extract Structured Fields from Response**

Ask the model to return JSON and parse it.

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": (
            f"Return ONLY JSON with keys summary and comfort_level "
            f"(comfortable/uncomfortable) for: {weather_json}"
        )}
    ],
    response_format={"type": "___"},     # fill: json_object
    temperature=0
)

parsed = json.loads(response.choices[0].message.content)
print("Summary:", parsed["___"])        # fill: summary
print("Comfort:", parsed["___"])        # fill: comfort_level
```

---

**Task 4 — Error Handling**

```python
def safe_api_call(messages):
    try:
        r = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=50)
        return r.choices[0].message.content
    except ___ as e:                      # fill: Exception
        return f"API error: {e}"

print(safe_api_call([{"role": "user", "content": "Hello!"}]))
```

---

## Key Takeaways

- Store API keys in environment variables, never in source code
- `json.loads()` converts JSON strings to Python dicts
- Always handle API errors gracefully in production code
