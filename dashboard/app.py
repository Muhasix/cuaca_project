import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

# Konfigurasi database PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "dbname": "cuaca_db",
    "user": "cuaca_user",
    "password": "cuaca_pass"
}

# Buat engine koneksi menggunakan SQLAlchemy
db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
engine = create_engine(db_url)

# Konfigurasi tampilan halaman
st.set_page_config(page_title="Dashboard Cuaca", layout="wide")
st.title("🌤️ Dashboard Cuaca Indonesia")

# Interval refresh dalam detik
REFRESH_INTERVAL = 60
countdown = st.empty()

# Fungsi ambil data terbaru dari database
@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data():
    query = "SELECT * FROM cuaca ORDER BY waktu DESC LIMIT 500"
    df = pd.read_sql(query, engine)
    return df

# Load data
data = load_data()

if data.empty:
    st.warning("Data belum tersedia.")
else:
    # Pilih kota
    kota_terpilih = st.multiselect(
        "Pilih kota:",
        options=sorted(data['kota'].unique()),
        default=sorted(data['kota'].unique())
    )

    # Filter berdasarkan kota
    data_filtered = data[data['kota'].isin(kota_terpilih)]

    # Tampilkan tabel data
    st.dataframe(data_filtered, use_container_width=True)

    # Urutkan berdasarkan waktu
    sorted_data = data_filtered.sort_values("waktu")

    # Grafik Suhu Terbaru
    st.subheader("🌡️ Grafik Suhu Terbaru")
    chart_suhu = sorted_data.groupby("kota").head(10)
    st.line_chart(chart_suhu.pivot(index="waktu", columns="kota", values="suhu"))

    # Grafik Kelembapan Terbaru
    st.subheader("💧 Grafik Kelembapan Terbaru")
    chart_kelembapan = sorted_data.groupby("kota").head(10)
    st.line_chart(chart_kelembapan.pivot(index="waktu", columns="kota", values="kelembapan"))

    # Grafik Rata-Rata Suhu Harian
    st.subheader("📈 Rata-Rata Suhu Harian per Kota")
    daily_avg = sorted_data.copy()
    daily_avg['tanggal'] = pd.to_datetime(daily_avg['waktu']).dt.date
    avg_per_day = daily_avg.groupby(['tanggal', 'kota'])['suhu'].mean().reset_index()
    st.line_chart(avg_per_day.pivot(index="tanggal", columns="kota", values="suhu"))

# Auto-refresh countdown
with st.empty():
    for i in range(REFRESH_INTERVAL, 0, -1):
        countdown.markdown(f"🔄 Auto-refresh dalam {i} detik...")
        time.sleep(1)
    st.rerun()
