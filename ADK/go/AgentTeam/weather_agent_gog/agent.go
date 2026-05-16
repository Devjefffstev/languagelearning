// Package weatheragentgog provides the weather_agent_gog sub-agent.
// Model and endpoint are configured via WEATHER_AGENT_MODEL and OLLAMA_LOCAL_BASE_URL env vars.
package weatheragentgog

import (
	"fmt"
	"os"

	litellmmodel "agent-team/model"
	"agent-team/tools"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	adktool "google.golang.org/adk/tool"
)

// New creates and returns the weather_agent_gog agent.
// Model and base URL are configured via WEATHER_AGENT_MODEL and OLLAMA_LOCAL_BASE_URL env vars.
func New() (agent.Agent, error) {
	baseURL := os.Getenv("OLLAMA_LOCAL_BASE_URL")
	if baseURL == "" {
		baseURL = "http://192.168.1.121:11434/v1"
	}

	modelName := os.Getenv("WEATHER_AGENT_MODEL")
	if modelName == "" {
		modelName = "gemma4:e2b"
	}

	m, err := litellmmodel.New(litellmmodel.Config{
		ModelName: modelName,
		BaseURL:   baseURL,
		APIKey:    "ollama",
	})
	if err != nil {
		return nil, fmt.Errorf("weather agent: model init: %w", err)
	}

	weatherTool, err := tools.NewGetWeatherTool()
	if err != nil {
		return nil, fmt.Errorf("weather agent: tool init: %w", err)
	}

	return llmagent.New(llmagent.Config{
		Name:        "weather_agent_gog",
		Model:       m,
		Description: "Provides the current weather for a specific city.",
		Instruction: "You are a weather assistant. Your ONLY job is to report the weather for the city the user asks about. " +
			"ALWAYS call the 'get_weather' tool with the city name extracted from the user's message. " +
			"Then present the result clearly. Do not do anything else.",
		Tools:                    []adktool.Tool{weatherTool},
		DisallowTransferToParent: true,
		DisallowTransferToPeers:  true,
	})
}
