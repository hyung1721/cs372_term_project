# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:44:16 2020

@author: haechan
"""
print("do following : pip install google-api-python-client")

import html
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import nltk

from crawl import after_tokenize
from pickle import dump
from pickle import load


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


## retunrs list of tuple (commneString:string, likeNum:int)
def get_all_comments(vid):
    comments_likes=[] # list of tuple (commentString, likeNum)
    nextPageToken = ''
    cnt = 0;
    
    while(cnt<50): # 1000 comments per video
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
        cnt+=1
            
    return comments_likes         

def get_all_comments_url (url):
    vid = url.split('?')[-1][2:]
    return get_all_comments(vid)


## return tokenized / liked_tokenized
def tokenize_comments_singlevid (comments_likes):
    tokenized_comment_list=[]
    
    comments_likes = sorted(comments_likes, key= lambda x:x[0], reverse=True)
    for like, comment in comments_likes:
        tokens = nltk.word_tokenize(comment)
        tokens = after_tokenize(tokens)
        tokenized_comment_list.append(tokens)
    
    liked_num = int(len(comments_likes)*0.01)
    
    liked_tokenized_comment_list = tokenized_comment_list[:liked_num]
   
    return tokenized_comment_list, liked_tokenized_comment_list



###### Now for multiple videos
    

def get_and_tokenize_singlevid (url):
    return tokenize_comments_singlevid(get_all_comments_url(url)) 
    

def get_and_tokenize_multiplevids (urls):

    comments_multiplevids = []
    liked_comments_multiplevids = []

    for url in urls:
        comments_singlevid, liked_comments_singlevid = get_and_tokenize_singlevid(url)
        comments_multiplevids += comments_singlevid
        liked_comments_multiplevids += liked_comments_singlevid
        
    return comments_multiplevids, liked_comments_multiplevids 


def save_comments(isTrain=True):
    
    
    if isTrain:
        urls = ['https://www.youtube.com/watch?v=9bZkp7q19f0', 'https://www.youtube.com/watch?v=W85F-UmnbF4'
,'https://www.youtube.com/watch?v=Yr14Io0wsiU', 'https://www.youtube.com/watch?v=0mJiPcKybzU', 'https://www.youtube.com/watch?v=szdbKz5CyhA'
,'https://www.youtube.com/watch?v=Y_ZS_EfoYpA', 'https://www.youtube.com/watch?v=yPWAfjvVtEM', 'https://www.youtube.com/watch?v=2Qa9YDgtcaM',
'https://www.youtube.com/watch?v=WN-IW6wOdnI', 'https://www.youtube.com/watch?v=vWgjqMyP5kk', 'https://www.youtube.com/watch?v=27Dx6ztJ8jw',
'https://www.youtube.com/watch?v=PzVqQWxBXQE',  'https://www.youtube.com/watch?v=27Dx6ztJ8jw', 'https://www.youtube.com/watch?v=HFsKxbrZKNQ',
'https://www.youtube.com/watch?v=cG_NB2cQnGU', 'https://www.youtube.com/watch?v=XDXrP9HET2A', 'https://www.youtube.com/watch?v=N-sLp2Ri76s']
        
    else:
        urls = ["https://www.youtube.com/watch?v=AGL7ealeXpw", "https://www.youtube.com/watch?v=quACziGJqQM", 
        "https://www.youtube.com/watch?v=pE49WK-oNjU", "https://www.youtube.com/watch?v=H2dXou6v8gA",
        "https://www.youtube.com/watch?v=AZyxG2FpgpQ", "https://www.youtube.com/watch?v=M1FxrfCjRbI",
        "https://www.youtube.com/watch?v=Mm8RfyKqZ3s", "https://www.youtube.com/watch?v=lhfAXsEfGKw",
        "https://www.youtube.com/watch?v=Tji5DtyLbNU", "https://www.youtube.com/watch?v=pU4iFVR3RCg",
        "https://www.youtube.com/watch?v=FatzlG2DNdY", "https://www.youtube.com/watch?v=mcwlUdprz9E",
        "https://www.youtube.com/watch?v=C-DfE1GTRx0", "https://www.youtube.com/watch?v=he-VxfjhZt0",
        "https://www.youtube.com/watch?v=s8wZOEuPX38", "https://www.youtube.com/watch?v=azkVr0VUSTA",
        "https://www.youtube.com/watch?v=LV_xfEC4qhw", "https://www.youtube.com/watch?v=QAVpbnpX7ww",
        "https://www.youtube.com/watch?v=wfGAktuU93s", "https://www.youtube.com/watch?v=6HjpvJG3-Hg",
        "https://www.youtube.com/watch?v=GCp2gZ-BMIw", "https://www.youtube.com/watch?v=_FTimJqrz64",
        "https://www.youtube.com/watch?v=GErG9femMQk", "https://www.youtube.com/watch?v=0JvQOJl3Eds",
        "https://www.youtube.com/watch?v=NAmOdxZKWjY", "https://www.youtube.com/watch?v=eIZkVaM-0K8",
        "https://www.youtube.com/watch?v=dworC_RqzHw", "https://www.youtube.com/watch?v=KfKKfEm3H6M",
        "https://www.youtube.com/watch?v=7qyKhP4lzsY", "https://www.youtube.com/watch?v=zFDwECtUjRg",
        "https://www.youtube.com/watch?v=dQM-h3M4BZc", "https://www.youtube.com/watch?v=M8-49EaVE00",
        "https://www.youtube.com/watch?v=5Hg_QSIJm8I", "https://www.youtube.com/watch?v=6ptc4wBo1uY",
        "https://www.youtube.com/watch?v=jAbeBXAYztk", "https://www.youtube.com/watch?v=Q2ce9VSNsjE",
        "https://www.youtube.com/watch?v=TgOu00Mf3kI", "https://www.youtube.com/watch?v=KPYp3lOOOrg",
        "https://www.youtube.com/watch?v=wYBEbNbirkA", "https://www.youtube.com/watch?v=47Tm5U6zif0",
        "https://www.youtube.com/watch?v=hoYo4tFWotg", "https://www.youtube.com/watch?v=NDqq8wK6K7s",
        "https://www.youtube.com/watch?v=bCrYGsWoppQ", "https://www.youtube.com/watch?v=3yjcqsNNa24",
        "https://www.youtube.com/watch?v=uXiJBkWZ2E8", "https://www.youtube.com/watch?v=Obgg5BNqJWg",
        "https://www.youtube.com/watch?v=_T_0FYHn0I0", "https://www.youtube.com/watch?v=gSxZMYjDBZE",
        "https://www.youtube.com/watch?v=i7gxGEhU-Wk", "https://www.youtube.com/watch?v=u8eIJYt68IE",
        "https://www.youtube.com/watch?v=lwp429eqER4", "https://www.youtube.com/watch?v=Chb_Iyx9ODQ",
        "https://www.youtube.com/watch?v=ewLpXw6uN28", "https://www.youtube.com/watch?v=eZUKSxE2UZg",
        "https://www.youtube.com/watch?v=45Cs6mZsGok", "https://www.youtube.com/watch?v=1MhcOlpalbw",
        "https://www.youtube.com/watch?v=2QNM3lnv7v0", "https://www.youtube.com/watch?v=HPlcL8MpAzk",
        "https://www.youtube.com/watch?v=nr56NIvkNZk", "https://www.youtube.com/watch?v=jtVKXoNA-K0"]
    
   
    urls=urls
    comments , liked_comments = get_and_tokenize_multiplevids(urls)
    save_tup = (comments, liked_comments)
    
    if isTrain:
        output = open('youtubeapi_train_data.pkl', 'wb')
    else:
        output = open('youtubeapi_test_data.pkl', 'wb')
    dump(save_tup, output, -1)
    output.close()
    
    
def load_comments(isTrain):
    comments= []
    liked_comments = []
    
    if isTrain:
        input = open('youtubeapi_train_data.pkl', 'rb')
    else:
        input = open('youtubeapi_test_data.pkl', 'rb')
    
   # load(input)
    
    while True:
        try:
            (load_comments, load_liked_comments) = load(input)
        except:
            break
        
        comments +=  load_comments
        liked_comments += load_liked_comments
        
    input.close()
    
    return comments, liked_comments 