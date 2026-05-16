// Package orchestrator provides the root orchestrator agent that routes
// incoming user requests to the appropriate sub-agent.
package orchestrator

import (
	"context"
	"fmt"
	"os"
	"strings"

	farewellagent "agent-team/farewell_agent"
	greetingagent "agent-team/greeting_agent"
	litellmmodel "agent-team/model"
	weatheragentgog "agent-team/weather_agent_gog"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	adkmodel "google.golang.org/adk/model"
	"google.golang.org/adk/model/gemini"
	"google.golang.org/genai"
)

// New creates and returns the orchestrator agent together with all configured sub-agents.
// ORCHESTRATOR_MODEL selects the model (default: gemini-2.5-flash).
// Models starting with "gemini-" use the Gemini SDK; all others use the local Ollama
// litellm adapter via OLLAMA_LOCAL_BASE_URL.
func New(ctx context.Context) (agent.Agent, error) {
	modelName := os.Getenv("ORCHESTRATOR_MODEL")
	if modelName == "" {
		modelName = "gemini-2.5-flash"
	}

	var m adkmodel.LLM
	var err error

	if strings.HasPrefix(modelName, "gemini-") {
		m, err = gemini.NewModel(ctx, modelName, &genai.ClientConfig{
			APIKey: os.Getenv("GOOGLE_API_KEY"),
		})
		if err != nil {
			return nil, fmt.Errorf("orchestrator: gemini model init: %w", err)
		}
	} else {
		baseURL := os.Getenv("OLLAMA_LOCAL_BASE_URL")
		if baseURL == "" {
			baseURL = "http://192.168.1.121:11434/v1"
		}
		m, err = litellmmodel.New(litellmmodel.Config{
			ModelName: modelName,
			BaseURL:   baseURL,
			APIKey:    "ollama",
		})
		if err != nil {
			return nil, fmt.Errorf("orchestrator: ollama model init: %w", err)
		}
	}

	// Build all sub-agents.
	weatherAgent, err := weatheragentgog.New()
	if err != nil {
		return nil, fmt.Errorf("orchestrator: %w", err)
	}

	greetingAgent, err := greetingagent.New()
	if err != nil {
		return nil, fmt.Errorf("orchestrator: %w", err)
	}

	farewellAgent, err := farewellagent.New()
	if err != nil {
		return nil, fmt.Errorf("orchestrator: %w", err)
	}

	return llmagent.New(llmagent.Config{
		Name:        "orchestrator",
		Model:       m,
		Description: "Orchestrator of the conversation",
		Instruction: "You are a helpful orchestrator that receives a prompt and routes it to the " +
			"specific sub-agent best suited for the task. " +
			"- For weather questions, delegate to 'weather_agent_gog'. " +
			"- For greetings or hellos, delegate to 'greeting_agent'. " +
			"- For farewells or goodbyes, delegate to 'farewell_agent'.",
		SubAgents: []agent.Agent{
			weatherAgent,
			greetingAgent,
			farewellAgent,
		},
	})
}
