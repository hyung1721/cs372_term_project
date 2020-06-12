# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:44:16 2020

@author: haechan
"""
print("do following : pip install google-api-python-client")

import html
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

api_key = "AIzaSyDnxAFkwrfghu1m9hWnV_mHVbuZRYldMZQ"

youtube = build('youtube','v3',developerKey=api_key)



def get_response(vid, nextPageToken=''):
    if nextPageToken:
        request = youtube.commentThreads().list(
            part = 'snippet',
            videoId = vid,
            pageToken = nextPageToken
            )
    else:
        request = youtube.commentThreads().list(
            part = 'snippet',
            videoId = vid
            )
    response= request.execute()
    return response


def get_all_comments(vid):
    comments_likes=[] # list of tuple (commentString, likeNum)
    nextPageToken = ''
    
    while(True):
        response = get_response(vid, nextPageToken)
        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            likeNum = snippet['likeCount']
            commentString = snippet['textDisplay']
            commentString = BeautifulSoup(commentString, 'html.parser').get_text()
            comments_likes.append((likeNum,commentString))
            
        if 'nextPageToken' not in response.keys():
            break
        else:
            nextPageToken = response['nextPageToken']
            
    return comments_likes         

def get_all_comments_url (url):
    vid = url.split('?')[-1][2:]
    return get_all_comments(vid)