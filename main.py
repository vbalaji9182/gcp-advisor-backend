from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS for frontend access
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for ICH GCP compliance."},
                {"role": "user", "content": query.query}
            ]
        )
        return {"response": response["choices"][0]["message"]["content"].strip()}
    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

