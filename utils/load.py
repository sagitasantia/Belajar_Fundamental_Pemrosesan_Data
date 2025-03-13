import pandas as pd
from sqlalchemy import create_engine, text

def load_to_postgres(data_bersih, db_url):
    try:
        engine = create_engine(db_url)

        # Validasi koneksi ke database
        with engine.connect() as con:
            print("✅ Koneksi ke database berhasil!")

            # Pastikan tabel tersedia
            create_table_query = text("""
                CREATE TABLE IF NOT EXISTS fashion_products (
                    id SERIAL PRIMARY KEY,
                    "Title" TEXT NOT NULL,
                    "Price" NUMERIC(10, 2) NOT NULL,
                    "Rating" NUMERIC(3, 2) NOT NULL,
                    "Colors" INTEGER NOT NULL,
                    "Size" TEXT NOT NULL,
                    "Gender" TEXT NOT NULL,
                    "Timestamp" TIMESTAMP NOT NULL
                );
            """)
            con.execute(create_table_query)
            print("✅ Tabel 'fashion_products' berhasil dicek atau dibuat.")

            # Validasi data yang dimuat
            print("🔎 Kolom di data:", data_bersih.columns.tolist())
            
            expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
            if not all(col in data_bersih.columns for col in expected_columns):
                raise ValueError("❌ Kolom di CSV tidak sesuai dengan tabel PostgreSQL.")

            # Load data ke tabel
            data_bersih.to_sql('fashion_products', con=engine, if_exists='append', index=False)
            print("✅ Data berhasil disimpan ke tabel 'fashion_products'.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
        raise
