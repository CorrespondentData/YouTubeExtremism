from googleapiclient.discovery import build
import csv


def get_channels(channel_id, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY):
    '''Queries the youtube API and
    gets a json in return'''

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.channels().list(
        part='snippet,contentDetails,topicDetails,statistics,brandingSettings',
        id=channel_id
    ).execute()
    # print('getting channel info for %s' % (channel_id))
    return response


def get_channel_data(response):
    '''Extracts the needed variables
    from the returned json'''

    for channel in response['items']:
        channel_id = channel['id']
        channel_title = channel['snippet']['title']
        channel_description = channel['snippet']['description']
        try:  # many channels do not set a language so we need to catch the exception
            channel_default_language = channel['snippet']['defaultLanguage']
        except:
            channel_default_language = 'not set'
        try:
            channel_country = channel['snippet']['country']
        except:
            channel_country = 'not set'
        channel_viewcount = channel['statistics']['viewCount']
        channel_commentcount = channel['statistics']['commentCount']
        channel_subscribercount = channel['statistics']['subscriberCount']
        channel_videocount = channel['statistics']['videoCount']
        try:
            channel_topic_ids = channel['topicDetails']['topicIds']
        except:
            channel_topic_ids = 'not set'
        try:
            channel_topic_categories = channel['topicDetails']['topicCategories']
        except:
            channel_topic_categories = 'not set'

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


def to_csv(channel_seeds, PATH_TEMP_LEFT):
    # Write the data to a file

    channels = PATH_TEMP_LEFT + 'channels_left.csv'
    count = -1  # if there is an error, it's easier to find the index position from where to continue

    with open(channels, "a") as csvFile:
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

        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        for channel in channel_seeds['Id']:
            try:
                response = get_channels(channel)
                variabelen = get_channel_data(response)
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
                 channel_branding_keywords) = variabelen
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

            print('wrote data for ' + channel_title + ' and index is ' + str(count))
