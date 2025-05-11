# SAFE: Skrip ini hanya dijalankan manual saat migrasi lokal → Railway
# Tidak dipakai di deploy, cron, atau auto task

import psycopg2
import os
from dotenv import load_dotenv

# Load environment untuk Railway dari migrate.env
load_dotenv("migrate.env")

# Konfigurasi database lokal (langsung ditulis)
LOCAL_DB = {
    "host": "localhost",
    "dbname": "cuaca_db",
    "user": "cuaca_user",
    "password": "cuaca_pass",
    "port": "5432"
}

# Konfigurasi database Railway (dari migrate.env)
RAILWAY_DB = {
    "host": os.getenv("PGHOST"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "port": os.getenv("PGPORT", "5432")
}

def migrate_data():
    try:
        print("🔗 Menghubungkan ke database lokal...")
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cur = local_conn.cursor()

        print("🌐 Menghubungkan ke database Railway...")
        remote_conn = psycopg2.connect(**RAILWAY_DB)
        remote_cur = remote_conn.cursor()

        # Ambil data dari lokal
        local_cur.execute("SELECT waktu, kota, suhu, kelembapan, cuaca FROM cuaca")
        rows = local_cur.fetchall()
        print(f"📦 Menyalin {len(rows)} baris data...")

        # Buat tabel jika belum ada di Railway
        remote_cur.execute("""
            CREATE TABLE IF NOT EXISTS cuaca (
                id SERIAL PRIMARY KEY,
                waktu TIMESTAMP,
                kota TEXT,
                suhu REAL,
                kelembapan REAL,
                cuaca TEXT
            );
        """)

        # Insert data ke Railway
        for row in rows:
            remote_cur.execute("""
                INSERT INTO cuaca (waktu, kota, suhu, kelembapan, cuaca)
                VALUES (%s, %s, %s, %s, %s)
            """, row)

        remote_conn.commit()
        print("✅ Migrasi selesai!")

        # Tutup koneksi
        local_cur.close()
        local_conn.close()
        remote_cur.close()
        remote_conn.close()

    except Exception as e:
        print("❌ Gagal migrasi:", e)

if __name__ == "__main__":
    migrate_data()
