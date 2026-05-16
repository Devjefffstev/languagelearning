// Package farewellagent provides the farewell_agent sub-agent.
// Model and endpoint are configured via FAREWELL_AGENT_MODEL, OLLAMA_CLOUD_BASE_URL,
// and OLLAMA_CLOUD_API_KEY env vars.
package farewellagent

import (
	"fmt"
	"os"

	litellmmodel "agent-team/model"
	"agent-team/tools"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	adktool "google.golang.org/adk/tool"
)

// ollamaCloudBaseURL is the Ollama Cloud OpenAI-compatible endpoint.
// Override with OLLAMA_CLOUD_BASE_URL environment variable if needed.
const ollamaCloudBaseURL = "https://api.ollama.com/v1"

// New creates and returns the farewell_agent.
// All config is read from env vars: FAREWELL_AGENT_MODEL, OLLAMA_CLOUD_BASE_URL, OLLAMA_CLOUD_API_KEY.
func New() (agent.Agent, error) {
	baseURL := os.Getenv("OLLAMA_CLOUD_BASE_URL")
	if baseURL == "" {
		baseURL = ollamaCloudBaseURL
	}

	apiKey := os.Getenv("OLLAMA_CLOUD_API_KEY")
	if apiKey == "" {
		apiKey = "ollama"
	}

	modelName := os.Getenv("FAREWELL_AGENT_MODEL")
	if modelName == "" {
		modelName = "gemma4:31b-cloud"
	}

	m, err := litellmmodel.New(litellmmodel.Config{
		ModelName: modelName,
		BaseURL:   baseURL,
		APIKey:    apiKey,
	})
	if err != nil {
		return nil, fmt.Errorf("farewell agent: model init: %w", err)
	}

	goodbyeTool, err := tools.NewSayGoodbyeTool()
	if err != nil {
		return nil, fmt.Errorf("farewell agent: tool init: %w", err)
	}

	return llmagent.New(llmagent.Config{
		Name:        "farewell_agent",
		Model:       m,
		Description: "Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
		Instruction: "You are the Farewell Agent. Your ONLY task is to say goodbye. " +
			"ALWAYS call the 'say_goodbye' tool to respond — never reply without calling it.",
		Tools:                    []adktool.Tool{goodbyeTool},
		DisallowTransferToParent: true,
		DisallowTransferToPeers:  true,
	})
}
