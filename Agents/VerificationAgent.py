import subprocess
from typing import Tuple, Optional

import requests

from Agents.BaseAgent import BaseAgent


class VerificationAgent(BaseAgent):
    """Agent responsible for verifying the system is working correctly after fixes"""

    def __init__(self, kubernetes_context: Optional[str] = None):
        super().__init__("Verifier")
        self.kubernetes_context = kubernetes_context

    def verify_pods_running(self) -> Tuple[bool, str]:
        """Verify that all pods are running correctly"""
        try:
            context_arg = f"--context={self.kubernetes_context}" if self.kubernetes_context else ""
            cmd = f"kubectl {context_arg} get pods --all-namespaces"

            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )

            # Check if any pods are not in Running state
            non_running_pods = []
            for line in result.stdout.splitlines()[1:]:  # Skip header line
                parts = line.split()
                if len(parts) >= 3 and parts[3] != "Running":
                    non_running_pods.append(line)

            if non_running_pods:
                return False, f"Some pods are not running:\n{''.join(non_running_pods)}"
            else:
                return True, "All pods are running correctly"

        except subprocess.CalledProcessError as e:
            return False, f"Failed to verify pods: {e.stderr}"

    def verify_application_running(self, endpoint: str) -> Tuple[bool, str]:
        """Verify that the application is accessible via HTTP"""
        try:
            response = requests.get(endpoint, timeout=10)

            if response.status_code >= 200 and response.status_code < 300:
                return True, f"Application is accessible at {endpoint}"
            else:
                return False, f"Application returned status code {response.status_code}"

        except requests.RequestException as e:
            return False, f"Failed to access application at {endpoint}: {str(e)}"