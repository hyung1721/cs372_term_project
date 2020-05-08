# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:43:17 2020

@author: hoyac
"""
import nltk
from nltk import FreqDist
from nltk.corpus import gutenberg, brown

HIGH_FREQ_UNI=0.01
HIGH_FREQ_BI = 0.003
HIGH_FREQ_TRI = 0.001

def high_freq(elems,percent):
    fdist=FreqDist(elems)
    return [elem for (elem,_) in fdist.most_common(int(len(fdist)*percent))]

other_corpus_unigrams = [w.lower() for w in (gutenberg.words() + brown.words())]
other_corpus_freq_unigrams = high_freq(other_corpus_unigrams, HIGH_FREQ_UNI)

other_corpus_bigrams = nltk.bigrams(other_corpus_unigrams)
other_corpus_freq_bigrams = high_freq(other_corpus_bigrams, HIGH_FREQ_BI)

other_corpus_trigrams = nltk.trigrams(other_corpus_unigrams)
other_corpus_freq_trigrams = high_freq(other_corpus_trigrams, HIGH_FREQ_TRI)

def add_uni(cmt, uni):
    return uni+cmt
    
def add_bi(cmt, bi):
    cmt_bi=list(nltk.bigrams(cmt))
    return bi+cmt_bi
       
def add_tri(cmt, tri):
    cmt_tri=list(nltk.trigrams(cmt))
    return tri+cmt_tri
      
def not_other_corpus(high_freq_elems, other_corpus_elems):
    return [elem for elem in high_freq_elems if not elem in other_corpus_elems]
    
def get_format_criteria (comments):
    unigrams, bigrams, trigrams = ([],[],[])
    
    for cmt in comments:
        comment = [w.lower() for w in cmt]
        unigrams = add_uni(comment,unigrams)
        bigrams = add_bi(comment, bigrams)
        trigrams = add_tri(comment, trigrams)
        
    unigrams = not_other_corpus(high_freq(unigrams, HIGH_FREQ_UNI), other_corpus_freq_unigrams)
    bigrams = not_other_corpus(high_freq(bigrams, HIGH_FREQ_BI), other_corpus_freq_bigrams)
    trigrams = not_other_corpus(high_freq(trigrams, HIGH_FREQ_TRI), other_corpus_freq_trigrams)
    return unigrams, bigrams, trigrams




    






    
    
    