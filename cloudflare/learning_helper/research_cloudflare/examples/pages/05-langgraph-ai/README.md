# 05 - LangGraph AI Agent (called from Pages)

The first non-JS example. It takes the "Pages calls a backend" pattern from example 04 and points it at a **Python LangGraph agent** that uses a non-OpenAI LLM (Anthropic Claude by default). It exists to answer one question: how do I wire an agent framework that isn't on the Cloudflare runtime, and still keep the API key out of the browser?

The agent is a canonical LangGraph pattern: one LLM node, one tool node, one conditional edge. The tool is a safe calculator so the whole thing is testable end-to-end with no external APIs beyond the LLM itself.

## Layout

```
05-langgraph-ai/
├── README.md                     <- you are here
├── agent/                        <- the Python LangGraph agent (FastAPI)
│   ├── main.py
│   ├── graph.py
│   ├── requirements.txt
│   └── .env.example
└── site/                         <- the Pages site that calls the agent
    ├── package.json
    ├── wrangler.jsonc
    ├── public/
    │   ├── index.html
    │   ├── app.js
    │   └── style.css
    └── functions/
        └── api/
            └── chat.ts
```

## Prerequisites

- **Python 3.11+** with `pip` and `venv`
- **Node.js 18+** and `npm` (for the Pages site / wrangler)
- An **Anthropic API key** — get one at https://console.anthropic.com. (Free tier gives a few dollars of credit; enough to try this example dozens of times.)

## Run it (local dev, three terminals)

```bash
# Terminal 1 — the LangGraph agent
cd agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then put your real ANTHROPIC_API_KEY in .env
python main.py             # -> http://localhost:8000
```

```bash
# Terminal 2 — the Pages site
cd site
npm install
printf 'AGENT_URL="http://localhost:8000/chat"\n' > .dev.vars
npm run dev                # -> http://localhost:8788
```

Then open `http://localhost:8788` in a browser. Type a message. Try:
- `"What is 23 * 47?"` — the agent will call the calculator tool, then answer in prose.
- `"What is the capital of France?"` — no tool needed, straight LLM answer.
- `"Compute (12 + 8) * 3, then add 100."` — multi-step, demonstrates the loop.

## How the agent works

The graph has three nodes and one conditional edge:

```
        ┌─────────┐
   ───▶ │   llm   │ ─── tool_calls? ───▶ ┌──────────┐
        └─────────┘                       │   tool   │
              ▲                           └──────────┘
              │                                 │
              └─────────────── always ──────────┘
```

1. **State** is just a list of messages (`messages: list[BaseMessage]`).
2. **`llm` node** calls Claude with the current message history + a description of the `calculator` tool.
3. **Conditional edge** — if the LLM's response includes a `tool_call`, route to the `tool` node. Otherwise, end the graph.
4. **`tool` node** runs the requested tool (only `calculator` for now) and appends the result as a `ToolMessage`. Then we go back to `llm` so it can write a final answer grounded in the tool's output.

`graph.py` defines the graph; `main.py` wraps it in a FastAPI app with one endpoint:

```
POST /chat
Content-Type: application/json
Body: { "message": "What is 23 * 47?" }

→ 200 OK
{ "reply": "23 times 47 equals 1081." }
```

## How to swap the LLM (the whole point of this example)

The model-agnostic part of LangGraph is the chat model class. To swap providers, change the import and the class — nothing else moves:

| Provider | Import | Class |
|---|---|---|
| **Anthropic (default)** | `from langchain_anthropic import ChatAnthropic` | `ChatAnthropic(model="claude-haiku-4-5", ...)` |
| OpenAI | `from langchain_openai import ChatOpenAI` | `ChatOpenAI(model="gpt-4o-mini", ...)` |
| Google Gemini | `from langchain_google_genai import ChatGoogleGenerativeAI` | `ChatGoogleGenerativeAI(model="gemini-2.0-flash", ...)` |
| Groq | `from langchain_groq import ChatGroq` | `ChatGroq(model="llama-3.1-8b-instant", ...)` |
| Cloudflare Workers AI (via AI Gateway) | `from langchain_openai import ChatOpenAI` | `ChatOpenAI(base_url="https://gateway.ai.cloudflare.com/v1/<acct>/<gw>/openai", api_key=..., model="@cf/meta/llama-3.1-8b-instruct-fp8-fast")` |

All of them implement the same `BaseChatModel` interface, so the graph, the state, and the tool-calling loop stay identical. The `requirements.txt` already includes `langchain-anthropic`; uncomment the matching line and add the provider's SDK to switch.

## How the Pages function calls the agent

`site/functions/api/chat.ts` is the bridge. It accepts a POST from the browser, forwards it to the agent URL (read from the `AGENT_URL` Pages env var / `.dev.vars`), and returns the agent's reply. The `ANTHROPIC_API_KEY` lives only in the agent's process — the browser never sees it, the Pages function never sees it.

## Deploying

The agent is a regular Python service, so it goes anywhere Python runs (Fly.io, Railway, Render, a VM, your laptop). The Pages site deploys with `wrangler pages deploy public`. Set `AGENT_URL` to your deployed agent's public URL in the Cloudflare dashboard under the Pages project's **Settings → Environment variables**.

For local dev, `wrangler pages dev` reads `.dev.vars`, which is why the run-it steps put `AGENT_URL` there.