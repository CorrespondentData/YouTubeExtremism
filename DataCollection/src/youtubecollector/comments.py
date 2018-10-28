import csv
from collections import namedtuple as _namedtuple
from .util import is_empty_file as _is_empty_file
from .util import convert_to_dictionary as _convert_to_dictionary

comment = _namedtuple("comment", ('video_id',
                                  'comment_id',
                                  'author_display_name',
                                  'author_channel_url',
                                  'author_channel_id',
                                  'comment_text',
                                  'comment_like_count',
                                  'comment_dislike_count',
                                  'comment_time'))


def _get_comment_header():
    return comment._fields


def get_comments(video_id, youtube_client, next_page_token=None):
    return youtube_client.commentThreads().list(
        videoId=video_id,
        part='snippet,replies',
        pageToken=next_page_token
    ).execute()


def convert_to_comments(response):
    comments = list()
    for data in response['items']:
        comments.append(comment(comment_id=data['id'],
                                video_id=data['snippet']['videoId'],
                                author_display_name=data['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                author_channel_url=data['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                                author_channel_id=data['snippetauthorChannelId']['topLevelComment']['snippet']
                                ['authorChannelId']['value'],
                                comment_text=data['snippet']['topLevelComment']['snippet']['textDisplay'],
                                comment_like_count=data['snippet']['topLevelComment']['snippet']['likeCount'],
                                comment_dislike_count=data['snippet']['topLevelComment']['snippet']['disLikeCount'],
                                comment_time=data['snippet']['topLevelComment']['snippet']['publishedAt'])
                        )
    return comments


def write_comments(comments_file, comments):
    with open(comments_file, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=_get_comment_header())
        if _is_empty_file(comments_file):
            writer.writeheader()

        for comment_row in comments:
            writer.writerow(_convert_to_dictionary(comment_row))
