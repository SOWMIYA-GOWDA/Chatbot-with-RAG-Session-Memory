# Chatbot-with-RAG-Session-Memory
An intelligent chatbot built with LangGraph that routes queries between general LLM responses and policy-specific answers using RAG, with session memory to retain user context across conversations.

# LangGraph Chatbot with RAG and Session Memory

## 📌 Overview
This project is a LangGraph-based conversational AI system designed to intelligently handle both general user questions and company policy-related queries. It uses a routing mechanism to decide whether to answer using a standard LLM or perform Retrieval-Augmented Generation (RAG) over a policy document stored in a vector database. The chatbot also maintains session memory to remember user-specific context during a conversation.

---

## 🎯 Objective
The goal of this project is to demonstrate:
- LangGraph multi-node workflow design
- Conditional routing using an analyzer node
- RAG implementation with a real vector database
- Session memory handling within a conversation

---

## 🧠 System Architecture

### Graph Nodes
The LangGraph consists of **three mandatory nodes**:

1. **Analyzer / Router Node**
   - Input: `user_message`, `session_state`
   - Decides whether the query is:
     - `"general"` → general conversation
     - `"policy"` → company policy related
   - This is the **only node** responsible for routing decisions.

2. **General Q&A Node**
   - Triggered when route = `"general"`
   - Uses an LLM to answer open-domain questions
   - Updates session memory when relevant

3. **Policy RAG Node**
   - Triggered when route = `"policy"`
   - Retrieves relevant policy chunks from a vector database
   - Uses LLM to generate answers grounded in retrieved documents
   - Includes citations for transparency
   - Updates session memory when relevant

---
## Project Structure
```text
somwi/
│
├── backend/
│   ├── __pycache__/
│   ├── graph.py          # LangGraph workflow definition
│   ├── nodes.py          # Analyzer, General Q&A, and Policy RAG nodes
│   ├── rag.py            # RAG logic (vector retrieval + LLM)
│   └── schema.py         # State / schema definitions
│
├── data/
│   └── leave_policy.md   # Company leave policy document
│
├── frontend/
│   ├── index.html        # Chat UI layout
│   ├── script.js         # Frontend logic and API calls
│   └── style.css         # UI styling
│
├── vector_db/            # Vector database storage (Chroma / FAISS)
│
├── venv/                 # Python virtual environment
│
├── app.py                # Application entry point
├── setup_db.py           # Script to load policy and build vector DB
├── requirements.txt      # Project dependencies
└── .env                  # Environment variables (API keys)
```
## 🔀 Routing Logic
Routing is implemented using **LangGraph conditional edges**:

- Analyzer → General Q&A Node (if route == "general")
- Analyzer → Policy RAG Node (if route == "policy")

❌ Disallowed:
- Combining routing and response logic in one node
- Calling both nodes in a single execution
- Performing policy retrieval in the general node

---

## 📄 Policy Document
- File: `leave_policy.md`
- Created manually for this project

### Covered Sections:
- Annual leave entitlement
- Sick leave policy
- Carry-over / rollover rules
- Leave approval process
- Unpaid leave
- Contractor vs Full-time employee rules

The policy is detailed enough to answer **8+ unique questions**.

---

## 📚 RAG Implementation

### Vector Database
- Uses a real vector database (e.g., **Chroma** or **FAISS**)

### Steps:
1. Load `leave_policy.md`
2. Chunk the document
3. Generate embeddings
4. Store vectors with metadata:
   - document name
   - chunk ID
5. Retrieve top-k similar chunks during a query

### Citations
Policy answers include sources such as:
