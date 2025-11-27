from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# Redis host definido via variável de ambiente
redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route("/set", methods=["POST"])
def set_value():
    data = request.get_json()
    r.set(data["key"], data["value"])
    return jsonify({"message": "Valor salvo com sucesso!"})

@app.route("/get/<key>", methods=["GET"])
def get_value(key):
    value = r.get(key)
    if value:
        return jsonify({"key": key, "value": value})
    return jsonify({"error": "Chave não encontrada"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
