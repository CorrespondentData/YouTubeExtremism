import os as _os
import glob as _glob
import csv as _csv
import webvtt as _webvtt
from .util import is_empty_file as _is_empty_file
import youtube_dl as _youtube_dl


def _get_captions_header():
    return 'videoId', 'transcript'


# TODO(OMeuwese) suppress messages and choose output dir
def get_captions(videos):
    ydl_opts = {
        'writeautomaticsub': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'verbose': False  # doesn't seem to work
    }
    with _youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for video in videos:
            video_url = 'https://www.youtube.com/watch?v={}'.format(video.video_id)
            ydl.download([video_url])


# TODO(OMeuwese) provide folder as argument and extract all vtt_files from given folder
def extract_transcripts(vtt_folder):
    """:param vtt_folder should be location string ending in *.vtt to get all .vtt files like "files/output/*.vtt" """

    video_ids = []
    transcripts = []

    for filename in _glob.glob(vtt_folder):
        ids = _get_ids_from_filename(filename)
        video_ids.append(ids)

        try:
            words = []
            for caption in _webvtt.read(filename):
                words.append(caption.text)
            transcripts.append(words)
        except:
            pass
    return list(zip(video_ids, transcripts))


def write_transcripts(captions_filename, video_id_transcript_list):
    with open(captions_filename, 'a') as csv_file:
        writer = _csv.writer(csv_file, delimiter=',')

        if _is_empty_file(captions_filename):
            writer.writerow(_get_captions_header())

        writer.writerows(video_id_transcript_list)


def _get_ids_from_filename(filename):
    ids = _os.path.basename(filename)
    ids = ids[-18:-7]
    return ids


# TODO (OMeuwese) Unclear how this will be used in getting started
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
