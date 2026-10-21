# Lecture Script: Building AI Workflows in LangChain
> **Instructor Reference** — Module 3: GenAI & Agents | Session 7 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students move from "a single prompt and a single chain" (Session 6) to real multi-step AI WORKFLOWS: extraction and summarization pipelines using structured output parsers, a simple FAQ bot, and a "CSV copilot" pattern that answers natural-language questions about tabular data — all built from the same prompt/chain primitives learned last session, composed into pipelines that pass STRUCTURED data (not just plain strings) between steps.

**Student profile at this point:** Just finished Session 6 — comfortable with `ChatOpenAI` pointed at OpenRouter, `PromptTemplate`/`ChatPromptTemplate`, the pipe operator (`|`), and chaining two calls together by passing one chain's string output into the next chain's input dict. Also remembers Session 5's Pydantic models for validating LLM output shape.

**Key outcome:** Every student builds an extraction chain that pulls structured fields out of free text using a Pydantic-backed output parser, a summarization chain, a minimal FAQ-answering chain grounded in a small fixed knowledge snippet, and a CSV copilot chain that converts a natural-language question about a small dataset into a pandas operation and a plain-English answer.

**Dataset for this session:** A small CSV of synthetic order records, `orders.csv`, used for the CSV-copilot workflow (SEGMENT 5 and the lab). All other examples use small inline strings.

**A note on non-determinism:** All example LLM-GENERATED text (summaries, extracted field VALUES when the input is ambiguous, FAQ answers, natural-language explanations) is explicitly non-deterministic and marked **"Example output (illustrative — actual LLM output will vary run to run)"**. The chain/parser MECHANICS — what gets passed between steps, how a Pydantic schema structures a parser's expected output, and the pandas operations in the CSV copilot — are deterministic and stated as fact, verified against the current LangChain and Pydantic APIs.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — From Single Chains to Workflows | 8 min | 0:08 |
| SEGMENT 2: Structured Extraction with Pydantic Output Parsers | 25 min | 0:33 |
| SEGMENT 3: A Summarization Pipeline with Length Control | 17 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 4: Building a Simple FAQ Bot | 20 min | 1:20 |
| SEGMENT 5: A CSV Copilot — Natural Language Over Tabular Data | 25 min | 1:45 |
| SEGMENT 6: Lab — Combine Extraction and Summarization into One Pipeline | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — From Single Chains to Workflows (8 min)

### The Hook (4 min)

**Say:** *"Last session, every chain we built did exactly one thing: fill a prompt, call the LLM, get text back. Today we build WORKFLOWS — pipelines with a PURPOSE, where the output of one step isn't just text to print, it's structured data the NEXT step actually consumes programmatically. This is the difference between 'a chatbot' and 'an application that happens to use an LLM internally.'"*

**Ask:** *"If you wanted a program that reads a messy customer email and pulls out just the order number, the complaint category, and whether a refund was requested — as clean Python values you could store in a database — how would Session 2's raw `requests` approach have handled getting the LLM's answer back as a PYTHON DICT instead of a paragraph of prose?"* Guide toward: you'd have to ask the model to "please reply in JSON," then manually `json.loads()` its reply and hope it actually followed instructions — fragile, and exactly the gap Session 5's Pydantic validation addressed. Today, LangChain's structured output parsers combine that Session 5 idea directly into the chain itself.

### Learning Contract for Today (4 min)

**Write on board:**

- Build an extraction chain that returns validated, structured fields from free text (not just a string)
- Build a summarization chain with a controllable target length
- Build a minimal FAQ bot grounded in a fixed knowledge snippet
- Build a CSV copilot that answers natural-language questions about a small dataset
- Chain these primitives into a single multi-step pipeline passing structured data forward

---

## SEGMENT 2: Structured Extraction with Pydantic Output Parsers (25 min)

### Why Plain `StrOutputParser` Isn't Enough Here (5 min)

**Say:** *"Session 6's `StrOutputParser` gives you a string. Great for a story opening line; useless if you need `order_id`, `category`, and `wants_refund` as separate, typed Python values your database can actually store. We need the LLM's reply to come back as STRUCTURED data, validated the same way Session 5 validated it with Pydantic — and LangChain has a parser built exactly for this."*

### Defining the Schema with Pydantic (8 min)

**Say:** *"Step one is identical in spirit to Session 5: define a Pydantic model describing exactly the fields you want extracted."*

**Live-code:**

```python
from pydantic import BaseModel, Field
from typing import Optional

class SupportTicket(BaseModel):
    order_id: Optional[str] = Field(description="The order number mentioned, if any, otherwise null")
    category: str = Field(description="One of: shipping, refund, product_defect, billing, other")
    wants_refund: bool = Field(description="True if the customer explicitly asks for a refund")

print(SupportTicket.model_fields.keys())
```

**Example output (actual — Pydantic model introspection is deterministic, verified):**
```
dict_keys(['order_id', 'category', 'wants_refund'])
```

**Say:** *"Nothing new here versus Session 5 — a Pydantic model with typed fields and a `description` on each `Field()`. The description text matters more here than it did in Session 5, though: in a moment, it gets automatically turned into part of the PROMPT the LLM sees, telling it exactly what each field means."*

### Wiring the Schema into a Chain with `PydanticOutputParser` (8 min)

**Live-code:**

```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

parser = PydanticOutputParser(pydantic_object=SupportTicket)

extraction_template = ChatPromptTemplate.from_messages([
    ("system", "You extract structured support ticket data from customer messages. {format_instructions}"),
    ("user", "{message}"),
]).partial(format_instructions=parser.get_format_instructions())

extraction_chain = extraction_template | llm | parser

ticket = extraction_chain.invoke({
    "message": "Hi, my order #A1092 arrived broken. I want my money back, please."
})
print(type(ticket))
print(ticket)
```

**Example output (illustrative field VALUES — actual LLM extraction will vary run to run depending on model and phrasing; the TYPE and field STRUCTURE are deterministic and verified against the Pydantic schema above):**
```
<class '__main__.SupportTicket'>
order_id='A1092' category='product_defect' wants_refund=True
```

**Say, explaining each new piece:** *"`parser.get_format_instructions()` auto-generates a block of text telling the LLM exactly what JSON shape to produce, straight from your Pydantic field descriptions — you didn't have to hand-write 'please reply in JSON with these exact keys' yourself. `.partial(format_instructions=...)` bakes that instruction text into the template PERMANENTLY, so every future `.invoke()` call doesn't need to pass it again — only `{message}` is left as a per-call placeholder. And `PydanticOutputParser` does double duty: it parses the LLM's raw JSON-ish text reply into a Python dict, AND validates it against `SupportTicket`, exactly like Session 5's manual `model_validate()` step — except it now happens automatically as part of the chain, raising a validation error if the LLM's output doesn't match the schema."*

**Ask:** *"What happens, concretely, if the LLM's raw reply ISN'T valid JSON matching this schema — say it adds a friendly sentence before the JSON block?"* Guide toward: `PydanticOutputParser` will raise a parsing/validation error, exactly like Session 5's `ValidationError` — this is a REAL failure mode with structured extraction, not a hypothetical; production systems often add a retry-with-correction step for this reason (mention `OutputFixingParser` as an advanced option, out of scope for today).

### A Second Worked Example, Testing an Ambiguous Message (4 min)

**Live-code:**

```python
ticket2 = extraction_chain.invoke({
    "message": "I'm just checking when my package will arrive, no order number handy."
})
print(ticket2)
```

**Example output (illustrative — actual LLM output will vary run to run; `order_id` being `None` for a message with no order number is the expected, correctly-modeled behavior):**
```
order_id=None category='shipping' wants_refund=False
```

**Say:** *"This is exactly why we made `order_id` `Optional` in the schema — a real customer message won't always contain every field. Good schema design anticipates which fields are genuinely optional versus always required, same lesson as Session 5."*

### Comprehension Check (3 min)

1. *"What does `parser.get_format_instructions()` actually produce, and where does that text go?"* (Auto-generated instruction text describing the required JSON shape, based on the Pydantic schema; it gets baked into the prompt via `.partial()`.)
2. *"What happens if the LLM's reply doesn't match the Pydantic schema?"* (`PydanticOutputParser` raises a validation error, the same category of failure as Session 5's manual Pydantic validation.)

---

## SEGMENT 3: A Summarization Pipeline with Length Control (17 min)

### Building a Controllable Summarizer (8 min)

**Say:** *"Summarization is one of the most common real LLM workflows, and the key design decision is giving the CALLER control over output length and style, rather than hardcoding it into the prompt."*

**Live-code:**

```python
from langchain_core.output_parsers import StrOutputParser

summary_template = ChatPromptTemplate.from_messages([
    ("system", "You are a precise summarization assistant. Summarize the user's text in at most {max_sentences} sentences. Do not add information not present in the original text."),
    ("user", "{text}"),
])

summary_chain = summary_template | llm | StrOutputParser()

long_text = (
    "The CloudNote remote work policy allows full-time employees to request remote "
    "work after a 90-day probationary period. Requests go through the HR portal and "
    "require manager approval within five business days, followed by an HR compliance "
    "check. Approved employees receive a one-time home office stipend and monthly "
    "internet reimbursement, but must return company equipment within ten days of "
    "employment ending."
)

summary = summary_chain.invoke({"text": long_text, "max_sentences": 1})
print(summary)
```

**Example output (illustrative — actual LLM output will vary run to run; the input text and `max_sentences` parameterization are deterministic and verified):**
```
Full-time CloudNote employees can request remote work after 90 days by getting manager and HR approval, which comes with equipment stipends but requires returning company gear when employment ends.
```

**Say:** *"`{max_sentences}` is a placeholder just like any other — nothing new mechanically, but notice the DESIGN choice: we didn't hardcode '1 sentence' into the system prompt text. We parameterized it, so the exact same chain object can produce a 1-sentence summary or a 5-sentence summary just by changing the `.invoke()` dict, without rewriting the template."*

**Say, pointing at the explicit instruction:** *"'Do not add information not present in the original text' is doing real work here — without it, models sometimes 'helpfully' embellish a summary with plausible-sounding but unverified details, a failure mode called hallucination that you'll hear about often in this field. An explicit grounding instruction like this meaningfully reduces — though does not perfectly eliminate — that risk."*

### Testing Different Lengths with the Same Chain (5 min)

**Live-code:**

```python
for n in [1, 3]:
    result = summary_chain.invoke({"text": long_text, "max_sentences": n})
    print(f"--- max_sentences={n} ---")
    print(result)
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
--- max_sentences=1 ---
CloudNote lets full-time employees request remote work after 90 days with manager and HR approval, offering a stipend and internet reimbursement but requiring equipment return at employment's end.
--- max_sentences=3 ---
Full-time CloudNote employees become eligible for remote work after a 90-day probationary period. Requests must go through the HR portal, needing manager approval within five business days and a subsequent HR compliance check. Approved employees get a one-time home office stipend and monthly internet reimbursement, and must return company equipment within ten days if employment ends.
```

**Say:** *"Same chain object, same template, two completely different-length outputs, purely from changing one dict value at call time. This reusability — one chain, many parameterized calls — is the whole point of templating instead of hand-writing a fresh f-string prompt every time, going all the way back to Session 6's opening motivation."*

### Comprehension Check (4 min)

1. *"Why parameterize `max_sentences` instead of hardcoding a specific number into the system prompt?"* (So the same chain object can be reused for different desired lengths, just by changing the `.invoke()` input, without rewriting the template.)
2. *"What's the purpose of the instruction 'do not add information not present in the original text'?"* (Reduces (does not fully eliminate) the risk of the model hallucinating plausible-sounding but unverified details into the summary.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict: for a FAQ bot that should only answer from a FIXED set of known facts (not the model's general knowledge), where in the chain should those facts be inserted — the system message, the user message, or neither? Come back ready to see the grounded-FAQ pattern.

---

## SEGMENT 4: Building a Simple FAQ Bot (20 min)

### The Core Idea: Grounding the Model in Known Facts (6 min)

**Say:** *"A FAQ bot's whole value proposition is answering ONLY from a known, trusted set of facts — not the model's general training knowledge, which could be outdated, wrong, or simply not about your specific product. The simplest possible version of this pattern: paste the known facts directly into the system message, and instruct the model to answer ONLY using them."*

**Say, resolving the break prediction:** *"The known facts go in the SYSTEM message, not the user message — the system message is the right place for standing context that applies to every question, while the user message stays reserved for the actual, changing question being asked. This is a direct, simple preview of the 'retrieval-augmented' pattern you'll build properly with real document retrieval in Session 9 and Session 11 — today's version just uses a small, fixed, hand-written knowledge block instead of looking facts up dynamically."*

### Building the FAQ Chain (9 min)

**Live-code:**

```python
faq_knowledge = """
- CloudNote's Pro plan costs 499 rupees per month, billed monthly or annually.
- CloudNote supports exporting notes to PDF from the Settings > Export menu.
- CloudNote is available on Android, iOS, and the web; there is no native Windows or Mac desktop app yet.
- Password resets are done via the 'Forgot password' link on the login screen, which sends a reset email.
- Account deletion can be requested from Settings > Account > Delete Account, and takes up to 7 days to fully process.
"""

faq_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are a support FAQ assistant for the CloudNote app. "
     "Answer the user's question using ONLY the facts below. "
     "If the answer is not contained in these facts, say you don't know and suggest contacting human support.\n\n"
     "Known facts:\n{knowledge}"),
    ("user", "{question}"),
]).partial(knowledge=faq_knowledge)

faq_chain = faq_template | llm | StrOutputParser()

print(faq_chain.invoke({"question": "How much is the Pro plan?"}))
print("---")
print(faq_chain.invoke({"question": "Can I use CloudNote on a Windows desktop app?"}))
print("---")
print(faq_chain.invoke({"question": "Do you support exporting to Microsoft Word?"}))
```

**Example output (illustrative — actual LLM wording will vary run to run; the STRUCTURE — facts baked into the system message via `.partial()`, question as the only per-call placeholder — is deterministic and verified):**
```
The Pro plan costs 499 rupees per month, billed either monthly or annually.
---
No, CloudNote doesn't currently have a native Windows desktop app — it's available on Android, iOS, and the web.
---
I don't have that in my known facts — CloudNote's export options I know about are PDF only. I'd suggest contacting human support to confirm if Word export is available.
```

**Say, pointing at the third answer:** *"THIS is the most important behavior in the whole demo: the model correctly says 'I don't know' instead of guessing or making something up, because we explicitly instructed it to stick to the given facts and admit when something isn't covered. An ungrounded, uninstructed model might instead confidently invent a plausible-sounding but entirely false answer about Word export — this is exactly the hallucination risk from SEGMENT 3, and explicit grounding plus an explicit 'say you don't know' instruction is the core mitigation."*

### Why This Doesn't Scale Past a Small Knowledge Block (3 min)

**Say:** *"Notice `faq_knowledge` is five short bullet points, pasted directly into the prompt. This works great for a small FAQ. It breaks down fast once you have hundreds or thousands of facts or documents — you can't paste your entire company wiki into every system message; you'd blow through the context window from Session 1 and pay for re-sending it on every single call. The real fix is Session 8 and 9's embeddings and retrieval: instead of pasting EVERYTHING, you search for and paste only the few MOST RELEVANT facts per question. Today's hand-written block is the simplified, foundational version of that much more scalable idea."*

### Comprehension Check (2 min)

1. *"Why does the known-facts block go in the system message rather than the user message?"* (The system message holds standing context relevant to every question; the user message is reserved for the specific, changing question being asked.)
2. *"What's the single most important instruction added to make this FAQ bot trustworthy, and why?"* (Instructing it to say 'I don't know' rather than guess when the answer isn't in the given facts — this directly reduces hallucination risk.)

---

## SEGMENT 5: A CSV Copilot — Natural Language Over Tabular Data (25 min)

### The Pattern: Natural Language In, Structured Insight Out (5 min)

**Say:** *"A 'CSV copilot' answers natural-language questions about tabular data a user already has — 'which product sold the most last month?' — without the user writing any pandas code themselves. There are two honest ways to build this: (1) describe the data's shape to the LLM and ask it to generate the ANSWER directly from a text description of the data, or (2) have the LLM generate pandas CODE, which YOUR program then actually executes against the real DataFrame, returning a guaranteed-correct computed answer rather than the model's own arithmetic. We'll build approach (2), because it's the honest, reliable pattern used in real production tools — never trust an LLM's own mental arithmetic over a real dataset when you can have it write code and let Python do the computing."*

### Loading the Dataset (4 min)

**Live-code:**

```python
import pandas as pd

orders = pd.read_csv("orders.csv")
print(orders.shape)
print(orders.head())
```

**Example output (actual — reflects the real structure of this session's `orders.csv`, verified):**
```
(12, 4)
   order_id     product  quantity  price_each
0      1001     Notebook         3        50.0
1      1002         Pen        10         8.0
2      1003      Laptop         1      55000.0
3      1004     Notebook         2        50.0
4      1005  Headphones         4      1200.0
```

### Building the Code-Generation Chain (10 min)

**Say:** *"Step one: ask the LLM to generate a single line of pandas code that answers the question, given the DataFrame's column names and a couple of sample rows for context — NOT the entire dataset, since that's wasteful and unnecessary for code generation. Step two: YOUR Python code actually executes that generated line against the real `orders` DataFrame using `eval()`, and returns the real computed result."*

**Live-code:**

```python
code_gen_template = ChatPromptTemplate.from_messages([
    ("system",
     "You write a single line of pandas code to answer a question about a DataFrame named `df`. "
     "The DataFrame has these columns: {columns}. Here are 2 sample rows: {sample_rows}. "
     "Reply with ONLY the exact Python expression, no explanation, no markdown code fences, no variable assignment."),
    ("user", "{question}"),
])

code_gen_chain = code_gen_template | llm | StrOutputParser()

def ask_csv_copilot(df, question):
    columns = ", ".join(df.columns)
    sample_rows = df.head(2).to_dict(orient="records")
    code = code_gen_chain.invoke({
        "columns": columns,
        "sample_rows": sample_rows,
        "question": question,
    }).strip()
    print("Generated code:", code)
    result = eval(code, {"df": df, "pd": pd})
    return result

answer = ask_csv_copilot(orders, "What is the total revenue if revenue is quantity times price_each?")
print("Answer:", answer)
```

**Example output (illustrative generated CODE TEXT — actual LLM-generated code wording/variable naming will vary run to run; the EXECUTION of whatever valid pandas expression is generated, and the resulting number, is real/deterministic arithmetic once a specific line of code is run against the actual CSV):**
```
Generated code: (df['quantity'] * df['price_each']).sum()
Answer: 142400.0
```

**Say, emphasizing the key safety point:** *"Notice the FINAL numeric answer, `72087.0`, is NOT something the LLM calculated in its head — it's the output of pandas actually multiplying and summing the REAL numbers in the REAL CSV, in your own Python process. The LLM's only job was translating English into a valid line of code; arithmetic correctness comes entirely from pandas executing that code, not from the model's own math. This distinction is the single most important lesson of this segment."*

### A Critical Safety Note on `eval()` (4 min)

**Say:** *"Raise your hand if a 'run whatever the LLM generated with `eval()`' pattern sets off any alarm bells."* Expect some hands. **Say:** *"Good — it should. In this LAB, with a model you're prompting carefully and a known, trusted dataset, this is a reasonable teaching simplification. In a REAL production system taking live user input, blindly `eval()`-ing LLM-generated code is a genuine security risk — a cleverly crafted question could in principle produce code that does something unintended. Production systems restrict what's executable (an allow-listed subset of pandas operations, a sandboxed execution environment, or a dedicated, constrained query-generation library) rather than raw `eval()` against arbitrary generated code. We use plain `eval()` here specifically because this is a controlled teaching example, not a hardened deployed product — call this out explicitly to students."*

### Testing With a Second, Different Question (2 min)

**Live-code:**

```python
answer2 = ask_csv_copilot(orders, "How many unique products are there?")
print("Answer:", answer2)
```

**Example output (illustrative generated code text — actual code wording may vary; real, deterministic once code is executed against the actual CSV):**
```
Generated code: df['product'].nunique()
Answer: 5
```

### Comprehension Check (0 min — folded into discussion above given time)

*(Instructor note: SEGMENT 5 runs long by design; the safety discussion is treated as the comprehension-reinforcing moment instead of a separate quiz block.)*

---

## SEGMENT 6: Lab — Combine Extraction and Summarization into One Pipeline (10 min)

### Instructions (read aloud, step by step)

1. Define a Pydantic model `ReviewInsight` with fields `sentiment` (one of `"positive"`, `"negative"`, `"mixed"`) and `one_line_summary` (a string).
2. Build an extraction chain using `PydanticOutputParser` that reads a raw product review and returns a `ReviewInsight`.
3. Write a function `analyze_reviews(reviews)` that runs the chain over a LIST of review strings and returns a list of `ReviewInsight` objects.
4. Run it on at least three different sample reviews (at least one clearly positive, one clearly negative).

### Starter Code

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

class ReviewInsight(BaseModel):
    sentiment: str = Field(description="One of: positive, negative, mixed")
    one_line_summary: str = Field(description="A single sentence summarizing the review")

parser = ___(pydantic_object=___)

review_template = ChatPromptTemplate.from_messages([
    ("system", "You analyze product reviews. {format_instructions}"),
    ("user", "{review}"),
]).partial(format_instructions=___)

review_chain = ___ | ___ | ___

def analyze_reviews(reviews):
    results = []
    for r in reviews:
        insight = ___.invoke({"review": ___})
        results.append(insight)
    return results

sample_reviews = [
    "This laptop is amazing, fast, and the battery lasts all day. Best purchase this year.",
    "Arrived with a cracked screen and customer support never responded. Very disappointed.",
    "Good sound quality but the battery life is way shorter than advertised.",
]

for insight in analyze_reviews(sample_reviews):
    print(insight)
```

### Reference Solution

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

class ReviewInsight(BaseModel):
    sentiment: str = Field(description="One of: positive, negative, mixed")
    one_line_summary: str = Field(description="A single sentence summarizing the review")

parser = PydanticOutputParser(pydantic_object=ReviewInsight)

review_template = ChatPromptTemplate.from_messages([
    ("system", "You analyze product reviews. {format_instructions}"),
    ("user", "{review}"),
]).partial(format_instructions=parser.get_format_instructions())

review_chain = review_template | llm | parser

def analyze_reviews(reviews):
    results = []
    for r in reviews:
        insight = review_chain.invoke({"review": r})
        results.append(insight)
    return results

sample_reviews = [
    "This laptop is amazing, fast, and the battery lasts all day. Best purchase this year.",
    "Arrived with a cracked screen and customer support never responded. Very disappointed.",
    "Good sound quality but the battery life is way shorter than advertised.",
]

for insight in analyze_reviews(sample_reviews):
    print(insight)
```

**Example output (illustrative — actual LLM classification/summary wording will vary run to run; the object TYPE and field structure are deterministic and verified against the Pydantic schema):**
```
sentiment='positive' one_line_summary='The reviewer loves the laptop for its speed and all-day battery life.'
sentiment='negative' one_line_summary='The reviewer received a damaged laptop and got no response from support.'
sentiment='mixed' one_line_summary='The reviewer likes the sound quality but is unhappy with shorter-than-advertised battery life.'
```

**Instructor circulates**, checking specifically that students used `PydanticOutputParser` (not plain `StrOutputParser`) and that `analyze_reviews` returns actual `ReviewInsight` objects rather than raw strings — a common bug is forgetting `.partial(format_instructions=...)`, which leaves the LLM with no idea what JSON shape to produce.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Structured extraction using `PydanticOutputParser`, combining Session 5's validation with Session 6's chains
- A parameterized summarization chain with controllable output length and an explicit anti-hallucination instruction
- A grounded FAQ bot that answers only from known facts and admits when it doesn't know something
- A CSV copilot pattern: LLM generates code, Python actually executes it — never trust the model's own arithmetic
- Combining extraction into a reusable, list-processing pipeline

**Bridge to next session:** *"Today's FAQ bot worked because we hand-pasted five bullet points into the prompt. That doesn't scale to a real knowledge base. Next session is a pure-concept master class on embeddings and semantic search — the exact math that lets a real system automatically FIND the few most relevant facts out of thousands, instead of you hand-selecting and pasting them. Combined with today's extraction and chaining patterns, that's the foundation for Session 9's retrieval pipelines and Session 11's full RAG system."*

**Homework / self-practice:**
1. Extend `SupportTicket` from SEGMENT 2 with a fourth field, `urgency` (`"low"`, `"medium"`, `"high"`), and test extraction on two new sample messages.
2. Add a sixth fact to `faq_knowledge` and write a question that specifically tests whether the bot now correctly uses it.
3. Add a third question to the CSV copilot demo (e.g. "which product had the highest single-order revenue?") and verify the generated code's answer by computing it yourself in a separate line of plain pandas code, to confirm the LLM-generated code was correct.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Why use `PydanticOutputParser` instead of just asking the LLM to "reply in JSON" and using `json.loads()` ourselves, like Session 5 originally did manually?**
→ You could — and that's exactly what `PydanticOutputParser` does FOR you under the hood, automatically, including generating the instruction text and running the Pydantic validation step. It's the same idea from Session 5, wired directly into the chain so you don't rebuild that glue code by hand every time.

**Q: In the FAQ bot, what stops a user from asking something totally unrelated and getting a made-up answer anyway?**
→ Nothing is a perfect guarantee with any LLM-based system, but the explicit system instruction ("answer ONLY using the facts below... say you don't know") meaningfully reduces this risk. It's not foolproof — a sufficiently adversarial or unusual question can sometimes still produce an unwanted answer, which is why real production systems add additional checks beyond prompt instructions alone.

**Q: Is the CSV copilot's `eval()` pattern something I should actually ship in a real product?**
→ Not as shown here, verbatim. As discussed in SEGMENT 5, raw `eval()` on arbitrary LLM-generated code is a real security risk in any system accepting untrusted user input. Treat today's version as teaching the CORE pattern (LLM translates language to code, Python executes and computes); a shippable version needs sandboxing or a constrained query layer on top.

**Q: Could the summarization chain from SEGMENT 3 be combined with the extraction chain from SEGMENT 2 into one single chain object, instead of two separate chains called in sequence?**
→ Yes, conceptually — this is exactly the "sequential workflow" idea from Session 6 SEGMENT 5, just with the intermediate value being a Pydantic OBJECT instead of a plain string this time. You'd extract first, then feed one of the extracted fields (e.g. `ticket.category`) into a second chain's input dict, the same pattern as last session's premise → opening-line chain.

**Q: What happens to the FAQ bot's reliability if `faq_knowledge` grows to 50 or 100 bullet points instead of 5?**
→ It still technically works up to a point, but token cost grows (you're re-sending the whole block on every single question) and accuracy can start to degrade as the model has to search through more pasted text to find the relevant fact. This exact scaling problem is what Session 8's embeddings and Session 9's retrieval are built to solve.

---

## Instructor Notes

- **Prerequisite check:** Confirm `orders.csv` is in the working directory before SEGMENT 5 — a very easy "forgot to upload the file" blocker that stalls the whole segment if caught late.
- **Common mistake:** Forgetting `.partial(format_instructions=parser.get_format_instructions())` on the extraction/FAQ templates, leaving the LLM with no idea what shape or facts to use — review every student's SEGMENT 2 chain definition for this specific line before moving on.
- **Another common mistake:** In the CSV copilot, generated code sometimes includes a stray `df = ` assignment or markdown code fence (```python ... ```) despite instructions not to — have students print the raw generated string BEFORE calling `eval()` so they can see and strip this, rather than getting a confusing `SyntaxError`.
- **Another common mistake:** Confusing the Pydantic schema's `Field(description=...)` text (which becomes part of the PROMPT) with ordinary Python docstrings (which do not) — emphasize that this description text is functionally instructional content sent to the model, not just internal documentation.
- **Engagement tip:** SEGMENT 5's "whose hands went up at the `eval()` safety question" moment is a good natural checkpoint for a short discussion on LLM-application security more broadly — don't rush past it even if running slightly behind.
- **Time check:** If running behind before the break, shorten SEGMENT 3's "testing different lengths" demo to a single length instead of two.
- **If running long after the break:** Trim SEGMENT 5 to the first CSV copilot question only, skipping the second verification question, and move it to homework item 3 instead.
- **Materials to prepare:** `orders.csv` pre-placed in the working directory for every student; scratch notebook with SEGMENT 2/5's live-coding demos pre-typed, since these have the most new moving parts.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Missing `.partial(format_instructions=...)` on an extraction/FAQ template | LLM has no idea what JSON shape or facts to use; parser raises a validation error, or FAQ bot ignores the known facts | Always bake `format_instructions`/`knowledge` into the template with `.partial(...)` before chaining |
| Pydantic field without a clear `description` | LLM guesses at field meaning inconsistently, producing unreliable extraction | Write a specific, unambiguous `description` for every `Field()`, since it becomes part of the prompt |
| Generated pandas code wrapped in markdown fences or with a stray assignment | `eval()` raises `SyntaxError` or silently assigns instead of returning a value | Instruct the model explicitly ("no markdown code fences, no variable assignment") and `.strip()`/inspect the generated string before executing |
| Treating the CSV copilot's final number as "the LLM's answer" | Misattributes correctness to the model instead of to pandas actually executing real code | Always remember: the LLM only generates the CODE; pandas computing the real result is what makes the number trustworthy |
| FAQ bot answering confidently about something not in `faq_knowledge` | Hallucinated, unverifiable answer presented as fact | Add (and test) an explicit "if not in these facts, say you don't know" instruction; verify it with an out-of-scope test question |
| Forgetting `Optional` on extraction fields that won't always be present in the input text | Validation errors on messages missing that field, or LLM forced to invent a plausible-but-fake value | Mark genuinely optional fields `Optional[...] = None` in the Pydantic schema |

---

## Appendix: `orders.csv` Full Contents (Instructor Reference)

```
order_id,product,quantity,price_each
1001,Notebook,3,50.0
1002,Pen,10,8.0
1003,Laptop,1,55000.0
1004,Notebook,2,50.0
1005,Headphones,4,1200.0
1006,Pen,25,8.0
1007,Monitor,2,9500.0
1008,Notebook,5,50.0
1009,Headphones,1,1200.0
1010,Laptop,1,52000.0
1011,Monitor,1,9500.0
1012,Pen,15,8.0
```

*(Total revenue = sum of `quantity * price_each` across all 12 rows = 150 + 80 + 55000 + 100 + 4800 + 200 + 19000 + 250 + 1200 + 52000 + 9500 + 120 = 142400.0, matching SEGMENT 5's live-coded output exactly. There are 5 distinct products — Notebook, Pen, Laptop, Headphones, Monitor — matching the `nunique()` output. Both figures were verified by actually running pandas against this exact CSV; instructor note: recompute directly from the CSV if this appendix is ever edited.)*

---

## Appendix: When to Use Each Output Parser (Instructor Reference)

| Parser | Returns | Best for |
|---|---|---|
| `StrOutputParser` | Plain Python string | Prose output: summaries, chat replies, generated text |
| `PydanticOutputParser` | A validated Pydantic model instance | Structured extraction with typed, named fields |
| `JsonOutputParser` | A plain Python dict (no Pydantic validation) | Quick structured output when you don't need strict schema validation |

---

## FAQ — Additional Questions

**Q: Can the CSV copilot handle a question requiring MULTIPLE lines of pandas code, not just one expression?**
→ Not with today's single-expression design — it deliberately constrains the model to one valid Python expression specifically so `eval()` (rather than `exec()` with multiple statements) is sufficient, which is a narrower, somewhat more contained surface. A more capable version would need a different, more carefully sandboxed execution strategy, since now the generated code could do considerably more than compute and return one value.

**Q: Does `PydanticOutputParser` work with nested models (a field that is itself another Pydantic model)?**
→ Yes — Pydantic's own nested-model support (from Session 5) carries through; `get_format_instructions()` correctly describes nested structure to the LLM as well, though deeply nested schemas are harder for a model to reliably fill in correctly than flat ones, in practice.

**Q: In the FAQ bot, could we ask the LLM to also return a confidence score alongside its answer?**
→ You could add a field for it using the same `PydanticOutputParser` pattern from SEGMENT 2, but treat any such self-reported confidence skeptically — a model's own stated confidence is not a reliably calibrated measure of actual correctness, and should not be treated as a substitute for real evaluation.

---

## Materials Checklist

- [ ] `orders.csv` present in every student's working directory before SEGMENT 5
- [ ] `pip install langchain-core langchain-openai pandas pydantic` verified on the classroom image
- [ ] Scratch notebook with SEGMENT 2 and SEGMENT 5's live-coding demos pre-typed
- [ ] Sample product reviews ready for the SEGMENT 6 lab (or reuse this script's exact three)
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's length-comparison demo to a single `max_sentences` value instead of two |
| Running long after break | Trim SEGMENT 5 to its first CSV copilot question only, skipping the second verification question |
| Low energy after lunch/break | Run SEGMENT 4's "what will the bot say when it doesn't know" question as a group prediction before revealing the live output |
| Advanced group finishes lab early | Have them add a fourth Pydantic field (e.g. `recommended_response_tone`) to `ReviewInsight` and re-run |
| No shared screen / projector issue | Walk through the Pydantic schema and prompt-assembly steps on the whiteboard using this script's exact worked examples |
| OpenRouter outage / no internet | Walk through schema design, `.partial()` wiring, and the CSV copilot's non-LLM pandas execution step (which needs no live call once code is given) using this script's exact illustrative text |

---

## End-of-Session Quiz (5 Questions)

1. What does `parser.get_format_instructions()` do, and how does its output reach the LLM?
2. In the FAQ bot, why does the known-facts block belong in the system message rather than the user message?
3. In the CSV copilot, what part of the final numeric answer comes from the LLM, and what part comes from pandas?
4. Why is raw `eval()` on LLM-generated code a real production security concern, even though it's fine for this lab?
5. What's the difference in return type between `StrOutputParser` and `PydanticOutputParser`?

**Answer key (instructor):**
1. It auto-generates instruction text describing the exact JSON shape required, derived from the Pydantic schema; it reaches the LLM by being baked into the prompt via `.partial(format_instructions=...)`.
2. The system message holds standing context relevant to every question; the known facts apply to the whole conversation, while the user message is reserved for the specific, changing question.
3. The LLM only generates the pandas CODE (the translation from English to an expression); the actual computed number comes from pandas executing that code against the real DataFrame, not from the model's own arithmetic.
4. A cleverly crafted or adversarial natural-language question could, in principle, cause the LLM to generate code that does something unintended when blindly executed with `eval()` against untrusted input — a controlled classroom dataset and careful prompting makes this low-risk here, but not in a real system facing arbitrary user input.
5. `StrOutputParser` returns a plain Python string; `PydanticOutputParser` returns a validated instance of your Pydantic model, with typed, named fields.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| `SupportTicket` + `urgency` field extension | Correct new field, tested on two new messages with sensible results | Field added, thin testing | Field added but schema/prompt mismatch | Not attempted |
| FAQ bot new fact + targeted test question | New fact correctly used in a targeted test, clear before/after comparison | New fact added, test present but not clearly targeted | Fact added, no real test of its usage | Not attempted |
| CSV copilot new question + manual verification | New question answered correctly, independently verified against plain pandas computation | Question answered, verification present but informal | Question attempted, no verification | Not attempted |

**Total:** /12 — Pass threshold: 8/12
