import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    title = ""
    description = ""
    url = ""
    channel_subscription_count = 0
    video_count = 0
    channel_views_count = 0

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        data = self.print_info()
        self.title = data['items'][0]['snippet']['title']
        self.description = data['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + data['items'][0]['snippet']['customUrl']
        self.channel_subscription_count = int(data['items'][0]['statistics']['subscriberCount'])
        self.video_count = data['items'][0]['statistics']['videoCount']
        self.channel_views_count = data['items'][0]['statistics']['viewCount']

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'channel_subscription_count': self.channel_subscription_count,
            'video_count': self.video_count,
            'channel_views_count': self.channel_views_count}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)

