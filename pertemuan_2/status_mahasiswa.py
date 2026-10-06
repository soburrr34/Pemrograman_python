"""
Program: Status Mahasiswa
Deskripsi: Menerima data 5 mahasiswa dan menampilkan laporan status
           berdasarkan IPK dan SKS.
Aturan:
  - Aktif       : IPK >= 2.0 dan SKS >= 18
  - Peringatan  : 1.5 <= IPK < 2.0  ATAU  IPK >= 2.0 dan SKS < 18
  - Tidak Aktif : IPK < 1.5
"""

import io, sys

# Paksa encoding UTF-8 agar karakter khusus tampil di semua terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def tentukan_status(ipk, sks):
    """Menentukan status mahasiswa berdasarkan IPK dan SKS."""
    if ipk < 1.5:
        return "Tidak Aktif"
    elif 1.5 <= ipk < 2.0:
        return "Peringatan"
    elif ipk >= 2.0 and sks >= 18:
        return "Aktif"
    else:
        return "Peringatan"


def input_mahasiswa(nomor):
    """Menerima input data satu mahasiswa."""
    print(f"\n{'='*40}")
    print(f"  Data Mahasiswa ke-{nomor}")
    print(f"{'='*40}")

    while True:
        nim = input("  NIM         : ").strip()
        if nim:
            break
        print("  [!] NIM tidak boleh kosong.")

    while True:
        nama = input("  Nama        : ").strip()
        if nama:
            break
        print("  [!] Nama tidak boleh kosong.")

    while True:
        try:
            ipk = float(input("  IPK (0-4.0) : "))
            if 0.0 <= ipk <= 4.0:
                break
            print("  [!] IPK harus antara 0.0 - 4.0.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    while True:
        try:
            sks = int(input("  SKS (0-24)  : "))
            if 0 <= sks <= 24:
                break
            print("  [!] SKS harus antara 0 - 24.")
        except ValueError:
            print("  [!] Masukkan bilangan bulat yang valid.")

    return {"nim": nim, "nama": nama, "ipk": ipk, "sks": sks}


def tampilkan_laporan(daftar_mahasiswa):
    """Menampilkan laporan status seluruh mahasiswa."""
    print("\n")
    print("=" * 70)
    print("                   LAPORAN STATUS MAHASISWA")
    print("=" * 70)
    print(f"{'No':<4} {'NIM':<12} {'Nama':<20} {'IPK':<6} {'SKS':<5} {'Status'}")
    print("-" * 70)

    hitung = {"Aktif": 0, "Peringatan": 0, "Tidak Aktif": 0}

    for i, mhs in enumerate(daftar_mahasiswa, start=1):
        status = tentukan_status(mhs["ipk"], mhs["sks"])
        hitung[status] += 1

        ikon = {"Aktif": "[OK]", "Peringatan": "[!!]", "Tidak Aktif": "[XX]"}[status]

        print(
            f"{i:<4} {mhs['nim']:<12} {mhs['nama']:<20} "
            f"{mhs['ipk']:<6.2f} {mhs['sks']:<5} {ikon} {status}"
        )

    print("-" * 70)
    print("\n  RINGKASAN:")
    print(f"    Aktif       : {hitung['Aktif']} mahasiswa")
    print(f"    Peringatan  : {hitung['Peringatan']} mahasiswa")
    print(f"    Tidak Aktif : {hitung['Tidak Aktif']} mahasiswa")
    print("=" * 70)


def main():
    print("=" * 70)
    print("          PROGRAM STATUS MAHASISWA")
    print("=" * 70)
    print("  Silakan masukkan data 5 mahasiswa.\n")

    JUMLAH_MAHASISWA = 5
    daftar_mahasiswa = []

    for i in range(1, JUMLAH_MAHASISWA + 1):
        data = input_mahasiswa(i)
        daftar_mahasiswa.append(data)

    tampilkan_laporan(daftar_mahasiswa)


if __name__ == "__main__":
    main()
