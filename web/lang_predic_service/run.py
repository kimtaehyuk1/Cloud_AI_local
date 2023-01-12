
# 머신러닝 모델을 제공받아서 언어 감지 서비스를 구현

from flask import Flask, render_template, jsonify, request
from model import predict_lang_type

app = Flask(__name__)

@app.route('/')
def home():
    # html 파일을 랜더링해서 응답하겠다.
    # html 파일을 읽고, 데이터가 전달되면 버무려서 동적으로 html을 변형하여 응답처리 한다.
    return render_template('index.html')

# 텍스트 데이터를 받아서 예측후 응답하는 URL 구성
# 404 : 해당 페이지가 없다 -> url을 라우팅하지 않았다., url이 오타
# 405 : method not allow -> 그 주소가 있긴 하는데, 요청한 메소드가 아닌데?
# 아무것도 표현하지 않으면 GET방식이 구현된것
@app.route('/predict', methods=['POST'])  # 아까 클라이언트 쪽에서 post로 보냇으니까 여기서도 메소드가 post여야함.
def predict():
    # 1. 사용자가 보낸 데이터 추출(프런트에서 전송한 내용을 백엔드에서 획득)
    # 사용자의 모든 요청은 request라는 객체를 타고 들어온다(데이터도 포함)
    law_text = request.form.get('text')
    print(law_text)

    # 2. 모델로드 -> law_text -> 전처리 -> 데이터인코딩 -> 모델 넣어서 예측수행
    y_pred = predict_lang_type(law_text)
    print(y_pred)



    # jsonify(파라미터)
    # 파라미터는 {'키':'값'} or [{'키':'값'},...] 가능 -> json처리 되서 클라이언트에서 json형태로 받는다
    return jsonify(y_pred) # {'lang':'영어'}


if __name__ == '__main__': 
    # app.run()  실제 서비스 할때는 소스가 수정되도 바로 반영안되게 처리
    # 개발시-디버깅 모드로 실행
    app.run(debug=True)


