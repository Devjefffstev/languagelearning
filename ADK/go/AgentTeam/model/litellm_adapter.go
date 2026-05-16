// Package litellmmodel provides a model.LLM adapter backed by github.com/voocel/litellm.
// It translates between the ADK's genai-based request/response format and the
// litellm OpenAI-compatible wire format, enabling Ollama models to participate
// in an ADK agent team.
package litellmmodel

import (
	"context"
	"encoding/json"
	"fmt"
	"iter"
	"strings"

	"github.com/voocel/litellm"
	"google.golang.org/adk/model"
	"google.golang.org/genai"
)

// Config holds configuration for creating a litellm-backed LLM.
type Config struct {
	// ModelName is the Ollama model identifier (e.g. "gemma4:e2b", "llama3.2:1b").
	ModelName string
	// BaseURL is the OpenAI-compatible endpoint (e.g. "http://192.168.1.121:11434/v1").
	BaseURL string
	// APIKey is the API key; use "ollama" or any non-empty string for local Ollama.
	APIKey string
}

// Model implements model.LLM using litellm's OpenAI-compatible provider.
type Model struct {
	name   string
	model  string
	client *litellm.Client
}

// New creates a new litellm-backed LLM model.
func New(cfg Config) (*Model, error) {
	apiKey := cfg.APIKey
	if apiKey == "" {
		apiKey = "ollama"
	}
	client, err := litellm.NewWithProvider("openai", litellm.ProviderConfig{
		APIKey:  apiKey,
		BaseURL: cfg.BaseURL,
	})
	if err != nil {
		return nil, fmt.Errorf("litellm: failed to create client: %w", err)
	}
	return &Model{
		name:   cfg.ModelName,
		model:  cfg.ModelName,
		client: client,
	}, nil
}

// Name returns the model identifier.
func (m *Model) Name() string { return m.name }

// GenerateContent implements model.LLM by translating genai types to litellm and back.
// The stream parameter is accepted but litellm chat is called synchronously.
func (m *Model) GenerateContent(ctx context.Context, req *model.LLMRequest, _ bool) iter.Seq2[*model.LLMResponse, error] {
	return func(yield func(*model.LLMResponse, error) bool) {
		resp, err := m.generate(ctx, req)
		yield(resp, err)
	}
}

func (m *Model) generate(ctx context.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
	messages := contentsToMessages(req)
	tools := extractTools(req)

	llmReq := &litellm.Request{
		Model:    m.model,
		Messages: messages,
		Tools:    tools,
	}

	resp, err := m.client.Chat(ctx, llmReq)
	if err != nil {
		return nil, fmt.Errorf("litellm chat: %w", err)
	}

	return responseToLLMResponse(resp), nil
}

// contentsToMessages converts the ADK conversation history plus any system
// instruction into the flat list of litellm messages expected by OpenAI API.
func contentsToMessages(req *model.LLMRequest) []litellm.Message {
	var messages []litellm.Message

	// Prepend the system instruction when present.
	if req.Config != nil && req.Config.SystemInstruction != nil {
		sys := contentText(req.Config.SystemInstruction)
		if sys != "" {
			messages = append(messages, litellm.SystemMessage(sys))
		}
	}

	// Track function-call IDs so tool-response messages can reference them.
	// callIDs maps function name → last known call ID.
	callIDs := map[string]string{}
	callIndex := 0

	for _, c := range req.Contents {
		if c == nil {
			continue
		}
		role := c.Role
		if role == "model" {
			role = "assistant"
		}

		// Separate text, function calls, and function responses.
		var textParts []string
		var toolCalls []litellm.ToolCall
		var toolMessages []litellm.Message

		for _, p := range c.Parts {
			switch {
			case p.Text != "":
				textParts = append(textParts, p.Text)

			case p.FunctionCall != nil:
				callID := p.FunctionCall.ID
				if callID == "" {
					callID = fmt.Sprintf("call_%d", callIndex)
					callIndex++
				}
				callIDs[p.FunctionCall.Name] = callID

				argsJSON, _ := json.Marshal(p.FunctionCall.Args)
				toolCalls = append(toolCalls, litellm.ToolCall{
					ID:   callID,
					Type: "function",
					Function: litellm.FunctionCall{
						Name:      p.FunctionCall.Name,
						Arguments: string(argsJSON),
					},
				})

			case p.FunctionResponse != nil:
				// Look up the call ID for this function name.
				callID := p.FunctionResponse.ID
				if callID == "" {
					if id, ok := callIDs[p.FunctionResponse.Name]; ok {
						callID = id
					} else {
						callID = fmt.Sprintf("call_%d", callIndex)
						callIndex++
					}
				}
				respJSON, _ := json.Marshal(p.FunctionResponse.Response)
				toolMessages = append(toolMessages, litellm.Message{
					Role:       "tool",
					ToolCallID: callID,
					Content:    string(respJSON),
				})
			}
		}

		if len(toolCalls) > 0 {
			messages = append(messages, litellm.Message{
				Role:      "assistant",
				Content:   strings.Join(textParts, "\n"),
				ToolCalls: toolCalls,
			})
		} else if len(toolMessages) > 0 {
			messages = append(messages, toolMessages...)
		} else {
			messages = append(messages, litellm.Message{
				Role:    role,
				Content: strings.Join(textParts, "\n"),
			})
		}
	}

	return messages
}

// extractTools converts genai FunctionDeclarations into litellm Tool definitions.
func extractTools(req *model.LLMRequest) []litellm.Tool {
	if req.Config == nil {
		return nil
	}

	var tools []litellm.Tool
	for _, t := range req.Config.Tools {
		if t == nil {
			continue
		}
		for _, fd := range t.FunctionDeclarations {
			if fd == nil {
				continue
			}
			params := schemaToJSON(fd.Parameters)
			tools = append(tools, litellm.Tool{
				Type: "function",
				Function: litellm.FunctionDef{
					Name:        fd.Name,
					Description: fd.Description,
					Parameters:  params,
				},
			})
		}
	}
	return tools
}

// responseToLLMResponse converts a litellm Response into an ADK model.LLMResponse.
func responseToLLMResponse(resp *litellm.Response) *model.LLMResponse {
	var parts []*genai.Part

	// Plain text content.
	if resp.Content != "" {
		parts = append(parts, genai.NewPartFromText(resp.Content))
	}

	// Tool calls become FunctionCall parts.
	for _, tc := range resp.ToolCalls {
		var args map[string]any
		if err := json.Unmarshal([]byte(tc.Function.Arguments), &args); err != nil {
			args = map[string]any{"raw": tc.Function.Arguments}
		}
		args = normalizeArgs(args)
		parts = append(parts, &genai.Part{
			FunctionCall: &genai.FunctionCall{
				ID:   tc.ID,
				Name: tc.Function.Name,
				Args: args,
			},
		})
	}

	content := &genai.Content{
		Role:  "model",
		Parts: parts,
	}

	finishReason := genai.FinishReasonStop
	if resp.FinishReason == "tool_calls" {
		finishReason = genai.FinishReasonStop
	}

	return &model.LLMResponse{
		Content:      content,
		TurnComplete: true,
		FinishReason: finishReason,
	}
}

// contentText extracts the concatenated text from a genai.Content (used for
// system instructions).
func contentText(c *genai.Content) string {
	if c == nil {
		return ""
	}
	var sb strings.Builder
	for _, p := range c.Parts {
		sb.WriteString(p.Text)
	}
	return sb.String()
}

// schemaToJSON converts a genai.Schema to a plain map[string]any suitable for
// embedding as the "parameters" field of an OpenAI function definition.
func schemaToJSON(s *genai.Schema) map[string]any {
	if s == nil {
		return map[string]any{
			"type":       "object",
			"properties": map[string]any{},
		}
	}
	b, err := json.Marshal(s)
	if err != nil {
		return map[string]any{"type": "object"}
	}
	var m map[string]any
	_ = json.Unmarshal(b, &m)
	return m
}

// normalizeArgs removes the spurious "parameters" wrapper that some Ollama models
// inject into tool-call arguments. Two patterns are handled:
//
//	{"parameters": {"agent_name": "X"}}          → {"agent_name": "X"}   (unwrap)
//	{"parameters": {}, "agent_name": "X"}         → {"agent_name": "X"}   (strip)
func normalizeArgs(args map[string]any) map[string]any {
	params, hasParams := args["parameters"]
	if !hasParams {
		return args
	}
	paramsMap, isMap := params.(map[string]any)
	if !isMap {
		return args
	}
	if len(args) == 1 {
		// "parameters" is the only key — unwrap its contents to the top level.
		return paramsMap
	}
	// Other real keys exist alongside "parameters" — just drop the wrapper.
	delete(args, "parameters")
	return args
}
