import pandas as pd
import sys
from bs4 import BeautifulSoup
from selenium import webdriver as wd
import time
import random


driver = wd.Chrome('C://Users//USER//Desktop//PY_PROJECTS//selenium_level4//chromedriver.exe')
def term_make(x, y): return random.randint(x, y)*0.1  # 0.1 ~ 0.9까지 나옴


# 모든 지점의 정보를 담는 그릇
starbucks_store_infos = list()

for sido_idx in range(1, 17+1):
    # 초기 진입 사이트 접속
    driver.get('https://www.starbucks.co.kr/store/store_map.do?disp=locale')
    time.sleep(1*5+term_make(1, 5))  # 5초는 깔고 함수로 0.1~0.9 더해서 난수 가미

    # 시도 선택
    # 이건 문자열 li:nth-child(1)여기가 1번이니까 서울이었다.
    css_sel = f'div.loca_step1_cont > ul > li:nth-child({sido_idx}) > a'
    si_do_a_tag = driver.find_element_by_css_selector(css_sel)
    si_do_a_tag.click()
    time.sleep(1*5+term_make(1, 5))

    # 전체 선택, 1번 멤버가 무조건 전체이다 -> 고정
    if sido_idx<17:
        css_sel = '#mCSB_2_container > ul > li:nth-child(1) > a'
        driver.find_element_by_css_selector(css_sel).click()
        time.sleep(1*5+term_make(1, 5))

    # 정보 추출 (셀레니움 방식과 뷰티풀수프 방식)
    # soup(DOM Tree) 생성
    src = driver.page_source  # 현재 페이지의 HTML 소스
    soup = BeautifulSoup(src, 'html5lib')

    # 정보추출
    starbucks_store_local_infos = [{
        'name': li.get('data-name'),  # 지점명, 속성값 추출 => 요소.get('속성이름')
        'lat': float(li.get('data-lat')),   # 위도 -> float()
        'long': float(li.get('data-long')),   # 경도 -> float()
        'code': li.get('data-code'),  # 지점코드
        'storecd': li.get('data-storecd'),                 # 관리코드(?)
        'addr': li.p.text.strip()[:len('1522-3232')*-1],   # 전화번호가 모두 동일하다
        # class는 속성값으로 뽑으면 리스트로 나온다(특징), pin_ 제거
        'spec': li.i.get('class')[0][len('pin_'):]
    } for li in soup.select('.quickSearchResultBoxSidoGugun > li')]

    # starbucks_store_infos에 starbucks_store_local_infos값 하나하나를 멤버로 추가한다. 우리는 리스트안 리스트말고 동급인 리스트안 딕셔너리 원함
    starbucks_store_infos.extend(starbucks_store_local_infos)  # 동등한 위치로 들어감

    print(f'{sido_idx}번 실행')
    #if sido_idx == 1:
    #    print(len(starbucks_store_infos))
    #    break

# csv에 저장
# [{},{},{}...] => DataFrame => csv저장
# df 생성

df = pd.DataFrame.from_dict(starbucks_store_infos)
df.to_excel('starbucks_store_full.xlsx', index=False)


# 브라우저 닫기
driver.close()
driver.quit()

#파이썬 파일에서 사용
sys.exit(0)
