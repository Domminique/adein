from flask import Flask, request, make_response
from elasticsearch import Elasticsearch
import datetime
import os
from dotenv import load_dotenv

# Load variables locally or from Render environment
load_dotenv()

app = Flask(__name__)

# 1. Connect to Elastic Cloud using Environment Variables
ELASTIC_CLOUD_ID = os.environ.get("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY")

if not ELASTIC_CLOUD_ID or not ELASTIC_API_KEY:
    print("❌ CRITICAL: Missing Elastic Cloud credentials!")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,
    api_key=ELASTIC_API_KEY
)

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # 2. USSD Navigation Logic
    if text == "":
        response = "CON Welcome to Sentinel-Pulse\n"
        response += "1. Report Human Symptoms\n"
        response += "2. Report Animal Health Issue"
    elif text == "1":
        response = "CON What is the primary symptom?\n"
        response += "1. Fever\n"
        response += "2. Rash\n"
        response += "3. Cough"
    elif text == "2":
        response = "CON Animal Health: What did you observe?\n"
        response += "1. Unusual livestock death\n"
        response += "2. Sudden illness in cattle"
    else:
        # 3. Final Input - Send to Elastic Inference Pipeline
        doc = {
            "session_id": session_id,
            "phone": phone_number,
            "raw_input": text,
            "channel": "ussd",
            "timestamp": datetime.datetime.now().isoformat(),
            "location_code": "KE-01" 
        }
        
        try:
            # The 'pipeline' parameter tells Elastic to run our Risk-Triage logic
            es.index(
                index="health-reports", 
                document=doc, 
                pipeline="disease-triage-pipeline"
            )
            # We use a smart response to show the user the AI is working
            response = "END Thank you. Your report has been received and triaged by our AI Agent."
        except Exception as e:
            print(f"Elastic Error: {e}")
            response = "END System error. We are working on it."

    return make_response(response, 200, {'Content-Type': 'text/plain'})

if __name__ == '__main__':
    # Bind to Render's dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
