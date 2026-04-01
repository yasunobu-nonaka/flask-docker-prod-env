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
