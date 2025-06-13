from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
print("🔐 Loaded OpenAI Key:", api_key[:5] + "********" if api_key else "❌ Key not found")

client = OpenAI(api_key=api_key)

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
