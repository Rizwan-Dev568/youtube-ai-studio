from app.youtube_client import YouTubeClient
from app.trend_analyzer import TrendAnalyzer
from app.video_ranker import VideoRanker
from app.opportunity_analyzer import OpportunityAnalyzer


class YouTubeResearch:

    def __init__(self):
        self.youtube = YouTubeClient()
        self.analyzer = TrendAnalyzer()
        self.ranker = VideoRanker()
        self.opportunity = OpportunityAnalyzer()

    def research(self, topic):

        # Step 1: Search videos
        search = self.youtube.search_videos(topic)

        # Step 2: Get video IDs
        ids = [
            item["id"]["videoId"]
            for item in search["items"]
        ]

        # Step 3: Get video details
        details = self.youtube.get_video_details(ids)

        # Step 4: Rank videos
        ranked = self.ranker.rank(details)

        # Step 5: Analyze opportunity
        report = self.opportunity.analyze(ranked)

        # Final result
        return {
            "topic": topic,
            "report": report,
            "videos": ranked
        }