# AGENTS

Detailed description of every agent in this team.

---

## orchestrator

| Field | Value |
|---|---|
| **Model** | `gemini-2.5-flash` (Google AI) |
| **Package** | `agent-team/orchestrator` |
| **Tools** | `geminitool.GoogleSearch` |
| **Sub-agents** | `weather_agent_gog`, `greeting_agent`, `farewell_agent` |

### Behaviour

The orchestrator is the entry point for all user interactions. It inspects the
user's intent and delegates to the most appropriate sub-agent:

- Weather queries → `weather_agent_gog`
- Greetings / hellos → `greeting_agent`
- Farewells / goodbyes → `farewell_agent`
- General knowledge → Google Search (handled directly)

---

## weather_agent_gog

| Field | Value |
|---|---|
| **Model** | `gemma4:e2b` (Ollama local · `192.168.1.121:11434`) |
| **Package** | `agent-team/weather_agent_gog` |
| **Tools** | `get_weather` |
| **Sub-agents** | — |

### `get_weather` tool

```
get_weather(city: string) → {status, report?, error_message?}
```

Returns a mock weather report for the given city. A production deployment
should replace the in-memory lookup with a real weather API call.

---

## greeting_agent

| Field | Value |
|---|---|
| **Model** | `llama3.2:1b` (Ollama local · `192.168.1.121:11434`) |
| **Package** | `agent-team/greeting_agent` |
| **Tools** | `say_hello` |
| **Sub-agents** | — |

### `say_hello` tool

```
say_hello(name?: string) → string
```

Returns `"Hello, <name>!"` when a name is provided, or `"Hello there!"` otherwise.

---

## farewell_agent

| Field | Value |
|---|---|
| **Model** | `gemma4:31b-cloud` (Ollama Cloud) |
| **Package** | `agent-team/farewell_agent` |
| **Tools** | `say_goodbye` |
| **Sub-agents** | — |

The farewell agent base URL defaults to `https://api.ollama.com/v1` and can be
overridden by setting the `OLLAMA_CLOUD_BASE_URL` environment variable.
The API key is read from `OLLAMA_CLOUD_API_KEY`.

### `say_goodbye` tool

```
say_goodbye() → string
```

Returns the static farewell message `"Goodbye! Have a great day."`.

---

## LiteLLM Adapter (`model/litellm_adapter.go`)

Custom implementation of `model.LLM` that bridges the ADK's `genai`-based
request/response format to the OpenAI-compatible wire format consumed by
Ollama (and any other OpenAI-compatible endpoint).

Conversion summary:

| ADK / genai | litellm / OpenAI |
|---|---|
| `Content{Role: "user"}` | `Message{Role: "user"}` |
| `Content{Role: "model"}` | `Message{Role: "assistant"}` |
| `Part.FunctionCall` | assistant message with `ToolCalls` |
| `Part.FunctionResponse` | `Message{Role: "tool", ToolCallID: ...}` |
| `Config.SystemInstruction` | `Message{Role: "system"}` (prepended) |
| `Config.Tools[].FunctionDeclarations` | `Request.Tools` |
