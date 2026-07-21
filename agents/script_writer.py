from agents.base_agent import BaseAgent


class ScriptWriter(BaseAgent):

    def __init__(self):

        super().__init__()

    def write_script(self, topic):

        prompt = self.load_prompt(
            "script_prompt.txt"
        )

        prompt = prompt.replace(
            "{topic}",
            topic
        )

        return self.ask(prompt)