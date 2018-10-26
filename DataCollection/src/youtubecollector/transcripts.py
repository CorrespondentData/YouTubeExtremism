import os
import glob
import csv
import webvtt
from os.path import isfile


def get_transcripts(vtt_folder):
    """:param vtt_folder should be location string ending in *.vtt to get all .vtt files like "files/output/*.vtt" """

    video_ids = []
    transcripts = []

    for filename in glob.glob(vtt_folder):
        ids = get_ids_from_filename(filename)
        video_ids.append(ids)

        try:
            words = []
            for caption in webvtt.read(filename):
                words.append(caption.text)
            transcripts.append(words)
        except:
            pass

    with open('captions.csv', 'w') as csv_file:
        header = ['videoId', 'transcript']
        writer = csv.writer(csv_file, delimiter=',', fieldnames=header)

        if not isfile('captions.csv'):
            writer.writeheader()
        writer.writerows(zip(video_ids, transcripts))


def get_ids_from_filename(filename):
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
        language = translation['detectedSourceLanguage']

        lang.append(language_result)
        conf.append(confidence_result)
        trans.append(translation_result)

    videos_sample['language_videoDescription'] = lang
    videos_sample['language_videoDescription_confidence'] = conf
    videos_sample['english_videoDescription'] = trans
