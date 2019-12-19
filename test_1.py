#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from konlpy.tag import Okt
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#path = "C:/Users/yhs25/Downloads/chromedriver_win32/chromedriver.exe"
path = "/usr/lib/chromium-browser/chromedriver"

comment_data = pd.DataFrame({'youtube_id': [],
                             'comment': [],
                             'comment_token':[],
                             'like_num': [],
                             'user_img': []})
comment_data2 = pd.DataFrame({'youtube_id': [],
                             'comment': [],
                             'comment_token':[],
                             'like_num': [],
                             'user_img': []})
browser = webdriver.Chrome(path)  # chrome_options=options
browser.implicitly_wait(2)
browser.maximize_window()  # 전체화면이 아니라 최대화하는 방법

browser.get('http://www.youtube.com')
elem = browser.find_element_by_name("search_query")
elem.clear()
elem.send_keys("무한도전 괴도광희")
elem.submit()
browser.find_element_by_id("video-title").click()

body = browser.find_element_by_tag_name('body')
# 웹드라이버로 url접속한 뒤 스크롤 내리기 위한 소스를 받아오는 것

time.sleep(2)

num_page_down = 1
while num_page_down:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1.5)
    num_page_down -= 1


#browser.find_element_by_xpath('//*[@id="sort-menu"]').click()
#browser.find_element_by_xpath('//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]').click()
#browser.find_element_by_xpath('//paper-menu-button[@class="style-scope yt-dropdown-menu"]').click()


#time.sleep(1.5)
#browser.find_element_by_xpath('//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()
# driver.find_element_by_xpath('//*[@id="menu"]/a[2]/paper-item/paper-item-body/div[text()="최근 날짜순"]').click()


num_page_down = 20
while num_page_down:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1.5)
    num_page_down -= 1

html_s0 = browser.page_source
html_s = BeautifulSoup(html_s0, 'html.parser')

comment0 = html_s.find_all('ytd-comment-renderer', {'class': 'style-scope ytd-comment-thread-renderer'})

okt = Okt()

for i in range(len(comment0)):
    # 댓글
    comment = comment0[i].find('yt-formatted-string',
                               {'id': 'content-text', 'class': 'style-scope ytd-comment-renderer'}).text
    #comment_token = okt.nouns(comment)
    comment_token = okt.morphs(comment)
    #comment_token2 = hannanum.nouns(comment)
    try:
        aa = comment0[i].find('span', {'id': 'vote-count-left'}).text

        # re.findall('[0-9]',aa)
        # "".join(re.findall('[0-9]',aa)) -> 리스트 내부의 문자열의 합
        like_num = "".join(re.findall('[0-9]', aa)) + "개"
    except:
        like_num = 0

    bb = comment0[i].find('a', {'id': 'author-text'}).find('span').text
    youtube_id = "".join(re.findall('[가-힣0-9a-zA-Z]', bb))

    user_img = comment0[i].find('img', {'id': 'img'}).get('src')
    
    insert_data = pd.DataFrame({'youtube_id': [youtube_id],
                                'comment': [comment],
                                'comment_token': [comment_token],
                                'like_num': [like_num],
                                'user_img': [user_img]})

    comment_data = comment_data.append(insert_data)

    if '광희' not in comment_token:
        insert_data2 = pd.DataFrame({'youtube_id': [youtube_id],
                                     'comment':[comment],
                                     'comment_token': [comment_token],
                                     'like_num': [like_num],
                                     'user_img': [user_img]})
        comment_data2 = comment_data2.append(insert_data2)
    else: pass    
            
comment_data.index = range(len(comment_data))
comment_data.to_csv('comments_python.csv', encoding='utf-8-sig')
comment_data2.index = range(len(comment_data2))
comment_data2.to_csv('comments_python2.csv', encoding='utf-8-sig')
