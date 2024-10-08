import time

# 1. 크롬브라우저 열기
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# chromedriver 최신버전설치
chromedriver_autoinstaller.install()
# 브라우저 열기
browser = webdriver.Chrome()

url = 'https://search.shopping.naver.com/catalog/25995128523?cat_id=50002543'
browser.get(url)

results = [ ]

page_button_list = browser.find_elements("css selector","div.productList_seller_wrap__FZtUS > div.pagination_pagination__JW7zT > a")
for page_button in page_button_list:
    page_button.click() # 페이지 버튼 클릭해줘
    time.sleep(1) # 1초만 기다려줘

    soup = BeautifulSoup(browser.page_source, "html.parser")
    item_list = soup.select('ul.productList_list_seller__XGhCk > li')

    # 전체 상품에서 --> 상품별 정보 찾기
    for item in item_list:
        title = item.select('a.productList_title__R1qZP')[0].text
        url = item.select('a.productList_title__R1qZP')[0]['href']
        try: # 먼저 이미지 찾아줘
            mall = item.select('img')[0]['alt']
        except:  # 만약 에러난다면...  span 으로 찾아줘
            mall = item.select('a.productList_mall_link__TrYxC > span')[0].text
        price = item.select('a > span > em')[0].text
        deli = item.select('div.productList_delivery__WwSwL')[0].text
        if deli == '무료배송': # True / False
            deli_num = '0'
        elif deli == '착불':
            deli_num = '5,000'
        else:
        #     deli_num = deli.replace('원', '')
            deli_num = deli[:-1]
        print(title, mall, price, deli, deli_num)

        data = [title, mall, price, deli, deli_num]
        results.append(data)

import pandas as pd
df = pd.DataFrame(results)
df.columns = ['title','mall', 'price','delivery_text','delivery']
df.to_excel('네이버 쇼핑몰 크롤링.xlsx', index = False)

