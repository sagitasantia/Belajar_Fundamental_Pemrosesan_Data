import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import transform_to_DataFrame, clean_and_transform

class TestTransform(unittest.TestCase):
    def setUp(self):
        # Data sampel 
        self.sample_data = [
            {
                'Title': 'T-shirt 01',
                'Price': '$25.00',
                'Rating': 'Rating: 4.5/5',
                'Colors': '3 Colors',
                'Size': 'Size: M',
                'Gender': 'Gender: Unisex',
                'Timestamp': '2024-02-20T12:00:00'
            },
            {
                'Title': 'Jacket 02',
                'Price': 'Price Unavailable',
                'Rating': 'Invalid Rating',
                'Colors': 'NaN',
                'Size': 'Size: L',
                'Gender': 'Gender: Men',
                'Timestamp': '2024-02-20T12:00:00'
            },
            {
                'Title': 'Unknown Product',
                'Price': '$100.00',
                'Rating': 'Rating: 3.8/5',
                'Colors': '5 Colors',
                'Size': 'Size: XL',
                'Gender': 'Gender: Women',
                'Timestamp': '2024-02-20T12:00:00'
            }
        ]
        self.df = transform_to_DataFrame(self.sample_data)

    def test_transform_columns(self):
        """Pastikan kolom sesuai dengan tabel PostgreSQL."""
        expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        self.assertListEqual(self.df.columns.tolist(), expected_columns)

    def test_clean_and_transform(self):
        """Menguji pembersihan dan transformasi DataFrame."""
        cleaned_df = clean_and_transform(self.sample_data)
        self.assertEqual(cleaned_df.shape[0], 1)  
        self.assertEqual(cleaned_df.iloc[0]['Title'], 'T-shirt 01')
        self.assertEqual(cleaned_df.iloc[0]['Price'], 400000.0) 
        self.assertEqual(cleaned_df.iloc[0]['Rating'], 4.5)  
        self.assertEqual(cleaned_df.iloc[0]['Colors'], 3)  
        self.assertEqual(cleaned_df.iloc[0]['Size'], 'M')
        self.assertEqual(cleaned_df.iloc[0]['Gender'], 'Unisex')

    def test_handle_invalid_data(self):
        """Pastikan data tidak valid dihapus atau ditangani dengan benar."""
        cleaned_df = clean_and_transform(self.sample_data)
        self.assertNotIn('Unknown Product', cleaned_df['Title'].values)
        self.assertFalse(cleaned_df['Price'].isna().any(), "Terdapat harga kosong.")

    def test_data_types(self):
        """Memastikan tipe data kolom sesuai."""
        cleaned_df = clean_and_transform(self.sample_data)

        self.assertTrue(pd.api.types.is_float_dtype(cleaned_df['Price']), "Price harus float.")
        self.assertTrue(pd.api.types.is_float_dtype(cleaned_df['Rating']), "Rating harus float.")
        self.assertTrue(pd.api.types.is_integer_dtype(cleaned_df['Colors']), "Colors harus integer.")
        self.assertTrue(pd.api.types.is_object_dtype(cleaned_df['Title']), "Title harus string.")

if __name__ == '__main__':
    unittest.main()
