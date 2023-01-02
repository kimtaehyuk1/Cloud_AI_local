# 기본 설치
# (base)$ pip install html5lib BeautifulSoup pandas sqlalchemy, pymysql

# 모듈 가져오기
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

# 메인 처리 함수
def main():
    # 1. 환율 메타 정보를 구한다
    infos = get_exchange_info()
    # 2. 환율 정보를 구한다
    raw_data = get_exchange_value( infos )
    # 3. 1번과 2번이 합쳐진 데이터를 DataFrame로 구성한다
    df = get_dataframe_from_raw_data( raw_data )    
    # 4. 3번의 결과물(DataFrame)을 DB에 입력한다
    get_insert_data( df )
    # 5. 프로세스 종료 (스케줄러 입장에서는 필수로 작성)
    import sys
    sys.exit(0)
    pass

def get_exchange_info():
  '''
    네이버 증권 > 환율 관련 사이트에서 환율 관련 메타 정보 추출하는 함수
    다른 사이트에서 동일하게 적용된다는 법이 없어서 입력을 넣지 않고, 고정했다
  '''
  target_site = 'https://finance.naver.com/marketindex/?tabSel=exchange'
  res = urlopen( target_site )
  soup = BeautifulSoup( res , 'html5lib' )

  exchange_date = soup.select_one('.date').text.strip()
  exchange_bank = soup.select_one('.standard').text.strip().split('은행')[0]
  exchange_round = soup.select_one('.round > em').text.strip()

  return { "exchange_date":exchange_date, 
           "exchange_bank":exchange_bank, 
           "exchange_round":exchange_round }

def get_exchange_value( infos=None ):
  target_site = 'https://finance.naver.com/marketindex/exchangeList.naver'
  res = urlopen( target_site )
  soup = BeautifulSoup( res , 'html5lib' )
  myData  = lambda tr, x:tr.select_one(x).text.strip()
  myData2 = lambda tr, x: float( tr.select_one(x).text.strip().replace(',','').replace('N/A','0') )
  return [ {
    'name'     : myData(tr, '.tit'),
    'std_rate' : myData2(tr, '.sale'),
    'cash_buy' : myData2(tr, 'td:nth-of-type(3)'),
    'rate'     : myData2(tr, 'td:nth-of-type(7)'),    
    'code'     : tr.select_one('.tit').a.get('href')[-6:-6+3],
    # 은행
    'bank'     : infos.get('exchange_date'),
    # 날짜
    'date'     : infos.get('exchange_bank'),
    # 회차
    'round'    : infos.get('exchange_round')
  } for tr in soup.select('tbody > tr') ]

def get_dataframe_from_raw_data( raw_data ):
    '''
        [ {}, {}, {}, ..] => DataFrame
    '''
    return pd.DataFrame.from_dict(raw_data)

def get_insert_data( df ):
    # 데이터베이스에 적제
    ip = '127.0.0.1'    # or 'localhost'
    id = 'root'         # 사용자 계정
    pw = '12341234'     # 계정 비밀번호
    port = 3306         # 포트는 1 ~ 65525 번 (2^31 - 1)
    dbname = 'news_data_db'     # 접속하고자 하는 데이터베이스명
    table = 'tbl_exchange'      # 환율을 저장하는 테이블명
    protocal = 'mysql+pymysql'  # 통신규약, 상호간 통신하는 규칙을 정한것

    db_url = f'{protocal}://{id}:{pw}@{ip}:{port}/{dbname}'
    engine = create_engine(db_url, encoding='utf8')
    conn = engine.connect()
    df.to_sql(name=table, con=conn, if_exists='append', index=False)
    conn.close()
    pass

# 프로그램 가동 -> 엔트리 포인트
if __name__ == '__main__':
    main()