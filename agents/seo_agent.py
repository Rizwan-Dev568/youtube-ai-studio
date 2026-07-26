from agents.base_agent import BaseAgent
import json


class SEOAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def generate(self, research):

        if isinstance(research, dict):
            research = json.dumps(
                research,
                indent=2
            )

        prompt = self.load_prompt(
            "seo_prompt.txt"
        )

        prompt = prompt.replace(
            "{research}",
            research
        )

        return self.ask(prompt)