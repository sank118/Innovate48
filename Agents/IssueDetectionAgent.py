import re
from datetime import datetime
from typing import List, Dict, Any

from Agents.BaseAgent import BaseAgent


class IssueDetectionAgent(BaseAgent):
    """Agent responsible for detecting issues in log"""

    def __init__(self):
        super().__init__("IssueDetector")
        # Common error patterns in log
        self.error_patterns = [
            r"error",
            r"exception",
            r"failed",
            r"failure",
            r"timeout",
            r"crash",
            r"exit code [1-9]",
            r"out of memory",
            r"cannot pull image",
            r"permission denied",
            r"connection refused",
            r"not found",
            r"404",
            r"403",
            r"500",
            r"terminate"
        ]

    def detect_issues(self, logs: List[str]) -> List[Dict[str, Any]]:
        """Detect issues in the provided log"""
        issues = []

        for i, log in enumerate(logs):
            for pattern in self.error_patterns:
                if re.search(pattern, log.lower()):
                    # Get some context (a few lines before and after)
                    start_idx = max(0, i - 2)
                    end_idx = min(len(logs), i + 3)
                    context = logs[start_idx:end_idx]

                    issue = {
                        "timestamp": datetime.now().isoformat(),
                        "error_line": log.strip(),
                        "context": [l.strip() for l in context],
                        "pattern_matched": pattern,
                        "resolved": False,
                        "solution_applied": None
                    }

                    issues.append(issue)
                    self.log(f"Detected issue: {log.strip()}")
                    break  # Move to next log line after finding an issue

        return issues