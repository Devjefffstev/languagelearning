package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/voocel/litellm"
)

var llmClient *litellm.Client
var model = "llama3.2"

func init() {
	var err error
	llmClient, err = litellm.NewWithProvider("ollama", litellm.ProviderConfig{
		APIKey: "ollama",
	})
	if err != nil {
		log.Fatalf("Failed to initialize litellm client: %v", err)
	}
}

func main() {
	http.HandleFunc("/api/conversation", conversationHandler)
	http.HandleFunc("/health", healthHandler)

	port := ":8080"
	log.Printf("Server starting on %s\n", port)
	log.Printf("Using model: %s\n", model)
	log.Fatal(http.ListenAndServe(port, nil))
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status": "healthy",
		"model":  model,
	})
}

func conversationHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ConversationRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(ErrorResponse{Error: "Invalid request body"})
		return
	}

	response, err := generateConversation(r.Context(), req.CustomerData, req.CustomerQuestion)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(ErrorResponse{Error: err.Error()})
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func generateConversation(ctx context.Context, customer CustomerData, question string) (*ConversationResponse, error) {
	customerSummary := fmt.Sprintf(
		"CUSTOMER INFO:\n- Name: %s %s\n- Email: %s\n- Customer ID: %s\n- Wallet: $%.2f\n- Account Status: %s\n- Plan: %s\n- Member Since: %s\n\nCUSTOMER QUESTION:\n%s",
		customer.Name, customer.Surname, customer.Email, customer.CustomerID,
		customer.WalletBalance, customer.AccountStatus,
		customer.SubscriptionLevel, customer.JoinDate, question,
	)

	systemPrompt := `You are an expert Intercom support specialist with deep knowledge of Intercom products (messaging, customer data platform, ticketing, resolution bots, etc.). 
Your role is to provide empathetic, helpful support while subtly showcasing how Intercom features can help this customer's business.
Keep responses professional, concise, and focused on solving the customer's needs.`

	acknowledgePrompt := fmt.Sprintf(`Based on the customer information and their question below, generate a brief acknowledgment message that:
1. Shows you've understood their situation
2. References their specific account status and plan level
3. Sets the stage for helping them

Keep it to 2-3 sentences and be conversational.

%s`, customerSummary)

	initialMsg, err := generateResponse(ctx, systemPrompt, acknowledgePrompt)
	if err != nil {
		return nil, fmt.Errorf("failed to generate initial message: %w", err)
	}

	return &ConversationResponse{
		CustomerInfo:   customerSummary,
		InitialMessage: initialMsg,
	}, nil
}

func generateResponse(ctx context.Context, systemPrompt, userPrompt string) (string, error) {
	resp, err := llmClient.Chat(ctx, &litellm.Request{
		Model: model,
		Messages: []litellm.Message{
			{Role: "system", Content: systemPrompt},
			{Role: "user", Content: userPrompt},
		},
		MaxTokens: litellm.IntPtr(300),
	})
	if err != nil {
		return "", err
	}

	return resp.Content, nil
}
