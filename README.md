# 📊 ETL Pipeline - Fashion Product

Proyek ini adalah implementasi ETL (Extract, Transform, Load) pipeline sederhana yang mengambil data produk dari website [Fashion Studio Dicoding](https://fashion-studio.dicoding.dev/), membersihkan data, lalu menyimpan hasilnya ke Google Sheets dan PostgreSQL.

---

## 📌 Cara Menjalankan ETL Pipeline
1. Pastikan semua dependency sudah terinstall dengan menjalankan:

    ```bash
    pip install -r requirements.txt
    ```

2. Jalankan pipeline ETL dengan perintah berikut:

    ```bash
    python main.py
    ```

---

## 🧪 Cara Menjalankan Unit Test
Untuk memastikan semua fungsi berjalan dengan benar, jalankan unit test menggunakan perintah ini:

```bash
pytest tests/
```

Jika ingin melihat hasil lebih rinci, gunakan opsi `-v`:

```bash
pytest tests/ -v
```

---

## 📊 Cara Menjalankan Test Coverage
Untuk memeriksa seberapa besar kode telah diuji oleh unit test, gunakan perintah berikut:

1. Jalankan test coverage:

    ```bash
    pytest tests/ --cov=tests --cov-report=term-missing
    ```

2. Hasilnya akan menampilkan persentase cakupan kode yang diuji di setiap file.

---

## 📄 Struktur Proyek
```
submission-pemda/
├── .venv/                 # Virtual environment (opsional)
├── main.py                # Skrip utama untuk menjalankan ETL
├── requirements.txt       # Daftar dependency
├── utils/                 # Folder untuk modul ETL
│    ├── extract.py        # Modul untuk scraping data
│    ├── transform.py      # Modul untuk membersihkan dan memproses data
│    └── load.py           # Modul untuk menyimpan data ke Google Sheets & PostgreSQL
└── tests/                 # Folder untuk unit test
     ├── test_extract.py   # Unit test untuk extract.py
     ├── test_transform.py # Unit test untuk transform.py
     └── test_load.py      # Unit test untuk load.py
```

---

## 📊 URL Google Sheets
Anda dapat melihat hasil data yang sudah diekstrak dan dibersihkan di Google Sheets melalui tautan berikut:

👉 [Google Sheets - Fashion Product](https://docs.google.com/spreadsheets/d/1_AhSsHZkj45gLNP6Ou32EvJFp7_gUyMOXILvmf_eXcc)

---

✅ **Proyek ini telah melalui pengujian menyeluruh dengan cakupan (coverage) lebih dari 90% di semua unit test.**
![image](https://github.com/user-attachments/assets/d01dcc63-4edb-44ea-81cf-454800724493)

