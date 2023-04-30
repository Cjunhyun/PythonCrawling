from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium import webdriver
import time

wd = webdriver.Chrome('/Users/jnhyn/Documents/Jun/4학년1학기/빅데이터/chromedriver')

#베스트 국내도서 중 여행 카테고리에서 크롤링
def Book_crawling(result,check):
    wd = webdriver.Chrome('/Users/jnhyn/Documents/Jun/4학년1학기/빅데이터/chromedriver')

    for i in ["1","2","3","4"]:
        url = "https://product.kyobobook.co.kr/bestseller/online?period=001#?page="+i+"&per=50&ymw=&period=001&saleCmdtClstCode=32&dsplDvsnCode=001&dsplTrgtDvsnCode=004&saleCmdtDsplDvsnCode="

        wd.get(url)
        time.sleep(15)

        if(check == 0):

            #카테고리의 화살표를 눌러 카테고리 전체 보기
            category_button1 = wd.find_element_by_xpath('//*[@id="domesticList"]/button')
            category_button1.click()
            time.sleep(15)

            #카테고리 중 "여행" 클릭
            category_button2 = wd.find_element_by_xpath('//*[@id="domesticList"]/div/ul/li[20]/button')
            category_button2.click()
            time.sleep(15)

            check = 1

        html = wd.page_source
        soupCB1 = BeautifulSoup(html, 'html.parser')

        try:
            #책 개수
            book_name_list = soupCB1.select("div.prod_info_box > a > span")
            book_len = len(book_name_list)

            for n in range(book_len):
                #책 이름
                book_name_list = soupCB1.select("div.prod_info_box > a > span")
                one_book_name = book_name_list[n].string

                #책 정보(지은이, 출판일)
                book_writer_list = soupCB1.select("div.prod_info_box > span.prod_author")
                one_book_writer_date = book_writer_list[n].get_text().strip()
                one_book_writer_date = one_book_writer_date.split('  · ')
                #책 지은이
                one_book_writer = one_book_writer_date[0]
                #책 출판일
                one_book_date = one_book_writer_date[1]


                #책 가격
                book_price_list = soupCB1.select("div.prod_info_box > div.prod_price > span.price > span.val")
                book_price = book_price_list[n].text


                result.append([one_book_name]+[one_book_writer]+[one_book_date]+[book_price])
        except:
            continue
            
    return


def main():
    result= []
    check = 0
    print('book crawling >>>>>>>>>>>>>>>>>>>>>>>>') 
    Book_crawling(result,check)
    print(result)
    CB_tbl = pd.DataFrame(result,columns =('name','writer','date','price')) 
    CB_tbl.to_csv('./2-최준현-201835753.csv', encoding = 'cp949', mode = 'w',index = True)

main()