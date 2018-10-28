import os
import glob
import csv
import webvtt
from .util import is_empty_file as _is_empty_file


def _get_captions_header():
    return 'videoId', 'transcript'


def get_transcripts(vtt_folder):
    """:param vtt_folder should be location string ending in *.vtt to get all .vtt files like "files/output/*.vtt"
       :param captions_filename is the name of the csv file where the output should be written to
    """

    video_ids = []
    transcripts = []

    for filename in glob.glob(vtt_folder):
        ids = _get_ids_from_filename(filename)
        video_ids.append(ids)

        try:
            words = []
            for caption in webvtt.read(filename):
                words.append(caption.text)
            transcripts.append(words)
        except:
            pass
    return list(zip(video_ids, transcripts))


def write_transcripts(captions_filename, video_id_transcript_list):
    with open(captions_filename, 'a') as csv_file:

        writer = csv.writer(csv_file, delimiter=',', fieldnames=_get_captions_header())

        if _is_empty_file(captions_filename):
            writer.writeheader()
        writer.writerows(video_id_transcript_list)


def _get_ids_from_filename(filename):
    ids = os.path.basename(filename)
    ids = ids[-18:-7]
    return ids


def get_language_and_translations(translate_client, videos_sample, lang):
    trans = []
    conf = []
    target = 'en'

    for text in videos_sample['videoDescription']:
        translation = translate_client(text, target_language=target)
        language = translate_client.detect_language(text)

        language_result = language['language']
        confidence_result = language['confidence']
        translation_result = translation['translatedText']

        lang.append(language_result)
        conf.append(confidence_result)
        trans.append(translation_result)

    videos_sample['language_videoDescription'] = lang
    videos_sample['language_videoDescription_confidence'] = conf
    videos_sample['english_videoDescription'] = trans
