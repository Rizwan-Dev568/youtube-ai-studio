from pathlib import Path

from agents.base_agent import BaseAgent
from app.file_manager import FileManager


class ThumbnailAgent(BaseAgent):

    def generate(self, topic):

        prompt_path = (
            Path(__file__).parent
            / "prompts"
            / "thumbnail_prompt.txt"
        )

        prompt = FileManager.read_text(prompt_path)

        prompt = prompt.replace(
            "{topic}",
            topic
        )

        return self.ask(prompt)