"""
Soal 3 - main.py (File Terpisah)
==================================
File utama yang mengimport dan menggunakan module utilitas_akademik.
Mendemonstrasikan penggunaan semua fungsi dalam modul.
"""

# Import fungsi dari module utilitas_akademik
from utilitas_akademik import (
    hitung_ipk,
    konversi_nilai_huruf,
    generate_transkrip,
)


def demo_konversi_nilai():
    """Demonstrasi fungsi konversi_nilai_huruf()."""
    print("\n" + "=" * 65)
    print("  DEMO 1: Konversi Nilai Angka ke Huruf")
    print("=" * 65)

    nilai_uji = [95, 80, 76, 70, 65, 60, 55, 45, 35]
    print(f"\n  {'Nilai Angka':<14} {'Nilai Huruf':<13} {'Bobot':<8} {'Keterangan'}")
    print(f"  {'-'*14} {'-'*13} {'-'*8} {'-'*20}")

    for nilai in nilai_uji:
        hasil = konversi_nilai_huruf(nilai)
        print(
            f"  {hasil['nilai_angka']:<14} "
            f"{hasil['nilai_huruf']:<13} "
            f"{hasil['bobot']:<8} "
            f"{hasil['keterangan']}"
        )


def demo_hitung_ipk():
    """Demonstrasi fungsi hitung_ipk()."""
    print("\n" + "=" * 65)
    print("  DEMO 2: Hitung IPK Mahasiswa")
    print("=" * 65)

    # Daftar mata kuliah semester 1
    mk_semester_1 = [
        {'nama_mk': 'Pengantar Informatika',  'sks': 2, 'nilai_angka': 88},
        {'nama_mk': 'Matematika Diskrit',      'sks': 3, 'nilai_angka': 75},
        {'nama_mk': 'Pemrograman Dasar',       'sks': 3, 'nilai_angka': 90},
        {'nama_mk': 'Bahasa Indonesia',        'sks': 2, 'nilai_angka': 85},
        {'nama_mk': 'Pendidikan Pancasila',    'sks': 2, 'nilai_angka': 78},
        {'nama_mk': 'Bahasa Inggris',          'sks': 2, 'nilai_angka': 82},
    ]

    hasil = hitung_ipk(mk_semester_1)

    print(f"\n  Jumlah Mata Kuliah : {hasil['jumlah_mk']}")
    print(f"  Total SKS          : {hasil['total_sks']}")
    print(f"  Total Angka Mutu   : {hasil['total_mutu']}")
    print(f"  IPK                : {hasil['ipk']:.2f}")
    print(f"  Predikat           : {hasil['predikat']}")

    print(f"\n  {'Mata Kuliah':<28} {'SKS':<5} {'Nilai':<6} {'Huruf':<6} {'Mutu'}")
    print(f"  {'-'*28} {'-'*5} {'-'*6} {'-'*6} {'-'*6}")
    for mk in hasil['detail']:
        print(
            f"  {mk['nama_mk']:<28} {mk['sks']:<5} "
            f"{mk['nilai_angka']:<6} {mk['nilai_huruf']:<6} {mk['angka_mutu']}"
        )

    return mk_semester_1


def demo_generate_transkrip(daftar_mk: list):
    """Demonstrasi fungsi generate_transkrip()."""
    print("\n" + "=" * 65)
    print("  DEMO 3: Generate Transkrip Akademik")
    print("=" * 65)

    transkrip = generate_transkrip(
        nama              = 'Rina Safitri',
        nim               = '2023050123',
        program_studi     = 'Teknik Informatika',
        semester          = 1,
        daftar_matakuliah = daftar_mk,
        tahun_akademik    = '2023/2024 Ganjil',
        wali_dosen        = 'Dr. Hendra Kusuma, M.T.',
        kampus            = 'Universitas Teknologi Nusantara',
    )

    print()
    print(transkrip)


def main():
    """Fungsi utama yang menjalankan semua demo."""
    print("\n" + "#" * 65)
    print("  SOAL 3 - MAIN.PY: Menggunakan Module utilitas_akademik")
    print("#" * 65)

    # Jalankan semua demo
    demo_konversi_nilai()
    daftar_mk = demo_hitung_ipk()
    demo_generate_transkrip(daftar_mk)

    print("\n" + "#" * 65)
    print("  Program selesai!")
    print("#" * 65)


# Guard agar kode hanya berjalan jika file ini dijalankan langsung
if __name__ == '__main__':
    main()
