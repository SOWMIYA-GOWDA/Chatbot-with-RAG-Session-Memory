from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from backend.graph import build_graph
import uvicorn

app = FastAPI()

try:
    graph = build_graph()
except Exception as e:
    print(f"Error building graph: {e}")
    graph = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

memory = {}

@app.post("/chat")
async def chat(data: dict):
    global memory

    try:
        if graph is None:
            return {"reply": "Error: The application is not properly initialized. Please restart."}

        state = {
            "question": data.get("message", ""),
            "answer": "",
            "route": "",
            "memory": memory
        }

        result = graph.invoke(state)
        memory = result.get("memory", {})
        answer = result.get("answer", "I couldn't generate a response.")
        
        return {"reply": str(answer)}
    
    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()
        return {"reply": f"Error: {str(e)}"}

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Mount static files AFTER API routes
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")


# 🔥 ADD THIS BLOCK
if __name__ == "__main__":
    print("🚀 Server starting at http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)