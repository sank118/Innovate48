from datetime import datetime
from typing import List, Dict, Any
from typing import List, Dict, Any

from Agents.BaseAgent import BaseAgent


class ReportingAgent(BaseAgent):
    """Agent responsible for generating reports on issues and solutions"""

    def __init__(self):
        super().__init__("Reporter")

    def generate_report(self, issues: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive report of issues and solutions"""
        if not issues:
            return "No issues detected during the monitoring period."

        report_lines = ["# Build and Deployment Monitoring Report", ""]
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total issues detected: {len(issues)}")
        report_lines.append(f"Issues resolved: {sum(1 for issue in issues if issue.get('resolved', False))}")
        report_lines.append("")

        # Add detailed issue information
        report_lines.append("## Issue Details")
        report_lines.append("")

        for i, issue in enumerate(issues, 1):
            report_lines.append(f"### Issue {i}")
            report_lines.append(f"**Timestamp:** {issue['timestamp']}")
            report_lines.append(f"**Status:** {'Resolved' if issue.get('resolved', False) else 'Unresolved'}")
            report_lines.append(f"**Error:** {issue['error_line']}")
            report_lines.append("")
            report_lines.append("**Context:**")
            for line in issue['context']:
                report_lines.append(f"> {line}")
            report_lines.append("")

            if issue.get('solution_applied'):
                report_lines.append("**Solution Applied:**")
                report_lines.append(issue['solution_applied'])
                report_lines.append("")

            if issue.get('verification_results'):
                report_lines.append("**Verification Results:**")
                report_lines.append(issue['verification_results'])
                report_lines.append("")

        return "\n".join(report_lines)

    def save_report(self, report: str, output_path: str = "monitoring_report.md") -> None:
        """Save the report to a file"""
        with open(output_path, 'w') as f:
            f.write(report)
        self.log(f"Report saved to {output_path}")