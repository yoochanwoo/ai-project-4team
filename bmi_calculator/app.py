# 사전 설치 : pip install flask pymysql ## 했음
from flask import Flask, render_template, request, redirect, url_for # 얘가 웹 url 만듦
from bmi import BMICalculator
from db import Database
import atexit

app = Flask(__name__)
db = Database()

# 애플리케이션 종료 시 DB 연결 종료
atexit.register(db.close)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
# index파일 웹페이지 구축하는 url
# get 방식이고 url은 공백

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        #request로 체중 신장값을 받음
        
        # 입력값 유효성 검사
        if weight <= 0 or height <= 0:
            return render_template('index.html', error="체중과 신장은 양수여야 합니다.")
        
        # BMI 계산
        calculator = BMICalculator(weight, height)
        result = calculator.get_result()
        
        # 데이터베이스에 저장
        db.save_bmi_record(weight, height, result["bmi"], result["category"])
        
        return render_template('result.html', 
                              bmi=result["bmi"], 
                              category=result["category"],
                              weight=weight,
                              height=height)
    except ValueError:
        return render_template('index.html', error="유효한 숫자를 입력해주세요.")
# 등록하고 계산하는 웹페이지 구축하는 url
# post 방식이고 url은 /calculate
# 계산이 되면 result.html에 weight, height, bmi = result["bmi"], category = result["category"]
# 오류가 생기면 index.html에 error를 보냄

@app.route('/history')
def history():
    # 최근 BMI 기록 10개 가져오기
    records = db.get_bmi_records(10)
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
# 기록 확인하는 웹페이지 구축하는 url
# get 방식(default)이고 url은 /history
# history.html에 records 를 보냄
    