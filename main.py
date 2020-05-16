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

#print ("first time: initialize_dataset()")
#print ("other times: get_format_from_comments(load_comment_data_train()) ")
print ("other times: probability_factor_format() ")



def initialize_dataset():
    save_other_grams()
    save_comment_data_train()
    save_comment_data_test()


def probability_factor_format (): 
    _, bigrams, trigrams = get_format_from_comments(load_comment_data_train())
    tokenized_comment_list = tokenize_comments(load_comment_data_test())
    
    
    liked_tokenized_comment_list = tokenize_liked_comments(load_comment_data_test())
    
    
    factor_comments = defaultdict(int)
    
    num_factor_comments = 0
    
    for tokenized_comment in tokenized_comment_list:
        is_bigram = False
        for bigram in nltk.bigrams(tokenized_comment):
            if bigram in bigrams:
                num_factor_comments += 1
                is_bigram = True 
              #  factor_comments.append(tokenized_comment)]
                factor_comments[bigram] = factor_comments[bigram]+1
                break
        if is_bigram: continue
        for trigram in nltk.trigrams(tokenized_comment):
            if trigram in trigrams:
                num_factor_comments+=1
              #  factor_comments.append(tokenized_comment)
                factor_comments[trigram] = factor_comments[trigram]+1
                break
    
    liked_factor_comments = defaultdict(int)
    num_liked_factor_comments = 0
    
    for liked_tokenized_comment in liked_tokenized_comment_list:
        is_bigram = False
        for bigram in nltk.bigrams(liked_tokenized_comment):
            if bigram in bigrams:
                num_liked_factor_comments += 1
                is_bigram = True 
                liked_factor_comments[bigram] = liked_factor_comments[bigram]+1
                break
        if is_bigram: continue
        for trigram in nltk.trigrams(liked_tokenized_comment):
            if trigram in trigrams:
                num_liked_factor_comments+=1
                liked_factor_comments[trigram] = liked_factor_comments[trigram]+1
                break
       
    r1=sorted(factor_comments.items(), key= lambda elem:elem[1], reverse=True)
    r2=sorted(liked_factor_comments.items(), key= lambda elem:elem[1], reverse=True)
    return r1, num_factor_comments, r2, num_liked_factor_comments, num_liked_factor_comments/num_factor_comments


def probability_factor_timing ():
    
    return 1.0

def probabilty_factor_subscribers ():
    
    return 1.0

