from typing import Dict, Any

import requests

from Agents.BaseAgent import BaseAgent


class SolutionRecommendationAgent(BaseAgent):
    """Agent responsible for suggesting solutions to detected issues using LLM"""

    def __init__(self, api_key: str, api_url: str, model_name: str):
        super().__init__("SolutionRecommender")
        self.api_key = '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'
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.model_name = 'llama3-70b-8192'

    def get_solution_recommendation(self, issue: Dict[str, Any]) -> str:
        """Query LLM to get solution recommendations for the given issue"""
        prompt = self._build_prompt(issue)
        response = self._query_llm(prompt)
        return response

    def _build_prompt(self, issue: Dict[str, Any]) -> str:
        """Build a prompt for the LLM based on the issue"""
        context = "\n".join(issue["context"])

        prompt = f"""
        You are a DevOps expert helping to fix build and deployment issues.

        Here is a log snippet containing an error:

        {context}

        The specific error line is:
        {issue["error_line"]}

        Based on these logs, what is the most likely cause of the issue and how would you fix it?
        Provide a clear explanation and specific steps to resolve the problem.
        Keep your answer concise and actionable.
        """

        return prompt

    def _query_llm(self, prompt: str) -> str:
        """Query the LLM API to get a response"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": self.model_name,  # or your preferred model
                "messages": [
                    {"role": "system", "content": "You are a helpful DevOps and build system expert."},
                    {"role": "user", "content": prompt}
                ],
            }

            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()

            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            self.log(f"Error querying LLM API: {str(e)}", "error")
            return "Unable to get solution recommendation due to API error."