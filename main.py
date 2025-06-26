import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Enhanced reference map for ICH E6(R3)
GCP_REFERENCES = {
    "informed consent": "ICH E6(R3) – Section 4.4: Informed Consent of Trial Subjects",
    "eligibility": "ICH E6(R3) – Section 5.3.1: Protocol and Amendments",
    "protocol": "ICH E6(R3) – Section 5: Trial Management, Data Handling, and Recordkeeping",
    "protocol deviation": "ICH E6(R3) – Section 5.20: Noncompliance",
    "source data": "ICH E6(R3) – Section 2.10: Source Data Accuracy and Integrity",
    "investigator": "ICH E6(R3) – Section 4: Investigator Responsibilities",
    "monitoring": "ICH E6(R3) – Section 5.18: Monitoring",
    "ethics committee": "ICH E6(R3) – Section 3: Institutional Review Board/Independent Ethics Committee",
    "subject safety": "ICH E6(R3) – Section 2.3: Subject Rights and Safety",
    "data integrity": "ICH E6(R3) – Section 2.10: Source Data Accuracy and Integrity",
}

def extract_reference(user_query):
    matches = [ref for kw, ref in GCP_REFERENCES.items() if kw in user_query.lower()]
    return matches[0] if matches else "ICH E6(R3) – Refer to appropriate section based on context."

@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("query", "").strip()
    if not query:
        return jsonify({"response": "Please enter a valid GCP-related question."}), 400

    try:
        system_prompt = (
            "You are a professional GCP Compliance Assistant trained to answer based on ICH E6(R3). "
            "Give concise, context-aware answers, and avoid generic refusals. "
            "When unsure about local policies, advise the user to refer to their SOP or Line Manager."
        )

        chat = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )

        gpt_answer = chat.choices[0].message.content.strip()
        reference = extract_reference(query)
        full_response = f"{gpt_answer}\n\n📘 Reference: {reference}"

        return jsonify({"response": full_response})

    except Exception as e:
        return jsonify({"response": f"⚠️ Backend error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
