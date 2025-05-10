import streamlit as st
import pandas as pd
import psycopg2

# Konfigurasi database
DB_CONFIG = {
    "host": "localhost",
    "dbname": "cuaca_db",
    "user": "cuaca_user",
    "password": "cuaca_pass"
}

def load_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = "SELECT * FROM cuaca ORDER BY waktu DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Gagal mengambil data: {e}")
        return pd.DataFrame()

# Judul
st.title("Dashboard Cuaca Jakarta (Realtime via PostgreSQL)")

# Ambil data
df = load_data()

if not df.empty:
    # Konversi kolom waktu
    df["waktu"] = pd.to_datetime(df["waktu"])

    # Sidebar filter
    st.sidebar.header("Filter")

    # Filter kota
    kota_options = df["kota"].unique().tolist()
    kota_terpilih = st.sidebar.selectbox("Pilih Kota", kota_options)

    # Filter tanggal
    tanggal_awal = st.sidebar.date_input("Dari Tanggal", df["waktu"].min().date())
    tanggal_akhir = st.sidebar.date_input("Sampai Tanggal", df["waktu"].max().date())

    # Terapkan filter
    mask = (
        (df["kota"] == kota_terpilih) &
        (df["waktu"].dt.date >= tanggal_awal) &
        (df["waktu"].dt.date <= tanggal_akhir)
    )
    df_filter = df.loc[mask]

    # Tampilkan hasil
    st.subheader(f"Data Cuaca: {kota_terpilih}")
    st.dataframe(df_filter)

    st.subheader("Suhu dari waktu ke waktu")
    if not df_filter.empty:
        st.line_chart(df_filter.sort_values("waktu").set_index("waktu")["suhu"])
    else:
        st.info("Tidak ada data pada rentang waktu tersebut.")
else:
    st.warning("Data belum tersedia.")
