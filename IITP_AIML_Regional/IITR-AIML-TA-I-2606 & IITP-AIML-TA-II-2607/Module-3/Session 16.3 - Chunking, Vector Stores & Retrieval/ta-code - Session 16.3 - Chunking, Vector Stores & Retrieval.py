# =============================================================
# Session 16.3: Chunking, Vector Stores & Retrieval
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: From 12 short messages to the whole Partner Handbook -
# let's chunk it, store it in ChromaDB and FAISS, and pull back
# the right section for a partner's question in milliseconds.
#
# Syntax scope check: HuggingFaceEmbeddings (16.2), plus today's new
# tools: RecursiveCharacterTextSplitter, Document, Chroma, FAISS,
# similarity search, MMR, as_retriever(). Still NO LLM - connecting
# retrieval to an LLM is Session 17.1 (RAG).
#
# Install once:
#   pip install "langchain-text-splitters<1" "langchain-community<1" "langchain-chroma<1" \
#               "langchain-huggingface<1" sentence-transformers chromadb faiss-cpu
# Put partner_handbook.txt (provided) next to this script.
# =============================================================

# --- SETUP ---
import re
import shutil
import time
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

handbook = open("partner_handbook.txt", encoding="utf-8").read()
print("Handbook length:", len(handbook), "characters")


# --- EXPLAIN ---
# Keep each section's title as METADATA, so every chunk remembers
# where it came from. Later we can show "Source: 4. Safety" to the
# partner, and filter by section.
# -------------------------------------------------------------

sections = re.split(r"\n## ", handbook)[1:]        # skip the title line
section_docs = []
for sec in sections:
    title, body = sec.split("\n", 1)
    section_docs.append(Document(page_content=body.strip(), metadata={"section": title.strip()}))

print("Sections:", [d.metadata["section"] for d in section_docs])


# --- EXPLAIN ---
# Concept Blocks 1-2: RecursiveCharacterTextSplitter tries to cut at
# paragraphs first, then lines, then spaces - so chunks end at natural
# breaks. chunk_size and chunk_overlap are in CHARACTERS.
# Try three settings and compare.
# -------------------------------------------------------------

for size, overlap in [(200, 0), (500, 80), (1500, 150)]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    pieces = splitter.split_documents(section_docs)
    print(f"chunk_size={size:<5} overlap={overlap:<4} -> {len(pieces):3} chunks")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
chunks = splitter.split_documents(section_docs)
print("\nSample chunk:\n", chunks[3].page_content, "\nMetadata:", chunks[3].metadata)


# --- SETUP ---
emb = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2",
                            encode_kwargs={"normalize_embeddings": True})


# --- EXPLAIN ---
# Concept Block 3: ChromaDB - a vector DATABASE that saves to disk.
# from_documents() embeds every chunk and stores vector + text + metadata.
# We delete the folder first: re-running from_documents on the same
# folder ADDS duplicates (a classic trap).
# -------------------------------------------------------------

from langchain_chroma import Chroma

shutil.rmtree("chroma_partner_handbook", ignore_errors=True)
chroma_db = Chroma.from_documents(chunks, emb, collection_name="partner_handbook",
                                  persist_directory="chroma_partner_handbook")
print("\nChroma stored", len(chroma_db.get()["ids"]), "chunks on disk")


# --- EXPLAIN ---
# Concept Block 3: FAISS - a fast in-memory INDEX (a library, not a
# server). Save it with save_local() if you want it later.
# -------------------------------------------------------------

from langchain_community.vectorstores import FAISS

faiss_db = FAISS.from_documents(chunks, emb)
faiss_db.save_local("faiss_partner_handbook")


# --- EXPLAIN ---
# Concept Block 4: similarity search - embed the question, return the
# k closest chunks. Both stores return a DISTANCE here: LOWER = closer.
# Note the question is Hinglish; the handbook is English.
# -------------------------------------------------------------

question = "bonus nahi mila barish wale din"

for name, db in [("Chroma", chroma_db), ("FAISS", faiss_db)]:
    start = time.perf_counter()
    results = db.similarity_search_with_score(question, k=3)
    ms = (time.perf_counter() - start) * 1000
    print(f"\n{name} ({ms:.0f} ms):")
    for doc, dist in results:
        print(f"  dist={dist:.3f} [{doc.metadata['section']}] {doc.page_content[:80]}...")


# --- EXPLAIN ---
# Concept Block 5: MMR - Maximal Marginal Relevance. Fetch fetch_k
# candidates, then pick k that are relevant BUT different from each
# other. lambda_mult: 1.0 = pure relevance, 0.0 = pure variety.
# Compare plain similarity vs MMR for a broad question.
# -------------------------------------------------------------

broad = "how is my weekly payout calculated"

print("\nPlain similarity:")
for doc in chroma_db.similarity_search(broad, k=3):
    print("  -", doc.page_content[:90], "...")

print("\nMMR (more variety):")
for doc in chroma_db.max_marginal_relevance_search(broad, k=3, fetch_k=10, lambda_mult=0.5):
    print("  -", doc.page_content[:90], "...")


# --- EXPLAIN ---
# Concept Block 6: a VectorStoreRetriever - one standard object with
# .invoke(question) -> list of Documents. This is the exact object
# Session 17.1 plugs into a RAG chain.
# Metadata filter: only search the Safety section.
# -------------------------------------------------------------

retriever = chroma_db.as_retriever(search_type="mmr",
                                   search_kwargs={"k": 3, "fetch_k": 10})
docs = retriever.invoke("I fell off my bike during a delivery, what do I do?")
print("\nRetriever returned sections:", [d.metadata["section"] for d in docs])

safety_only = chroma_db.as_retriever(search_kwargs={"k": 2, "filter": {"section": "4. Safety and Insurance"}})
print("Safety-filtered:", [d.page_content[:60] for d in safety_only.invoke("claim")])


# --- EXPLAIN ---
# Reload from disk to prove Chroma persisted (FAISS needs load_local).
# -------------------------------------------------------------

reloaded = Chroma(collection_name="partner_handbook", embedding_function=emb,
                  persist_directory="chroma_partner_handbook")
print("\nReloaded Chroma has", len(reloaded.get()["ids"]), "chunks")


# --- EXPLAIN ---
# What this demo does NOT do yet: it returns CHUNKS, not answers. A
# partner doesn't want to read three paragraphs of handbook - they want
# "Your rain bonus is Rs 10 per order; raise a dispute within 7 days."
# Session 17.1 feeds these retrieved chunks to an LLM: that's RAG.
# -------------------------------------------------------------
