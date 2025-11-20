from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/orders')
def get_orders():
    users = requests.get('http://users_service:5001/users').json()
    return jsonify([
        {"order_id": 101, "user": users[0]},
        {"order_id": 102, "user": users[1]}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
