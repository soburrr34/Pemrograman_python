# Sistem Informasi Mahasiswa (SIM)

Aplikasi console-based untuk mengelola data mahasiswa pada Program Studi Sistem Informasi.

## Identitas
- **Nama**    : Sobur
- **NIM**     : 20241320046
- **Kelas**   : A1
- **Jurusan** : Sistem Informasi

## Fitur
- ✅ Tambah data mahasiswa (NIM, nama, prodi, angkatan, IPK)
- ✅ Tampilkan seluruh data dalam tabel
- ✅ Cari mahasiswa berdasarkan NIM
- ✅ Hapus data mahasiswa
- ✅ Validasi data input
- ✅ Unit test dengan pytest

## Prasyarat
- Python 3.10+
- pip

## Instalasi & Menjalankan

```bash
# Clone repo
git clone https://github.com/soburrr34/Pemrograman_python.git
cd sim-mahasiswa

# Buat virtual environment
python -m venv venv

# Aktifkan venv (Windows PowerShell)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Jalankan program
python src/main.py
```

## Menjalankan Test

```bash
pytest tests/ -v
```

## Struktur Direktori

```
sim-mahasiswa/
├── src/
│   ├── __init__.py
│   ├── main.py       # Entry point & menu interaktif
│   └── models.py     # Model data Mahasiswa & DaftarMahasiswa
├── tests/
│   ├── __init__.py
│   └── test_main.py  # Unit tests
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Checklist
- [x] Struktur direktori proyek dibuat
- [x] Virtual environment dikonfigurasi
- [x] Paket dependensi diinstal
- [x] Model data Mahasiswa (dataclass) dibuat
- [x] Program utama dengan menu interaktif
- [x] Unit test dasar dengan pytest
- [x] .gitignore dikonfigurasi
- [x] README.md disusun
- [x] Push ke GitHub
