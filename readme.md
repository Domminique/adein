KilimoPulse 🌾

> **Real-time Agricultural Intelligence for the Last Mile.** > Bridging the gap between rural smallholder farmers and advanced AI using USSD and the Elastic Stack.

## 🌟 The Vision

Smallholder farmers in Africa often lose up to 40% of their yields to pests and diseases simply because they lack an early warning system. **KilimoPulse** solves this by turning any basic feature phone into a sentinel for food security. By leveraging **Africa's Talking USSD** and **Elasticsearch's RAG (Retrieval-Augmented Generation) capabilities**, we provide real-time outbreak mapping and AI-driven agronomical advice without requiring a single byte of mobile data.

---

## 🚀 Features

* **Zero-Data Reporting:** Farmers report pest sightings and crop diseases via a simple USSD menu (`*384#`).
* **AI Agronomist:** An Elastic AI Agent (Agent Builder) analyzes incoming reports to provide localized mitigation strategies.
* **Outbreak Heatmaps:** Real-time geospatial visualization of pest movement across sub-counties.
* **Market Intelligence:** Integrated market price tracking to help farmers maximize profit and avoid exploitation.

---

## 🛠️ Technical Stack

* **Elasticsearch:** Vector database and geospatial indexing engine.
* **Kibana:** Operational dashboards, geospatial mapping, and AI Agent hosting.
* **Africa's Talking:** USSD Gateway for GSM-to-Cloud connectivity.
* **Python (Flask):** Scalable backend for processing USSD callbacks and data enrichment.

---

## 📐 Architecture

KilimoPulse follows a **RAG (Retrieval-Augmented Generation)** pattern:

1. **Ingest:** USSD inputs are received via Flask and indexed into Elasticsearch.
2. **Enrich:** An **Elastic Ingest Pipeline** calculates an "Infestation Index" ($I$) based on report frequency:

$$I = \frac{\sum (Severity \times Frequency)}{\Delta t}$$


3. **Retrieve:** The **Elastic AI Assistant** queries the live `crop-reports` index to identify localized trends.
4. **Respond:** The AI generates actionable advice for extension officers and farmers.

---

## 💻 Installation & Setup

### Prerequisites

* Python 3.9+
* An Elastic Cloud Account (Trial works!)
* An Africa's Talking Sandbox account

### Setup Instructions

1. **Clone the Repository:**
```bash
git clone https://github.com/your-username/KilimoPulse.git
cd KilimoPulse

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Environment Configuration:**
Create a `.env` file in the root directory:
```env
ELASTIC_CLOUD_ID=your_cloud_id
ELASTIC_API_KEY=your_api_key
PORT=5000

```


4. **Run the Application:**
```bash
python app.py

```



---

## 📂 Project Structure

```text
KilimoPulse/
├── app.py              # Main USSD logic & Elastic integration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Prevents leaking API keys
└── README.md           # Project documentation

```

---

## ⚖️ License

This project is licensed under the **MIT License**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more details.

---

## 🤝 Acknowledgments

* Built for the **Elastic Hackathon 2026**.
* Special thanks to the rural farming communities of **Kakamega County** for the inspiration behind this project.

---

