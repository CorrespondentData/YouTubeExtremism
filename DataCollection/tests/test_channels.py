from unittest import TestCase

import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import HttpMockSequence

from channels import get_channels, channel
from utils_for_test import get_content_from_file


class ChannelTest(TestCase):

    def test_get_full_channel(self):
        expected = [
            channel(channel_id='Some_ID', channel_title='The test channel',
                    channel_description='The Official YouTube Channel for testing',
                    channel_default_language='en', channel_country='US',
                    channel_uploads='UU_8WUrPbi8clO6sWt_FDvuA', channel_viewcount='2640735',
                    channel_commentcount='0', channel_subscribercount='9779', channel_videocount='258',
                    channel_topic_ids=['topic1', 'topic2', 'topic3'],
                    channel_topic_categories=['https://en.wikipedia.org/wiki/Society',
                                              'https://en.wikipedia.org/wiki/Politics'],
                    channel_branding_keywords='"Testing is fun", "More Testing"')
        ]
        service_json = get_content_from_file("youtube_service.json")
        full_channel_response = get_content_from_file("full_channel_response.json")
        url = HttpMockSequence([
            ({'status': '200'}, service_json),
            ({'status': '200'}, full_channel_response)
        ])
        channel_seed = pd.DataFrame([{"channel_id": "Some_ID"}])

        client = build("youtube", "v3", http=url, developerKey="key")
        actual = get_channels(channel_seed, client)

        self.assertEqual(expected, actual)

    def test_get_minimal_channel(self):
        expected = [
            channel(channel_id='Some_ID', channel_title='The test channel',
                    channel_description='The Official YouTube Channel for testing',
                    channel_default_language='not set', channel_country='not set',
                    channel_uploads='', channel_viewcount='2640735',
                    channel_commentcount='0', channel_subscribercount='9779', channel_videocount='258',
                    channel_topic_ids="not set",
                    channel_topic_categories="not set",
                    channel_branding_keywords="not set")
        ]
        service_json = get_content_from_file("youtube_service.json")
        minimal_channel_response = get_content_from_file("nullable_fields_channel_response.json")
        url = HttpMockSequence([
            ({'status': '200'}, service_json),
            ({'status': '200'}, minimal_channel_response)
        ])
        channel_seed = pd.DataFrame([{"channel_id": "Some_ID"}])

        client = build("youtube", "v3", http=url, developerKey="key")
        actual = get_channels(channel_seed, client)

        self.assertEqual(expected, actual)
