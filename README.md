# Repositori Tugas & Praktikum Pemrograman Python

Repositori ini berisi kumpulan tugas, modul praktikum, dan proyek rekayasa perangkat lunak untuk mata kuliah **Pemrograman Python / Pemrograman Modern**.

---

## 👤 Identitas Mahasiswa
- **Nama**    : Sobur
- **NIM**     : 20241320046
- **Kelas**   : A1
- **Program Studi** : Sistem Informasi / Teknik Informatika
- **GitHub**  : [soburrr34/Pemrograman_python](https://github.com/soburrr34/Pemrograman_python)

---

## 📁 Struktur Direktori Repositori

```text
pemograman_python/
├── sim-mahasiswa/                 # Proyek Aplikasi Sistem Informasi Mahasiswa (Console-based CRUD)
│   ├── src/                       # Source code (main.py, models.py)
│   ├── tests/                     # Unit testing menggunakan pytest
│   └── requirements.txt
├── pertemuan_1/                   # Pengenalan & Dasar Pemrograman Python
│   └── biodata.py                 # Program interaktif input/output biodata
├── pertemuan_2/                   # Struktur Kendali, Logika Percabangan & Perulangan
│   ├── status_mahasiswa.py        # Penentuan kelulusan dan predikat nilai
│   ├── diskon_biaya.py            # Kalkulasi diskon pembayaran UKT/biaya
│   ├── peringatan_stok.py         # Sistem peringatan stok inventaris
│   ├── validasi_data.py           # Validasi format input pengguna
│   ├── menu_si_mahasiswa.py       # Menu navigasi console SI Mahasiswa
│   └── ringkasan_algoritma.py     # Rangkuman logika algoritma perulangan
├── pertemuan_5/                   # Struktur Data Koleksi Python
│   ├── soal1_analisis_kalimat.py  # Manipulasi String & statistik kata
│   ├── soal2_nilai_mahasiswa.py   # Operasi List untuk peringkat nilai
│   ├── soal3_operasi_set_beasiswa.py # Himpunan (Set): union, intersect, difference
│   ├── soal4_inventaris_toko.py   # Dictionary untuk manajemen inventaris barang
│   ├── soal5_analisis_teks.py     # Frekuensi kata dan analisis token
│   └── contoh_teks.txt            # Sampel korpus teks
├── pertemuan_6/                   # Pemrograman Modular, Ekosistem Package & REST API
│   ├── soal1_hitung_statistik.py  # Modul statistik deskriptif (mean, median, stdev)
│   ├── soal2_validasi_data.py     # Dynamic Schema Validator (*args, **kwargs)
│   ├── utilitas_akademik.py       # Custom reusable academic utility module
│   ├── sistem_informasi/          # Package modular hierarki sistem informasi
│   ├── soal3_main.py              # Runner integrasi modul akademik
│   ├── soal4_main.py              # Runner integrasi package sistem informasi
│   ├── soal5_api_data.py          # HTTP Client REST API & pengolahan data JSON
│   └── soal5_hasil_analisis.json  # Hasil serialisasi data analitik API
├── pertemuan_7/                   # Robust Programming: Exception, Logging, Testing, Refactoring & Hooks
│   ├── soal1_baca_mahasiswa_csv.py      # Exception handling CSV (try-except-else-finally)
│   ├── soal2_perpustakaan_exception.py  # Hierarki Custom Exception OOP SI Perpustakaan
│   ├── soal3_logging_si.py              # Dual-handler Logging (RotatingFileHandler & Console)
│   ├── soal4_unit_test.py               # Unit Testing unittest (26 Test Cases)
│   ├── soal5_refactoring_code_smell.py  # Identifikasi 5 Code Smell & Refactoring PEP 8
│   ├── soal6_demo_precommit.py          # Simulasi & Demonstrasi Pre-Commit Hooks
│   ├── .pre-commit-config.yaml          # Konfigurasi isort, black, flake8
│   ├── mahasiswa_valid.csv              # Sampel CSV valid
│   ├── mahasiswa_invalid_value.csv      # Sampel CSV pemicu ValueError
│   ├── mahasiswa_corrupt.csv            # Sampel CSV pemicu csv.Error (NUL byte)
│   ├── aplikasi_si.log                  # Log file hasil simulasi rotasi log
│   ├── buat_laporan_p7.py               # Generator laporan Word (.docx) otomatis
│   └── Laporan_Praktikum_Pertemuan_7_20241320046_Sobur.docx
├── .pre-commit-config.yaml        # Konfigurasi Root Pre-Commit Hooks
└── README.md                      # Dokumentasi utama repositori
```

---

## 🚀 Rangkuman Materi Tiap Pertemuan

### 📌 Pertemuan 7: Robust Programming & Software Quality
Fokus pada penulisan kode Python standar produksi yang andal, termonitor, teruji, dan patuh konvensi.

1. **Soal 1 — Pembacaan CSV & Exception Handling Lengkap (`soal1_baca_mahasiswa_csv.py`)**:
   - Menangani `FileNotFoundError`, `csv.Error`, dan `ValueError`.
   - Menggunakan blok **`else`** untuk menghitung statistik data jika pembacaan sukses.
   - Menggunakan blok **`finally`** untuk menjamin penutupan stream file (`file.close()`).

2. **Soal 2 — Hierarki Custom Exception OOP (`soal2_perpustakaan_exception.py`)**:
   - Membangun hierarki kelas berbasis `PerpustakaanError(Exception)`:
     - `BukuNotFoundError`
     - `BukuTidakTersediaError`
     - `AnggotaNotFoundError`
     - `BatasPeminjamanError`
   - Implementasi logika bisnis `pinjam_buku()` dengan validasi integritas katalog & anggota.

3. **Soal 3 — Modul Logging Terstruktur Aplikasi SI (`soal3_logging_si.py`)**:
   - **`RotatingFileHandler`**: Menangkap log `DEBUG` ke atas ke file `aplikasi_si.log` dengan rotasi otomatis (`maxBytes`, `backupCount`).
   - **`StreamHandler` (Console)**: Menangkap log `WARNING` ke atas untuk menjaga terminal tetap bersih.
   - **`Formatter`**: Menyertakan `timestamp`, `levelname`, `name`, dan `message`.

4. **Soal 4 — Unit Testing Menggunakan `unittest` (`soal4_unit_test.py`)**:
   - Menguji 3 fungsi: `hitung_ipk()`, `validasi_nim()`, dan `konversi_nilai_huruf()`.
   - Meliputi pengujian **Happy Path**, **Edge Cases** (nilai batas), dan **Invalid Input**.
   - Total **26 Test Cases** lolos 100% (*Ran 26 tests in 0.004s, OK*).

5. **Soal 5 — Identifikasi & Refactoring 5 Code Smell (`soal5_refactoring_code_smell.py`)**:
   - Identifikasi dan eliminasi:
     1. *Magic Number* $\rightarrow$ Konstanta global UPPERCASE deskriptif.
     2. *Duplikasi Logika* $\rightarrow$ Ekstraksi fungsi mandiri (DRY).
     3. *Long Method* $\rightarrow$ Penerapan *Single Responsibility Principle* (SRP).
     4. *Deep Nesting* $\rightarrow$ Penggunaan *Guard Clauses* (*Early Return*).
     5. *Dead Code* $\rightarrow$ Pembersihan variabel tak terpakai & blok *unreachable*.
   - Dilengkapi *type hints* dan *docstrings* standar PEP 8.

6. **Soal 6 — Otomasi Git Pre-Commit Hooks (`soal6_demo_precommit.py` & `.pre-commit-config.yaml`)**:
   - Menjalankan **`isort`** (pengurutan impor modul), **`black`** (formatter deterministik), dan **`flake8`** (linter statis).
   - Menunjukkan bagaimana hook membatalkan commit (*commit rejection*) jika terdapat kode cacat (misal: *unused variable* atau baris melampaui batas kolom).

---

### 📌 Pertemuan 6: Pemrograman Modular & REST API
- Pembuatan fungsi statistik deskriptif (`hitung_statistik`) menggunakan standard library.
- Validator kamus fleksibel berbasis skema (`validasi_data`) menggunakan `*args` dan `**kwargs`.
- Pengorganisasian modul ke dalam package hierarkis (`sistem_informasi`).
- Konsumsi data eksternal via HTTP REST API (`requests`) dan analisis serialisasi format JSON.

---

### 📌 Pertemuan 5: Koleksi & Struktur Data Python
- Eksplorasi tipe data bawaan: `string`, `list`, `set`, `dictionary`, dan `tuple`.
- Analisis frekuensi kata, pencarian nilai ekstrem, operasi himpunan (beasiswa mahasiswa), dan manajemen inventaris toko.

---

### 📌 Pertemuan 2: Percabangan, Logika & Perulangan
- Implementasi seleksi kondisi `if-elif-else` untuk penentuan status akademik mahasiswa.
- Algoritma perhitungan diskon UKT dan pemantauan batas aman stok inventaris.
- Desain menu interaktif antarmuka konsol.

---

### 📌 Pertemuan 1: Pengenalan Sintaks Python
- Dasar sintaks Python, manipulasi tipe data primitif, formatted print, dan program biodata mahasiswa.

---

### 📌 Proyek Mandiri: Sistem Informasi Mahasiswa (`sim-mahasiswa`)
Aplikasi konsol interaktif berbasis Object-Oriented & Dataclass:
- Operasi CRUD (Create, Read, Update, Delete) data mahasiswa.
- Pencarian dan filter berdasarkan NIM/Prodi.
- Pengujian unit otomatis berbasis `pytest`.

---

## 🛠️ Panduan Instalasi & Menjalankan Program

### 1. Kloning Repositori & Persiapan Lingkungan
```powershell
# Clone repositori
git clone https://github.com/soburrr34/Pemrograman_python.git
cd Pemrograman_python

# Buat dan aktifkan Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalasi dependensi
pip install pre-commit black flake8 isort python-docx pytest requests
```

### 2. Menjalankan Skrip Pertemuan 7
Pindah ke direktori `pertemuan_7`:
```powershell
cd pertemuan_7

# Soal 1: Pembacaan CSV & Exception Handling
python soal1_baca_mahasiswa_csv.py

# Soal 2: Custom Exception Perpustakaan
python soal2_perpustakaan_exception.py

# Soal 3: Logging Terstruktur
python soal3_logging_si.py

# Soal 4: Rangkaian Unit Testing (26 Tests)
python soal4_unit_test.py

# Soal 5: Refactoring Code Smell
python soal5_refactoring_code_smell.py

# Soal 6: Demonstrasi Pre-Commit Hooks
python soal6_demo_precommit.py

# Generate Laporan Dokumen Word (.docx)
python buat_laporan_p7.py
```

### 3. Mengaktifkan Git Pre-Commit Hooks
```powershell
# Pasang git pre-commit hook ke direktori .git/hooks/
pre-commit install

# Uji jalankan hooks ke seluruh file di repositori
pre-commit run --all-files
```

### 4. Menjalankan Proyek SIM Mahasiswa & Pytest
```powershell
cd ..\sim-mahasiswa
python src\main.py

# Menjalankan unit test dengan pytest
pytest tests\ -v
```

---

## 📜 Lisensi & Catatan Akademik
Seluruh kode dalam repositori ini disusun untuk keperluan studi dan penyelesaian tugas akademik mata kuliah Pemrograman Python. Bebas dipelajari dan dikembangkan dengan tetap mengedepankan etika akademik.
