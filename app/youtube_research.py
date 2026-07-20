from app.youtube_client import YouTubeClient
from app.trend_analyzer import TrendAnalyzer
from app.video_ranker import VideoRanker


class YouTubeResearch:

    def __init__(self):
        self.youtube = YouTubeClient()
        self.analyzer = TrendAnalyzer()
        self.ranker = VideoRanker()

    def research(self, topic):

        search = self.youtube.search_videos(topic)

        analyzed = self.analyzer.analyze(search)

        ranked = self.ranker.rank(analyzed)

        return ranked