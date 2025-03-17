import os
from typing import List

from Agents.BaseAgent import BaseAgent


class LogMonitoringAgent(BaseAgent):
    """Agent responsible for monitoring log files for build and deployment activities"""

    def __init__(self, log_path: str):
        super().__init__("LogMonitor")
        self.log_path = log_path
        self.log_position = 0

    def read_new_logs(self) -> List[str]:
        """Read new log entries since last check"""
        if not os.path.exists(self.log_path):
            self.log(f"Log file {self.log_path} does not exist", "error")
            return []

        with open(self.log_path, 'r') as f:
            f.seek(self.log_position)
            new_logs = f.readlines()
            self.log_position = f.tell()

        return new_logs

    def filter_build_deployment_logs(self, logs: List[str]) -> List[str]:
        """Filter log to only include build and deployment related entries"""
        build_deploy_keywords = [
            "build", "deploy", "container", "pod", "kubernetes", "k8s",
            "docker", "image", "ci/cd", "pipeline", "helm", "chart"
        ]

        filtered_logs = []
        for log in logs:
            if any(keyword in log.lower() for keyword in build_deploy_keywords):
                filtered_logs.append(log)

        return filtered_logs