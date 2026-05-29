package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strings"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/runner"

	genaiopenai "github.com/achetronic/adk-utils-go/genai/openai"
	"google.golang.org/adk/cmd/launcher"
	"google.golang.org/adk/cmd/launcher/full"
	"google.golang.org/adk/session"
	"google.golang.org/genai"
)

const (
	appName   = "state_inject_app"
	userID    = "state_inject_user"
	sessionID = "state_inject_session"
)

func main() {
	ctx := context.Background()
	sessionService := session.InMemoryService()

	// 1. Initialize a session with a 'topic' in its state.
	_, err := sessionService.Create(ctx, &session.CreateRequest{
		AppName:   appName,
		UserID:    userID,
		SessionID: sessionID,
		State: map[string]any{
			"topic": "friendship",
		},
	})
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}

	// 2. Create an agent with an instruction that uses a {topic} placeholder.
	//    The ADK will automatically inject the value of "topic" from the
	//    session state into the instruction before calling the LLM.
	apiKey := strings.TrimSpace(os.Getenv("OLLAMA_API_KEY"))
	var baseURL string
	var modelName string

	if apiKey != "" {
		baseURL = "https://ollama.com"
		modelName = strings.TrimSpace(os.Getenv("OLLAMA_CLOUD_MODEL"))
	} else {
		baseURL = strings.TrimSpace(os.Getenv("OLLAMA_BASE_URL"))
		if baseURL == "" {
			baseURL = "http://localhost:11434"
		}
		modelName = strings.TrimSpace(os.Getenv("OLLAMA_MODEL"))
	}
	if modelName == "" {
		modelName = "gemma3:latest"
	}

	model := genaiopenai.New(genaiopenai.Config{
		APIKey:    apiKey,
		BaseURL:   baseURL + "/v1",
		ModelName: modelName,
	})
	fmt.Printf("Using model: %s\n", modelName)
	s, err := sessionService.Get(ctx, &session.GetRequest{AppName: appName, UserID: userID, SessionID: sessionID})
	if err != nil {
		log.Fatalf("Failed to get session: %v", err)
	}
	vael_state, _ := s.Session.State().Get("topic")

	fmt.Println(vael_state)
// Add this before creating the agent
initTopic := func(ctx agent.CallbackContext) (*genai.Content, error) {
    if _, err := ctx.State().Get("topic"); err != nil {
        ctx.State().Set("topic", "friendship")
    }
    return nil, nil
}
	storyGenerator, err := llmagent.New(llmagent.Config{
		Name:        "StoryGenerator",
		Model:       model,		
		Instruction: "Write a short story (50 words) about a cat, focusing on the theme: {topic}.",
		BeforeAgentCallbacks: []agent.BeforeAgentCallback{initTopic},  // add this

	})
	if err != nil {
		log.Fatalf("Failed to create agent: %v", err)
	}

	r, err := runner.New(runner.Config{
		AppName:        appName,
		Agent:          agent.Agent(storyGenerator),
		SessionService: sessionService,
	})

	fmt.Printf("Initialized runner: %p\n", r)
	if err != nil {
		log.Fatalf("Failed to create runner: %v", err)
	}

	config := &launcher.Config{
		AgentLoader:    agent.NewSingleLoader(storyGenerator),
		SessionService: sessionService,
	}

	l := full.NewLauncher()
	if err = l.Execute(ctx, config, os.Args[1:]); err != nil {
		log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
	}
}
