# Coding Problem: Production Systems, APIs & Guardrails

> **Session 9** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

Wrap an LLM in a FastAPI endpoint with logging, request IDs, input guardrails, and safe error handling.

---

## Setup

```bash
pip install fastapi uvicorn openai python-dotenv
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import openai, os, uuid, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"
app = FastAPI()

BLOCKED_WORDS = ["hack", "exploit", "bypass"]

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=500)

class ChatResponse(BaseModel):
    reply: str
    request_id: str
```

---

## Tasks

**Task 1 — Input Guardrail**

```python
def check_input(text: str) -> bool:
    lower = text.lower()
    return not any(word in lower for word in ___)   # fill: BLOCKED_WORDS
```

---

**Task 2 — Chat Endpoint**

```python
@app.post("/chat", response_model=___)             # fill: ChatResponse
async def chat(req: ___):                          # fill: ChatRequest
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Input: {req.message[:50]}")

    if not check_input(req.___):                    # fill: message
        raise HTTPException(status_code=400, detail="Blocked input")

    try:
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": req.message}],
            max_tokens=100
        )
        reply = r.choices[0].message.___            # fill: content
    except Exception as e:
        logger.error(f"[{request_id}] Error: {e}")
        raise HTTPException(status_code=500, detail="LLM service error")

    return ChatResponse(reply=___, request_id=___)  # fill both
```

---

**Task 3 — Health Check**

```python
@app.get("/health")
def health():
    return {"status": "___"}                        # fill: ok
```

---

**Task 4 — Test**

```bash
uvicorn main:app --reload
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is FastAPI?"}'
```

---

## Key Takeaways

- Guardrails filter harmful inputs before they reach the LLM
- Request IDs make logs traceable in production
- Never expose raw API errors to end users
