from googleapiclient.discovery import build


def create_youtube_client(youtube_api_service_name, youtube_api_version, developer_key):
    return build(youtube_api_service_name, youtube_api_version, developerKey=developer_key)
