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
def crawl_comment(url):
    comment_data = pd.DataFrame({'content':[],
                                'subcomment_num':[],
                                'like_num':[]})
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
    
    
    # 인기많은 댓글로 정렬
    #sort_xpath = '//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]'
    #browser.find_element_by_xpath(sort_xpath).click()
    
    browser.find_element_by_xpath('//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()
    
    # n번 스크롤하기 이거 늘리면 댓글 개수 늘어남!!!
    num_page_down = 10
    while num_page_down:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1.5)
        num_page_down -= 1
    
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
        
        new_comment_data =  pd.DataFrame({'content':[comment], 'subcomment_num':[subcomment_num], 'like_num':[like_num]})
        comment_data = comment_data.append(new_comment_data)
    
    comment_data.index = range(len(comment_data))
    
    return comment_data