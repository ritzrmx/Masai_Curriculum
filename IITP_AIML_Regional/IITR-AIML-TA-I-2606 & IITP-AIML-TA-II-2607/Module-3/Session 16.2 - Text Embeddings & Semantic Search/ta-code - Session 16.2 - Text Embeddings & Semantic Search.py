# =============================================================
# Session 16.2: Text Embeddings & Semantic Search
# TA Live Coding Demo - ~5 min typing, under 10 min total
# Scenario: A partner types "where is my money" - let's see which
# helpdesk messages keyword search finds, and which ones meaning-
# based search finds.
#
# Syntax scope check: NumPy, Matplotlib (Module 1), the cosine
# formula (Session 14.2), plus today's new tools:
# sentence-transformers, HuggingFaceEmbeddings, PCA for plotting.
# NO API key needed - the embedding model runs on your laptop.
#
# Install once:
#   pip install sentence-transformers "langchain-huggingface<1" scikit-learn numpy matplotlib
# First run downloads the model (~470 MB) from Hugging Face.
# =============================================================

# --- SETUP ---
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"   # handles Hindi/Hinglish


# --- EXPLAIN ---
# Concept Blocks 1-2: an embedding model turns each sentence into
# a vector of 384 numbers. Downloaded once, then free to run.
# normalize_embeddings=True makes every vector length 1 (Session 14.2).
# -------------------------------------------------------------

model = SentenceTransformer(MODEL_NAME)

docs = [
    "Payout not credited since Friday",
    "kal ka paisa nahi aaya",
    "Weekly amount still showing pending",
    "Rain bonus not added for yesterday's orders",
    "mera peak hour bonus kahan hai",
    "App keeps crashing when I go online",
    "GPS shows the wrong location",
    "Mera app login nahi ho raha",
    "A customer threatened me at the gate",
    "I had a small accident, bike damaged",
    "Where is the nearest hub?",
    "P-20417 needs a callback",
]
labels = ["payout", "payout", "payout", "incentive", "incentive",
          "app", "app", "app", "safety", "safety", "other", "other"]

doc_vecs = model.encode(docs, normalize_embeddings=True)
print("Embedding matrix shape:", doc_vecs.shape)
print("First 5 numbers of doc 0:", np.round(doc_vecs[0][:5], 3))
print("Length of doc 0 vector:", round(float(np.linalg.norm(doc_vecs[0])), 4))


# --- EXPLAIN ---
# Concept Block 3: cosine similarity by the 14.2 formula, then the
# dot product. Because vectors are normalised, they are IDENTICAL.
# -------------------------------------------------------------

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


for i, j in [(0, 1), (0, 2), (0, 5)]:
    print(f"\n'{docs[i]}' vs '{docs[j]}'")
    print(f"   cosine = {cosine(doc_vecs[i], doc_vecs[j]):.3f} | dot = {np.dot(doc_vecs[i], doc_vecs[j]):.3f}")


# --- EXPLAIN ---
# Concept Block 4: keyword search = count shared words.
# Semantic search = embed the query, rank docs by cosine.
# -------------------------------------------------------------

def keyword_search(query, k=3):
    q_words = set(query.lower().replace("?", "").split())
    scores = [len(q_words & set(d.lower().replace("?", "").split())) for d in docs]
    order = np.argsort(scores)[::-1][:k]
    return [(docs[i], scores[i]) for i in order]


def semantic_search(query, k=3):
    q_vec = model.encode(query, normalize_embeddings=True)
    scores = doc_vecs @ q_vec               # dot product with every doc at once
    order = np.argsort(scores)[::-1][:k]
    return [(docs[i], round(float(scores[i]), 3)) for i in order]


for query in ["where is my money", "bonus missing hai", "P-20417"]:
    print(f"\nQUERY: {query}")
    print("  keyword :", keyword_search(query))
    print("  semantic:", semantic_search(query))


# --- EXPLAIN ---
# Read the "P-20417" result out loud: an ID has no "meaning", so
# keyword search is the reliable one there. Semantic for meaning,
# keyword for exact codes - many real systems use both.
# -------------------------------------------------------------


# --- EXPLAIN ---
# Concept Block 5: the same model through LangChain's standard
# interface. Session 16.3 hands this "emb" object to a vector store.
# -------------------------------------------------------------

from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name=MODEL_NAME,
                            encode_kwargs={"normalize_embeddings": True})
q = emb.embed_query("where is my money")
d = emb.embed_documents(docs[:2])
print("\nLangChain query vector length:", len(q))
print("Same scores as before?", round(float(np.dot(q, d[0])), 3))


# --- EXPLAIN ---
# Concept Block 6: squash 384 numbers to 2 with PCA, just for a
# picture. Colour by topic - meaning groups appear on the plot.
# -------------------------------------------------------------

from sklearn.decomposition import PCA

points = PCA(n_components=2, random_state=42).fit_transform(doc_vecs)
colours = {"payout": "tab:green", "incentive": "tab:olive", "app": "tab:blue",
           "safety": "tab:red", "other": "tab:gray"}

plt.figure(figsize=(7, 5))
for (x, y), text, lab in zip(points, docs, labels):
    plt.scatter(x, y, color=colours[lab])
    plt.annotate(text[:28], (x, y), fontsize=7)
plt.title("Partner messages in 'meaning space' (PCA to 2D)")
plt.grid(True); plt.show()


# --- EXPLAIN ---
# What this demo does NOT do yet: we compared the query with all 12
# messages one by one. A real handbook has thousands of chunks, and
# long pages must be split first. Session 16.3 adds chunking and vector
# stores (ChromaDB, FAISS) that search millions of vectors fast.
# -------------------------------------------------------------
