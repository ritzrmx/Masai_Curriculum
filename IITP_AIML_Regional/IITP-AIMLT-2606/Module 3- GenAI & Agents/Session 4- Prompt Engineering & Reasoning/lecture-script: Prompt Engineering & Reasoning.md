# Lecture Script: Prompt Engineering & Reasoning
> **Instructor Reference** — Module 3: GenAI & Agents | Session 4 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students design effective zero-shot and few-shot prompts using role prompting, apply chain-of-thought reasoning to improve multi-step problem solving, and evaluate/iteratively refine prompts against a defined test set with structured failure analysis.

**Student profile at this point:** Comfortable making raw OpenRouter API calls (Session 2) and now has the conceptual/mathematical foundation for tokens, temperature, and vector similarity (Sessions 1 and 3). Has not yet been taught any deliberate PROMPT DESIGN technique — has been writing simple, ad-hoc prompts so far. This session is the first time "how you phrase the prompt" becomes the explicit subject, not a side note.

**Key outcome:** Every student can write a zero-shot prompt, upgrade it to a few-shot prompt with well-chosen examples, apply role prompting, apply chain-of-thought prompting to a multi-step reasoning problem, and run a small test set of 3-5 cases through a prompt to systematically identify and fix a failure mode — producing a "before vs. after" comparison with concrete evidence.

**Dataset for this session:** None required from disk — a small inline test set of 4-5 example inputs (built live in SEGMENT 5) serves as this session's "dataset," kept in code, not a CSV file.

**API note for this script:** All example prompts are written to be correct and directly runnable against OpenRouter (from Session 2's `ask_llm()` pattern). All example LLM OUTPUTS are marked **"Example output (illustrative — actual LLM output will vary run to run)"** since this script is not executed against a live paid key and LLM text generation is inherently non-deterministic.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Why the Same Model Gives Different Quality Answers | 10 min | 0:10 |
| SEGMENT 2: Zero-Shot vs. Few-Shot Prompting | 25 min | 0:35 |
| SEGMENT 3: Role Prompting | 15 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 4: Chain-of-Thought Reasoning | 25 min | 1:25 |
| SEGMENT 5: Building a Test Set & Failure Analysis | 20 min | 1:45 |
| SEGMENT 6: Lab — Iteratively Refine a Prompt Against a Test Set | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Why the Same Model Gives Different Quality Answers (10 min)

### The Hook (5 min)

**Say:** *"Same model, same OpenRouter account, same day. Two different prompts, two wildly different quality answers to essentially the same underlying question. Let's see this live before we name any technique."*

**Live-code two contrasting prompts (using the `ask_llm()` helper built last session):**

```python
weak_prompt = "Is this email spam? 'Congratulations! You've won a $1000 gift card, click here now!!!'"

strong_prompt = """You are a spam-detection assistant for an email client.
Classify the following email as SPAM or NOT_SPAM. Respond with only the label.

Email: "Congratulations! You've won a $1000 gift card, click here now!!!"

Label:"""

print("Weak prompt result:", ask_llm(weak_prompt))
print("Strong prompt result:", ask_llm(strong_prompt))
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Weak prompt result: This email shows several classic signs of spam, including urgency, an unrealistic prize offer, and a suspicious call to action ("click here now"). It's very likely spam, though I can't be 100% certain without more context like the sender's address and links.
Strong prompt result: SPAM
```

**Say:** *"Both answers are 'correct' in the sense that both correctly identify this as spam. But look at the difference in USABILITY. The weak prompt's answer is a paragraph of hedged prose — if you wanted to plug this into a real email filter that needs to programmatically decide 'move to spam folder: yes/no,' you'd now have to parse THAT paragraph to extract a decision, which is fragile and error-prone. The strong prompt's answer is exactly one word, ready to use directly in an `if` statement. Nothing about the MODEL changed between these two calls — only the PROMPT did. That's the entire subject of today's session."*

### Why This Session Matters (5 min)

**Say:** *"Prompt engineering is not 'talking nicely to a chatbot.' It's a systematic, testable discipline — you form a hypothesis about what phrasing will help, you test it against real examples, you measure whether it actually helped, and you iterate. By the end of today you'll do exactly that full loop, with real evidence, not just vibes."*

**Learning contract for today — write on board:**

- Write and compare zero-shot vs. few-shot prompts
- Apply role prompting to shape a model's behavior and tone
- Apply chain-of-thought prompting to improve multi-step reasoning
- Build a small test set and use it to systematically refine a prompt

---

## SEGMENT 2: Zero-Shot vs. Few-Shot Prompting (25 min)

### Zero-Shot — Just Ask (6 min)

**Say:** *"Zero-shot prompting means you ask the model to do a task with ZERO examples of what a correct answer looks like — just an instruction. This is what both prompts in the opening demo were, technically — even the 'strong' one had zero worked examples, just clearer instructions. Zero-shot works surprisingly well for tasks the model has seen enormous amounts of during training — general knowledge questions, common classification tasks, well-known formats."*

**Live-code a zero-shot example:**

```python
zero_shot_prompt = """Classify the sentiment of this review as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only the label.

Review: "The battery life is decent but the screen scratches way too easily."

Label:"""

print(ask_llm(zero_shot_prompt))
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
NEGATIVE
```

**Say:** *"Reasonable answer — this review is mixed but leans negative overall, focused more on the complaint. Zero-shot got us a clean, usable answer here. But zero-shot starts to struggle when the task has a NON-obvious rule, a specific format you need followed exactly, or edge cases that are genuinely ambiguous without a worked example to anchor the model's judgment."*

### Few-Shot — Show, Don't Just Tell (12 min)

**Say:** *"Few-shot prompting adds a small number of worked EXAMPLES — input paired with the correct output — directly in the prompt, before your real question. The model uses these examples as a pattern to follow, without any retraining. This is one of the most powerful, cheap techniques in prompt engineering, precisely because it requires no fine-tuning, no new model — just more careful prompt construction."*

**Say:** *"Let's build a case where zero-shot genuinely struggles: classifying customer support tickets by urgency, using a company-specific rule that isn't standard knowledge — 'any mention of a competitor switching threat is automatically HIGH urgency, even if the tone is calm.'"*

**Live-code the zero-shot version first, showing the failure:**

```python
zero_shot = """Classify this support ticket's urgency as LOW, MEDIUM, or HIGH.
Respond with only the label.

Ticket: "Just a heads up, we're evaluating a couple of other vendors for next quarter. No rush on this, take your time."

Label:"""

print("Zero-shot:", ask_llm(zero_shot))
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Zero-shot: LOW
```

**Say:** *"A plausible, but for THIS company's rules, WRONG answer — the calm tone ('no rush') misleads a zero-shot model into missing the buried competitor-switching signal, which this company treats as an automatic HIGH regardless of tone. This is a company-specific business rule; there's no way the model could know it without being shown."*

**Now live-code the few-shot version:**

```python
few_shot = """Classify each support ticket's urgency as LOW, MEDIUM, or HIGH.
IMPORTANT: any mention of considering a competitor or vendor switch is automatically HIGH, regardless of tone.

Ticket: "The dashboard has been loading a bit slowly this week."
Urgency: LOW

Ticket: "We can't process any payments right now, this is blocking our whole team."
Urgency: HIGH

Ticket: "Loving the product so far, just curious if you support SSO login."
Urgency: LOW

Ticket: "Just a heads up, we're evaluating a couple of other vendors for next quarter. No rush on this, take your time."
Urgency:"""

print("Few-shot:", ask_llm(few_shot))
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Few-shot: HIGH
```

**Say:** *"There it is. The few-shot examples didn't just show the FORMAT (label after 'Urgency:') — the explicit rule plus the pattern of examples anchored the model onto the specific, non-obvious business logic. This is the core value of few-shot prompting: encoding rules and edge-case handling that zero-shot instructions alone often miss, especially when the correct behavior isn't 'common sense' but a specific policy."*

### How Many Examples, and How to Choose Them (5 min)

**Say:** *"How many examples is 'few'? Typically 2-8 in practice — enough to establish the pattern and cover the important edge cases, not so many that you burn excessive tokens (remember, EVERY example counts against the context window and your bill, from Sessions 1 and 2) or dilute the pattern with redundant examples."*

**Say:** *"Choosing WHICH examples matters as much as how many. Good few-shot examples: cover the range of possible labels/outputs (don't show 5 examples that are all HIGH), include at least one edge case similar to what commonly gets misclassified (like our competitor-mention example), and stay consistent in format with each other and with your final unlabeled query. This selection problem — 'which past examples are most relevant/similar to this new case?' — is, incidentally, exactly the kind of problem cosine similarity from last session is built to solve at scale, when you have hundreds of possible examples to choose from instead of a handful you pick by hand."*

### Comprehension Check (2 min)

1. *"What's the main risk of using TOO MANY few-shot examples in a prompt?"* (Wastes tokens/cost and context-window space, and may dilute the pattern if examples aren't well-chosen — more isn't automatically better.)
2. *"Would few-shot prompting help a model follow a highly company-specific rule better than zero-shot? Why?"* (Yes — worked examples can encode specific rules or edge cases that plain instructions alone may not reliably convey, especially ones that aren't "common sense.")

---

## SEGMENT 3: Role Prompting (15 min)

### What Role Prompting Actually Does (6 min)

**Say:** *"Role prompting means assigning the model a specific persona or professional identity, usually via the `system` message from Session 2 — 'You are a senior tax accountant,' 'You are a patient elementary school teacher,' 'You are a terse, no-nonsense code reviewer.' This shapes the STYLE, tone, vocabulary, and sometimes the depth/rigor of the response, by conditioning the model on patterns it learned from text written by or about people in that role."*

**Live-code a side-by-side role comparison, same question, different roles:**

```python
question = "Why does my code throw a KeyError when I access a dictionary?"

casual_role = "You are a friendly, encouraging coding buddy explaining things to a total beginner."
expert_role = "You are a terse senior backend engineer doing a rapid-fire code review. No pleasantries."

casual_reply = ask_llm(question, system_message=casual_role)
expert_reply = ask_llm(question, system_message=expert_role)

print("Casual role:", casual_reply)
print("Expert role:", expert_reply)
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
Casual role: No worries, this happens to everyone when they're starting out! A KeyError means you tried to grab a key from a dictionary that doesn't actually exist in it -- kind of like asking for a book on a shelf that was never put there. Try using `.get("your_key")` instead, which returns None instead of crashing if the key's missing. You've got this!

Expert role: KeyError = accessed a nonexistent dict key. Use `.get(key, default)` or check `if key in d` first. Check for typos in the key name or upstream data not populating it.
```

**Say:** *"Same underlying technical content, same underlying model — genuinely different length, tone, and vocabulary, driven entirely by the system message. This is a powerful, low-cost lever: choosing the right role for your application's audience (a customer-facing chatbot vs. an internal engineering tool) can meaningfully change user experience without touching the model itself."*

### Role Prompting's Real Limits (5 min)

**Say:** *"Important honesty check: role prompting changes STYLE far more reliably than it changes underlying FACTUAL ACCURACY or reasoning CAPABILITY. Telling a model 'You are a world-class mathematician' does not actually make its arithmetic more correct — the model doesn't gain new computational ability from a persona label. Where role prompting genuinely helps accuracy is narrower: it can nudge the model toward using more appropriate vocabulary, applying relevant domain conventions, or adopting a more careful, formal register that happens to correlate with more careful answers — but it is not a substitute for techniques that actually improve REASONING, which is exactly where chain-of-thought comes in after the break."*

**Ask:** *"If you told a model 'You are a Nobel Prize-winning physicist' before asking it to solve a tricky physics problem, would you expect that framing alone to guarantee a correct answer?"* Guide toward: no — it might shift tone/vocabulary toward more technical, formal language, but the underlying reasoning quality depends on the model's actual capability and how the PROBLEM itself is presented, not the persona label alone.

### Comprehension Check (4 min)

1. *"Where in an OpenRouter request does a role prompt typically go?"* (In the `system` message, usually the first entry in the `messages` list.)
2. *"Is role prompting mainly a lever for style/tone, or for factual accuracy?"* (Mainly style, tone, and vocabulary — it is not a reliable lever for improving factual accuracy or reasoning quality on its own.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to try mentally solving this multi-step word problem without writing anything down: "A store had 120 apples. They sold 35% in the morning and then 40 more in the afternoon. How many apples are left?" Come back ready to see how a prompting technique changes whether an LLM gets this right.

---

## SEGMENT 4: Chain-of-Thought Reasoning (25 min)

### The Problem — Jumping Straight to an Answer (6 min)

**Say:** *"Let's test the apple problem from the break, directly, with a prompt that asks ONLY for the final number."*

**Live-code:**

```python
direct_prompt = """A store had 120 apples. They sold 35% in the morning and then 40 more in the afternoon.
How many apples are left? Respond with only the final number."""

print(ask_llm(direct_prompt, temperature=0.7))
```

**Example output (illustrative — actual LLM output will vary run to run; models CAN get simple multi-step arithmetic like this right, but asking for an immediate bare answer with no reasoning shown measurably increases the rate of silent arithmetic slips on problems with several sequential steps):**
```
34
```

**Say:** *"Let's check that by hand. 35% of 120 is 42, so 120 - 42 = 78 remain after the morning. Then 78 - 40 = 38 remain after the afternoon. The correct answer is 38 — the illustrative output above, 34, is wrong, and this is a realistic type of mistake worth understanding: when a model jumps straight to a final number for a multi-step problem, it has no scratch space to carry intermediate values accurately, similar to how a person asked to do multi-step arithmetic 'in their head, silently, no fingers, no paper' is more likely to slip somewhere along the chain."*

### Chain-of-Thought — Show Your Work (10 min)

**Say:** *"Chain-of-thought (CoT) prompting asks the model to work through the problem step by step BEFORE giving a final answer — literally the equivalent of 'show your work,' which most of us were taught in school for exactly this reason: it catches errors that jumping straight to an answer hides."*

**Live-code the same problem with a CoT instruction added:**

```python
cot_prompt = """A store had 120 apples. They sold 35% in the morning and then 40 more in the afternoon.
How many apples are left?

Think through this step by step, showing each calculation, then give your final answer
on a new line starting with "Final answer:"."""

print(ask_llm(cot_prompt, temperature=0.7))
```

**Example output (illustrative — actual LLM output will vary run to run, but this is the realistic SHAPE and typically-improved reliability CoT produces on this kind of problem):**
```
Step 1: Find 35% of 120 apples sold in the morning.
35% of 120 = 0.35 x 120 = 42 apples sold in the morning.

Step 2: Find how many apples remain after the morning.
120 - 42 = 78 apples remaining.

Step 3: Subtract the 40 apples sold in the afternoon.
78 - 40 = 38 apples remaining.

Final answer: 38
```

**Say:** *"Now it matches our hand calculation exactly: 38. Notice WHY this tends to help: by writing out `35% of 120 = 42` as an explicit intermediate step, the model has that number available as literal TEXT in its own generated output for the next step to build on, rather than needing to have gotten the whole multi-step computation right silently in one shot. Remember from Session 1: generation is sequential, token by token, each new token conditioned on everything generated so far — so an explicit correct intermediate step becomes part of the context the NEXT step is conditioned on, which is genuinely useful scaffolding, not just a cosmetic difference."*

### Zero-Shot CoT — The "Let's Think Step by Step" Trick (5 min)

**Say:** *"There's an even simpler version of this technique, sometimes called zero-shot chain-of-thought: you don't need to design worked examples at all — often just appending a phrase like 'Let's think step by step' or 'Show your reasoning before answering' to an otherwise plain prompt is enough to trigger this same step-by-step behavior."*

**Live-code:**

```python
simple_cot_prompt = """A train travels 60 km in the first hour and then increases its speed
by 20 km/h for the next 2 hours. What is the total distance traveled?

Let's think step by step."""

print(ask_llm(simple_cot_prompt))
```

**Example output (illustrative — actual LLM output will vary run to run):**
```
First hour: the train travels 60 km.
For the next 2 hours, the speed increases by 20 km/h, so the new speed is 60 + 20 = 80 km/h.
Distance for those 2 hours: 80 km/h x 2 hours = 160 km.
Total distance: 60 km + 160 km = 220 km.
```

**Say:** *"Four words — 'Let's think step by step' — appended to an otherwise plain prompt, and the model structured its own reasoning without us hand-writing any worked examples at all. This costs almost nothing extra and is one of the highest 'value per word added' techniques in this entire session."*

### When NOT to Use Chain-of-Thought (4 min)

**Say:** *"CoT isn't free — it generates more output tokens (more reasoning text before the final answer), which costs more and takes longer to generate, connecting back to Session 1's token-cost discussion. For simple, single-step lookups or classifications — like our earlier spam or sentiment examples — CoT usually adds cost without adding accuracy, since there's no multi-step reasoning chain to benefit from. Reserve it specifically for problems with several sequential logical or arithmetic steps, where an early error would otherwise silently propagate through to a wrong final answer."*

**Ask:** *"Would chain-of-thought likely help our earlier spam classification example from SEGMENT 1? Why or why not?"* Guide toward: probably not much — spam/not-spam is close to a single-step judgment call, not a multi-step calculation, so the main benefit CoT provides (catching errors across sequential steps) doesn't really apply there.

---

## SEGMENT 5: Building a Test Set & Failure Analysis (20 min)

### Why "It Worked Once" Isn't Enough (5 min)

**Say:** *"Every demo so far in this session showed ONE example working. That is not how you should evaluate a prompt in a real project — a prompt that works on one hand-picked example can still fail badly on realistic variety. The discipline here is: build a small TEST SET of representative cases up front, including tricky edge cases, run your prompt against ALL of them, and look systematically at where it fails before calling a prompt 'done.'"*

### Building a Small Test Set, Live (7 min)

**Say:** *"Let's build a 5-case test set for our urgency classifier from SEGMENT 2, this time including cases specifically chosen to probe known trouble spots — not just easy, obvious cases."*

**Live-code:**

```python
test_cases = [
    {"ticket": "The dashboard has been loading a bit slowly this week.", "expected": "LOW"},
    {"ticket": "We can't process any payments right now, this is blocking our whole team.", "expected": "HIGH"},
    {"ticket": "Loving the product so far, just curious if you support SSO login.", "expected": "LOW"},
    {"ticket": "Just a heads up, we're evaluating a couple of other vendors for next quarter. No rush on this.", "expected": "HIGH"},
    {"ticket": "Getting occasional timeout errors during our busiest hour, happening a few times a day.", "expected": "MEDIUM"},
]

def classify_urgency(ticket_text, prompt_template):
    full_prompt = prompt_template.format(ticket=ticket_text)
    return ask_llm(full_prompt).strip()
```

**Say:** *"Notice test case 4 is our known-tricky competitor-mention case from earlier, deliberately kept IN the test set — a good test set doesn't just confirm what already works, it specifically re-checks known trouble spots every time you revise a prompt."*

### Running the Test Set and Analyzing Failures (8 min)

**Live-code, running the ORIGINAL zero-shot prompt (no few-shot examples, no explicit rule) against all five cases:**

```python
zero_shot_template = """Classify this support ticket's urgency as LOW, MEDIUM, or HIGH.
Respond with only the label.

Ticket: "{ticket}"

Urgency:"""

correct = 0
for case in test_cases:
    result = classify_urgency(case["ticket"], zero_shot_template)
    is_correct = result == case["expected"]
    correct += is_correct
    status = "PASS" if is_correct else "FAIL"
    print(f"[{status}] expected={case['expected']:>6} got={result:>6} | {case['ticket'][:50]}...")

print(f"\nScore: {correct}/{len(test_cases)}")
```

**Example output (illustrative — actual LLM output will vary run to run, but this is a realistic pattern: the zero-shot version reliably gets the two "obvious" cases right and reliably struggles on the competitor-mention edge case, since nothing in the prompt tells it that rule):**
```
[PASS] expected=   LOW got=   LOW | The dashboard has been loading a bit slowly thi...
[PASS] expected=  HIGH got=  HIGH | We can't process any payments right now, this i...
[PASS] expected=   LOW got=   LOW | Loving the product so far, just curious if you ...
[FAIL] expected=  HIGH got=   LOW | Just a heads up, we're evaluating a couple of o...
[PASS] expected=MEDIUM got=MEDIUM | Getting occasional timeout errors during our bu...

Score: 4/5
```

**Say:** *"4 out of 5 — and crucially, the ONE failure is exactly the case we already suspected would be a problem, now confirmed with concrete evidence instead of a hunch. This is the failure-analysis discipline: don't just report a score, IDENTIFY the specific pattern in what failed. Here the pattern is clear: the model isn't applying the buried company-specific rule about competitor mentions."*

**Now live-code the FIXED prompt (few-shot with the explicit rule, from SEGMENT 2) against the same test set:**

```python
few_shot_template = """Classify each support ticket's urgency as LOW, MEDIUM, or HIGH.
IMPORTANT: any mention of considering a competitor or vendor switch is automatically HIGH, regardless of tone.

Ticket: "The dashboard has been loading a bit slowly this week."
Urgency: LOW

Ticket: "We can't process any payments right now, this is blocking our whole team."
Urgency: HIGH

Ticket: "Loving the product so far, just curious if you support SSO login."
Urgency: LOW

Ticket: "{ticket}"
Urgency:"""

correct = 0
for case in test_cases:
    result = classify_urgency(case["ticket"], few_shot_template)
    is_correct = result == case["expected"]
    correct += is_correct
    status = "PASS" if is_correct else "FAIL"
    print(f"[{status}] expected={case['expected']:>6} got={result:>6} | {case['ticket'][:50]}...")

print(f"\nScore: {correct}/{len(test_cases)}")
```

**Example output (illustrative — actual LLM output will vary run to run; this is the realistic, expected improvement pattern after adding the explicit rule and worked examples):**
```
[PASS] expected=   LOW got=   LOW | The dashboard has been loading a bit slowly thi...
[PASS] expected=  HIGH got=  HIGH | We can't process any payments right now, this i...
[PASS] expected=   LOW got=   LOW | Loving the product so far, just curious if you ...
[PASS] expected=  HIGH got=  HIGH | Just a heads up, we're evaluating a couple of o...
[PASS] expected=MEDIUM got=MEDIUM | Getting occasional timeout errors during our bu...

Score: 5/5
```

**Say:** *"5 out of 5, with concrete before/after evidence — this is a genuine, testable improvement, not a guess about which prompt 'feels' better. THIS full loop — test set, run, analyze failure pattern, revise, re-run, compare — is the actual discipline of prompt engineering, and it's exactly what you'll do in today's lab."*

---

## SEGMENT 6: Lab — Iteratively Refine a Prompt Against a Test Set (10 min)

### Instructions (read aloud, step by step)

1. You're given a starter zero-shot prompt for classifying product reviews as `POSITIVE`, `NEGATIVE`, or `MIXED`, plus a 5-case test set including one deliberately tricky sarcastic review.
2. Run the zero-shot prompt against all 5 cases and record the score.
3. Identify which case(s) failed and form a hypothesis about WHY.
4. Revise the prompt — using few-shot examples, role prompting, chain-of-thought, or a combination — to fix the identified failure.
5. Re-run against the SAME test set and confirm the score improved, without breaking any previously-passing case.

### Starter Code

```python
test_cases = [
    {"review": "Absolutely love this product, works perfectly!", "expected": "POSITIVE"},
    {"review": "Terrible quality, broke after one day.", "expected": "NEGATIVE"},
    {"review": "Great screen, but the battery life is disappointing.", "expected": "MIXED"},
    {"review": "Oh WONDERFUL, another product that stopped working after a week. Just what I needed.", "expected": "NEGATIVE"},
    {"review": "It's fine, does what it says, nothing special either way.", "expected": "MIXED"},
]

zero_shot_template = """Classify this review as POSITIVE, NEGATIVE, or MIXED.
Respond with only the label.

Review: "{review}"

Label:"""

def classify_review(review_text, prompt_template):
    full_prompt = ___.format(review=___)
    return ask_llm(full_prompt).strip()

# Step 2: run the baseline
for case in test_cases:
    result = ___
    status = "PASS" if result == case["expected"] else "FAIL"
    print(f"[{status}] expected={case['expected']} got={result} | {case['review'][:40]}...")

# TODO: write your hypothesis about the failure as a comment

# Step 4: your revised prompt template
revised_template = """___"""

# Step 5: re-run with the revised template
for case in test_cases:
    result = ___
    status = "PASS" if result == case["expected"] else "FAIL"
    print(f"[{status}] expected={case['expected']} got={result} | {case['review'][:40]}...")
```

### Reference Solution

```python
test_cases = [
    {"review": "Absolutely love this product, works perfectly!", "expected": "POSITIVE"},
    {"review": "Terrible quality, broke after one day.", "expected": "NEGATIVE"},
    {"review": "Great screen, but the battery life is disappointing.", "expected": "MIXED"},
    {"review": "Oh WONDERFUL, another product that stopped working after a week. Just what I needed.", "expected": "NEGATIVE"},
    {"review": "It's fine, does what it says, nothing special either way.", "expected": "MIXED"},
]

zero_shot_template = """Classify this review as POSITIVE, NEGATIVE, or MIXED.
Respond with only the label.

Review: "{review}"

Label:"""

def classify_review(review_text, prompt_template):
    full_prompt = prompt_template.format(review=review_text)
    return ask_llm(full_prompt).strip()

print("--- Baseline (zero-shot) ---")
for case in test_cases:
    result = classify_review(case["review"], zero_shot_template)
    status = "PASS" if result == case["expected"] else "FAIL"
    print(f"[{status}] expected={case['expected']} got={result} | {case['review'][:40]}...")

# Hypothesis: the sarcastic review ("Oh WONDERFUL...") likely gets misread as
# POSITIVE by a zero-shot model reacting to surface-level positive words
# ("WONDERFUL") without picking up on the sarcastic intent signaled by
# the contradictory context ("stopped working after a week").

revised_template = """Classify this review as POSITIVE, NEGATIVE, or MIXED.
Watch carefully for SARCASM -- positive-sounding words used to describe a
clearly negative experience should be classified as NEGATIVE, not POSITIVE.
Respond with only the label.

Review: "This is exactly the kind of quality I love, breaking after just two uses."
Label: NEGATIVE

Review: "Great screen, but the battery life is disappointing."
Label: MIXED

Review: "{review}"
Label:"""

print("\n--- Revised (few-shot + sarcasm rule) ---")
for case in test_cases:
    result = classify_review(case["review"], revised_template)
    status = "PASS" if result == case["expected"] else "FAIL"
    print(f"[{status}] expected={case['expected']} got={result} | {case['review'][:40]}...")
```

**Example output (illustrative — actual LLM output will vary run to run; this is the realistic pattern: zero-shot plausibly misreads the sarcastic review as POSITIVE due to the surface-level positive words, while the revised prompt, with an explicit sarcasm rule plus a matching worked example, correctly reads the contradictory context as NEGATIVE):**
```
--- Baseline (zero-shot) ---
[PASS] expected=POSITIVE got=POSITIVE | Absolutely love this product, works pe...
[PASS] expected=NEGATIVE got=NEGATIVE | Terrible quality, broke after one day....
[PASS] expected=MIXED got=MIXED | Great screen, but the battery life is di...
[FAIL] expected=NEGATIVE got=POSITIVE | Oh WONDERFUL, another product that sto...
[PASS] expected=MIXED got=MIXED | It's fine, does what it says, nothing s...

--- Revised (few-shot + sarcasm rule) ---
[PASS] expected=POSITIVE got=POSITIVE | Absolutely love this product, works pe...
[PASS] expected=NEGATIVE got=NEGATIVE | Terrible quality, broke after one day....
[PASS] expected=MIXED got=MIXED | Great screen, but the battery life is di...
[PASS] expected=NEGATIVE got=NEGATIVE | Oh WONDERFUL, another product that sto...
[PASS] expected=MIXED got=MIXED | It's fine, does what it says, nothing s...
```

**Instructor circulates**, checking specifically that students form a HYPOTHESIS about the failure before jumping to a fix (not just randomly trying things), and that their re-run genuinely re-tests all 5 cases (not just the one that failed) to confirm the fix didn't accidentally break something that was already passing.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Zero-shot vs. few-shot prompting, and how worked examples can encode non-obvious rules
- Role prompting as a style/tone lever via the `system` message, with honest limits on accuracy
- Chain-of-thought reasoning, both explicitly instructed and via the simple "let's think step by step" trick
- Building a test set and doing structured failure analysis, with a real before/after comparison

**Bridge to next session:** *"Today you learned to shape what a model produces through careful prompting. But every technique today still trusted the model to format its final answer correctly on its own — a bare label, a number after 'Final answer:'. In a real application, you often need a GUARANTEED, machine-parseable structure — a specific set of fields, correct types, no exceptions — not just 'usually formatted the way we asked.' Next session covers exactly that: structured outputs with Pydantic, and the `instructor` library, which forces and validates an LLM's response into a schema you define, closing the gap between 'usually right format' and 'always right format.'"*

**Homework / self-practice:**
1. Take the sarcasm test case from today's lab and add TWO more of your own tricky sarcastic/ambiguous reviews to the test set. Re-run your revised prompt against all 7 cases and report the final score.
2. Write a chain-of-thought prompt for a multi-step reasoning problem of your own choosing (word problem, logic puzzle, or multi-step planning task) and run it both with and without the "let's think step by step" phrase, comparing the two outputs.
3. In 3-4 sentences, describe a real scenario (from work, school, or daily life) where you'd choose role prompting, and specify exactly what system message you'd use and why.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Is few-shot prompting always better than zero-shot?**
→ No — for tasks the model already handles well with plain instructions (common classification, general knowledge), few-shot examples mainly add token cost without meaningfully improving accuracy. Few-shot earns its cost specifically when there's a non-obvious rule, a specific output format, or known edge cases the model needs anchoring on.

**Q: Can I combine few-shot, role prompting, AND chain-of-thought in the same prompt?**
→ Yes, and it's common in real production prompts — a system message setting the role, followed by a user message with a few worked examples and an instruction to reason step by step. Just be mindful of total token cost from Session 1/2, since every technique adds tokens to the request.

**Q: Does chain-of-thought reasoning shown in the output mean the model is "actually thinking," the way a person does?**
→ Mechanically, it's still next-token prediction from Session 1 — generating reasoning-shaped text tends to produce more reliable final answers on multi-step problems, largely because it gives the model useful intermediate text to condition on for later steps. Whether that constitutes "actual thinking" in a deeper sense is a genuinely debated question beyond this course's scope; what matters practically is that it measurably helps on the right kind of problems.

**Q: How large should a real test set be — is 5 cases from today's lab realistic for a production prompt?**
→ 5 is a reasonable MINIMUM for a classroom exercise to build the habit; real production prompt evaluation often uses dozens to hundreds of cases, ideally covering the full range of realistic inputs including known edge cases, specifically so a small sample doesn't hide a systematic failure pattern.

**Q: If a test-set case still fails after several revision attempts, what should I do?**
→ Consider whether the task might need a technique beyond prompting alone — very hard edge cases sometimes genuinely need structured output validation (next session) to catch and handle failures gracefully, or in some cases may need a different task decomposition entirely (breaking one hard prompt into two simpler chained prompts) rather than endlessly tweaking wording.

---

## Instructor Notes

- **Prerequisite check:** Confirm students still have `ask_llm()` working from Session 2 before SEGMENT 1 — this entire session depends on it being callable without re-explaining setup.
- **Common mistake:** Writing few-shot examples that are all the SAME label (e.g. all HIGH urgency), which fails to teach the model to discriminate between classes. Point this out explicitly if you see it during the lab.
- **Another common mistake:** Treating role prompting as a fix for factual/reasoning errors rather than style — revisit the SEGMENT 3 limits discussion if this comes up.
- **Another common mistake:** In the SEGMENT 6 lab, fixing the one failing case but not re-running the FULL test set afterward, silently breaking a previously-passing case. Emphasize "always re-run the whole set, not just the failure" explicitly.
- **Engagement tip:** SEGMENT 4's apple/CoT demo, with the deliberate wrong-vs-right comparison, is usually the strongest "aha" — the hand-verified 38 apples makes the improvement concrete and checkable, not just asserted.
- **Time check:** If running behind before the break, shorten SEGMENT 3's role-prompting limits discussion to the single comprehension-check question instead of the full "Ask" discussion.
- **If running long after the break:** Compress SEGMENT 5 to running just the zero-shot version live and describing the few-shot re-run's results verbally instead of live-coding both fully.
- **Materials to prepare:** `ask_llm()` from Session 2 working and tested; scratch notebook with SEGMENT 2, 4, and 5's demos pre-typed so live-coding doesn't stall; be ready with the exact by-hand apple-problem arithmetic (38) in case the live call returns something different than the illustrative example.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Few-shot examples all sharing the same label | Model doesn't learn to discriminate between classes, may default to that one label | Include examples spanning ALL possible output labels/classes |
| Role prompt used to try to fix factual/reasoning errors | Persona changes tone but not underlying correctness | Use chain-of-thought or better task decomposition for reasoning issues, not role prompting |
| CoT prompt applied to a trivial single-step task | Unnecessary extra tokens/cost with no accuracy benefit | Reserve CoT for genuinely multi-step reasoning or calculation tasks |
| Testing a prompt revision only on the case that previously failed | Silently breaks a previously-passing case without noticing | Always re-run the FULL test set after any prompt revision |
| Inconsistent formatting between few-shot examples and the final query | Model gets confused about the expected output format | Keep every example and the final query in an identical template/format |

---

## Appendix: Extra Chain-of-Thought Worked Example (Optional, If Time Allows)

```python
logic_prompt = """Five friends are sitting in a row. Priya is to the left of Raj.
Sam is to the right of Raj but to the left of Meera. Ana is at the far right.
Who is sitting in the middle (3rd position)?

Let's think step by step."""

print(ask_llm(logic_prompt))
```

**Example output (illustrative — actual LLM output will vary run to run, but this is the realistic shape of a correctly-reasoned answer):**
```
We know the order includes these constraints:
- Priya is left of Raj
- Sam is right of Raj but left of Meera
- Ana is at the far right (position 5)

So Ana is fixed at position 5. The remaining order must satisfy Priya < Raj < Sam < Meera.
That gives exactly one valid order: Priya, Raj, Sam, Meera, Ana.

Position 3 (the middle) is Sam.

Final answer: Sam
```

**Say (if running this appendix):** *"Logic puzzles like this are an even clearer illustration than arithmetic of why CoT helps — the model has to track several constraints simultaneously, and writing them out explicitly, one at a time, dramatically reduces the chance of silently dropping a constraint partway through."*

---

## Appendix: Prompt Technique Selection Cheat Sheet (Instructor Reference)

| Situation | Reach for |
|---|---|
| Simple, common task the model likely already handles well | Zero-shot |
| Task has a non-obvious rule or specific edge cases | Few-shot with examples covering those edge cases |
| Need a specific tone/style/audience fit | Role prompting (system message) |
| Multi-step arithmetic, logic, or planning task | Chain-of-thought ("let's think step by step" or explicit worked steps) |
| Need a guaranteed exact output structure | Preview of next session — structured outputs with Pydantic/instructor |

---

## FAQ — Additional Questions

**Q: Does adding "Let's think step by step" ever make an answer WORSE?**
→ Rarely, but possible on very simple tasks where the extra reasoning gives the model more opportunity to talk itself into an overcomplicated or wrong answer instead of a direct, already-correct one. This is exactly why testing against a real test set (SEGMENT 5) matters — don't assume any technique helps without checking.

**Q: Should the few-shot examples be real production examples, or can they be made up?**
→ Real, representative examples are ideal when available, since they reflect the actual distribution of inputs your application will see. Made-up examples work fine for learning the technique (as in today's session) but for a real project, mine actual logged inputs/edge cases where possible.

**Q: Is there a limit to how long a chain-of-thought reasoning trace should be?**
→ No hard limit, but longer isn't automatically better — connects back to Session 1's token-cost discussion and Session 2's `max_tokens` setting. A well-scoped CoT prompt should produce reasoning proportional to the problem's actual complexity, not padding.

---

## Materials Checklist

- [ ] `ask_llm()` helper from Session 2 working and tested
- [ ] Scratch notebook with SEGMENT 2, 4, and 5's demos pre-typed
- [ ] Whiteboard space for the by-hand apple-problem arithmetic (35% of 120 = 42, 120-42=78, 78-40=38)
- [ ] Printed or projected prompt-technique cheat sheet for reference during the lab
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's role-prompting limits discussion to the comprehension check only |
| Running long after break | Compress SEGMENT 5 to live-running only the zero-shot baseline, describing the few-shot re-run's results verbally |
| Low energy after lunch/break | Run the Appendix logic-puzzle CoT demo as an interactive "guess the answer first" group activity |
| Advanced group finishes lab early | Have them add a role-prompting layer on top of their revised few-shot prompt and re-test the full set again |
| No shared screen / projector issue | Walk through the test-set PASS/FAIL tables on the whiteboard using this script's exact illustrative results |

---

## End-of-Session Quiz (5 Questions)

1. What is the key difference between zero-shot and few-shot prompting?
2. Why might a set of few-shot examples that are ALL the same label hurt performance?
3. Is role prompting a reliable way to improve factual accuracy? What does it reliably change instead?
4. Why does chain-of-thought prompting tend to help on multi-step arithmetic or logic problems specifically?
5. Why is it important to re-run the FULL test set after revising a prompt, not just the case that previously failed?

**Answer key (instructor):**
1. Zero-shot gives only an instruction with no worked examples; few-shot includes a small number of input/output example pairs to anchor the model's pattern, useful for non-obvious rules or edge cases.
2. It gives the model no signal for how to discriminate between different possible labels, potentially biasing it toward always predicting that one label.
3. No, not reliably for accuracy — it mainly changes tone, style, and vocabulary; it does not give the model new computational or reasoning ability.
4. Because it gives the model explicit intermediate results as text to condition on for later steps, reducing the chance of a silent error accumulating across a chain of steps computed all at once.
5. Because a prompt revision that fixes one failing case can accidentally change behavior on previously-passing cases; only re-testing the whole set catches that regression.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Extended sarcasm test set (7 cases) + score | All 7 cases run, correct scoring, clear reporting | Cases run, minor scoring/reporting issues | Fewer than 7 cases or unclear results | Not attempted |
| CoT with/without comparison on own problem | Clear problem choice, both variants run, meaningful comparison written | Both variants run, thin comparison | Only one variant run | Not attempted |
| Role prompting scenario write-up | Concrete scenario, well-justified system message | Reasonable scenario, thin justification | Vague scenario or missing system message | Not attempted |

**Total:** /12 — Pass threshold: 8/12
