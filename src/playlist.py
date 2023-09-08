import isodate

from src.channel import Channel
import os
from googleapiclient.discovery import build
import datetime


class PlayList:
    title = ''
    utl = ''

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_playlist_data(self):
        """Данные одного плейлиста"""
        playlist = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                               part='contentDetails, id, snippet, status',
                                                               maxResults=50,
                                                               ).execute()
        return playlist

    def get_playlist_title(self):
        """
        Получение названия плейлиста
        """
        data = self.get_playlist_data()
        channel_id = data['items'][0]['snippet']['channelId']
        pl_title = PlayList.get_service().playlists().list(channelId=channel_id,
                                                           part='contentDetails,snippet',
                                                           maxResults=50,
                                                           ).execute()
        for playlist in pl_title['items']:
            if self.playlist_id == playlist['id']:
                return playlist['snippet']['title']

    def get_videos_ids(self):
        """
        Возвращает id видеороликов в плейлисте
        """
        data = self.get_playlist_data()
        videos = []
        for video in data['items']:
            videos.append(video['contentDetails']['videoId'])
        return videos

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def total_duration(self):
        """
        Возвращает суммарную длительность плейлиста
        """
        ttl_duration = datetime.timedelta()
        video_ids = self.get_videos_ids()
        video_duration = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()
        for video in video_duration['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            ttl_duration += duration
        return ttl_duration

    def show_best_video(self):
        """
        Возвращает ссылку на лучшее видео по количеству лайков
        """
        likes = {}
        video_ids = self.get_videos_ids()
        most_liked = 0
        for video_id in video_ids:
            video_response = PlayList.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                                      id=video_id
                                                                                      ).execute()

            likes_count = video_response['items'][0]['statistics']['likeCount']
            likes[likes_count] = f'https://youtu.be/' + f'{video_id}'
            for like in likes.keys():
                if most_liked < int(like):
                    most_liked = int(like)
                    most_liked_id = f'https://youtu.be/' + f'{video_id}'

        return most_liked_id
