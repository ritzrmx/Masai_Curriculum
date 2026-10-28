# =============================================================
# Session 17.2: Building an AI Agent with LangChain
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: Mini-build - an FAQ Helpdesk agent that can search the
# handbook, look up a partner's stats and calculate payouts, and
# finally answers the Rs 600 question by itself.
#
# Syntax scope check: ChatOpenAI (15.1), Chroma retriever (16.3/17.1),
# the payout rules (14.1), plus today's new tools: @tool, Tool,
# create_react_agent, AgentExecutor, initialize_agent,
# max_iterations, handle_parsing_errors.
#
# Install once:
#   pip install "langchain==0.3.*" "langchain-openai==0.3.*" "langchain-text-splitters<1" \
#               "langchain-chroma<1" "langchain-huggingface<1" sentence-transformers chromadb python-dotenv
# Put partner_handbook.txt (provided) next to this script.
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# NOTE: partner data below is synthetic, for teaching.
# =============================================================

# --- SETUP ---
import os
import re
import warnings
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

warnings.filterwarnings("ignore")
load_dotenv()

llm = ChatOpenAI(model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.getenv("OPENROUTER_API_KEY"),
                 temperature=0, max_retries=3)

emb = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2",
                            encode_kwargs={"normalize_embeddings": True})


def load_or_build_handbook_db(path="chroma_partner_handbook"):
    if os.path.isdir(path):
        db = Chroma(collection_name="partner_handbook", embedding_function=emb,
                    persist_directory=path)
        if db.get()["ids"]:
            return db
    text = open("partner_handbook.txt", encoding="utf-8").read()
    docs = []
    for sec in re.split(r"\n## ", text)[1:]:
        title, body = sec.split("\n", 1)
        docs.append(Document(page_content=body.strip(), metadata={"section": title.strip()}))
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80).split_documents(docs)
    return Chroma.from_documents(chunks, emb, collection_name="partner_handbook",
                                 persist_directory=path)


retriever = load_or_build_handbook_db().as_retriever(search_kwargs={"k": 3})

# Synthetic weekly stats. P-20417's numbers are the Rs 600 story from 14.1.
PARTNER_STATS = {
    "P-20417": {"last_week": {"orders": 62, "peak": 40, "cancels": 0, "rain": 0},
                "this_week": {"orders": 62, "peak": 20, "cancels": 3, "rain": 0}},
    "P-33150": {"last_week": {"orders": 55, "peak": 25, "cancels": 1, "rain": 0},
                "this_week": {"orders": 48, "peak": 20, "cancels": 0, "rain": 12}},
}


# --- EXPLAIN ---
# Concept Block 2: a tool = Python function + name + DESCRIPTION.
# The docstring is the ONLY thing the LLM reads to choose a tool,
# so it says what the tool does, what input it wants, and when to use it.
# ReAct agents pass ONE string as input, so each tool takes one string.
# -------------------------------------------------------------

@tool
def search_handbook(question: str) -> str:
    """Search the official Swiggy partner handbook for POLICY and RULES (payout schedule,
    bonuses, deductions, disputes, bank details, insurance, safety, app issues).
    Input: a short question. Returns handbook passages with section names."""
    docs = retriever.invoke(question)
    return "\n\n".join(f"[{d.metadata['section']}] {d.page_content}" for d in docs)


@tool
def get_partner_stats(partner_id: str) -> str:
    """Look up a partner's raw numbers for this week and last week: orders, peak-hour
    orders, cancellations, rain-alert orders. Input: a partner ID like P-20417."""
    stats = PARTNER_STATS.get(partner_id.strip().strip("'\""))
    return str(stats) if stats else f"No partner found with ID {partner_id}."


def weekly_payout(w):
    base, peak = w["orders"] * 30, w["peak"] * 15
    target = 400 if w["orders"] >= 60 else 0
    rain, deduct = w["rain"] * 10, w["cancels"] * 100
    total = base + peak + target + rain - deduct
    return total, f"base {base} + peak {peak} + target {target} + rain {rain} - deductions {deduct} = Rs {total}"


@tool
def calculate_weekly_payout(partner_id: str) -> str:
    """Calculate EXACT payout amounts for this week and last week with a full breakdown.
    Use this for any question about how much a partner earned or why a payout changed.
    Input: a partner ID like P-20417."""
    stats = PARTNER_STATS.get(partner_id.strip().strip("'\""))
    if not stats:
        return f"No partner found with ID {partner_id}."
    last_total, last_text = weekly_payout(stats["last_week"])
    this_total, this_text = weekly_payout(stats["this_week"])
    return (f"Last week: {last_text}\nThis week: {this_text}\n"
            f"Difference: Rs {this_total - last_total}")


tools = [search_handbook, get_partner_stats, calculate_weekly_payout]
for t in tools:
    print(f"TOOL {t.name}: {t.description[:70]}...")

print("\nDirect tool call:", calculate_weekly_payout.invoke("P-20417"))


# --- EXPLAIN ---
# Concept Blocks 3-4: the ReAct prompt. {tools} and {tool_names} list
# the tools; {agent_scratchpad} holds every Thought/Action/Observation
# so far. create_react_agent builds the decision-maker; AgentExecutor
# runs the loop, with a step cap and format-error recovery.
# -------------------------------------------------------------

from langchain.agents import AgentExecutor, create_react_agent

react_prompt = PromptTemplate.from_template(
    """You are Swiggy's delivery-partner helpdesk agent. Use tools for policy, partner
numbers and payout maths - never guess amounts or rules. Cite handbook sections.
If the tools can't answer, say a human support agent will follow up.

You have access to these tools:
{tools}

Use this format:
Question: the input question
Thought: think about what to do next
Action: one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: the answer for the partner, under 100 words

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

agent = create_react_agent(llm, tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                         max_iterations=6, handle_parsing_errors=True)


# --- EXPLAIN ---
# Concept Block 5: tool selection. Watch the verbose trace - each
# question should trigger different tools (or none).
# -------------------------------------------------------------

questions = [
    "How do I change my bank account?",
    "I'm P-33150. Did I get rain bonus this week, and how much?",
    "Why is my payout Rs 600 less this week? My ID is P-20417.",
]
for q in questions:
    print("\n" + "=" * 70 + f"\nQUESTION: {q}")
    result = executor.invoke({"input": q})
    print("\nFINAL:", result["output"])


# --- EXPLAIN ---
# Concept Block 6: safety limits. A question no tool can answer, with
# a tight cap of 2 steps - the executor stops instead of looping.
# -------------------------------------------------------------

capped = AgentExecutor(agent=agent, tools=tools, verbose=True,
                       max_iterations=2, handle_parsing_errors=True)
print("\nCAPPED:", capped.invoke({"input": "What will P-20417 earn next month?"})["output"])


# --- EXPLAIN ---
# The older one-liner you'll see in tutorials: initialize_agent builds
# a ReAct agent + executor in one call, with LangChain's own prompt.
# -------------------------------------------------------------

from langchain.agents import initialize_agent, AgentType

classic = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                           verbose=False, max_iterations=6, handle_parsing_errors=True)
print("\nCLASSIC:", classic.invoke({"input": "What is the payout for P-33150 this week?"})["output"])


# --- EXPLAIN ---
# What this demo does NOT do yet: we never MEASURED whether the
# agent's answers are correct and faithful to the handbook, and nothing
# stops a partner asking for another partner's data (try "show me
# P-33150's stats" while claiming to be P-20417). Session 18.1 adds
# RAGAS evaluation and guardrails; Session 18.2 turns this hidden loop
# into an explicit LangGraph flow you can design and debug.
# -------------------------------------------------------------
