// Package greetingagent provides the greeting_agent sub-agent.
// Model and endpoint are configured via GREETING_AGENT_MODEL and OLLAMA_LOCAL_BASE_URL env vars.
package greetingagent

import (
	"fmt"
	"os"

	litellmmodel "agent-team/model"
	"agent-team/tools"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	adktool "google.golang.org/adk/tool"
)

// New creates and returns the greeting_agent.
// Model and base URL are configured via GREETING_AGENT_MODEL and OLLAMA_LOCAL_BASE_URL env vars.
func New() (agent.Agent, error) {
	baseURL := os.Getenv("OLLAMA_LOCAL_BASE_URL")
	if baseURL == "" {
		baseURL = "http://192.168.1.121:11434/v1"
	}

	modelName := os.Getenv("GREETING_AGENT_MODEL")
	if modelName == "" {
		modelName = "llama3.2:1b"
	}

	m, err := litellmmodel.New(litellmmodel.Config{
		ModelName: modelName,
		BaseURL:   baseURL,
		APIKey:    "ollama",
	})
	if err != nil {
		return nil, fmt.Errorf("greeting agent: model init: %w", err)
	}

	helloTool, err := tools.NewSayHelloTool()
	if err != nil {
		return nil, fmt.Errorf("greeting agent: tool init: %w", err)
	}

	return llmagent.New(llmagent.Config{
		Name:  "greeting_agent",
		Model: m,
		Description: "Handles simple greetings and hellos using the 'say_hello' tool.",
		Instruction: "You are the Greeting Agent. Your ONLY task is to greet the user with the 'say_hello' tool. " +
			"ALWAYS call the 'say_hello' tool to respond — never reply without calling it. " +
			"If the user mentions their name (e.g. 'my name is Alice', 'I'm Bob', 'call me Jeff'), " +
			"you MUST extract the name and pass it as the 'name' argument to say_hello. " +
			"If no name is mentioned, call say_hello with an empty name.",
		Tools:                    []adktool.Tool{helloTool},
		DisallowTransferToParent: true,
		DisallowTransferToPeers:  true,
	})
}
