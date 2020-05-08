# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:30:05 2020

@author: hyung
"""

# git test 

from crawl import crawl_comment
import pandas as pd
from nltk import word_tokenize
from nltk import Text
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag

#import find_format

url = 'https://www.youtube.com/watch?v=9bZkp7q19f0'


comment_data = crawl_comment(url).copy()

raw_comment_list = []
tokenized_comment_list = []

for i in range(len(comment_data)):
    temp = comment_data['content'].iloc[i]
    raw_comment_list.append(temp)
    tokenized_comment_list.append(word_tokenize(temp))

raw_text = ".".join(raw_comment_list)

retokenize = RegexpTokenizer("[\w]+")
text = Text(retokenize.tokenize(raw_text))

#stop_words = stopwords.words('english')
#comment_tokens = pos_tag(retokenize.tokenize(raw_text))
#tokenized_comment_list = [word[0] for word in comment_tokens if word[0] not in stop_words]
freqdist_comment = FreqDist(tokenized_comment_list)

freqdist_comment.plot(20)

#uni, bi, tri = find_format.get_format_criteria(tokenized_comment_list)
# 위에서 바꿔야 하는 부분 : retokenize말고 word_tokenize 이용
# 즉 tokenize_comment_list 이용 

