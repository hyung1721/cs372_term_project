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
        "https://www.youtube.com/watch?v=nr56NIvkNZk", "https://www.youtube.com/watch?v=jtVKXoNA-K0",
        'https://www.youtube.com/watch?v=9bZkp7q19f0', 'https://www.youtube.com/watch?v=W85F-UmnbF4',
        'https://www.youtube.com/watch?v=Yr14Io0wsiU', 'https://www.youtube.com/watch?v=0mJiPcKybzU',
        'https://www.youtube.com/watch?v=szdbKz5CyhA', 'https://www.youtube.com/watch?v=Y_ZS_EfoYpA',
        'https://www.youtube.com/watch?v=yPWAfjvVtEM', 'https://www.youtube.com/watch?v=2Qa9YDgtcaM',
        'https://www.youtube.com/watch?v=WN-IW6wOdnI', 'https://www.youtube.com/watch?v=vWgjqMyP5kk',
        'https://www.youtube.com/watch?v=27Dx6ztJ8jw', 'https://www.youtube.com/watch?v=PzVqQWxBXQE',
        'https://www.youtube.com/watch?v=27Dx6ztJ8jw', 'https://www.youtube.com/watch?v=HFsKxbrZKNQ',
        'https://www.youtube.com/watch?v=cG_NB2cQnGU', 'https://www.youtube.com/watch?v=XDXrP9HET2A',
        'https://www.youtube.com/watch?v=N-sLp2Ri76s',]

def probability_factor_script_interval_relation(url, comment_list):
    video_id = url.split("=")[-1]
    script_data = YouTubeTranscriptApi.get_transcript(video_id)
    
    
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
            weights_comment.append(0.0)
        for target_word in tokenized_comment:
            for j in range(num_interval):
                if target_word.lower() in new_keyword_list[j]:
                    portion = 1
                    if(comment_list['like_num'].iloc[index_comment] >= 100):
                        sum_weight_list_with_liked_comment[j] += portion
                    else:
                        sum_weight_list_with_non_liked_comment[j] += portion
    count_all_comment = count_liked_comment + count_non_liked_comment
    sum_weight_list_with_all_comment = []
    for i in range(num_interval):
        liked_portion  = sum_weight_list_with_liked_comment[i]
        non_liked_portion = sum_weight_list_with_non_liked_comment[i]
        sum_weight_list_with_all_comment.append((liked_portion+non_liked_portion)/(count_all_comment))
    
    
    sum_weight_list_with_liked_comment = [portion/count_liked_comment for portion in sum_weight_list_with_liked_comment]
    sum_weight_list_with_non_liked_comment = [portion/count_non_liked_comment for portion in sum_weight_list_with_non_liked_comment]
    
    #print(comment_list_with_weight[:20])
    #print("------------------------")
    #print(sum_weight_list_with_all_comment)
    #print(sum_weight_list_with_liked_comment)
    #print(sum_weight_list_with_non_liked_comment)
    return sum_weight_list_with_all_comment, sum_weight_list_with_liked_comment, sum_weight_list_with_non_liked_comment


def probability_factor_script_interval_relation_comment(new_keyword_list, comment): 
    
    num_interval = 10

    tokenized_comment = word_tokenize(comment)
    
    weights_comment = []
    for i in range(num_interval):
        weights_comment.append(0.0)
    for target_word in tokenized_comment:
        for j in range(num_interval):
            if target_word.lower() in new_keyword_list[j]:
                portion = 1
                weights_comment[j]+=portion
    weights_comment = [round(x, 2) for x in weights_comment]
    
    return weights_comment

# execution
    

comment_data_list = load_comment_data_test()
all_comment_total = [0.0] * 10
all_liked_comment_total = [0.0] * 10
all_non_liked_comment_total = [0.0] * 10

count = 0

for index_data in range(len(comment_data_list)):
    current_url = urls[index_data]
    current_comment_data = comment_data_list[index_data]
    try:
        all_comment, liked_comment, non_liked_comment = probability_factor_script_interval_relation(current_url, current_comment_data)
        
        if(sum(all_comment) < 0.5):
            continue
        
        count += 1
    except:
        continue
    
    for index in range(10):
        all_comment_total[index] += all_comment[index]
        all_liked_comment_total[index] += liked_comment[index]
        all_non_liked_comment_total[index] += non_liked_comment[index]

average_all_comment = [ str(round(x/count, 3)) for x in all_comment_total]
average_liked_comment = [ str(round(x/count, 3)) for x in all_liked_comment_total]
average_non_liked_comment = [ str(round(x/count, 3)) for x in all_non_liked_comment_total]

# print result
print('-----------------------------------------------------------------------------')
print("|                                                                           |")
print("|   Average number of video context references per comment by interval      |")
print("|                                                                           |")
print("|   All comments:                                                           |")
print("|     "+ ", ".join(average_all_comment) + "  |")
print("|                                                                           |")
print("|   Liked comments:                                                         |")
print("|     "+ ", ".join(average_liked_comment) + "   |")
print("|                                                                           |")
print("|   Non-liked comments:                                                     |")
print("|     "+ ", ".join(average_non_liked_comment) + "  |")
print("|                                                                           |")
print('-----------------------------------------------------------------------------')
