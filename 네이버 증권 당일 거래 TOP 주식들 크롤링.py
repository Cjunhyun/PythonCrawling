from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium import webdriver
import time
#네이버 증권 당일 거래 TOP 주식들 크롤링

def Stock_crawling(result):
    wd = webdriver.Chrome('chromedriver 디렉토리 위치')
    time.sleep(3)
    
    url = "https://finance.naver.com/"
    wd.get(url)
    time.sleep(3)
    
    html = wd.page_source
    soupCB1 = BeautifulSoup(html, 'html.parser')
    
    #당일 거래 상위 종목(상승)
    stock_name_list1 = soupCB1.select("#_topItems1 > tr.up")

    #당일 거래 상위 종목(하락)
    stock_name_list2 = soupCB1.select("#_topItems1 > tr.down")

    #당일 거래 상위 종목리스트(상승 + 하락)
    stock_name_list = stock_name_list1 + stock_name_list2

    #종목(주식) 개수
    stock_len = len(stock_name_list)

    for i in range(stock_len):
        n = str(i+1)
        try:
            #주식 가격
            stock_price_list = soupCB1.select("#_topItems1 > tr:nth-child("+n+") > td:nth-child(2)")
            stock_price = stock_price_list[0].text

            #주식 이름
            stock_name_list = soupCB1.select("#_topItems1 > tr:nth-child("+n+") > th > a")
            stock_name = stock_name_list[0].text

            #주식 상승하락폭(금액)
            stock_pice_updown_list1 = soupCB1.select("#_topItems1 > tr:nth-child("+n+") > td:nth-child(3)")
            stock_pice_updown1 = stock_pice_updown_list1[0].text

            #주식 상승하락폭(퍼센트)
            stock_pice_updown_list2 = soupCB1.select("#_topItems1 > tr:nth-child("+n+") > td:nth-child(4)")
            stock_pice_updown2 = stock_pice_updown_list2[0].text

            result.append([stock_name]+[stock_price]+[stock_pice_updown1]+[stock_pice_updown2])
        except:
            continue
    
    return

def main():
    result= []
    check = 0
    print('stock crawling >>>>>>>>>>>>>>>>>>>>>>>>') 
    Stock_crawling(result)
    print(result)
    CB_tbl = pd.DataFrame(result,columns =('name','price','updown','updown(%)')) 
    CB_tbl.to_csv('./Stock_crawling.csv', encoding = 'cp949', mode = 'w',index = True)

main()
