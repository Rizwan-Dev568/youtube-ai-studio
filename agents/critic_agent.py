from agents.base_agent import BaseAgent
import json


class CriticAgent(BaseAgent):

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
            "critic_prompt.txt"
        )

        prompt = prompt.replace(
            "{data}",
            json.dumps(
                data,
                indent=2
            )
        )

        return self.ask(prompt)