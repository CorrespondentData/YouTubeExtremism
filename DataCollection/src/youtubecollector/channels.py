import csv
import os


def get_channels(channel_id, youtube_client):
    """Queries the youtube API and gets a json in return"""

    return youtube_client.channels().list(
        part='snippet,contentDetails,topicDetails,statistics,brandingSettings',
        id=channel_id
    ).execute()


def get_channel_data(response):
    """Extracts the needed variables from the returned json"""

    for channel in response['items']:
        channel_id = channel['id']
        channel_title = channel['snippet']['title']
        channel_description = channel['snippet']['description']
        channel_default_language = channel['snippet'].get('defaultLanguage', 'not set')
        channel_country = channel['snippet'].get('country', 'not set')
        channel_viewcount = channel['statistics']['viewCount']
        channel_commentcount = channel['statistics']['commentCount']
        channel_subscribercount = channel['statistics']['subscriberCount']
        channel_videocount = channel['statistics']['videoCount']
        channel_topic_ids = channel['topicDetails'].get('topicIds', 'not set')
        channel_topic_categories = channel['topicDetails'].get('topicCategories', 'not set')

        try:
            channel_branding_keywords = channel['brandingSettings']['channel']['keywords']
        except:
            channel_branding_keywords = 'not set'

        return (channel_id,
                channel_title,
                channel_description,
                channel_default_language,
                channel_country,
                channel_viewcount,
                channel_commentcount,
                channel_subscribercount,
                channel_videocount,
                channel_topic_ids,
                channel_topic_categories,
                channel_branding_keywords)


def to_csv(channel_seeds, youtube_client, path_temp_left):
    # Write the data to a file

    channels = os.path.join(path_temp_left, 'channels_left.csv')
    count = -1  # if there is an error, it's easier to find the index position from where to continue

    fieldnames = ['channel_id',
                  'channel_title',
                  'channel_description',
                  'channel_default_language',
                  'channel_country',
                  'channel_viewcount',
                  'channel_commentcount',
                  'channel_subscribercount',
                  'channel_videocount',
                  'channel_topic_ids',
                  'channel_topic_categories',
                  'channel_branding_keywords'
                  ]

    with open(channels, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for channel in channel_seeds['Id']:
            try:
                response = get_channels(channel, youtube_client)
                variables = get_channel_data(response)
                (channel_id,
                 channel_title,
                 channel_description,
                 channel_default_language,
                 channel_country,
                 channel_viewcount,
                 channel_commentcount,
                 channel_subscribercount,
                 channel_videocount,
                 channel_topic_ids,
                 channel_topic_categories,
                 channel_branding_keywords) = variables
            except:
                continue

            writer.writerow({'channel_id': channel_id,
                             'channel_title': channel_title,
                             'channel_description': channel_description,
                             'channel_default_language': channel_default_language,
                             'channel_country': channel_country,
                             'channel_viewcount': channel_viewcount,
                             'channel_commentcount': channel_commentcount,
                             'channel_subscribercount': channel_subscribercount,
                             'channel_videocount': channel_videocount,
                             'channel_topic_ids': channel_topic_ids,
                             'channel_topic_categories': channel_topic_categories,
                             'channel_branding_keywords': channel_branding_keywords
                             })
            count += 1

            print(f'wrote data for {channel_title} and index is  {count}')
