from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import Database
import atexit

app = Flask(__name__)
db = Database()

# 애플리케이션 종료 시 DB 연결 종료
atexit.register(db.close)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fruit = request.form.get('fruit')
        
        if not fruit:
            return render_template('index.html', error="과일을 선택해주세요.")
        
        # 과일 선택 시 cnt 증가
        db.update_fruit_count(fruit)
        return redirect(url_for('history'))  # history 페이지로 이동

    return render_template('index.html')

@app.route('/history')
def history():
    try:
        records = db.get_fruit_data()
        data = {"labels": [], "counts": []}
        #print(data)
        for record in records:
            data["labels"].append(record["name"])
            data["counts"].append(record["cnt"])
        #print(data)
        chart_data = str(data)
        #print(chart_data)
        '''
        chart_data = str(jsonify(data))
        print(chart_data)
        '''
        return render_template('history.html',chart_data=data)
    
    except Exception as e:
        print(f"Error fetching chart data: {e}")
        chart_data = {"labels": [], "counts": []}
        return render_template('history.html',chart_data=chart_data,error=e)
'''
@app.route('/chart-data')
def chart_data():
    """차트에서 사용할 과일 데이터를 JSON 형태로 반환"""
    try:
        records = db.get_fruit_data()
        data = {"labels": [], "counts": []}
        
        for record in records:
            data["labels"].append(record["name"])
            data["counts"].append(record["cnt"])

        return jsonify(data)
    
    except Exception as e:
        print(f"Error fetching chart data: {e}")
        return jsonify({"labels": [], "counts": []})
'''
if __name__ == '__main__':
    app.run(debug=True)
