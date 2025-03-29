from typing import Dict, Any
from groq import Groq
import requests
from Agents.BaseAgent import BaseAgent


class SolutionRecommendationAgent(BaseAgent):
    """Agent responsible for suggesting solutions to detected issues using LLM"""

    def __init__(self, api_key: str, api_url: str, model_name: str):
        super().__init__("SolutionRecommender")
        self.api_key = api_key
        self.api_url = api_url
        self.model_name = model_name

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
            client = Groq(api_key=self.api_key)

            payload = {
                "model": self.model_name,  # or your preferred model
                "messages": [
                    {"role": "system", "content": "You are a helpful DevOps and build system expert."},
                    {"role": "user", "content": prompt}
                ],
            }

            # Send the message and get the response
            chat_completion = client.chat.completions.create(
                messages=payload['messages'],
                model=self.model_name,
                temperature=0.7,
                max_tokens=1000,
            )

            # Print the response
            return (chat_completion.choices[0].message.content)

        except Exception as e:
            self.log(f"Error querying LLM: {str(e)}", "error")
            return "Unable to get solution recommendation due to GROQ error."