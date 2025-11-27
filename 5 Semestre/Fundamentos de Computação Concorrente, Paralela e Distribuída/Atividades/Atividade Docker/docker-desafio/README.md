# Desafio: Aplicação Web + Banco de Dados em Docker

## Objetivo

Criar e executar uma aplicação web Python (Flask) que se conecta a um banco de dados **PostgreSQL**, utilizando **contêineres Docker**.

---

## Descrição do Desafio

Você deve construir **dois contêineres**:

1. Um contêiner rodando uma **API Flask** (backend).
2. Um contêiner rodando o **PostgreSQL** (banco de dados).

A aplicação deve permitir inserir e listar mensagens salvas no banco via endpoints REST.

---

## Estrutura do Projeto

```
docker-desafio/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

---

## Passos a seguir

### **1. Criar o banco de dados**

Execute um contêiner do PostgreSQL:

```bash
docker run -d   --name meu-banco   -e POSTGRES_USER=usuario   -e POSTGRES_PASSWORD=senha123   -e POSTGRES_DB=mensagensdb   postgres:15
```

Crie uma **rede Docker** para comunicação:

```bash
docker network create minha-rede
docker network connect minha-rede meu-banco
```

---

### **2. Criar a aplicação Flask**

#### **Arquivo: `requirements.txt`**

```
flask
psycopg2-binary
```

#### **Arquivo: `app.py`**

```python
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
```

---

### **3. Criar o Dockerfile**

**Arquivo: `Dockerfile`**

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

---

### **4. Construir e executar**

```bash
docker build -t flask-db-app ./app
docker run -d --name minha-api --network minha-rede -p 5000:5000 flask-db-app
```

---

### **5. Testar a aplicação**

Enviar uma nova mensagem:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"texto":"Olá Docker!"}' http://localhost:5000/mensagem
```

Listar mensagens:

```bash
curl http://localhost:5000/mensagens
```
