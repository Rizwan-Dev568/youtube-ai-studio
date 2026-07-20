from app.ai_client import AIClient


class SEOAgent:

    def __init__(self):
        self.ai = AIClient()

    def generate(self, topic):

        prompt = f"""
You are the world's best YouTube SEO Expert.

Topic:
{topic}

Generate:

1. Viral SEO Title
2. SEO Description
3. 30 High Search Tags
4. 20 High Search Keywords
5. Thumbnail Text
6. Viral Score (0-100)
7. Competition (Low/Medium/High)
8. Best Video Length
9. Target Audience

Return in professional markdown.
"""

        return self.ai.ask(prompt)