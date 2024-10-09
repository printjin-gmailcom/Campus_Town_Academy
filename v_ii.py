import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup

# chromedriver 최신버전설치
chromedriver_autoinstaller.install()
# 브라우저 열기
browser = webdriver.Chrome()

url = 'https://www.melon.com/chart/index.htm'
browser.get(url)

soup = BeautifulSoup( browser.page_source, 'html.parser')
soup

# soup.select('tr.lst50')
# soup.select('tr.lst100')

song_list = soup.select('tbody > tr')
for song in song_list:
    title = song.select('div.ellipsis.rank01 > span > a')[0].text
    singer_tag_list = song.select('div.ellipsis.rank02 > a')
    singer_text_list = [ ]
    for singer_tag in singer_tag_list:
        singer = singer_tag.text
        singer_text_list.append(singer)
    singer_text = ' ||| '.join(singer_text_list)
    print(title, singer_text)



# song_list = soup.select('tbode > tr')
# results = [ ]
# for song in song_list:
#     song = soup.select('div.ellipsis.rank01 > span > a')[0].text
#     singer = soup.select('div.ellipsis.rank02 > a')[0].text
#     album = soup.select('div.ellipsis.rank03 > a')[0].text
#     like = soup.select('button.like > span.cnt')[0].text.strip()[4:]

#    data[song, singer, album, like]
#    results.append(data)

# results

