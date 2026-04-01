# 🚀 Step 5：HTTPS対応（Let's Encrypt + Certbot）

ここでやること：

- 無料SSL証明書を取得
- NginxでHTTPS対応
- 自動更新設定

---

# 🧭 完成イメージ

```
https://your-domain.com
        ↓
   Nginx（SSL終端）
        ↓
   Flask（Gunicorn）
        ↓
   PostgreSQL
```

---

# ⚠️ 重要前提（ここ超大事）

HTTPSは👇が必要です：

### ✅ 必須条件

- ドメイン（例：example.com）
- VPS / サーバー（インターネット公開）
- ポート80/443開放

👉 ローカル（localhost）ではできません

---

# 🧩 構成追加

今回追加するコンテナ：

- `certbot`（証明書取得）

---

# 📁 ディレクトリ構成（最終）

```
my-flask-app/
├── nginx/
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
├── certbot/
│   └── www/
```

---

# 🧩 ① Nginx設定（HTTP + HTTPS対応）

## 📄 nginx/conf.d/default.conf

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://web:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

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

  db:
    image: postgres:15
    env_file:
      - .env
    volumes:
      - pgdata:/var/lib/postgresql/data

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./certbot/www:/var/www/certbot
      - ./certbot/conf:/etc/letsencrypt
    depends_on:
      - web

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/www:/var/www/certbot
      - ./certbot/conf:/etc/letsencrypt

volumes:
  pgdata:
```

---

# 🧾 ③ 証明書取得コマンド

初回だけ実行👇

```bash
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d your-domain.com \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email
```

---

# ▶️ ④ 起動

```bash
docker compose up -d
```

---

# 🌐 確認

```
https://your-domain.com
```

👉 鍵マーク 🔒 が出れば成功！

---

# 🔁 ⑤ 自動更新（重要）

Let's Encryptは**90日で期限切れ**になります

---

## 🔄 更新コマンド

```bash
docker compose run --rm certbot renew
```

---

## ⏰ 自動化（cron）

```bash
0 3 * * * docker compose run --rm certbot renew && docker compose restart nginx
```

---

# 🎯 Step 5のゴール

- HTTPS化完了
- 実運用可能な構成

---

# 🔥 ここまで来たあなたは

正直かなりすごいです：

✅ Docker
✅ Flask
✅ Gunicorn
✅ PostgreSQL
✅ Nginx
✅ HTTPS

👉 **完全に実務レベルのWebバックエンド構成**

---

# 🚀 次にやるとさらに強い

余裕があれば👇

### 🔹 CI/CD（GitHub Actions）

→ pushで自動デプロイ

### 🔹 AWS / GCPデプロイ

→ 本当のクラウド運用

### 🔹 ログ管理（ELK / Loki）

→ 運用レベル

---

# 💬 最後に確認

ここまでで：

- ドメイン持ってる？
- VPS使う予定ある？

👉 もしまだなら
「ローカルでHTTPSっぽく試す方法」や
「おすすめVPS構成」も教えます 👍
