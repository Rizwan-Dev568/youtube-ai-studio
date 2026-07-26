from agents.base_agent import BaseAgent
import json


class HookAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def generate(self, research, seo):

        if isinstance(research, dict):
            research = json.dumps(
                research,
                indent=2
            )

        if isinstance(seo, dict):
            seo = json.dumps(
                seo,
                indent=2
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

        return self.ask(prompt)