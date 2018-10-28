import pandas as pd

def read_comments(comments_file):
    '''
    Read comments file into Pandas DataFrame

    Keyword parameters:
    comments_file - filename of comments csv file
    '''
    comments_df = pd.read_csv(comments_file, encoding = 'utf8', header = 0)
    comments_df = comments_df[comments_df['video_id'] != 'video_id']

    comments_df['comment_time'] = pd.to_datetime(comments_df['comment_time'])

    return comments_df

def add_video_metadata(comments_df, video_file, keep_vars = None):
    '''
    Add video metadata to the comments dataset

    Keyword parameters:
    comments_df - DataFrame with comments, construct using comment_lib.read_comments
    video_file - filename of video metadata csv file
    keep_vars - list of variables to keep (a selection of video variables). If not supplied, all will be matched.
        video_id is always kept to match, does not necessarily need to be specified here.
    '''
    video_df = pd.read_csv(video_file, encoding = 'utf8', header = 0)
    video_df = video_df[video_df['video_id'] != 'video_id']

    video_df['video_published'] = pd.to_datetime(video_df['video_published'])

    if keep_vars:
        if 'video_id' not in keep_vars:
            keep_vars.append('video_id')
        video_df = video_df[keep_vars]

    return comments_df.merge(video_df, how = 'left', on = 'video_id')
