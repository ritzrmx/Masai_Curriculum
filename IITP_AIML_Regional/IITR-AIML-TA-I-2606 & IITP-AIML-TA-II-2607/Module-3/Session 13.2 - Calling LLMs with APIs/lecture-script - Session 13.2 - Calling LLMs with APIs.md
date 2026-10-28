# Lecture Script: Generative AI — Calling LLMs with APIs
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 13.2 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can choose a provider with reasons, store an API key safely with `python-dotenv`, send a structured system/user/assistant conversation to an LLM with raw `requests`, parse the answer and token usage, and handle errors and rate limits with retry-and-backoff.

**Student profile at this point:** They know from Session 13.1 how LLMs generate tokens and what temperature and context windows are, and they've used `requests` and JSON in Module 1. They have never called an LLM from code. Likely wrong assumptions: "the key is just a config value, it can sit in my notebook," "the model remembers what I said last call," and "if it fails, just retry until it works." Boredom risk: low — the first real API response is a strong hook — but setup friction is high, so the TA should be ready to help during the break.

**Key outcome:** Students should leave instinctively asking, before writing any LLM code: "Where is my key stored, what goes in the system message, what's my `max_tokens`, and which errors should I retry?"

> 🎯 **The one sentence this session must land:** *An LLM API call is just a courier parcel — address, ID slip and contents — and a professional sends it with the key hidden, the rules in the system message, a cap on the reply, and a plan for when the counter says "come back later."*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The ₹40,000 GitHub Push" | 8 min | 8 min |
| Concept Block 1: Picking a Provider | 10 min | 18 min |
| Concept Block 2: API Keys with python-dotenv | 10 min | 28 min |
| Practical Block 1: Spot the Leaked Key | 7 min | 35 min |
| Concept Block 3: Raw Calls via requests | 12 min | 47 min |
| Concept Block 4: Message Structure | 10 min | 57 min |
| **BREAK** | 10 min | 67 min |
| Practical Block 2: Write the Messages List | 8 min | 75 min |
| Concept Block 5: Parsing Responses | 8 min | 83 min |
| Practical Block 3: Live Coding Demo (TA Code) | 12 min | 95 min |
| Concept Block 6: Errors & Rate Limits | 10 min | 105 min |
| Practical Block 4: Retry or Fix? | 7 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "The ₹40,000 GitHub Push" (8 min)

Open with this, verbatim-ish:

> "Picture this. A student finishes a cool LLM project late one night. Proud of it, he pushes his notebook to a public GitHub repo and goes to sleep. He wakes up to an email from the provider: ₹40,000 of usage overnight — not from him. Bots scan GitHub constantly for strings that look like API keys. His was on line 3. This happens to real developers every week."

Pause. Ask the room:

> "How many of you have ever pasted a password or key straight into a notebook cell?"

(Honest hands will go up.)

> "Today you get a key that can spend real money. So we'll do this like professionals from the very first line."

**Pivot line:** "In 13.1 we simulated the next-token guess with NumPy. Today, the 11:40 pm partner's question goes to a real model, from real Python, and comes back as a real answer."

**Context for sessions ahead:** "Prompt engineering in 14.1 changes what you send, Pydantic in 14.3 changes what comes back, and LangChain in 15.1 wraps this exact call in nicer building blocks."

---

## Concept Block 1: Picking a Provider (10 min)

> "When you book a cab, you might open Ola, Uber or Rapido — or an app that compares all three. OpenAI, Anthropic and Google each sell model access through an **API**. **OpenRouter** is the comparison app: one key, one format, hundreds of models — switching from GPT to Claude to Llama is changing one string."

Write on the board:

> Choose by: How good? · How fast? · Cost per million tokens (13.1's formula)? · Where does the data go?

### 🔴 The trap / highest-value moment
> "The trap is reaching for the biggest model by default. Our helpdesk answers 'when is my payout credited' — a small model might do that at a fraction of the cost and twice the speed. Write this down: *start with the smallest model that passes your test set — upgrade only with evidence.* You'll build that test set in 14.1."

---

## Concept Block 2: API Keys with python-dotenv (10 min)

> "Your UPI PIN lets anyone who knows it spend your money. An **API key** is exactly that for your provider account."

Write on the board:

```
1. .env file:   OPENROUTER_API_KEY=sk-or-v1-...
2. Python:      load_dotenv()  →  os.getenv("OPENROUTER_API_KEY")
3. .gitignore:  .env
```

> "All three steps, every project. And if a key ever leaks, don't just delete the message — revoke the key on the provider's site and create a new one."

### 🔴 The trap / highest-value moment
> "The sneaky leak isn't the key in the code — it's the output. Print the key while debugging, save the notebook, push it: leaked. Write this down: *never print the full key — print the first few characters at most.*"

---

## Practical Block 1: Spot the Leaked Key (7 min)

Show four snippets and have pairs decide "safe" or "leaked", with a reason, in two minutes: (1) the key typed into cell 1 — leaked; (2) a `.env` file loaded properly but no `.gitignore` — leaked on the next push; (3) `.env` plus `.gitignore`, but `print(api_key)` with the output saved — leaked; (4) `.env` plus `.gitignore`, printing only `api_key[:10]` — safe. Cold-call pairs, and point out that #2 and #3 look careful: leaks usually come from one missing step.

---

## Concept Block 3: Raw Calls via requests (12 min)

> "Sending a request to an LLM is like sending a courier parcel: an address, a proof-of-identity slip and the parcel itself."

```python
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",                 # address
    headers={"Authorization": f"Bearer {api_key}",                   # ID slip
             "Content-Type": "application/json"},
    json={"model": "openai/gpt-4o-mini",                             # parcel
          "messages": [{"role": "user", "content": "Why is my weekly payout less than last week?"}],
          "temperature": 0.2, "max_tokens": 150},
    timeout=30)
```

> "Two settings from 13.1: low `temperature` because policy answers should be steady, and `max_tokens`, a hard cap on reply length — your cost and latency brake. `timeout=30` stops you waiting forever. Why raw `requests`? Because when LangChain throws a strange error later, you'll know it's just this POST request underneath."

### 🔴 The trap / highest-value moment
> "Forget `max_tokens` and a chatty model may write a 1,000-token essay to a yes/no question — you pay for every token and the partner waits for every token. Write this down: *always cap the reply.*"

---

## Concept Block 4: Message Structure (10 min)

> "Before a support call, the agent gets a briefing card from her manager: be polite, payout questions only, reply in the partner's language. Then the partner speaks, she replies, the partner speaks again."

Write on the board:

> `system` = developer's rules (the briefing card)
> `user` = the partner
> `assistant` = the model's earlier replies

> "And remember 13.1: the model has no memory. To continue a chat, you resend the whole list every time. That's why long chats get expensive — the input grows every turn."

### 🔴 The trap / highest-value moment
> "The classic bug: sending only the newest message. The partner asks 'Agar Friday chhutti ho toh?' and the model has no idea this is even about payouts. Write this down: *every call carries the whole conversation — system first, newest user message last.*"

---

## BREAK (10 min)

*(TA: use the break to help anyone whose `.env` isn't loading. The usual causes are a file saved as `.env.txt` on Windows, the `.env` file sitting in a different folder from the notebook, a typo in the variable name, or forgetting to call `load_dotenv()` — restart the kernel after fixing.)*

---

## Practical Block 2: Write the Messages List (8 min)

Give students this scenario and four minutes to write the full `messages` list: the helpdesk must reply only in simple Hindi, under 50 words, payout topics only; the partner asked "Mera payout kab aayega?", the bot replied "Aapka payout har Friday aata hai.", and the partner now asks "Agar Friday chhutti ho toh?" Reveal the answer: four messages — the rules in `system`, the first question as `user`, the bot's reply as `assistant`, and the newest question last as `user`. If someone asks why the rules can't just go at the start of the user message, say a partner could then type "ignore the above" and it's one user message arguing with another — we'll meet this "prompt injection" properly in 18.1.

---

## Concept Block 5: Parsing Responses (8 min)

> "When an Amazon parcel arrives, the item is inside the packaging, along with an invoice. The LLM reply is the same."

```python
data = response.json()
answer = data["choices"][0]["message"]["content"]     # the item
finish = data["choices"][0]["finish_reason"]          # did it finish?
usage = data["usage"]                                 # the invoice
```

> "`usage` gives `prompt_tokens` and `completion_tokens` — plug them into 13.1's cost formula and you know exactly what that one answer cost."

### 🔴 The trap / highest-value moment
> "Check `finish_reason`. `'stop'` means the model finished. `'length'` means it hit `max_tokens` and was chopped — the partner sees 'Your payout is credited every' and nothing else. Write this down: *finish_reason 'length' means the answer was cut off.*"

---

## Practical Block 3: Live Coding Demo (TA Code) (12 min)

**Handoff line (must match TA code file's opening comment):** "Time to send our partner's payout question to a real LLM — safely, from our own Python code."

Hand off to `ta-code - Session 13.2 - Calling LLMs with APIs.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Load the key from `.env` — show only the first 10 characters on screen
2. Send the system + user messages — show status code 200
3. Parse the answer, `finish_reason` and token usage
4. Continue the conversation by appending the assistant reply and a new user message — point out that input tokens went up
5. Run the `ask_llm()` helper with retry-and-backoff
6. Send a fake key on purpose — show the 401 and say, "this is the one you never retry"

💬 Expect a question: "The answer said payouts come on a certain day — is that right?" Welcome it. Say: "Great catch. It has never seen our helpdesk's payout policy. It's guessing — confidently. That's 13.1's hallucination trap, live. RAG in 17.1 is the fix."

---

## Concept Block 6: Errors & Rate Limits (10 min)

> "At a busy railway ticket counter, three things can go wrong: 'wrong form' — your mistake; 'too many people, come back in two minutes' — wait and retry; 'counter closed' — their problem, try later."

Write on the board:

> 200 success · 400 bad body (fix) · 401 bad key (fix) · 402 no credits (top up)
> 429 rate limit (wait, retry) · 500/502/503 provider trouble (wait, retry)

> "A **rate limit** caps requests or tokens per minute. On payout Friday evening, when every partner checks at once, we *will* hit 429s. The fix is **exponential backoff**: wait 1 second, then 2, then 4, then give up."

### 🔴 The trap / highest-value moment
> "The lazy fix is `while True: try again`. Retrying a 401 forever never succeeds, and retrying a 429 instantly makes the rate limit worse. Write this down: *retry only what can fix itself — 429 and 5xx — with growing waits and a maximum number of tries.*"

---

## Practical Block 4: Retry or Fix? (7 min)

Rapid fire around the room, five seconds each, "retry" or "fix": a 429 at 9:05 pm on payout Friday (retry with backoff); a 401 right after rotating your key (fix — `.env` still has the old key); a 503 from the provider (retry); a 400 saying `messages` must be a list (fix the body); a 402 (fix — top up credits); a request hanging for two minutes (fix — add a `timeout`, then retry). If someone asks what happens when the 429s never stop, say that's not a burst any more — you're over your plan's limit, so slow your own traffic, queue requests or upgrade.

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| Picking a provider | Smallest model that passes your tests; OpenRouter switches by one string |
| API keys | `.env` + `python-dotenv` + `.gitignore`; never print the full key |
| Raw calls | URL + Bearer header + JSON body; always set `max_tokens` and `timeout` |
| Message structure | system = rules, user = person, assistant = past replies; resend the whole list |
| Parsing | `choices[0].message.content`, check `finish_reason`, read `usage` for cost |
| Errors & rate limits | Retry 429/5xx with backoff; fix 400/401/402 |

Close on the thesis line: "An LLM API call is just a courier parcel — address, ID slip and contents — and a professional sends it with the key hidden, the rules in the system message, a cap on the reply, and a plan for when the counter says 'come back later.'"

**Bridge to next session:** "Today the model answered — but did it answer well? Session 14.1 — Prompt Engineering & Reasoning — uses this exact `ask_llm()` helper to compare zero-shot, few-shot and chain-of-thought prompts on a small test set, so you can prove which prompt is better instead of hoping."

---

## Q&A & Doubt Solving (4 min)

**Q: Is OpenRouter free?**
→ It's pay-as-you-go, and it lists some free model variants (often ending in `:free`) with stricter rate limits. Those are fine for class; production would use a paid model.

**Q: Why not use the OpenAI Python library instead of `requests`?**
→ You can, and we will from Session 14.3. Starting raw means you understand exactly what any library sends for you, which makes debugging much easier.

**Q: Does the system message guarantee the model follows the rules?**
→ No — it strongly influences it but doesn't guarantee it. That's why we test prompts in 14.1 and add guardrails in 18.1.

**Q: Can I keep the conversation history forever?**
→ Only until it fills the context window, and you pay for every resent token. Real apps trim or summarise old messages; we'll see summarisation chains in 15.2.

**Q: What if I accidentally commit my `.env` file?**
→ Revoke the key on the provider's site immediately and create a new one. Deleting the file in a later commit isn't enough — it's still in Git history.

---

## Instructor Notes
- **Words not yet earned:** few-shot and chain-of-thought (14.1), Pydantic and structured output (14.3), LangChain and chains (15.1), embeddings (16.2), prompt injection (name only — 18.1).
- **Biggest risk in this session:** setup friction — `.env` not loading, typos in the key, the wrong folder. Show a working `.env` on screen before the break and have the TA ready to troubleshoot.
- **Board management:** keep the three-step key pattern and the status-code list visible from Concept Block 2 to the end.
- **Common confusions, numbered:**
  1. Thinking a private repo makes a hard-coded key safe
  2. Expecting the model to remember earlier calls without resending messages
  3. Putting the rules in the user message instead of the system message
  4. Ignoring `finish_reason == "length"`
  5. Retrying every error, including 400 and 401
- **Cross-references:** Session 14.1 reuses `ask_llm()`; Session 14.3 switches to the OpenAI client patched with instructor; Session 15.1 wraps this call in `ChatOpenAI`; Session 18.1 covers prompt injection and privacy.
- **Local/cultural context notes:** the UPI-PIN and railway-counter analogies land well; keep the Hindi and Hinglish messages in the practical blocks — the multilingual angle makes message structure feel real for this cohort.
