# extract.py
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import time
from datetime import datetime

SERVICE_ACCOUNT_FILE = 'google-sheets-api.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key('1_AhSsHZkj45gLNP6Ou32EvJFp7_gUyMOXILvmf_eXcc').sheet1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

base_url = 'https://fashion-studio.dicoding.dev/?page={}'

def extract_product_data(product):
    """Mengambil detail produk dari elemen HTML."""
    try:
        # Ekstrak informasi produk
        title = product.select_one('.product-title').text.strip()
        price = product.select_one('.price-container').text.strip() if product.select_one('.price-container') else 'Price Unavailable'

        details = product.find_all('p')
        rating = details[0].text.strip().split('/')[0].replace('Rating: ', '') if len(details) > 0 else 'N/A'
        colors = ''.join(filter(str.isdigit, details[1].text.strip())) if len(details) > 1 else 'N/A'
        size = details[2].text.replace('Size: ', '').strip() if len(details) > 2 else 'N/A'
        gender = details[3].text.replace('Gender: ', '').strip() if len(details) > 3 else 'N/A'

        timestamp = datetime.now().isoformat()

        return {
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender,
            'Timestamp': timestamp
        }
    except Exception as e:
        print(f"❌ Gagal memproses produk: {e}")
        return None

def extract_data():
    """Scraping data dari website dan mengembalikan list of dictionaries."""
    all_data = []
    print("📊 Memulai proses ekstraksi data...")

    # Loop untuk scraping dari halaman 2 hingga 52
    for page in range(2, 53):
        print(f"🔍 Mengambil data dari halaman {page}...")
        url = base_url.format(page)

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"❌ Gagal mengakses halaman {page}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.select('.collection-card')

            if not products:
                print(f"❌ Tidak ada produk di halaman {page}")
                continue

            # Ekstrak data dari setiap produk
            for product in products:
                data = extract_product_data(product)
                if data:
                    all_data.append(data)

            # Tunggu 2 detik untuk menghindari rate limit
            time.sleep(2)

        except Exception as e:
            print(f"❌ Kesalahan saat mengambil halaman {page}: {e}")

    print(f"✅ Total data yang diekstrak: {len(all_data)} baris.")

    # Tulis hasil ke Google Sheets
    try:
        print("📤 Menulis data ke Google Sheets...")
        sheet.clear()  # Hapus data lama di spreadsheet
        header = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        sheet.append_rows([header] + [list(item.values()) for item in all_data])
        print("✅ Data berhasil ditulis ke Google Sheets!")
    except Exception as e:
        print(f"❌ Gagal menulis ke Google Sheets: {e}")

    return all_data
