from unittest import TestCase

from comments import convert_to_comments, comment
from utils_for_test import read_json_from_file


class CommentTest(TestCase):

    def test_get_full_comment(self):
        response = read_json_from_file("comment_full.json")
        actual = convert_to_comments(response)

        expected = [
            comment(video_id='the video id', comment_id='The comment id that is used',
                    author_display_name='Author name',
                    author_channel_url='http://www.youtube.com/channel/someone',
                    author_channel_id='someone',
                    comment_text='The text that is displayed',
                    comment_like_count=4,
                    comment_dislike_count=2,
                    comment_time='2017-11-02T19:25:12.000Z',
                    reply_count=0)
        ]

        self.assertEqual(actual, expected)

    def test_get_minimal_comment(self):
        raise NotImplementedError()

    def test_get_comments_with_replies(self):
        raise NotImplementedError()
