# 💬 SupportFlow AI
### Enterprise Multi-Agent Customer Support System with Human-in-the-Loop

SupportFlow AI is an enterprise-grade **multi-agent customer support system** built using **LangGraph, FastAPI, Streamlit, SQLite, Docker, and Groq LLMs**. The system intelligently classifies customer support requests, predicts ticket priority, retrieves relevant customer and ticket information, generates AI-assisted responses, and incorporates **Human-in-the-Loop (HITL)** supervision before responses are delivered to customers.

Unlike traditional chatbots, **SupportFlow AI** follows an **agentic workflow**, where specialized AI agents collaborate to automate customer support while maintaining response quality through supervisor approval and feedback-driven response regeneration.

---

# 🚀 Features

- 🤖 Multi-Agent Workflow using LangGraph
- 🎯 Automatic Ticket Classification
- ⚡ Priority Prediction (Low, Medium, High)
- 🗄️ SQLite-based Customer & Ticket Lookup
- ✍️ AI-generated Customer Support Responses
- 👨‍💼 Human-in-the-Loop (HITL) Supervisor Approval
- 🔄 AI Response Regeneration using Supervisor Feedback
- 🎫 Ticket Continuation Support
- 📊 Supervisor Review Dashboard
- ⚡ FastAPI REST API
- 🎨 Interactive Streamlit Dashboard
- 🐳 Dockerized Deployment

---

# 🏗️ System Architecture

```
                Customer
                    │
                    ▼
          Streamlit Customer Portal
                    │
                    ▼
                FastAPI API
                    │
                    ▼
          LangGraph Multi-Agent Workflow
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Triage Agent   Priority Agent   Database Agent
                    │
                    ▼
            Resolution Agent
                    │
                    ▼
            Human Review (HITL)
            ┌─────────┴─────────┐
            ▼                   ▼
        Reject             Approve
            │                   │
            ▼                   ▼
    Regenerate Draft     Execute Action
            │                   │
            └──────────► Customer
```

---

# 🔄 Workflow

1. Customer submits a support request.
2. Triage Agent classifies the ticket.
3. Priority Agent predicts urgency.
4. Database Agent retrieves customer and ticket details.
5. Resolution Agent generates a professional response.
6. Supervisor reviews the response.
7. Supervisor can:
   - ✅ Approve and send to customer.
   - ❌ Reject and provide feedback.
8. AI regenerates the response using supervisor feedback.
9. Customer query history is preserved to generate context-aware AI responses throughout the ticket lifecycle.
---

# 🖥️ Dashboard

## 👤 Customer Portal

- Create a new support ticket
- Continue an existing ticket using Ticket ID
- Submit follow-up queries
- Receive supervisor-approved responses
---

## 👨‍💼 Supervisor Portal

- View pending review queue
- Review customer information
- Inspect customer query history
- Edit AI-generated responses
- Approve responses
- Reject and regenerate responses using supervisor feedback
- Monitor queue statistics
---

# 🛠️ Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3.11 |
| Large Language Model | Groq (Llama-3.3-70B) |
| Agent Framework | LangGraph |
| Backend Framework | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| Containerization | Docker & Docker Compose |
| API Documentation | Swagger UI |

---


# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Prachee314/SupportFlow-AI.git

cd SupportFlow-AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create

```
.env
```

Add

```
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Running Locally

Start FastAPI

```bash
uvicorn app_api:api --reload
```

Start Streamlit

```bash
streamlit run app_dashboard.py
```

Open

FastAPI

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

Dashboard

```
http://localhost:8501
```

---

# 🐳 Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

Stop

```bash
docker compose down
```

---

# 💡 Key Highlights

- Multi-Agent AI workflow
- Human-in-the-Loop governance
- Persistent ticket conversations
- Supervisor-guided response regeneration
- Dockerized deployment
- Enterprise-ready architecture
- Resume-ready portfolio project

---

# 👨‍💻 Author

**Prachee Dewangan**

M.Tech – Data Science & Artificial Intelligence

IIIT Naya Raipur

---

# 📄 License

This project is licensed under the MIT License.