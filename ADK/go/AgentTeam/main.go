// Agent Team – multi-agent system built with Google ADK for Go.
//
// Agents:
//   - orchestrator      (gemma4:e2b  via localhost Ollama)
//   - weather_agent_gog (gemma4:e2b  via local Ollama  + get_weather)
//   - greeting_agent    (llama3.2:1b via local Ollama  + say_hello)
//   - farewell_agent    (gemma4:31b-cloud via Ollama Cloud + say_goodbye)
//
// Run:
//
//	source .env && go run main.go web api webui
package main

import (
	"context"
	"log"
	"os"
	"slices"

	"agent-team/orchestrator"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/cmd/launcher"
	"google.golang.org/adk/cmd/launcher/full"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"google.golang.org/genai"
)

// preloadMessages are seeded into the demo session so the web UI shows
// a real conversation covering every agent on first open.
var preloadMessages = []string{
	"Hello! My name is Alice.",
	"What is the weather in London?",
	"What is the weather in New York?",
	"Hi there, I'm Bob!",
	"Goodbye, it was nice talking to you!",
}

func main() {
	ctx := context.Background()

	root, err := orchestrator.New(ctx)
	if err != nil {
		log.Fatalf("Failed to build agent team: %v", err)
	}

	svc := session.InMemoryService()

	// Pre-seed a demo session when starting the web UI so all agents are
	// visible in the conversation history before the browser is opened.
	if slices.Contains(os.Args[1:], "web") {
		log.Println("Pre-seeding demo session for web UI…")
		if seedErr := seedSession(ctx, root, svc); seedErr != nil {
			log.Printf("Warning: demo session seeding failed: %v", seedErr)
		} else {
			log.Println("Demo session ready — open http://localhost:8080 and select 'orchestrator'.")
		}
	}

	config := &launcher.Config{
		AgentLoader:    agent.NewSingleLoader(root),
		SessionService: svc,
	}

	l := full.NewLauncher()
	if err = l.Execute(ctx, config, os.Args[1:]); err != nil {
		log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
	}
}

// seedSession runs preloadMessages through the runner and stores the full
// conversation in svc under a fixed user/session so the web UI can display it.
func seedSession(ctx context.Context, root agent.Agent, svc session.Service) error {
	const appName = "orchestrator"
	const userID = "demo-user"
	const sessionID = "demo-session"

	r, err := runner.New(runner.Config{
		AppName:           appName,
		Agent:             root,
		SessionService:    svc,
		AutoCreateSession: true,
	})
	if err != nil {
		return err
	}

	for _, msg := range preloadMessages {
		userContent := &genai.Content{
			Role:  "user",
			Parts: []*genai.Part{{Text: msg}},
		}
		for _, iterErr := range r.Run(ctx, userID, sessionID, userContent, agent.RunConfig{}) {
			if iterErr != nil {
				return iterErr
			}
		}
	}
	return nil
}
