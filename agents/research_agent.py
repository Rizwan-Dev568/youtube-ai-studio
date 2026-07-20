from app.youtube_research import YouTubeResearch


class ResearchAgent:

    def __init__(self):
        self.researcher = YouTubeResearch()

    def research(self, topic):

        return self.researcher.research(topic)