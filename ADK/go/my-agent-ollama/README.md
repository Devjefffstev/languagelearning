# Ollama ADK Agent

A Go-based AI agent built on [Google Agent Development Kit (ADK)](https://adk.dev) that runs on Ollama models — locally or on Ollama Cloud.

## Prerequisites

- Go (the module requires Go 1.25.6)
- An Ollama Cloud API key (from https://ollama.com/settings/keys) — only needed for cloud mode

## Setup

Copy or edit `.env` with your configuration:

```bash
# Local Ollama server
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="gemma3:latest"

# Ollama Cloud (set this to switch to cloud mode)
export OLLAMA_API_KEY="your-api-key"
export OLLAMA_CLOUD_MODEL="gemma4:31b"
```

## Run

### Cloud mode

`OLLAMA_API_KEY` must be set and non-empty:

```bash
source .env && go run . "What time is it in Tokyo?"
```

### Local mode

Unset or comment out `OLLAMA_API_KEY`:

```bash
unset OLLAMA_API_KEY && source .env && go run . "What time is it in Tokyo?"
```

Or comment it out in `.env`:

```bash
# export OLLAMA_API_KEY="..."
source .env && go run . "What time is it in Tokyo?"
```

Or override with an inline env:

```bash
OLLAMA_API_KEY="" source .env && go run . "What time is it in Tokyo?"
```

### Web UI mode

```bash
source .env && go run . web api webui
```

## How switching works

The agent checks the presence of `OLLAMA_API_KEY`:

| `OLLAMA_API_KEY` | Base URL | Model |
|---|---|---|
| Set | `https://ollama.com/v1` | `OLLAMA_CLOUD_MODEL` (or `OLLAMA_MODEL`) |
| Empty/unset | `OLLAMA_BASE_URL` + `/v1` | `OLLAMA_MODEL` |

## Troubleshooting

**401 Unauthorized**: If you see this when `OLLAMA_API_KEY` is set, the key may be invalid or expired. Generate a new one at https://ollama.com/settings/keys. Also verify you are hitting `ollama.com` (not `api.ollama.com`) — the `api.` subdomain redirects and drops the auth header.

**Model not found**: Make sure the model name exists on the server you're targeting. Cloud and local models are independent — a model pulled locally may not be available on cloud and vice versa.
