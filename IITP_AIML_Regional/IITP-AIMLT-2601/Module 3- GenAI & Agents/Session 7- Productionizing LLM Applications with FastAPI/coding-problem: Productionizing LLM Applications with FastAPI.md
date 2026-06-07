# Coding Problem: Productionizing LLM Applications with FastAPI

> **Session 7** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

You are wrapping an LLM chat endpoint in a FastAPI application — the kind of backend that powers real AI products. You will define request/response schemas with Pydantic, handle secrets via environment variables, and add basic logging with request IDs.

---

## Setup

```bash
pip install fastapi uvicorn openai python-dotenv
```

Create a `.env` file in the same folder:

```
OPENROUTER_API_KEY=sk-or-...
```

---

## Tasks

**Task 1 — Pydantic Schemas**

Define the request and response models for the `/chat` endpoint.

```python
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message:     str
    system:      Optional[str] = "You are a helpful assistant."
    temperature: float         = Field(default=0.7, ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    reply:       str
    request_id:  str
    model_used:  str
    tokens_used: ___    # fill: data type (int)
```

---

**Task 2 — Load Secrets Safely**

Fill in the blanks to load the API key from `.env` — never hardcode keys in source code.

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("___")    # fill: env variable name

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not set in environment")
```

---

**Task 3 — Build the FastAPI App**

Fill in the `/chat` endpoint. It should log each request with a unique ID, call the LLM, and return a `ChatResponse`.

```python
from fastapi import FastAPI
import openai, uuid, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"
app   = FastAPI(title="LLM Chat API")

@app.post("/chat", response_model=___)         # fill: response model class
async def chat(req: ___):                      # fill: request model class
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Received: {req.message[:60]}")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": req.___},    # fill: system field
            {"role": "user",   "content": req.___}     # fill: message field
        ],
        temperature=req.___                            # fill: temperature field
    )

    reply      = response.choices[0].message.content
    tokens     = response.usage.total_tokens
    model_used = response.model

    logger.info(f"[{request_id}] Tokens used: {tokens}")

    return ChatResponse(
        reply=___,           # fill
        request_id=___,      # fill
        model_used=___,      # fill
        tokens_used=___      # fill
    )
```

---

**Task 4 — Add a Health Check Route**

Add a simple `/health` endpoint that returns `{"status": "ok"}`. Standard for any production API.

```python
@app.get("/health")
def health():
    return ___    # fill: the dict
```

---

**Task 5 — Run and Test**

Start the server:

```bash
uvicorn main:app --reload
```

Test with `curl` or open `http://localhost:8000/docs` in your browser:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is FastAPI?", "temperature": 0}'
```

**Expected response shape:**
```json
{
  "reply": "FastAPI is a modern, high-performance web framework...",
  "request_id": "a3f9c1b2",
  "model_used": "meta-llama/llama-3.3-70b-instruct:free",
  "tokens_used": 87
}
```

---

## Key Takeaways

- Pydantic schemas validate inputs at the boundary — bad requests fail fast before hitting the LLM
- `uuid4()` request IDs make logs traceable across distributed services
- `load_dotenv()` + `os.getenv()` is the standard pattern for secrets — never commit API keys to git
