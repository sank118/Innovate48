import logging

# Configure logging
from Orchestrator.AgentOrchestrator import AgentOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("var/log/agent_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AgentSystem")

if __name__ == "__main__":
    # Configuration
    log_path = "build/deployment.log"  # Path to your deployment logs
    api_key = "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"  # Your API key for the LLM service
    api_url = "https://api.groq.com/openai/v1"  # LLM API endpoint
    model_name = 'llama3-70b-8192'

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

