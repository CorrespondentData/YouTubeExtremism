import pandas as pd
import re

COMMENT_TEXT_FIELDS = ['video_id', 'comment_id', 'author_display_name',
       'author_channel_url', 'author_channel_id', 'comment_text']
VIDEO_TEXT_FIELDS = ['channel_id', 'video_title', 'video_description',
       'video_channel_title', 'video_default_language', 'video_duration']

def read_comments(comments_file, convert_string = True):
    '''
    Read comments file into Pandas DataFrame.

    Keyword parameters:
    comments_file - filename of comments csv file
    convert_string - boolean. Force conversion of string fields to strings (e.g. comments containing only numbers). 
        Defaults to True
    '''
    comments_df = pd.read_csv(comments_file, encoding = 'utf8', header = 0)
    comments_df = comments_df[comments_df['video_id'] != 'video_id']

    comments_df['comment_time'] = pd.to_datetime(comments_df['comment_time'])

    if convert_string:
        for field in COMMENT_TEXT_FIELDS:
            comments_df[field] = comments_df[field].apply(str)

    return comments_df

def add_video_metadata(comments_df, video_file, keep_vars = None, convert_string = True):
    '''
    Add video metadata to the comments dataset

    Keyword parameters:
    comments_df - DataFrame with comments, construct using comment_lib.read_comments
    video_file - filename of video metadata csv file
    keep_vars - list of variables to keep (a selection of video variables). If not supplied, all will be matched.
        video_id is always kept to match, does not necessarily need to be specified here.
    convert_string - boolean. Force conversion of string fields to strings (e.g. comments containing only numbers). 
        Defaults to True
    '''
    video_df = pd.read_csv(video_file, encoding = 'utf8', header = 0)
    video_df = video_df[video_df['video_id'] != 'video_id']

    if convert_string:
        for field in VIDEO_TEXT_FIELDS:
            video_df[field] = video_df[field].apply(str)

    video_df['video_published'] = pd.to_datetime(video_df['video_published'])
    
    #Set duration to integer (number of seconds)
    video_df['video_duration'] = video_df['video_duration'].apply(video_duration_to_int)

    if keep_vars:
        if 'video_id' not in keep_vars:
            keep_vars.append('video_id')
        video_df = video_df[keep_vars]

    return comments_df.merge(video_df, how = 'left', on = 'video_id')

def video_duration_minutes(duration_string):
    ''' Get the number of minutes from a youtube video duration string'''
    minute_count = re.search('(?<=PT)[0-9]+(?=M)', duration_string)
    if minute_count:
        return int(minute_count[0])
    else:
        return 0

def video_duration_seconds(duration_string):
    ''' Get the number of seconds from a youtube video duration string'''
    second_count = re.search('(?<=M)[0-9]+(?=S)', duration_string)
    if second_count:
        return int(second_count[0])
    else:
        return 0

def video_duration_to_int(duration_string):
    '''Convert a youtube video duration string to the total number of seconds'''
    return 60*video_duration_minutes(duration_string) + video_duration_seconds(duration_string)