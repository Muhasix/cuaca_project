import psycopg2

try:
    conn = psycopg2.connect(
        dbname="cuaca_db",
        user="cuaca_user",
        password="cuaca_pass",
        host="localhost",
        port="5432"
    )
    print("✅ Koneksi ke PostgreSQL berhasil.")
    conn.close()
except Exception as e:
    print("❌ Gagal koneksi ke database:")
    print(e)
