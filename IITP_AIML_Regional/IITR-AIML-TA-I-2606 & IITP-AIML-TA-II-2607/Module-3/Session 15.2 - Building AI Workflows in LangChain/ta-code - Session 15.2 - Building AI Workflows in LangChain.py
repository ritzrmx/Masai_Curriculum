# =============================================================
# Session 15.2: Building AI Workflows in LangChain
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Four asks from Swiggy partner-ops - clean tickets, a
# weekly brief, an FAQ bot, and a CSV copilot - built as chains.
#
# Syntax scope check: Pandas/NumPy (Module 1), the PartnerTicket
# model (14.3), ChatOpenAI + templates (15.1), plus today's new
# tools: the | pipe style, StrOutputParser, JsonOutputParser,
# PydanticOutputParser, .partial(), .batch().
# No retrieval or vector stores yet (Sessions 16.3 / 17.1).
#
# Install once:
#   pip install "langchain==0.3.*" "langchain-openai==0.3.*" pydantic pandas numpy python-dotenv
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# NOTE: all policy text and data below are synthetic, for teaching.
# =============================================================

# --- SETUP ---
import os
from typing import Literal, Optional

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (StrOutputParser, JsonOutputParser,
                                           PydanticOutputParser)

load_dotenv()
llm = ChatOpenAI(model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.getenv("OPENROUTER_API_KEY"),
                 temperature=0, max_retries=3)


# --- EXPLAIN ---
# Concept Blocks 1-2: PydanticOutputParser = the 14.3 form, inside a
# chain. get_format_instructions() writes the "return JSON like this"
# text for us; .partial() fills that blank once.
# Pipe style: prompt | llm | parser  ("then ... then ...")
# -------------------------------------------------------------

class PartnerTicket(BaseModel):
    partner_id: Optional[str] = Field(default=None, description="Like P-12345, null if absent")
    category: Literal["payout", "incentive", "app_issue", "safety", "other"]
    amount_disputed: Optional[int] = Field(default=None, ge=0, description="Rupees, digits only")
    urgency: Literal["low", "medium", "high"]


ticket_parser = PydanticOutputParser(pydantic_object=PartnerTicket)

extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract a support ticket from a Swiggy delivery-partner message "
               "(English, Hindi or Hinglish). Never invent values.\n{format_instructions}"),
    ("human", "{message}"),
]).partial(format_instructions=ticket_parser.get_format_instructions())

extract_chain = extract_prompt | llm | ticket_parser

t = extract_chain.invoke({"message": "bhai mera ID P-20417 hai, payout Rs 600 kam aaya. jaldi dekho"})
print("Extracted ticket:", t)

# JsonOutputParser for contrast: a dict, no type checks at all.
loose_chain = extract_prompt | llm | JsonOutputParser()
print("Loose dict      :", loose_chain.invoke({"message": "P-33150 rain bonus missing"}))


# --- EXPLAIN ---
# Concept Block 6 (pipeline): extract many messages with .batch(),
# compute exact totals in Pandas, THEN let the LLM summarise.
# Structured hand-offs = correct numbers in the summary.
# -------------------------------------------------------------

inbox = [
    "bhai mera ID P-20417 hai, payout Rs 600 kam aaya, 3 cancellation galat lage",
    "P-33150: rain bonus not added for Tuesday",
    "ID P-10982 - customer pushed me at the gate, I'm hurt",
    "P-41877 weekly payout short by Rs 250",
    "P-55021 app GPS wrong since morning, lost 4 orders",
    "P-60213 kal ka paisa nahi aaya, Rs 1,180 pending",
]

tickets = extract_chain.batch([{"message": m} for m in inbox])
df = pd.DataFrame([tk.model_dump() for tk in tickets])
totals = df.groupby("category").agg(tickets=("category", "size"),
                                    disputed_rs=("amount_disputed", "sum"))
print("\n", df, "\n\n", totals)

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You write crisp weekly briefs for Swiggy's partner-ops manager. "
               "Max 4 bullet points. Use ONLY the numbers given."),
    ("human", "Ticket totals by category:\n{ticket_table}"),
])
summary_chain = summary_prompt | llm | StrOutputParser()
print("\nWeekly brief:\n", summary_chain.invoke({"ticket_table": totals.to_string()}))


# --- EXPLAIN ---
# Concept Block 4: FAQ bot. A small approved FAQ in the system prompt,
# plus an exact fallback line. First time our helpdesk answers payout
# timing from approved text instead of guessing (remember 13.2?).
# -------------------------------------------------------------

FAQ = """
Q: When are weekly payouts credited? A: Every Friday by 8 pm to your registered bank account.
Q: How is the rain bonus paid? A: Rs 10 extra per order delivered during an active rain alert.
Q: How do I change my bank account? A: Profile > Bank Details; changes take 2 working days.
Q: What if I have an accident on duty? A: Use the in-app SOS button. Accident cover applies on active orders.
"""

faq_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Swiggy's partner helpdesk. Answer ONLY using this FAQ:\n{faq}\n"
               "If the answer is not in the FAQ, reply exactly: "
               "'I'll connect you to a support agent.' Reply in the partner's language."),
    ("human", "{question}"),
]).partial(faq=FAQ)
faq_bot = faq_prompt | llm | StrOutputParser()

for q in ["Paisa kab aata hai?", "How much extra do I get when it rains?",
          "Can I deliver on a bicycle?"]:
    print(f"\nQ: {q}\nA: {faq_bot.invoke({'question': q})}")


# --- EXPLAIN ---
# Concept Block 5: CSV copilot. Same synthetic partner data as the
# Session 17 churn demo, plus a zone column. The LLM only fills a
# QueryPlan; Pandas does the maths; the LLM explains the number.
# The LLM never runs code and never does arithmetic.
# -------------------------------------------------------------

np.random.seed(42)
n = 200
partners = pd.DataFrame({
    "orders_last_30_days": np.random.randint(0, 60, n),
    "avg_rating": np.round(np.random.uniform(3.0, 5.0, n), 2),
    "months_active": np.random.randint(1, 36, n),
    "zone": np.random.choice(["Madhapur", "Kukatpally", "Gachibowli", "Ameerpet"], n),
})
partners["churned"] = ((partners["orders_last_30_days"] < 10) &
                       (partners["avg_rating"] < 4.2)).astype(int)


class QueryPlan(BaseModel):
    metric: Literal["orders_last_30_days", "avg_rating", "months_active", "churned"]
    aggregation: Literal["mean", "sum", "count", "max", "min"]
    group_by: Optional[Literal["zone", "churned"]] = None


plan_parser = PydanticOutputParser(pydantic_object=QueryPlan)
plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "Turn the manager's question into a query plan over a table with columns: "
               "orders_last_30_days, avg_rating, months_active, zone, churned (0/1).\n"
               "{format_instructions}"),
    ("human", "{question}"),
]).partial(format_instructions=plan_parser.get_format_instructions())
plan_chain = plan_prompt | llm | plan_parser

explain_chain = ChatPromptTemplate.from_messages([
    ("system", "Answer the manager's question in 1-2 sentences using ONLY this result."),
    ("human", "Question: {question}\nResult:\n{result}"),
]) | llm | StrOutputParser()


def ask_csv(question):
    plan = plan_chain.invoke({"question": question})
    if plan.group_by:
        result = partners.groupby(plan.group_by)[plan.metric].agg(plan.aggregation).round(2)
    else:
        result = round(partners[plan.metric].agg(plan.aggregation), 2)
    print(f"\nQ: {question}\n  plan  : {plan}\n  pandas: {result.to_dict() if hasattr(result, 'to_dict') else result}")
    print("  answer:", explain_chain.invoke({"question": question, "result": str(result)}))


ask_csv("Which zone has the lowest average partner rating?")
ask_csv("How many partners churned in total?")


# --- EXPLAIN ---
# What this demo does NOT do yet: the FAQ bot only knows 4 answers we
# pasted in. The full partner handbook can't fit (Session 13.1's context
# window problem). Sessions 16.2-17.1 fix that with embeddings, vector
# stores and RAG. And the CSV copilot always runs the SAME two steps -
# in Session 17.2 an agent decides for itself which tools to use.
# -------------------------------------------------------------
