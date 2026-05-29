//Basic agent that uses Ollama-hosted models via OpenAI-compatible API.
// https://adk.dev/agents/models/ollama/
//
// Usage:
//   source .env && go run . "What time is it in Tokyo?"          (CLI mode)
//   source .env && go run . "fetch the page https://example.com" (CLI with fetchPage tool)
//   source .env && go run . web api webui                         (Web UI + REST API mode)
//   source .env && go run . --prompt "hello, Im jeff" web api webui (Web UI with pre-seeded prompt)
package main

import (
	"bufio"
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	genaiopenai "github.com/achetronic/adk-utils-go/genai/openai"
	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/artifact"
	"google.golang.org/adk/cmd/launcher"
	"google.golang.org/adk/cmd/launcher/full"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"google.golang.org/adk/tool"
	"google.golang.org/genai"

	"webui-agent/tools"
)

func main() {
	promptPtr := flag.String("prompt", "", "Pre-seed the Web UI chat with an initial prompt.")
	flag.Parse()
	args := flag.Args()

	ctx := context.Background()

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

	ag, err := llmagent.New(llmagent.Config{
		Name:        "family_support_agent",
		Model:       model,
		Description: "A helpful family support agent that can answer questions and search the internet.",
		Instruction: "You are a helpful family support assistant. Answer questions helpfully and use searchInternet to look up current information when needed.",
		Tools: []tool.Tool{
			tools.SearchInternet{},
			tools.FetchPage{},
		},
	})
	if err != nil {
		log.Fatalf("Failed to create agent: %v", err)
	}

	if len(args) > 0 && (args[0] == "web" || args[0] == "api" || args[0] == "webui" || args[0] == "a2a" || args[0] == "console") {
		runServer(ctx, ag, args, *promptPtr)
		return
	}

	if *promptPtr != "" {
		args = append([]string{*promptPtr}, args...)
	}
	runCLI(ctx, ag, args)
}

func runServer(ctx context.Context, ag agent.Agent, args []string, initialPrompt string) {
	ss := session.InMemoryService()

	if initialPrompt != "" {
		ss = &promptSeedingService{Service: ss, prompt: initialPrompt, agent: ag}
	}

	agentLoader := agent.NewSingleLoader(ag)

	config := &launcher.Config{
		AgentLoader:     agentLoader,
		SessionService:  ss,
		ArtifactService: artifact.InMemoryService(),
	}

	l := full.NewLauncher()
	if err := l.Execute(ctx, config, args); err != nil {
		log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
	}
}

type promptSeedingService struct {
	session.Service
	prompt string
	seeded bool
	agent  agent.Agent
}

func (s *promptSeedingService) Create(ctx context.Context, req *session.CreateRequest) (*session.CreateResponse, error) {
	resp, err := s.Service.Create(ctx, req)
	if err != nil {
		return resp, err
	}
	if s.prompt != "" && !s.seeded {
		s.seeded = true
		go func() {
			r, err := runner.New(runner.Config{
				AppName:        req.AppName,
				Agent:          s.agent,
				SessionService: s.Service,
			})
			if err != nil {
				return
			}
			userMsg := genai.NewContentFromText(s.prompt, "user")
			for range r.Run(context.Background(), req.UserID, resp.Session.ID(), userMsg, agent.RunConfig{}) {
			}
		}()
	}
	return resp, nil
}

func runCLI(ctx context.Context, ag agent.Agent, args []string) {
	prompt := strings.Join(args, " ")
	if prompt == "" {
		prompt = "What time is it in Tokyo?"
	}

	srv := session.InMemoryService()
	r, err := runner.New(runner.Config{
		AppName:        "demo",
		Agent:          ag,
		SessionService: srv,
	})
	if err != nil {
		log.Fatalf("Failed to create runner: %v", err)
	}

	resp, err := srv.Create(ctx, &session.CreateRequest{
		AppName: "demo",
		UserID:  "user1",
	})
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}

	sessionID := resp.Session.ID()
	reader := bufio.NewReader(os.Stdin)

	for {
		msg := prompt
		if prompt == "" {
			fmt.Print("\nYou: ")
			msg, _ = reader.ReadString('\n')
			msg = strings.TrimSpace(msg)
			if msg == "" {
				continue
			}
		}
		prompt = ""

		userMsg := genai.NewContentFromText(msg, "user")
		fmt.Print("Agent: ")
		for event, err := range r.Run(ctx, "user1", sessionID, userMsg, agent.RunConfig{}) {
			if err != nil {
				log.Fatalf("Run error: %v", err)
			}
			if event.IsFinalResponse() {
				for _, part := range event.Content.Parts {
					if part.Text != "" {
						fmt.Print(part.Text)
					}
				}
				fmt.Println()
			}
		}
	}
}
