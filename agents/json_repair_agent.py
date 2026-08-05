"""
JSON Repair Agent

Repairs malformed AI JSON responses.
"""

from agents.base_agent import BaseAgent


class JsonRepairAgent(BaseAgent):

    def repair(self, broken_json):

        prompt = self.load_prompt(
            "json_repair_prompt.txt"
        )

        prompt = prompt.replace(
            "{json}",
            broken_json
        )

        return self.ai.ask(
            prompt=prompt,
            schema=None
        )