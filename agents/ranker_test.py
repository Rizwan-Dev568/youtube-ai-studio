from app.youtube_client import YouTubeClient
from app.video_ranker import VideoRanker

yt = YouTubeClient()
ranker = VideoRanker()

search = yt.search_videos("Artificial Intelligence")

video_ids = [
    item["id"]["videoId"]
    for item in search["items"]
]

details = yt.get_video_details(video_ids)

videos = ranker.rank(details)

for video in videos:
    print(video)