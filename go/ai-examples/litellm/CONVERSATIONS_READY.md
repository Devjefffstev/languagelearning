# ✅ 3 CONVERSATIONS READY TO USE

**Status**: All conversations created and ready to load into OpenUI

## 🌐 Access OpenUI Now

### Frontend: http://localhost:3000
### Backend: http://localhost:8080 (Health check available)

---

## 📊 Conversation 1: NEW USER (Sarah Johnson)

**Customer Profile:**
- Name: Sarah Johnson
- Email: sarah.johnson@example.com
- Customer ID: CUST001
- Wallet Balance: $0.00
- Account Status: **new**
- Subscription Plan: **free**
- Member Since: 2025-01-15

**Customer Question:**
> "I just signed up. How do I get started with Intercom?"

**Agent Response Generated:**
> "Hi Sarah, Thanks for reaching out to us! I've checked on your account and I see that you're one of our newest members, still in the free plan. How can we get you set up with a great Intercom experience tailored to what you need as a new user?"

**Copy-Paste Block for Chat:**
```
CUSTOMER INFO:
- Name: Sarah Johnson
- Email: sarah.johnson@example.com
- Customer ID: CUST001
- Wallet: $0.00
- Account Status: new
- Plan: free
- Member Since: 2025-01-15

CUSTOMER QUESTION:
I just signed up. How do I get started with Intercom?
```

**Agent Focus Areas:**
- Onboarding new users with the platform
- Explaining core features available in free tier
- Building confidence and engagement
- Identifying upsell opportunities

---

## 📊 Conversation 2: PREMIUM CUSTOMER (Marcus Thompson)

**Customer Profile:**
- Name: Marcus Thompson
- Email: marcus.thompson@company.com
- Customer ID: CUST042
- Wallet Balance: $4,850.75
- Account Status: **active**
- Subscription Plan: **premium**
- Member Since: 2023-06-20

**Customer Question:**
> "Can we set up custom API integrations with our backend?"

**Agent Response Generated:**
> "Hi Marcus, Thanks for reaching out to us about setting up custom API integrations in Intercom. I've checked your account, and as a premium user since June 2023, you're already taking advantage of many advanced features that can help streamline your backend integrations - would you like some guidance on how to get started with creating private APIs or custom connections?"

**Copy-Paste Block for Chat:**
```
CUSTOMER INFO:
- Name: Marcus Thompson
- Email: marcus.thompson@company.com
- Customer ID: CUST042
- Wallet: $4850.75
- Account Status: active
- Plan: premium
- Member Since: 2023-06-20

CUSTOMER QUESTION:
Can we set up custom API integrations with our backend?
```

**Agent Focus Areas:**
- Advanced technical capabilities
- Enterprise-level customization
- Demonstrating premium value
- Building long-term partnership
- Complex solution architecture

---

## 📊 Conversation 3: AT-RISK CUSTOMER (Elena Rodriguez)

**Customer Profile:**
- Name: Elena Rodriguez
- Email: elena.r.2022@email.com
- Customer ID: CUST089
- Wallet Balance: $12.50
- Account Status: **at_risk**
- Subscription Plan: **starter**
- Member Since: 2024-03-08

**Customer Question:**
> "Your pricing seems high for what we need. Do you have a smaller plan?"

**Agent Response Generated:**
> "Hi Elena, thanks for reaching out to us about your pricing concerns - I completely understand how budget can be tied up quickly as a new business owner! Given that you're currently on our Starter plan (CUST089), I'd be happy to help you explore potential upgrades or look into more affordable options that might fit your needs today."

**Copy-Paste Block for Chat:**
```
CUSTOMER INFO:
- Name: Elena Rodriguez
- Email: elena.r.2022@email.com
- Customer ID: CUST089
- Wallet: $12.50
- Account Status: at_risk
- Plan: starter
- Member Since: 2024-03-08

CUSTOMER QUESTION:
Your pricing seems high for what we need. Do you have a smaller plan?
```

**Agent Focus Areas:**
- Customer retention and empathy
- Understanding budget constraints
- Demonstrating value at starter tier
- Cost-effective solutions
- Preventing churn

---

## 🎯 How to Load Conversations

### Step 1: Open OpenUI
```
http://localhost:3000
```

### Step 2: Copy Customer Block
Pick any conversation from above and copy the "Copy-Paste Block" section.

### Step 3: Paste into Chat
Click the chat input field and paste the customer information.

### Step 4: Send
Press Enter or click Send button.

### Step 5: Interact
The Intercom specialist agent will respond with context-aware advice. Continue the conversation naturally!

### Step 6: Repeat
Load the other two conversations by repeating steps 2-5.

---

## 🔄 System Workflow

```
Customer JSON
    ↓
Backend (LiteLLM + Ollama)
    ↓
Generate Customer Context + Initial Message
    ↓
Return to Frontend
    ↓
Display in OpenUI Chat
    ↓
Agent (Intercom Specialist) Responds
    ↓
Conversation Continues
    ↓
Agent Refines & Improves Responses
```

---

## 🎯 Account Status Variations

### NEW Status
- Expected behavior: Welcoming, educational tone
- Feature set: Free tier basics
- Goal: Onboarding and activation

### ACTIVE Status  
- Expected behavior: Technical, advanced tone
- Feature set: Premium capabilities highlighted
- Goal: Maximize platform adoption and ROI

### AT-RISK Status
- Expected behavior: Empathetic, retention-focused
- Feature set: Cost-effective alternatives offered
- Goal: Prevent churn, rebuild engagement

---

## 🤖 System Prompt

All conversations use this Intercom specialist prompt:

> "You are an expert Intercom support specialist with deep knowledge of Intercom products (messaging, customer data platform, ticketing, resolution bots, etc.). Your role is to provide empathetic, helpful support while subtly showcasing how Intercom features can help this customer's business. Keep responses professional, concise, and focused on solving the customer's needs."

---

## 🚀 Advanced Usage

### Create Your Own Conversations

Use the backend API directly:

```bash
curl -X POST http://localhost:8080/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "customer_data": {
      "name": "Your Name",
      "surname": "Last Name",
      "wallet_balance": 1000.00,
      "account_status": "active",
      "subscription_level": "premium",
      "email": "email@example.com",
      "customer_id": "CUST123",
      "join_date": "2024-01-01"
    },
    "customer_question": "Your customer question here?"
  }'
```

### Customize Customer Schema

Supported fields:
- `name` (required) - Customer first name
- `surname` (required) - Customer last name  
- `wallet_balance` (required) - Account balance/credit
- `account_status` (required) - "new", "active", or "at_risk"
- `subscription_level` (required) - "free", "starter", or "premium"
- `email` (optional) - Contact email
- `customer_id` (optional) - Unique identifier
- `join_date` (optional) - Account creation date

---

## ✨ Key Features Demonstrated

✅ **Account Status Recognition** - Different responses for new/active/at-risk customers

✅ **Plan-Based Personalization** - Features mentioned match subscription level

✅ **Customer Context Loading** - Full customer info available in chat

✅ **Intercom Expertise** - All responses showcase Intercom product knowledge

✅ **Natural Conversation Flow** - Agent and customer can interact naturally

✅ **Refinement Capability** - Agent can improve and adapt responses in real-time

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 not responding | `cd openui-go && npm run dev` |
| Port 8080 not responding | `cd backend && ./build-littlellm-app-example` |
| Chat responses are slow | Ensure Ollama model is downloaded: `ollama pull llama3.2` |
| Customer info not loading | Copy entire block including all 7 customer info lines |
| Agent not recognizing status | Verify account_status is "new", "active", or "at_risk" |

---

## 📖 Documentation

- **README.md** - Full system architecture and setup
- **QUICK_START.md** - Getting started guide
- **CONVERSATIONS_READY.md** - This file (conversation usage)

---

**Status**: ✅ Ready to Use

**Created**: 2026-05-03

**All 3 conversations are generated and ready for interaction!**
