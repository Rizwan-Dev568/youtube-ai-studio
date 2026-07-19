from app.youtube_client import YouTubeClient
from app.video_ranker import VideoRanker
from app.openai_client import OpenAIClient

yt = YouTubeClient()
ranker = VideoRanker()
ai = OpenAIClient()

search = yt.search_videos("Artificial Intelligence")

video_ids = [
    item["id"]["videoId"]
    for item in search["items"]
]

details = yt.get_video_details(video_ids)

videos = ranker.rank(details)

prompt = f"""
Analyze these YouTube videos.

{videos}

Tell me:

1. What topics are trending?
2. Which video idea should I make?
3. Give me 5 unique video ideas.
4. Give each idea a viral score out of 10.

Return in clean markdown.
"""

answer = ai.ask(prompt)

print(answer)