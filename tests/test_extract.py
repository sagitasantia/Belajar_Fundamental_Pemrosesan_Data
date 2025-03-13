import unittest
from bs4 import BeautifulSoup
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import extract_product_data

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <div class="collection-card">
            <h3 class="product-title">T-shirt 01</h3>
            <div class="price-container">$25.00</div>
            <p>Rating: 4.5/5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')

    def test_extract_product_data_valid(self):
        """Menguji ekstraksi data produk yang valid."""
        result = extract_product_data(self.soup)
        self.assertIsInstance(result, dict, "Hasil ekstraksi ")

        expected_output = {
            'Title': 'T-shirt 01',
            'Price': '$25.00',
            'Rating': '4.5',
            'Colors': '3',
            'Size': 'M',
            'Gender': 'Unisex'
        }

        for key, value in expected_output.items():
            self.assertIn(key, result, f"Kolom '{key}' harus ada di hasil ekstraksi")
            self.assertEqual(result[key], value, f"Nilai '{key}' tidak sesuai")

        self.assertIn('Timestamp', result, "Kolom 'Timestamp' harus ada")
        self.assertIsInstance(result['Timestamp'], str, "Timestamp harus berupa string")

    def test_extract_invalid_product(self):
        """Menguji ekstraksi pada produk yang tidak valid."""
        invalid_html = "<div class='collection-card'></div>"
        invalid_soup = BeautifulSoup(invalid_html, 'html.parser')
        result = extract_product_data(invalid_soup)


        self.assertIsNone(result, "Produk yang tidak valid harus menghasilkan None")

    def test_partial_data(self):
        """Menguji ekstraksi jika sebagian data hilang."""
        partial_html = """
        <div class="collection-card">
            <h3 class="product-title">T-shirt 02</h3>
            <div class="price-container">$30.00</div>
        </div>
        """
        partial_soup = BeautifulSoup(partial_html, 'html.parser')
        result = extract_product_data(partial_soup)

        self.assertIsInstance(result, dict, "Hasil ekstraksi harus berupa dictionary")
        self.assertEqual(result['Title'], 'T-shirt 02')
        self.assertEqual(result['Price'], '$30.00')

        self.assertEqual(result['Rating'], 'N/A')
        self.assertEqual(result['Colors'], 'N/A')
        self.assertEqual(result['Size'], 'N/A')
        self.assertEqual(result['Gender'], 'N/A')

    def test_extract_product_data_no_price(self):
        """Menguji ekstraksi jika harga tidak tersedia."""
        no_price_html = """
        <div class="collection-card">
            <h3 class="product-title">Hoodie 03</h3>
            <p>Rating: 4.3/5</p>
            <p>5 Colors</p>
            <p>Size: L</p>
            <p>Gender: Men</p>
        </div>
        """
        no_price_soup = BeautifulSoup(no_price_html, 'html.parser')
        result = extract_product_data(no_price_soup)

        self.assertIsInstance(result, dict, "Hasil ekstraksi")
        self.assertEqual(result['Title'], 'Hoodie 03')
        self.assertEqual(result['Price'], 'Price Unavailable')
        self.assertEqual(result['Rating'], '4.3')
        self.assertEqual(result['Colors'], '5')
        self.assertEqual(result['Size'], 'L')
        self.assertEqual(result['Gender'], 'Men')

if __name__ == '__main__':
    unittest.main()