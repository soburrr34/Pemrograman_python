"""
Program: Kalkulator Diskon Biaya Kuliah
Deskripsi: Menghitung diskon biaya SPP berdasarkan:
  - Anak karyawan    : 25%
  - IPK >= 3.8       : 20%
  - IPK >= 3.5       : 15%
  - IPK >= 3.0       : 10%
  - Tepat waktu      : +5%
Catatan: Diskon akademik bersifat bertingkat (ambil yang tertinggi).
         Diskon anak karyawan dan tepat waktu bersifat kumulatif.
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def hitung_diskon(biaya_spp, anak_karyawan, ipk, tepat_waktu):
    """
    Menghitung rincian diskon biaya kuliah.

    Returns:
        dict: rincian semua komponen diskon dan biaya final.
    """
    rincian = []
    total_persen = 0.0

    # 1. Diskon anak karyawan
    if anak_karyawan:
        rincian.append({"keterangan": "Anak Karyawan", "persen": 25.0})
        total_persen += 25.0

    # 2. Diskon akademik (IPK) - ambil yang paling tinggi saja
    if ipk >= 3.8:
        rincian.append({"keterangan": "IPK >= 3.8 (Prestasi Istimewa)", "persen": 20.0})
        total_persen += 20.0
    elif ipk >= 3.5:
        rincian.append({"keterangan": "IPK >= 3.5 (Prestasi Sangat Baik)", "persen": 15.0})
        total_persen += 15.0
    elif ipk >= 3.0:
        rincian.append({"keterangan": "IPK >= 3.0 (Prestasi Baik)", "persen": 10.0})
        total_persen += 10.0

    # 3. Diskon tepat waktu
    if tepat_waktu:
        rincian.append({"keterangan": "Pembayaran Tepat Waktu", "persen": 5.0})
        total_persen += 5.0

    # Batasi maksimum diskon 100%
    total_persen = min(total_persen, 100.0)
    potongan = biaya_spp * (total_persen / 100)
    biaya_final = biaya_spp - potongan

    return {
        "biaya_spp": biaya_spp,
        "rincian_diskon": rincian,
        "total_persen": total_persen,
        "potongan": potongan,
        "biaya_final": biaya_final,
    }


def format_rupiah(angka):
    """Format angka ke format Rupiah."""
    return f"Rp {angka:>15,.2f}".replace(",", ".")


def tampilkan_hasil(hasil):
    """Menampilkan hasil perhitungan diskon."""
    print("\n" + "=" * 58)
    print("     HASIL PERHITUNGAN DISKON BIAYA KULIAH")
    print("=" * 58)
    print(f"  Biaya SPP Awal  : {format_rupiah(hasil['biaya_spp'])}")
    print("-" * 58)
    print("  Diskon yang Berlaku:")

    if hasil["rincian_diskon"]:
        for item in hasil["rincian_diskon"]:
            potongan_item = hasil["biaya_spp"] * (item["persen"] / 100)
            print(
                f"    [{item['persen']:5.1f}%] {item['keterangan']:<32}"
                f"- {format_rupiah(potongan_item)}"
            )
    else:
        print("    Tidak ada diskon yang berlaku.")

    print("-" * 58)
    print(f"  Total Diskon    : {hasil['total_persen']:.1f}%")
    print(f"  Total Potongan  : {format_rupiah(hasil['potongan'])}")
    print("=" * 58)
    print(f"  BIAYA FINAL     : {format_rupiah(hasil['biaya_final'])}")
    print("=" * 58)


def input_ya_tidak(prompt):
    """Menerima input y/n dari pengguna."""
    while True:
        jawaban = input(prompt).strip().lower()
        if jawaban in ("y", "n"):
            return jawaban == "y"
        print("  [!] Masukkan 'y' untuk Ya atau 'n' untuk Tidak.")


def main():
    print("=" * 58)
    print("      KALKULATOR DISKON BIAYA KULIAH")
    print("=" * 58)

    # Input biaya SPP
    while True:
        try:
            biaya_input = input("  Biaya SPP (Rp) : ").strip().replace(".", "").replace(",", "")
            biaya_spp = float(biaya_input)
            if biaya_spp > 0:
                break
            print("  [!] Biaya SPP harus lebih dari 0.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    # Input status anak karyawan
    anak_karyawan = input_ya_tidak("  Anak karyawan? (y/n)            : ")

    # Input IPK
    while True:
        try:
            ipk = float(input("  IPK mahasiswa (0.0 - 4.0)       : "))
            if 0.0 <= ipk <= 4.0:
                break
            print("  [!] IPK harus antara 0.0 - 4.0.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    # Input status pembayaran tepat waktu
    tepat_waktu = input_ya_tidak("  Bayar tepat waktu? (y/n)        : ")

    # Hitung dan tampilkan
    hasil = hitung_diskon(biaya_spp, anak_karyawan, ipk, tepat_waktu)
    tampilkan_hasil(hasil)


if __name__ == "__main__":
    main()
