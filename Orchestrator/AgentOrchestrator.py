import time
import logging
from typing import Dict, Any, Optional

from Agents.FixImplementationAgent import FixImplementationAgent
from Agents.IssueDetectionAgent import IssueDetectionAgent
from Agents.LogMonitoringAgent import LogMonitoringAgent
from Agents.ReportingAgent import ReportingAgent
from Agents.SolutionRecommendationAgent import SolutionRecommendationAgent
from Agents.VerificationAgent import VerificationAgent


class AgentOrchestrator:
    """Orchestrates the interactions between all agents"""

    def __init__(
            self,
            log_path: str,
            api_key: str,
            api_url: str,
            model_name: str,
            kubernetes_context: Optional[str] = None,
            application_endpoint: str = "http://localhost:8080"
    ) -> None:
        self.log_monitor = LogMonitoringAgent(log_path)
        self.issue_detector = IssueDetectionAgent()
        self.solution_recommender = SolutionRecommendationAgent(api_key, api_url, model_name)
        self.fix_implementer = FixImplementationAgent()
        self.verifier = VerificationAgent(kubernetes_context)
        self.reporter = ReportingAgent()

        self.application_endpoint = application_endpoint
        self.issues = []
        self.logger = logging.getLogger("AgentSystem.Orchestrator")

    def run_monitoring_cycle(self):
        """Run a full monitoring cycle"""
        # Step 1: Read and filter logs
        self.logger.info("Starting monitoring cycle")
        raw_logs = self.log_monitor.read_new_logs()
        build_deploy_logs = self.log_monitor.filter_build_deployment_logs(raw_logs)

        if not build_deploy_logs:
            self.logger.info("No new build/deployment logs found")
            return

        # Step 2: Detect issues
        new_issues = self.issue_detector.detect_issues(build_deploy_logs)

        if not new_issues:
            self.logger.info("No issues detected in logs")
            return

        # Step 3: Process each issue
        for issue in new_issues:
            self.logger.info(f"Processing issue: {issue['error_line'][:100]}...")

            # Get solution recommendation
            solution = self.solution_recommender.get_solution_recommendation(issue)

            # Present to user and get confirmation
            user_confirmation = self._get_user_confirmation(issue, solution)

            if user_confirmation:
                # Apply fix
                success, result = self.fix_implementer.apply_fix(issue, solution, user_confirmation)
                issue['resolved'] = success
                issue['solution_applied'] = solution
                issue['fix_result'] = result

                # Verify system state
                if success:
                    self._verify_and_update_issue(issue)

            # Add to issues list
            self.issues.append(issue)

        # Generate report
        report = self.reporter.generate_report(self.issues)
        self.reporter.save_report(report)
        self.logger.info("Monitoring cycle completed")

    def _get_user_confirmation(self, issue: Dict[str, Any], solution: str) -> bool:
        """Get user confirmation for applying a fix"""
        print("\n" + "=" * 80)
        print("ISSUE DETECTED:")
        print("-" * 80)
        print(f"Error: {issue['error_line']}")
        print("\nContext:")
        for line in issue['context']:
            print(f"  {line}")

        print("\nRECOMMENDED SOLUTION:")
        print("-" * 80)
        print(solution)
        print("-" * 80)

        while True:
            response = input("Apply this solution? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please answer 'yes' or 'no'")

    def _verify_and_update_issue(self, issue: Dict[str, Any]):
        """Verify system state after fix and update issue"""
        verification_results = []

        # Verify pods
        pods_ok, pods_message = self.verifier.verify_pods_running()
        verification_results.append(f"Pods status: {pods_message}")

        # Verify application
        app_ok, app_message = self.verifier.verify_application_running(self.application_endpoint)
        verification_results.append(f"Application status: {app_message}")

        # Update issue with verification results
        issue['verification_results'] = "\n".join(verification_results)
        issue['fully_resolved'] = pods_ok and app_ok

    def run_continuous_monitoring(self, interval_seconds: int = 60):
        """Run continuous monitoring with the specified interval"""
        self.logger.info(f"Starting continuous monitoring with {interval_seconds}s interval")

        try:
            while True:
                self.run_monitoring_cycle()
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
            # Generate final report
            report = self.reporter.generate_report(self.issues)
            self.reporter.save_report(report)