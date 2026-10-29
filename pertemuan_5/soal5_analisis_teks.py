# ============================================================
# PERTEMUAN 5 - SOAL PRAKTIK 5
# Analisis Teks dari File:
# Frekuensi Kata, Top-10, Hapax Legomena, Type-Token Ratio
# ============================================================

import os
import re
import string


# ─── Utilitas ────────────────────────────────────────────────

def bersihkan_kata(teks):
    """
    Membersihkan teks dan mengembalikan list kata:
    - Ubah ke huruf kecil
    - Hapus tanda baca dan karakter non-alfabet
    - Hilangkan token kosong
    """
    # Hapus tanda baca, ganti dengan spasi
    teks_bersih = re.sub(r"[^\w\s]", " ", teks.lower())
    # Pisahkan kata, hilangkan token kosong dan angka murni
    kata_list = [
        kata for kata in teks_bersih.split()
        if kata and not kata.isdigit()
    ]
    return kata_list


def baca_teks_dari_file(nama_file):
    """
    Membaca isi teks dari file .txt.
    Mengembalikan string isi file.
    """
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"  [!] Gagal membaca file: {e}")
        return None


# ─── Analisis ────────────────────────────────────────────────

def hitung_frekuensi(kata_list):
    """
    (a) Menghitung frekuensi setiap kata menggunakan dictionary.
    Mengembalikan dict {kata: frekuensi}.
    """
    frekuensi = {}
    for kata in kata_list:
        frekuensi[kata] = frekuensi.get(kata, 0) + 1
    return frekuensi


def top_n_kata(frekuensi, n=10):
    """
    (b) Mengembalikan N kata yang paling sering muncul.
    Mengembalikan list of tuple [(kata, frekuensi), ...].
    """
    # Urutkan berdasarkan frekuensi (descending), lalu alfabetis
    return sorted(frekuensi.items(), key=lambda x: (-x[1], x[0]))[:n]


def hapax_legomena(frekuensi):
    """
    (c) Mengidentifikasi hapax legomena:
    kata-kata yang HANYA muncul SATU KALI.
    Menggunakan set comprehension.
    """
    hapax = {kata for kata, freq in frekuensi.items() if freq == 1}
    return hapax


def type_token_ratio(frekuensi, total_kata):
    """
    (d) Menghitung Type-Token Ratio (TTR):
    TTR = jumlah kata unik (type) / total kata (token)
    TTR mendekati 1.0 = kosakata sangat beragam
    TTR mendekati 0.0 = banyak pengulangan kata
    """
    jumlah_type = len(frekuensi)
    if total_kata == 0:
        return 0.0
    return jumlah_type / total_kata


# ─── Tampilan ────────────────────────────────────────────────

def tampilkan_bar_horizontal(kata, frekuensi, maks_freq, lebar=30):
    """Menampilkan bar horizontal sederhana."""
    panjang_bar = int((frekuensi / maks_freq) * lebar)
    bar = "#" * panjang_bar
    return f"{bar:<{lebar}} {frekuensi}"


def tampilkan_hasil(nama_file, kata_list, frekuensi, hasil_top, hapax, ttr):
    garis = "=" * 60

    total_token = len(kata_list)
    total_type  = len(frekuensi)

    print(f"\n{garis}")
    print("       ANALISIS TEKS - HASIL LENGKAP")
    print(garis)
    print(f"  File sumber      : {os.path.basename(nama_file)}")
    print(f"  Total token      : {total_token} kata")
    print(f"  Total type (unik): {total_type} kata")
    print(garis)

    # (a) Cuplikan frekuensi kata (tampilkan 15 besar untuk gambaran umum)
    print("\n  (a) FREKUENSI KATA (15 Besar - ringkasan)")
    print(f"  {'No':<4} {'Kata':<20} {'Bar':<35} Frekuensi")
    print("  " + "-" * 56)
    top15     = sorted(frekuensi.items(), key=lambda x: (-x[1], x[0]))[:15]
    maks_freq = top15[0][1] if top15 else 1
    for i, (kata, freq) in enumerate(top15, 1):
        bar_str = tampilkan_bar_horizontal(kata, freq, maks_freq)
        print(f"  {i:<4} {kata:<20} {bar_str}")

    # (b) Top 10 kata paling sering
    print(f"\n  (b) TOP 10 KATA PALING SERING MUNCUL")
    print(f"  {'Peringkat':<10} {'Kata':<20} {'Frekuensi':>10}")
    print("  " + "-" * 42)
    for i, (kata, freq) in enumerate(hasil_top, 1):
        print(f"  #{i:<9} {kata:<20} {freq:>10}x")

    # (c) Hapax Legomena
    print(f"\n  (c) HAPAX LEGOMENA (kata yang hanya muncul 1 kali)")
    print(f"      Jumlah: {len(hapax)} kata")
    if hapax:
        hapax_terurut = sorted(hapax)
        # Tampilkan dalam baris dengan maksimal 5 kata per baris
        for i in range(0, len(hapax_terurut), 5):
            baris = hapax_terurut[i:i+5]
            print("      " + "  |  ".join(f"{k:<15}" for k in baris))
    else:
        print("      (Tidak ada hapax legomena)")

    # (d) Type-Token Ratio
    print(f"\n  (d) TYPE-TOKEN RATIO (TTR)")
    print(f"      Jumlah type (unik) : {total_type}")
    print(f"      Jumlah token (total): {total_token}")
    print(f"      TTR                 : {ttr:.4f} ({ttr*100:.2f}%)")
    if ttr >= 0.70:
        interpretasi = "Sangat beragam - kosakata kaya"
    elif ttr >= 0.50:
        interpretasi = "Cukup beragam - kosakata normal"
    elif ttr >= 0.30:
        interpretasi = "Sedang - ada pengulangan cukup banyak"
    else:
        interpretasi = "Rendah - banyak pengulangan kata"
    print(f"      Interpretasi       : {interpretasi}")
    print(garis)


def simpan_laporan(nama_file, kata_list, frekuensi, hasil_top, hapax, ttr):
    """Menyimpan hasil analisis ke file teks."""
    nama_output = nama_file.replace(".txt", "_laporan_analisis.txt")
    try:
        with open(nama_output, "w", encoding="utf-8") as f:
            f.write("LAPORAN ANALISIS TEKS\n")
            f.write("=" * 60 + "\n")
            f.write(f"File sumber : {os.path.basename(nama_file)}\n")
            f.write(f"Total token : {len(kata_list)}\n")
            f.write(f"Total type  : {len(frekuensi)}\n\n")

            f.write("TOP 10 KATA:\n")
            for i, (kata, freq) in enumerate(hasil_top, 1):
                f.write(f"  {i}. {kata} ({freq}x)\n")

            f.write(f"\nHAPAX LEGOMENA ({len(hapax)} kata):\n")
            f.write("  " + ", ".join(sorted(hapax)) + "\n")

            f.write(f"\nTYPE-TOKEN RATIO: {ttr:.4f}\n")

            f.write("\nSEMUA FREKUENSI KATA (diurutkan):\n")
            for kata, freq in sorted(frekuensi.items(), key=lambda x: (-x[1], x[0])):
                f.write(f"  {kata:<25} : {freq}\n")

        print(f"\n  [✓] Laporan disimpan ke: {os.path.basename(nama_output)}")
    except Exception as e:
        print(f"\n  [!] Gagal menyimpan laporan: {e}")


# ─── Main ────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   PROGRAM ANALISIS TEKS DARI FILE - PERTEMUAN 5")
    print("=" * 60)

    # Tentukan file yang akan dibaca
    direktori_ini = os.path.dirname(os.path.abspath(__file__))
    file_default  = os.path.join(direktori_ini, "contoh_teks.txt")

    print(f"\n  File default tersedia : contoh_teks.txt")
    print(f"  Letak file            : {direktori_ini}")

    nama_file = input(
        "\n  Masukkan path file teks\n"
        "  (tekan Enter untuk gunakan contoh_teks.txt): "
    ).strip()

    if not nama_file:
        nama_file = file_default

    # Baca file
    print(f"\n  Membaca file: {nama_file} ...")
    teks = baca_teks_dari_file(nama_file)

    if teks is None:
        print(f"  [!] File '{nama_file}' tidak ditemukan!")
        print("  Pastikan file ada di direktori yang benar.")
        return

    if not teks.strip():
        print("  [!] File kosong!")
        return

    # Proses analisis
    print("  Menganalisis teks...")
    kata_list  = bersihkan_kata(teks)              # (a) buat list kata bersih
    frekuensi  = hitung_frekuensi(kata_list)       # (a) hitung frekuensi
    hasil_top  = top_n_kata(frekuensi, n=10)       # (b) top 10
    hapax      = hapax_legomena(frekuensi)          # (c) hapax legomena
    ttr        = type_token_ratio(frekuensi, len(kata_list))  # (d) TTR

    # Tampilkan hasil
    tampilkan_hasil(nama_file, kata_list, frekuensi, hasil_top, hapax, ttr)

    # Tanya apakah ingin simpan laporan
    simpan = input("\n  Simpan laporan ke file? (y/n): ").strip().lower()
    if simpan == "y":
        simpan_laporan(nama_file, kata_list, frekuensi, hasil_top, hapax, ttr)

    print("\n  Program selesai!")


if __name__ == "__main__":
    main()
