from agents.base_agent import BaseAgent
from app.output_schema import SCRIPT_SCHEMA

import json


class ScriptWriter(BaseAgent):

    schema = SCRIPT_SCHEMA

    def __init__(self):
        super().__init__()

    def write_script(self, research, seo):

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
            "script_prompt.txt"
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
            schema=self.schema
        )