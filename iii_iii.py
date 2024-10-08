import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver_autoinstaller.install()
browser = webdriver.Chrome()

url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page=1'
browser.get(url)

soup = BeautifulSoup(browser.page_source, "html.parser")

channel_list = soup.select('tr.aos-init')
len(channel_list)

for channel in channel_list:
    title = channel.select("h1>a")[0].text.strip()
    category = channel.select("p.category")[0].text.strip()
    sub = channel.select("td.subscriber_cnt")[0].text.strip()
    view = channel.select("td.view_cnt")[0].text.strip()
    video = channel.select("td.video_cnt")[0].text.strip()
    print(title,category,sub,view,video)

page = 5
url = f'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page= {page}'
browser.get(url)



import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup

# chromedriver 최신버전설치
chromedriver_autoinstaller.install()
# 브라우저 열기
browser = webdriver.Chrome()



import time

results = [ ]


# 접속하기
for page in range(1,11):

    url = f'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page={page}'
    browser.get(url)

    # 잠깐 기다려줘!!!
    time.sleep(1)

    # 데이터 다운 -> 해석하기
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 채널리스트 찾기
    channel_list = soup.select('tr.aos-init')

    # 각 채널별로 필요한 정보(채널명, 카테고리, 구독자수 ,,, )
    # 채널별 정보 찾기
    for channel in channel_list:
        title = channel.select('h1 > a')[0].text.strip()
        category = channel.select('p.category')[0].text.strip()
        subscriber = channel.select('td.subscriber_cnt')[0].text# 구독자수
        view = channel.select('td.view_cnt')[0].text  # 영상조회수
        video = channel.select('td.video_cnt')[0].text  # 영상수
        # print(title, category, subscriber, view, video)
        data = [ title, category, subscriber, view, video ]
        results.append(data)

    print(results)

import pandas as pd
df = pd.DataFrame(results)
df.columns = ['채널명', '카테고리', '구독자수', '조회수', '영상수']
df.to_excel('./유튜브랭킹.xlsx', index = False)

