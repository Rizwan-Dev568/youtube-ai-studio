from app.logger import Logger
from app.file_manager import FileManager
from config.settings import OUTPUT_FOLDER


class BaseAgent:

    def __init__(self, agent_name):
        self.agent_name = agent_name
        FileManager.create_folder(OUTPUT_FOLDER)
        Logger.success(f"{self.agent_name} Initialized")

    def log(self, message):
        Logger.info(f"[{self.agent_name}] {message}")