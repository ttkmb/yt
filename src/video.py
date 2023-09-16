import os
from googleapiclient.discovery import build


class Video:
    """Класс для видео"""

    title = ""
    url = ""
    count_views = 0
    count_likes = 0

    def __init__(self, video_id):
        try:
            self.video_id = video_id
            data = self.get_video_data()
            self.title = data['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/' + f'{self.video_id}'
            self.count_views = data['items'][0]['statistics']['viewCount']
            self.count_likes = data['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.link = None
            self.views_count = None
            self.like_count = None

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_video_data(self):
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.video_id
                                                          ).execute()
        return video_response

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, pl_id):
        super().__init__(video_id)
        self.pl_id = pl_id

    def __str__(self):
        return self.title
