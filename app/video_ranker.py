from datetime import datetime, timezone


class VideoRanker:

    def rank(self, youtube_details):

        results = []

        for item in youtube_details.get("items", []):

            stats = item["statistics"]
            snippet = item["snippet"]

            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))

            published = snippet["publishedAt"]

            publish_date = datetime.fromisoformat(
                published.replace("Z", "+00:00")
            )

            days = (datetime.now(timezone.utc) - publish_date).days

            score = (
                views * 0.001 +
                likes * 0.05 +
                comments * 0.2
            )

            results.append({
                "title": snippet["title"],
                "views": views,
                "likes": likes,
                "comments": comments,
                "days_old": days,
                "score": round(score, 2)
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results