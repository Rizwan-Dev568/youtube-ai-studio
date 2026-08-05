"""
Reviewer Agent

Reviews all generated content before final output.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import REVIEW_SCHEMA


class ReviewerAgent(BaseAgent):

    schema = REVIEW_SCHEMA

    def __init__(self):
        super().__init__()

    def review(
        self,
        research,
        seo,
        title_rank,
        hooks,
        thumbnail,
        script,
    ):

        data = {
            "research": research,
            "seo": seo,
            "title_rank": title_rank,
            "hooks": hooks,
            "thumbnail": thumbnail,
            "script": script,
        }

        prompt = self.load_prompt(
            "review_prompt.txt"
        )

        prompt = prompt.replace(
            "{workflow}",
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )

        return self.ask(prompt)