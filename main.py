from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class QueryInput(BaseModel):
    query: str

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keyword to ICH GCP E6(R3) reference map
GCP_REFERENCES = {
    "informed consent": "ICH E6(R3) – Section 4.4: Informed Consent of Trial Subjects",
    "investigator": "ICH E6(R3) – Section 4: Investigator Responsibilities",
    "sponsor": "ICH E6(R3) – Section 5: Sponsor Responsibilities",
    "monitoring": "ICH E6(R3) – Section 5.18: Monitoring",
    "audit": "ICH E6(R3) – Section 5.19: Audits",
    "adverse event": "ICH E6(R3) – Section 4.11: Safety Reporting",
    "pii": "ICH E6(R3) – Section 2.11: Subject Confidentiality",
    "ethics committee": "ICH E6(R3) – Section 3: IRB/IEC",
    "essential documents": "ICH E6(R3) – Section 8: Essential Documents",
    "source data": "ICH E6(R3) – Section 1.55 & 5.0: Source Documentation",
    "protocol deviation": "ICH E6(R3) – Section 4.5: Compliance with Protocol",
    "training": "ICH E6(R3) – Section 2.8: Staff Qualifications and Training",
    "gcp principles": "ICH E6(R3) – Section 2: Principles of ICH GCP",
    "data integrity": "ICH E6(R3) – Section 5.5: Trial Data Handling",
    "risk-based": "ICH E6(R3) – Section 5.0: Quality Management",
    "confidentiality": "ICH E6(R3) – Section 2.11: Subject Confidentiality",
}

def get_reference(text: str) -> str:
    matches = [
        ref for keyword, ref in GCP_REFERENCES.items()
        if keyword.lower() in text.lower()
    ]
    if matches:
        return "\n\nReference: " + "; ".join(set(matches))
    else:
        return "\n\nReference: ICH E6(R3) – Section 2: Principles of GCP"

@app.post("/ask")
async def ask(query_input: QueryInput):
    question = query_input.query.strip()
    if not question:
        return {"response": "Please enter a valid question."}

    # Simulate GCP assistant answer (replace with OpenAI/GPT in production)
    base_response = f"Here is your guidance related to: \"{question}\""

    # Append contextual GCP reference
    reference = get_reference(question)

    # Simulated smart answer
    answer = f"{base_response}{reference}"
    return {"response": answer}


