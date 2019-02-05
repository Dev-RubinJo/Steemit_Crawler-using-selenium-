from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
import time

get_ids = pd.read_csv('total.csv')
test_id_list = get_ids['Userid']

driver_path = "/Users/yoobinjo/Desktop/My stuff/programming/Developing/Developing language/tools/chromedriver"

options = webdriver.ChromeOptions()
#options.add_argument('headless')

dv = webdriver.Chrome(driver_path, chrome_options=options)
#페이지 로딩 대기 시간 10초
dv.implicitly_wait(10)

f = open('data.csv', 'w', encoding='utf-8', newline='')

def set_url(list):
    url_list = []
    for i in range(len(list)):
        url = 'https://'
        url += list[i]
        url_list.append(url)
    return url_list

#맨 밑에 포스트까지 업데이트 후 긁어오는 함수
def get_full_html(dv):
    flag = False
    while flag == False:
        html = dv.page_source
        soup = bs(html, 'html.parser')
        comment_list = soup.find_all('div', class_='PostSummary__body entry-content')
        tag_content1= comment_list[len(comment_list)-1]
        dv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #콘텐츠 로딩시간 3초
        time.sleep(3)
        html = dv.page_source
        soup = bs(html, 'html.parser')
        comment_list = soup.find_all('div', class_='PostSummary__body entry-content')
        tag_content2 = comment_list[len(comment_list) - 1]

        if tag_content1 == tag_content2:
            flag = True
            return soup

def get_some_html(dv):
    flag = 5
    while flag > 0:
        dv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        flag -= 1
    html = dv.page_source
    soup = bs(html, 'html.parser')
    return soup

#dv.get('https://steemit.com/@explorenature')   <- 예시로 한번 해본 계정
def get_data(dv, url_list, list, file):
    f = csv.writer(file)
    f.writerow(['account', 'comment'])
    for i in range(len(url_list)):
        user_comment = []
        user_comment.append(list[i])
        dv.get(url_list[i])

        #테스트를 위한 코드 삽입
        #dv.get('https://steemit.com/@explorenature')

        soup = get_full_html(dv)

        # 테스트를 위한 코드 삽입
        #soup = get_some_html(dv)

        comment_list = soup.find_all('div', class_='PostSummary__body entry-content')
        for comment in comment_list:
            user_comment.append(comment.get_text())
        f.writerow(user_comment)

url_list = set_url(test_id_list)
get_data(dv, url_list, test_id_list, f)





f.close()
dv.quit()

#처음 페이지에서 보여지는 게시글 태그 셀렉터
#posts_list > ul > li:nth-child(15) > div > div.articles__content.hentry.with-image > div.articles__content-block.articles__content-block--text > div.PostSummary__body.entry-content

#포스트 게시자 계정
#posts_list > ul > li:nth-child(1) > div > div.articles__summary-header > div.user > div.user__col.user__col--right > span.user__name > span > strong > a

#포스팅 된 글
#posts_list > ul > li:nth-child(1) > div > div.articles__content.hentry.with-image > div.articles__content-block.articles__content-block--text > div.PostSummary__body.entry-content > a