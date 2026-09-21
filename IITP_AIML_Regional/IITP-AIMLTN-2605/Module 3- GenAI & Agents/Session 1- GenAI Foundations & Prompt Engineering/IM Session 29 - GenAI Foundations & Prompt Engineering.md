# Instructor Reference: Session 12.1 — GenAI Foundations & Prompt Engineering
90 min | 75 min teaching + 5 min break + 10 min coding practice
Domain: Coding
Tools / Dataset: `support_tickets.csv` (40 support tickets, 6 categories) in the `Datasets` folder; companion notebook `IM Session 29 - GenAI Foundations & Prompt Engineering.ipynb`. Python, pandas, scikit-learn. **No API key, no network, no cost.**
Prior knowledge: Students have completed Module 2 end to end — regression through PCA, model selection and persistence (11.2). They have trained and evaluated their own classifiers, and know train/test splits, accuracy and stratification.
Next session: LLM APIs, Integration & Ethics

**LMS:** IM Session 29 · Lecture ID 166774 · Thu 3 Sept, 8:00 pm

---

## Pre-Class Setup

> Run before class — students never see this.

Open the companion notebook and **Run All**. Every cell must complete with no error. Confirm these five numbers,
because the whole session is built on them:

```
characters per token across the corpus : 3.38
average ticket = 27.7 tokens | longest ticket = 47 tokens
all 40 tickets            : 1107 tokens
temperature 0.2  -> mrd=0.99  history=0.01  ?=0.00  .=0.00
strategy         user_tokens  total_with_system
zero_shot                 31                145
few_shot                 279                393
chain_of_thought          82                196
```

Have the notebook open at Part 3 before you start — the temperature demo is the moment the session turns, and
you do not want to be scrolling for it.

---

## Opening & Problem Framing `(10 min)`

**Hook** `(2-3 min)`
Ask: "Last session you finished Module 2. Every model you built, you trained yourself — you chose the features,
you saw the coefficients, you could point at exactly why it predicted what it predicted. Today you start using a
model with **billions** of parameters that you did not train, cannot inspect, and cannot retrain. So: what is
left to control?"

Let 2–3 answers land. Then reveal: the answer is the **words you send it**, and that is the entire discipline of
prompt engineering. It sounds soft. It is not — by the end of today they will be measuring prompts in tokens and
rupees.

**Bridge from prior session** `(1-2 min)`
Say: "Last session we did Model Selection, Persistence & Module Review — you closed out classical ML. Today we
open Module 3 with the models you steer instead of train."

| Prior sessions | Today |
|---|---|
| You trained the model on your data | Someone else trained it; you steer it with words |
| Control came from features and hyperparameters | Control comes from the context you send |
| A wrong answer meant retrain or tune | A wrong answer means change the prompt or ground the input |
| Cost was compute time | Cost is tokens, billed per request |

**Real-world relevance** `(2-3 min)`
Instructor picks 2–3 to say aloud; the list is reference only.
- Support desks triage and draft replies with LLMs, keeping a human on anything consequential.
- Banks summarise long policy documents into agent-facing answers — with strict grounding rules.
- E-commerce teams generate product descriptions at a scale no copywriting team could match.
- Healthcare scribes draft consultation notes for a clinician to approve, never to file directly.
- Every one of these is a prompt plus a guardrail, which is precisely today plus next session.

**Session promise** `(30 sec)`
Say: "By the end of today you'll be able to count the tokens in any prompt, explain why an LLM hallucinates in
one sentence, and build and price zero-shot, few-shot and chain-of-thought prompts for our ticket dataset."

---

### SEGMENT 1 — Tokens and the Context Window `(14 min)`

> Instructor note: Students have used `train_test_split` and pandas aggregation since Module 1. Do not re-explain
> either — use them and move on.

**Concept** `(4 min)`
Analogy — a courier charges by parcel, not by what is written inside. A model charges by **token**, not by
meaning. Ask a room of students to guess how many tokens `"immediately"` costs; the guesses will vary wildly,
which is the point.
Formal definition: a **token** is a sub-word unit — common words are one token, rarer or longer words split into
several. The **context window** is the maximum number of tokens the model can hold at once, and it is shared by
your instructions, your data *and* the reply.

**Implementation / Demonstration** `(7 min)`
Run the tokenizer cell:

```python
demo = "I was charged twice for the same order. Please reverse one immediately."
print(tokenize(demo))
```
```
['I', 'was', 'char', 'ged', 'twic', 'e', 'for', 'the', 'same', 'orde', 'r', '.',
 'Plea', 'se', 'reve', 'rse', 'one', 'imme', 'diat', 'ely', '.']
count  : 21
```

Say: eleven words became twenty-one tokens. Be explicit that ours is a **teaching approximation**, not the real
byte-pair encoder — the intuition transfers, the exact count must come from the provider's tokenizer.

Then the corpus stats and the budget table:

```
characters per token : 3.38      tokens per word : 1.75
average ticket = 27.7 tokens | longest ticket = 47 tokens

         window  usable_tokens  tickets_if_average  tickets_if_all_worst_case
0    small (8K)           6980                 252                        148
1  medium (32K)          30980                1119                        659
2  large (128K)         126980                4588                       2701
```

Ask: "Which column do you size your batch on?" Let someone say *average*, then point at the 252 vs 148 gap. That
gap is the job that worked in testing and silently truncated in production.

**Key point**
**The context window is a hard budget shared by your instructions, your data and the reply — and you plan it against the worst-case item, never the average.**

**Student try** `(3 min)`
Task: compute the token count of your own name plus your college name using `count_tokens()`. Then predict, before
running it, whether `"Thiruvananthapuram"` costs more tokens than `"Chennai"` — and by how many.

---

### SEGMENT 2 — Probabilistic Generation and Hallucination `(14 min)`

**Concept** `(4 min)`
Analogy — predictive text on a phone keyboard, scaled up enormously. It does not know what you mean to say; it
knows what usually comes next.
Formal definition: at each step the model produces a **probability distribution over the next token** and samples
from it. **Temperature** reshapes that distribution before sampling — low sharpens it, high flattens it.
Connect to prior knowledge: they have seen `predict_proba` on a classifier. This is the same idea, applied to a
vocabulary of thousands, once per token.

**Implementation / Demonstration** `(7 min)`
Show the real bigram counts built from the ticket corpus:

```
What actually follows 'order' in this corpus:
   mrd          5
   history      2
   ?            1
```

Say: **that table is a next-token distribution, learned from our data.** Then the temperature sweep:

```
temperature 0.2  -> mrd=0.99  history=0.01  ?=0.00  .=0.00
temperature 1.0  -> mrd=0.36  history=0.14  ?=0.07  .=0.07
temperature 2.0  -> mrd=0.21  history=0.13  ?=0.09  .=0.09
```

Say: same model, same data — only the sampling rule changed. At 0.2 it will say the same thing every time; at 2.0
unlikely tokens become live options.

Now generate and read one aloud:
```
[temp 1.0] order . k @ example . this needs immediate attention . how do i want
```

Ask: "Is this true?" It is grammatical, on-topic, uses the right vocabulary — and describes nothing that ever
happened. **Nothing malfunctioned.** It was asked for likely tokens and gave likely tokens. Land it: fluency is
evidence of a good language model, never evidence of a true statement.

**Key point**
**A hallucination is the system working exactly as designed, applied to a question that needed a fact — you fix it by changing the inputs and the checks, not by asking the model to try harder.**

**Student try** `(3 min)`
Task: run `generate("delivery", temperature=1.5)` twice. Write one sentence explaining why the two outputs differ
even though nothing about the model changed.

---

### SEGMENT 3 — Prompt Anatomy: System, Zero-shot, Few-shot, CoT `(12 min)`

**Concept** `(4 min)`
Analogy — a new hire's job description versus today's ticket. The **system prompt** is the standing brief: role,
rules, output format. The **user prompt** is this one request. Putting standing rules in the user prompt is like
re-reading someone their job description before every single task — expensive, and it does not outrank what the
customer just said.

**Implementation / Demonstration** `(5 min)`
Show the system prompt (114 tokens, paid on every request), then the three strategies and their real cost:

```
strategy         user_tokens  total_with_system
zero_shot                 31                145
few_shot                 279                393
chain_of_thought          82                196
```

Say: few-shot is **nine times** the user-prompt cost of zero-shot, because every example is re-sent every time.
Chain-of-thought is cheap to send and expensive to receive — the reasoning comes back as output tokens.

Then the honest experiment. Be careful and explicit here:

```
means:  curated_keywords 0.69   raw_examples 0.46   both 0.58
```

Say: on this keyword matcher, curated descriptions beat three raw examples per category on **all five splits** —
and adding examples to the curated text made it *worse*. State the caveat plainly: **this is TF-IDF cosine
similarity, not an LLM**, so it is not evidence about how few-shot performs on GPT or Gemini. What it does show
is narrower and still useful — a longer context is not automatically a better context, because real tickets are
mostly words that carry no category signal.

**Key point**
**Before you pay to send more context, check that what you are sending carries signal — and for a real model, measure it rather than assuming.**

**Student try** `(3 min)`
Task: rewrite the system prompt to also return a priority (`high`/`medium`/`low`), then use `count_tokens()` to
report how many extra tokens per request your version costs.

---

--- BREAK (5 min) ---

---

## Building Programs `(15 min)`

### Program 1: Token budget checker `(5 min)`

Purpose: turn the context window from an abstract limit into a go/no-go check.

```python
def fits_in_window(texts, window=8000, overhead=220, reserve=800):
    total = sum(count_tokens(t) for t in texts) + overhead + reserve
    return {"tokens_needed": total, "window": window,
            "fits": total <= window, "headroom": window - total}

print(fits_in_window(tickets["ticket_text"]))
print(fits_in_window(tickets["ticket_text"], window=1500))
```
```
{'tokens_needed': 2127, 'window': 8000, 'fits': True, 'headroom': 5873}
{'tokens_needed': 2127, 'window': 1500, 'fits': False, 'headroom': -627}
```

Say: the second line is what you want to discover *before* the batch runs, not from a truncated result afterwards.

### Program 2: Temperature comparison `(5 min)`

Purpose: make the determinism/variety trade-off something they have seen with their own eyes.

```python
for temp in [0, 0.7, 1.5]:
    outs = {generate("order", n=8, temperature=temp) for _ in range(3)}
    print(f"temp {temp}: {len(outs)} distinct output(s) from 3 runs")
```
```
temp 0: 1 distinct output(s) from 3 runs
temp 0.7: 3 distinct output(s) from 3 runs
temp 1.5: 3 distinct output(s) from 3 runs
```

Say: temperature 0 is the right default for classification and extraction — same input, same answer, every time.

### Program 3: Prompt cost calculator `(5 min)`

Purpose: connect prompt design to a number a manager cares about.

```python
def daily_cost(strategy_tokens, volume=5000, rate_per_1k=0.00015):
    tokens = strategy_tokens * volume
    return {"tokens_per_day": tokens, "usd_per_day": round(tokens / 1000 * rate_per_1k, 2)}

for _, r in cost.iterrows():
    print(f"{r['strategy']:<18}", daily_cost(r["total_with_system"]))
```
```
zero_shot          {'tokens_per_day': 725000, 'usd_per_day': 0.11}
few_shot           {'tokens_per_day': 1965000, 'usd_per_day': 0.29}
chain_of_thought   {'tokens_per_day': 980000, 'usd_per_day': 0.15}
```

Say: rates are illustrative placeholders — always check current pricing. The *ratio* is the durable lesson:
few-shot costs roughly 2.7× zero-shot here, every day, forever. It must earn that.

---

## Common Mistakes `(10 min)`

**Mistake 1: Estimating tokens by counting words**
Wrong: "The ticket is 16 words, so about 16 tokens."
Right: Measure it — 16 words came to 27.7 tokens on average here, about 1.75 tokens per word.
Why it matters: A 75% under-estimate turns into truncated inputs and a bill nobody forecast.

**Mistake 2: Treating hallucination as a defect to be scolded out**
Wrong: Adding "do not hallucinate" or "only tell the truth" to the prompt and considering it handled.
Right: Ground the model in retrieved source text, constrain the output so it can be checked, keep a human on consequential calls.
Why it matters: The model has no notion of truth to appeal to — instruction alone cannot supply one.

**Mistake 3: Putting standing rules in the user prompt**
Wrong: Repeating the full role, format and refusal rules inside every user message.
Right: Standing behaviour goes in the system prompt; the user prompt carries only this turn's request and data.
Why it matters: You pay for the repetition on every request, and the rules no longer clearly outrank user text.

**Mistake 4: Assuming more examples always help**
Wrong: "Accuracy is low, so let me paste in ten more examples."
Right: Measure it. On our matcher, adding verbose examples cut accuracy from 0.69 to 0.58.
Why it matters: Signal dilution is real, and unmeasured context growth costs money while making things worse.

**Mistake 5: Using a high temperature for classification**
Wrong: Leaving temperature at 1.0 for a triage task, then reporting inconsistent accuracy.
Right: Temperature 0 for classification and extraction; raise it only where variety is the goal.
Why it matters: You cannot debug a pipeline whose answers change between identical runs.

**Mistake 6: Believing the teaching tokenizer is the real one**
Wrong: Quoting our token counts as production figures.
Right: Use ours for intuition; get real counts from the provider's tokenizer before you budget.
Why it matters: Confidently wrong numbers in a costing document are worse than admitting you have not measured yet.

---

## Session Recap

| Topic | What to remember |
|---|---|
| Tokens | Sub-word units — ~3.4 characters each on our corpus, ~1.75 per word. Never estimate by word count |
| Context window | A hard budget shared by instructions, data and reply. Plan against the worst case |
| Probabilistic generation | The model samples from a next-token distribution; temperature reshapes it |
| Hallucination | The mechanism working normally on a question needing a fact — fix the inputs and checks |
| System vs user prompt | Standing rules in system, this turn's request in user |
| Strategy cost | Few-shot cost 9× zero-shot's user tokens here; verbose context can reduce accuracy |

Path forward: "Next session: LLM APIs, Integration & Ethics — today we wrote prompts by hand and priced them; next session the same triage job runs programmatically, which brings keys, retries, and guardrails."

---

## Coding Practice `(10 min)`

**Question**: Write `compare_prompts(ticket)` that builds all three prompt strategies for a given ticket and
returns a DataFrame with the strategy name, its user token count, and its total cost including the system prompt.
Run it on `TKT-1011` and state which strategy you would ship for a 5,000-ticket-per-day pipeline, and why.

**Expected solution**:

```python
def compare_prompts(ticket):
    strategies = {
        "zero_shot": zero_shot(ticket),
        "few_shot": few_shot(ticket, examples),
        "chain_of_thought": chain_of_thought(ticket),
    }
    return pd.DataFrame([
        {"strategy": name,
         "user_tokens": count_tokens(p),
         "total_with_system": count_tokens(SYSTEM_PROMPT) + count_tokens(p)}
        for name, p in strategies.items()
    ])

t = tickets.loc[tickets["ticket_id"] == "TKT-1011", "ticket_text"].iloc[0]
print(compare_prompts(t))
```
```
           strategy  user_tokens  total_with_system
0         zero_shot           38                152
1          few_shot          286                400
2  chain_of_thought           89                203
```

Expected answer: **zero-shot**, unless few-shot can be shown to buy accuracy worth 2.6× the token cost every day.
Accept any answer that (a) cites the token numbers and (b) says the decision needs a measured accuracy comparison
rather than an assumption — that reasoning is the point, not the specific choice.
