import os
import glob
import csv
import webvtt


def get_transcripts():
    videoId = []
    words = []
    transcript = []

    for filename in glob.glob('~/Documents/projecten/extremisme/youtube/data/temp/bubble/*.vtt'):
        ids = os.path.basename(filename)
        ids = ids[-18:-7]
        videoId.append(ids)
        try:
            for caption in webvtt.read(filename):
                words.append(caption.text)
            transcript.append(words)
        except:
            pass
        words = []

    file_exists = os.path.isfile('captions.csv')

    with open('captions.csv', 'w') as csvfile:
        header = ['videoId', 'transcript']
        writer = csv.writer(csvfile, delimiter=',', fieldnames=header)

        if not file_exists:
            writer.writeheader()
        writer.writerows(zip(videoId, transcript))


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