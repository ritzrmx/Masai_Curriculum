# =============================================================
# Session 18.2: Agent Orchestration with LangGraph
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: All of Module 3 in one flowchart - guardrails, handbook
# retrieval, the answer, the number check, one retry, and a human
# fallback - built as an explicit LangGraph flow.
#
# Syntax scope check: retriever (16.3), RAG prompt (17.1), guardrails
# and number check (18.1), plus today's new tools: TypedDict state,
# StateGraph, add_node, add_edge, add_conditional_edges, START, END,
# compile(), get_graph().draw_mermaid().
#
# Install once:
#   pip install "langchain==0.3.*" "langchain-openai==0.3.*" "langchain-text-splitters<1" \
#               "langchain-chroma<1" "langchain-huggingface<1" "langgraph<1" \
#               sentence-transformers chromadb python-dotenv
# Put partner_handbook.txt (provided) next to this script.
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# =============================================================

# --- SETUP ---
import os
import re
import warnings
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

warnings.filterwarnings("ignore")
load_dotenv()

llm = ChatOpenAI(model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.getenv("OPENROUTER_API_KEY"),
                 temperature=0, max_tokens=200, max_retries=3)
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


retriever = load_or_build_handbook_db().as_retriever(search_kwargs={"k": 4})


# --- EXPLAIN ---
# Concept Block 2: the STATE - one typed dictionary that travels
# through every node. Each node reads what it needs and returns
# only the keys it changes.
# -------------------------------------------------------------

class HelpdeskState(TypedDict):
    partner_id: str
    question: str
    route: str
    context: List[str]
    answer: str
    check_passed: bool
    attempts: int


# --- EXPLAIN ---
# Concept Block 3: NODES are plain functions. These reuse 18.1's
# guardrails and number check, and 17.1's RAG prompt idea.
# -------------------------------------------------------------

SAFETY_WORDS = ["threat", "hurt", "injured", "harass", "dhamki", "maara"]
INJECTION = ["ignore previous", "ignore your instructions", "system prompt"]


def guard(state: HelpdeskState) -> dict:
    q = re.sub(r"\b[6-9]\d{9}\b", "[PHONE]", state["question"])
    low = q.lower()
    if any(p in low for p in INJECTION):
        return {"question": q, "route": "block"}
    if any(w in low for w in SAFETY_WORDS):
        return {"question": q, "route": "escalate"}
    if set(re.findall(r"P-\d+", q)) - {state["partner_id"]}:
        return {"question": q, "route": "block"}
    return {"question": q, "route": "ok"}


def refuse(state: HelpdeskState) -> dict:
    return {"answer": "Sorry, I can only help with questions about your own partner account."}


def human(state: HelpdeskState) -> dict:
    return {"answer": "Connecting you to the safety team now. Press SOS in the app if you're in danger."}


def retrieve(state: HelpdeskState) -> dict:
    return {"context": [d.page_content for d in retriever.invoke(state["question"])]}


def answer(state: HelpdeskState) -> dict:
    strict = ("\nThis is a RETRY: your last answer used a number not in the handbook. "
              "Quote every amount and time limit EXACTLY as written.") if state["attempts"] > 0 else ""
    prompt = ("You are Swiggy's partner helpdesk. Answer ONLY from the handbook context, under "
              "60 words, in the partner's language, citing section numbers. If it's not there, "
              "say you couldn't find it." + strict +
              "\n\nContext:\n" + "\n\n".join(state["context"]) +
              "\n\nQuestion: " + state["question"])
    reply = llm.invoke(prompt).content
    if state.get("force_bad_first") and state["attempts"] == 0:      # demo only: fake a hallucination
        reply = "Accident cover is Rs 5,00,000."
    return {"answer": reply, "attempts": state["attempts"] + 1}


def numbers_in(text):
    return set(re.findall(r"\d+", text.replace(",", "")))


def check(state: HelpdeskState) -> dict:
    unsupported = numbers_in(state["answer"]) - numbers_in(" ".join(state["context"]))
    return {"check_passed": len(unsupported) == 0}


def fallback(state: HelpdeskState) -> dict:
    return {"answer": "I couldn't confirm this from the handbook - I'll connect you to a support agent."}


# --- EXPLAIN ---
# Concept Blocks 3-5: build the graph. add_node registers boxes,
# add_edge draws fixed arrows, add_conditional_edges draws branches
# chosen by tiny routing functions. Every path must reach END.
# -------------------------------------------------------------

from langgraph.graph import StateGraph, START, END

MAX_ATTEMPTS = 2


def route_after_guard(state: HelpdeskState) -> str:
    return state["route"]


def route_after_check(state: HelpdeskState) -> str:
    if state["check_passed"]:
        return "done"
    return "retry" if state["attempts"] < MAX_ATTEMPTS else "give_up"


class DemoState(HelpdeskState, total=False):
    force_bad_first: bool          # only used to demo the retry path


graph = StateGraph(DemoState)
for name, fn in [("guard", guard), ("refuse", refuse), ("human", human),
                 ("retrieve", retrieve), ("answer", answer), ("check", check),
                 ("fallback", fallback)]:
    graph.add_node(name, fn)

graph.add_edge(START, "guard")
graph.add_conditional_edges("guard", route_after_guard,
                            {"ok": "retrieve", "block": "refuse", "escalate": "human"})
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", "check")
graph.add_conditional_edges("check", route_after_check,
                            {"done": END, "retry": "answer", "give_up": "fallback"})
for last in ["refuse", "human", "fallback"]:
    graph.add_edge(last, END)

app = graph.compile()
print(app.get_graph().draw_mermaid())       # the flow, as a mermaid diagram


# --- EXPLAIN ---
# Run four journeys and print the FINAL STATE for each - the route
# taken, how many attempts, whether the check passed.
# -------------------------------------------------------------

def run(question, partner_id="P-20417", **extra):
    start = {"partner_id": partner_id, "question": question, "route": "", "context": [],
             "answer": "", "check_passed": False, "attempts": 0, **extra}
    final = app.invoke(start)
    print(f"\nQ: {question}\n  route={final['route']} attempts={final['attempts']} "
          f"check_passed={final['check_passed']}\n  A: {final['answer']}")


run("How much is the rain bonus?")                                 # happy path
run("What was P-33150's payout this week?")                         # privacy block
run("customer ne gate pe dhamki di")                                # safety escalation
run("How much accident insurance do I get?", force_bad_first=True)  # retry path


# --- EXPLAIN ---
# Concept Block 6: compare with AgentExecutor (17.2). There, "always
# check safety first" and "retry once with stricter rules" were only
# requests in a prompt. Here they are GUARANTEED by the graph's edges.
#
# What this demo does NOT do: put the full 17.2 agent inside a node.
# You can - replace the retrieve/answer nodes with an agent node, and
# the graph still guarantees the guardrails and checks around it.
# -------------------------------------------------------------
