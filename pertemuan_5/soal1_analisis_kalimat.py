# ============================================================
# PERTEMUAN 5 - SOAL PRAKTIK 1
# Analisis Kalimat: Jumlah Kata, Karakter, Kata Terpanjang,
# dan Title Case
# ============================================================

def analisis_kalimat(kalimat):
    """
    Fungsi untuk menganalisis sebuah kalimat:
    - Menghitung jumlah kata
    - Menghitung jumlah karakter (tanpa spasi)
    - Menampilkan kata terpanjang
    - Menampilkan kalimat dalam title case
    """

    # (a) Hitung jumlah kata
    daftar_kata = kalimat.split()
    jumlah_kata = len(daftar_kata)

    # (b) Hitung jumlah karakter (termasuk spasi dan tidak termasuk spasi)
    jumlah_karakter_total    = len(kalimat)
    jumlah_karakter_tanpa_spasi = len(kalimat.replace(" ", ""))

    # (c) Cari kata terpanjang (jika ada lebih dari satu, tampilkan semua)
    if daftar_kata:
        panjang_max = max(len(kata) for kata in daftar_kata)
        kata_terpanjang = [kata for kata in daftar_kata if len(kata) == panjang_max]
    else:
        kata_terpanjang = []
        panjang_max = 0

    # (d) Title case
    kalimat_title_case = kalimat.title()

    return {
        "jumlah_kata"              : jumlah_kata,
        "jumlah_karakter_total"    : jumlah_karakter_total,
        "jumlah_karakter_tanpa_spasi": jumlah_karakter_tanpa_spasi,
        "kata_terpanjang"          : kata_terpanjang,
        "panjang_max"              : panjang_max,
        "kalimat_title_case"       : kalimat_title_case,
    }


def tampilkan_hasil(kalimat, hasil):
    """Menampilkan hasil analisis secara terformat."""
    garis = "=" * 55
    print(f"\n{garis}")
    print("       HASIL ANALISIS KALIMAT")
    print(garis)
    print(f"  Kalimat asli   : {kalimat}")
    print(garis)
    print(f"  (a) Jumlah kata                : {hasil['jumlah_kata']} kata")
    print(f"  (b) Jumlah karakter (dengan spasi)   : {hasil['jumlah_karakter_total']} karakter")
    print(f"      Jumlah karakter (tanpa spasi)    : {hasil['jumlah_karakter_tanpa_spasi']} karakter")
    print(f"  (c) Kata terpanjang ({hasil['panjang_max']} huruf) : {', '.join(hasil['kata_terpanjang'])}")
    print(f"  (d) Kalimat title case         : {hasil['kalimat_title_case']}")
    print(garis)


def main():
    print("=" * 55)
    print("     PROGRAM ANALISIS KALIMAT - PERTEMUAN 5")
    print("=" * 55)

    # Input dari pengguna
    kalimat = input("\nMasukkan sebuah kalimat: ").strip()

    if not kalimat:
        print("[!] Kalimat tidak boleh kosong!")
        return

    hasil = analisis_kalimat(kalimat)
    tampilkan_hasil(kalimat, hasil)


if __name__ == "__main__":
    main()
