# =============================================================
# Session 17.1: Building a RAG Pipeline
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: The 11:40 pm partner finally gets answers from the
# real handbook - same questions, LLM alone vs LLM + retrieval.
#
# Syntax scope check: ChatOpenAI + templates (15.1), HuggingFace
# embeddings (16.2), Chroma + retrievers (16.3), plus today's new
# tools: RetrievalQA, create_stuff_documents_chain,
# create_retrieval_chain. No agents or tools yet (Session 17.2).
#
# Install once:
#   pip install "langchain==0.3.*" "langchain-openai==0.3.*" "langchain-text-splitters<1" \
#               "langchain-chroma<1" "langchain-huggingface<1" sentence-transformers chromadb python-dotenv
# Put partner_handbook.txt (provided) next to this script.
# .env needs OPENROUTER_API_KEY (and optionally OPENROUTER_MODEL)
# =============================================================

# --- SETUP ---
import os
import re
import warnings
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

warnings.filterwarnings("ignore")
load_dotenv()

llm = ChatOpenAI(model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.getenv("OPENROUTER_API_KEY"),
                 temperature=0, max_tokens=250, max_retries=3)

emb = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2",
                            encode_kwargs={"normalize_embeddings": True})


# --- SETUP ---
# Load the Chroma store from Session 16.3 if it exists; otherwise
# build it the same way (sections -> metadata -> 500/80 chunks).
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


db = load_or_build_handbook_db()
retriever = db.as_retriever(search_kwargs={"k": 4})
print("Handbook chunks in store:", len(db.get()["ids"]))

questions = [
    "When is my payout credited if Friday is a bank holiday?",
    "bonus nahi mila barish wale din, kya karun?",
    "How much accident insurance do I get?",
    "Can I deliver on a bicycle?",
]


# --- EXPLAIN ---
# Concept Block 5 (first half): UNGROUNDED - the LLM alone, no
# handbook. Watch how confident and how wrong (or vague) it can be.
# -------------------------------------------------------------

print("\n========== UNGROUNDED (LLM alone) ==========")
for q in questions:
    print(f"\nQ: {q}\nA: {llm.invoke(q + ' (Answer in under 60 words.)').content}")


# --- EXPLAIN ---
# Concept Block 2: context injection. {context} receives the
# retrieved chunks; the fallback line handles "not in handbook".
# Concept Block 4: create_stuff_documents_chain stuffs the chunks
# into {context}; create_retrieval_chain runs the retriever first.
# -------------------------------------------------------------

from langchain.chains import create_retrieval_chain, RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain

rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are Swiggy's delivery-partner helpdesk.\n"
     "Answer ONLY using the handbook context below.\n"
     "If the answer is not in the context, reply exactly: "
     "'I couldn't find this in the handbook - I'll connect you to a support agent.'\n"
     "Reply in the partner's language, under 80 words, and mention the section number(s).\n\n"
     "Handbook context:\n{context}"),
    ("human", "{input}"),
])

combine_docs_chain = create_stuff_documents_chain(llm, rag_prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

print("\n========== GROUNDED (RAG) ==========")
for q in questions:
    out = rag_chain.invoke({"input": q})
    sources = sorted({d.metadata["section"] for d in out["context"]})
    print(f"\nQ: {q}\nA: {out['answer']}\n   sources: {sources}")


# --- EXPLAIN ---
# Concept Block 3: the classic RetrievalQA does the same job in one
# call. Note the different blank names ({question}, not {input}) and
# output keys ("result", "source_documents").
# -------------------------------------------------------------

qa_prompt = PromptTemplate.from_template(
    "You are Swiggy's partner helpdesk. Answer ONLY from this handbook context. "
    "If it's not there, say you couldn't find it.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\nAnswer (under 60 words):")

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                 return_source_documents=True,
                                 chain_type_kwargs={"prompt": qa_prompt})

out = qa.invoke({"query": "How many days do I have to report an accident?"})
print("\nRetrievalQA answer:", out["result"])
print("RetrievalQA sources:", [d.metadata["section"] for d in out["source_documents"]])


# --- EXPLAIN ---
# Concept Block 6: diagnose a wrong answer. Force a BAD retriever
# (k=1, filtered to the wrong section) and see the model answer
# faithfully from the wrong chunk. That's a RETRIEVAL failure -
# rewriting the prompt would not fix it.
# -------------------------------------------------------------

bad_retriever = db.as_retriever(search_kwargs={"k": 1, "filter": {"section": "2. Incentives"}})
bad_chain = create_retrieval_chain(bad_retriever, combine_docs_chain)
out = bad_chain.invoke({"input": "How many days do I have to report an accident?"})
print("\nWith a bad retriever:", out["answer"])
print("It only saw:", out["context"][0].page_content[:90], "...")


# --- EXPLAIN ---
# What this demo does NOT do yet: the bot can only READ the handbook.
# It can't calculate a partner's payout, or look up their weekly stats.
# Session 17.2 gives an agent TOOLS and lets it decide which to use.
# And we compared answers by eye - Session 18.1 measures them with
# RAGAS (faithfulness, context recall, answer correctness).
# -------------------------------------------------------------
