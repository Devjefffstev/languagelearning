// cmd/test_runner/main.go
// Programmatic test runner that exercises all agents.
// Run: go run cmd/test_runner/main.go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"google.golang.org/genai"

	"agent-team/orchestrator"
)

func main() {
	ctx := context.Background()

	root, err := orchestrator.New(ctx)
	if err != nil {
		log.Fatalf("failed to create orchestrator: %v", err)
	}

	r, err := runner.New(runner.Config{
		AppName:           "agent-team-test",
		Agent:             root,
		SessionService:    session.InMemoryService(),
		AutoCreateSession: true,
	})
	if err != nil {
		log.Fatalf("failed to create runner: %v", err)
	}

	userID := "test-user"
	sessionID := "test-session-001"

	// Pre-load messages that exercise every agent.
	messages := []string{
		"Hello! My name is Alice.",           // → greeting_agent
		"What is the weather in London?",     // → weather_agent_gog
		"What is the weather in New York?",   // → weather_agent_gog
		"Hi there, I'm Bob!",                 // → greeting_agent
		"Goodbye, it was nice talking to you!", // → farewell_agent
	}

	fmt.Fprintf(os.Stderr, "=== Agent Team Test Runner ===\n\n")

	for _, msg := range messages {
		fmt.Printf("────────────────────────────────────────\n")
		fmt.Printf("USER: %s\n", msg)

		userContent := &genai.Content{
			Role:  "user",
			Parts: []*genai.Part{{Text: msg}},
		}

		var finalResponse string
		for event, err := range r.Run(ctx, userID, sessionID, userContent, agent.RunConfig{}) {
			if err != nil {
				fmt.Printf("ERROR: %v\n", err)
				break
			}
			if event.IsFinalResponse() && event.LLMResponse.Content != nil {
				for _, p := range event.LLMResponse.Content.Parts {
					if p.Text != "" {
						finalResponse = p.Text
					}
				}
			}
		}

		if finalResponse != "" {
			fmt.Printf("AGENT: %s\n", finalResponse)
		} else {
			fmt.Printf("AGENT: (no text response)\n")
		}
	}

	fmt.Printf("────────────────────────────────────────\n")
	fmt.Fprintf(os.Stderr, "\n=== Test complete ===\n")
}
