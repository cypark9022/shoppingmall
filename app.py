from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.shoppingmall                  # 'shoppingmall'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('shoppingmall.html')

## API 역할을 하는 부분
## POST 형식으로 입력된 데이터를 전송할 경우, DB에 딕셔너리 형태로 저장
@app.route('/orders', methods=['POST'])
def write_order():
    name_receive = request.form['name_give']
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # DB에 저장할 딕셔너리 
    order = {
       'name': name_receive,
       'amount': amount_receive,
       'address': address_receive,
       'phone' : phone_receive
    }

    db.orders.insert_one(order)

    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '주문이 완료되었습니다.'})


@app.route('/orders', methods=['GET'])
def read_order():
    # 모든 orders의 데이터 가져온 후 list로 변환
    orders = list(db.orders.find({},{'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})


@app.route('/delete', methods=['POST'])
def delete_tables():
    # orders collection의 모든 데이터를 삭제
    db.orders.remove({})
    return jsonify({'result': 'success', 'msg': '주문을 전체삭제 하였습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)