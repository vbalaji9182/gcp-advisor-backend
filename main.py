from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from any frontend (for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "GCP Advisor Chatbot is running."}

@app.post("/ask")
def ask_question(query: Query):
    return {"response": f"You asked: '{query.query}', here’s a placeholder answer from the bot."}

@app.get("/")
def read_root():
    return {"message": "GCP Advisor Chatbot is running."}
