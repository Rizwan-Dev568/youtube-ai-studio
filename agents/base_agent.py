"""
Base Agent

All AI agents inherit from this class.
"""

from pathlib import Path

from app.ai_client import AIClient
from app.file_manager import FileManager
from app.response_parser import ResponseParser


class BaseAgent:

    def __init__(self):

        self.ai = AIClient()

    def load_prompt(self, filename):

        prompt_path = (
            Path(__file__).parent
            / "prompts"
            / filename
        )

        return FileManager.read_text(prompt_path)

    def ask(self, prompt):

        response = self.ai.ask(prompt)

        return ResponseParser.parse(response)