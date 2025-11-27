from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="meu-banco",
    database="mensagensdb",
    user="usuario",
    password="senha123"
)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS mensagens (id SERIAL PRIMARY KEY, texto TEXT);")
conn.commit()

@app.route('/mensagem', methods=['POST'])
def add_msg():
    texto = request.json.get('texto')
    cur.execute("INSERT INTO mensagens (texto) VALUES (%s);", (texto,))
    conn.commit()
    return jsonify({"status": "mensagem salva"}), 201

@app.route('/mensagens', methods=['GET'])
def get_msgs():
    cur.execute("SELECT * FROM mensagens;")
    data = cur.fetchall()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
