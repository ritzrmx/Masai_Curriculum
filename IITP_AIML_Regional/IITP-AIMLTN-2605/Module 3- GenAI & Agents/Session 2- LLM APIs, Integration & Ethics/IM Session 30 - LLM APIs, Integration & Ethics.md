# Instructor Reference: Session 12.2 — LLM APIs, Integration & Ethics
90 min | 75 min teaching + 5 min break + 10 min coding practice
Domain: Coding
Tools / Dataset: `support_tickets.csv` (40 tickets, 6 categories) in the `Datasets` folder; companion notebook `IM Session 30 - LLM APIs, Integration & Ethics.ipynb`. Python, pandas. **No API key, no network, no cost — the notebook uses a deterministic simulator with the real request/response shape.**
Prior knowledge: Students can count tokens, explain the context window as a shared budget, describe probabilistic generation and hallucination, and build zero-shot, few-shot and chain-of-thought prompts with their token costs (12.1).
Next session: RAG & Embedding Foundations

**LMS:** IM Session 30 · Lecture ID 166775 · Tue 8 Sept, 8:00 pm

---

## Pre-Class Setup

> Run before class — students never see this.

Open the companion notebook and **Run All**. Confirm these outputs, which the session is built on:

```
SAFE FAILURE - no key present, and nothing secret was printed:
OPENAI_API_KEY is not set. ...

request 2: succeeded on attempt 2 -> delivery
input tokens for all 40 tickets : 4,307
tickets containing PII : 8 of 40
identifiers found      : {'EMAIL': 3, 'PHONE': 2, 'ORDER_ID': 5}
replies accepted by the validator : 37 / 40
accuracy on accepted replies : 0.865  (n = 37)
```

Two things to be clear about before you begin:
- **Do not** set a real API key on the teaching machine. The safe-failure path in Part 2 *is* the demonstration.
- Say out loud, early, that the `MockLLM` is a keyword matcher, not a language model. Students must not leave
  thinking they called GPT. Everything wrapped *around* it — retries, redaction, validation — is production-real.

---

## Opening & Problem Framing `(10 min)`

**Hook** `(2-3 min)`
Ask: "Last session you wrote a prompt and priced it. Now imagine it runs over 5,000 tickets tonight while you
sleep. Name everything that can go wrong that simply could not go wrong when you were pasting one ticket into a
chat window by hand."

Collect answers on the board — you are looking for: the key leaks, the network fails, the bill runs away, customer
data gets sent, the reply comes back in the wrong shape. Then reveal: those five are today's session, in order.

**Bridge from prior session** `(1-2 min)`
Say: "Last session we did GenAI Foundations & Prompt Engineering — a human held the wheel. Today the same triage
job runs programmatically, and everything a human was silently absorbing becomes your code's problem."

| Prior sessions | Today |
|---|---|
| A human pasted each ticket | Code sends every ticket, unattended |
| A human noticed a weird reply | A validator must catch it, or it corrupts the pipeline |
| No key, no bill | A secret that must not leak, and a per-token bill |
| The whole ticket was sent | Only the minimum necessary is sent |

**Real-world relevance** `(2-3 min)`
Instructor picks 2–3 to say aloud; the list is reference only.
- Leaked API keys in public GitHub repos are found by scanning bots within minutes and drained.
- Samsung banned internal ChatGPT use in 2023 after engineers pasted proprietary source code into it.
- Under India's DPDP Act, sending customer personal data to a third-party processor without a lawful basis is a compliance failure, not a style issue.
- Every serious LLM pipeline has a retry policy, because a 429 rate-limit response is routine, not exceptional.
- Support teams report coverage and accuracy together — "we auto-handle 80% at 95% accuracy" is the shape of a real SLA.

**Session promise** `(30 sec)`
Say: "By the end of today you'll be able to describe an API call's anatomy, load a key without ever leaking it,
retry only the failures worth retrying, estimate a batch's cost before running it, and put guardrails on both what
you send and what you accept back."

---

### SEGMENT 1 — Anatomy of an API Call and Key Safety `(14 min)`

> Instructor note: Students met system vs user prompts in 12.1. Acknowledge the `messages` list as that same
> distinction in wire format — do not reteach the roles.

**Concept** `(4 min)`
Analogy — ordering at a counter. You state which menu item (**model**), what you want (**messages**), any
modifications (**parameters**), and you get back the item plus a bill (**response** with `usage`). Every provider
sells the same four things under different names.
Formal definition: an LLM API call sends a model identifier, a list of `{role, content}` messages, and decoding
parameters; it returns generated text plus a usage block reporting tokens consumed.

**Implementation / Demonstration** `(7 min)`
Show the two reference blocks side by side — OpenAI and Gemini — and say: different SDK names, identical shape.
Learn it once, switch providers cheaply.

Then run the simulator and show the response:

```
{"model": "mock-triage-1",
 "choices": [{"message": {"role": "assistant", "content": "delivery"}, "finish_reason": "stop"}],
 "usage": {"prompt_tokens": 105, "completion_tokens": 2, "total_tokens": 107}}
```

Say: point at `usage`. That is what you are billed on, and it is the only trustworthy basis for a cost estimate.

Now the key section. Run it with **no key set** and let the failure happen live:

```
SAFE FAILURE - no key present, and nothing secret was printed:
OPENAI_API_KEY is not set. Export it in your shell before running:
    export OPENAI_API_KEY='your-key-here'
```

Say: the error tells you exactly what to do and reveals nothing. Then walk the four wrong patterns, pausing on the
third:

```
requests.get(f"https://api.x.com?key={api_key}")   # secret in a URL, logged by every proxy
```

Ask: "Why is this worse than it looks?" Answer: query strings are recorded by proxies, load balancers and browser
history. A key in a URL is a key in someone else's log file. Credentials belong in a header, never a URL.

**Key point**
**An API key is a password that spends your money — it loads from the environment, it is masked in logs, and a missing key fails loudly rather than leaking quietly.**

**Student try** `(3 min)`
Task: write `mask()` for a key of length 4 or fewer. What should it return, and why is returning the first
character still wrong for a short key?

---

### SEGMENT 2 — Usage Patterns: Retries, Backoff and Cost `(14 min)`

**Concept** `(4 min)`
Analogy — redialling a busy phone line makes sense; redialling a disconnected number does not. Same with API
failures: some are worth another attempt, some will fail identically forever.
Formal definition: retry only **transient** failures (timeout, 429 rate limit, 5xx), back off exponentially so you
do not pile load onto a struggling service, cap the attempts, and re-raise honestly when they are exhausted. Never
retry 400 (malformed request) or 401 (bad key).

**Implementation / Demonstration** `(7 min)`
Run the flaky client — every second underlying call fails:

```
request 1: succeeded on attempt 1 -> delivery
request 2: succeeded on attempt 2 -> delivery
request 3: succeeded on attempt 2 -> delivery
```

Say: all three succeeded despite half the calls failing. Then point at the `raise` in the function and ask why it
matters. Land it: **a retry wrapper that silently returns a default on final failure is worse than no wrapper**,
because the caller can no longer tell a real answer from a fallback.

Now cost, before the batch rather than after:

```
input tokens for all 40 tickets : 4,307
output tokens (estimated)       : 200
estimated cost for one full pass: $0.00077
cost per 100,000 tickets        : $1.92
```

Say: fractions of a cent today — but the right-hand number is the one that decides whether someone runs this over
a year of history. Flag that the rates are illustrative placeholders; always check current pricing.

Then the finding worth pausing on: the system prompt is **74 tokens paid 40 times = 2,960 of 4,307 input tokens,
68.7% of everything sent.** On a repetitive classification job the instructions, not the data, dominate the bill.

**Key point**
**Retry only what is genuinely transient, cap it, and re-raise honestly — then estimate the bill before you launch the batch, not after.**

**Student try** `(3 min)`
Task: your provider returns `429 Too Many Requests` with a `Retry-After: 30` header. Should your backoff schedule
override that header or respect it? Give one sentence of justification.

---

### SEGMENT 3 — Guardrails and Ethics `(12 min)`

**Concept** `(4 min)`
Analogy — an airport has security on the way in *and* customs on the way out. One direction is not enough.
Formal definition: **input guardrails** control what leaves your system (chiefly, do not send personal data you do
not need — data minimisation). **Output guardrails** control what you accept back, because the model returns free
text while your code expects structure.

**Implementation / Demonstration** `(5 min)`
Run the redaction pass:

```
tickets containing PII : 8 of 40
identifiers found      : {'EMAIL': 3, 'PHONE': 2, 'ORDER_ID': 5}

BEFORE: ... I want a refund not a replacement. Order MRD-88213. Reach me at arun.k@example.com
AFTER : ... I want a refund not a replacement. Order [ORDER_ID]. Reach me at [EMAIL]
```

Ask: "Can you still tell this is a refund ticket?" Yes. Land the test for any redaction rule: **does removing it
cost you accuracy on the actual task?** If not, there was never a reason to send it.

Then the output side:

```
replies accepted by the validator : 37 / 40
replies rejected                  : 3

   ticket_id                             raw_reply
6   TKT-1007  Sorry, I am not sure about this one.
15  TKT-1016  Sorry, I am not sure about this one.
39  TKT-1040  Sorry, I am not sure about this one.
```

Say: without the validator that sentence lands in a `category` column and quietly corrupts every downstream count.
A rejection is a **routing decision, not a crash** — send it to a human queue. Never coerce it into a category to
keep the batch tidy.

```
accuracy on accepted replies : 0.865  (n = 37)
coverage (share auto-handled): 0.925
```

Say: report both. 92.5% coverage at 0.865 accuracy with 3 escalations is a describable system; a single accuracy
number hides the trade-off.

Close on the ethics table — the rules you cannot code: data minimisation and DPDP, confidential data, provider
terms, whether your tier trains on your data, attribution, and accountability. Say the last one plainly:
**"the model decided" is not a defence.**

**Key point**
**Guardrails work in both directions — minimise what you send, validate what you accept — and a named human owns every consequential decision.**

**Student try** `(3 min)`
Task: add a `CREDIT_CARD` pattern to `PII_PATTERNS` for a 16-digit number. Then name one field in our tickets that
looks like PII but is safe to send, and justify it.

---

--- BREAK (5 min) ---

---

## Building Programs `(15 min)`

### Program 1: Safe key loader with masking `(5 min)`

Purpose: a reusable loader that fails loudly and never leaks.

```python
def get_key(var_name, required=True):
    key = os.environ.get(var_name)
    if not key and required:
        raise RuntimeError(f"{var_name} not set. Run: export {var_name}='...'")
    return key

def mask(key):
    if not key:
        return "<not set>"
    return f"{key[:3]}...{key[-2:]} (len {len(key)})" if len(key) > 6 else "***"

for var in ["OPENAI_API_KEY", "GEMINI_API_KEY"]:
    print(f"{var:<18} {mask(get_key(var, required=False))}")
```
```
OPENAI_API_KEY     <not set>
GEMINI_API_KEY     <not set>
```

Say: `required=False` is for a status check like this one. The call that actually needs the key must use
`required=True` so it fails before spending anything.

### Program 2: Guardrailed single-ticket call `(5 min)`

Purpose: the whole pipeline for one ticket — redact, call, validate.

```python
def triage(text, client):
    clean, removed = redact(text)
    resp = client.chat(model="mock-triage-1",
                       messages=[{"role": "system", "content": SYSTEM_PROMPT},
                                 {"role": "user", "content": f"Ticket: {clean}\nCategory:"}])
    raw = resp["choices"][0]["message"]["content"]
    check = validate_category(raw)
    return {"category": check["category"], "accepted": check["ok"],
            "pii_removed": removed, "tokens": resp["usage"]["total_tokens"],
            "route": "auto" if check["ok"] else "human_queue"}

client = MockLLM()
print(triage(tickets.iloc[0]["ticket_text"], client))
print(triage(tickets.loc[tickets["ticket_id"] == "TKT-1016", "ticket_text"].iloc[0], client))
```
```
{'category': 'refund', 'accepted': True, 'pii_removed': {'EMAIL': 1, 'ORDER_ID': 1}, 'tokens': 125, 'route': 'auto'}
{'category': None, 'accepted': False, 'pii_removed': {}, 'tokens': 112, 'route': 'human_queue'}
```

Say: the second return is not an error — it is the system correctly declining to guess and routing to a human.

### Program 3: Batch runner with a cost ceiling `(5 min)`

Purpose: stop a runaway batch before it spends the budget.

```python
def run_batch(df, client, token_budget=3000):
    used, rows = 0, []
    for row in df.itertuples():
        if used >= token_budget:
            print(f"STOPPED at budget: {used} tokens used, {len(rows)} of {len(df)} processed")
            break
        out = triage(row.ticket_text, client)
        used += out["tokens"]
        rows.append({"ticket_id": row.ticket_id, **out})
    return pd.DataFrame(rows), used

batch, used = run_batch(tickets, MockLLM())
print(f"processed {len(batch)} tickets, {used} tokens")
print(batch["route"].value_counts().to_dict())
```
```
STOPPED at budget: 3105 tokens used, 28 of 40 processed
processed 28 tickets, 3105 tokens
{'auto': 26, 'human_queue': 2}
```

Say: the budget ceiling is what turns "the job overran overnight" into a controlled stop you can investigate.

---

## Common Mistakes `(10 min)`

**Mistake 1: Hardcoding the key in the notebook**
Wrong: `api_key = "sk-proj-abc123..."` in a cell, then committing it.
Right: `os.environ["OPENAI_API_KEY"]`, with the key exported in the shell and never in the file.
Why it matters: Public repos are scanned by bots within minutes; a committed key is a burned key even after deletion.

**Mistake 2: Retrying every exception**
Wrong: `except Exception: retry` so the batch never dies.
Right: Retry only transient failures — timeout, 429, 5xx. Let 400 and 401 fail immediately.
Why it matters: Retrying a bad key or a malformed request burns time and quota while hiding the real fault.

**Mistake 3: Returning a default when retries are exhausted**
Wrong: `except: return "unknown"` at the end of the retry wrapper.
Right: Re-raise, so the caller knows the difference between an answer and a failure.
Why it matters: A silent fallback contaminates results with values that were never model output.

**Mistake 4: Sending the whole record because filtering is effort**
Wrong: Passing the full ticket, including email and phone, because the model "ignores what it does not need."
Right: Redact first — 10 identifiers here, with no loss of task accuracy.
Why it matters: Once data leaves your system it cannot be recalled, and under DPDP that disclosure needs a lawful basis.

**Mistake 5: Trusting the reply's shape**
Wrong: Writing `response.content` straight into a `category` column.
Right: Validate against the allowed set; route anything else to a human queue.
Why it matters: Three replies here were not categories at all and would have silently corrupted every downstream count.

**Mistake 6: Reporting accuracy without coverage**
Wrong: "The system is 86.5% accurate."
Right: "It auto-handles 92.5% of tickets at 86.5% accuracy, escalating the rest."
Why it matters: Accuracy alone hides whether the system answered everything or quietly skipped the hard cases.

---

## Session Recap

| Topic | What to remember |
|---|---|
| API anatomy | model + messages (`role`/`content`) + parameters → text plus a `usage` block you are billed on |
| Key safety | Load from the environment, mask in logs, fail loudly; never in a URL, a print, or an error |
| Retries | Transient failures only, exponential backoff, capped attempts, re-raise honestly at the end |
| Cost | Estimate before the batch. Here the system prompt was 68.7% of all input tokens |
| Input guardrail | Redact PII — 10 identifiers removed across 8 tickets, no accuracy lost |
| Output guardrail | Validate against the allowed set; 3 of 40 replies were not categories and were routed to a human |
| Ethics | Data minimisation, provider terms, disclosure — and a named human owns consequential decisions |

Path forward: "Next session: RAG & Embedding Foundations — today we controlled what goes in and what we accept back; next session we fix the hallucination problem itself by grounding the model in retrieved source text."

---

## Coding Practice `(10 min)`

**Question**: Write `audit_batch(df)` that returns, for the whole ticket file: how many tickets contain PII, how
many identifiers would be sent if redaction were skipped, the total input tokens, and the share of those tokens
spent on the system prompt. Use it to make one concrete recommendation for reducing cost.

**Expected solution**:

```python
def audit_batch(df):
    total_pii, tickets_with_pii = 0, 0
    for text in df["ticket_text"]:
        _, found = redact(text)
        if found:
            tickets_with_pii += 1
            total_pii += sum(found.values())
    sys_tokens = count_tokens(SYSTEM_PROMPT)
    input_tokens = sum(sys_tokens + count_tokens(f"Ticket: {t}\nCategory:") for t in df["ticket_text"])
    return {"tickets_with_pii": tickets_with_pii,
            "identifiers_exposed_if_unredacted": total_pii,
            "total_input_tokens": input_tokens,
            "system_prompt_share": round(sys_tokens * len(df) / input_tokens, 3)}

print(audit_batch(tickets))
```
```
{'tickets_with_pii': 8, 'identifiers_exposed_if_unredacted': 10,
 'total_input_tokens': 4307, 'system_prompt_share': 0.687}
```

Expected recommendation: **shorten the system prompt** — it is 68.7% of all input tokens and is re-sent on every
request, so trimming it is the single largest available saving. Accept any recommendation that cites the 0.687
share and targets the repeated cost rather than the ticket text.
