# Pertemuan 7 - Robust Programming & Software Quality

Direktori ini berisi implementasi lengkap tugas praktikum **Pertemuan 7** untuk mata kuliah **Pemrograman Python**.

## 👤 Identitas Mahasiswa
- **Nama**  : Sobur
- **NIM**   : 20241320046
- **Prodi** : Teknik Informatika / Sistem Informasi

---

## 📋 Daftar Soal & Berkas Implementasi

| No | Berkas | Deskripsi Topik |
| :---: | :--- | :--- |
| **1** | [`soal1_baca_mahasiswa_csv.py`](soal1_baca_mahasiswa_csv.py) | Pembacaan file CSV dengan penanganan lengkap: `FileNotFoundError`, `csv.Error`, dan `ValueError`. Dilengkapi blok `else` untuk statistik dan `finally` untuk penutupan file. |
| **2** | [`soal2_perpustakaan_exception.py`](soal2_perpustakaan_exception.py) | Hierarki Custom Exception OOP Sistem Perpustakaan (`PerpustakaanError`, `BukuNotFoundError`, `BukuTidakTersediaError`, `AnggotaNotFoundError`, `BatasPeminjamanError`) dan implementasi `pinjam_buku()`. |
| **3** | [`soal3_logging_si.py`](soal3_logging_si.py) | Konfigurasi logging dual-handler: `RotatingFileHandler` (DEBUG ke atas) dan Console `StreamHandler` (WARNING ke atas) dengan Formatter terstandarisasi. |
| **4** | [`soal4_unit_test.py`](soal4_unit_test.py) | Rangkaian unit test (`unittest.TestCase`) untuk `hitung_ipk()`, `validasi_nim()`, dan `konversi_nilai_huruf()` menguji Happy Path, Edge Cases, dan Invalid Input (Total 26 test cases). |
| **5** | [`soal5_refactoring_code_smell.py`](soal5_refactoring_code_smell.py) | Identifikasi 5 Code Smell (*Magic Number, Duplikasi, Long Method, Deep Nesting, Dead Code*) dan refactoring bersih berstandar PEP 8 (*type hints* & *docstrings*). |
| **6** | [`soal6_demo_precommit.py`](soal6_demo_precommit.py) | Demonstrasi Pre-Commit Hooks (`isort`, `black`, `flake8`) yang secara otomatis mencegah kode cacat masuk ke git repository. |
| **Doc**| [`buat_laporan_p7.py`](buat_laporan_p7.py) | Skrip generator dokumen laporan Word (`.docx`) otomatis. |

---

## 🧪 Berkas Sampel Pengujian

- `mahasiswa_valid.csv`: Data valid mahasiswa untuk pengujian blok `else` dan `finally`.
- `mahasiswa_invalid_value.csv`: Berisi data IPK non-numerik untuk memicu `ValueError`.
- `mahasiswa_corrupt.csv`: Berisi karakter biner `NUL` untuk memicu `csv.Error`.
- `aplikasi_si.log`: File log rotasi yang dihasilkan dari eksekusi `soal3_logging_si.py`.
- `kode_berantakan.py`: File dengan pelanggaran aturan untuk mendemonstrasikan penolakan git commit oleh pre-commit hooks.
- `.pre-commit-config.yaml`: File konfigurasi pre-commit hooks.

---

## ⚡ Cara Menjalankan

Buka terminal di dalam folder `pertemuan_7`:

```powershell
# 1. Menjalankan Soal 1 (Pembacaan CSV)
python soal1_baca_mahasiswa_csv.py

# 2. Menjalankan Soal 2 (Custom Exception Perpustakaan)
python soal2_perpustakaan_exception.py

# 3. Menjalankan Soal 3 (Logging Terstruktur)
python soal3_logging_si.py

# 4. Menjalankan Soal 4 (Rangkaian 26 Unit Test)
python soal4_unit_test.py

# 5. Menjalankan Soal 5 (Refactoring Code Smell)
python soal5_refactoring_code_smell.py

# 6. Menjalankan Soal 6 (Demo Pre-Commit Hooks)
python soal6_demo_precommit.py

# Menghasilkan Laporan Word (.docx)
python buat_laporan_p7.py
```

