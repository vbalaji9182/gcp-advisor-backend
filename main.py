from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# GCP reference keywords
GCP_REFERENCES = {
    "informed consent": "ICH E6(R3) – Section 4.4: Informed Consent of Trial Subjects",
    "eligibility criteria": "ICH E6(R3) – Section 5.3.1: Protocol and Amendments",
    "protocol deviation": "ICH E6(R3) – Section 5.20: Noncompliance",
    "source data": "ICH E6(R3) – Section 2.10: Source Data Accuracy and Integrity",
    "investigator": "ICH E6(R3) – Section 4: Investigator Responsibilities",
    "monitoring": "ICH E6(R3) – Section 5.18: Monitoring",
    "ethics committee": "ICH E6(R3) – Section 3: Ethics Committee/IRB",
    "sponsor": "ICH E6(R3) – Section 5: Sponsor Responsibilities",
    "risk-based monitoring": "ICH E6(R3) – Section 5.0: Quality Management",
}

def extract_reference(query: str) -> str:
    for keyword, ref in GCP_REFERENCES.items():
        if keyword.lower() in query.lower():
            return ref
    return "ICH E6(R3)."

# Input and output schemas
class QueryRequest(BaseModel):
    query: str

class Feedback(BaseModel):
    query: str
    response: str
    rating: int  # 1 to 5
    comments: str | None = None

@app.post("/ask")
async def ask_question(data: QueryRequest):
    query = data.query

    try:
        system_prompt = (
            "You are a GCP Compliance Assistant. Respond clearly and accurately to user questions "
            "based on ICH GCP E6(R3) principles. Always include a relevant section reference."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )

        gpt_reply = completion["choices"][0]["message"]["content"]
        reference = extract_reference(query)

        final_response = f"{gpt_reply}\n\n📘 Further reading: {reference}"
        return {"response": final_response}

    except Exception as e:
        return {"error": str(e)}

# Endpoint to collect feedback
@app.post("/feedback")
async def collect_feedback(data: Feedback):
    # Save or log feedback (for demo, we just print it)
    print("📥 Feedback received:")
    print(f"Query: {data.query}")
    print(f"Response: {data.response}")
    print(f"Rating: {data.rating} ⭐")
    print(f"Comments: {data.comments or 'None'}")
    return {"message": "Feedback recorded. Thank you!"}

