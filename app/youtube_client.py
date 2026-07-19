import requests
from config.settings import YOUTUBE_API_KEY


class YouTubeClient:

    def search_videos(self, query, max_results=10):

        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()


    def get_video_details(self, video_ids):

        url = "https://www.googleapis.com/youtube/v3/videos"

        params = {
            "part": "statistics,contentDetails,snippet",
            "id": ",".join(video_ids),
            "key": YOUTUBE_API_KEY
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()