# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:43:17 2020

@author: hoyac
"""
import nltk
from nltk import FreqDist
from nltk.corpus import gutenberg, brown
from pickle import dump
from pickle import load



def high_freq(elems,percent):
    fdist=FreqDist(elems)
    return [elem for (elem,_) in fdist.most_common(int(len(fdist)*percent))]


def save_other_grams ():
    HIGH_FREQ_UNI=0.01
    HIGH_FREQ_BI = 0.003
    HIGH_FREQ_TRI = 0.001
    other_corpus_unigrams = [w.lower() for w in (gutenberg.words() + brown.words())]
    other_corpus_freq_unigrams = high_freq(other_corpus_unigrams, HIGH_FREQ_UNI)
    output = open('unigrams_data.pkl', 'wb')
    dump(other_corpus_freq_unigrams, output, -1)
    output.close()
    
    other_corpus_bigrams = nltk.bigrams(other_corpus_unigrams)
    other_corpus_freq_bigrams = high_freq(other_corpus_bigrams, HIGH_FREQ_BI)
    output = open('bigrams_data.pkl', 'wb')
    dump(other_corpus_freq_bigrams, output, -1)
    output.close()


    other_corpus_trigrams = nltk.trigrams(other_corpus_unigrams)
    other_corpus_freq_trigrams = high_freq(other_corpus_trigrams, HIGH_FREQ_TRI)
    output = open('trigrams_data.pkl', 'wb')
    dump(other_corpus_freq_trigrams, output, -1)
    output.close()
    
def load_other_grams ():
    input = open('unigrams_data.pkl', 'rb')
    other_corpus_freq_unigrams = load(input)
    input.close()
    
    input = open('bigrams_data.pkl', 'rb')
    other_corpus_freq_bigrams = load(input)
    input.close()
    
    input = open('trigrams_data.pkl', 'rb')
    other_corpus_freq_trigrams = load(input)
    input.close()
    
    return other_corpus_freq_unigrams, other_corpus_freq_bigrams, other_corpus_freq_trigrams


def add_uni(cmt, uni):
    cmt_uni = [w for w in cmt if w.isalpha()]
    return uni+cmt_uni
    
def add_bi(cmt, bi):
    cmt_bi=list(nltk.bigrams(cmt))
    return bi+cmt_bi
       
def add_tri(cmt, tri):
    cmt_tri=list(nltk.trigrams(cmt))
    return tri+cmt_tri
      
def not_other_corpus(high_freq_elems, other_corpus_elems):
    return [elem for elem in high_freq_elems if not elem in other_corpus_elems]
    
def get_format_criteria (comments,other_grams_triple):
    HIGH_FREQ_UNI=0.01
    HIGH_FREQ_BI = 0.003
    HIGH_FREQ_TRI = 0.001
    unigrams, bigrams, trigrams = ([],[],[])
    
    other_corpus_freq_unigrams = other_grams_triple[0]
    other_corpus_freq_bigrams = other_grams_triple[1]
    other_corpus_freq_trigrams = other_grams_triple[2]
    
    for cmt in comments:
        comment = [w.lower() for w in cmt]
        unigrams = add_uni(comment,unigrams)
        bigrams = add_bi(comment, bigrams)
        trigrams = add_tri(comment, trigrams)
        
    unigrams = not_other_corpus(high_freq(unigrams, HIGH_FREQ_UNI), other_corpus_freq_unigrams)
########할거면 거른 후에 해야함!!  -> bigrams도 마찬가지~
    
    
    bigrams = not_other_corpus(high_freq(bigrams, HIGH_FREQ_BI), other_corpus_freq_bigrams)
    trigrams = not_other_corpus(high_freq(trigrams, HIGH_FREQ_TRI), other_corpus_freq_trigrams)
    return unigrams, bigrams, trigrams




    






    
    
    