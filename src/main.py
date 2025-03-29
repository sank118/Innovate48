import logging
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Configure logging
from Orchestrator.AgentOrchestrator import AgentOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../var/log/agent_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AgentSystem")

if __name__ == "__main__":
    # Configuration
    log_path = "../build/deployment.log"  # Path to your deployment log
    api_key = os.environ.get("API_KEY")  # Your API key for the LLM service
    api_url = os.environ.get("API_URL")   # LLM API endpoint
    model_name = os.environ.get("MODEL_NAME")

    # Create and run orchestrator
    orchestrator = AgentOrchestrator(
        log_path=log_path,
        api_key=api_key,
        api_url=api_url,
        model_name=model_name
    )

    # Run continuous monitoring
    orchestrator.run_continuous_monitoring(interval_seconds=60)

    #Testing Git

