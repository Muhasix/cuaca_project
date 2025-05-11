# 🌤️ Dashboard Cuaca Indonesia

[![Live](https://img.shields.io/website?url=https://cuacaproject1.up.railway.app&label=Dashboard&style=flat-square)](https://cuacaproject1.up.railway.app)
[![GitHub last commit](https://img.shields.io/github/last-commit/Muhasix/cuaca_project?style=flat-square)](https://github.com/Muhasix/cuaca_project)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://www.python.org/)

---

## 🚀 Fitur

- Ambil data cuaca otomatis dari OpenWeatherMap API
- Mendukung multi-kota: Jakarta, Bandung, Surabaya, dll.
- Simpan data ke PostgreSQL (lokal & Railway)
- Dashboard real-time dengan auto-refresh
- Otomatisasi fetch via cron di Railway

---

## 🖥️ Tampilan

![screenshot](screenshot.png)

---

## 🗂️ Struktur Proyek

<details>
<summary>📁 Klik untuk lihat</summary>

```

cuaca\_project/
├── dashboard/
│   └── app.py                  # Dashboard Streamlit
├── data/                       # (Opsional jika pakai CSV)
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── fetch\_data.py           # Ambil data cuaca ke DB
│   └── migrate\_to\_railway.py   # Migrasi manual dari lokal ke cloud
├── tools/
│   └── migrate\_to\_railway.py   # Bisa dipindah ke sini
├── .env                        # Env lokal (diabaikan Git)
├── migrate.env                 # Env Railway (jangan di-commit)
├── requirements.txt
├── .gitignore
└── README.md

````

</details>

---

## ⚙️ Instalasi Lokal

1. Clone repo:
```bash
git clone https://github.com/Muhasix/cuaca_project.git
cd cuaca_project
````

2. Buat virtual environment & aktifkan:

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependency:

```bash
pip install -r requirements.txt
```

4. Buat file `.env` dan isi:

```env
OPENWEATHER_API_KEY=your_api_key
PGHOST=localhost
PGDATABASE=cuaca_db
PGUSER=cuaca_user
PGPASSWORD=cuaca_pass
PGPORT=5432
```

5. Jalankan dashboard:

```bash
streamlit run dashboard/app.py
```

---

## ☁️ Deployment di Railway

* Setup PostgreSQL dan Streamlit di Railway
* Tambahkan variabel `.env` di Railway Environment tab
* Gunakan **Pre-deploy command** untuk `fetch_data.py`
* Gunakan **Cron Schedule** untuk auto-refresh data

---

## 📦 Migrasi Data Lokal ke Railway (opsional)

1. Siapkan `migrate.env`:

```env
PGHOST=your_railway_host
PGPORT=your_railway_port
PGUSER=postgres
PGPASSWORD=your_password
PGDATABASE=railway
```

2. Jalankan migrasi dari lokal:

```bash
python scripts/migrate_to_railway.py
```

---

## 📄 Lisensi

MIT License — bebas digunakan, dimodifikasi, dan dikembangkan.

---

Sukses deploy? ✨ Update link dashboard-nya ya!
