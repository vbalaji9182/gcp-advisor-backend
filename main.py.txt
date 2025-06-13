from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_gcp_advisor(query: Query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a GCP advisor..."},
                {"role": "user", "content": query.question}
            ]
        )
        return {"response": response.choices[0].message['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "GCP Advisor Chatbot is running."}
