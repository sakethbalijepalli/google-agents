import os
from dotenv import load_dotenv
load_dotenv()

import vertexai
from vertexai.preview import reasoning_engines
from deploy_app import DanceAgentApp

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
STAGING_BUCKET = os.getenv("GCS_STAGING_BUCKET")

def deploy():
    print(f"Deploying to Project: {PROJECT_ID}, Location: {LOCATION}, Bucket: {STAGING_BUCKET}")
    
    vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

    remote_app = reasoning_engines.ReasoningEngine.create(
        DanceAgentApp(),
        requirements=[
            "google-adk",
            "google-genai",
            "python-dotenv",
            "beautifulsoup4",
            "requests",
            "ddgs",
            "google-cloud-aiplatform",
            "cloudpickle",
        ],
        display_name="DanceAgentSystem",
    )
    
    print(f"Deployment Complete! Resource Name: {remote_app.resource_name}")
    return remote_app

if __name__ == "__main__":
    deploy()
