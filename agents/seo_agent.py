from agents.base_agent import BaseAgent


class SEOAgent(BaseAgent):

    def __init__(self):

        super().__init__()

    def generate(self, topic):

        prompt = self.load_prompt("seo_prompt.txt")

        prompt = prompt.replace(
            "{topic}",
            topic
        )

        return self.ask(prompt)