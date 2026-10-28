# =============================================================
# Session 13.2: Calling LLMs with APIs
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Time to send our partner's payout question to a real
# LLM - safely, from our own Python code.
#
# Syntax scope check: requests + os (Module 1, File Handling & APIs),
# plus today's new tools: python-dotenv, the chat-completions
# message format, and retry-with-backoff. No frameworks yet -
# LangChain is Session 15.1.
#
# Install once:  pip install requests python-dotenv
# Create a file named .env next to this script containing:
#     OPENROUTER_API_KEY=sk-or-v1-...your key...
#     OPENROUTER_MODEL=openai/gpt-4o-mini
# and add ".env" to your .gitignore.
# =============================================================

# --- SETUP ---
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


# --- EXPLAIN ---
# Concept Block 2: the key lives in .env, never in this file.
# os.getenv reads it by name. We fail loudly and early if it's
# missing, instead of getting a confusing 401 later.
# -------------------------------------------------------------

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    raise SystemExit("No OPENROUTER_API_KEY found - check your .env file.")

print("Key loaded:", API_KEY[:10] + "..." )   # never print the full key
print("Model:", MODEL)


# --- EXPLAIN ---
# Concept Blocks 3-4: one POST request. Headers carry the key,
# the body carries the model, the messages and our settings.
# The system message is the helpdesk's "briefing card".
# -------------------------------------------------------------

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

messages = [
    {"role": "system",
     "content": "You are Swiggy's delivery-partner helpdesk. Answer only "
                "payout and incentive questions, politely, in under 60 words."},
    {"role": "user",
     "content": "Why is my weekly payout Rs 600 less than last week?"},
]

body = {
    "model": MODEL,
    "messages": messages,
    "temperature": 0.2,
    "max_tokens": 150,
}

response = requests.post(URL, headers=headers, json=body, timeout=30)
print("\nStatus code:", response.status_code)


# --- EXPLAIN ---
# Concept Block 5: the answer is nested inside JSON. We also read
# finish_reason (was it cut off?) and usage (the "invoice").
# -------------------------------------------------------------

data = response.json()

if response.status_code == 200:
    answer = data["choices"][0]["message"]["content"]
    finish = data["choices"][0].get("finish_reason")
    usage = data.get("usage", {})
    print("\nAnswer:", answer)
    print("Finish reason:", finish)
    print("Input tokens:", usage.get("prompt_tokens"),
          "| Output tokens:", usage.get("completion_tokens"))
else:
    print("Error body:", data)


# --- EXPLAIN ---
# The model has NO memory. To continue the chat, we append its
# reply as an "assistant" message, add the partner's next message,
# and resend the WHOLE list. Watch prompt_tokens grow.
# -------------------------------------------------------------

if response.status_code == 200:
    messages.append({"role": "assistant", "content": answer})
    messages.append({"role": "user", "content": "I did 62 orders both weeks."})
    body["messages"] = messages
    follow_up = requests.post(URL, headers=headers, json=body, timeout=30).json()
    print("\nFollow-up answer:", follow_up["choices"][0]["message"]["content"])
    print("Input tokens now:", follow_up["usage"]["prompt_tokens"])


# --- EXPLAIN ---
# Concept Block 6: a reusable helper with retry + exponential
# backoff. Retry ONLY 429 (rate limit) and 5xx (provider trouble).
# 400/401/402 are our problem - retrying won't fix them.
# -------------------------------------------------------------

RETRYABLE = {429, 500, 502, 503}


def ask_llm(messages, temperature=0.2, max_tokens=150, retries=4):
    payload = {"model": MODEL, "messages": messages,
               "temperature": temperature, "max_tokens": max_tokens}
    for attempt in range(retries):
        try:
            r = requests.post(URL, headers=headers, json=payload, timeout=30)
        except requests.exceptions.Timeout:
            print(f"  attempt {attempt + 1}: timed out, retrying...")
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        if r.status_code in RETRYABLE:
            wait = 2 ** attempt
            print(f"  attempt {attempt + 1}: got {r.status_code}, waiting {wait}s")
            time.sleep(wait)
        else:
            raise RuntimeError(f"Not retryable ({r.status_code}): {r.text[:200]}")
    raise RuntimeError("Gave up after all retries.")


print("\nHelper answer:",
      ask_llm([{"role": "user", "content": "In one line: when are Swiggy partner payouts usually credited?"}]))


# --- EXPLAIN ---
# Prove the "don't retry a 401" rule: send a fake key on purpose.
# -------------------------------------------------------------

bad = requests.post(URL, headers={"Authorization": "Bearer sk-fake"},
                    json=body, timeout=30)
print("\nWith a fake key ->", bad.status_code, "(not retryable: fix the key)")


# --- EXPLAIN ---
# Notice the helper's answer about payout days: it sounds confident,
# but the model has never seen Swiggy's real payout policy - it is
# guessing (Session 13.1's hallucination trap). What this demo does
# NOT do yet: write prompts that reliably behave (Session 14.1),
# force the reply into clean JSON (Session 14.3), or ground answers
# in the real handbook (Session 17.1, RAG). We'll reuse ask_llm()
# all through Session 14.
# -------------------------------------------------------------
