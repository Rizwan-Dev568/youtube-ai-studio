"""
Title Ranker Agent
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import TITLE_RANK_SCHEMA


class TitleRankerAgent(BaseAgent):

    schema = TITLE_RANK_SCHEMA

    def __init__(self):
        super().__init__()

    def generate(self, titles):

        if isinstance(titles, list):
            titles = json.dumps(
                titles,
                indent=2
            )

        prompt = self.load_prompt(
            "title_ranker_prompt.txt"
        )

        prompt = prompt.replace(
            "{titles}",
            titles
        )

        return self.ask(prompt)