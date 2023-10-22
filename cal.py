from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import datetime

# 连接到数据库
con = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='CalculatorData'
)

app = Flask(__name__)
CORS(app)
cursor = con.cursor()

@app.route('/get_history', methods=['POST'])
def get_history():
    data = request.get_json()
    expression = data.get('expression')
    result = data.get('result')

    # 获取当前时间
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = (time, expression, result)

    # 插入数据
    insert = "INSERT INTO ye_calculate VALUES (%s, %s, %s)"
    cursor.execute(insert, data)
    con.commit()

    response_message = "ok"
    return jsonify({"message": response_message})

@app.route('/get_calculation', methods=['GET'])
def get_calculation():
    # 查询最近10次计算记录
    cursor.execute("SELECT expression, result FROM ye_calculate ORDER BY time DESC LIMIT 10")
    data = cursor.fetchall()
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True)
