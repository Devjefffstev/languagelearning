// Loop Agent – iterative document improvement using Google ADK for Go.
//
// Uses a LoopAgent to repeatedly critique and refine a document until
// the critic signals completion or the max iteration count is reached.
//
// Usage:
//
//	source .env && go run main.go
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strings"

	genaiopenai "github.com/achetronic/adk-utils-go/genai/openai"
	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/agent/workflowagents/loopagent"
	"google.golang.org/adk/agent/workflowagents/sequentialagent"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"google.golang.org/adk/tool"
	"google.golang.org/adk/tool/functiontool"
	"google.golang.org/genai"
)

const (
	appName    = "IterativeWritingPipeline"
	userID     = "writer_user"
	stateDoc   = "current_document"
	stateCrit  = "criticism"
	donePhrase = "No major issues found."
)

// ExitLoopArgs defines the (empty) arguments for the ExitLoop tool.
type ExitLoopArgs struct{}

// ExitLoopResults defines the output of the ExitLoop tool.
type ExitLoopResults struct{}

// ExitLoop is a tool that signals the loop to terminate by setting Escalate to true.
func ExitLoop(ctx tool.Context, input ExitLoopArgs) (ExitLoopResults, error) {
	fmt.Printf("[Tool Call] exitLoop triggered by %s \n", ctx.AgentName())
	ctx.Actions().Escalate = true
	return ExitLoopResults{}, nil
}

func main() {
	ctx := context.Background()

	if err := runAgent(ctx, "Write a document about a cat"); err != nil {
		log.Fatalf("Agent execution failed: %v", err)
	}
}

func runAgent(ctx context.Context, prompt string) error {
	// Ollama model setup — mirrors orchestrator.go pattern.
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

	// STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
	initialWriterAgent, err := llmagent.New(llmagent.Config{
		Name:        "InitialWriterAgent",
		Model:       model,
		Description: "Writes the initial document draft based on the topic.",
		Instruction: `You are a Creative Writing Assistant tasked with starting a story.
Write the *first draft* of a short story (aim for 2-4 sentences).
Base the content *only* on the topic provided in the user's prompt.
Output *only* the story/document text. Do not add introductions or explanations.`,
		OutputKey: stateDoc,
	})
	if err != nil {
		return fmt.Errorf("failed to create initial writer agent: %v", err)
	}

	// STEP 2a: Critic Agent (Inside the Refinement Loop)
	criticAgentInLoop, err := llmagent.New(llmagent.Config{
		Name:        "CriticAgent",
		Model:       model,
		Description: "Reviews the current draft, providing critique or signaling completion.",
		Instruction: fmt.Sprintf(`You are a Constructive Critic AI reviewing a short document draft.
**Document to Review:**
"""
{%s}
"""
**Task:**
Review the document.
IF you identify 1-2 *clear and actionable* ways it could be improved:
Provide these specific suggestions concisely. Output *only* the critique text.
ELSE IF the document is coherent and addresses the topic adequately:
Respond *exactly* with the phrase "%s" and nothing else.`, stateDoc, donePhrase),
		OutputKey: stateCrit,
	})
	if err != nil {
		return fmt.Errorf("failed to create critic agent: %v", err)
	}

	exitLoopTool, err := functiontool.New(
		functiontool.Config{
			Name:        "exitLoop",
			Description: "Call this function ONLY when the critique indicates no further changes are needed.",
		},
		ExitLoop,
	)
	if err != nil {
		return fmt.Errorf("failed to create exit loop tool: %v", err)
	}

	// STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
	refinerAgentInLoop, err := llmagent.New(llmagent.Config{
		Name:  "RefinerAgent",
		Model: model,
		Instruction: fmt.Sprintf(`You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
**Current Document:**

"""
{%s}
"""

**Critique/Suggestions:**
{%s}
**Task:**
Analyze the 'Critique/Suggestions'.
IF the critique is *exactly* "%s":
You MUST call the 'exitLoop' function. Do not output any text.
ELSE (the critique contains actionable feedback):
Carefully apply the suggestions to improve the 'Current Document'. Output *only* the refined document text.`, stateDoc, stateCrit, donePhrase),
		Description: "Refines the document based on critique, or calls exitLoop if critique indicates completion.",
		Tools:       []tool.Tool{exitLoopTool},
		OutputKey:   stateDoc,
	})
	if err != nil {
		return fmt.Errorf("failed to create refiner agent: %v", err)
	}

	// STEP 2: Refinement Loop Agent
	refinementLoop, err := loopagent.New(loopagent.Config{
		AgentConfig: agent.Config{
			Name:      "RefinementLoop",
			SubAgents: []agent.Agent{criticAgentInLoop, refinerAgentInLoop},
		},
		MaxIterations: 5,
	})
	if err != nil {
		return fmt.Errorf("failed to create loop agent: %v", err)
	}

	// STEP 3: Overall Sequential Pipeline
	iterativeWriterAgent, err := sequentialagent.New(sequentialagent.Config{
		AgentConfig: agent.Config{
			Name:      appName,
			SubAgents: []agent.Agent{initialWriterAgent, refinementLoop},
		},
	})
	if err != nil {
		return fmt.Errorf("failed to create sequential agent pipeline: %v", err)
	}

	// Run the pipeline via an in-memory runner.
	srv := session.InMemoryService()
	r, err := runner.New(runner.Config{
		AppName:        appName,
		Agent:          iterativeWriterAgent,
		SessionService: srv,
	})
	if err != nil {
		return fmt.Errorf("failed to create runner: %v", err)
	}

	createResp, err := srv.Create(ctx, &session.CreateRequest{
		AppName: appName,
		UserID:  userID,
	})
	if err != nil {
		return fmt.Errorf("failed to create session: %v", err)
	}

	sessionID := createResp.Session.ID()
	userMsg := genai.NewContentFromText(prompt, "user")

	fmt.Printf("=== Running IterativeWritingPipeline ===\nPrompt: %s\n\n", prompt)

	for event, err := range r.Run(ctx, userID, sessionID, userMsg, agent.RunConfig{}) {
		if err != nil {
			return fmt.Errorf("run error: %v", err)
		}
		if event.IsFinalResponse() && event.Content != nil {
			for _, part := range event.Content.Parts {
				if part.Text != "" {
					fmt.Printf("[%s] %s\n\n", event.Author, part.Text)
				}
			}
		}
	}

	fmt.Println("=== Pipeline Complete ===")
	return nil
}
