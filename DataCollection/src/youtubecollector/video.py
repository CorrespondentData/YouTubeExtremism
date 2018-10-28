import csv
from collections import namedtuple as _namedtuple

from .util import is_empty_file as _is_empty_file
from .util import convert_to_dictionary as _convert_to_dictionary

video = _namedtuple("video", ('video_published',
                              'video_id',
                              'channel_id',
                              'video_title',
                              'video_description',
                              'channel_title',
                              'video_category_id',
                              'video_tags',
                              'video_duration',
                              'video_view_count',
                              'video_comment_count',
                              'video_likes_count',
                              'video_dislikes_count',
                              'video_topic_ids',
                              'video_topic_categories'))


def _get_video_header():
    return video._fields


def get_videos(channel, youtube_client, max_results=50, next_page_token=None):
    return youtube_client.search().list(
        channelId=channel,
        type='video',
        part='snippet',
        maxResults=max_results,
        pageToken=next_page_token
    ).execute()


def _get_video_metadata(video_id, youtube_client):
    return youtube_client.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    ).execute()


def convert_to_videos(response):
    videos = list()
    for data in response['items']:
        video_id = data['id']['videoId']
        video_metadata = _get_video_metadata(video_id)
        metadata = video_metadata['items'][0]

        next_video = video(video_published=data['snippet']['publishedAt'],
                           video_id=video_id,
                           channel_id=data['snippet']['channelId'],
                           video_title=data['snippet']['title'],
                           video_description=data['snippet']['description'],
                           channel_title=data['snippet']['channelTitle'],
                           video_category_id=metadata['snippet'].get('categoryId', 'not set'),
                           video_duration=metadata['contentDetails']['duration'],
                           video_view_count=metadata['statistics']['viewCount'],
                           video_comment_count=metadata['statistics'].get('commentCount', 0),
                           video_likes_count=metadata['statistics'].get('likeCount', 0),
                           video_tags=metadata['snippet'].get('tags', 'not set'),
                           video_dislikes_count=metadata['statistics'].get('dislikeCount', 0),
                           video_topic_ids=metadata['topicDetails'].get('topicIds', "not set"),
                           video_topic_categories=metadata['topicDetails'].get('topicCategories', "not set")
                           )
        videos.append(next_video)

    return videos


def write_video_data_to_file(videos, video_file):
    with open(video_file, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=_get_video_header())
        if _is_empty_file(video_file):
            writer.writeheader()

        for video_row in videos:
            writer.writerow(_convert_to_dictionary(video_row))
