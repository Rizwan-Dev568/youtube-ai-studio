from app.openai_client import OpenAIClient


class TrendHunter:

    def __init__(self):
        self.ai = OpenAIClient()

    def find_topics(self, niche: str):

        prompt = f"""
You are a professional YouTube strategist.

Find 10 viral YouTube video ideas.

Niche:
{niche}

Return only:

Title
Why Viral
Difficulty
Viral Score out of 10
"""

        return self.ai.ask(prompt)