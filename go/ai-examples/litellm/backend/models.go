package main

type CustomerData struct {
	Name              string  `json:"name"`
	Surname           string  `json:"surname"`
	WalletBalance     float64 `json:"wallet_balance"`
	AccountStatus     string  `json:"account_status"`
	SubscriptionLevel string  `json:"subscription_level"`
	Email             string  `json:"email,omitempty"`
	CustomerID        string  `json:"customer_id,omitempty"`
	JoinDate          string  `json:"join_date,omitempty"`
}

type ConversationRequest struct {
	CustomerData     CustomerData `json:"customer_data"`
	CustomerQuestion string       `json:"customer_question"`
}

type ConversationResponse struct {
	CustomerInfo string `json:"customer_info"`
	InitialMessage string `json:"initial_message"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}
