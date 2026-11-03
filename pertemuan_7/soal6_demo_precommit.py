"""
Soal 6 - Demonstrasi Pre-Commit Hooks (Black, Flake8, Isort)
============================================================
Program ini mendemonstrasikan bagaimana Pre-Commit Hooks bekerja secara otomatis
untuk mencegah kode yang tidak memenuhi standar masuk ke repositori Git:
  1. isort   : Mengurutkan dan mengelompokkan import (Standar -> Pihak Ketiga -> Lokal).
  2. black   : Memformat kode secara otomatis agar konsisten dan deterministik.
  3. flake8  : Memeriksa kode statis terhadap pelanggaran PEP 8, unused variable, dll.

File ini mensimulasikan file Python yang sengaja dibuat 'kotor' dan memperlihatkan
tahapan deteksi serta pencegahan commit (rejection) saat standar dilanggar.
"""

import os
import subprocess
import sys


def buat_file_kotor_simulasi(path_file: str) -> None:
    """
    Membuat file kode Python dengan berbagai pelanggaran standar:
      - isort violation  : Urutan import acak-acakan
      - black violation  : Spasi tidak konsisten, tanda kurung berantakan
      - flake8 violation : Variabel tidak terpakai (F841), baris > 88 karakter (E501)
    """
    konten_kotor = '''# File simulasi kode tidak patuh standar
import sys
import math
import os
from datetime import datetime
import json

def fungsi_berantakan( a,b,c ):
    # Black violation: spasi di dalam kurung dan operator tanpa spasi
    hasil=a+b*c
    variabel_tidak_terpakai = 999  # Flake8 violation: F841 local variable never used
    
    # Flake8 violation: E501 line too long (> 88 karakter)
    pesan_sangat_panjang_sekali_yang_melebihi_batas_maksimum_kolom_delapan_puluh_delapan_karakter_pep8 = "Ini adalah string yang sengaja dibuat sangat amat panjang agar ditangkap linter flake8"
    
    if hasil>10:
        return {'status':"ok",'nilai':hasil}
    else:
        return {'status':"kurang",'nilai':hasil}
'''
    with open(path_file, "w", encoding="utf-8") as f:
        f.write(konten_kotor)
    print(f"[OK] File uji 'kode_berantakan.py' berhasil dibuat dengan 3 jenis pelanggaran.")


def tampilkan_isi_file(path_file: str, judul: str) -> None:
    """Membaca dan menampilkan isi file dengan format jelas."""
    print(f"\n--- {judul} ---")
    with open(path_file, "r", encoding="utf-8") as f:
        print(f.read())
    print("-" * 65)


def jalankan_alat(perintah: list, nama_alat: str) -> int:
    """Menjalankan command line tool dan menampilkan outputnya."""
    print(f"\n>>> Menjalankan: {' '.join(perintah)} ({nama_alat})")
    hasil = subprocess.run(perintah, capture_output=True, text=True)
    
    if hasil.stdout:
        print("[STDOUT]:")
        print(hasil.stdout.strip())
    if hasil.stderr:
        print("[STDERR]:")
        print(hasil.stderr.strip())
        
    print(f"Status Kode Keluar (Exit Code): {hasil.returncode}")
    if hasil.returncode == 0:
        print(f"Hasil: [PASSED] {nama_alat} berhasil!")
    else:
        print(f"Hasil: [FAILED] {nama_alat} menemukan pelanggaran standar!")
    return hasil.returncode


def main():
    direktori = os.path.dirname(os.path.abspath(__file__))
    path_kotor = os.path.join(direktori, "kode_berantakan.py")

    print("=" * 70)
    print("DEMO SOAL 6: MEKANISME PRE-COMMIT HOOKS (BLACK, FLAKE8, ISORT)")
    print("=" * 70)

    # 1. Buat file sampel tidak memenuhi standar
    buat_file_kotor_simulasi(path_kotor)
    tampilkan_isi_file(path_kotor, "KODE AWAL (MELANGGAR STANDAR)")

    # 2. Tahap 1: Jalankan isort
    print("\n" + "=" * 70)
    print("TAHAP 1: PEMERIKSAAN & PERBAIKAN URUTAN IMPORT (ISORT)")
    print("=" * 70)
    jalankan_alat(["isort", path_kotor, "--diff"], "isort (Pratinjau Perubahan Diff)")
    jalankan_alat(["isort", path_kotor], "isort (Terapkan Pengurutan)")

    # 3. Tahap 2: Jalankan Black
    print("\n" + "=" * 70)
    print("TAHAP 2: PEMERIKSAAN & FORMATTING GAYA KODE (BLACK)")
    print("=" * 70)
    jalankan_alat(["black", path_kotor, "--diff"], "black (Pratinjau Formatter Diff)")
    jalankan_alat(["black", path_kotor], "black (Terapkan Auto-Format)")

    tampilkan_isi_file(path_kotor, "KODE SETELAH DITATA OLEH ISORT & BLACK")

    # 4. Tahap 3: Jalankan Flake8 (Linter Pencegah Commit)
    print("\n" + "=" * 70)
    print("TAHAP 3: LINTING PEP 8 DENGAN FLAKE8 (VERIFIKASI ERROR STATIS)")
    print("=" * 70)
    kode_keluar_flake8 = jalankan_alat(
        ["flake8", path_kotor, "--max-line-length=88", "--extend-ignore=E203"],
        "flake8 (Pengecekan Kualitas Kode)"
    )

    print("\n" + "=" * 70)
    print("KESIMPULAN CARA PRE-COMMIT MENCEGAH KODE MASUK KE REPOSITORI:")
    print("=" * 70)
    if kode_keluar_flake8 != 0:
        print("[GAGAL COMMIT - PRE-COMMIT BERAKSI!]")
        print("1. File 'kode_berantakan.py' memiliki error kualitas (unused variable / line too long).")
        print("2. Flake8 mengembalikan exit code non-zero (1).")
        print("3. Git Hook pre-commit secara otomatis MEMBATALKAN aksi 'git commit'.")
        print("4. Repositori terlindungi dari kode yang cacat atau melanggar konvensi tim.")
        print("\nUntuk dapat melakukan commit, developer wajib memperbaiki temuan flake8 terlebih dahulu.")
    print("=" * 70)


if __name__ == "__main__":
    main()

