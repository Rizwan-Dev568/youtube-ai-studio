from app.youtube_client import YouTubeClient

yt = YouTubeClient()

data = yt.search_videos("Artificial Intelligence")

print(data)