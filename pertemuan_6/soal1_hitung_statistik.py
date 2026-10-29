"""
Soal 1 - Fungsi Hitung Statistik
=================================
Membuat fungsi hitung_statistik() yang menerima list angka dan mengembalikan
dictionary berisi mean, median, modus, range (max-min), dan standard deviation.
Hanya menggunakan standard library: statistics dan math.
"""

import statistics
import math


def hitung_statistik(angka: list) -> dict:
    """
    Menghitung statistik deskriptif dari list angka.

    Args:
        angka (list): List berisi angka-angka (int atau float)

    Returns:
        dict: Dictionary berisi:
            - mean              : Rata-rata
            - median            : Nilai tengah
            - modus             : Nilai yang paling sering muncul
            - range             : Selisih nilai max dan min
            - standard_deviation: Simpangan baku
            - jumlah_data       : Jumlah elemen
            - nilai_max         : Nilai terbesar
            - nilai_min         : Nilai terkecil
            - variance          : Varians

    Raises:
        ValueError: Jika list angka kosong atau berisi bukan angka
    """
    # Validasi input
    if not angka:
        raise ValueError("List angka tidak boleh kosong!")

    if not all(isinstance(n, (int, float)) for n in angka):
        raise ValueError("Semua elemen harus berupa angka (int atau float)!")

    # Mean (rata-rata aritmetika)
    mean = statistics.mean(angka)

    # Median (nilai tengah setelah diurutkan)
    median = statistics.median(angka)

    # Modus (nilai yang paling sering muncul)
    try:
        # mode() melempar StatisticsError jika ada lebih dari satu modus
        modus = statistics.mode(angka)
    except statistics.StatisticsError:
        # multimode() mengembalikan semua nilai dengan frekuensi tertinggi
        modus = statistics.multimode(angka)

    # Range (max - min)
    nilai_max = max(angka)
    nilai_min = min(angka)
    nilai_range = nilai_max - nilai_min

    # Standard Deviation & Variance
    if len(angka) > 1:
        # stdev() = simpangan baku sampel (n-1)
        std_dev  = statistics.stdev(angka)
        variance = statistics.variance(angka)
    else:
        std_dev  = 0.0
        variance = 0.0

    return {
        "mean"              : round(mean,     4),
        "median"            : round(median,   4),
        "modus"             : modus,
        "range"             : round(nilai_range, 4),
        "standard_deviation": round(std_dev,  4),
        "variance"          : round(variance, 4),
        "jumlah_data"       : len(angka),
        "nilai_max"         : nilai_max,
        "nilai_min"         : nilai_min,
    }


def tampilkan_statistik(label: str, hasil: dict) -> None:
    """Menampilkan hasil statistik secara terformat."""
    lebar = 50
    print(f"\n{'=' * lebar}")
    print(f"  {label}")
    print(f"{'=' * lebar}")
    for key, value in hasil.items():
        print(f"  {key:<22}: {value}")
    print(f"{'=' * lebar}")


# Testing
if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  TESTING SOAL 1 - hitung_statistik()")
    print("=" * 50)

    # Test 1: Nilai ujian mahasiswa
    data_nilai = [75, 80, 85, 90, 75, 85, 70, 95, 85, 80]
    print(f"\n[Test 1] Data nilai ujian: {data_nilai}")
    hasil1 = hitung_statistik(data_nilai)
    tampilkan_statistik("Statistik Nilai Ujian Mahasiswa", hasil1)

    # Test 2: Data dengan modus ganda (multimodal)
    data_multimodal = [1, 2, 2, 3, 3, 4, 5]
    print(f"\n[Test 2] Data multimodal: {data_multimodal}")
    hasil2 = hitung_statistik(data_multimodal)
    tampilkan_statistik("Statistik Data Multimodal", hasil2)

    # Test 3: Data IPK (float)
    data_ipk = [3.75, 3.50, 3.85, 2.90, 3.75, 3.60, 4.00, 3.20]
    print(f"\n[Test 3] Data IPK: {data_ipk}")
    hasil3 = hitung_statistik(data_ipk)
    tampilkan_statistik("Statistik Data IPK", hasil3)

    # Test 4: Data tunggal
    data_tunggal = [42]
    print(f"\n[Test 4] Data tunggal: {data_tunggal}")
    hasil4 = hitung_statistik(data_tunggal)
    tampilkan_statistik("Statistik Data Tunggal", hasil4)

    # Test 5: Error handling
    print("\n[Test 5] Error handling - list kosong:")
    try:
        hitung_statistik([])
    except ValueError as e:
        print(f"  ValueError: {e}")

    print("\n[Test 5b] Error handling - bukan angka:")
    try:
        hitung_statistik([1, 2, "tiga", 4])
    except ValueError as e:
        print(f"  ValueError: {e}")

    print("\n[SELESAI] Semua test berhasil!")
