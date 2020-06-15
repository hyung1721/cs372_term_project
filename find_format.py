# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:43:17 2020

@author: hoyac
"""
import nltk
from nltk import FreqDist
from nltk.corpus import gutenberg, brown, webtext
from pickle import dump
from pickle import load
from crawl import tokenize_comments


def high_freq(elems,percent):
    fdist=FreqDist(elems)
    return [elem for (elem,_) in fdist.most_common(int(len(fdist)*percent))]


def save_other_grams ():
    HIGH_FREQ_UNI=0.01
    HIGH_FREQ_BI = 0.02
    HIGH_FREQ_TRI = 0.02
    other_corpus_unigrams = [w.lower() for w in (gutenberg.words() + brown.words()+webtext.words())]
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
      
def not_other_corpus(elems, other_corpus_elems):
    #return elems
    return [elem for elem in elems if not elem in other_corpus_elems]

def remove_aph(elems):
    return [elem for elem in elems if not '’' in elem and all( ("'" not in word) for word in elem ) ] 
    
def get_format_criteria (comments,other_grams_triple):
    HIGH_FREQ_UNI=0.001
    HIGH_FREQ_BI = 0.001
    HIGH_FREQ_TRI = 0.001
    unigrams, bigrams, trigrams = ([],[],[])
    
    other_corpus_freq_unigrams = other_grams_triple[0]
    other_corpus_freq_bigrams = other_grams_triple[1]
    other_corpus_freq_trigrams = other_grams_triple[2]
    
    
    try:
        f = open("unigrams_from_all_comments.pkl", "rb")
        unigrams=load(f)
        f.close()
        
        f = open("biigrams_from_all_comments.pkl", "rb")
        bigrams=load(f)
        f.close()
        
        f = open("trigrams_from_all_comments.pkl", "rb")
        trigrams=load(f)
        f.close()
    
    except:
        print(len(comments))
        for idx,cmt in enumerate(comments):
            if idx%1000==0: 
                print(idx)
    
            comment = [w.lower() for w in cmt]
    
            unigrams = add_uni(comment,unigrams)
    
            bigrams = add_bi(comment, bigrams)
    
            trigrams = add_tri(comment, trigrams)
        
        f = open("unigrams_from_all_comments.pkl", "wb")
        dump(unigrams, f)
        f.close()
        
        f = open("biigrams_from_all_comments.pkl", "wb")
        dump(bigrams, f)
        f.close()
        
        f = open("trigrams_from_all_comments.pkl", "wb")
        dump(trigrams, f)
        f.close()

        
    print("here1")

    #unigrams = high_freq( not_other_corpus (unigrams, other_corpus_freq_unigrams) , HIGH_FREQ_UNI)

    bigrams = high_freq( remove_aph(not_other_corpus (bigrams, other_corpus_freq_bigrams)), HIGH_FREQ_BI )
    print("here2")

    bigrams = [bigram for bigram in bigrams if bigram not in[('?','!'),('...','...'),('--', '--'),('...','.'),('!','!'),('?','?'),('...', '..')]]
    
                                                                        

    
    trigrams = high_freq ( remove_aph(not_other_corpus(trigrams, other_corpus_freq_trigrams)) , HIGH_FREQ_TRI)
    print("here3")

    trigrams=[trigram for trigram in trigrams if trigram not in [('!','!', '!'), ('?','?','?'), ('--', '--', '--'), ('...', '...', '...')]]
                                                       
    print("here4")
#############################################
  #  try:
   #     bigrams.remove(('this','video'))
   # except:None
    #bigrams.remove(('this','song')) 
   # try:
   #     bigrams.remove(('https', ':'))
  #  except: None
   # if('so','cute') in bigrams: bigrams.remove(('so','cute'))
 #   try:
       # trigrams.remove(('this','song','is'))
    #except:None

##############################################
    return [], bigrams, trigrams


def get_format_from_comments(train_comment_data_list):
    other_grams_triple = load_other_grams()
    tokenized_comment_list = tokenize_comments(train_comment_data_list)  
    
    ##
#    tokenized_comment_list = tokenized_comment_list[:5000]
    
    print(len(tokenized_comment_list))
    
    return get_format_criteria(tokenized_comment_list, other_grams_triple )


    






    
    
    