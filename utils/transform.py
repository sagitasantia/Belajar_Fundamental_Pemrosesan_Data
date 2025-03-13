import pandas as pd
import numpy as np

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    return pd.DataFrame(data)

def clean_and_transform(data):
    """Membersihkan dan mentransformasi DataFrame."""
    # Konversi ke DataFrame
    df = transform_to_DataFrame(data)

    # Validasi kolom
    expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"❌ Kolom berikut tidak ditemukan di CSV: {missing_columns}")

    # Bersihkan kolom 'Price'
    df['Price'] = df['Price'].replace('Price Unavailable', np.nan)

    # Hapus baris dengan harga kosong
    df.dropna(subset=['Price'], inplace=True)

    # Bersihkan simbol '$' dari kolom 'Price' (Pastikan semua dihapus)
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True).astype(float) * 16000

    # Hapus produk 'Unknown Product'
    df = df[df['Title'] != 'Unknown Product']

    # Bersihkan kolom 'Rating'
    df['Rating'] = pd.to_numeric(df['Rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')

    # Bersihkan kolom 'Colors' dan tangani NaN
    df['Colors'] = pd.to_numeric(df['Colors'].str.extract(r'(\d+)')[0], errors='coerce').fillna(0).astype(int)

    # Bersihkan label di kolom 'Size' dan 'Gender'
    df['Size'] = df['Size'].str.replace('Size: ', '', regex=True)
    df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=True)

    # Simpan hasil transformasi
    df.to_csv('data_bersih.csv', index=False)

    print("✅ Data berhasil dibersihkan dan disimpan ke 'data_bersih.csv'")

    return df
