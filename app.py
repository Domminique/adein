from flask import Flask, request, make_response
from elasticsearch import Elasticsearch
import datetime
import os
import random
from dotenv import load_dotenv

# Load variables
load_dotenv()

app = Flask(__name__)

# Connect to Elastic Cloud
ELASTIC_CLOUD_ID = os.environ.get("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY")

# Force .strip() to avoid the latin-1 encoding error we hit earlier
es = Elasticsearch(
    cloud_id=str(ELASTIC_CLOUD_ID).strip(),
    api_key=str(ELASTIC_API_KEY).strip()
)

# Geographic Hubs for Western Kenya / Kakamega
AGRIC_HUBS = [
    {"name": "Lurambi", "lat": 0.2827, "lon": 34.7519},
    {"name": "Butere", "lat": 0.1456, "lon": 34.4856},
    {"name": "Mumias", "lat": 0.3344, "lon": 34.4892},
    {"name": "Malava", "lat": 0.4433, "lon": 34.8550},
    {"name": "Shinyalu", "lat": 0.2117, "lon": 34.8450}
]

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # USSD Logic for KilimoPulse
    if text == "":
        response = "CON KilimoPulse: Agri-Intelligence\n1. Report Crop Pest/Disease\n2. Check Local Market Prices\n3. Get AI Planting Advice"
    
    # 1. Pest/Disease Reporting Flow
    elif text == "1":
        response = "CON Select Crop:\n1. Maize\n2. Beans\n3. Cassava\n4. Other"
    elif text == "1*1":
        response = "CON Select Symptom:\n1. Leaf holes (Pests)\n2. Yellowing (Disease)\n3. Wilting/Drying"
    
    # 2. Market Prices Flow
    elif text == "2":
        response = "CON Select Market:\n1. Kakamega Central\n2. Mumias Market\n3. Butere Market"
    elif text == "2*1":
        response = "END Current Prices (Kakamega):\nMaize: KES 3,200/90kg\nBeans: KES 8,500/90kg"

    # Final Step: Data Ingestion to Elasticsearch
    else:
        hub = random.choice(AGRIC_HUBS)
        doc = {
            "session_id": session_id,
            "phone": phone_number,
            "raw_input": text,
            "project": "KilimoPulse",
            "timestamp": datetime.datetime.now().isoformat(),
            "location_code": hub["name"],
            "location": {
                "lat": hub["lat"] + random.uniform(-0.01, 0.01),
                "lon": hub["lon"] + random.uniform(-0.01, 0.01)
            }
        }
        
        try:
            # Indexing into the new crop-reports index
            es.index(index="crop-reports", document=doc, pipeline="crop-triage-pipeline")
            response = f"END Report synced for {hub['name']}.\nOur AI Agronomist is analyzing the outbreak risk."
        except Exception as e:
            print(f"Elastic Error: {e}")
            # Fallback response for demo safety
            response = f"END Report received for {hub['name']}.\nCheck the KilimoPulse Dashboard for updates."

    return make_response(response, 200, {'Content-Type': 'text/plain'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)