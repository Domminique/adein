from flask import Flask, request, make_response
from elasticsearch import Elasticsearch
import datetime
import os

app = Flask(__name__)

# 1. Connect to Elastic Cloud
# Get these from your Elastic Cloud Deployment dashboard
ELASTIC_CLOUD_ID = "your_cloud_id"
ELASTIC_API_KEY = "your_api_key"

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,
    api_key=ELASTIC_API_KEY
)

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    # Africa's Talking sends data as form-urlencoded
    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default") # Example: "1*1*Fever"

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
    else:
        # 3. Data Ingestion to Elasticsearch
        # We push the final selection to Elastic
        doc = {
            "session_id": session_id,
            "phone": phone_number,
            "raw_input": text,
            "channel": "ussd",
            "timestamp": datetime.datetime.now().isoformat(),
            "location_code": "KE-01" # In a real app, map phone prefix or prompt for area
        }
        
        try:
            # We use a 'pipeline' to let Elastic Agent Builder/Inference 
            # process the text into 'Disease Categories' automatically.
            es.index(index="health-reports", document=doc, pipeline="disease-triage-pipeline")
            response = "END Thank you. Health officials have been notified."
        except Exception as e:
            print(f"Error: {e}")
            response = "END System error. Please try again later."

    return make_response(response, 200, {'Content-Type': 'text/plain'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
