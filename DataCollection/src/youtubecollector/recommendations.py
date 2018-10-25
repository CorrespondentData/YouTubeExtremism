from apiclient.discovery import build
import csv


def get_recommendations(video_id, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.search().list(
        # videoId = video_id,
        part='snippet',
        type='video',
        relatedToVideoId=video_id,
        maxResults=50
    ).execute()

    return response


def write_recommendations(response, recommendations_file, videoId):
    for data in response['items']:
        targetVideoId = data['id']['videoId']
        publishedAt = data['snippet']['publishedAt']
        channelId = data['snippet']['channelId']
        title = data['snippet']['title']
        description = data['snippet']['description']

        with open(recommendations_file, 'a') as csvFile:
            header = ['videoId', 'targetVideoId', 'publishedAt', 'channelId', 'title', 'description']
            writer = csv.DictWriter(csvFile, fieldnames=header)
            writer.writerow(({'videoId': videoId,
                              'targetVideoId': targetVideoId,
                              'publishedAt': publishedAt,
                              'channelId': channelId,
                              'title': title,
                              'description': description
                              }))
