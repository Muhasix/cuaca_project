# 🌤️ Dashboard Cuaca Indonesia

Dashboard Streamlit yang menampilkan data cuaca real-time dari berbagai kota di Indonesia. Data diambil dari API OpenWeatherMap dan disimpan otomatis ke PostgreSQL, dengan visualisasi interaktif menggunakan **Altair**.

![Dashboard Screenshot](screenshot.png)

---

## 🚀 Fitur Utama

- ✅ Data suhu dan kelembapan real-time dari banyak kota
- 🔁 Auto-refresh setiap 60 detik
- 📊 Grafik interaktif (Altair): suhu, kelembapan, dan rata-rata harian
- 🗂️ Filter multi-kota langsung dari UI
- 📥 Data disimpan otomatis ke PostgreSQL via script
- 🧠 Cache dan optimisasi query
- 🕒 Otomatisasi lewat cron
- 🔐 Keamanan API key melalui `.env`

---

## 🧰 Teknologi

- [Python](https://python.org)
- [Streamlit](https://streamlit.io)
- [PostgreSQL](https://www.postgresql.org)
- [Altair](https://altair-viz.github.io)
- Pandas, SQLAlchemy, psycopg2, python-dotenv

---

## 📂 Struktur Folder

```

cuaca\_project/
├── dashboard/
│   └── app.py              # Aplikasi Streamlit
├── scripts/
│   └── fetch\_data.py       # Ambil data dari API & simpan ke DB
├── logs/
│   └── fetch.log           # Logging otomatisasi
├── .env                    # API key (tidak di-commit)
├── requirements.txt
├── README.md
└── screenshot.png

````

---

## ⚙️ Instalasi & Setup

### 1. Clone & buat virtual environment

```bash
git clone https://github.com/Muhasix/cuaca_project.git
cd cuaca_project
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
````

### 2. Buat file `.env`

```env
OPENWEATHER_API_KEY=masukkan_api_key_anda
```

### 3. Setup PostgreSQL

```sql
-- Masuk ke PostgreSQL:
sudo -u postgres psql

-- Jalankan:
CREATE USER cuaca_user WITH PASSWORD 'cuaca_pass';
CREATE DATABASE cuaca_db OWNER cuaca_user;
GRANT ALL PRIVILEGES ON DATABASE cuaca_db TO cuaca_user;
\q
```

### 4. Jalankan script ambil data

```bash
python scripts/fetch_data.py
```

### 5. Jalankan dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🔁 Otomatisasi (Cron)

Edit crontab:

```bash
crontab -e
```

Tambahkan:

```bash
*/30 * * * * /home/username/projects/cuaca_project/env/bin/python /home/username/projects/cuaca_project/scripts/fetch_data.py >> /home/username/projects/cuaca_project/logs/cron.log 2>&1
```

---

## 🔒 Keamanan

Pastikan `.env` dan `logs/` **masuk dalam `.gitignore`**:

```
.env
logs/
```

---

## 📃 Lisensi

MIT License – Bebas digunakan dan dimodifikasi.

---

## 🙋 Kontribusi

Saran, issue, dan pull request sangat terbuka!