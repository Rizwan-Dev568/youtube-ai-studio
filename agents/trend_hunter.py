from base_agent import BaseAgent


class TrendHunter(BaseAgent):

    def __init__(self):
        super().__init__("Trend Hunter")

    def start(self):
        self.log("Searching for trending topics...")


if __name__ == "__main__":
    agent = TrendHunter()
    agent.start()