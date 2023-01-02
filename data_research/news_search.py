# -*- coding: utf-8 -*-

import json
import pandas.io.sql as pSql
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os
import sys
import urllib.request

# 데이터 수집 레벨 2
CLIENT_ID = "09R0nErlhLWC7k_vvnzn"
CLIENT_SECRET = "RSD6YSNMJB"
NAVER_NEWS_QUERY_URL = 'openapi.naver.com/v1/search/news.json'

def get_search_news(keyword: str, dp_cnt=20, sort='date') -> list:
  '''
    검색어를 넣어서 네이버 뉴스를 수집해서 가져온다
    검색할때 20개 가져오고, 최신순으로 가져온다 => 단 변경가능하다(외부조정가능)
      Args
        keyword `str` : 검색어
        ...
      Returns
        ...
  '''
  # 키워드 인자값을 인코딩 변환에 삽입
  encText = urllib.parse.quote(keyword)
  # 파라미터 구성 : 키=값&키=값&키=값 <- http에서 GET 방식으로 데이터 전송시 포멧
  PARAM = f'display={dp_cnt}&sort={sort}&query={encText}'  # 구조가 보인다
  url = f"https://{NAVER_NEWS_QUERY_URL}?{PARAM}"  # https 프로토콜 구조

  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id", CLIENT_ID)
  request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
  response = urllib.request.urlopen(request)
  rescode = response.getcode()
  if(rescode == 200):
    tmp = json.load(response)
    #print( tmp['items'] )
    return tmp.get('items')
  else:
    # 단 통신 오류등의 문제라면 로그 처리
    return []

  pass

if __name__ == '__main__':
  tmp = get_search_news('2023', dp_cnt=5)
  print(tmp)

# 데이터 클리닝 작업 
pattern = [('<b>', ''), ('</b>', ''), ('&quot;', '"'),('&apos;', "'"), ('&amp;', '&')]

def clean_str_ex(ori_txt, pattern):

  while pattern:
    old_str, new_str = pattern.pop()  # 뒤에서 하나씩 제거하여 리턴
    #print( old_str, new_str )
    ori_txt = ori_txt.replace(old_str, new_str)

  return ori_txt

newDatas = [{'tit': clean_str_ex(n.get('title'),  pattern.copy()),
             'desc': clean_str_ex(n['description'],  pattern[:]),
             'date': clean_str_ex(n.get('pubDate'),  pattern[:]),
             } for n in tmp]

# 데이터 중간 변환
df = pd.DataFrame.from_dict(newDatas)

# 데이터베이스에 적제
ip = '127.0.0.1'  # or 'localhost'
id = 'root'      # 사용자 계정
pw = '12341234'  # 계정 비밀번호
port = 3306      # 포트는 1 ~ 65525 번 (2^31 - 1)
dbname = 'news_data_db'  # 접속하고자 하는 데이터베이스명
table = 'tbl_news'     # 뉴스를 저장하는 테이블명
protocal = 'mysql+pymysql'  # 통신규약, 상호간 통신하는 규칙을 정한것

db_url = f'{protocal}://{id}:{pw}@{ip}:{port}/{dbname}'
engine = create_engine(db_url, encoding='utf8')
conn = engine.connect()
df.to_sql(name=table, con=conn, if_exists='append', index=False)
conn.close()

