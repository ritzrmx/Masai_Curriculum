# Lecture Script: Getting Started with LangChain
> **Instructor Reference** — Module 3: GenAI & Agents | Session 6 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students set up LangChain with OpenRouter as the LLM backend, understand WHY a framework like LangChain exists given everything they already built by hand in Session 2, and learn the three foundational LangChain building blocks: `PromptTemplate` / `ChatPromptTemplate` for reusable prompts, and chaining multiple LLM calls together (taught as the classic `LLMChain`/`SequentialChain` concept, expressed in the modern LangChain Expression Language pipe syntax that current LangChain versions actually ship).

**Student profile at this point:** Finished Session 5 (structured outputs with Pydantic) — comfortable with raw `requests.post()` calls to OpenRouter (Session 2), prompt engineering technique names (Session 4), and validating LLM output shapes with Pydantic (Session 5). Has never imported `langchain`.

**Key outcome:** Every student installs and configures `langchain-openai` pointed at OpenRouter instead of OpenAI directly, builds both a plain-text `PromptTemplate` and a role-structured `ChatPromptTemplate`, and chains two LLM calls together so the first call's output becomes the second call's input — without manually writing the "take output, stuff into next payload" glue code they had to hand-write in Session 2.

**Dataset for this session:** None required — all examples use small inline strings. All example LLM-GENERATED text is explicitly non-deterministic and marked **"Example output (illustrative — actual LLM output will vary run to run)"**; the LangChain object construction, prompt formatting, and chaining mechanics shown are stated as fact because they are deterministic, verified against the current LangChain API (`langchain-core` / `langchain-openai`, LCEL pipe syntax).

**A note on `LLMChain` and `SequentialChain` specifically:** Older LangChain tutorials (and this course's own curriculum notes) reference two classes by name: `LLMChain` (one prompt → one LLM call) and `SequentialChain` (multiple chained calls, passing outputs forward). As of the LangChain version this course targets, these classes are deprecated/removed in favor of the **pipe operator** (`|`), which composes a prompt, an LLM, and a parser into a `RunnableSequence` — mechanically the exact same idea, written more directly. This script teaches the concept under its classic names, then shows the current idiomatic code that actually implements it, so students are not confused when they see either style in the wild.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Why a Framework, Why Now? | 10 min | 0:10 |
| SEGMENT 2: Installing & Configuring LangChain for OpenRouter | 20 min | 0:30 |
| SEGMENT 3: Your First Chain — Prompt + LLM + Parser | 25 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: `PromptTemplate` vs. `ChatPromptTemplate` | 20 min | 1:25 |
| SEGMENT 5: Chaining Multiple Calls — the `LLMChain`/`SequentialChain` Idea | 20 min | 1:45 |
| SEGMENT 6: Lab — Build a Two-Step Chain | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Why a Framework, Why Now? (10 min)

### The Hook (5 min)

**Say:** *"Session 2, you built `ask_llm()` by hand — raw `requests.post()`, manually building the `messages` list, manually parsing `choices[0]['message']['content']`. Quick show of hands: who had to copy-paste that same 'build headers, build payload, post, parse response' block more than three times across your Session 2/4/5 labs?"* Most hands go up. **Say:** *"That repetition is exactly the gap LangChain closes. It is NOT new AI capability — OpenRouter and the underlying models do all the actual thinking. LangChain is a convenience and composition layer on top of exactly the HTTP calls you already know how to make by hand."*

**Ask:** *"If you already know how to do all of this manually, why learn a framework at all?"* Collect guesses. Guide toward: readability (named objects instead of raw dicts), reusable templates (so you're not hand-formatting an f-string every time), and — the big one for today — easy composition, so chaining "call 1's output feeds call 2's input" doesn't require you to hand-write the same glue code every single time.

### What LangChain Is, and Is Not (5 min)

**Say:** *"LangChain is a Python library for building applications on top of LLMs. It gives you: prompt templates (reusable, fillable prompt text), chains (composing a prompt, a model call, and output parsing into one reusable pipeline), and — later in this module — tools, agents, and retrieval components. It does NOT give you a new or different model; underneath, it still sends the exact same kind of HTTP request to a provider like OpenRouter that you built by hand in Session 2."*

**Write on board:**

```
Session 2 (by hand):   build headers -> build payload -> requests.post() -> parse JSON
Session 6 (LangChain): ChatOpenAI(...) | prompt | parser   <- same HTTP call, less glue code
```

**Learning contract for today — write on board:**

- Configure `ChatOpenAI` from `langchain-openai` to call OpenRouter instead of OpenAI directly
- Build and fill a `PromptTemplate` and a `ChatPromptTemplate`
- Compose a prompt, an LLM, and an output parser into one chain using the pipe operator
- Chain two LLM calls together so the first call's output flows into the second call's prompt

---

## SEGMENT 2: Installing & Configuring LangChain for OpenRouter (20 min)

### Installing the Right Packages (5 min)

**Say:** *"LangChain is split into several packages. For today you need three: `langchain-core` (the base abstractions — prompts, parsers, the pipe operator), `langchain-openai` (the integration that lets LangChain talk to any OpenAI-COMPATIBLE API — which is exactly what OpenRouter is), and optionally the umbrella `langchain` package for a few higher-level helpers."*

**Write on board:**

```bash
pip install langchain-core langchain-openai langchain
```

**Say:** *"Notice we are installing `langchain-openai`, not a separate 'langchain-openrouter' package — because OpenRouter deliberately mimics OpenAI's exact API shape, the OpenAI integration works against it directly. You just point it at a different URL. This is the exact same 'OpenAI-compatible' idea from Session 2, now handled for you by the library instead of by your own `requests` calls."*

### Pointing `ChatOpenAI` at OpenRouter Instead of OpenAI (8 min)

**Say:** *"`ChatOpenAI` is the LangChain class that wraps a chat-style LLM call. By default it assumes you're calling OpenAI's own servers with an OpenAI key. We redirect it to OpenRouter using two parameters: `base_url` and `api_key`."*

**Live-code:**

```python
import os
from langchain_openai import ChatOpenAI

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment.")

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
)

print("LLM object created:", llm.model_name)
```

**Example output (actual — object construction and attribute access are deterministic, verified against the current `langchain-openai` API):**
```
LLM object created: openai/gpt-4o-mini
```

**Say, pointing at each parameter:** *"`model` is the exact same `provider/model-name` slug from Session 2 — nothing changed there. `api_key` is your OpenRouter key, same key, same account, same billing as Session 2 — LangChain just calls the parameter `api_key` instead of building an `Authorization` header by hand for you. `base_url` is the critical piece: this single parameter is what redirects every request this `llm` object makes away from `api.openai.com` and toward OpenRouter's endpoint instead. Change that one string, and the entire rest of your LangChain code — prompts, chains, parsers — works completely unchanged against a totally different provider."*

### Making Your First Call Through LangChain (7 min)

**Live-code:**

```python
response = llm.invoke("Say hello in exactly five words.")
print(type(response))
print(response.content)
```

**Example output (illustrative — actual LLM output will vary run to run; `type(response)` is deterministic and verified):**
```
<class 'langchain_core.messages.ai.AIMessage'>
Hello there, nice to meet you!
```

**Say:** *"Compare this to Session 2. There, you called `requests.post()`, got back a raw JSON dict, and manually dug out `data['choices'][0]['message']['content']`. Here, `.invoke()` does that entire request/response cycle for you and hands back an `AIMessage` object — `.content` is the LangChain equivalent of that same JSON path you used to write by hand. Same HTTP call happening underneath, same OpenRouter account being billed — just less glue code on your end."*

**Ask:** *"If `llm.invoke()` throws an error — say, a bad API key — do you think LangChain still goes through OpenRouter's servers the same way your raw Session 2 code did, including the same 401 behavior?"* Guide toward: yes — LangChain doesn't change what OpenRouter does server-side at all; it only changes how you, the Python developer, construct the request and read the response. A bad key still produces the same 401 underneath; LangChain surfaces it as a Python exception instead of a raw status code your code has to check.

### Comprehension Check (2 min)

1. *"Which two parameters redirect `ChatOpenAI` from OpenAI's own servers to OpenRouter?"* (`base_url` and `api_key`.)
2. *"What LangChain object type does `.invoke()` return, and which attribute holds the actual generated text?"* (An `AIMessage`; the text is in `.content`.)

---

## SEGMENT 3: Your First Chain — Prompt + LLM + Parser (25 min)

### Why Not Just Call `.invoke()` with a Plain String Forever? (5 min)

**Say:** *"`llm.invoke('some string')` works fine for a one-off call, but real applications need: a REUSABLE prompt template with blanks to fill in per request, and often a step that takes the raw `AIMessage` and converts it into plain text or structured data automatically, rather than you writing `.content` everywhere by hand. That's exactly what a LangChain 'chain' bundles together."*

### Building a `PromptTemplate` (8 min)

**Say:** *"A `PromptTemplate` is a reusable prompt with named placeholders, using the same `{curly_brace}` syntax as an ordinary Python f-string — except the FILLING-IN happens later, not at the moment you define the template, which is exactly what makes it reusable across many different inputs."*

**Live-code:**

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Write a one-sentence summary of the following topic for a beginner: {topic}"
)

filled = template.format(topic="photosynthesis")
print(filled)
```

**Example output (actual — template filling is deterministic string substitution, verified):**
```
Write a one-sentence summary of the following topic for a beginner: photosynthesis
```

**Say:** *"`{topic}` is a placeholder, and `.format(topic=...)` fills it in — this part is pure, deterministic string substitution, no LLM involved yet, and you can verify it with your own eyes exactly like an f-string. The power shows up once we hand this TEMPLATE, unfilled, to a chain — the chain fills it in AND calls the LLM in one step, for whatever `topic` you give it at call time."*

### Composing a Chain with the Pipe Operator (8 min)

**Say:** *"This is the single most important syntax in modern LangChain: the pipe operator, `|`. It chains a prompt, a model, and a parser together into one callable pipeline — read it left to right as 'the output of this step becomes the input of the next step,' exactly like a Unix shell pipe."*

**Live-code:**

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = template | llm | parser

result = chain.invoke({"topic": "photosynthesis"})
print(type(result))
print(result)
```

**Example output (illustrative text, but the TYPE and pipeline structure are deterministic and verified; actual LLM wording will vary run to run):**
```
<class 'str'>
Photosynthesis is the process plants use to turn sunlight, water, and carbon dioxide into the energy they need to grow.
```

**Say, tracing the pipe step by step:** *"`template` takes the dict `{'topic': 'photosynthesis'}` and produces a filled prompt string. That filled prompt flows into `llm`, which sends the actual HTTP request to OpenRouter and gets back an `AIMessage`. That `AIMessage` flows into `parser` — `StrOutputParser` does exactly one thing: pulls `.content` out for you, so your final `result` is a plain Python string instead of an `AIMessage` object. Three steps, one `.invoke()` call, zero manual JSON digging on your part."*

**Say:** *"This three-piece pipeline — prompt, LLM, parser — composed with `|` is literally what current LangChain means by 'a chain.' It replaces the older `LLMChain` class you may see referenced in older tutorials or in this course's own curriculum notes; `LLMChain` did the exact same prompt-then-LLM composition, just as an explicit class instead of the pipe operator. If you ever see `LLMChain(llm=llm, prompt=template)` in an older codebase, mentally translate it to `template | llm | StrOutputParser()` — same behavior, current syntax."*

### Comprehension Check (4 min)

1. *"In `chain = template | llm | parser`, what flows out of `template` and into `llm`?"* (A filled prompt string, produced by substituting the input dict's values into the template's placeholders.)
2. *"What specifically does `StrOutputParser` do to the `AIMessage` that `llm` produces?"* (Extracts `.content`, converting the `AIMessage` object into a plain Python string.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict: if a prompt template has TWO placeholders instead of one, does `chain.invoke(...)` still take a single dict argument, or does it need two separate arguments? Come back ready to test that guess.

---

## SEGMENT 4: `PromptTemplate` vs. `ChatPromptTemplate` (20 min)

### Why Chat Models Need a Different Template Type (6 min)

**Say:** *"`PromptTemplate` produces one plain string — perfect for a single `user`-role message. But remember from Session 2: real conversations use THREE roles — `system`, `user`, `assistant`. `ChatPromptTemplate` is built specifically to template a LIST of role-tagged messages, not just one string, mirroring exactly the `messages` list structure you built by hand in Session 2."*

### Building a `ChatPromptTemplate` (10 min)

**Live-code:**

```python
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant. Always answer in one short sentence."),
    ("user", "{question}"),
])

filled_messages = chat_template.format_messages(question="What causes seasons on Earth?")
for m in filled_messages:
    print(m.type, "-", m.content)
```

**Example output (actual — message construction and role-tagging are deterministic, verified):**
```
system - You are a concise assistant. Always answer in one short sentence.
human - What causes seasons on Earth?
```

**Say:** *"Notice `format_messages` (plural) returns a LIST of message objects, one per role — this is the direct LangChain equivalent of the `messages` list you built by hand in Session 2's `payload['messages']`. Also notice the role name in the tuple was `'user'`, but LangChain's internal type name for it is `'human'` — same role, LangChain's own vocabulary; don't let that naming difference confuse you."*

**Live-code, now chaining it exactly like SEGMENT 3:**

```python
chat_chain = chat_template | llm | parser
answer = chat_chain.invoke({"question": "What causes seasons on Earth?"})
print(answer)
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Seasons are caused by the tilt of Earth's axis as it orbits the Sun.
```

**Say:** *"Identical pipe pattern as SEGMENT 3 — `chat_template | llm | parser` — the ONLY thing that changed is we're now templating a full role-structured conversation instead of one plain string. This is the general LangChain pattern: however you build your prompt object, the rest of the chain composition looks the same."*

### Multiple Placeholders in One Template (4 min)

**Live-code, answering the break-time prediction question:**

```python
multi_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {persona}."),
    ("user", "Explain {topic} in one sentence."),
])

multi_chain = multi_template | llm | parser
result = multi_chain.invoke({"persona": "patient elementary school teacher", "topic": "gravity"})
print(result)
```

**Example output (illustrative — actual LLM output will vary run to run; the dict-with-two-keys calling convention is deterministic and verified):**
```
Gravity is the invisible force that pulls things down toward the ground, like when you drop a ball and it falls.
```

**Say, resolving the break prediction:** *"Two placeholders, `{persona}` and `{topic}` — and `.invoke()` still takes exactly ONE argument: a single dict with BOTH keys. This generalizes to any number of placeholders — one dict, one key per placeholder, always a single `.invoke()` argument, never multiple positional arguments."*

### Comprehension Check (2 min)

1. *"Why does `ChatPromptTemplate` exist when `PromptTemplate` already works for sending text to an LLM?"* (Chat models use role-structured `system`/`user`/`assistant` messages, not one plain string; `ChatPromptTemplate` templates that whole role-tagged list, matching Session 2's `messages` structure.)
2. *"If a template has three placeholders, how many arguments does `.invoke()` take?"* (Still exactly one — a single dict containing all three keys.)

---

## SEGMENT 5: Chaining Multiple Calls — the `LLMChain`/`SequentialChain` Idea (20 min)

### The Problem: One LLM Call's Output Feeding Another's Input (5 min)

**Say:** *"Here's a genuinely common real pattern: call an LLM to generate something, then call the LLM AGAIN, using the first call's output as part of the second call's prompt. In Session 2, if you wanted this, you'd manually store the first reply in a variable and manually insert it into your next f-string payload. Today we do the same thing, but the chain handles passing that value forward for you."*

**Say:** *"This exact pattern is what older LangChain tutorials call `SequentialChain` — a chain of chains, where each step's output becomes the next step's input. Current LangChain expresses the same idea by composing multiple `RunnableSequence` pipelines, where one chain's STRING output is fed into the next chain's input dict."*

### Building a Two-Step Sequential Chain (10 min)

**Say:** *"Let's build a concrete example: step one generates a short story premise from a genre; step two writes an opening line FOR that premise. The premise `.invoke()` produces becomes part of the input to the second chain."*

**Live-code:**

```python
premise_template = ChatPromptTemplate.from_messages([
    ("system", "You are a creative writing assistant."),
    ("user", "In one sentence, invent a story premise in the {genre} genre."),
])
premise_chain = premise_template | llm | parser

opening_line_template = ChatPromptTemplate.from_messages([
    ("system", "You are a creative writing assistant."),
    ("user", "Given this story premise: \"{premise}\", write one compelling opening line for the story."),
])
opening_line_chain = opening_line_template | llm | parser

# Step 1
premise = premise_chain.invoke({"genre": "science fiction"})
print("Premise:", premise)

# Step 2 -- step 1's output becomes part of step 2's input dict
opening_line = opening_line_chain.invoke({"premise": premise})
print("Opening line:", opening_line)
```

**Example output (illustrative — actual LLM output will vary run to run; the two-step data-passing structure itself is deterministic and verified):**
```
Premise: In a future where memories can be traded as currency, a woman discovers someone has been secretly buying up her childhood.
Opening line: The first memory she sold was her tenth birthday, and she never noticed it was gone until the cake started tasting like someone else's.
```

**Say, pointing at the hand-off:** *"This is the entire 'sequential chain' idea in one line: `opening_line_chain.invoke({'premise': premise})` — the variable `premise`, which came OUT of the first chain, goes straight INTO the second chain's input dict. No manual string formatting, no manual re-building of a `messages` list like Session 2 required — the chain's own template handles slotting it in."*

### Composing Steps into a Single Runnable, One Level Deeper (5 min)

**Say:** *"For completeness: you CAN compose this into a single object instead of two separate `.invoke()` calls, using a small Python function wrapped as a `RunnableLambda`, or more simply, just calling the two chains back to back inside your own function — which is often the clearest, most debuggable choice in practice."*

**Live-code:**

```python
def story_pipeline(genre):
    premise = premise_chain.invoke({"genre": genre})
    opening_line = opening_line_chain.invoke({"premise": premise})
    return {"genre": genre, "premise": premise, "opening_line": opening_line}

result = story_pipeline("mystery")
print(result)
```

**Say:** *"Notice this is just a plain Python function calling two chains in order — there's no special magic required to replicate `SequentialChain`'s behavior. This is often the preferred modern style: plain functions composing chains are usually easier to debug, log, and step through than a deeply nested single-object pipeline, especially while you're learning. You'll meet more advanced multi-step composition (passing MULTIPLE intermediate values forward, conditional branching) in Session 7."*

### Comprehension Check (3 min)

1. *"What classic LangChain class name describes 'chain multiple LLM calls, passing one's output into the next's input'?"* (`SequentialChain` — now typically expressed as plain Python functions calling multiple pipe-composed chains in sequence, or composed `Runnable` objects.)
2. *"In the two-step story example, which variable physically carries data from the first chain to the second?"* (`premise` — the string returned by `premise_chain.invoke(...)`, passed into `opening_line_chain.invoke({"premise": premise})`.)

---

## SEGMENT 6: Lab — Build a Two-Step Chain (10 min)

### Instructions (read aloud, step by step)

1. Configure a `ChatOpenAI` instance pointed at OpenRouter (reuse the `llm` object pattern from SEGMENT 2).
2. Build a `ChatPromptTemplate` for a chain that takes a `{dish}` and returns one key ingredient needed to cook it.
3. Build a second `ChatPromptTemplate` for a chain that takes an `{ingredient}` and returns one fun fact about it.
4. Chain both templates to `llm | StrOutputParser()` separately.
5. Write a `dish_fact_pipeline(dish)` function that calls the first chain, then feeds its output into the second chain, and returns both results.

### Starter Code

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model=___,
    api_key=___,
    base_url=___,
    temperature=0.7,
)
parser = StrOutputParser()

ingredient_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful cooking assistant."),
    ("user", "Name exactly one key ingredient needed to cook {dish}. Reply with only the ingredient name."),
])
ingredient_chain = ___ | ___ | ___

fact_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful cooking assistant."),
    ("user", "Give one short, fun fact about {ingredient}."),
])
fact_chain = ___ | ___ | ___

def dish_fact_pipeline(dish):
    ingredient = ___.invoke({"dish": ___})
    fact = ___.invoke({"ingredient": ___})
    return {"dish": dish, "ingredient": ingredient, "fact": fact}

print(dish_fact_pipeline("margherita pizza"))
```

### Reference Solution

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
)
parser = StrOutputParser()

ingredient_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful cooking assistant."),
    ("user", "Name exactly one key ingredient needed to cook {dish}. Reply with only the ingredient name."),
])
ingredient_chain = ingredient_template | llm | parser

fact_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful cooking assistant."),
    ("user", "Give one short, fun fact about {ingredient}."),
])
fact_chain = fact_template | llm | parser

def dish_fact_pipeline(dish):
    ingredient = ingredient_chain.invoke({"dish": dish})
    fact = fact_chain.invoke({"ingredient": ingredient})
    return {"dish": dish, "ingredient": ingredient, "fact": fact}

print(dish_fact_pipeline("margherita pizza"))
```

**Example output (illustrative — actual LLM output will vary run to run; the dict-passing structure between chains is deterministic and verified):**
```
{'dish': 'margherita pizza', 'ingredient': 'Mozzarella cheese', 'fact': 'Fresh mozzarella is traditionally made from the milk of water buffalo in parts of Italy, giving it a distinctively soft, creamy texture.'}
```

**Instructor circulates**, checking specifically that students correctly pass the FIRST chain's return value into the SECOND chain's input dict (a common bug: forgetting to use the returned `ingredient` variable and instead hardcoding a dish name or ingredient string), and that `base_url`/`api_key` are wired correctly to OpenRouter rather than left as OpenAI defaults.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Why LangChain exists: a composition and convenience layer over the exact same HTTP calls built by hand in Session 2
- Configuring `ChatOpenAI` to call OpenRouter via `base_url` and `api_key`
- Building `PromptTemplate` (plain string) and `ChatPromptTemplate` (role-structured messages)
- Composing a chain with the pipe operator: `prompt | llm | parser`
- Chaining multiple LLM calls together (the classic `LLMChain`/`SequentialChain` idea), passing one call's output into the next call's input

**Bridge to next session:** *"Today you learned the mechanical building blocks — templates and chains. Next session, we put them to real use: building an extraction workflow, a summarization pipeline, a simple FAQ bot, and a CSV copilot, all using exactly the prompt-template-and-chain patterns from today, composed into multi-step pipelines that pass STRUCTURED outputs between steps, not just plain strings."*

**Homework / self-practice:**
1. Build a three-placeholder `ChatPromptTemplate` (e.g. `{persona}`, `{topic}`, `{tone}`) and test it with at least two different combinations of values.
2. Extend today's two-step dish/ingredient/fact lab into a THREE-step chain: dish → ingredient → fact → one rhyming couplet about the fact.
3. Read the LangChain documentation's page on `Runnable` and write two sentences, in your own words, explaining what the pipe operator `|` actually does to the objects on either side of it.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Do I need an OpenAI API key to use `ChatOpenAI`, even though we're routing through OpenRouter?**
→ No. `ChatOpenAI`'s name refers to the API FORMAT it speaks (OpenAI-compatible), not which company's servers it calls. With `base_url` pointed at OpenRouter and `api_key` set to your OpenRouter key, no OpenAI account or key is involved at all.

**Q: Is `LLMChain` completely gone, or will I still see it in real code?**
→ You'll likely still encounter it in older tutorials, Stack Overflow answers, and some existing production codebases, since it was the standard pattern for years. It still functions in some installed versions, but is deprecated in favor of pipe-composed chains; new code should use the `|` syntax taught today.

**Q: What's the actual difference between `.invoke()` and just calling the LLM directly with a string?**
→ `.invoke()` is the standard method name across ALL `Runnable` objects in LangChain — prompts, LLMs, parsers, and full chains all expose it. Calling `llm.invoke("some string")` directly skips the prompt-templating step entirely; calling `chain.invoke({...})` runs the full prompt → LLM → parser pipeline. Same underlying method name, different amount of the pipeline it triggers.

**Q: Can a chain have more than one LLM in it, e.g. a cheap model for one step and an expensive model for another?**
→ Yes — this is a common and often cost-effective real pattern. Each step in a sequential pipeline can use its own separately configured `ChatOpenAI` instance pointed at a different model slug, exactly like swapping the `model` string in Session 2's raw JSON payload.

**Q: Does LangChain add noticeable latency compared to the raw `requests` calls from Session 2?**
→ The extra Python-side overhead (template filling, object construction) is negligible compared to network round-trip time to the LLM provider itself, which dominates total latency either way. LangChain is not meaningfully slower for this reason, though it does add some import/startup overhead the first time you run it in a session.

---

## Instructor Notes

- **Prerequisite check:** Confirm every student still has a working `OPENROUTER_API_KEY` set from Session 2 before SEGMENT 2 — this is a hard blocker for every live-coding demo today.
- **Common mistake:** Leaving `base_url` out entirely, which silently sends requests to OpenAI's own servers using an OpenRouter key — this produces a confusing 401, not an obviously wrong-URL error, so it looks like a key problem at first glance.
- **Another common mistake:** Passing a `PromptTemplate` (plain-string) object into a chat-oriented workflow, or vice versa — walk past screens during SEGMENT 4 to confirm students used `ChatPromptTemplate.from_messages` with role tuples, not `PromptTemplate.from_template` with a single string, once roles are needed.
- **Another common mistake:** In SEGMENT 5/6, forgetting that the SECOND chain's input dict key must match its OWN template's placeholder name (e.g. `{"ingredient": ingredient}`, not `{"premise": ingredient}`) — a `KeyError`-style failure that's an easy copy-paste mistake between the two template blocks.
- **Engagement tip:** SEGMENT 3's side-by-side comparison of Session 2's raw JSON-digging code versus today's three-line chain usually produces a visible "oh, that's it?" reaction — lean into that moment rather than rushing past it.
- **Time check:** If running behind before the break, compress SEGMENT 3's chain-tracing explanation to a single pass instead of narrating each pipe stage separately.
- **If running long after the break:** Skip SEGMENT 5's "composing into a single Runnable" subsection (the `story_pipeline` function is sufficient on its own) and go straight to the lab.
- **Materials to prepare:** Confirm `pip install langchain-core langchain-openai langchain` succeeds on the classroom network/image before class; scratch notebook with SEGMENT 2/3's live-coding demos pre-typed.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Forgetting `base_url` when constructing `ChatOpenAI` | Requests silently go to OpenAI's servers instead of OpenRouter; confusing 401 with a valid-looking OpenRouter key | Always pass `base_url="https://openrouter.ai/api/v1"` alongside `api_key` |
| Using `PromptTemplate` where a system/user role split is needed | No way to set a system message; prompt reads as one flat block of text | Use `ChatPromptTemplate.from_messages([("system", ...), ("user", ...)])` for role-structured prompts |
| Calling `.invoke()` with a plain string on a template that expects a dict | `TypeError` or missing-key error from the template | Always pass a dict matching the template's placeholder names, e.g. `{"topic": "gravity"}` |
| Mismatched placeholder names between template and `.invoke()` dict | `KeyError` at template-fill time | Double-check the dict key exactly matches the `{placeholder}` name used in `from_template`/`from_messages` |
| Feeding the wrong variable into the second chain in a two-step pipeline | Second call ignores the first call's actual output; uses a hardcoded or stale value instead | Explicitly trace which variable the first chain returned and pass THAT variable into the second chain's input dict |
| Assuming `LLMChain`/`SequentialChain` are required, current syntax | Import errors on newer LangChain installs (`ImportError: cannot import name 'LLMChain'`) | Use the pipe operator (`prompt | llm | parser`) and plain Python functions for sequential composition instead |

---

## Appendix: Mapping Classic Class Names to Current Syntax (Instructor Reference)

| Classic name (older tutorials) | What it did | Current idiomatic equivalent |
|---|---|---|
| `LLMChain(llm=llm, prompt=template)` | One prompt template + one LLM call | `template | llm | StrOutputParser()` |
| `SequentialChain(chains=[chain1, chain2], ...)` | Multiple chains, passing outputs forward | Plain Python function calling each `Runnable` chain in order, passing each result into the next chain's input dict |
| `chain.run(...)` | Execute the chain and get a string back | `chain.invoke(...)` (returns whatever the final step produces — a string if the chain ends in `StrOutputParser()`) |
| `chain.predict(...)` | Alias for `.run()` on some chain types | `chain.invoke(...)` |

*(This mapping is provided so students recognize older code they'll encounter online; all LIVE-CODED examples in this session use current syntax only.)*

---

## Appendix: Full `ChatOpenAI` Parameter Reference for OpenRouter (Instructor Reference)

| Parameter | Purpose | Typical value for this course |
|---|---|---|
| `model` | `provider/model-name` slug, identical to Session 2's `payload["model"]` | `"openai/gpt-4o-mini"` |
| `api_key` | Your OpenRouter API key | Loaded from `OPENROUTER_API_KEY` environment variable |
| `base_url` | Redirects requests away from OpenAI's own servers | `"https://openrouter.ai/api/v1"` |
| `temperature` | Same randomness control from Session 1/2 | `0.0`-`1.0` depending on the task |
| `max_tokens` | Same hard output-length cap from Session 2 | Set explicitly for cost-sensitive or latency-sensitive use cases |

---

## FAQ — Additional Questions

**Q: Can I use a local open-source model instead of OpenRouter with the exact same `ChatOpenAI` class?**
→ Many local model servers (for example, ones exposing an OpenAI-compatible local endpoint) can be used the same way, by pointing `base_url` at your local server's address instead of OpenRouter's. The `ChatOpenAI` class only cares that the endpoint SPEAKS the OpenAI-compatible request/response shape — it doesn't care who's actually hosting it.

**Q: Does LangChain hide the `temperature`/`top_p` concepts from Session 1, or do they still apply?**
→ They still apply exactly as before — `ChatOpenAI`'s `temperature` parameter maps directly onto the same field in the underlying JSON payload Session 2 built by hand. LangChain is a thinner layer than it might feel like at first; almost every concept from Sessions 1-2 maps onto a LangChain parameter with the same name or a very close equivalent.

**Q: If two chains share the same `llm` object, do they share conversation history with each other?**
→ No — `ChatOpenAI`, prompts, and chains as used today are stateless between `.invoke()` calls, exactly like the raw API in Session 2. Sharing one `llm` object across multiple chains only saves you from re-configuring the connection; it does not carry conversation memory. Memory/history management is a more advanced LangChain topic beyond today's scope.

---

## Materials Checklist

- [ ] Every student has `OPENROUTER_API_KEY` set from Session 2, verified working
- [ ] `pip install langchain-core langchain-openai langchain` succeeds on the classroom machine image
- [ ] Scratch notebook with SEGMENT 2/3's live-coding demos pre-typed
- [ ] Session 2's raw `requests`-based `ask_llm()` code available to reference for side-by-side comparison
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Compress SEGMENT 3's pipe-tracing explanation into a single pass instead of narrating each stage separately |
| Running long after break | Skip SEGMENT 5's "composing into a single Runnable" subsection; the `story_pipeline` function is sufficient on its own |
| Low energy after lunch/break | Run SEGMENT 4's multi-placeholder demo as an interactive "guess what keys the dict needs" activity before revealing |
| Advanced group finishes lab early | Have them extend `dish_fact_pipeline` into a three-step chain (dish → ingredient → fact → rhyming couplet) |
| No shared screen / projector issue | Walk through the chain composition on the whiteboard, tracing each `|` stage using this script's exact worked examples |
| OpenRouter outage / no internet | Walk through template-filling and chain STRUCTURE (which is fully deterministic and doesn't require a live call) using printed `.format()`/`.format_messages()` output only |

---

## End-of-Session Quiz (5 Questions)

1. What two `ChatOpenAI` parameters redirect requests from OpenAI's own servers to OpenRouter?
2. What is the key structural difference between `PromptTemplate` and `ChatPromptTemplate`?
3. In `chain = template | llm | parser`, what does `StrOutputParser` specifically extract from the LLM's output?
4. What classic LangChain class name is now typically expressed as plain Python functions calling pipe-composed chains in sequence?
5. If a template has two placeholders, `{a}` and `{b}`, how many arguments does `chain.invoke(...)` take, and what type is it?

**Answer key (instructor):**
1. `base_url` and `api_key`.
2. `PromptTemplate` produces a single plain string; `ChatPromptTemplate` produces a list of role-tagged messages (`system`/`user`/etc.).
3. The `.content` attribute of the `AIMessage`, converting it into a plain Python string.
4. `SequentialChain`.
5. One argument — a single dict containing both keys, e.g. `{"a": ..., "b": ...}`.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Three-placeholder `ChatPromptTemplate` + two test runs | Correct template, both runs demonstrate different values producing different prompts | Correct template, thin variation between runs | Template has fewer than three working placeholders | Not attempted |
| Three-step chain extension (dish → ingredient → fact → couplet) | All three hand-offs correct, final output clearly builds on prior steps | Chain works, minor hand-off issue | Chain partially works but skips or hardcodes a step | Not attempted |
| `Runnable`/pipe operator explanation | Clear, accurate, in the student's own words | Accurate but close to copied documentation wording | Vague or partially incorrect | Not attempted |

**Total:** /12 — Pass threshold: 8/12
