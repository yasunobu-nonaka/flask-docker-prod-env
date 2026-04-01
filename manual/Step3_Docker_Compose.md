# 🚀 Step 3：PostgreSQL + Docker Compose構成

ここでは👇をやります：

- PostgreSQLコンテナ追加
- FlaskからDB接続
- `.env`で環境変数管理
- Docker Composeでまとめて起動

---

# 🧭 完成イメージ（今回作る構成）

```
docker-compose.yml

services:
  web  ← Flask + Gunicorn
  db   ← PostgreSQL
```

---

# 📁 ディレクトリ構成（更新）

```
my-flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

# 🧩 ① requirements.txt 追加

```txt
Flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

👉 PostgreSQL接続用

---

# 🔐 ② .env を作成

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb

DATABASE_URL=postgresql://postgres:password@db:5432/mydb
```

---

## 💡 ポイント

- `db` → Docker Composeのサービス名（超重要）
- Flaskからは「db」に接続する

---

# 🐳 ③ docker-compose.yml

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    restart: always
    env_file:
      - .env
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

# 🧠 ポイント解説

## depends_on

```yaml
depends_on:
  - db
```

👉 DBを先に起動

（※ただし「完全に準備完了」までは待たない → 実務では対策必要）

---

## volumes

```yaml
pgdata:
```

👉 DBデータを永続化（超重要）

---

# 🐍 ④ app.py を少し強化

まずは接続テストだけやります👇

```python
from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

@app.route("/")
def hello():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    cur.close()
    conn.close()

    return f"Hello! DB version: {db_version}"

if __name__ == "__main__":
    app.run(debug=True)
```

---

# ▶️ ⑤ 起動

```bash
docker compose up --build
```

---

# 🌐 確認

```
http://localhost:8000
```

👉 こう出れば成功：

```
Hello! DB version: ('PostgreSQL 15.x ...',)
```

---

# ⚠️ よくあるエラー

## ❌ connection refused

👉 原因：

- DB起動前に接続してる

👉 対策（後でやる）：

- リトライ処理

---

## ❌ password authentication failed

👉 .envミス

---

## ❌ psycopg2エラー

👉 requirements.txt入れ忘れ

---

# 🎯 Step 3のゴール

- Flask ⇄ PostgreSQL接続成功
- Docker Composeで複数コンテナ管理

---

# 🔥 ここまで来たらもう中級者

正直ここまでできれば：

👉 「DockerでWebアプリ構築できます」と言えるレベル

---

# 🔜 次のステップ（かなり重要）

いよいよ👇

---

# 🌐 Step 4：Nginx（リバースプロキシ）

やること：

- Nginxコンテナ追加
- Gunicornの前に配置
- 本番っぽい構成にする

👉 ここで「完全に実務構成」になります

---

# 💬 まずここ確認

やってみて：

- ✅ DB接続できた
- ❌ エラー出た（そのまま貼ってOK）

教えてください 👍
次は**Nginx導入編**いきます。
