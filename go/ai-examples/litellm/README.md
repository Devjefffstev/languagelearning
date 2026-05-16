# Intercom Agent Chat System

A full-stack application that integrates a Go backend with litellm and a Next.js/OpenUI frontend to create AI-powered customer support conversations with Intercom product specialist knowledge.

## Architecture

### Backend (Go + LiteLLM)
- REST API that processes customer data + customer questions (JSON format)
- Generates customer context info and initial acknowledgment using local LLM (Ollama)
- Returns formatted customer information to display in chat context
- System prompt specialized in Intercom products

### Frontend (Next.js + OpenUI)
- Customer selection interface with 3 example scenarios
- Automatically loads customer info + question into chat context
- OpenUI chat interface where agent responds directly to customer
- Integrates with OpenAI API for streaming chat responses

## Workflow

1. **Select Customer**: Agent clicks one of three example customer scenarios
2. **Load Context**: Backend processes customer JSON + their question
3. **Display Chat**: OpenUI interface opens with customer context in system prompt
4. **Interact**: Agent reads customer info and responds directly in chat
5. **Continue**: Agent can ask clarifying questions and refine responses

## Prerequisites

- **Go 1.25+**
- **Node.js 18+** / **npm**
- **Ollama** (with at least `llama3.2` model installed and running)
- **OpenAI API key** (for the chat interface)

### Installation

#### 1. Start Ollama (in separate terminal)
```bash
ollama serve
# Verify llama3.2 is available:
ollama list
# If not available, pull it:
ollama pull llama3.2
```

#### 2. Backend Setup
```bash
cd backend
go build -o build-littlellm-app-example
./build-littlellm-app-example
# Server will start on http://localhost:8080
```

#### 3. Frontend Setup
```bash
cd openui-go
npm install
# Set OpenAI API key for chat responses
export OPENAI_API_KEY="your-api-key-here"

# For development
npm run dev
# Open http://localhost:3000

# For production
npm run build
npm run start
```

## API Endpoints

### Backend (Go) - Port 8080
```
POST /api/conversation
Content-Type: application/json

Request:
{
  "customer_data": {
    "name": "Sarah",
    "surname": "Johnson",
    "wallet_balance": 0.00,
    "account_status": "new",
    "subscription_level": "free",
    "email": "sarah.johnson@example.com",
    "customer_id": "CUST001",
    "join_date": "2025-01-15"
  },
  "customer_question": "Hi, I need help setting up our messaging system."
}

Response:
{
  "customer_info": "CUSTOMER INFO:\n- Name: Sarah Johnson\n...\n\nCUSTOMER QUESTION:\nHi, I need help...",
  "initial_message": "Hi Sarah! Thanks for reaching out..."
}
```

### Frontend (Next.js) - Port 3000
```
POST /api/conversation - Proxies to Go backend
POST /api/chat - OpenAI streaming chat endpoint
```

## Example Customer Data Schema

```json
{
  "name": "string",
  "surname": "string", 
  "wallet_balance": "float64",
  "account_status": "string (new|active|at_risk)",
  "subscription_level": "string (free|starter|premium)",
  "email": "string",
  "customer_id": "string",
  "join_date": "string (YYYY-MM-DD)",
  "customer_question": "string"
}
```

## Configuration

### Environment Variables

**Frontend (.env.local):**
```bash
OPENAI_API_KEY=sk-...  # For chat responses
BACKEND_URL=http://localhost:8080  # Backend endpoint (default)
```

**Backend:**
- Uses local Ollama at `http://localhost:11434` (default)
- Model: `llama3.2` (configurable in code)

## File Structure

```
litellm/
├── backend/
│   ├── main.go              # REST API server
│   ├── models.go            # Go structs for request/response
│   ├── go.mod
│   ├── go.sum
│   ├── build-littlellm-app-example  # Compiled binary
│   └── examples/
│       ├── customer_new_user.json
│       ├── customer_premium.json
│       └── customer_at_risk.json
│
└── openui-go/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx                  # Main UI with customer selection & chat
    │   │   ├── layout.tsx
    │   │   └── api/
    │   │       ├── chat/route.ts         # OpenAI chat streaming
    │   │       └── conversation/route.ts # Backend proxy
    │   └── library.ts
    ├── public/
    │   └── examples/
    │       ├── customer_new_user.json
    │       ├── customer_premium.json
    │       └── customer_at_risk.json
    ├── package.json
    └── next.config.ts
```

## Example Customers

### 1. New User (Sarah Johnson)
- Status: new
- Plan: free
- Wallet: $0.00
- Question: Help with messaging system setup

### 2. Premium (Marcus Thompson)
- Status: active
- Plan: premium
- Wallet: $4,850.75
- Question: Customer engagement optimization

### 3. At Risk (Elena Rodriguez)
- Status: at_risk
- Plan: starter
- Wallet: $12.50
- Question: Feature inquiry about Intercom

## System Prompt

The backend uses this system prompt for all interactions:

> "You are an expert Intercom support specialist with deep knowledge of Intercom products (messaging, customer data platform, ticketing, resolution bots, etc.). Your role is to provide empathetic, helpful support while subtly showcasing how Intercom features can help this customer's business. Keep responses professional, concise, and focused on solving the customer's needs."

Customer context is added to the system prompt at runtime, including:
- Customer name, email, ID
- Wallet balance
- Account status and subscription level
- Member since date
- Their specific question/inquiry

## Usage

1. Run Ollama: `ollama serve`
2. Run Backend: `cd backend && ./build-littlellm-app-example`
3. Run Frontend: `cd openui-go && OPENAI_API_KEY=... npm run dev`
4. Open browser: http://localhost:3000
5. Click a customer button to start conversation
6. Respond to customer in OpenUI chat interface

## Testing with curl

Load customer conversation:
```bash
curl -X POST http://localhost:8080/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "customer_data": {
      "name": "Sarah",
      "surname": "Johnson",
      "wallet_balance": 0.00,
      "account_status": "new",
      "subscription_level": "free",
      "email": "sarah.johnson@example.com",
      "customer_id": "CUST001",
      "join_date": "2025-01-15"
    },
    "customer_question": "Hi, I need help setting up our messaging system."
  }'
```

## Troubleshooting

### Backend Connection Refused
- Ensure Ollama is running: `ollama serve`
- Check Go backend is running on port 8080
- Verify `BACKEND_URL` environment variable if needed

### Missing OpenAI API Key
- Set `OPENAI_API_KEY` before running frontend
- Chat interface will show error if key is missing

### LLM Response Errors
- Verify `llama3.2` model is installed: `ollama list`
- Check Ollama is not out of memory
- Retry or restart Ollama

### Frontend Build Issues
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Performance Notes

- Initial LLM generation: ~1-3 seconds (depends on hardware)
- Chat responses use OpenAI (fast, requires API key)
- Backend can run fully offline with Ollama

## Future Enhancements

- Support for different LLM providers (OpenAI, Claude, etc.)
- Conversation history persistence
- Custom customer field mappings
- Multiple agent roles (sales, support, success)
- Analytics on customer interactions
- Multi-language support
- Bulk customer import/processing

## License

MIT
