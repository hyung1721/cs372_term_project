# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 10:18:14 2020

@author: hyung
"""

from bs4 import BeautifulSoup 
import pandas as pd 
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from pickle import dump
from pickle import load
from nltk import word_tokenize


def crawl_comment(url, onlyTop=True):
    comment_data = pd.DataFrame({'content':[],
                                'subcomment_num':[],
                                'like_num':[],
                                'uploaded_time':[]})
    options = Options()
    options.add_argument('--start-maximized')
    
    delay=3
    browser = Chrome()
    browser.implicitly_wait(delay)
    #browser.maximize_window()
    
    start_url = url
    
    browser.get(start_url) 
    body = browser.find_element_by_tag_name('body')
    
    # 댓글 창으로 이동
    num_page_down = 1
    while(True):
        try:
            sort_xpath = '//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]'
            browser.find_element_by_xpath(sort_xpath).click()
            time.sleep(1.5)
            break
        except:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
            continue
    
    
    # 인기많은 댓글로 정렬      ->>  인기많은 댓글로 정렬 - train할때만 필요 <- 인기~likes라는 assumption 필요
    #sort_xpath = '//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]'
    #browser.find_element_by_xpath(sort_xpath).click()
    
    browser.find_element_by_xpath('//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()
    
    # n번 스크롤하기 이거 늘리면 댓글 개수 늘어남!!!
    # n = 원하는 댓글 개수 // 5
    if onlyTop:
        num_page_down = 15
        while num_page_down:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
            num_page_down -= 1
    else:
        last_page_height = browser.execute_script("return document.body.scrollHeight")
            
        while True:
            browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3.0)
            new_page_height = browser.execute_script("return document.documentElement.scrollHeight")
            if new_page_height == last_page_height:
                break
            last_page_height = new_page_height

            
        
  
    
    html_current = browser.page_source
    html_parsed = BeautifulSoup(html_current, 'html.parser')
    comment_block = html_parsed.find_all('ytd-comment-thread-renderer',{'class':'style-scope ytd-item-section-renderer'})
    
    for i in range(len(comment_block)):
        # content of comment
        comment = comment_block[i].find('yt-formatted-string',{'id':'content-text','class':'style-scope ytd-comment-renderer'}).text.lower()
        
        # number of subcomment of comment
        try:
            subcomment_button = comment_block[i].find('yt-formatted-string',{'id':'text','class':'style-scope ytd-button-renderer'}).text
            if (subcomment_button.strip() == '답글 보기'):
                subcomment_num = 1
            else:
                subcomment_num = subcomment_button.lstrip('답글').rstrip('개 보기').strip()
                if('천' in subcomment_num):
                    subcomment_num = subcomment_num.rstrip('천').strip()
                    subcomment_num = int(float(subcomment_num) * 1000)
                elif('만' in subcomment_num):
                    subcomment_num = subcomment_num.rstrip('만').strip()
                    subcomment_num = int(float(subcomment_num) * 10000)
                else:
                    subcomment_num = int(subcomment_num)
        except:
            subcomment_num = 0
        
        # number of like of comment
        try:
            like_button = comment_block[i].find('span',{'id':'vote-count-left'}).text
            like_num = like_button.strip()
            if('천' in like_num):
                like_num = like_num.rstrip('천').strip()
                #print(like_num)
                like_num = int(float(like_num) * 1000)
            elif('만' in like_num):
                like_num = like_num.rstrip('만').strip()
                #print(like_num)
                like_num = int(float(like_num) * 10000)
            else:
                like_num = int(like_num)
        except:
            like_num = 0
            
        try:
            uploaded_time = comment_block[i].find('yt-formatted-string', {'class':'published-time-text above-comment style-scope ytd-comment-renderer'}).find('a',{'class':'yt-simple-endpoint style-scope yt-formatted-string'}).text
            print(uploaded_time)
            uploaded_time = uploaded_time.split(' ')[0]
            print(uploaded_time)
            if('분' in uploaded_time or '초' in uploaded_time):
                uploaded_time = 0
            elif('시간' in uploaded_time):
                uploaded_time = uploaded_time.rstrip('시간').strip()
                uploaded_time = int(uploaded_time)
            elif('일' in uploaded_time):
                uploaded_time = uploaded_time.rstrip('일').strip()
                uploaded_time = int(uploaded_time) * 24
            elif('주' in uploaded_time):
                uploaded_time = uploaded_time.rstrip('주').strip()
                uploaded_time = int(uploaded_time) * 24 * 7
            elif('개월' in uploaded_time):
                uploaded_time = uploaded_time.rstrip('개월').strip()
                print(uploaded_time)
                uploaded_time = int(uploaded_time) * 24 * 30
                print(uploaded_time)
            elif('년' in uploaded_time):
                uploaded_time = uploaded_time.rstrip('년').strip()
                uploaded_time = int(uploaded_time) * 24 * 365
        except:
            print('error')
        new_comment_data =  pd.DataFrame({'content':[comment], 'subcomment_num':[subcomment_num], 'like_num':[like_num], 'uploaded_time':[uploaded_time]})
        comment_data = comment_data.append(new_comment_data)
    
    comment_data.index = range(len(comment_data))
    
    return comment_data


def crawl_comment_list(urls, isTop):
    comment_data_list = []
    
    for url in urls:
        comment_data_list.append(crawl_comment(url, isTop).copy())
    
    return comment_data_list
    

def save_comment_data_train(): 
    # csv파일에서 링크들을 받아오도록 수정 
    urls = ['https://www.youtube.com/watch?v=9bZkp7q19f0', 'https://www.youtube.com/watch?v=W85F-UmnbF4'
,'https://www.youtube.com/watch?v=Yr14Io0wsiU', 'https://www.youtube.com/watch?v=0mJiPcKybzU', 'https://www.youtube.com/watch?v=szdbKz5CyhA'
,'https://www.youtube.com/watch?v=Y_ZS_EfoYpA', 'https://www.youtube.com/watch?v=yPWAfjvVtEM', 'https://www.youtube.com/watch?v=2Qa9YDgtcaM',
'https://www.youtube.com/watch?v=WN-IW6wOdnI', 'https://www.youtube.com/watch?v=vWgjqMyP5kk', 'https://www.youtube.com/watch?v=27Dx6ztJ8jw',
'https://www.youtube.com/watch?v=PzVqQWxBXQE',  'https://www.youtube.com/watch?v=27Dx6ztJ8jw', 'https://www.youtube.com/watch?v=HFsKxbrZKNQ',
'https://www.youtube.com/watch?v=cG_NB2cQnGU', 'https://www.youtube.com/watch?v=XDXrP9HET2A', 'https://www.youtube.com/watch?v=N-sLp2Ri76s']
    

    comment_data_list = crawl_comment_list(urls, True)
   
    output = open('train_comment_data_list.pkl', 'ab')

    dump(comment_data_list, output, -1)
    output.close()

def load_comment_data_train():
  
    input = open('train_comment_data_list.pkl', 'rb')
  
    
    ## 여기서 while문이 들어가야함()
    comment_data_list = load(input)
    
    
    
    input.close()
    
    return comment_data_list


def save_comment_data_test(): 
    # csv파일에서 링크들을 받아오도록 수정 
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
    

    comment_data_list = crawl_comment_list(urls, False)
 
   # output = open('test_comment_data_list.pkl', 'ab')
    output = open('test_comment_data_list.pkl', 'ab')

    dump(comment_data_list, output, -1)
    output.close()
    
def load_comment_data_test():
    comment_data_list = []
    input = open('test_comment_data_list.pkl', 'rb')
    
    while True:
        try:
            load_data_list = load(input)
        except:
            break
        
        comment_data_list = comment_data_list + load_data_list
        
    input.close()
    return comment_data_list


def after_tokenize(words):
    for index,word in enumerate(words):
        if index==len(words)-1: break
        if word=='gon' and words[index+1] =='na':
            words[index] = 'gonna'
            words.pop(index+1)
        if word=='wan' and words[index+1] =='na':
            words[index] = 'wanna'
            words.pop(index+1)
    return words

def tokenize_comments (comment_data_list):
    #raw_comment_list = []
    tokenized_comment_list = []
    
    for comment_data in comment_data_list:
        for i in range(len(comment_data)):
            temp = comment_data['content'].iloc[i]
       #     raw_comment_list.append(temp)
            tokenized_comment_list.append(after_tokenize(word_tokenize(temp)))
############################################################################    
   # raw_text = ".".join(raw_comment_list)    
  #  retokenize = RegexpTokenizer("[\w]+")
  #  text = Text(retokenize.tokenize(raw_text))    
  #  stop_words = stopwords.words('english')
  #  comment_tokens = pos_tag(retokenize.tokenize(raw_text))
  #  tokenized_comment_list2 = [word[0] for word in comment_tokens if word[0] not in stop_words]
  #  freqdist_comment = FreqDist(tokenized_comment_list2)  
  #  freqdist_comment.plot(20)
############################################################################ 
    return tokenized_comment_list 
    #return raw_comment_list, tokenized_comment_list

def tokenize_liked_comments(comment_data_list):
    tokenized_liked_comment_list = []
    
  
    for index, comment_data in enumerate(comment_data_list):
        like_content_list = []
        num_comments = len(comment_data)
        for i in range(num_comments):
            likenum, content = comment_data['like_num'].iloc[i] , comment_data['content'].iloc[i]
            like_content_list.append((likenum, content))
        like_content_list.sort(key = lambda x:x[0] , reverse=True)
        like_content_list = like_content_list[:max(int(num_comments*0.01),1)]
        
        for _, content in like_content_list:
            tokenized_liked_comment_list.append( after_tokenize(word_tokenize(content)))      
        
    return tokenized_liked_comment_list