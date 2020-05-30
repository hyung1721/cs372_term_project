# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:28:19 2020

@author: hyung
"""

from crawl import load_comment_data_test
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
import pandas as pd
from nltk import FreqDist

video_id = 'pE49WK-oNjU'
script_data = YouTubeTranscriptApi.get_transcript(video_id)
comment_list = load_comment_data_test()[2]

full_time = script_data[-1]['start'] + script_data[-1]['duration']
num_interval = 10
interval_time = full_time/num_interval
keyword_list = [list() for i in range(num_interval)]
common_words = stopwords.words('english')
all_words = []

for script in script_data:
    start = script['start']
    duration = script['duration']
    text = script['text']
    
    tagged_script = nltk.pos_tag(text.split(), tagset = "universal")
    
    #tokenized_script = word_tokenize(text)
    #print(tagged_script)
    n = ["NOUN"]
    keyword_tokenized_script = [word[0].lower() for word in tagged_script 
                                if not (word[0].lower() in common_words) 
                                and word[0].lower().isalpha()
                                and word[1] == 'NOUN']
    all_words += keyword_tokenized_script
    start_index = -1
    end_index   = -1
    for i in range(num_interval):
        if(start >= i * interval_time and start < (i+1) * interval_time):
            start_index = i
        if(start + duration >= i * interval_time and start + duration < (i+1) * interval_time):
            end_index = i
    
    for i in range(start_index, end_index + 1):
        keyword_list[i] += keyword_tokenized_script

freqdist_all_words = FreqDist(all_words)
most_common_keyword_list = [word[0] for word in freqdist_all_words.most_common(len(freqdist_all_words)//20)]

new_keyword_list = [set() for i in range(num_interval)]

for interval in range(len(keyword_list)):
    for word in keyword_list[interval]:
        if(keyword_list[interval].count(word) >= 2):
            new_keyword_list[interval].add(word)

keyword_dict = dict()
for i in range(len(new_keyword_list)):
    keyword_dict[i]=list(new_keyword_list[i])

#print(keyword_dict)

comment_list_with_weight = []
sum_weight_list_with_liked_comment = [0.0] * num_interval
sum_weight_list_with_non_liked_comment = [0.0] * num_interval

count_liked_comment = 0
count_non_liked_comment = 0
for index_comment in range(len(comment_list['content'])):
    tokenized_comment = word_tokenize(comment_list['content'].iloc[index_comment])
    
    if(comment_list['like_num'].iloc[index_comment] >= 100):
        count_liked_comment += 1
    else:
        count_non_liked_comment += 1
    
    weights_comment = []
    for i in range(num_interval):
        #weights_comment.append([0.0,[]])
        weights_comment.append(0.0)
    for target_word in tokenized_comment:
        for j in range(num_interval):
            if target_word.lower() in new_keyword_list[j]:
                '''
                a[j][0]+=1/len(tokenized_comment) * 100
                a[j][0]=round(a[j][0], 2)
                a[j][1].append(i)
                '''
                #'''
                portion = 1 #* new_keyword_list[j].count(target_word.lower())
                weights_comment[j] += portion
                #weights_comment[j]=round(weights_comment[j], 2)
                #'''
                if(comment_list['like_num'].iloc[index_comment] >= 100):
                    sum_weight_list_with_liked_comment[j] += portion
                    #sum_weight_list_with_liked_comment[j] = round(sum_weight_list_with_liked_comment[j], 2)
                else:
                    sum_weight_list_with_non_liked_comment[j] += portion
                    #sum_weight_list_with_non_liked_comment[j] = round(sum_weight_list_with_non_liked_comment[j], 2)
    comment_list_with_weight.append(weights_comment)

sum_weight_list_with_liked_comment = [round(portion/count_liked_comment, 2) for portion in sum_weight_list_with_liked_comment]
sum_weight_list_with_non_liked_comment = [round(portion/count_non_liked_comment, 2) for portion in sum_weight_list_with_non_liked_comment]

#print(comment_list_with_weight[:20])
print(sum_weight_list_with_liked_comment)
print(sum_weight_list_with_non_liked_comment)