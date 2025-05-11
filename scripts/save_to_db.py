import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Muat file .env
load_dotenv()

# Konfigurasi koneksi
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("PGPASSWORD")
DB_HOST = os.getenv("PGHOST")
DB_PORT = os.getenv("PGPORT")

# Baca data dari CSV
csv_file = "data/processed/cuaca_bersih.csv"
df = pd.read_csv(csv_file)

# Buat koneksi ke database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Koneksi ke database berhasil.")

    # Buat tabel jika belum ada
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cuaca (
        waktu TIMESTAMP PRIMARY KEY,
        suhu FLOAT,
        tekanan INT,
        kelembapan INT,
        cuaca TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Masukkan data ke tabel
    for _, row in df.iterrows():
        insert_query = sql.SQL("""
            INSERT INTO cuaca (waktu, suhu, tekanan, kelembapan, cuaca)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (waktu) DO NOTHING;
        """)
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    print("✅ Data berhasil disimpan ke database.")

except Exception as e:
    print("❌ Terjadi kesalahan:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
