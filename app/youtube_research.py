from app.youtube_client import YouTubeClient
from app.video_ranker import VideoRanker
from app.opportunity_analyzer import OpportunityAnalyzer


class YouTubeResearch:

    def __init__(self):

        self.youtube = YouTubeClient()
        self.ranker = VideoRanker()
        self.opportunity = OpportunityAnalyzer()

    def research(self, topic):

        search = self.youtube.search_videos(topic)

        ids = []

        for item in search.get("items", []):

            video_id = (
                item.get("id", {})
                .get("videoId")
            )

            if video_id:
                ids.append(video_id)

        if not ids:

            return {
                "topic": topic,
                "summary": {},
                "top_videos": []
            }

        details = self.youtube.get_video_details(ids)

        ranked = self.ranker.rank(details)

        report = self.opportunity.analyze(ranked)

        top_videos = []

        for video in ranked[:5]:

            top_videos.append({

                "title": video.get("title"),

                "video_id": video.get("video_id"),

                "video_url":
                    f"https://www.youtube.com/watch?v={video.get('video_id')}",

                "channel": video.get("channel"),

                "channel_id": video.get("channel_id"),

                "published_at": video.get("published_at"),

                "thumbnail": video.get("thumbnail"),

                "description": video.get("description"),

                "views": video.get("views"),

                "likes": video.get("likes"),

                "comments": video.get("comments"),

                "duration": video.get("duration"),

                "days_old": video.get("days_old"),

                "score": video.get("score")

            })

        return {

            "topic": topic,

            "summary": report,

            "top_videos": top_videos

        }