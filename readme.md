curl -X POST https://adein.onrender.com/ussd \
     -d "sessionId=test_123&phoneNumber=+254700000000&text="
PUT _ingest/pipeline/disease-triage-pipeline
{
  "description": "Triage USSD reports into Risk Levels",
  "processors": [
    {
      "script": {
        "description": "Calculate Risk Level based on symptoms",
        "source": """
          // Define symptom codes from your USSD logic
          def fever = "1*1";
          def rash = "1*2";
          def cough = "1*3";
          def animal_death = "2*1";

          if (ctx.raw_input == animal_death) {
            ctx.risk_level = "CRITICAL";
            ctx.priority = 1;
          } else if (ctx.raw_input == fever || ctx.raw_input == rash) {
            ctx.risk_level = "HIGH";
            ctx.priority = 2;
          } else {
            ctx.risk_level = "LOW";
            ctx.priority = 3;
          }
        """
      }
    },
    {
      "set": {
        "field": "processed_at",
        "value": "{{{_ingest.timestamp}}}"
      }
    }
  ]
}
We leverage Elastic Ingest Pipelines to decouple our application logic from our data enrichment. Our Python script simply sends raw data, and the Elastic 'Brain' calculates the risk level as the data lands, ensuring zero-latency triage.

ELASTIC_API_KEY=WmJrNWdKd0I4eWxCaWM5Y1RKM1o6NG0tZGxKRElIQlR3MlVLY2J6U3RKQQ==
ELASTIC_ENDPOINT=https://my-elasticsearch-project-af83a4.es.us-central1.gcp.elastic.cloud:44
ELASTIC_CLOUD_ID=My_Elasticsearch_project:dXMtY2VudHJhbDEuZ2NwLmVsYXN0aWMuY2xvdWQkYWY4M2E0NWQ4MzEzNGE1MjljOGRkM2M2N2JhOTJhNzUuZXMkYWY4M2E0NWQ4MzEzNGE1MjljOGRkM2M2N2JhOTJhNzUua2I=

