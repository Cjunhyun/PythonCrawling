from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium import webdriver
import time

def Store_crawling(result):
    wd = webdriver.Chrome('chromedriver 디렉토리 위치')
    
    for i in ["16","17","18"]:
        #교촌치킨 성남시 매장은 3부분으로 나눠져있다(분당구, 수정구, 중원구)
        
        time.sleep(2) #웹페이지 연결할 동안 1초 대기 
        url = "https://www.kyochon.com/shop/domestic.asp?sido1=9&sido2="+ i + "&txtsearch="
        wd.get(url)
        html = wd.page_source
        soupCB1 = BeautifulSoup(html, 'html.parser')
        time.sleep(2)

        try:
            
            #매장개수 확인   
            store_num = soupCB1.select("span.store_item > strong")
            store_num = len(store_num)

            #매장개수 만큼 for문을 통해 정보 출력
            for i in range(store_num):

                #매장 이름
                store_name_list = soupCB1.select("span.store_item > strong")
                store_name = store_name_list[i].string

                #매장 정보
                store_info = soupCB1.select("span.store_item > em")
                one_store_info = store_info[i].text.strip().split('\n') #한개 매장 가져와서 리스트화
                one_store_info = [text.replace('\t', '') for text in one_store_info] #리스트에 '\t' 제거
                one_store_ad = one_store_info[0] #매장 주소
                one_store_ph = one_store_info[2] #매장 번호

                #result에 담기
                result.append([store_name]+[one_store_ad]+[one_store_ph])
        
        except:
            continue
    return

def main():
    result= []
    print('store crawling >>>>>>>>>>>>>>>>>>>>>>>>') 
    Store_crawling(result)
    print(result)
    CB_tbl = pd.DataFrame(result,columns =('store','address','phone')) 
    CB_tbl.to_csv('./store.csv', encoding = 'cp949', mode = 'w',index = True)

main()