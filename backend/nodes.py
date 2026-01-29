import os
import google.generativeai as genai
from backend.schema import GraphState

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Auto-select an available model
def get_available_model():
    try:
        models = genai.list_models()
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                return model.name
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Fallback to gemini-pro if no model found
    return "gemini-pro"

model_name = get_available_model()
print(f"Using model: {model_name}")
model = genai.GenerativeModel(model_name)

vector_db = None

def get_vector_db():
    global vector_db
    if vector_db is None:
        from backend.rag import load_vector_db
        try:
            vector_db = load_vector_db()
        except Exception as e:
            print(f"Warning: Could not load vector database: {e}")
            vector_db = None
    return vector_db

# ---------------- ROUTER NODE ----------------
def analyzer_node(state: GraphState) -> GraphState:
    text = state["question"].lower()

    keywords = ["leave", "policy", "sick", "annual", "contractor", "approval"]

    if any(k in text for k in keywords):
        route = "policy"
    else:
        route = "general"

    return {**state, "route": route}

# ---------------- GENERAL NODE ----------------
def general_node(state: GraphState) -> GraphState:
    response = model.generate_content(state["question"])
    answer = response.text

    return {**state, "answer": answer}

# ---------------- POLICY RAG NODE ----------------
def policy_node(state: GraphState) -> GraphState:
    db = get_vector_db()
    
    if db is None:
        answer = "I apologize, but the policy database is not available. Please try a general question instead."
        return {**state, "answer": answer}
    
    docs = db.similarity_search(state["question"], k=2)

    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    Answer based only on the policy text below and give citation.

    Policy:
    {context}

    Question:
    {state['question']}
    """

    response = model.generate_content(prompt)
    answer = response.text + "\n\nSource: leave_policy.md"

    return {**state, "answer": answer}