# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:28:19 2020

@author: hyung
"""

from youtube_transcript_api import YouTubeTranscriptApi
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
video_id = 'SzOhHutFVKs&t=16s'

'''
    time -> //span[@class="ytp-time-duration"] 으로 찾고 병합해야 할듯(나중에)
'''



script_data = YouTubeTranscriptApi.get_transcript(video_id)

full_time = script_data[-1]['start'] + script_data[-1]['duration']
num_interval = 15
interval_time = full_time/num_interval
keyword_list = [list() for i in range(num_interval)]
common_words = stopwords.words('english')

for script in script_data:
    start = script['start']
    duration = script['duration']
    text = script['text']
    
    tagged_script = nltk.pos_tag(text.split(), tagset = "universal")
    #tokenized_script = word_tokenize(text)
   # print(tagged_script)
    n = ["NOUN"]
    keyword_tokenized_script = [word[0].lower() for word in tagged_script if not word[0].lower() in common_words and word[1].lower().isalpha()]
    
    start_index = -1
    end_index   = -1
    for i in range(num_interval):
        if(start >= i * interval_time and start < (i+1) * interval_time):
            start_index = i
        if(start + duration >= i * interval_time and start + duration < (i+1) * interval_time):
            end_index = i
    
    for i in range(start_index, end_index + 1):
        keyword_list[i] += keyword_tokenized_script

#for i in range(len(keyword_list)):
#    keyword_list[i] = list(keyword_list[i])
keyword_dict = dict()
for i in range(len(keyword_list)):
    keyword_dict[i]=keyword_list[i]

#print(keyword_dict)
comments = ["Honestly, well done to Adam for editing this so well. It dosen’t even seem like theyre not sitting next to each other", 
            "Steven didn't even say 'three drastically different pricepoints'. The world is in trouble",
            "This is the most Adam has ever spoken",
            '''Y'all didn't do takeout fact! So I took it upon myself to do it😊
            Fact 1: 1 in 4 people in the US eat some type of takeout food everyday according to the department of agriculture 
            Fact 2 : according to National restaurant news chicken wings ranked as the most ordered fast food in the US 
            you're welcome😂''',
            "im not crying. I missed y’all! Worth It has always been my favorite series and i was so worried y’all wouldn’t be able to do the vids you wanted. I’m glad y’all figured it out and I appreciate the editing to make it so as if you’re all still together. I love you guys and please continue to stay safe. Your health is ‘Worth It’."
            ]

for comment in comments:
    tokenized_comment = word_tokenize(comment)
    a = []
    for i in range(num_interval):
        a.append([0.0,[]])
        #a.append(0.0)
    for i in tokenized_comment:
        for j in range(len(keyword_list)):
            if i.lower() in keyword_list[j]:
                
                a[j][0]+=1/len(tokenized_comment) * 100
                a[j][0]=round(a[j][0], 2)
                a[j][1].append(i)
                '''
                a[j]+=1/len(tokenized_comment) * 100 * keyword_list[j].count(i.lower())
                a[j]=round(a[j], 2)
                '''
                
    print(a)