import os
import pandas as pd
from glob import glob

# Folder input dan output
raw_dir = "data/raw"
processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

# Ambil file terbaru
raw_files = sorted(glob(f"{raw_dir}/cuaca_*.csv"), reverse=True)
if not raw_files:
    print("❌ Tidak ada file data mentah di folder data/raw/")
    exit()

latest_file = raw_files[0]
print(f"📂 Membaca data dari: {latest_file}")
df = pd.read_csv(latest_file)

# Pembersihan dasar
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Ubah format waktu (jika perlu)
df['waktu'] = pd.to_datetime(df['waktu'])

# Simpan hasil
output_file = os.path.join(processed_dir, "cuaca_bersih.csv")
df.to_csv(output_file, index=False)
print(f"✅ Data bersih disimpan ke: {output_file}")
