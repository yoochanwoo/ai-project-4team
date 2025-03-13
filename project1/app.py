from flask import Flask, render_template, request, redirect, url_for
from db import Database
import atexit # 애플리케이션 종료시 실행을 요청 (ex. DB연결 종료)

app = Flask(__name__)  # Flask 앱 초기화
db = Database()  # DB 초기화

# 애플리케이션 종료 시 DB 연결 종료
atexit.register(db.close)
# 조회
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
# 등록
@app.route('/fruits', methods=['POST'])
def add_fruit():
    try:
        name = request.form['name']  # 과일 이름
        
        # 데이터베이스에 과일 데이터 추가 (cnt 증가)
        success = db.save_bmi_record(name)
        
        if not success:
            return render_template('index.html', error="데이터 저장 중 오류가 발생했습니다.")
        
        return redirect(url_for('history'))  # 예외 처리
    except Exception as e:
        return render_template('index.html', error=f"오류 발생: {e}")

@app.route('/history')
def history():
    try:
        # 최근 과일 기록 10개 가져오기
        records = db.get_bmi_records()
        return render_template('history.html', records=records)
    
    except Exception as e:
        return render_template('history.html', error=f"오류 발생: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
