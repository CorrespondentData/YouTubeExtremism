import csv


def get_comments(video_id, youtube_client):
    return youtube_client.commentThreads().list(
        videoId=video_id,
        part='snippet,replies'
    ).execute()


def get_more_comments(video_id, youtube_client, next_page_token):
    return youtube_client.commentThreads().list(
        videoId=video_id,
        pageToken=next_page_token,
        part='snippet,replies'
    ).execute()


def write_comments(comments_file, response):
    header = ['video_id',
              'comment_id',
              'author_display_name',
              'author_channel_url',
              'author_channel_id',
              'comment_text',
              'comment_like_count',
              'comment_dislike_count']

    with open(comments_file, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
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
