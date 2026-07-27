from agents.base_agent import BaseAgent


class TitleRankerAgent(BaseAgent):

    def generate(self, titles):

        prompt = self.load_prompt(
            "title_ranker_prompt.txt"
        )

        prompt = prompt.replace(
            "{titles}",
            str(titles)
        )

        return self.ask(prompt)