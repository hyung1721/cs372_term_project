# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:30:05 2020

@author: hyung
"""

# git test 
import nltk
from find_format import save_other_grams,load_other_grams, get_format_from_comments
from crawl import save_comment_data_train, load_comment_data_train, save_comment_data_test, load_comment_data_test, tokenize_comments, tokenize_liked_comments
import pandas as pd
from collections import defaultdict
from pickle import load, dump
from operator import itemgetter
import csv

import youtubeapi

#print ("first time: initialize_dataset()")
#print ("other times: get_format_from_comments(load_comment_data_train()) ")
print ("other times: bigrams, trigrams, bi, tri = probability_factor_format() ")
print ("get result: produce_result_from_file() ")



def initialize_dataset():
    save_other_grams()
    save_comment_data_train()
    save_comment_data_test()


def probability_factor_format (): 
    
    
  
   
    
    ## previous crawl
    #_, bigrams, trigrams = get_format_from_comments(load_comment_data_train())
   # tokenized_comment_list = tokenize_comments(load_comment_data_test())
   # liked_tokenized_comment_list = tokenize_liked_comments(load_comment_data_test())
    
    
    ## using youtube api
    #_, bigrams, trigrams = get_format_from_comments(youtubeapi.load_comments(isTrain=True))
   # tokenized_comment_list, liked_tokenized_comment_list = youtubeapi.load_comments(isTrain=False)
    
    
    ### new one
    
    ## load_comment_data_test() 만 계속 쓰면 됨!!
    try:
        f = open("high_freq_bigrams_0.1%.pkl", "rb")
        bigrams = load(f)
        f.close()
        
        f = open("high_freq_trigrams_0.1%.pkl", "rb")
        trigrams = load(f)
        f.close()
    except:
        _, bigrams, trigrams = get_format_from_comments(load_comment_data_test())
        
        
        f = open("high_freq_bigrams_0.1%.pkl", "wb")
        dump(bigrams, f)
        f.close()
        
        f = open("high_freq_trigrams_0.1%.pkl", "wb")
        dump(trigrams, f)
        f.close()
        
#    _, bigrams, trigrams = get_format_from_comments(load_comment_data_test())
        
        
#    f = open("high_freq_bigrams.pkl", "wb")
#    dump(bigrams, f)
#    f.close()
    
#    f = open("high_freq_trigrams.pkl", "wb")
#    dump(trigrams, f)
#    f.close()
    
    tokenized_comment_list = tokenize_comments(load_comment_data_test())
    liked_tokenized_comment_list = tokenize_liked_comments(load_comment_data_test())
    
    
    print("bigram start") 
    bigram_common_freq = []
    bigram_liked_freq = []
    for bigram in bigrams:
        if bigrams.index(bigram)%1000 == 0: print(bigrams.index(bigram))
        cnt_common = 0
        cnt_liked = 0
        for comment in tokenized_comment_list:
            if bigram in nltk.bigrams(comment): cnt_common+=1
        for liked_comment in liked_tokenized_comment_list:
            if bigram in nltk.bigrams(liked_comment): cnt_liked+=1
        bigram_common_freq.append(cnt_common/len(tokenized_comment_list))
        bigram_liked_freq.append(cnt_liked/len(liked_tokenized_comment_list))
    
    
    print("trigram start") 
    trigram_common_freq = []
    trigram_liked_freq = []
    for trigram in trigrams:
        if trigrams.index(trigram)%1000 == 0: print(trigrams.index(trigram))
        cnt_common = 0
        cnt_liked = 0
        for comment in tokenized_comment_list:
            if trigram in nltk.trigrams(comment): cnt_common+=1
        for liked_comment in liked_tokenized_comment_list:
            if trigram in nltk.trigrams(liked_comment): cnt_liked+=1
        trigram_common_freq.append(cnt_common/len(tokenized_comment_list))
        trigram_liked_freq.append(cnt_liked/len(liked_tokenized_comment_list))
    
    
    
    result_bi = sorted(list(zip(bigrams, bigram_common_freq, bigram_liked_freq)), key = itemgetter(2), reverse = True)
    f = open("bigram_frequency_in_liked.pkl", "wb")
    dump(result_bi, f)
    f.close()
    
    result_tri = sorted(list(zip(trigrams, trigram_common_freq, trigram_liked_freq)), key = itemgetter(2), reverse = True)
    f = open("trigram_frequency_in_liked.pkl", "wb")
    dump(result_tri, f)
    f.close()
    
    return bigrams, trigrams, result_bi, result_tri    

def produce_result_from_file():
    f = open("bigram_frequency_in_liked.pkl", "rb")
    bigram_result = load(f)
    f.close()
    
    f = open("trigram_frequency_in_liked.pkl", "rb")
    trigram_result = load(f)
    f.close()
    
    bigrams, bi_common_freq, bi_like_freq = tuple(zip(*bigram_result))
    trigrams, tri_common_freq, tri_like_freq = tuple(zip(*trigram_result))
    
#    plt.plot(list(bigrams), list(bi_like_freq))
    bi_ratio = [list(bi_like_freq)[i]/list(bi_common_freq)[i] for i in range(len(bigrams))]
    tri_ratio = [list(tri_like_freq)[i]/list(tri_common_freq)[i] for i in range(len(bigrams))]
    
    bi_with_common = sorted(list(zip(bigrams, bi_common_freq)), key = itemgetter(1), reverse = True)
    tri_with_common = sorted(list(zip(trigrams, tri_common_freq)), key = itemgetter(1), reverse = True)
    
    bi_with_like = list(zip(bigrams, bi_like_freq))
    tri_with_like = list(zip(trigrams, tri_like_freq))
    
    bi_with_ratio = sorted(list(zip(bigrams, bi_ratio)), key = itemgetter(1), reverse = True)
    tri_with_ratio = sorted(list(zip(trigrams, tri_ratio)), key = itemgetter(1), reverse = True)
    
    

#    """

    f = open("bi_common_freq.csv", 'w', encoding = 'UTF-8')
    wr = csv.writer(f)
    for r in bi_with_common: wr.writerow(r)
    f.close()
    
    f = open("bi_like_freq.csv", 'w', encoding = 'UTF-8')
    wr = csv.writer(f)
    for r in bi_with_like: wr.writerow(r)
    f.close()
    
    f = open("bi_ratio.csv", 'w', encoding = 'UTF-8')
    wr = csv.writer(f)
    for r in bi_with_ratio: wr.writerow(r)
    f.close()
    
    f = open("tri_common_freq.csv", 'w', encoding = 'UTF-8')
    wr = csv.writer(f)
    for r in tri_with_common: wr.writerow(r)
    f.close()
    
    f = open("tri_like_freq.csv", 'w', encoding = 'UTF-8')
    wr = csv.writer(f)
    for r in tri_with_like: wr.writerow(r)
    f.close()
    
    f = open("tri_ratio.csv", 'w', encoding = 'UTF-8')
    wr = csv.writer(f)
    for r in tri_with_ratio: wr.writerow(r)
    f.close()

#    """
    
    
    print("""
          --------------------------------------------------------------
          Producing Results
          
          For 0.5% high frequency bigrams and 1% high frequency trigrams
          
          --------------------------------------------------------------
          Top 20 bigrams ranked by frequency in common comments
          You can see whole result in bi_common_freq.csv
          """)
    print(bi_with_common[:20])
    print("""
          --------------------------------------------------------------
          Top 20 bigrams ranked by frequency in like comments
          You can see whole result in bi_like_freq.csv
          """)
    print(bi_with_like[:20])
    print("""
          --------------------------------------------------------------
          Top 20 bigrams ranked by ratio of like-freq and common-freq
          You can see whole result in bi_ratio.csv
          """)
    print(bi_with_ratio[:20])
    print("""
          --------------------------------------------------------------
          Top 20 trigrams ranked by frequency in common comments
          You can see whole result in tri_common_freq.csv
          """)
    print(tri_with_common[:20])
    print("""
          --------------------------------------------------------------
          Top 20 trigrams ranked by frequency in like comments
          You can see whole result in tri_like_freq.csv
          """)
    print(tri_with_like[:20])
    print("""
          --------------------------------------------------------------
          Top 20 trigrams ranked by ratio of like-freq and common-freq
          You can see whole result in tri_ratio.csv
          """)
    print(tri_with_ratio[:20])
    print("""
          --------------------------------------------------------------
          """)
    
    
    

    
    
    

def probability_factor_timing ():
    
    return 1.0

def probabilty_factor_subscribers ():
    
    return 1.0

