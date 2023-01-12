import joblib
import re

def predict_lang_type(src):
    # 모델로드 -> law_text -> 전처리 -> 데이터인코딩 -> 모델 넣어서 예측수행
    # 1. 모델로드
    model = joblib.load('./web/lang_predic_service/model/lang_predict.ml')
     # 이 모델은 코랩에서 다 훈련시킨거를 받아만 온것이다.
     # 코랩에서 훈련시킨 clf을 joblib.dump해서 파일로 만들고 그거 다운후 Copy Relative path 해서 경로 들고와 맨앞 ./ 붙이고 \를 /로 바꿔서 정의
    print(model)
    # 2. src -> 전처리 -> 데이터인코딩 -> 예측에 사용될 데이터 형태로 처리
    data = encode_freqs_data(src)
    # 3. 예측
    y_pred = model.predict(data)
    print(y_pred[0])
    # 4. 예측값을 한국어로 표기
    targets = joblib.load('./web/lang_predic_service/model/lang.label')
    print(targets[y_pred[0]])  


    return {'lang':targets[y_pred[0]]}


def encode_freqs_data(src):
    # 이함수는 사용자가 입력한 문자열을 받아서 전처리 -> 데이터인코딩 -> [[빈도값,....]]이렇게 리턴하는 함수
    STD_IDX = ord('a')

    text = src.lower()
    p = re.compile('[^a-z]*') 
    text = p.sub('',text) 
    counts = [0]*26 
    for w in text:  
        counts[ ord(w) - STD_IDX ] += 1
    total_counts = sum(counts) # len(text) 와 같은거다
    count_norms = list(map(lambda x:x/total_counts,counts))

    return [count_norms] 