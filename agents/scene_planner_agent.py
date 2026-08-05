"""
Scene Planner Agent

Converts a script into a complete
scene-by-scene production plan.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import SCENE_PLAN_SCHEMA


class ScenePlannerAgent(BaseAgent):

    schema = SCENE_PLAN_SCHEMA

    def __init__(self):

        super().__init__()

    def generate(
        self,
        script
    ):

        prompt = self.load_prompt(
            "scene_planner_prompt.txt"
        )

        prompt = prompt.replace(
            "{script}",
            json.dumps(
                script,
                indent=2,
                ensure_ascii=False
            )
        )

        return self.ask(prompt)