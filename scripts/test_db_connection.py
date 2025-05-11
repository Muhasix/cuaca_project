import psycopg2
import os
from dotenv import load_dotenv

# Muat file .env
load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    print("✅ Koneksi ke PostgreSQL berhasil.")
    conn.close()
except Exception as e:
    print("❌ Gagal koneksi ke database:")
    print(e)
