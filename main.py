from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend requests (adjust domain later for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for incoming requests
class Query(BaseModel):
    query: str

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "GCP Advisor Chatbot is running."}

# /ask endpoint that talks to OpenAI
@app.post("/ask")
def ask_question(query: Query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if your key has access
            messages=[
                {"role": "system", "content": "You are a GCP compliance advisor. Give helpful and compliant responses."},
                {"role": "user", "content": query.query}
            ],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message["content"]
        return {"response": answer}
    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

