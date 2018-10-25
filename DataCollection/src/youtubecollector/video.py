import csv
from apiclient.discovery import build


def get_videos(channel, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY):
    '''Takes a channel_id and finds
    the first 50 videos'''
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.search().list(
        channelId=channel,
        type='video',
        part='snippet',
        maxResults=50,
    ).execute()
    print('getting videos for ' + channel)
    return response


def get_more_videos(channel, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY, nextPageToken):
    '''Takes a channel_id and looks for
    the next page in the result list.'''
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.search().list(
        channelId=channel,
        type='video',
        part='snippet',
        maxResults=50,
        pageToken=nextPageToken
    ).execute()
    print('getting more pages of ' + channel)

    return response


def get_video_metadata(video_id, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY):
    '''Takes a video_id and gets
    the associated metadata'''

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    ).execute()

    return response


def write_video_data_to_file(response, video_file):
    '''Write the video data to a file'''

    with open(video_file, "a") as csvFile:
        fieldnames = ['video_published',
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
                      'video_topic_categories'
                      ]

        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        for video in response['items']:

            video_published = video['snippet']['publishedAt']
            video_id = video['id']['videoId']
            channel_id = video['snippet']['channelId']
            video_title = video['snippet']['title']
            video_description = video['snippet']['description']
            channel_title = video['snippet']['channelTitle']
            try:
                video_category_id = video['snippet']['categoryId']
            except:
                video_category_id = 'not set'
            try:
                video_tags = video['snippet']['tags']
            except:
                video_tags = 'not set'

            video_metadata = get_video_metadata(video_id)

            for metadata in video_metadata['items']:
                print('getting metadata for ' + video_title)

                video_duration = metadata['contentDetails']['duration']
                video_view_count = metadata['statistics']['viewCount']
                try:
                    video_comment_count = metadata['statistics']['commentCount']
                except:
                    video_comment_count = 0

                try:
                    video_likes_count = metadata['statistics']['likeCount']
                except:
                    video_likes_count = 0

                try:
                    video_dislikes_count = metadata['statistics']['dislikeCount']
                except:
                    video_dislikes_count = 0

                try:
                    video_topic_ids = metadata['topicDetails']['topicIds']
                except:
                    video_topic_ids = 'not set'
                try:
                    video_topic_categories = metadata['topicDetails']['topicCategories']
                except:
                    video_topic_categories = 'not set'
                try:
                    video_category_id = metadata['snippet']['categoryId']
                except:
                    video_category_id = 'not set'
                try:
                    video_tags = metadata['snippet']['tags']
                except:
                    video_tags = 'not set'

                writer.writerow({'video_published': video_published,
                                 'video_id': video_id,
                                 'channel_id': channel_id,
                                 'video_title': video_title,
                                 'video_description': video_description,
                                 'channel_title': channel_title,
                                 'video_category_id': video_category_id,
                                 'video_tags': video_tags,
                                 'video_duration': video_duration,
                                 'video_view_count': video_view_count,
                                 'video_comment_count': video_comment_count,
                                 'video_likes_count': video_likes_count,
                                 'video_dislikes_count': video_dislikes_count,
                                 'video_topic_ids': video_topic_ids,
                                 'video_topic_categories': video_topic_categories
                                 })
    return response
