import re
import subprocess
from typing import List, Dict, Any, Tuple

from Agents.BaseAgent import BaseAgent


class FixImplementationAgent(BaseAgent):
    """Agent responsible for implementing fixes based on recommendations"""

    def __init__(self):
        super().__init__("FixImplementer")

    def apply_fix(self, issue: Dict[str, Any], solution: str, user_confirmation: bool) -> Tuple[bool, str]:
        """Apply the fix based on the solution and user confirmation"""
        if not user_confirmation:
            return False, "Fix not applied due to lack of user confirmation"

        # Parse the solution to extract actionable commands
        commands = self._extract_commands_from_solution(solution)

        if not commands:
            return False, "No actionable commands found in the solution"

        # Execute the commands
        results = []
        success = True

        for cmd in commands:
            try:
                self.log(f"Executing command: {cmd}")
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                results.append(f"Command '{cmd}' executed successfully")

            except subprocess.CalledProcessError as e:
                success = False
                error_message = f"Command '{cmd}' failed with error: {e.stderr}"
                results.append(error_message)
                self.log(error_message, "error")

        return success, "\n".join(results)

    def _extract_commands_from_solution(self, solution: str) -> List[str]:
        """Extract executable commands from the solution text"""
        # Look for commands in code blocks or after keywords like "run", "execute", etc.
        commands = []

        # Extract commands from markdown code blocks
        code_block_pattern = r"```(?:bash|shell|sh)?\n(.*?)\n```"
        code_blocks = re.findall(code_block_pattern, solution, re.DOTALL)

        for block in code_blocks:
            # Split multi-line commands
            block_commands = [cmd.strip() for cmd in block.split("\n") if cmd.strip()]
            commands.extend(block_commands)

        # If no code blocks, look for command lines
        if not commands:
            command_line_patterns = [
                r"Run:?\s+`(.*?)`",
                r"Execute:?\s+`(.*?)`",
                r"Command:?\s+`(.*?)`",
                r"^\$\s+(.*?)$"
            ]

            for pattern in command_line_patterns:
                command_matches = re.findall(pattern, solution, re.MULTILINE)
                commands.extend([cmd.strip() for cmd in command_matches])

        return commands