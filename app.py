from flask import Flask, request, make_response
from elasticsearch import Elasticsearch
import datetime
import os
from dotenv import load_dotenv

# This loads variables from a .env file locally, 
# but on Render, it will use the dashboard variables.
load_dotenv()

app = Flask(__name__)

# 1. Connect to Elastic Cloud using Environment Variables
# These must be set in the Render Dashboard under "Environment"
ELASTIC_CLOUD_ID = os.environ.get("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY")

# Safety check: logs error if variables are missing
if not ELASTIC_CLOUD_ID or not ELASTIC_API_KEY:
    print("❌ CRITICAL: Missing Elastic Cloud credentials in Environment Variables!")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,
    api_key=ELASTIC_API_KEY
)

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # 2. Basic USSD Logic (The Menu)
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
        # 3. Data Ingestion to Elasticsearch
        doc = {
            "session_id": session_id,
            "phone": phone_number,
            "raw_input": text,
            "channel": "ussd",
            "timestamp": datetime.datetime.now().isoformat(),
            "location_code": "KE-01" 
        }
        
        try:
            # Note: Ensure "disease-triage-pipeline" is created in Elastic or remove the pipeline param
            es.index(index="health-reports", document=doc)
            response = "END Thank you. The AI Agent is analyzing your report. Stay safe."
        except Exception as e:
            print(f"Elastic Error: {e}")
            response = "END System error. We are working on it."

    return make_response(response, 200, {'Content-Type': 'text/plain'})

if __name__ == '__main__':
    # IMPORTANT: Render sets the PORT variable. This ensures your app binds correctly.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
