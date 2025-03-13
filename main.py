from utils.extract import extract_data
from utils.transform import clean_and_transform
from utils.load import load_to_postgres

# URL koneksi PostgreSQL
db_url = "postgresql://developer:tia2209116043@localhost:5432/fashion_product"

# 1. 📊 Ambil data dari website
data = extract_data()

# 2. 🔄 Bersihkan dan transformasi data
cleaned_df = clean_and_transform(data)

# 3. 📥 Muat data ke PostgreSQL
load_to_postgres(cleaned_df, db_url)

print("🎉 Proses ETL selesai!")
