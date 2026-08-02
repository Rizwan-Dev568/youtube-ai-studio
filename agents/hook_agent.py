"""
Hook Agent
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import HOOK_SCHEMA


class HookAgent(BaseAgent):

    schema = HOOK_SCHEMA

    def __init__(self):
        super().__init__()

    def generate(self, research, seo):

        if isinstance(research, dict):
            research = json.dumps(
                research,
                indent=2,
                ensure_ascii=False
            )

        if isinstance(seo, dict):
            seo = json.dumps(
                seo,
                indent=2,
                ensure_ascii=False
            )

        prompt = self.load_prompt(
            "hook_prompt.txt"
        )

        prompt = prompt.replace(
            "{research}",
            research
        )

        prompt = prompt.replace(
            "{seo}",
            seo
        )

        return self.ask(
            prompt,
            self.schema
        )