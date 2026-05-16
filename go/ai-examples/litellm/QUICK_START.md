# Quick Start: Creating Conversations with Mock Users

## Prerequisites
- Ollama running: `ollama serve`
- Backend compiled: `backend/build-littlellm-app-example`

## Method 1: Simple curl (Fastest)

```bash
curl -X POST http://localhost:8080/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "customer_data": {
      "name": "John",
      "surname": "Doe",
      "wallet_balance": 1500.50,
      "account_status": "active",
      "subscription_level": "premium",
      "email": "john@example.com",
      "customer_id": "CUST123",
      "join_date": "2024-01-20"
    },
    "customer_question": "How can I set up automated messaging?"
  }'
```

## Method 2: From Example File

```bash
CUSTOMER=$(cat backend/examples/customer_new_user.json)
curl -X POST http://localhost:8080/api/conversation \
  -H "Content-Type: application/json" \
  -d "{
    \"customer_data\": $CUSTOMER,
    \"customer_question\": \"I'm new to Intercom. What should I do first?\"
  }"
```

## Method 3: Bash Script (test_mock.sh)

```bash
#!/bin/bash
curl -s -X POST http://localhost:8080/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "customer_data": {
      "name": "Alice",
      "surname": "Smith",
      "wallet_balance": 2500.00,
      "account_status": "active",
      "subscription_level": "enterprise",
      "email": "alice@company.com",
      "customer_id": "CUST999",
      "join_date": "2023-09-15"
    },
    "customer_question": "How do I integrate with our CRM?"
  }' | jq .
```

## Method 4: Python Script (test_mock.py)

```python
#!/usr/bin/env python3
import requests
import json

response = requests.post(
    "http://localhost:8080/api/conversation",
    json={
        "customer_data": {
            "name": "Bob",
            "surname": "Wilson",
            "wallet_balance": 3200.75,
            "account_status": "premium",
            "subscription_level": "enterprise",
            "email": "bob@company.com",
            "customer_id": "CUST456",
            "join_date": "2023-06-10"
        },
        "customer_question": "What's included in the enterprise plan?"
    }
)

print(json.dumps(response.json(), indent=2))
```

## Response Example

```json
{
  "customer_info": "CUSTOMER INFO:\n- Name: John Doe\n- Email: john@example.com\n- Customer ID: CUST123\n- Wallet: $1500.50\n- Account Status: active\n- Plan: premium\n- Member Since: 2024-01-20\n\nCUSTOMER QUESTION:\nHow can I set up automated messaging?",
  "initial_message": "Hi John! Thanks for reaching out. That's a great question about automated messaging..."
}
```

## Customer Data Schema

Required fields:
- `name` (string)
- `surname` (string)
- `wallet_balance` (number)
- `account_status` (string: "new", "active", "at_risk")
- `subscription_level` (string: "free", "starter", "premium", "enterprise")
- `email` (string)
- `customer_id` (string)
- `join_date` (string: YYYY-MM-DD)

## Test Multiple Conversations

```bash
# New user scenario
curl -s -X POST http://localhost:8080/api/conversation -H "Content-Type: application/json" -d '{"customer_data":{"name":"Sarah","surname":"Johnson","wallet_balance":0,"account_status":"new","subscription_level":"free","email":"sarah@example.com","customer_id":"CUST001","join_date":"2025-01-15"},"customer_question":"Hi, I need help getting started"}' | jq '.initial_message'

# Premium customer
curl -s -X POST http://localhost:8080/api/conversation -H "Content-Type: application/json" -d '{"customer_data":{"name":"Marcus","surname":"Thompson","wallet_balance":4850.75,"account_status":"active","subscription_level":"premium","email":"marcus@company.com","customer_id":"CUST042","join_date":"2023-06-20"},"customer_question":"How can we optimize our messaging?"}' | jq '.initial_message'

# At-risk customer
curl -s -X POST http://localhost:8080/api/conversation -H "Content-Type: application/json" -d '{"customer_data":{"name":"Elena","surname":"Rodriguez","wallet_balance":12.50,"account_status":"at_risk","subscription_level":"starter","email":"elena@example.com","customer_id":"CUST089","join_date":"2024-03-08"},"customer_question":"Do you have a solution for our support team?"}' | jq '.initial_message'
```

## Full End-to-End Setup

Terminal 1:
```bash
ollama serve
```

Terminal 2:
```bash
cd backend
./build-littlellm-app-example
```

Terminal 3:
```bash
# Create conversation
curl -s -X POST http://localhost:8080/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "customer_data": {
      "name": "Test",
      "surname": "Customer",
      "wallet_balance": 1000,
      "account_status": "active",
      "subscription_level": "premium",
      "email": "test@example.com",
      "customer_id": "TEST001",
      "join_date": "2024-01-01"
    },
    "customer_question": "Your question here?"
  }' | jq .
```

## Tips

- Use `jq` for pretty printing JSON: `curl ... | jq .`
- The `initial_message` is the Intercom specialist's acknowledgment
- The `customer_info` contains all customer context
- Backend runs on port 8080
- No OpenAI key needed for backend (uses local Ollama)
