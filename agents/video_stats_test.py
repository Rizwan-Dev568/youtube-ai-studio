from app.youtube_client import YouTubeClient

yt = YouTubeClient()

search = yt.search_videos("Artificial Intelligence")

video_ids = []

for item in search["items"]:
    video_ids.append(item["id"]["videoId"])

details = yt.get_video_details(video_ids)

print(details)