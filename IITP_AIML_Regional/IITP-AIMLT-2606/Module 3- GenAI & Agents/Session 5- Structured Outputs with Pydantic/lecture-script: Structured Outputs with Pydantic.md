# Lecture Script: Structured Outputs with Pydantic
> **Instructor Reference** — Module 3: GenAI & Agents | Session 5 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students define structured output schemas using Pydantic `BaseModel`, patch an OpenRouter client with the `instructor` library to enforce structured JSON responses, and validate/parse structured LLM outputs while handling malformed responses gracefully — closing the gap Session 4 left open between "usually formatted correctly" and "guaranteed, validated structure."

**Student profile at this point:** Comfortable with raw OpenRouter API calls (Session 2) and deliberate prompt design (Session 4). Has NOT used Pydantic before in this course (it wasn't part of Module 1/2's curriculum) — today introduces `BaseModel` from first principles, correctly, using current Pydantic v2 syntax. This is the final session of the first five in Module 3.

**Key outcome:** Every student can define a Pydantic `BaseModel` schema with typed fields (including `Literal` choices and nested models), validate a plain dict or JSON string against it and correctly interpret a `ValidationError`, patch an OpenRouter-backed OpenAI client with `instructor` to get a schema-enforced LLM response directly as a validated Python object (no manual JSON parsing), and write a `try/except` wrapper that handles a validation failure gracefully instead of crashing.

**Dataset for this session:** None required from disk — small inline example dicts/JSON strings and schemas serve as this session's working material.

**API note for this script:** All Pydantic `BaseModel` code and validation examples in this script are ACTUAL, VERIFIED code — every printed output for plain Pydantic sections (no LLM call involved) has been run and confirmed correct against Pydantic v2 (`model_dump()`, `model_validate_json()`, `ValidationError` messages, etc.). For sections where `instructor` patches a live LLM call, the REQUEST code and the `instructor`/`BaseModel` API usage are written to be correct, current, and directly runnable, but the actual LLM-populated field VALUES in example responses are marked **"Example output (illustrative — actual LLM output will vary run to run)"** since this script is not executed against a live paid API key.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — The Problem With "Usually Correct" JSON | 10 min | 0:10 |
| SEGMENT 2: Pydantic `BaseModel` Fundamentals | 25 min | 0:35 |
| SEGMENT 3: Validating Data & Reading `ValidationError` | 20 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Patching OpenRouter with `instructor` | 25 min | 1:30 |
| SEGMENT 5: Handling Malformed Responses Gracefully | 15 min | 1:45 |
| SEGMENT 6: Lab — A Validated Ticket-Extraction Pipeline | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — The Problem With "Usually Correct" JSON (10 min)

### The Hook (5 min)

**Say:** *"Last session, our best prompts got a model to respond with just one word, like `HIGH` or `SPAM`. That's a huge improvement over a paragraph of prose. But 'usually responds with just one clean word' is still not the same as 'GUARANTEED to respond with exactly one of three specific labels, every single time, in a form your code can trust without checking.' Today we close that gap completely."*

**Live-code a realistic failure of prompt-only formatting:**

```python
prompt = """Extract the customer's name, order number, and issue category
(one of: SHIPPING, BILLING, DEFECTIVE_ITEM, OTHER) from this message,
as JSON with keys name, order_number, issue_category.

Message: "Hi, this is Rohan Verma, order #48213 — the item arrived cracked."
"""

print(ask_llm(prompt))
```

**Example output (illustrative — actual LLM output will vary run to run; this is a realistic FAILURE MODE, not a guaranteed one — the point is that it's POSSIBLE and prompt-only formatting cannot rule it out):**
```
Sure! Here's the extracted information:

```json
{
  "name": "Rohan Verma",
  "order_number": "48213",
  "issue_category": "Damaged Item"
}
```
```

**Say:** *"Two real problems in this one illustrative response, both common in practice. One: the model wrapped the JSON in a friendly sentence and markdown code fences — if your code does `json.loads(response_text)` directly, this crashes, because that's not valid JSON on its own, it's JSON embedded inside other text. Two, and more subtle: `issue_category` came back as `'Damaged Item'`, which is NOT one of our four allowed categories (`SHIPPING`, `BILLING`, `DEFECTIVE_ITEM`, `OTHER`) — the model invented a plausible-sounding but off-schema value. Neither failure is a 'bug' in the traditional sense — the model did a genuinely reasonable job at the LANGUAGE task. The problem is we needed a STRICT DATA CONTRACT, and prompting alone, even good prompting, cannot fully guarantee one."*

### Why This Session Matters (5 min)

**Say:** *"This is precisely the problem Pydantic plus the `instructor` library solves. Pydantic lets you define, in Python, EXACTLY what a valid piece of data looks like — field names, types, allowed values. `instructor` then uses that definition to force and validate an LLM's response against it directly, re-asking the model automatically if the first attempt doesn't validate. By the end of today, the messy example above becomes a guaranteed, typed Python object — no manual JSON parsing, no manual checking whether `issue_category` is one of the four allowed values, because the SCHEMA enforces it."*

**Learning contract for today — write on board:**

- Define a Pydantic `BaseModel` schema with typed and constrained fields
- Validate data against a schema and correctly read a `ValidationError`
- Use `instructor` to patch an OpenRouter-backed client for guaranteed structured output
- Handle a validation failure gracefully, without crashing the program

---

## SEGMENT 2: Pydantic `BaseModel` Fundamentals (25 min)

### Your First Schema (8 min)

**Say:** *"Pydantic v2 is the current version, and the syntax we use today reflects that — some older tutorials online use Pydantic v1 syntax, which differs in a few method names. We're using `BaseModel`, the standard building block: a Python class where every attribute is a typed FIELD, and Pydantic automatically validates and converts data against those types."*

**Live-code a first schema:**

```python
from pydantic import BaseModel

class SupportTicket(BaseModel):
    customer_name: str
    order_number: int
    issue_description: str

ticket = SupportTicket(
    customer_name="Rohan Verma",
    order_number=48213,
    issue_description="Item arrived cracked",
)
print(ticket)
print(type(ticket))
```

**Example output (actual — verified by running this exact code against Pydantic v2):**
```
customer_name='Rohan Verma' order_number=48213 issue_description='Item arrived cracked'
<class '__main__.SupportTicket'>
```

**Say:** *"This is a real, typed Python object — not a dict, not raw JSON. You get `ticket.customer_name`, `ticket.order_number` with dot-notation access AND type safety, and if you try to construct one with the wrong type for a field, Pydantic will actually try to coerce it if reasonable, or raise a clear error if it can't."*

**Live-code showing automatic type coercion:**

```python
ticket2 = SupportTicket(
    customer_name="Anita Rao",
    order_number="48910",  # a string here, but the field expects int
    issue_description="Billing question",
)
print(ticket2.order_number, type(ticket2.order_number))
```

**Example output (actual — verified):**
```
48910 <class 'int'>
```

**Say:** *"Notice we passed `'48910'` as a STRING, but `ticket2.order_number` came back as an actual `int`. Pydantic tried to coerce the string into the declared type, succeeded because it was a clean numeric string, and stored the correctly-typed value. This 'coerce if reasonable, error if not' behavior is exactly why Pydantic is so useful for LLM output specifically — LLMs often return numbers as strings inside JSON, and Pydantic cleans that up automatically rather than you writing manual `int(...)` conversions everywhere."*

### Restricting Values with `Literal` (7 min)

**Say:** *"Plain `str` accepts ANY string — but our `issue_category` field from the opening demo needed to be one of exactly four specific values. For that, use `Literal`, imported from `typing`."*

**Live-code:**

```python
from typing import Literal

class SupportTicketV2(BaseModel):
    customer_name: str
    order_number: int
    issue_category: Literal["SHIPPING", "BILLING", "DEFECTIVE_ITEM", "OTHER"]

good_ticket = SupportTicketV2(
    customer_name="Rohan Verma",
    order_number=48213,
    issue_category="DEFECTIVE_ITEM",
)
print(good_ticket)
```

**Example output (actual — verified):**
```
customer_name='Rohan Verma' order_number=48213 issue_category='DEFECTIVE_ITEM'
```

**Say:** *"This is the fix for problem #2 from our opening demo. `Literal[...]` tells Pydantic that ONLY these exact four strings are valid — anything else, including a plausible-sounding near-miss like `'Damaged Item'`, will raise a `ValidationError`, which we'll see and handle properly in SEGMENT 3."*

### `Field()` for Descriptions, Defaults, and Constraints (6 min)

**Say:** *"`Field()` lets you add metadata to a field — a description (which, as we'll see in SEGMENT 4, `instructor` actually shows to the LLM to help it understand what to generate), a default value, or numeric constraints."*

**Live-code:**

```python
from pydantic import Field

class SupportTicketV3(BaseModel):
    customer_name: str
    order_number: int
    issue_category: Literal["SHIPPING", "BILLING", "DEFECTIVE_ITEM", "OTHER"]
    urgency_score: int = Field(ge=1, le=5, description="Urgency from 1 (low) to 5 (critical)")
    requires_manager: bool = False  # default value if not provided

t = SupportTicketV3(
    customer_name="Priya Nair",
    order_number=91022,
    issue_category="BILLING",
    urgency_score=4,
)
print(t)
```

**Example output (actual — verified):**
```
customer_name='Priya Nair' order_number=91022 issue_category='BILLING' urgency_score=4 requires_manager=False
```

**Say:** *"`ge=1, le=5` means 'greater than or equal to 1, less than or equal to 5' — a numeric range constraint. `requires_manager` wasn't provided at all, so it fell back to its default, `False`. And that `description` string isn't just documentation for humans reading your code — when `instructor` builds a schema to send to the LLM, that description text becomes part of what GUIDES the model's understanding of what value belongs in that field, which is a genuinely important detail for SEGMENT 4."*

### Comprehension Check (4 min)

1. *"If a field is typed `int` and you pass the string `'42'`, what happens?"* (Pydantic coerces it to the integer `42`, since it's a clean, unambiguous numeric string.)
2. *"What does `Literal["A", "B", "C"]` do that a plain `str` type doesn't?"* (Restricts the field to ONLY those exact values; anything else raises a validation error.)

---

## SEGMENT 3: Validating Data & Reading `ValidationError` (20 min)

### Validating From a Dict or JSON String (7 min)

**Say:** *"So far we've constructed objects directly with keyword arguments. In practice, LLM output arrives as a JSON STRING (or a Python dict after `json.loads`), not neat keyword arguments. Pydantic has dedicated methods for exactly that."*

**Live-code:**

```python
json_string = '{"customer_name": "Anita Rao", "order_number": 55210, "issue_category": "SHIPPING", "urgency_score": 2}'

ticket_from_json = SupportTicketV3.model_validate_json(json_string)
print(ticket_from_json)

data_dict = {"customer_name": "Karan Mehta", "order_number": 33012, "issue_category": "OTHER", "urgency_score": 1}
ticket_from_dict = SupportTicketV3.model_validate(data_dict)
print(ticket_from_dict)
```

**Example output (actual — verified):**
```
customer_name='Anita Rao' order_number=55210 issue_category='SHIPPING' urgency_score=2 requires_manager=False
customer_name='Karan Mehta' order_number=33012 issue_category='OTHER' urgency_score=1 requires_manager=False
```

**Say:** *"`model_validate_json()` for a raw JSON string, `model_validate()` for an already-parsed dict — both run the exact same validation rules as constructing the object directly. And going the other direction, back to JSON, is just as simple."*

**Live-code:**

```python
print(ticket_from_json.model_dump())        # plain Python dict
print(ticket_from_json.model_dump_json())    # JSON string
```

**Example output (actual — verified):**
```
{'customer_name': 'Anita Rao', 'order_number': 55210, 'issue_category': 'SHIPPING', 'urgency_score': 2, 'requires_manager': False}
{"customer_name":"Anita Rao","order_number":55210,"issue_category":"SHIPPING","urgency_score":2,"requires_manager":false}
```

**Say:** *"`model_dump()` and `model_dump_json()` are the Pydantic v2 method names — if you ever see `.dict()` or `.json()` in an older tutorial, that's Pydantic v1 syntax; it may still work with a deprecation warning depending on the installed version, but `model_dump()`/`model_dump_json()` are the current, correct methods to use going forward."*

### Triggering and Reading a `ValidationError` (9 min)

**Say:** *"Now let's deliberately break validation, on purpose, and read the error message carefully — because in production, THIS is what you'll be catching and handling."*

**Live-code:**

```python
from pydantic import ValidationError

bad_data = {
    "customer_name": "Sanya Kapoor",
    "order_number": "not-a-number",
    "issue_category": "DAMAGED",  # not one of our four allowed values
    "urgency_score": 9,           # out of the 1-5 range
}

try:
    ticket = SupportTicketV3.model_validate(bad_data)
except ValidationError as e:
    print(e)
```

**Example output (actual — verified by running this exact code):**
```
3 validation errors for SupportTicketV3
order_number
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not-a-number', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/int_parsing
issue_category
  Input should be 'SHIPPING', 'BILLING', 'DEFECTIVE_ITEM' or 'OTHER' [type=literal_error, input_value='DAMAGED', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/literal_error
urgency_score
  Input should be less than or equal to 5 [type=less_than_equal, input_value=9, input_type=int]
    For further information visit https://errors.pydantic.dev/2.13/v/less_than_equal
```

**Say, walking through the structure:** *"Three separate errors reported in ONE exception — Pydantic doesn't stop at the first problem, it collects ALL of them, which is enormously useful for debugging a malformed LLM response: you see every field that failed, not just the first. Each error names the exact field (`order_number`, `issue_category`, `urgency_score`), the TYPE of error (`int_parsing`, `literal_error`, `less_than_equal`), and the actual bad input value that was rejected. This structure is exactly what we'll use in SEGMENT 5 to build genuinely useful error-handling, not just a blanket 'something went wrong.'"*

### Programmatically Inspecting Errors (4 min)

**Say:** *"You rarely want to just print the raw error text in production — you usually want to inspect it programmatically, for example to decide whether to retry."*

**Live-code:**

```python
try:
    ticket = SupportTicketV3.model_validate(bad_data)
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {error['loc']}, Problem: {error['msg']}")
```

**Example output (actual — verified):**
```
Field: ('order_number',), Problem: Input should be a valid integer, unable to parse string as an integer
Field: ('issue_category',), Problem: Input should be 'SHIPPING', 'BILLING', 'DEFECTIVE_ITEM' or 'OTHER'
Field: ('urgency_score',), Problem: Input should be less than or equal to 5
```

**Say:** *"`e.errors()` gives you a clean list of dicts, one per problem, each with a `'loc'` (which field, as a tuple, since nested models can have deeper paths) and a `'msg'`. This is what real error-handling code inspects — logging exactly which field failed and why, rather than showing a raw traceback to an end user."*

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict how `instructor` might use a Pydantic schema to get an LLM to return correctly-structured data in the first place — is it just prompting behind the scenes, is it something else, or some combination? Come back ready to see how it actually works.

---

## SEGMENT 4: Patching OpenRouter with `instructor` (25 min)

### What `instructor` Actually Does (6 min)

**Say:** *"`instructor` is a library that 'patches' a standard OpenAI-compatible client — which our OpenRouter setup from Session 2 already is, since OpenRouter deliberately mirrors OpenAI's request format — so that a single new parameter, `response_model`, becomes available on `chat.completions.create()`. You pass it a Pydantic class, and instead of getting back raw JSON text you have to parse yourself, you get back an already-validated INSTANCE of that class directly."*

**Say:** *"Mechanically, under the hood, `instructor` does roughly what you'd expect from your break-time guesses: it builds a JSON-schema description of your Pydantic model (which is why `Field(description=...)` from SEGMENT 2 matters — that text gets included), sends it to the model as part of the request so the model knows the exact shape to produce, parses the model's JSON response, validates it against your Pydantic schema, and — this is the genuinely powerful part — if validation FAILS, it can automatically retry the API call, showing the model its own validation error, asking it to correct the mistake. You get the reliability of a hand-written validation loop, without writing that loop yourself."*

**Say:** *"Install it with `pip install instructor` if you haven't already."*

### Setting Up the Patched Client (8 min)

**Say:** *"`instructor` patches an `OpenAI`-shaped client object, so first we create a standard `openai.OpenAI` client, but point its `base_url` at OpenRouter instead of OpenAI directly — this works because OpenRouter is intentionally OpenAI-API-compatible."*

**Live-code:**

```python
import os
import instructor
from openai import OpenAI

base_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

client = instructor.from_openai(base_client)
```

**Say:** *"That's the entire setup — two lines of real work. `base_client` is a normal OpenAI-shaped client pointed at OpenRouter's endpoint. `instructor.from_openai(base_client)` wraps it, returning a new client with the exact same interface PLUS the new `response_model` capability. Everything else about how you'd call it looks almost identical to a normal OpenAI-style call."*

### Making Your First Structured Call (7 min)

**Say:** *"Let's re-run our opening demo's exact scenario, but now with a guaranteed schema instead of a hopeful prompt."*

**Live-code:**

```python
from pydantic import BaseModel
from typing import Literal

class ExtractedTicket(BaseModel):
    customer_name: str
    order_number: int
    issue_category: Literal["SHIPPING", "BILLING", "DEFECTIVE_ITEM", "OTHER"]

result = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    response_model=ExtractedTicket,
    messages=[
        {"role": "user", "content": "Hi, this is Rohan Verma, order #48213 — the item arrived cracked."}
    ],
)

print(result)
print(type(result))
print(result.issue_category)
```

**Example output (illustrative — actual LLM output will vary run to run in terms of which exact category is chosen for an ambiguous case, but the STRUCTURE — a validated `ExtractedTicket` instance with `issue_category` guaranteed to be one of our four literal values — is the real, correct behavior `instructor` provides, not something that can silently fail the way the opening demo's raw prompt did):**
```
customer_name='Rohan Verma' order_number=48213 issue_category='DEFECTIVE_ITEM'
<class '__main__.ExtractedTicket'>
DEFECTIVE_ITEM
```

**Say:** *"Compare this directly to SEGMENT 1's opening failure. No markdown code fences to strip. No manual `json.loads()`. No manually checking whether `issue_category` is one of our four allowed values — Pydantic's `Literal` constraint, enforced through `instructor`, GUARANTEES it, or the call would have raised a validation error (with automatic retry attempted first) instead of silently returning something like `'Damaged Item'`. This is the entire value proposition of today's session in one worked example."*

### Comprehension Check (4 min)

1. *"What new parameter does `instructor` add to `client.chat.completions.create()`?"* (`response_model`, which takes a Pydantic `BaseModel` class.)
2. *"Why does `base_client` point `base_url` at OpenRouter instead of using OpenAI directly?"* (Because OpenRouter's API is intentionally OpenAI-compatible, so the standard `OpenAI` client class works against it just by changing the base URL and API key.)

---

## SEGMENT 5: Handling Malformed Responses Gracefully (15 min)

### Why You Still Need a Try/Except, Even With `instructor` (5 min)

**Say:** *"`instructor` dramatically reduces malformed-output failures by retrying automatically when validation fails — but 'dramatically reduces' is not the same as 'mathematically impossible.' A model might still fail validation on every retry attempt (for a genuinely ambiguous or adversarial input), or the network call itself might fail entirely. Production code should never assume ANY external call — including a nicely wrapped one — can't fail."*

### Building a Defensive Wrapper (7 min)

**Live-code:**

```python
from pydantic import ValidationError

def extract_ticket_safely(message_text, max_retries=2):
    try:
        result = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            response_model=ExtractedTicket,
            max_retries=max_retries,  # instructor's own built-in retry-on-validation-failure count
            messages=[{"role": "user", "content": message_text}],
        )
        return result
    except ValidationError as e:
        print(f"Could not extract a valid ticket after retries. Errors: {e.errors()}")
        return None
    except Exception as e:
        print(f"Unexpected error during extraction: {e}")
        return None

ticket = extract_ticket_safely("asdkj not really a support message at all, just noise")
if ticket is None:
    print("Falling back to manual review queue.")
else:
    print(ticket)
```

**Say:** *"Two separate `except` blocks, deliberately. `ValidationError` is the SPECIFIC, expected failure mode — even after `instructor`'s built-in retries, the model genuinely couldn't produce something matching our schema (a realistic outcome for a nonsense input like this one, which doesn't actually describe a support ticket at all). We handle that with a clear message and a sensible fallback — here, routing to a manual review queue rather than crashing the whole pipeline. The broader `Exception` catch is a safety net for anything else unexpected — a network timeout, an auth failure, anything not specifically a schema validation problem — logged clearly rather than taking down the whole program."*

**Say:** *"Notice `max_retries` is passed directly into `instructor`'s own `create()` call — this controls how many times `instructor` will automatically retry, showing the model its own validation error, BEFORE giving up and raising `ValidationError` up to our own code. This is a genuinely different, and more efficient, retry mechanism than Session 2's exponential-backoff retry — that one handled RATE LIMITS (429s); this one handles SCHEMA VALIDATION failures. Both are real, both matter, and a mature production system often needs both, for different failure modes."*

### Designing Schemas That Are Easier for the Model to Satisfy (3 min)

**Say:** *"One more practical tip, connecting back to Session 4's prompt engineering: a well-designed schema is itself a form of prompt engineering. Clear `Field(description=...)` text, sensibly-named fields, and `Literal` choices that are genuinely mutually exclusive and unambiguous all reduce how often the model needs a retry in the first place. A confusing or overly complex schema — deeply nested, ambiguous field names, overlapping category choices — will produce more validation failures even with `instructor`'s retry safety net, simply because the model has a harder time understanding exactly what's being asked."*

---

## SEGMENT 6: Lab — A Validated Ticket-Extraction Pipeline (10 min)

### Instructions (read aloud, step by step)

1. Define a Pydantic schema `FeedbackEntry` with fields: `customer_sentiment` (`Literal["POSITIVE", "NEGATIVE", "MIXED"]`), `product_mentioned` (`str`), `follow_up_needed` (`bool`), and `priority` (`int`, constrained between 1 and 5 using `Field`).
2. Write a function `extract_feedback_safely(text)` that uses the `instructor`-patched `client` to extract a `FeedbackEntry` from raw customer feedback text, wrapped in a try/except that handles `ValidationError` gracefully.
3. Test it against two example feedback strings, one clearly well-formed and one deliberately vague/nonsensical.
4. Confirm the well-formed case returns a valid `FeedbackEntry` object, and the vague case either returns a best-effort valid object or `None` with a clear printed message — not a crash.

### Starter Code

```python
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

class FeedbackEntry(BaseModel):
    customer_sentiment: Literal[___, ___, ___]
    product_mentioned: ___
    follow_up_needed: ___
    priority: int = Field(ge=___, le=___)

def extract_feedback_safely(text, max_retries=2):
    try:
        result = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            response_model=___,
            max_retries=___,
            messages=[{"role": "user", "content": ___}],
        )
        return result
    except ValidationError as e:
        print(f"Validation failed: {___}")
        return None

# Test cases
well_formed = "The new blender is great but shipping took way too long -- 10 days! Might return it if it happens again."
vague = "hmm ok"

print(extract_feedback_safely(well_formed))
print(extract_feedback_safely(vague))
```

### Reference Solution

```python
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

class FeedbackEntry(BaseModel):
    customer_sentiment: Literal["POSITIVE", "NEGATIVE", "MIXED"]
    product_mentioned: str
    follow_up_needed: bool
    priority: int = Field(ge=1, le=5)

def extract_feedback_safely(text, max_retries=2):
    try:
        result = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            response_model=FeedbackEntry,
            max_retries=max_retries,
            messages=[{"role": "user", "content": text}],
        )
        return result
    except ValidationError as e:
        print(f"Validation failed after retries: {e.errors()}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

well_formed = "The new blender is great but shipping took way too long -- 10 days! Might return it if it happens again."
vague = "hmm ok"

print(extract_feedback_safely(well_formed))
print(extract_feedback_safely(vague))
```

**Example output (illustrative — actual LLM output will vary run to run; the well-formed case has clear signal (mixed sentiment, a named product, an implied follow-up risk) so a valid `FeedbackEntry` is the realistic and expected outcome, while the vague case has almost no extractable signal, so a low-confidence best-effort object OR a graceful `None` with a printed message are both realistic, acceptable outcomes — the key contract is that neither case crashes the program):**
```
customer_sentiment='MIXED' product_mentioned='blender' follow_up_needed=True priority=3
Validation failed after retries: [{'type': 'missing', 'loc': ('product_mentioned',), 'msg': 'Field required', ...}]
```

**Instructor circulates**, checking specifically that students used `Literal` (not plain `str`) for `customer_sentiment`, that `Field(ge=1, le=5)` is used for the numeric constraint rather than validating the range manually after the fact, and that BOTH `ValidationError` and a general `Exception` are caught so a genuinely unexpected failure (e.g. a network issue) also doesn't crash the lab.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Defined Pydantic v2 `BaseModel` schemas with typed fields, `Literal` constraints, and `Field()` metadata
- Validated data with `model_validate()`/`model_validate_json()` and read structured `ValidationError` output
- Patched an OpenRouter-backed OpenAI client with `instructor` to get guaranteed, schema-validated LLM responses via `response_model`
- Built defensive error handling distinguishing `ValidationError` (schema failure) from general exceptions (everything else)

**Bridge to what comes next:** *"This wraps the first five sessions of Module 3. You now have the complete foundational toolkit: how LLMs generate text (Session 1), how to call them directly (Session 2), the math behind similarity and embeddings (Session 3), how to shape what they produce through prompting (Session 4), and now, how to GUARANTEE the shape of what comes back (Session 5). Every one of these pieces — tokens, raw API calls, vectors, prompting technique, and validated structured output — is a building block the next set of sessions will combine into more advanced GenAI systems, including retrieval and agents."*

**Homework / self-practice:**
1. Extend `FeedbackEntry` with a nested `BaseModel` field — for example, a `ProductDetails` model with `name: str` and `category: str`, used as `product: ProductDetails` instead of a flat `product_mentioned: str`. Test that nested validation errors still report a clear `'loc'` path (e.g. `('product', 'category')`).
2. Deliberately construct a dict that fails validation in THREE different ways at once for a schema of your choosing, and print each individual error's field and message using `e.errors()`.
3. Write 3-4 sentences comparing today's `instructor`-based validation retry (SEGMENT 5) to Session 2's exponential-backoff retry for rate limits — what different FAILURE MODE does each one solve, and why can't one technique substitute for the other?

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Do I always need `instructor` to use Pydantic with an LLM, or could I validate the response myself without it?**
→ You could — call the raw API as in Session 2, get the JSON text back, and manually call `YourModel.model_validate_json(response_text)` yourself, catching `ValidationError` yourself. `instructor` is a convenience and reliability layer on top of that same idea: it additionally builds the schema description automatically from your Pydantic class and sends it to the model, and it automatically retries with the model's own error shown back to it on failure — both of which you'd otherwise have to hand-write.

**Q: Is `response_model` an OpenAI API parameter, or something `instructor` invents?**
→ It's specific to `instructor` — it's not part of OpenAI's or OpenRouter's actual API. `instructor` intercepts the call, translates your Pydantic schema into whatever structured-output or tool-calling mechanism the underlying model/provider actually supports, and translates the raw response back into your validated Pydantic object — all invisibly, from your code's point of view.

**Q: What happens if I use a model that doesn't support "real" structured/JSON output well at all?**
→ `instructor` generally still works by prompting the model carefully to produce JSON and validating what comes back, but reliability (how often it needs a retry) can vary meaningfully depending on how well the underlying model follows formatting instructions in general — connecting back to Session 4's discussion of prompting quality mattering. Models with strong native structured-output support tend to need fewer `instructor` retries in practice.

**Q: Can `Literal` fields include numbers, not just strings?**
→ Yes — `Literal[1, 2, 3]` is valid and works the same way, restricting the field to exactly those integer values. `Literal` works with any combination of fixed, hashable values, not just strings.

**Q: Is there a limit to how deeply nested a Pydantic schema (nested `BaseModel`s inside other `BaseModel`s) can be for `instructor` to handle correctly?**
→ No hard technical limit in Pydantic or `instructor` itself, but very deep nesting tends to make it genuinely harder for the model to produce a fully correct structure on the first attempt, leading to more retries. As a practical rule, keep schemas as flat and simple as the actual data genuinely requires — nest only when the data is truly hierarchical.

---

## Instructor Notes

- **Prerequisite check:** Confirm `pip install pydantic instructor openai` all succeed before class — three dependencies today instead of one, worth testing installs ahead of time.
- **Common mistake:** Using Pydantic v1 method names (`.dict()`, `.json()`, `.parse_obj()`) copied from an older tutorial found online. Correct to v2 (`model_dump()`, `model_dump_json()`, `model_validate()`) explicitly if this surfaces.
- **Another common mistake:** Forgetting to import `Literal` from `typing` and instead trying to use it as a bare Pydantic feature — clarify it's a standard Python typing construct that Pydantic specifically knows how to validate against, not something Pydantic itself defines.
- **Another common mistake:** In SEGMENT 6's lab, catching only `ValidationError` and not a broader `Exception`, missing genuinely unexpected failures like network errors. Point this out explicitly during the lab if you see it.
- **Engagement tip:** SEGMENT 4's structured-call demo, directly re-running the SEGMENT 1 opening failure scenario with a guaranteed schema this time, is the strongest "full circle" moment of the session — explicitly call back to the opening demo's two named problems and confirm both are now solved.
- **Time check:** If running behind before the break, shorten SEGMENT 3's "programmatically inspecting errors" block to a quick mention of `e.errors()` existing, without a full live-coded loop.
- **If running long after the break:** Compress SEGMENT 5 to just the try/except pattern without the "designing easier schemas" discussion (assign it as a homework reading note instead).
- **Materials to prepare:** `pydantic`, `instructor`, and `openai` all installed and verified; scratch notebook with SEGMENT 2 and 3's fully-verified Pydantic code pre-typed; a backup pre-captured example of a real `instructor` structured response, in case of live API/network issues during SEGMENT 4.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Using Pydantic v1 method names (`.dict()`, `.json()`) | `AttributeError` or deprecation warning depending on installed version | Use `model_dump()` / `model_dump_json()` / `model_validate()` (Pydantic v2 syntax) |
| Forgetting `from typing import Literal` | `NameError: name 'Literal' is not defined` | Import `Literal` from the standard library `typing` module |
| Passing a plain dict/string where `response_model` expects a Pydantic CLASS, not an instance | `TypeError` or unexpected behavior from `instructor` | Pass the class itself, e.g. `response_model=ExtractedTicket`, not `response_model=ExtractedTicket(...)` |
| Catching only `ValidationError`, not general `Exception`, in production wrappers | An unrelated failure (network, auth) still crashes the program | Add a broader `except Exception` fallback after the specific `except ValidationError` |
| Overly complex/deeply nested schema causing frequent `instructor` retries | Slow, expensive calls; frequent validation failures even with retries | Simplify the schema, add clearer `Field(description=...)` text, flatten nesting where the data genuinely allows it |

---

## Appendix: Nested Models Worked Example (Optional, If Time Allows)

```python
from pydantic import BaseModel
from typing import List

class LineItem(BaseModel):
    product_name: str
    quantity: int

class Order(BaseModel):
    customer_name: str
    items: List[LineItem]

order_data = {
    "customer_name": "Meera Iyer",
    "items": [
        {"product_name": "Wireless Mouse", "quantity": 2},
        {"product_name": "USB-C Cable", "quantity": 1},
    ],
}

order = Order.model_validate(order_data)
print(order)
print(order.items[0].product_name, order.items[0].quantity)
```

**Example output (actual — verified by running this exact code against Pydantic v2):**
```
customer_name='Meera Iyer' items=[LineItem(product_name='Wireless Mouse', quantity=2), LineItem(product_name='USB-C Cable', quantity=1)]
Wireless Mouse 2
```

**Say (if running this appendix):** *"A `BaseModel` can contain a `List` of OTHER `BaseModel`s — this is how you represent genuinely hierarchical data, like an order with multiple line items, each with their own typed fields. `instructor` handles nested schemas like this the same way it handles flat ones — it just builds a more detailed schema description for the model to follow."*

---

## Appendix: Pydantic v1 vs. v2 Quick Reference (Instructor Reference)

| Pydantic v1 (older, may appear in older tutorials) | Pydantic v2 (current, use this) |
|---|---|
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `.parse_obj(data)` | `.model_validate(data)` |
| `.parse_raw(json_str)` | `.model_validate_json(json_str)` |
| `class Config:` inner class | `model_config = ConfigDict(...)` |

---

## FAQ — Additional Questions

**Q: Does `instructor` work with ANY model available on OpenRouter, or only certain ones?**
→ It works most reliably with models that have strong native support for structured/JSON output or tool-calling, since `instructor` typically builds on top of those provider-side features. Support and reliability can vary by model — always test with your specific chosen model rather than assuming universal identical behavior.

**Q: If `instructor` automatically retries on validation failure, does that mean it silently changes my `messages` list?**
→ It appends additional context internally for the retry attempt (typically including the previous invalid output and the validation error), so the model has something concrete to correct — but it does not silently modify the `messages` list YOU originally constructed for future calls; each `create()` call is its own independent request/retry cycle.

**Q: Should every single LLM-facing feature in a real application use `instructor`/structured output, even simple ones?**
→ Not necessarily — for genuinely free-form text generation (a chatbot reply, a written summary meant for a human to read as prose), structured output doesn't apply. Reach for `instructor`/Pydantic specifically when the OUTPUT needs to plug into other code as clean, typed, validated data — extraction, classification, form-filling, anything downstream code will parse and act on programmatically.

---

## Materials Checklist

- [ ] `pydantic`, `instructor`, and `openai` installed and verified on the demo machine
- [ ] Scratch notebook with SEGMENT 2 and 3's fully-verified Pydantic code pre-typed
- [ ] Backup pre-captured example of a real `instructor` structured response, for network/outage contingency
- [ ] Whiteboard space for the `ValidationError` structure walkthrough
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's "programmatically inspecting errors" block to a brief mention of `e.errors()` |
| Running long after break | Compress SEGMENT 5 to just the try/except pattern, skip the schema-design discussion |
| Low energy after lunch/break | Run the Appendix nested-models demo as a group "predict the output" activity before revealing |
| Advanced group finishes lab early | Have them add a nested `BaseModel` field to their `FeedbackEntry` schema and re-test |
| No shared screen / projector issue | Walk through the `ValidationError` output and `instructor` request/response flow on the whiteboard using this script's exact verified examples |
| OpenRouter outage / no internet | Use the backup pre-captured example for SEGMENT 4, focus live coding entirely on SEGMENT 2/3's plain Pydantic work, which requires no network access at all |

---

## End-of-Session Quiz (5 Questions)

1. What does `Literal["A", "B", "C"]` do differently from a plain `str` type annotation?
2. Which Pydantic v2 method converts a validated object back into a plain Python dict?
3. What new parameter does `instructor` add to `client.chat.completions.create()`, and what does it take as a value?
4. Why should production code catch both `ValidationError` specifically AND a general `Exception`, rather than just one or the other?
5. Name one way a well-designed Pydantic schema (field names, descriptions, choices) can reduce how often `instructor` needs to retry.

**Answer key (instructor):**
1. It restricts the field to ONLY the exact listed values; anything else raises a validation error, whereas plain `str` accepts any string.
2. `model_dump()` (and `model_dump_json()` for a JSON string specifically).
3. `response_model`, which takes a Pydantic `BaseModel` class (not an instance) defining the expected output schema.
4. `ValidationError` is the specific, expected schema-failure case with structured, actionable error detail; a general `Exception` catch is a safety net for anything else unexpected (network errors, auth failures) that would otherwise crash the program.
5. Any one of: clear `Field(description=...)` text, unambiguous/mutually-exclusive `Literal` choices, sensibly-named fields, or flatter (less deeply nested) structure where the data allows it.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Nested `ProductDetails` model + validation error path test | Correct nested schema, error `'loc'` path correctly demonstrated | Nested schema correct, error path not fully demonstrated | Nesting attempted with errors | Not attempted |
| Triple-failure validation dict + `e.errors()` breakdown | All 3 errors correctly triggered and clearly printed individually | 2-3 errors triggered, minor reporting issues | Fewer than 2 real errors triggered | Not attempted |
| `instructor` retry vs. rate-limit retry comparison write-up | Clear, correct distinction between the two failure modes and why neither substitutes for the other | Mostly correct, thin explanation | Vague or conflates the two mechanisms | Not attempted |

**Total:** /12 — Pass threshold: 8/12
