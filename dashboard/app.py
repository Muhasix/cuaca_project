import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine
import time
import os
from dotenv import load_dotenv

# Muat file .env DB_CONFIG
load_dotenv()

# --- Konfigurasi koneksi database PostgreSQL ---
DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD")
}

# Buat URL koneksi SQLAlchemy
db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
engine = create_engine(db_url)

# --- Konfigurasi halaman Streamlit ---
st.set_page_config(page_title="Dashboard Cuaca", layout="wide")
st.title("🌤️ Dashboard Cuaca Indonesia")

# Interval refresh otomatis (detik)
REFRESH_INTERVAL = 60
countdown = st.empty()  # Untuk menampilkan hitung mundur

# --- Fungsi ambil data dari database (dengan cache & TTL) ---
@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data():
    query = "SELECT * FROM cuaca ORDER BY waktu DESC LIMIT 500"
    df = pd.read_sql(query, engine)
    return df

# Ambil data
data = load_data()

# --- Jika data tidak tersedia ---
if data.empty:
    st.warning("Data belum tersedia.")
else:
    # --- Pilihan kota dinamis ---
    kota_terpilih = st.multiselect(
        "Pilih kota:",
        options=sorted(data['kota'].unique()),
        default=sorted(data['kota'].unique())
    )

    # Filter data berdasarkan kota yang dipilih
    data_filtered = data[data['kota'].isin(kota_terpilih)]

    # Tampilkan tabel data mentah
    st.dataframe(data_filtered, use_container_width=True)

    # Urutkan data berdasarkan waktu naik (penting untuk grafik)
    sorted_data = data_filtered.sort_values("waktu")

    # --- Grafik Suhu per Kota (Altair) ---
    st.subheader("🌡️ Grafik Suhu Terbaru")
    chart_suhu = (
        sorted_data.sort_values("waktu", ascending=False)
        .groupby("kota", group_keys=False)
        .head(20)
        .sort_values("waktu")
    )

    suhu_chart = alt.Chart(chart_suhu).mark_line(point=True).encode(
        x=alt.X("waktu:T", title="Waktu"),
        y=alt.Y("suhu:Q", title="Suhu (°C)"),
        color="kota:N",
        tooltip=["waktu:T", "kota:N", "suhu:Q"]
    ).properties(width="container", height=300)

    st.altair_chart(suhu_chart, use_container_width=True)

    # --- Grafik Kelembapan per Kota (Altair) ---
    st.subheader("💧 Grafik Kelembapan Terbaru")
    chart_kelembapan = (
        sorted_data.sort_values("waktu", ascending=False)
        .groupby("kota", group_keys=False)
        .head(20)
        .sort_values("waktu")
    )

    kelembapan_chart = alt.Chart(chart_kelembapan).mark_line(point=True).encode(
        x=alt.X("waktu:T", title="Waktu"),
        y=alt.Y("kelembapan:Q", title="Kelembapan (%)"),
        color="kota:N",
        tooltip=["waktu:T", "kota:N", "kelembapan:Q"]
    ).properties(width="container", height=300)

    st.altair_chart(kelembapan_chart, use_container_width=True)

    # --- Grafik Rata-Rata Suhu Harian ---
    st.subheader("📈 Rata-Rata Suhu Harian per Kota")
    daily_avg = sorted_data.copy()
    daily_avg['tanggal'] = pd.to_datetime(daily_avg['waktu']).dt.date

    avg_per_day = daily_avg.groupby(['tanggal', 'kota'])['suhu'].mean().reset_index()

    rata2_chart = alt.Chart(avg_per_day).mark_line(point=True).encode(
        x=alt.X("tanggal:T", title="Tanggal"),
        y=alt.Y("suhu:Q", title="Rata-rata Suhu (°C)"),
        color="kota:N",
        tooltip=["tanggal:T", "kota:N", "suhu:Q"]
    ).properties(width="container", height=300)

    st.altair_chart(rata2_chart, use_container_width=True)

# --- Hitung mundur untuk auto-refresh ---
with st.empty():
    for i in range(REFRESH_INTERVAL, 0, -1):
        countdown.markdown(f"🔄 Auto-refresh dalam {i} detik...")
        time.sleep(1)
    st.rerun()
