# Lecture Script: Calling LLMs with OpenRouter
> **Instructor Reference** — Module 3: GenAI & Agents | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students make raw HTTP calls to a real LLM through OpenRouter using nothing but the `requests` library — no LangChain, no OpenAI SDK, no framework — so they understand exactly what a "framework" is hiding before they ever use one. They structure system/user/assistant messages correctly, parse the JSON response, and handle errors and rate limits responsibly.

**Student profile at this point:** Just finished Session 1 — understands tokens, context windows, and temperature/top-p conceptually, but has never made a real LLM API call. Comfortable with `requests` and JSON from Module 1 ("File Handling, JSON & APIs"). Has an OpenRouter account and API key ready (set up as pre-work, or in the first few minutes of class).

**Key outcome:** Every student successfully sends a raw `requests.post()` call to OpenRouter's chat completions endpoint, correctly structures a `messages` list with `system`/`user`/`assistant` roles, extracts the assistant's reply text from the JSON response, and writes error-handling code that gracefully handles a 401 (bad key), a 429 (rate limit), and a malformed response — without the program crashing.

**Dataset for this session:** None. All work is live API calls and small inline example payloads — no CSV or file read from disk.

**API note for this script:** Example requests below use the real, correct OpenRouter request/response JSON shape and the real endpoint `https://openrouter.ai/api/v1/chat/completions`. All example RESPONSE bodies and printed assistant replies are marked **"Example output (illustrative — actual LLM output will vary run to run)"** since LLM text generation is non-deterministic and this script is not run against a live paid key — the REQUEST code itself, headers, and JSON structure are written to be correct and directly runnable once a student supplies their own `OPENROUTER_API_KEY`.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — What OpenRouter Is and Why Raw Calls First | 10 min | 0:10 |
| SEGMENT 2: Setup — API Key, Auth Headers & Your First Call | 25 min | 0:35 |
| SEGMENT 3: Structuring Messages — System, User, Assistant | 20 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Parsing Responses & Multi-Turn Conversations | 20 min | 1:25 |
| SEGMENT 5: Errors, Rate Limits & Responsible Retry Logic | 20 min | 1:45 |
| SEGMENT 6: Lab — Build a Robust `ask_llm()` Function | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — What OpenRouter Is and Why Raw Calls First (10 min)

### The Hook (5 min)

**Say:** *"Last session was entirely conceptual — tokens, context windows, temperature, all on the whiteboard. Today we go fully hands-on: by the end of this session, every one of you will have sent a real HTTP request to a real large language model and gotten a real response back, using nothing but the `requests` library you already know from Module 1."*

**Ask:** *"Who here has used an AI 'framework' before — LangChain, an SDK, anything with a name like `client.chat.completions.create()`? Keep your hand up if you could explain, right now, what HTTP request that convenience function is actually sending under the hood."* Most hands will drop for the second half. **Say:** *"That's exactly the gap today closes. We are deliberately starting with the RAW API — plain `requests.post()`, plain JSON — before you ever touch a framework, because frameworks are just convenience wrappers around exactly what we're about to build by hand. Once you've done it raw, every framework you meet later will feel like a shortcut, not a black box."*

### What Is OpenRouter, and Why Use It in This Course? (5 min)

**Say:** *"OpenRouter is a single API gateway that gives you access to models from many different providers — OpenAI, Anthropic, Google, Meta, and dozens more — through ONE consistent, OpenAI-compatible API format and ONE API key, instead of signing up separately with every provider. For this course, that means you learn one request shape and can experiment with many different underlying models just by changing a single `model` string in your JSON payload."*

**Write on board:**

```
Your code  --HTTP POST-->  OpenRouter  --routes to-->  the actual model provider
                                                          (OpenAI / Anthropic / etc.)
           <--HTTP response (JSON)--   <--model's raw output--
```

**Say:** *"Two housekeeping facts before we touch code. One: OpenRouter requires an account and an API key — if you haven't created one yet from openrouter.ai, do that right now, in the next two minutes, while I talk through the account/billing basics. Two: API keys are secrets — never hardcode them directly in a script you might commit to GitHub. We'll load ours from an environment variable, exactly like you practiced with API keys in Module 1's 'File Handling, JSON & APIs' session."*

**Learning contract for today — write on board:**

- Authenticate a request to OpenRouter using an API key in the `Authorization` header
- Structure a `messages` list with `system`, `user`, and `assistant` roles correctly
- Parse the JSON response to extract the assistant's reply text
- Handle errors (bad key, rate limit, malformed response) without crashing

---

## SEGMENT 2: Setup — API Key, Auth Headers & Your First Call (25 min)

### Loading the API Key Safely (6 min)

**Say:** *"First, never paste your API key directly into a code cell. Store it as an environment variable, and load it with `os.environ`. If you're on Colab, use Colab's 'Secrets' panel; locally, use a `.env` file loaded with `python-dotenv`, or export it in your shell before launching Python."*

**Live-code:**

```python
import os

# Option A: environment variable already set in your shell/Colab secrets
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found. Set it as an environment variable "
        "before running this notebook."
    )

print("Key loaded:", OPENROUTER_API_KEY[:8] + "..." )  # never print the full key
```

**Say:** *"Notice we print only the first 8 characters, followed by `...`, purely to confirm the key loaded — never print or log a full API key, even in a private notebook. This habit matters far beyond this classroom; leaked keys in shared notebooks or GitHub repos are one of the most common real-world security incidents in GenAI projects."*

### Anatomy of the Request (8 min)

**Say:** *"Every OpenRouter chat request has the same three ingredients: the URL, the headers, and the JSON body. Let's build each piece and understand exactly what it's for."*

**Write on board and explain each line:**

```python
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": "openai/gpt-4o-mini",   # any model slug available on OpenRouter
    "messages": [
        {"role": "user", "content": "Say hello in exactly five words."}
    ],
    "temperature": 0.7,
}
```

**Say, pointing at each part:** *"`Authorization: Bearer <key>` is the standard way almost every modern API authenticates you — the word 'Bearer' is literal, it's not a placeholder. `Content-Type: application/json` tells the server to expect a JSON body, not form data or plain text. And the `model` field is how OpenRouter knows WHICH underlying provider and model to route your request to — it's always `provider/model-name` format, like `openai/gpt-4o-mini` or `anthropic/claude-3.5-sonnet`. You can browse the full, current list of available model slugs on openrouter.ai/models — this list changes over time as providers add and retire models, so always check the live list rather than assuming a slug from an old tutorial still exists."*

### Making the First Real Call (8 min)

**Live-code the full call:**

```python
import requests

response = requests.post(url, headers=headers, json=payload)

print("Status code:", response.status_code)
data = response.json()
print(data)
```

**Example output (illustrative — actual LLM output will vary run to run; the JSON SHAPE shown is the real, correct OpenRouter/OpenAI-compatible response structure):**
```
Status code: 200
{
  "id": "gen-abc123xyz",
  "model": "openai/gpt-4o-mini",
  "object": "chat.completion",
  "created": 1732000000,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello there, nice to meet you!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 14,
    "completion_tokens": 8,
    "total_tokens": 22
  }
}
```

**Say, walking through the response shape:** *"`status_code` 200 means success — same HTTP status vocabulary you already know from Module 1. The real content you care about lives at `data['choices'][0]['message']['content']` — OpenRouter's response format follows the same `choices` list structure the underlying providers use, which is why it's called 'OpenAI-compatible.' And `usage` tells you exactly how many tokens this call cost, split into prompt (input) and completion (output) — remember from last session, you're billed on both separately."*

**Live-code extracting just the reply:**

```python
reply_text = data["choices"][0]["message"]["content"]
print("Assistant reply:", reply_text)
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Assistant reply: Hello there, nice to meet you!
```

**Ask:** *"The model was instructed 'exactly five words' but this illustrative example has six. Is that a bug in our code?"* Guide toward: no — this is the model itself not perfectly following an instruction, which is a real and common phenomenon, not a code error. This is exactly the kind of gap that Session 4 (prompt engineering) gives you techniques to reduce.

### Comprehension Check (3 min)

1. *"Which HTTP header carries your API key?"* (`Authorization`, formatted as `Bearer <key>`.)
2. *"Where in the JSON response does the model's actual generated text live?"* (`data["choices"][0]["message"]["content"]`.)

---

## SEGMENT 3: Structuring Messages — System, User, Assistant (20 min)

### The Three Roles (8 min)

**Say:** *"So far we've sent one lonely `user` message. Real conversations use THREE roles, and getting this right is the difference between a model that behaves the way you want and one that ignores your instructions."*

**Write on board:**

| Role | Purpose | Who writes it |
|---|---|---|
| `system` | Sets the model's behavior, persona, and rules for the ENTIRE conversation | You, once, usually first in the list |
| `user` | What the human is asking or saying | The end user (or you, simulating one) |
| `assistant` | The model's own previous replies | The model generated it; YOU resend it to preserve conversation history |

**Say:** *"The `system` message is the single most underused lever in prompt design, and we'll go much deeper on using it well in Session 4. For today, the key mechanical fact is: it goes FIRST in the `messages` list, and it applies to the whole conversation, not just the next turn."*

**Live-code with a system message added:**

```python
payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a concise assistant. Always answer in one short sentence."},
        {"role": "user", "content": "What causes seasons on Earth?"}
    ],
    "temperature": 0.3,
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
print(data["choices"][0]["message"]["content"])
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Seasons are caused by the tilt of Earth's axis as it orbits the Sun.
```

**Say:** *"Notice the system message asked for exactly one short sentence, and — unlike our five-word example earlier — this instruction is simple and concrete enough that models typically follow it reliably. Specificity in a system message tends to pay off, which is a preview of Session 4's whole focus."*

### Multi-Turn Conversations — Why You Resend Everything (8 min)

**Say:** *"Here's the fact from last session that becomes very real today: every API call is STATELESS. The model does not remember your previous message unless YOU include it again, as an `assistant` role entry, in the `messages` list you send THIS time."*

**Live-code a two-turn conversation, built manually:**

```python
messages = [
    {"role": "system", "content": "You are a helpful trivia assistant."},
    {"role": "user", "content": "What is the tallest mountain on Earth?"},
]

response = requests.post(url, headers=headers, json={"model": "openai/gpt-4o-mini", "messages": messages})
first_reply = response.json()["choices"][0]["message"]["content"]
print("Turn 1:", first_reply)

# Manually append the assistant's reply, then the next user question
messages.append({"role": "assistant", "content": first_reply})
messages.append({"role": "user", "content": "How tall is it, in meters?"})

response = requests.post(url, headers=headers, json={"model": "openai/gpt-4o-mini", "messages": messages})
second_reply = response.json()["choices"][0]["message"]["content"]
print("Turn 2:", second_reply)
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Turn 1: The tallest mountain on Earth, measured from sea level, is Mount Everest.
Turn 2: Mount Everest is approximately 8,849 meters tall.
```

**Say, pointing at Turn 2's answer:** *"Look closely — the second question was just 'How tall is it, in meters?' with no mention of Everest at all. The ONLY reason the model correctly answered about Everest specifically is that we resent the entire conversation history, including its own first answer, as part of the `messages` list. If we had sent ONLY the second question by itself, the model would have no idea what 'it' refers to."*

**Ask:** *"If this conversation kept going for 50 more turns, what would eventually become a problem, connecting back to last session?"* (Answer: the growing `messages` list eventually approaches the model's context window token limit, and each call also gets more expensive since you're re-sending the whole history every single time.)

### Comprehension Check (4 min)

1. *"If you forget to append the assistant's previous reply before sending the next user message, what happens to the model's ability to reference earlier turns?"* (It loses that context entirely — from the model's perspective, it's as if the earlier turns never happened.)
2. *"Does the `system` message need to be resent on every single call within one conversation, or just the first time?"* (It should be included in the `messages` list on EVERY call, same as everything else — there's no server-side memory; you resend the full relevant history including the system message each time.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict what HTTP status code they'd expect back if they deliberately sent a request with a typo'd, invalid API key. Come back ready to test that guess for real.

---

## SEGMENT 4: Parsing Responses & Multi-Turn Conversations (20 min)

### The Full Response Shape, Field by Field (7 min)

**Say:** *"Let's slow down and look at every field in a real response, because production code needs to read more than just the reply text."*

**Live-code and inspect:**

```python
import json

response = requests.post(url, headers=headers, json={
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "Name one moon of Jupiter."}],
})
data = response.json()
print(json.dumps(data, indent=2))
```

**Example output (illustrative — actual LLM output will vary run to run; JSON shape is the real, correct structure):**
```json
{
  "id": "gen-xyz789",
  "model": "openai/gpt-4o-mini",
  "object": "chat.completion",
  "created": 1732000500,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Europa is one of Jupiter's moons."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 9,
    "total_tokens": 21
  }
}
```

**Say, field by field:** *"`finish_reason` tells you WHY generation stopped — `'stop'` means the model naturally finished its answer. Watch for `'length'` instead, which means the response was CUT OFF because it hit the `max_tokens` limit you set (or a default) — a very common bug source: a response looks incomplete, and the fix is raising `max_tokens`, not something wrong with your prompt. `usage` is your exact token accounting for billing, straight from last session's discussion. `choices` is a LIST — with default settings you'll almost always have exactly one entry at index 0, but some requests can ask for multiple candidate completions at once (an `n` parameter), which is why it's a list, not a single object."*

### Setting `max_tokens` and Handling Truncation (7 min)

**Live-code:**

```python
payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "Explain photosynthesis in detail."}],
    "max_tokens": 15,  # deliberately small, to demonstrate truncation
}
response = requests.post(url, headers=headers, json=payload)
data = response.json()
print("finish_reason:", data["choices"][0]["finish_reason"])
print("content:", data["choices"][0]["message"]["content"])
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
finish_reason: length
content: Photosynthesis is the process by which plants convert sunlight into
```

**Say:** *"There it is — `finish_reason: 'length'`, and the sentence just stops mid-thought. This is exactly what 'ran out of tokens' looks like in practice, and now you know precisely where to check for it (`finish_reason`) instead of just guessing why a response looks cut off."*

### Building a Small Reusable Parsing Helper (6 min)

**Live-code:**

```python
def extract_reply(response_json):
    """Safely extract the assistant's reply text from an OpenRouter response."""
    choices = response_json.get("choices")
    if not choices:
        return None
    return choices[0].get("message", {}).get("content")

reply = extract_reply(data)
print(reply)
```

**Say:** *"We used `.get()` instead of direct bracket indexing on purpose — if the response is malformed or an error response without a `choices` key, `.get()` returns `None` gracefully instead of raising a `KeyError` and crashing your program. We'll build on this defensive pattern properly in SEGMENT 5."*

---

## SEGMENT 5: Errors, Rate Limits & Responsible Retry Logic (20 min)

### Simulating a Bad API Key (5 min)

**Say:** *"Let's deliberately break authentication and see exactly what a real failure looks like, so you recognize it instantly in your own projects."*

**Live-code:**

```python
bad_headers = {
    "Authorization": "Bearer sk-this-is-not-a-real-key",
    "Content-Type": "application/json",
}
response = requests.post(url, headers=bad_headers, json={
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello"}],
})
print("Status code:", response.status_code)
print(response.json())
```

**Example output (illustrative shape — actual error message wording may vary by provider, but a 401 with an error object is the correct, expected real behavior for invalid credentials on OpenRouter and essentially every OpenAI-compatible API):**
```
Status code: 401
{'error': {'message': 'No auth credentials found', 'code': 401}}
```

**Say:** *"401 means Unauthorized — same HTTP status code vocabulary as any other web API. Notice the response is STILL valid JSON, just with an `'error'` key instead of a `'choices'` key. This is exactly why our `extract_reply` helper checked for `choices` safely with `.get()` rather than assuming it's always there."*

### Rate Limits — What 429 Means and How to Respond (8 min)

**Say:** *"The other status code you must handle gracefully in any real project is 429 — Too Many Requests. Every API, including OpenRouter, enforces some limit on how many requests you can send per minute, and some plans additionally cap total tokens per minute. Hitting this limit isn't a bug in your code, necessarily — it's the provider protecting its infrastructure, and well-behaved client code respects it rather than hammering the API in a tight loop."*

**Write the responsible pattern on the board, then live-code it:**

```python
import time

def call_with_retry(payload, max_retries=3):
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            wait_seconds = 2 ** attempt  # exponential backoff: 1, 2, 4...
            print(f"Rate limited. Waiting {wait_seconds}s before retry {attempt + 1}/{max_retries}...")
            time.sleep(wait_seconds)
            continue

        # Any other error: don't blindly retry, surface it
        print(f"Request failed with status {response.status_code}: {response.text}")
        return None

    print("Max retries exceeded.")
    return None
```

**Say, explaining exponential backoff:** *"Notice the wait time DOUBLES each retry: 1 second, then 2, then 4. This is called exponential backoff, and it's the industry-standard, responsible way to handle rate limits — hammering an API with immediate retries the instant it says 'slow down' typically makes the problem worse for you and everyone else sharing that provider's infrastructure. Also notice we only retry on 429 specifically — a 401 (bad key) or a 400 (malformed request) will never succeed no matter how many times you retry, so we fail fast and surface the error instead of wasting time looping."*

### Handling Malformed or Unexpected Responses (4 min)

**Say:** *"One more defensive layer: even a successful 200 response could, in rare edge cases, come back in a shape your code doesn't expect — a network hiccup returning partial JSON, for instance. Wrap the JSON parsing itself in a try/except."*

**Live-code:**

```python
def safe_extract_reply(response):
    try:
        data = response.json()
    except ValueError:
        print("Response was not valid JSON.")
        return None

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        print("Response JSON did not have the expected shape:", data)
        return None
```

**Say:** *"This is the same defensive-programming instinct you practiced in Module 1's file-handling session — never assume external data (a file, an API response) is exactly the shape you expect. Always handle the 'it wasn't' case explicitly, rather than letting your whole program crash on one bad response."*

### Comprehension Check (3 min)

1. *"Should your code automatically retry on a 401 error the same way it retries on a 429?"* (No — a 401 means the credentials themselves are invalid; retrying with the same bad key will never succeed. Only 429 (and sometimes transient 5xx server errors) are worth retrying.)
2. *"What does exponential backoff mean, in one sentence?"* (Each retry waits progressively longer than the last — typically doubling — instead of retrying immediately or at a fixed interval.)

---

## SEGMENT 6: Lab — Build a Robust `ask_llm()` Function (10 min)

### Instructions (read aloud, step by step)

1. Write a function `ask_llm(user_message, system_message=None, model="openai/gpt-4o-mini", temperature=0.7)` that builds the correct `messages` list (including a system message only if one is provided).
2. Send the request using `requests.post()` with correct headers.
3. Handle a 200 response by returning the extracted reply text.
4. Handle a 429 by retrying once with a 2-second wait, then giving up gracefully.
5. Handle any other non-200 status by printing the status code and returning `None` instead of crashing.
6. Test your function with at least two different prompts, one of them using a system message.

### Starter Code

```python
import requests
import time
import os

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(user_message, system_message=None, model="openai/gpt-4o-mini", temperature=0.7):
    headers = {
        "Authorization": f"Bearer {___}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_message:
        messages.append({"role": ___, "content": ___})
    messages.append({"role": ___, "content": ___})

    payload = {
        "model": ___,
        "messages": ___,
        "temperature": ___,
    }

    response = requests.post(___, headers=___, json=___)

    if response.status_code == 200:
        data = response.json()
        return data[___][0][___][___]
    elif response.status_code == ___:
        time.sleep(2)
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return None
    else:
        print(f"Request failed: {response.status_code}")
        return ___

# Test it
print(ask_llm("What is 12 * 8?"))
print(ask_llm("Translate 'good morning' to French.", system_message="You are a translation assistant. Reply with only the translation, nothing else."))
```

### Reference Solution

```python
import requests
import time
import os

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(user_message, system_message=None, model="openai/gpt-4o-mini", temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    elif response.status_code == 429:
        print("Rate limited, retrying once after 2s...")
        time.sleep(2)
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        print(f"Retry also failed: {response.status_code}")
        return None
    else:
        print(f"Request failed: {response.status_code} - {response.text}")
        return None

# Test it
print(ask_llm("What is 12 * 8?"))
print(ask_llm(
    "Translate 'good morning' to French.",
    system_message="You are a translation assistant. Reply with only the translation, nothing else."
))
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
12 * 8 is 96.
Bonjour
```

**Instructor circulates**, checking specifically that students used `.get()`/status-code checks rather than assuming every response has `choices`, and that they correctly only append the `system` role conditionally (a common bug is appending an empty or `None` system message unconditionally, which some providers reject or handle oddly).

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Authenticated and made a raw `requests.post()` call to OpenRouter's chat completions endpoint
- Structured `system`/`user`/`assistant` messages correctly, including manually maintaining multi-turn history
- Parsed the full response shape — `choices`, `finish_reason`, `usage` — and handled truncated responses
- Built responsible error handling: fail-fast on 401/400, exponential-backoff retry on 429, defensive parsing for malformed responses

**Bridge to next session:** *"You can now talk to any LLM on OpenRouter using nothing but `requests` and JSON — a skill that will make you unafraid of any 'AI framework' you meet later, because you now know exactly what they're wrapping. Next session is a change of pace: a pure-math master class on vectors and linear algebra — the mathematics behind 'similarity' that powers embeddings, search, and recommendation systems, and that sets up everything from Session 4's few-shot example selection onward."*

**Homework / self-practice:**
1. Extend `ask_llm()` to accept and forward a `max_tokens` parameter, and test what happens with a deliberately small value (e.g. `max_tokens=10`) — confirm `finish_reason` reads `"length"`.
2. Write a small loop that sends the SAME prompt three times at `temperature=0.0` and three times at `temperature=1.2`, and compare how similar or different the three replies are within each group.
3. Read OpenRouter's own documentation on rate limits and note, in your own words, one detail about how limits work that wasn't covered in class today.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Why use OpenRouter instead of going directly to OpenAI's or Anthropic's own API?**
→ For this course specifically: one account, one key, and access to many providers' models through one consistent request format, which is ideal for comparing models side by side. In a real production project, you might choose a direct provider API instead for reasons like lower latency, provider-specific features, or contractual/compliance requirements — OpenRouter is a genuinely useful tool, not the only correct choice for every project.

**Q: What happens if I don't set `max_tokens` at all?**
→ Each provider/model has its own default and its own hard maximum output length. Not setting it means you get that default behavior, which is usually reasonable for short answers but can lead to unexpectedly long (and expensive) outputs for open-ended prompts. Explicitly setting `max_tokens` is a good production habit once you know roughly how long a response should be.

**Q: If two students send the exact same prompt to the exact same model right now, will they get the exact same answer?**
→ Only if `temperature` (and effectively `top_p`) are set to fully deterministic values, and even then, exact byte-for-byte determinism isn't always strictly guaranteed across a provider's infrastructure. At the default temperature many APIs ship with (often around 0.7-1.0), expect genuinely different answers between the two students, even from the identical prompt.

**Q: Is it safe to put my API key directly in a Colab notebook cell for a quick test?**
→ Only if that notebook is never shared, never committed to a public repository, and the key is revoked afterward. The safe habit — used throughout this session — is loading it from an environment variable or a secrets manager (like Colab's Secrets panel), so the literal key value is never visible in code you might accidentally share.

**Q: Our `call_with_retry` example only retries a FIXED number of times — what happens in a real production system if it still fails after all retries?**
→ A real system typically logs the failure, surfaces a graceful user-facing message ("please try again shortly") rather than a crash or a raw stack trace, and — depending on the application — may queue the request for a later retry or alert an engineer if failures are persistent and widespread rather than a one-off blip.

---

## Instructor Notes

- **Prerequisite check:** Confirm every student has a working OpenRouter API key BEFORE SEGMENT 2 — this is a hard blocker for the entire session. Have 2-3 spare demo keys ready for students whose signup is delayed, so nobody sits idle.
- **Common mistake:** Forgetting the `Bearer ` prefix (with the trailing space) in the `Authorization` header, or including the literal word `Bearer` without a key. Walk past every screen during SEGMENT 2's first live call.
- **Another common mistake:** Sending `messages` as a single dict instead of a list of dicts — a very easy typo (`{"role": "user", "content": "..."}` instead of `[{"role": "user", "content": "..."}]`) that produces a confusing 400 error.
- **Another common mistake:** Forgetting to append the assistant's own reply back into `messages` before the next turn in SEGMENT 3/4, then being confused why the model "forgot" context — this is the single most valuable "aha" moment of the session; don't rush past it.
- **Engagement tip:** SEGMENT 5's deliberate 401 demo (intentionally breaking the key) reliably gets a laugh and cements the error format better than any amount of describing it abstractly — do it live, don't just show a screenshot.
- **Time check:** If running behind before the break, compress SEGMENT 3's multi-turn demo to a single additional turn instead of walking through the full two-turn build.
- **If running long after the break:** Combine SEGMENT 4's `max_tokens`/truncation demo and the parsing-helper demo into one combined live-coding block instead of two separate ones.
- **Materials to prepare:** Verify OpenRouter's status page shows no ongoing outages before class; have a pre-recorded/pre-captured screenshot of a real successful response ready as backup in case of live network issues during the session; spare API keys as noted above.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Missing `Bearer ` prefix in `Authorization` header | 401 Unauthorized even with a valid key | Header value must be exactly `f"Bearer {api_key}"`, including the space |
| `messages` sent as a single dict, not a list | 400 Bad Request, often a vague error message | Always wrap message dicts in a list, even for a single message: `[{"role": "user", "content": "..."}]` |
| Forgetting to append the assistant's reply before the next user turn | Model gives answers that ignore or contradict earlier context | Manually append `{"role": "assistant", "content": reply_text}` to `messages` after every turn before sending the next one |
| Assuming `response.json()` always has a `"choices"` key | `KeyError` crash on error responses (401/429/400) | Always check `response.status_code` first, or use `.get()` defensively when parsing |
| Retrying a 401 in a loop, hoping it eventually works | Wastes time/requests; never succeeds | Only retry on 429 (and transient 5xx); fail fast on 4xx auth/client errors |
| Printing or logging the full API key | Security risk, especially in shared notebooks | Print only a short prefix (e.g. first 8 characters) to confirm the key loaded |

---

## Appendix: Common OpenRouter Model Slugs (Instructor Reference, Illustrative)

The exact set of available models and their slugs changes over time — always check openrouter.ai/models for the current, authoritative list before building a real project. Illustrative examples of the `provider/model-name` format, for demonstrating the pattern only:

| Illustrative slug pattern | Provider routed to |
|---|---|
| `openai/gpt-4o-mini` | OpenAI |
| `anthropic/claude-3.5-sonnet` | Anthropic |
| `google/gemini-flash-1.5` | Google |
| `meta-llama/llama-3.1-8b-instruct` | Meta (via a hosting partner) |

---

## Appendix: Full Request/Response Field Reference (Instructor Reference)

**Common request fields:**

| Field | Type | Purpose |
|---|---|---|
| `model` | string | `provider/model-name` slug to route to |
| `messages` | list of dicts | Conversation history with `role`/`content` pairs |
| `temperature` | float, 0-2 | Randomness control (Session 1) |
| `top_p` | float, 0-1 | Nucleus sampling pool restriction (Session 1) |
| `max_tokens` | int | Hard cap on generated output length |

**Common response fields:**

| Field | Type | Purpose |
|---|---|---|
| `choices[0].message.content` | string | The actual generated reply text |
| `choices[0].finish_reason` | string | `"stop"` (natural end) or `"length"` (truncated) |
| `usage.prompt_tokens` | int | Input token count, for billing |
| `usage.completion_tokens` | int | Output token count, for billing |

---

## FAQ — Additional Questions

**Q: Can I send an image or a file to an LLM through this same endpoint?**
→ Some models support multimodal input (images, for instance) through an extended `content` format (a list of typed content blocks instead of a plain string), but that's beyond today's scope, which focuses on plain text. It's a natural extension of exactly the same request shape you learned today, for when you need it later.

**Q: What's the difference between a 429 from OpenRouter itself versus a 429 forwarded from the underlying provider?**
→ Both are possible — OpenRouter enforces its own limits, and the underlying provider (OpenAI, Anthropic, etc.) may also enforce its own. From your code's perspective, both surface as the same HTTP 429 status, and the same backoff-and-retry strategy is the correct response either way.

**Q: Should `ask_llm()` from today's lab be considered "production-ready" code?**
→ It's a solid, correct foundation, but a real production system would typically add: configurable retry counts and backoff limits, structured logging instead of `print()`, timeout handling on the request itself (`requests.post(..., timeout=30)`), and probably a proper Python logging/monitoring setup instead of console output.

---

## Materials Checklist

- [ ] Every student has a verified working OpenRouter API key before class starts
- [ ] `requests` library available (standard, near-universally pre-installed)
- [ ] Spare demo API keys ready for signup stragglers
- [ ] Scratch notebook with SEGMENT 2/3's live-coding demos pre-typed
- [ ] Backup screenshot of a real successful API response, in case of live network/outage issues
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Compress SEGMENT 3's multi-turn demo to one additional turn instead of the full two-turn build |
| Running long after break | Combine SEGMENT 4's truncation demo and parsing-helper demo into a single live-coding block |
| Low energy after lunch/break | Run SEGMENT 5's deliberate-401-break demo as an interactive "guess the status code" activity before revealing |
| Advanced group finishes lab early | Have them add `max_tokens` and a configurable `max_retries` parameter to `ask_llm()`, and test truncation live |
| No shared screen / projector issue | Walk through the request/response JSON structures on the whiteboard using this script's exact worked examples |
| OpenRouter outage / no internet | Use the backup screenshot and walk through the full request/response cycle without a live call, emphasizing structure over live results |

---

## End-of-Session Quiz (5 Questions)

1. What HTTP header carries your OpenRouter API key, and what literal word must prefix the key value?
2. Why must you manually re-append the assistant's previous reply to `messages` before sending the next user turn?
3. What does `finish_reason: "length"` tell you, and what's the fix?
4. Should your code automatically retry a 401 the same way it retries a 429? Why or why not?
5. Where exactly in the JSON response does the assistant's generated text live?

**Answer key (instructor):**
1. `Authorization`, prefixed with `Bearer ` (the literal word "Bearer" followed by a space, then the key).
2. Because every API call is stateless — the model has no memory of prior turns unless the full relevant history, including its own earlier replies, is resent as part of the current `messages` list.
3. It means the response was cut off because it hit the `max_tokens` limit before the model naturally finished; the fix is raising `max_tokens`.
4. No — a 401 means the credentials are invalid and will never succeed no matter how many times you retry; only retry on 429 (and transient server errors), and fail fast on 4xx client/auth errors.
5. `data["choices"][0]["message"]["content"]`.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| `max_tokens` extension + truncation test | Correctly forwards param, confirms `finish_reason == "length"` with clear explanation | Extension works, thin explanation | Extension present but truncation not actually demonstrated | Not attempted |
| Temperature comparison (0.0 vs 1.2, 3 runs each) | Both groups run, clear comparison of variability observed | Both groups run, thin comparison | Only one temperature tested | Not attempted |
| Rate-limit documentation note | Clear, accurate, specific new detail from official docs | Accurate but generic/already-covered detail | Vague or unclear | Not attempted |

**Total:** /12 — Pass threshold: 8/12
