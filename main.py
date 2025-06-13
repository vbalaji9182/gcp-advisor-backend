from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

# Load OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model to parse incoming query
class Query(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "GCP Compliance Assistant is running."}

@app.post("/ask")
def ask_question(query: Query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant for ICH GCP compliance."},
                {"role": "user", "content": query.query}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"response": answer}
    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

