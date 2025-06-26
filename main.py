from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔍 GCP keyword-to-reference mapping
GCP_REFERENCES = {
    "informed consent": "ICH E6(R3) – Section 4.4: Informed Consent of Trial Subjects",
    "eligibility criteria": "ICH E6(R3) – Section 5.3.1: Protocol and Amendments",
    "protocol deviation": "ICH E6(R3) – Section 5.20: Noncompliance",
    "source data": "ICH E6(R3) – Section 2.10: Source Data Accuracy and Integrity",
    "investigator responsibilities": "ICH E6(R3) – Section 4: Investigator Responsibilities",
    "monitoring": "ICH E6(R3) – Section 5.18: Monitoring",
    "ethics committee": "ICH E6(R3) – Section 3: Institutional Review Board/Independent Ethics Committee",
}

# 🔧 Input model
class QueryRequest(BaseModel):
    query: str

# 🔍 Reference extraction logic
def extract_reference(user_query: str):
    for keyword, reference in GCP_REFERENCES.items():
        if keyword.lower() in user_query.lower():
            return reference
    return "ICH E6(R3) – Refer to appropriate section based on context."

# 📬 POST endpoint
@app.post("/ask")
async def ask(request: QueryRequest):
    try:
        system_prompt = (
            "You are a GCP Compliance Assistant providing helpful, compliant responses "
            "based on ICH E6(R3). Always give the reference section number that best fits the question."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.query},
            ]
        )

        gpt_answer = completion["choices"][0]["message"]["content"]
        reference = extract_reference(request.query)

        return {"response": f"{gpt_answer}\n\n📘 Reference: {reference}"}

    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}
