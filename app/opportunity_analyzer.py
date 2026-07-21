class OpportunityAnalyzer:

    def analyze(self, videos):

        if not videos:
            return {
                "opportunity": "Low",
                "reason": "No videos found."
            }

        avg_score = sum(
            video["score"] for video in videos
        ) / len(videos)

        avg_views = sum(
            video["views"] for video in videos
        ) / len(videos)

        newest = min(
            video["days_old"] for video in videos
        )

        if avg_score > 1000:
            opportunity = "High"

        elif avg_score > 500:
            opportunity = "Medium"

        else:
            opportunity = "Low"

        return {
            "opportunity": opportunity,
            "average_score": round(avg_score, 2),
            "average_views": int(avg_views),
            "newest_video_days": newest,
            "videos_analyzed": len(videos)
        }