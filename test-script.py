# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:28:19 2020

@author: hyung
"""

from youtube_transcript_api import YouTubeTranscriptApi
from nltk.corpus import stopwords
from nltk import word_tokenize

video_id = 'SzOhHutFVKs&t=16s'

'''
    time -> //span[@class="ytp-time-duration"] 으로 찾고 병합해야 할듯(나중에)
'''

full_time = 923
num_interval = 15
interval_time = full_time/num_interval

script_data = YouTubeTranscriptApi.get_transcript(video_id)

keyword_list = [set() for i in range(num_interval)]
common_words = stopwords.words('english')

for script in script_data:
    start = script['start']
    duration = script['duration']
    text = script['text']
    
    tokenized_script = word_tokenize(text)
    keyword_tokenized_script = set([word.lower() for word in tokenized_script if not word.lower() in common_words])
    
    start_index = -1
    end_index   = -1
    for i in range(num_interval):
        if(start >= i * interval_time and start < (i+1) * interval_time):
            start_index = i
        if(start + duration >= i * interval_time and start + duration < (i+1) * interval_time):
            end_index = i
    
    for i in range(start_index, end_index + 1):
        keyword_list[i] = keyword_list[i].union(keyword_tokenized_script)

for i in range(len(keyword_list)):
    keyword_list[i] = list(keyword_list[i])

print(keyword_list)