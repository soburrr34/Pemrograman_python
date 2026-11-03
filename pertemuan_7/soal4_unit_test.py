"""
Soal 4 - Unit Testing Menggunakan unittest
==========================================
Mengimplementasikan 3 fungsi akademik dan rangkaian pengujian unit (unit test) lengkap:
  (a) hitung_ipk(daftar_nilai)       : Menghitung rata-rata IPK dari list nilai (0.0 - 4.0)
  (b) validasi_nim(nim)              : Memvalidasi string NIM berformat 10 digit numerik
  (c) konversi_nilai_huruf(nilai)    : Mengkonversi skor numerik (0-100) ke huruf mutu (A, B+, dst)

Mencakup pengujian terstruktur untuk:
  - Happy Path (Kasus normal yang valid)
  - Edge Cases (Kasus batas/ekstrem)
  - Invalid Input (Input tidak valid, salah tipe data, di luar rentang)
"""

import unittest
from typing import List, Union


# =====================================================================
# 1. IMPLEMENTASI FUNGSI AKADEMIK
# =====================================================================

def hitung_ipk(daftar_nilai: List[Union[int, float]]) -> float:
    """
    Menghitung Indeks Prestasi Kumulatif (IPK) dari daftar nilai skala 0.00 - 4.00.

    Args:
        daftar_nilai (List[float/int]): Kumpulan nilai semester/mata kuliah.

    Returns:
        float: Rata-rata IPK dibulatkan 2 desimal.

    Raises:
        TypeError: Jika input bukan list atau elemen list bukan int/float.
        ValueError: Jika list kosong atau ada nilai di luar rentang 0.0 - 4.0.
    """
    if not isinstance(daftar_nilai, list):
        raise TypeError(f"Input harus berupa list, bukan {type(daftar_nilai).__name__}")

    if len(daftar_nilai) == 0:
        raise ValueError("Daftar nilai tidak boleh kosong!")

    for item in daftar_nilai:
        if not isinstance(item, (int, float)) or isinstance(item, bool):
            raise TypeError(f"Elemen nilai harus bertipe numerik (int/float), ditemukan: {type(item).__name__}")
        if not (0.0 <= item <= 4.0):
            raise ValueError(f"Nilai {item} berada di luar rentang valid IPK (0.00 - 4.00)!")

    return round(sum(daftar_nilai) / len(daftar_nilai), 2)


def validasi_nim(nim: str) -> bool:
    """
    Memvalidasi format Nomor Induk Mahasiswa (NIM).
    Syarat valid:
      - Tipe data string
      - Tepat 10 karakter
      - Semua karakter berupa angka digit (0-9)

    Args:
        nim (str): String NIM yang akan divalidasi.

    Returns:
        bool: True jika valid 10 digit angka, False jika tidak valid.

    Raises:
        TypeError: Jika argumen nim bukan bertipe string.
    """
    if not isinstance(nim, str):
        raise TypeError(f"NIM harus berupa string, bukan {type(nim).__name__}")

    if len(nim) != 10:
        return False

    return nim.isdigit()


def konversi_nilai_huruf(nilai: Union[int, float]) -> str:
    """
    Mengonversi nilai angka skala 0 - 100 menjadi nilai huruf mutu akademik.
    Skala:
      - 85.0 - 100.0 : A
      - 80.0 - <85.0 : A-
      - 75.0 - <80.0 : B+
      - 70.0 - <75.0 : B
      - 65.0 - <70.0 : B-
      - 60.0 - <65.0 : C+
      - 55.0 - <60.0 : C
      - 40.0 - <55.0 : D
      - 0.0  - <40.0 : E

    Args:
        nilai (int/float): Skor angka mahasiswa (0-100).

    Returns:
        str: Nilai huruf mutu (A, A-, B+, B, B-, C+, C, D, E).

    Raises:
        TypeError: Jika nilai bukan numerik (int/float).
        ValueError: Jika nilai < 0 atau > 100.
    """
    if not isinstance(nilai, (int, float)) or isinstance(nilai, bool):
        raise TypeError(f"Nilai harus berupa angka (int/float), bukan {type(nilai).__name__}")

    if not (0.0 <= float(nilai) <= 100.0):
        raise ValueError(f"Nilai angka {nilai} harus berada dalam rentang 0 hingga 100!")

    val = float(nilai)
    if val >= 85.0:
        return "A"
    elif val >= 80.0:
        return "A-"
    elif val >= 75.0:
        return "B+"
    elif val >= 70.0:
        return "B"
    elif val >= 65.0:
        return "B-"
    elif val >= 60.0:
        return "C+"
    elif val >= 55.0:
        return "C"
    elif val >= 40.0:
        return "D"
    else:
        return "E"


# =====================================================================
# 2. UNIT TESTING DENGAN UNITTEST
# =====================================================================

class TestHitungIPK(unittest.TestCase):
    """Pengujian Unit untuk fungsi hitung_ipk()"""

    # --- HAPPY PATH ---
    def test_happy_path_rata_rata_normal(self):
        """Memastikan perhitungan rata-rata IPK normal benar."""
        self.assertEqual(hitung_ipk([3.5, 3.75, 4.0, 3.25]), 3.62)
        self.assertEqual(hitung_ipk([3.0, 4.0]), 3.50)

    def test_happy_path_semua_nilai_maksimal(self):
        """Memastikan seluruh nilai 4.0 menghasilkan IPK 4.0."""
        self.assertEqual(hitung_ipk([4.0, 4.0, 4.0]), 4.00)

    def test_happy_path_campuran_int_float(self):
        """Memastikan fungsi menerima kombinasi integer dan float."""
        self.assertEqual(hitung_ipk([3, 4, 3.5]), 3.50)

    # --- EDGE CASES ---
    def test_edge_case_elemen_tunggal(self):
        """Batas: Hanya satu mata kuliah."""
        self.assertEqual(hitung_ipk([3.85]), 3.85)

    def test_edge_case_nilai_terendah_nol(self):
        """Batas: Seluruh nilai bernilai 0.0."""
        self.assertEqual(hitung_ipk([0.0, 0.0]), 0.00)

    def test_edge_case_pembulatan_dua_desimal(self):
        """Batas: Pembulatan floating point periodik."""
        # (3.33 + 3.33 + 3.34) / 3 = 10.0 / 3 = 3.33333... -> 3.33
        self.assertEqual(hitung_ipk([3.33, 3.33, 3.34]), 3.33)

    # --- INVALID INPUT ---
    def test_invalid_input_list_kosong(self):
        """Input tidak valid: List kosong harus memicu ValueError."""
        with self.assertRaises(ValueError) as ctx:
            hitung_ipk([])
        self.assertIn("tidak boleh kosong", str(ctx.exception))

    def test_invalid_input_nilai_di_bawah_nol(self):
        """Input tidak valid: Nilai negatif di luar rentang (<0.0)."""
        with self.assertRaises(ValueError):
            hitung_ipk([3.5, -0.5, 4.0])

    def test_invalid_input_nilai_melebihi_empat(self):
        """Input tidak valid: Nilai melebihi 4.0."""
        with self.assertRaises(ValueError):
            hitung_ipk([3.5, 4.5])

    def test_invalid_input_bukan_list(self):
        """Input tidak valid: Tipe data bukan list harus memicu TypeError."""
        with self.assertRaises(TypeError):
            hitung_ipk("3.5, 4.0")  # type: ignore

    def test_invalid_input_elemen_bukan_angka(self):
        """Input tidak valid: Terdapat elemen string/None dalam list."""
        with self.assertRaises(TypeError):
            hitung_ipk([3.5, "A", 4.0])  # type: ignore


class TestValidasiNIM(unittest.TestCase):
    """Pengujian Unit untuk fungsi validasi_nim()"""

    # --- HAPPY PATH ---
    def test_happy_path_nim_valid(self):
        """NIM 10 digit numerik valid."""
        self.assertTrue(validasi_nim("2024101001"))
        self.assertTrue(validasi_nim("1234567890"))
        self.assertTrue(validasi_nim("2023120046"))

    # --- EDGE CASES ---
    def test_edge_case_semua_angka_nol(self):
        """Batas: 10 karakter angka nol semua."""
        self.assertTrue(validasi_nim("0000000000"))

    def test_edge_case_awalan_nol(self):
        """Batas: 10 karakter dengan awalan nol."""
        self.assertTrue(validasi_nim("0123456789"))

    def test_edge_case_panjang_tepat_sembilan_dan_sebelas(self):
        """Batas: Selisih 1 digit batas panjang (9 digit dan 11 digit)."""
        self.assertFalse(validasi_nim("123456789"))     # 9 digit -> False
        self.assertFalse(validasi_nim("12345678901"))   # 11 digit -> False

    # --- INVALID INPUT ---
    def test_invalid_input_mengandung_huruf(self):
        """Input tidak valid: 10 karakter namun memuat alfabet."""
        self.assertFalse(validasi_nim("20241A1001"))
        self.assertFalse(validasi_nim("ABCDEFGHIJ"))

    def test_invalid_input_mengandung_simbol_atau_spasi(self):
        """Input tidak valid: Mengandung tanda hubung, titik, atau spasi."""
        self.assertFalse(validasi_nim("2024-101001"))
        self.assertFalse(validasi_nim("2024 10100"))
        self.assertFalse(validasi_nim("2024.10100"))

    def test_invalid_input_string_kosong(self):
        """Input tidak valid: String kosong."""
        self.assertFalse(validasi_nim(""))

    def test_invalid_input_tipe_bukan_string(self):
        """Input tidak valid: Tipe integer atau None memicu TypeError."""
        with self.assertRaises(TypeError):
            validasi_nim(2024101001)  # type: ignore
        with self.assertRaises(TypeError):
            validasi_nim(None)        # type: ignore


class TestKonversiNilaiHuruf(unittest.TestCase):
    """Pengujian Unit untuk fungsi konversi_nilai_huruf()"""

    # --- HAPPY PATH ---
    def test_happy_path_nilai_tengah(self):
        """Nilai representatif di tengah rentang masing-masing grade."""
        self.assertEqual(konversi_nilai_huruf(92.5), "A")
        self.assertEqual(konversi_nilai_huruf(82.0), "A-")
        self.assertEqual(konversi_nilai_huruf(77.5), "B+")
        self.assertEqual(konversi_nilai_huruf(72.0), "B")
        self.assertEqual(konversi_nilai_huruf(67.0), "B-")
        self.assertEqual(konversi_nilai_huruf(62.0), "C+")
        self.assertEqual(konversi_nilai_huruf(57.0), "C")
        self.assertEqual(konversi_nilai_huruf(45.0), "D")
        self.assertEqual(konversi_nilai_huruf(20.0), "E")

    # --- EDGE CASES (NILAI BATAS) ---
    def test_edge_case_batas_maksimal_seratus(self):
        """Batas atas absolut: 100.0 menghasilkan A."""
        self.assertEqual(konversi_nilai_huruf(100.0), "A")

    def test_edge_case_batas_minimal_nol(self):
        """Batas bawah absolut: 0.0 menghasilkan E."""
        self.assertEqual(konversi_nilai_huruf(0.0), "E")

    def test_edge_case_ambang_batas_kritis(self):
        """Titik tepat batas dan pecahan tepat di bawah batas."""
        # Batas A (>= 85.0)
        self.assertEqual(konversi_nilai_huruf(85.0), "A")
        self.assertEqual(konversi_nilai_huruf(84.99), "A-")

        # Batas A- (>= 80.0)
        self.assertEqual(konversi_nilai_huruf(80.0), "A-")
        self.assertEqual(konversi_nilai_huruf(79.99), "B+")

        # Batas B+ (>= 75.0)
        self.assertEqual(konversi_nilai_huruf(75.0), "B+")
        self.assertEqual(konversi_nilai_huruf(74.99), "B")

        # Batas D dan E
        self.assertEqual(konversi_nilai_huruf(40.0), "D")
        self.assertEqual(konversi_nilai_huruf(39.99), "E")

    # --- INVALID INPUT ---
    def test_invalid_input_nilai_di_bawah_nol(self):
        """Nilai negatif di luar rentang (<0)."""
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(-1)
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(-0.01)

    def test_invalid_input_nilai_melebihi_seratus(self):
        """Nilai melampaui batas atas (>100)."""
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(100.01)
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(150)

    def test_invalid_input_tipe_data_salah(self):
        """Input non-numerik (string, None, boolean)."""
        with self.assertRaises(TypeError):
            konversi_nilai_huruf("delapan puluh lima")  # type: ignore
        with self.assertRaises(TypeError):
            konversi_nilai_huruf(None)                  # type: ignore
        with self.assertRaises(TypeError):
            konversi_nilai_huruf(True)                  # type: ignore (bool dilarang)


# =====================================================================
# 3. RUNNER UTAMA
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MENJALANKAN SUITE PENGUJIAN UNIT (UNITTEST)")
    print("=" * 70)
    unittest.main(verbosity=2)

