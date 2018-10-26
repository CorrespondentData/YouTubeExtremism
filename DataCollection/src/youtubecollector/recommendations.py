import csv


def get_recommendations(video_id, youtube_client):
    return youtube_client.search().list(
        # videoId = video_id,
        part='snippet',
        type='video',
        relatedToVideoId=video_id,
        maxResults=50
    ).execute()


def write_recommendations(response, recommendations_file, video_id):
    header = ['videoId', 'targetVideoId', 'publishedAt', 'channelId', 'title', 'description']

    with open(recommendations_file, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)

        for data in response['items']:
            writer.writerow(({'videoId': video_id,
                              'targetVideoId': data['id']['videoId'],
                              'publishedAt': data['snippet']['publishedAt'],
                              'channelId': data['snippet']['channelId'],
                              'title': data['snippet']['title'],
                              'description': data['snippet']['description']
                              }))
