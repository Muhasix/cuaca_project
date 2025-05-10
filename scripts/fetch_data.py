import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

# Konfigurasi API dan database
load_dotenv()  # ini otomatis cari file .env di root
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
KOTA = "Jakarta"
DB_CONFIG = {
    "host": "localhost",
    "dbname": "cuaca_db",
    "user": "cuaca_user",
    "password": "cuaca_pass"
}

def fetch_weather_data():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={KOTA}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()


    cuaca = {
        "waktu": datetime.now(),
        "kota": data.get("name"),
        "suhu": data["main"]["temp"],
        "kelembapan": data["main"]["humidity"],
        "cuaca": data["weather"][0]["description"]
    }
    return cuaca

def save_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cuaca (
            id SERIAL PRIMARY KEY,
            waktu TIMESTAMP,
            kota TEXT,
            suhu REAL,
            kelembapan REAL,
            cuaca TEXT
        );
    """)
    cur.execute("""
        INSERT INTO cuaca (waktu, kota, suhu, kelembapan, cuaca)
        VALUES (%s, %s, %s, %s, %s);
    """, (data["waktu"], data["kota"], data["suhu"], data["kelembapan"], data["cuaca"]))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        data = fetch_weather_data()
        save_to_db(data)
        print("✅ Data berhasil diambil dan disimpan.")
    except Exception as e:
        print("❌ Gagal:", e)
