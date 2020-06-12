# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:44:24 2020

@author: KTY
"""


from find_script_interval_relation import *
from crawl import *
import pandas as pd 
from nltk import NaiveBayesClassifier
import random
from nltk.metrics import accuracy

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

def factor_features(script_data, comment):
    featureset = {}
    script_relation = probability_factor_script_interval_relation_comment(script_data, comment)
    global a
    featureset['related']=sum(script_relation)>sum(a)
    for i in range(len(script_relation)):
        featureset[str(i)] = script_relation[i]>a[i]
    return featureset

class EvaluateFactorClass():
    def __init__(self, train_comment_list, url):
        train_set = []
        video_id = url.split("=")[-1]
        script_data = YouTubeTranscriptApi.get_transcript(video_id)
        self.url = url
        self.script_data = script_data
        keyword_list = self.make_keyword_list()
        
        for comment_with_tag in train_comment_list:
            comment = comment_with_tag[0]
            tag = comment_with_tag[1] # 'liked' and 'non-liked', or just simply 1 and 0
            
            featureset = factor_features(keyword_list, comment) # factor_feature() may need more input arguments  
            train_set.append((featureset, tag))
        
        self.classifier = NaiveBayesClassifier.train(train_set)
    
    def tag(self, test_comment_list):
        # test -> list of comments
        result_list = []
        
        for comment in test_comment_list:
            featureset = factor_features(self.script_data, comment)
            tag = self.classifier.classify(featureset)
            result_list.append((comment, tag))
        return result_list
    
    def make_keyword_list(self):
        script_data = self.script_data
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
        return new_keyword_list
def tag_comment(comments, comment_url):
    comments_with_tag = []
    comments.sort_values(by = ['like_num'],axis = 0, inplace = True, ascending = False)
    cnt = 0
    for index, comment in comments.iterrows():
        if(cnt<int((len(comments)*0.05))):
            comments_with_tag.append((comment['content'], 1))
        else:
            comments_with_tag.append((comment['content'], 0))
        cnt+=1
    return comments_with_tag

def untag(tagged_sentences):
    return [sentence for (sentence, tag) in tagged_sentences]

comment = load_comment_data_test()[2]
url =  urls[2]
train_comments_with_tag = tag_comment(comment, url)
a,b,c = probability_factor_script_interval_relation(url, comment)
like_cnt = int((len(train_comments_with_tag)*0.05))
train_end = int(like_cnt+(len(train_comments_with_tag)-like_cnt)*0.8)
#test_comment_with_tag =tag_comment(load_comment_data_test()[2], urls[2])
#untagged_test_comments = untag(test_comment_with_tag)

classifier = EvaluateFactorClass(train_comments_with_tag[:int(like_cnt*0.8)]
                                 +train_comments_with_tag[like_cnt:train_end]
                                 , url)

classify_result =classifier.tag(untag(train_comments_with_tag[int(like_cnt*0.8):like_cnt]
                                      +train_comments_with_tag[train_end:]))

print(accuracy(train_comments_with_tag[int(like_cnt*0.8):like_cnt]
                                      +train_comments_with_tag[train_end:], classify_result) )
'''
classifier = EvaluateFactorClass(train_comments_with_tag[:60]
                                 +train_comments_with_tag[75:275]
                                 , urls[8])

classify_result =classifier.tag(untag(train_comments_with_tag[60:75]
                                      +train_comments_with_tag[275:315]))

print(accuracy(train_comments_with_tag[60:75]
                                      +train_comments_with_tag[275:315], classify_result) )
'''
print("up to %d is liked" % like_cnt)
for i in range(len(classify_result)):
    if(classify_result[i][1]==1):    
        print(i)
