# Agent Team

A multi-agent system built with the [Google Agent Development Kit (ADK) for Go](https://adk.dev/get-started/go/). An orchestrator agent powered by Gemini routes user requests to specialized sub-agents running on different LLM backends via [litellm](https://pkg.go.dev/github.com/voocel/litellm).

## Architecture

```
orchestrator  (gemini-2.5-flash)
├── weather_agent_gog  (gemma4:e2b    · local Ollama  · get_weather)
├── greeting_agent     (llama3.2:1b   · local Ollama  · say_hello)
└── farewell_agent     (gemma4:31b-cloud · Ollama Cloud · say_goodbye)
```

| Agent | Model | Backend | Tools |
|---|---|---|---|
| `orchestrator` | `gemini-2.5-flash` | Google AI | — |
| `weather_agent_gog` | `gemma4:e2b` | Ollama local `192.168.1.121:11434` | `get_weather` |
| `greeting_agent` | `llama3.2:1b` | Ollama local `192.168.1.121:11434` | `say_hello` |
| `farewell_agent` | `gemma4:31b-cloud` | Ollama Cloud | `say_goodbye` |

## Prerequisites

- Go 1.24.4+
- A Google AI API key ([AI Studio](https://aistudio.google.com/app/apikey))
- Local Ollama running (see setup below) with `gemma4:e2b` and `llama3.2:1b` pulled
- Ollama Cloud credentials (optional, only for `farewell_agent`)

## Local Ollama Setup

### Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull required models

```bash
ollama pull gemma4:e2b       # weather_agent_gog  (~3 GB)
ollama pull llama3.2:1b      # greeting_agent     (~1 GB)
```

### Configure the Ollama host

The sub-agents point to `192.168.1.121:11434` by default (a remote Ollama host on the same LAN). To use your **local** machine instead:

1. Start Ollama (it listens on `localhost:11434` by default):
   ```bash
   ollama serve
   ```
2. Update the base URL in each sub-agent file:

   | File | Constant to change |
   |---|---|
   | `weather_agent_gog/agent.go` | `ollamaBaseURL` |
   | `greeting_agent/agent.go` | `ollamaBaseURL` |

   ```go
   // Change this:
   const ollamaBaseURL = "http://192.168.1.121:11434/v1"
   // To:
   const ollamaBaseURL = "http://localhost:11434/v1"
   ```

### Ollama Cloud (optional — farewell_agent only)

```bash
echo 'export OLLAMA_CLOUD_BASE_URL="https://api.ollama.com/v1"' >> .env
echo 'export OLLAMA_CLOUD_API_KEY="YOUR_OLLAMA_CLOUD_KEY"'     >> .env
```

## Setup

```bash
# 1. Clone / enter the project
cd AgentTeam

# 2. Add your Google API key to .env
echo 'export GOOGLE_API_KEY="YOUR_API_KEY"' >> .env

# 3. Load environment variables
source .env

# 4. Install dependencies
go mod tidy
```

## Running

### CLI (no UI)

```bash
source .env && go run main.go
```

## Testing

### ADK Web UI (with pre-loaded demo session)

```bash
source .env && go run main.go web api webui
```

Before starting the server, this automatically runs the five demo messages through all agents and stores the conversation in an in-memory session. When the UI opens, you'll already see the full conversation history:

1. Open [http://localhost:8080](http://localhost:8080)
2. Select the **orchestrator** agent
3. Click on the **demo-session** (user: `demo-user`) — it will contain all pre-seeded messages

| Pre-seeded message | Routed to |
|---|---|
| `"Hello! My name is Alice."` | `greeting_agent` |
| `"What is the weather in London?"` | `weather_agent_gog` |
| `"What is the weather in New York?"` | `weather_agent_gog` |
| `"Hi there, I'm Bob!"` | `greeting_agent` |
| `"Goodbye, it was nice talking to you!"` | `farewell_agent` |

### Programmatic Test Runner

Runs the same five messages and prints responses to stdout without the web UI:

```bash
source .env && go run cmd/test_runner/main.go
```

## Project Layout

```
AgentTeam/
├── main.go                    # Entry point (ADK full launcher)
├── cmd/
│   └── test_runner/
│       └── main.go            # Programmatic test runner (pre-loaded messages)
├── model/
│   └── litellm_adapter.go     # model.LLM → litellm bridge (Ollama support)
├── tools/
│   ├── weather.go             # get_weather tool
│   └── greeting.go            # say_hello / say_goodbye tools
├── orchestrator/
│   └── agent.go               # Root orchestrator (Gemini)
├── weather_agent_gog/
│   └── agent.go               # Weather sub-agent (Ollama local)
├── greeting_agent/
│   └── agent.go               # Greeting sub-agent (Ollama local)
├── farewell_agent/
│   └── agent.go               # Farewell sub-agent (Ollama Cloud)
├── go.mod
├── .env
├── README.md
└── AGENTS.md
```

## Key Dependencies

| Package | Purpose |
|---|---|
| `google.golang.org/adk` | Agent framework, runner, launcher |
| `google.golang.org/genai` | Gemini types & client |
| `github.com/voocel/litellm` | OpenAI-compatible LLM client (Ollama bridge) |
