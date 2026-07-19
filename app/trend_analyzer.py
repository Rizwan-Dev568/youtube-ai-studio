class TrendAnalyzer:

    def analyze(self, youtube_data):
        videos = []

        for item in youtube_data.get("items", []):
            snippet = item["snippet"]

            videos.append({
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "published": snippet["publishedAt"],
                "video_id": item["id"]["videoId"]
            })

        return videos