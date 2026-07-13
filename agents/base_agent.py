"""
Base Agent
All AI agents will inherit from this class.
"""

class BaseAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name

    def log(self, message):
        print(f"[{self.agent_name}] {message}")