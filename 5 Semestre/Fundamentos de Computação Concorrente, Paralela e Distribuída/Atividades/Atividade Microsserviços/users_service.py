from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def get_users():
    return jsonify([
        {"id": 1, "nome": "Ana"},
        {"id": 2, "nome": "Bruno"},
        {"id": 3, "nome": "Carla"}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
