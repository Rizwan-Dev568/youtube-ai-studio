from datetime import datetime, timezone


class VideoRanker:

    def rank(self, youtube_details):

        results = []

        for item in youtube_details.get("items", []):

            stats = item.get("statistics", {})
            snippet = item.get("snippet", {})
            content = item.get("contentDetails", {})

            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))

            published = snippet.get("publishedAt")

            if published:
                publish_date = datetime.fromisoformat(
                    published.replace("Z", "+00:00")
                )

                days = (
                    datetime.now(timezone.utc)
                    - publish_date
                ).days
            else:
                days = 0

            score = (
                views * 0.001 +
                likes * 0.05 +
                comments * 0.2
            )

            results.append({

                "video_id": item.get("id"),

                "title": snippet.get("title"),

                "description": snippet.get(
                    "description"
                ),

                "channel": snippet.get(
                    "channelTitle"
                ),

                "channel_id": snippet.get(
                    "channelId"
                ),

                "published_at": published,

                "thumbnail": (
                    snippet.get(
                        "thumbnails",
                        {}
                    )
                    .get(
                        "high",
                        {}
                    )
                    .get(
                        "url"
                    )
                ),

                "duration": content.get(
                    "duration"
                ),

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