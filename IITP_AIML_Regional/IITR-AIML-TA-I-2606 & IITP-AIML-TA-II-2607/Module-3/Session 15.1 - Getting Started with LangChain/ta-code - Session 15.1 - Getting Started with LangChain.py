# =============================================================
# Session 15.1: Getting Started with LangChain
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Our helpdesk's two jobs - route the message, then
# reply in the partner's language - rebuilt as LangChain chains.
#
# Syntax scope check: dotenv (13.2), the router prompt (14.1), plus
# today's new tools: ChatOpenAI, PromptTemplate, ChatPromptTemplate,
# LLMChain, SequentialChain. Output parsers wait for Session 15.2.
#
# Install once (versions pinned so LLMChain/SequentialChain exist):
#   pip install "langchain==0.3.*" "langchain-openai==0.3.*" python-dotenv
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# =============================================================

# --- SETUP ---
import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore")   # hide LLMChain deprecation notices in class
load_dotenv()


# --- EXPLAIN ---
# Concept Block 2: ChatOpenAI talks to any OpenAI-style API. Pointing
# base_url at OpenRouter gives us every model on OpenRouter.
# max_retries replaces our hand-written backoff loop from 13.2.
# -------------------------------------------------------------

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    max_tokens=200,
    max_retries=3,
)

reply = llm.invoke("In one line, what is a weekly payout for a delivery partner?")
print("Type returned:", type(reply).__name__)
print("Text:", reply.content)


# --- EXPLAIN ---
# Concept Block 3: PromptTemplate = a prompt with named blanks.
# It's our 14.1 router prompt, now reusable and self-checking.
# -------------------------------------------------------------

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

router_template = PromptTemplate.from_template(
    "Classify this Swiggy delivery-partner message into one of: "
    "payout, incentive, app_issue, safety, other. "
    "Partners often write in Hinglish. Reply with only the lowercase label.\n\n"
    "Message: {message}"
)

print("\nBlanks in router_template:", router_template.input_variables)
print("Filled-in prompt:\n", router_template.format(message="kal ka paisa nahi aaya"))


# --- EXPLAIN ---
# Concept Block 4: ChatPromptTemplate = role messages with blanks.
# Rules go in "system"; the partner's content goes in "human".
# -------------------------------------------------------------

reply_template = ChatPromptTemplate.from_messages([
    ("system", "You are Swiggy's delivery-partner helpdesk. Reply in {language}, "
               "under 60 words, warmly and clearly. If you don't know a policy "
               "detail, say a human will follow up - never invent rules."),
    ("human", "Issue category: {category}\nPartner message: {message}"),
])

print("\nBlanks in reply_template:", reply_template.input_variables)


# --- EXPLAIN ---
# Concept Block 5: LLMChain = template + model in one unit.
# output_key names the answer - that name is the wiring for the
# next step. (Modern equivalent: router_template | llm)
# -------------------------------------------------------------

from langchain.chains import LLMChain, SequentialChain

router_chain = LLMChain(llm=llm, prompt=router_template, output_key="category")

result = router_chain.invoke({"message": "kal ka paisa nahi aaya"})
print("\nLLMChain result dict:", result)


# --- EXPLAIN ---
# Concept Block 6: SequentialChain wires chains by variable name.
# router_chain outputs "category"; reply_template has a {category}
# blank - so the value flows across automatically.
# -------------------------------------------------------------

reply_chain = LLMChain(llm=llm, prompt=reply_template, output_key="reply")

helpdesk = SequentialChain(
    chains=[router_chain, reply_chain],
    input_variables=["message", "language"],
    output_variables=["category", "reply"],
)

inbox = [
    ("kal ka paisa nahi aaya", "simple Hindi"),
    ("Rain bonus not added for yesterday's orders", "English"),
    ("A customer threatened me at the gate in Gachibowli", "English"),
]

for message, language in inbox:
    out = helpdesk.invoke({"message": message, "language": language})
    print(f"\n[{out['category'].strip()}] {message}\n  -> {out['reply']}")


# --- EXPLAIN ---
# Break the wiring on purpose: the router outputs "label" but the
# reply template still asks for {category}. SequentialChain refuses
# to even build - variable names ARE the connections.
# -------------------------------------------------------------

bad_router = LLMChain(llm=llm, prompt=router_template, output_key="label")
try:
    SequentialChain(chains=[bad_router, reply_chain],
                    input_variables=["message", "language"],
                    output_variables=["reply"])
except Exception as e:
    print("\nBroken wiring ->", type(e).__name__, ":", str(e)[:120])


# --- EXPLAIN ---
# Notice: the category comes back as free text again (we used .strip()
# as a band-aid), and the reply may still guess policy details.
# What this demo does NOT do yet: parse outputs into Pydantic objects
# inside a chain (Session 15.2), or ground replies in the real partner
# handbook (Session 17.1).
# -------------------------------------------------------------
