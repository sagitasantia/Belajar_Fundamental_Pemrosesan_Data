import unittest
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import load_to_postgres

class TestLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_url = "postgresql+psycopg2://developer:tia2209116043@localhost:5432/fashion_product"
        cls.engine = create_engine(cls.db_url)    
        # Data contoh 
        cls.sample_data = pd.DataFrame([
            {
                'Title': 'T-shirt 01',
                'Price': 400000.0,
                'Rating': 4.5,
                'Colors': 3,
                'Size': 'M',
                'Gender': 'Unisex',
                'Timestamp': '2025-03-20T12:00:00'
            }
        ])
        
        with cls.engine.connect() as con:
            con.execute(text("""
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
            """))
            print("✅ Tabel 'fashion_products' berhasil dibuat.")

    def test_load_to_postgres(self):
        print("Memulai pengujian load_to_postgres()...")

        try:
            load_to_postgres(self.sample_data, self.db_url)
        except Exception as e:
            self.fail(f"❌ Terjadi kesalahan saat memuat data: {e}")
        with self.engine.connect() as con:
            result = con.execute(text('SELECT * FROM fashion_products WHERE "Title" = :title'),
                                 {'title': 'T-shirt 01'}).fetchone()
            
            print(f"🔍 Data hasil query: {result}")
            self.assertIsNotNone(result, "❌ Data tidak ditemukan di tabel.")
            self.assertEqual(result.Title, 'T-shirt 01')
            self.assertEqual(result.Price, 400000.0)
            self.assertEqual(result.Rating, 4.5)
            self.assertEqual(result.Colors, 3)
            self.assertEqual(result.Size, 'M')
            self.assertEqual(result.Gender, 'Unisex')

    @classmethod
    def tearDownClass(cls):
        with cls.engine.connect() as con:
            con.execute(text('DELETE FROM fashion_products WHERE "Title" = :title'),
                        {'title': 'T-shirt 01'})
            print("✅ Data uji berhasil dihapus.")

if __name__ == '__main__':
    unittest.main()
