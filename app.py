from flask import Flask, request, make_response
from elasticsearch import Elasticsearch
import datetime
import os
import random
from dotenv import load_dotenv

# Load variables locally or from Render environment
load_dotenv()

app = Flask(__name__)

# 1. Connect to Elastic Cloud using Environment Variables
ELASTIC_CLOUD_ID = os.environ.get("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,
    api_key=ELASTIC_API_KEY
)

# Kakamega Coordinate Mapping for the Map "Money Shot"
# If we don't know the exact village, we pick a random hub in Kakamega
KAKAMEGA_HUBS = [
    {"name": "Lurambi", "lat": 0.2827, "lon": 34.7519},
    {"name": "Butere", "lat": 0.1456, "lon": 34.4856},
    {"name": "Mumias", "lat": 0.3344, "lon": 34.4892},
    {"name": "Malava", "lat": 0.4433, "lon": 34.8550}
]

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    # Africa's Talking POST data
    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # 2. USSD Navigation Logic
    if text == "":
        # Main Menu
        response = "CON AfyaPulse: Rural Surveillance\n"
        response += "1. Human Health Issue\n"
        response += "2. Animal Health Issue"
    
    elif text == "1":
        # Sub-menu Human
        response = "CON Select Primary Symptom:\n"
        response += "1. Fever\n"
        response += "2. Rash\n"
        response += "3. Respiratory/Cough"
        
    elif text == "2":
        # Sub-menu Animal
        response = "CON Animal Health Observation:\n"
        response += "1. Unusual death (Immediate alert)\n"
        response += "2. Sudden sickness/Lethargy"

    else:
        # 3. Data Ingestion - This executes when a user finishes a choice (e.g., '1*1' or '2*1')
        
        # Pick a location hub for the demo (simulating user location)
        location_hub = random.choice(KAKAMEGA_HUBS)
        
        doc = {
            "session_id": session_id,
            "phone": phone_number,
            "raw_input": text, # This will be '1*1', '2*1', etc.
            "channel": "ussd",
            "timestamp": datetime.datetime.now().isoformat(),
            "location_code": location_hub["name"],
            "location": {
                "lat": location_hub["lat"] + random.uniform(-0.02, 0.02),
                "lon": location_hub["lon"] + random.uniform(-0.02, 0.02)
            }
        }
        
        try:
            # Trigger the AI Triage Pipeline
            es.index(
                index="health-reports", 
                document=doc, 
                pipeline="disease-triage-pipeline"
            )
            response = f"END Report received for {location_hub['name']}.\nAI Triage is notifying the Sub-County Officer."
        except Exception as e:
            print(f"Elastic Error: {e}")
            response = "END Connection error. Please try again later."

    # Africa's Talking requires a 200 OK with 'text/plain'
    return make_response(response, 200, {'Content-Type': 'text/plain'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)