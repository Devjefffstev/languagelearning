"""
FastAPI server wrapping the LangGraph agent from graph.py.

Run:
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env  # then add your real ANTHROPIC_API_KEY
    python main.py

Endpoint:
    POST /chat
    Body: { "message": "What is 23 * 47?", "thread_id": "optional-default-user" }
    Returns: { "reply": "23 times 47 equals 1081." }
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load .env before importing graph so the key is present at module import time
load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
    )

from graph import chat as graph_chat  # noqa: E402

app = FastAPI(title="LangGraph Agent (Anthropic)")

# Permissive CORS so the local Pages site (http://localhost:8788) can call us.
# In production, lock this down to your Pages origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default-user"


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {
        "service": "langgraph-agent",
        "llm": "anthropic",
        "endpoints": {"POST /chat": "Send a message, get a reply."},
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="`message` must not be empty.")
    try:
        reply = graph_chat(req.message, thread_id=req.thread_id)
    except Exception as e:
        # Surface the error in the response so the front-end can show it.
        raise HTTPException(status_code=500, detail=f"Agent error: {e!s}")
    return ChatResponse(reply=reply)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("AGENT_PORT", "8000"))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)