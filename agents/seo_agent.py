from agents.base_agent import BaseAgent
from app.output_schema import SEO_SCHEMA

import json


class SEOAgent(BaseAgent):

    schema = SEO_SCHEMA

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