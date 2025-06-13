from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

# Load the API key from environment and print debug info
api_key = os.getenv("OPENAI_API_KEY")
print("🔐 Loaded OpenAI Key:", api_key[:5] + "********" if api_key else "❌ Key not found")

client = OpenAI(api_key=api_key)

app = FastAPI()

# Allow requests from frontend
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
    return {"message": "GCP Compliance Assistant is running."}

@app.post("/ask")
def ask_question(query: Query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful GCP compliance assistant."},
                {"role": "user", "content": query.query}
            ]
        )
        answer = response.choices[0].message.content
        return {"response": answer}
    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
