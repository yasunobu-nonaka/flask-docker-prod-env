# 🚀 Step 4：Nginx（リバースプロキシ）を導入

ここでやること：

- Nginxコンテナ追加
- Flask（Gunicorn）の前に配置
- 外部公開はNginxのみ

---

# 🧭 完成イメージ（今回）

```
Browser
   ↓
Nginx（80番ポート）
   ↓
Flask（Gunicorn）
   ↓
PostgreSQL
```

👉 これがほぼ実務の基本構成です

---

# 📁 ディレクトリ構成（更新）

```
my-flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── nginx/
    └── nginx.conf
```

---

# 🧩 ① Nginx設定ファイル作成

## 📄 nginx/nginx.conf

```nginx
events {}

http {
    server {
        listen 80;

        location / {
            proxy_pass http://web:8000;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

---

## 💡 ポイント

- `web` → Flaskコンテナ名（超重要）
- `8000` → Gunicornポート

---

# 🐳 ② docker-compose.yml 更新

```yaml
version: "3.9"

services:
  web:
    build: .
    expose:
      - "8000"
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

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  pgdata:
```

---

# 🧠 重要ポイント

## 🔹 ports → nginxだけ

```yaml
ports:
  - "80:80"
```

👉 外部公開はNginxだけ

---

## 🔹 expose

```yaml
expose:
  - "8000"
```

👉 コンテナ内通信だけ許可（外部から見えない）

---

# ▶️ ③ 起動

```bash
docker compose down
docker compose up --build
```

---

# 🌐 確認

ブラウザ：

```
http://localhost
```

👉 今までと同じ画面が出れば成功

（※ ポート8000じゃないので注意）

---

# 🎯 Step 4のゴール

- Nginx経由でFlaskにアクセス
- 本番と同じ構成になる

---

# ⚠️ よくあるミス

## ❌ 502 Bad Gateway

原因：

- Flask起動してない
- ポート違う
- `web:8000`ミス

---

## ❌ nginx設定ミス

👉 スペルミス多い

---

# 🔥 ここまでで実務レベル到達

正直これ👇ができてます：

✅ Docker
✅ Flask
✅ Gunicorn
✅ PostgreSQL
✅ Nginx

👉 **完全に実務構成です**

---

# 🔜 次（最終段階）

いよいよ最後👇

---

# 🔐 Step 5：HTTPS対応（本番仕上げ）

やること：

- Let's Encrypt
- SSL証明書
- HTTPS化

---

# 💬 次に進む前に

ここ確認させてください：

- ✅ [http://localhost](http://localhost) で動いた
- ❌ エラー出た

教えてください 👍
次は**HTTPS化（ガチ本番）**いきます。
