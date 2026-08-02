from app.youtube_client import YouTubeClient
from app.video_ranker import VideoRanker
from app.opportunity_analyzer import OpportunityAnalyzer


class YouTubeResearch:

    def __init__(self):

        self.youtube = YouTubeClient()
        self.ranker = VideoRanker()
        self.opportunity = OpportunityAnalyzer()

    def research(self, topic):

        # Search
        search = self.youtube.search_videos(topic)

        ids = [
            item["id"]["videoId"]
            for item in search["items"]
        ]

        details = self.youtube.get_video_details(ids)

        ranked = self.ranker.rank(details)

        report = self.opportunity.analyze(ranked)

        # Keep only Top 5 videos
        top_videos = []

        for video in ranked[:5]:

            top_videos.append({

                "title": video.get("title"),

                "views": video.get("views"),

                "likes": video.get("likes"),

                "channel": video.get("channel"),

                "score": video.get("score")

            })

        return {

            "topic": topic,

            "summary": report,

            "top_videos": top_videos

        }