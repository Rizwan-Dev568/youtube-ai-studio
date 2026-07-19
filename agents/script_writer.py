from app.ai_client import AIClient


class ScriptWriter:

    def __init__(self):
        self.ai = AIClient()

    def write_script(self, topic):

        prompt = f"""
You are a professional YouTube script writer.

Write a 10 minute engaging script.

Topic:

{topic}

Requirements:

- Strong Hook
- Curiosity
- Storytelling
- Simple English
- Ending CTA

"""

        return self.ai.ask(prompt)