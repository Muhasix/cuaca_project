Berikut adalah versi **lengkap dan utuh** dari `README.md` untuk proyek cuaca Anda, disusun rapi dan siap langsung dipakai:

---

````markdown
# 🌤️ Cuaca Project - Dashboard Cuaca Indonesia

Proyek ini menampilkan data cuaca real-time dari beberapa kota besar di Indonesia. Data diambil dari [OpenWeather API](https://openweathermap.org/api), disimpan ke PostgreSQL, dan divisualisasikan dalam dashboard interaktif menggunakan Streamlit.

---

## 📌 Fitur

- 🔄 Pengambilan data cuaca otomatis dari berbagai kota (Jakarta, Bandung, Surabaya, Yogyakarta, Medan)
- 🗃️ Penyimpanan data historis ke PostgreSQL
- 📊 Visualisasi data dalam bentuk tabel dan grafik (suhu & kelembapan)
- 🕒 Auto-refresh dashboard untuk update data terbaru
- 🧩 Otomatisasi pengambilan data via cron job

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/cuaca_project.git
cd cuaca_project
````

### 2. Buat dan Aktifkan Virtual Environment

```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

---

## 🔐 Konfigurasi API Key

Buat file `.env` di direktori utama proyek:

```
OPENWEATHER_API_KEY=masukkan_api_key_anda_di_sini
```

Tambahkan juga file `.env` ke `.gitignore` agar tidak ikut di-push ke GitHub:

```
.env
```

---

## 🗃️ Setup PostgreSQL

### 1. Buat user dan database

Masuk ke shell PostgreSQL:

```bash
sudo -u postgres psql
```

Lalu jalankan:

```sql
CREATE USER cuaca_user WITH PASSWORD 'cuaca_pass';
CREATE DATABASE cuaca_db OWNER cuaca_user;
GRANT ALL PRIVILEGES ON DATABASE cuaca_db TO cuaca_user;
\q
```

---

## 🔁 Jalankan Pengambilan Data Manual

Untuk mencoba menjalankan pengambilan data secara manual:

```bash
python scripts/fetch_data.py
```

Jika berhasil, data akan disimpan ke tabel `cuaca` di database `cuaca_db`.

---

## 📺 Jalankan Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard akan terbuka di browser dan menampilkan data cuaca terbaru secara interaktif.

---

## ⏰ Otomatisasi dengan Cron (Linux)

Buka crontab:

```bash
crontab -e
```

Tambahkan baris berikut untuk menjalankan setiap 5 menit:

```
*/5 * * * * /home/username/projects/cuaca_project/env/bin/python /home/username/projects/cuaca_project/scripts/fetch_data.py >> /home/username/projects/cuaca_project/logs/cron.log 2>&1
```

Pastikan direktori `logs/` sudah dibuat.

---

## 🧾 Struktur Folder

```
cuaca_project/
├── dashboard/
│   └── app.py               # Streamlit dashboard
├── logs/
│   └── cron.log             # Log hasil cron job
├── scripts/
│   └── fetch_data.py        # Script fetch dan simpan cuaca
├── .env                     # File rahasia API key
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📸 Screenshot

Tambahkan screenshot dashboard Anda (opsional):

```
![Dashboard Cuaca](screenshot.png)
```

---

## 🔒 Keamanan

* Pastikan `.env` **tidak pernah** di-commit ke GitHub.
* Gunakan `.gitignore` untuk menghindari kebocoran API key.

---

## 📝 Lisensi

Proyek ini bebas digunakan untuk pembelajaran dan pengembangan pribadi. Tidak untuk penggunaan komersial tanpa izin eksplisit.

---

## 🙌 Kontribusi

Pull request, issue, dan masukan sangat diterima! Jangan ragu untuk fork dan mengembangkan.

---

```

