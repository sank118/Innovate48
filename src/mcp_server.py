import os
from fastapi import FastAPI
import subprocess
import logging
from dotenv import load_dotenv
from Orchestrator.AgentOrchestrator import AgentOrchestrator

logging.basicConfig(filename="var/log/agent_system.log", level=logging.INFO)
load_dotenv('.env')
app = FastAPI()

# Endpoint to run monitoring
@app.get("/run_monitoring/")
async def run_monitoring():
    subprocess.run(["python", "src/main.py"])
    return {"status": "Monitoring started"}

# Endpoint to upload log
@app.post("/upload_log/")
async def upload_log(log_data: str):
    filename = 'build/user_input.log'
    try:
        with open(filename, 'w') as file:
            file.write(log_data)
        print(f"File '{filename}' created successfully.")
    except Exception as e:
        print(f"Error creating file: {e}")

    log_path = filename  # Path to your deployment log
    api_key = os.environ.get('API_KEY')  # Your API key for the LLM service
    api_url = os.environ.get('API_URL')   # LLM API endpoint
    model_name = os.environ.get('MODEL_NAME')

    # Create and run orchestrator
    orchestrator = AgentOrchestrator(
        log_path=log_path,
        api_key=api_key,
        api_url=api_url,
        model_name=model_name
    )

    # Run continuous monitoring
    orchestrator.run_continuous_monitoring(interval_seconds=60)

    return {"status": "Monitoring started for custom log"}

