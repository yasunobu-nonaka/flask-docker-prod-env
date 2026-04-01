# 🧭 今回のゴール構成（最終形）

最終的にこれを作ります：

```
🌐 Browser
   ↓
🧱 Nginx（HTTPS）
   ↓
🐍 Flask（Gunicorn）
   ↓
🐘 PostgreSQL
```

さらに全部を👇で管理：

👉 **Docker Compose**

---

# 🚀 進め方（重要）

いきなり全部やると確実に詰むので、段階的にいきます👇

---

# ✅ Step 2：FlaskをDocker + Gunicornで動かす

👉 今回はここだけやります（まだNginx・DBなし）

---

# 📁 ディレクトリ構成（更新）

```
my-flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml（後で使う）
```

---

# 🧩 ① requirements.txtを更新

```txt
Flask==3.0.0
gunicorn==21.2.0
```

---

# 🐳 ② Dockerfileを作る

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

---

## 💡 ポイント解説

- `python:3.11-slim` → 軽量
- `gunicorn` → 本番サーバー
- `app:app` →
  👉 app.pyの中の `app` を指す

---

# 🐳 ③ ビルド

```bash
docker build -t flask-app .
```

---

# ▶️ ④ 起動

```bash
docker run -p 8000:8000 flask-app
```

---

# 🌐 確認

ブラウザ：

```
http://localhost:8000
```

👉 **Hello, Production World!** が出ればOK

---

# 🎯 Step 2のゴール

- FlaskがDockerで動く
- Gunicornで本番風に動く

---

# ⚠️ よくあるエラー

## ❌ ModuleNotFoundError

→ requirements.txtミス

---

## ❌ app:app が見つからない

→ app.pyの名前 or Flaskインスタンス名ミス

---

## ❌ ポートアクセスできない

→ `-p 8000:8000`忘れ

---

# 👉 次のステップ（予告）

ここまでできたら次👇

---

# 🔜 Step 3：Docker Compose + PostgreSQL

やること：

- PostgreSQLコンテナ追加
- FlaskからDB接続
- 環境変数導入（.env）

👉 一気に「実務っぽさ」が上がります

---

# 💬 次に進む前に

ここまでやって：

- 動いた ✅
- エラー出た ❌（内容貼ってOK）

教えてください 👍
そこから**DB接続フェーズ**に進みます。
