from unittest import TestCase

from channels import _convert_to_channel, channel
from utils_for_test import read_json_from_file


class ChannelTest(TestCase):

    def test_convert_to_channel_entity(self):
        response = read_json_from_file("full_channel_response.json")

        expected = channel(channel_id='Some_ID', channel_title='The test channel',
                           channel_description='The Official YouTube Channel for testing',
                           channel_default_language='en', channel_country='US',
                           channel_uploads='UU_8WUrPbi8clO6sWt_FDvuA', channel_viewcount='2640735',
                           channel_commentcount='0', channel_subscribercount='9779', channel_videocount='258',
                           channel_topic_ids=['topic1', 'topic2', 'topic3'],
                           channel_topic_categories=['https://en.wikipedia.org/wiki/Society',
                                                     'https://en.wikipedia.org/wiki/Politics'],
                           channel_branding_keywords='"Testing is fun", "More Testing"')

        actual = _convert_to_channel(response)
        self.assertEqual(expected, actual)

    def test_convert_minimal_response(self):
        response = read_json_from_file("nullable_fields_channel_response.json")

        expected = channel(channel_id='Some_ID', channel_title='The test channel',
                           channel_description='The Official YouTube Channel for testing',
                           channel_default_language='not set', channel_country='not set',
                           channel_uploads='', channel_viewcount='2640735',
                           channel_commentcount='0', channel_subscribercount='9779', channel_videocount='258',
                           channel_topic_ids="not set",
                           channel_topic_categories="not set",
                           channel_branding_keywords="not set")

        actual = _convert_to_channel(response)
        self.assertEqual(expected, actual)
