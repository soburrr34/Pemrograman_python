"""
Program: Validasi Data Mahasiswa
Deskripsi: Memvalidasi data mahasiswa meliputi:
  - NIM       : 10 digit angka, tahun pada digit 1-4 antara 2000-2037
  - IPK       : float antara 0.0 - 4.0
  - SKS       : integer antara 0 - 24
  - Semester  : integer antara 1 - 14

Fungsi validasi_data_mahasiswa() mengembalikan list error jika ada data tidak valid.
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ======================================================================
#  FUNGSI-FUNGSI VALIDASI
# ======================================================================

def validasi_nim(nim: str) -> list:
    """
    Validasi NIM mahasiswa.
    Aturan:
      - Harus tepat 10 karakter
      - Semua karakter angka (digit)
      - 4 digit pertama = tahun masuk (2000 - 2037)

    Returns:
        list: Daftar pesan error. Kosong jika valid.
    """
    errors = []

    if not nim:
        errors.append("NIM tidak boleh kosong.")
        return errors

    if len(nim) != 10:
        errors.append(f"NIM harus tepat 10 digit (saat ini {len(nim)} karakter).")

    if not nim.isdigit():
        errors.append("NIM harus terdiri dari angka saja (0-9).")
    elif len(nim) >= 4:
        # Validasi tahun hanya jika panjang setidaknya 4 karakter
        tahun = int(nim[:4])
        if not (2000 <= tahun <= 2037):
            errors.append(
                f"4 digit pertama NIM menunjukkan tahun masuk ({tahun}), "
                f"harus antara 2000 - 2037."
            )

    return errors


def validasi_ipk(ipk_str: str) -> tuple:
    """
    Validasi IPK.
    Aturan: nilai float antara 0.0 - 4.0.

    Returns:
        tuple: (list_error, nilai_float_atau_None)
    """
    errors = []
    nilai = None

    if not ipk_str.strip():
        errors.append("IPK tidak boleh kosong.")
        return errors, nilai

    try:
        nilai = float(ipk_str)
    except ValueError:
        errors.append(f"IPK '{ipk_str}' bukan angka desimal yang valid.")
        return errors, None

    if not (0.0 <= nilai <= 4.0):
        errors.append(f"IPK {nilai} di luar rentang yang diizinkan (0.0 - 4.0).")
        nilai = None

    return errors, nilai


def validasi_sks(sks_str: str) -> tuple:
    """
    Validasi SKS.
    Aturan: integer antara 0 - 24.

    Returns:
        tuple: (list_error, nilai_int_atau_None)
    """
    errors = []
    nilai = None

    if not sks_str.strip():
        errors.append("SKS tidak boleh kosong.")
        return errors, nilai

    try:
        nilai = int(sks_str)
    except ValueError:
        errors.append(f"SKS '{sks_str}' bukan bilangan bulat yang valid.")
        return errors, None

    if not (0 <= nilai <= 24):
        errors.append(f"SKS {nilai} di luar rentang yang diizinkan (0 - 24).")
        nilai = None

    return errors, nilai


def validasi_semester(semester_str: str) -> tuple:
    """
    Validasi Semester.
    Aturan: integer antara 1 - 14.

    Returns:
        tuple: (list_error, nilai_int_atau_None)
    """
    errors = []
    nilai = None

    if not semester_str.strip():
        errors.append("Semester tidak boleh kosong.")
        return errors, nilai

    try:
        nilai = int(semester_str)
    except ValueError:
        errors.append(f"Semester '{semester_str}' bukan bilangan bulat yang valid.")
        return errors, None

    if not (1 <= nilai <= 14):
        errors.append(f"Semester {nilai} di luar rentang yang diizinkan (1 - 14).")
        nilai = None

    return errors, nilai


def validasi_data_mahasiswa(nim: str, ipk_str: str, sks_str: str, semester_str: str) -> list:
    """
    Fungsi utama validasi data mahasiswa.
    Mengumpulkan semua error dari keempat field.

    Args:
        nim          : string NIM
        ipk_str      : string IPK (sebelum konversi)
        sks_str      : string SKS (sebelum konversi)
        semester_str : string Semester (sebelum konversi)

    Returns:
        list: Daftar semua pesan error. Kosong jika semua data valid.
    """
    semua_error = []

    for e in validasi_nim(nim):
        semua_error.append(f"[NIM]      {e}")

    for e in validasi_ipk(ipk_str)[0]:
        semua_error.append(f"[IPK]      {e}")

    for e in validasi_sks(sks_str)[0]:
        semua_error.append(f"[SKS]      {e}")

    for e in validasi_semester(semester_str)[0]:
        semua_error.append(f"[Semester] {e}")

    return semua_error


# ======================================================================
#  PROGRAM UTAMA
# ======================================================================

def tampilkan_contoh():
    print("\n  Format NIM yang benar  : 2024010001")
    print("  Penjelasan             : [2024][01][0001]")
    print("                           tahun  jur  nomor")
    print("  Tahun yang diterima    : 2000 - 2037")


def main():
    print("=" * 60)
    print("         PROGRAM VALIDASI DATA MAHASISWA")
    print("=" * 60)
    tampilkan_contoh()

    while True:
        print("\n" + "-" * 60)
        print("  Masukkan Data Mahasiswa (tekan Enter untuk kosong):")
        print("-" * 60)

        nim      = input("  NIM      (10 digit, tahun 2000-2037) : ").strip()
        ipk_str  = input("  IPK      (0.0 - 4.0)                 : ").strip()
        sks_str  = input("  SKS      (0 - 24)                    : ").strip()
        sem_str  = input("  Semester (1 - 14)                    : ").strip()

        print("\n" + "=" * 60)
        print("  HASIL VALIDASI")
        print("=" * 60)

        errors = validasi_data_mahasiswa(nim, ipk_str, sks_str, sem_str)

        if errors:
            print(f"  Status : [GAGAL] DATA TIDAK VALID ({len(errors)} kesalahan)")
            print("-" * 60)
            for i, err in enumerate(errors, 1):
                print(f"  {i}. {err}")
        else:
            _, ipk      = validasi_ipk(ipk_str)
            _, sks      = validasi_sks(sks_str)
            _, semester = validasi_semester(sem_str)

            print("  Status : [VALID] SEMUA DATA VALID")
            print("-" * 60)
            print(f"  NIM      : {nim}   (Tahun masuk: {nim[:4]})")
            print(f"  IPK      : {ipk:.2f}")
            print(f"  SKS      : {sks}")
            print(f"  Semester : {semester}")

        print("=" * 60)

        ulang = input("\n  Validasi data lain? (y/n) : ").strip().lower()
        if ulang != "y":
            print("\n  Program selesai.\n")
            break


if __name__ == "__main__":
    main()
