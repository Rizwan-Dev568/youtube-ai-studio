"""
Director Agent

Final AI Decision Maker
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import DIRECTOR_SCHEMA


class DirectorAgent(BaseAgent):

    schema = DIRECTOR_SCHEMA

    def __init__(self):

        super().__init__()

    def review_workflow(
        self,
        workflow
    ):

        prompt = self.load_prompt(
            "director_prompt.txt"
        )

        prompt = prompt.replace(
            "{workflow}",
            json.dumps(
                workflow,
                indent=2,
                ensure_ascii=False
            )
        )

        return self.ask(prompt)