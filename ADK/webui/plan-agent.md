# Plan: Create ADK Go Web UI Agent

## Goal
Create a Go-based ADK agent at `/Users/jeffersonsoto/Documents/personalGitHub/languagelearning/ADK/webui/agent/` that runs with Web UI + REST API and supports `--prompt` to pre-seed the initial conversation.

## Source
Copied from `/Users/jeffersonsoto/Documents/personalGitHub/languagelearning/ADK/go/my-agent-ollama/` (working Ollama agent).

---

## Files to Create

### 1. `agent/agent.go`
- Copied from source with module import changed: `firts-agent/tools` → `webui-agent/tools`
- Added `--prompt` flag parsing that works in **both** CLI and web modes
- In web mode: if `--prompt` is provided, it pre-seeds the first session with that message so it appears in the Web UI chat

### 2. `agent/go.mod`
- Module name: `webui-agent`
- Same dependencies as source:
  - `github.com/achetronic/adk-utils-go v0.16.0`
  - `google.golang.org/adk v1.2.0`
  - `google.golang.org/genai v1.56.0`

### 3. `agent/tools/fetch.go`
- Exact copy from source

### 4. `agent/tools/search.go`
- Exact copy from source

### 5. `agent/.env`
```bash
export OLLAMA_BASE_URL="http://192.168.1.172:11434"
export OLLAMA_MODEL="g4:e2b-64k"
```

---

## Run Command
```bash
cd /Users/jeffersonsoto/Documents/personalGitHub/languagelearning/ADK/webui/agent
source .env && go run agent.go --prompt "hello, Im jeff" web api webui
```

---

## Test & Confirmation

### Steps
1. **Verify server started** — console should show server running on `http://localhost:8000`
2. **Open browser** — navigate to `http://localhost:8000`
3. **Check the chat** — Web UI should show:
   - **User message**: `hello, Im jeff`
   - **Agent response**: model reply from Ollama

### If prompt NOT visible
- Diagnose: `--prompt` may not pass through to web mode session correctly
- Fix options:
  - Use ADK API `/run` endpoint to seed message into a session before Web UI connects
  - Inject via launcher's session service
  - Pre-create session with prompt in `runServer()`

### If prompt visible but NO agent response
- Check Ollama connectivity on `192.168.1.172:11434`
- Verify `g4:e2b-64k` model is pulled and available

### If Web UI shows empty chat
- Pivot: use `/run` API to seed the message into a session the Web UI picks up

---

## Implementation Steps
1. Create directory structure `agent/tools/`
2. Write `agent.go` (with `--prompt` support for web mode)
3. Write `go.mod`
4. Copy `tools/fetch.go` and `tools/search.go`
5. Write `.env`
6. Run `go mod tidy` to generate `go.sum`
7. Test: `source .env && go run agent.go --prompt "hello, Im jeff" web api webui`
8. Verify prompt appears in Web UI at `http://localhost:8000`
