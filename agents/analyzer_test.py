from app.youtube_client import YouTubeClient
from app.trend_analyzer import TrendAnalyzer

yt = YouTubeClient()
analyzer = TrendAnalyzer()

data = yt.search_videos("Artificial Intelligence")

videos = analyzer.analyze(data)

for video in videos:
    print(video)