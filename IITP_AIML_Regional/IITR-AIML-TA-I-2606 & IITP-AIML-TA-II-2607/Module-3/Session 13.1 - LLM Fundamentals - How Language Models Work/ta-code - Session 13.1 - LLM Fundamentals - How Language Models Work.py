# =============================================================
# Session 13.1: LLM Fundamentals - How Language Models Work
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Let's look inside the engine of our Swiggy partner
# helpdesk - tokens, temperature, top-p and the bill, in code.
#
# Syntax scope check: only NumPy (Module 1) plus one new library,
# tiktoken, to count tokens. NO API key and NO internet LLM call
# is needed today - calling a real LLM is Session 13.2's job.
#
# Install once:  pip install tiktoken numpy
# (tiktoken downloads its token dictionary the first time it runs)
# =============================================================

# --- SETUP ---
import numpy as np
import tiktoken

np.random.seed(42)


# --- EXPLAIN ---
# Concept Block 2: an LLM never sees "words" - it sees tokens.
# tiktoken is the tokenizer used by several OpenAI models. Other
# providers use different tokenizers, so exact counts differ,
# but the idea is identical.
# -------------------------------------------------------------

enc = tiktoken.get_encoding("cl100k_base")

question = "Why is my weekly payout less than last week?"
token_ids = enc.encode(question)

print("Question:", question)
print("Word count :", len(question.split()))
print("Token count:", len(token_ids))
print("Token pieces:", [enc.decode([t]) for t in token_ids])


# --- EXPLAIN ---
# Same meaning, different token counts. Numbers, rupee symbols and
# Indian-language scripts usually cost MORE tokens. This is the
# "short message isn't always cheap" trap from the pre-read.
# -------------------------------------------------------------

samples = {
    "English": "My payout is delayed",
    "Hindi": "मेरा भुगतान देर से आया है",
    "Telugu": "నా చెల్లింపు ఆలస్యమైంది",
    "Amount": "₹1,250.75 credited on 14/10",
}

for label, text in samples.items():
    print(f"{label:8} -> {len(enc.encode(text)):3} tokens  | {text}")


# --- EXPLAIN ---
# Concept Block 4: after the model scores every possible next token,
# temperature reshapes those scores before one is picked.
# These are the SAME five options and starting chances as the
# pre-read table: "Your payout will be credited by ___".
# Dividing log-scores by temperature, then re-normalising (softmax),
# is exactly what the provider does behind the scenes.
# -------------------------------------------------------------

next_tokens = ["Friday", "tomorrow", "Monday", "tonight", "never"]
base_probs = np.array([0.55, 0.25, 0.12, 0.06, 0.02])
log_scores = np.log(base_probs)


def apply_temperature(scores, temperature):
    scaled = np.exp(scores / temperature)
    return scaled / scaled.sum()


for t in [0.2, 1.0, 1.5]:
    probs = apply_temperature(log_scores, t)
    pretty = ", ".join(f"{w}: {p:.0%}" for w, p in zip(next_tokens, probs))
    print(f"\nTemperature {t}: {pretty}")
    picks = np.random.choice(next_tokens, size=10, p=probs)
    print("  10 sampled answers:", [str(p) for p in picks])


# --- EXPLAIN ---
# Top-p keeps only the most likely tokens whose chances add up to p.
# With p = 0.9 at temperature 1.0: Friday + tomorrow + Monday = 92%,
# so "tonight" and "never" are thrown away BEFORE sampling.
# -------------------------------------------------------------

def apply_top_p(probs, p=0.9):
    order = np.argsort(probs)[::-1]          # biggest first
    cumulative = np.cumsum(probs[order])
    keep_count = np.searchsorted(cumulative, p) + 1
    kept = np.zeros_like(probs)
    kept[order[:keep_count]] = probs[order[:keep_count]]
    return kept / kept.sum()


probs_t1 = apply_temperature(log_scores, 1.0)
probs_top_p = apply_top_p(probs_t1, p=0.9)
print("\nAfter top-p 0.9:")
for w, p in zip(next_tokens, probs_top_p):
    print(f"  {w:9} {p:.0%}")


# --- EXPLAIN ---
# Concept Block 5: cost = input tokens x input price + output tokens
# x output price. Prices below are ILLUSTRATIVE (Rs per million
# tokens) - always check your provider's pricing page.
# -------------------------------------------------------------

INPUT_PRICE_PER_M = 15     # Rs per 1,000,000 input tokens (illustrative)
OUTPUT_PRICE_PER_M = 60    # Rs per 1,000,000 output tokens (illustrative)


def cost_per_call(input_tokens, output_tokens):
    return (input_tokens * INPUT_PRICE_PER_M
            + output_tokens * OUTPUT_PRICE_PER_M) / 1_000_000


daily_questions = 50_000
lean = cost_per_call(500, 200)
whole_handbook = cost_per_call(150_000 + 500, 200)

print(f"\nLean prompt      : Rs {lean:.4f} per question -> Rs {lean * daily_questions:,.0f} per day")
print(f"Paste handbook   : Rs {whole_handbook:.4f} per question -> Rs {whole_handbook * daily_questions:,.0f} per day")


# --- EXPLAIN ---
# Context window check: input + output must fit. A 128k-token model
# simply cannot take the whole 150k-token handbook.
# -------------------------------------------------------------

CONTEXT_WINDOW = 128_000
needed = 150_000 + 500 + 200
print(f"\nTokens needed: {needed:,} | Window: {CONTEXT_WINDOW:,} | Fits? {needed <= CONTEXT_WINDOW}")


# --- EXPLAIN ---
# What this demo does NOT do yet: it never calls a real LLM. We
# simulated the "pick the next token" step with NumPy so you can
# SEE temperature and top-p working. Session 13.2 makes the first
# real API call; Session 17.1 (RAG) solves the "handbook doesn't
# fit" problem by sending only the relevant pages.
# -------------------------------------------------------------
