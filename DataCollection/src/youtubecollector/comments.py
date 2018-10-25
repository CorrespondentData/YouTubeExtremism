from googleapiclient.discovery import build
import csv


def get_comments(videoId, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.commentThreads().list(
        videoId=videoId,
        part='snippet,replies'
    ).execute()

    return response


def get_more_comments(videoId, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY, nextPageToken):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.commentThreads().list(
        videoId=videoId,
        pageToken=nextPageToken,
        part='snippet,replies'
    ).execute()

    return response


def write_comments(response, comments_file):
    with open(comments_file, 'a') as csvFile:
        header = ['video_id',
                  'comment_id',
                  'author_display_name',
                  'author_channel_url',
                  'author_channel_id',
                  'comment_text',
                  'comment_like_count',
                  'comment_dislike_count']
        writer = csv.DictWriter(csvFile, fieldnames=header)
        writer.writeheader()
        for data in response['items']:
            comment_id = data['id']
            video_id = data['snippet']['videoId']
            author_display_name = data['snippet']['topLevelComment']['snippet']['authorDisplayName']
            author_channel_url = data['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            author_channel_id = data['snippetauthorChannelId']['topLevelComment']['snippet']['authorChannelId']['value']
            comment_text = data['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_likes_count = data['snippet']['topLevelComment']['snippet']['likeCount']
            comment_dislikes_count = data['snippet']['topLevelComment']['snippet']['disLikeCount']
            comment_time = data['snippet']['topLevelComment']['snippet']['publishedAt']

            writer.writerow(({'video_id': video_id,
                              'comment_id': comment_id,
                              'author_display_name': author_display_name,
                              'author_channel_url': author_channel_url,
                              'author_channel_id': author_channel_id,
                              'comment_text': comment_text,
                              'comment_like_count': comment_likes_count,
                              'comment_dislike_count': comment_dislikes_count,
                              'comment_time': comment_time
                              }))
