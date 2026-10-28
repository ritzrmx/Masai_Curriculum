# =============================================================
# Session 14.3: Structured Outputs with Pydantic
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Same messy Hinglish payout complaint - this time the
# LLM must hand back a clean, validated support ticket, not text.
#
# Syntax scope check: Python classes basics, Pandas (Module 1),
# dotenv (Session 13.2), plus today's new tools: pydantic
# (BaseModel, Field, Literal, field_validator), the openai client
# pointed at OpenRouter, and instructor. No LangChain yet (15.1).
#
# Install once:  pip install pydantic instructor openai python-dotenv pandas
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# =============================================================

# --- SETUP ---
import os
from typing import Literal, Optional

import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

load_dotenv()
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")


# --- EXPLAIN ---
# Concept Block 2: the "printed form". Each field is a box with a
# type. Literal = only these values. Optional = may be empty, so
# the LLM isn't forced to invent an amount that wasn't mentioned.
# Field descriptions are passed to the LLM by instructor.
# -------------------------------------------------------------

class PartnerTicket(BaseModel):
    partner_id: str = Field(description="Partner ID in the form P-12345")
    category: Literal["payout", "incentive", "app_issue", "safety", "other"]
    amount_disputed: Optional[int] = Field(
        default=None, ge=0, description="Disputed amount in rupees, digits only; null if not mentioned")
    orders_mentioned: Optional[int] = Field(default=None, ge=0)
    disputes_cancellations: bool = Field(
        default=False, description="True if the partner says cancellations were unfair")
    urgency: Literal["low", "medium", "high"] = Field(
        description="high for safety issues or angry/urgent tone")

    @field_validator("partner_id")
    @classmethod
    def id_format(cls, v):
        if not (v.startswith("P-") and v[2:].isdigit()):
            raise ValueError("partner_id must look like P-12345")
        return v


# --- EXPLAIN ---
# Concept Block 3: validation BEFORE any LLM is involved.
# Good data passes (and "600" text becomes the int 600).
# Bad data is refused with a precise, field-by-field reason.
# -------------------------------------------------------------

ok = PartnerTicket(partner_id="P-20417", category="payout", amount_disputed="600",
                   orders_mentioned=62, disputes_cancellations=True, urgency="high")
print("Valid ticket:", ok.model_dump())
print("Amount + 100 =", ok.amount_disputed + 100, "(a real int)")

try:
    PartnerTicket(partner_id="20417", category="Payout",
                  amount_disputed="600 rupees", urgency="high")
except ValidationError as e:
    print("\nRejected! Pydantic says:\n", e)


# --- SETUP ---
import instructor
from openai import OpenAI

# --- EXPLAIN ---
# Concept Block 4: the openai client speaks the OpenAI format;
# base_url points it at OpenRouter (Session 13.2). instructor
# "patches" it so create() accepts response_model=PartnerTicket.
# Mode.JSON = plain JSON, which nearly every OpenRouter model supports.
# -------------------------------------------------------------

base_client = OpenAI(base_url="https://openrouter.ai/api/v1",
                     api_key=os.getenv("OPENROUTER_API_KEY"))
client = instructor.from_openai(base_client, mode=instructor.Mode.JSON)

SYSTEM = ("You extract support tickets from Swiggy delivery-partner messages. "
          "Messages may be in English, Hindi or Hinglish. Never invent values: "
          "use null when something is not mentioned.")


def extract_ticket(message):
    return client.chat.completions.create(
        model=MODEL,
        response_model=PartnerTicket,
        max_retries=2,            # re-ask with the validation error, at most twice
        temperature=0,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": message}],
    )


message = ("bhai mera ID P-20417 hai, last week 62 orders kiye but payout ₹600 kam aaya, "
           "3 cancellation bhi lage jo maine nahi kiye. jaldi dekho")
ticket = extract_ticket(message)
print("\nExtracted:", ticket)
print("Type of amount_disputed:", type(ticket.amount_disputed).__name__)


# --- EXPLAIN ---
# Concept Block 5: same schema, many messages -> a clean table.
# Now it's ordinary Pandas from Module 1.
# -------------------------------------------------------------

inbox = [
    message,
    "P-33150: rain bonus not added for Tuesday",
    "ID P-10982 - customer pushed me at the gate, I'm hurt",
    "P-55021 app GPS wrong since morning, lost 4 orders",
]

tickets = [extract_ticket(m) for m in inbox]
df = pd.DataFrame([t.model_dump() for t in tickets])
print("\n", df)
print("\nTickets per category:\n", df["category"].value_counts())


# --- EXPLAIN ---
# Concept Block 6: handling malformed output. This message has no
# partner ID at all, so the validator can NEVER pass. instructor
# retries with the error, then gives up - and we fall back safely
# instead of crashing the helpdesk.
# -------------------------------------------------------------

no_id = "payout nahi aaya yaar, kab aayega??"
try:
    extract_ticket(no_id)
except Exception as e:   # instructor raises after max_retries is used up
    print(f"\nCould not extract a valid ticket ({type(e).__name__}).")
    print("Fallback: send to human review queue with the raw message.")


# --- EXPLAIN ---
# Check the first ticket against what the partner actually said.
# Pydantic guarantees the SHAPE (600 is an int, category is allowed),
# not the TRUTH (was it really 600?). That's still the test-set job
# from Session 14.1.
#
# What this demo does NOT do yet: reuse this schema inside a bigger
# multi-step pipeline. Session 15.2 plugs the same Pydantic model into
# LangChain's PydanticOutputParser to build extraction chains.
# -------------------------------------------------------------
