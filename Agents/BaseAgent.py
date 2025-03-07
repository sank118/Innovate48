import logging


class BaseAgent:
    """Base class for all agents in the system"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"AgentSystem.{name}")

    def log(self, message: str, level: str = "info"):
        """Log a message with the appropriate level"""
        if level.lower() == "info":
            self.logger.info(message)
        elif level.lower() == "warning":
            self.logger.warning(message)
        elif level.lower() == "error":
            self.logger.error(message)
        elif level.lower() == "debug":
            self.logger.debug(message)