# =============================================================
# Session 14.1: Prompt Engineering & Reasoning
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Same 10 partner messages, three prompt versions -
# let's prove which prompt routes them best, then crack the
# Rs 600 payout question with chain-of-thought.
#
# Syntax scope check: requests/dotenv + the ask_llm() helper from
# Session 13.2, plain Python lists/dicts (Module 1). No frameworks.
#
# Install once:  pip install requests python-dotenv
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# =============================================================

# --- SETUP ---
# The ask_llm() helper from Session 13.2, trimmed down.
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def ask_llm(system, user, temperature=0, max_tokens=300, retries=4):
    payload = {"model": MODEL, "temperature": temperature, "max_tokens": max_tokens,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    for attempt in range(retries):
        r = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 ** attempt)
            continue
        raise RuntimeError(f"{r.status_code}: {r.text[:200]}")
    raise RuntimeError("Gave up after retries")


# --- EXPLAIN ---
# Concept Block 4: the test set. Correct labels are known in
# advance. None of these 10 appear in our few-shot examples below
# - that's the "never grade your own homework" rule from Session 17.
# -------------------------------------------------------------

LABELS = ["payout", "incentive", "app_issue", "safety", "other"]

test_set = [
    ("Payout not credited since Friday", "payout"),
    ("Why did I not get the 60-order bonus? I did 61", "incentive"),
    ("App keeps crashing when I go online", "app_issue"),
    ("A customer threatened me at the gate", "safety"),
    ("Can I change my registered bank account?", "payout"),
    ("Rain bonus not added for yesterday's orders", "incentive"),
    ("GPS shows me in Secunderabad but I'm in Gachibowli", "app_issue"),
    ("I met with a small accident, bike damaged, am I covered?", "safety"),
    ("kal ka paisa nahi aaya", "payout"),
    ("Thanks for the help!", "other"),
]


# --- EXPLAIN ---
# Three prompt versions, each changing ONE thing (Concept Block 5):
#   v1 zero-shot, no role
#   v2 + role and label definitions
#   v3 + few-shot examples covering the tricky boundaries
# Temperature 0, because routing should be consistent (Session 13.1).
# -------------------------------------------------------------

v1_system = "Classify the message. Labels: payout, incentive, app_issue, safety, other."

v2_system = (
    "You are a senior support lead at Swiggy who routes delivery-partner messages. "
    "Partners often write short messages in English, Hindi or Hinglish. "
    "Labels:\n"
    "- payout: anything about getting paid, payment timing, or bank details\n"
    "- incentive: bonuses, targets, surge or rain pay\n"
    "- app_issue: app crashes, login, GPS or map problems\n"
    "- safety: threats, accidents, injuries, insurance after an incident - never miss these\n"
    "- other: anything else\n"
    "Reply with ONLY the label, nothing else."
)

few_shot_examples = (
    "Examples:\n"
    "Message: Weekly amount still showing pending -> payout\n"
    "Message: Peak hour bonus missing for Sunday -> incentive\n"
    "Message: Fell off the scooter near Ameerpet, need help with insurance -> safety\n"
    "Message: Mera app login nahi ho raha -> app_issue\n"
)
v3_system = v2_system + "\n\n" + few_shot_examples


def run_prompt(name, system):
    correct, failures = 0, []
    for message, expected in test_set:
        predicted = ask_llm(system, f"Message: {message}").lower().strip(" .'\"")
        if predicted == expected:
            correct += 1
        else:
            failures.append((message, expected, predicted))
    print(f"\n{name}: {correct}/{len(test_set)} correct ({correct / len(test_set):.0%})")
    for message, expected, predicted in failures:
        print(f"   x '{message}' -> expected {expected}, got '{predicted}'")
    return correct


scores = {
    "v1 zero-shot": run_prompt("v1 zero-shot", v1_system),
    "v2 + role & definitions": run_prompt("v2 + role & definitions", v2_system),
    "v3 + few-shot": run_prompt("v3 + few-shot", v3_system),
}


# --- EXPLAIN ---
# Failure analysis: read the "x" lines above out loud and group them.
# Typical groups: FORMAT (model wrote "Label: payout" - v1 never said
# "only the label"), LANGUAGE (Hinglish), BOUNDARY (bank details,
# insurance). Each version fixed one group. Your exact failures may
# differ by model - that's normal, and it's why we test.
# -------------------------------------------------------------


# --- EXPLAIN ---
# Concept Block 3: chain-of-thought on the Rs 600 question.
# First we compute the TRUE answer in plain Python, so we can check
# the model instead of trusting it.
# -------------------------------------------------------------

def weekly_payout(orders, peak_orders, cancellations):
    base = orders * 30
    peak = peak_orders * 15
    target = 400 if orders >= 60 else 0
    penalty = cancellations * 100
    return base + peak + target - penalty


last_week = weekly_payout(62, 40, 0)
this_week = weekly_payout(62, 20, 3)
print(f"\nTrue answer: last week Rs {last_week}, this week Rs {this_week}, "
      f"difference Rs {last_week - this_week}")

rules = ("Payout rules: Rs 30 per order; Rs 15 extra per peak-hour order; "
         "Rs 400 bonus if 60 or more orders in the week; Rs 100 deducted per "
         "customer-reported cancellation.\n"
         "Last week: 62 orders, 40 peak-hour, 0 cancellations.\n"
         "This week: 62 orders, 20 peak-hour, 3 cancellations.\n")

helpdesk_role = "You are Swiggy's partner helpdesk."

direct = ask_llm(helpdesk_role,
                 rules + "In one short sentence, why is this week's payout lower?",
                 max_tokens=60)
print("\nWithout CoT:", direct)

cot = ask_llm(helpdesk_role,
              rules + "Work it out step by step: compute each week's payout line by "
                      "line, then state the difference and its causes.")
print("\nWith CoT:\n", cot)


# --- EXPLAIN ---
# Compare both answers to the true Rs 600 and its two causes (fewer
# peak-hour orders: Rs 300; cancellations: Rs 300). CoT shows its
# working, so if a step is wrong you can see exactly which one.
#
# What this demo does NOT do yet: the replies are still free text we
# compare by eye or with string matching. Session 14.3 forces the
# model to return validated JSON (e.g. {"label": "payout"}), so
# parsing can't break. And 10 messages is a quick check, not proof -
# larger evaluation sets and RAGAS metrics come in Session 18.1.
# -------------------------------------------------------------
