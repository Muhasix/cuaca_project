import requests
import psycopg2
from datetime import datetime
import os
import time
import logging
from dotenv import load_dotenv

# Muat file .env untuk API key dan DB_CONFIG
load_dotenv()

# Konfigurasi logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "fetch.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# API key dari file .env
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Daftar kota yang ingin diambil
KOTA_LIST = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Medan"]

# Konfigurasi PostgreSQL
DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD")
}


# Ambil data cuaca, dengan retry jika gagal
def fetch_weather_data(kota, retries=3, delay=3):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={API_KEY}&units=metric"

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or "main" not in data:
                raise ValueError(data.get("message", "Unknown error"))

            return {
                "waktu": datetime.now(),
                "kota": data.get("name"),
                "suhu": data["main"]["temp"],
                "kelembapan": data["main"]["humidity"],
                "cuaca": data["weather"][0]["description"]
            }

        except Exception as e:
            logging.warning(f"Gagal ambil data {kota} (percobaan {attempt}): {e}")
            time.sleep(delay)

    # Jika gagal semua percobaan
    logging.error(f"Gagal ambil data dari {kota} setelah {retries} percobaan.")
    return None

# Simpan ke database
def save_to_db(data_list):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cuaca (
            id SERIAL PRIMARY KEY,
            waktu TIMESTAMP NOT NULL,
            kota TEXT NOT NULL,
            suhu REAL,
            kelembapan REAL,
            cuaca TEXT
        );
    """)

    for data in data_list:
        cur.execute("""
            INSERT INTO cuaca (waktu, kota, suhu, kelembapan, cuaca)
            VALUES (%s, %s, %s, %s, %s);
        """, (data["waktu"], data["kota"], data["suhu"], data["kelembapan"], data["cuaca"]))

    conn.commit()
    cur.close()
    conn.close()

# Main script
if __name__ == "__main__":
    try:
        hasil = []
        for kota in KOTA_LIST:
            logging.info(f"Fetching: {kota}")
            data = fetch_weather_data(kota)
            if data:
                hasil.append(data)
                logging.info(f"✅ {kota}: Data berhasil diambil.")
            else:
                logging.error(f"❌ {kota}: Gagal mengambil data.")

        if hasil:
            save_to_db(hasil)
            logging.info("📦 Semua data berhasil disimpan ke database.")
            print("✅ Data berhasil disimpan.")
        else:
            logging.warning("⚠️ Tidak ada data yang berhasil diambil.")
            print("⚠️ Tidak ada data yang disimpan.")
    except Exception as e:
        logging.critical(f"Script error: {e}")
        print("❌ Gagal:", e)
