"""
Program: Ringkasan Algoritma Tiga Studi Kasus
Deskripsi: Menghitung dan menampilkan ringkasan dalam format tabel:
  (a) Persentase mahasiswa aktif vs tidak aktif
  (b) Rata-rata diskon yang diberikan
  (c) Persentase item inventaris yang perlu restock
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ======================================================================
#  DATA SAMPEL
# ======================================================================

# (a) Data mahasiswa sampel
DATA_MAHASISWA = [
    {"nim": "2021010001", "nama": "Andi Pratama",      "ipk": 3.75, "sks": 22},
    {"nim": "2021010002", "nama": "Budi Santoso",      "ipk": 2.50, "sks": 20},
    {"nim": "2022010003", "nama": "Citra Dewi",        "ipk": 1.80, "sks": 18},
    {"nim": "2022010004", "nama": "Dian Rahayu",       "ipk": 1.20, "sks": 15},
    {"nim": "2023010005", "nama": "Eko Wijaya",        "ipk": 3.90, "sks": 24},
    {"nim": "2023010006", "nama": "Fitri Handayani",   "ipk": 2.10, "sks": 12},
    {"nim": "2024010007", "nama": "Gilang Ramadan",    "ipk": 0.80, "sks": 10},
    {"nim": "2024010008", "nama": "Hana Pertiwi",      "ipk": 3.20, "sks": 21},
    {"nim": "2025010009", "nama": "Ivan Kurniawan",    "ipk": 1.60, "sks": 19},
    {"nim": "2025010010", "nama": "Jasmine Anggraini", "ipk": 2.95, "sks": 18},
]

# (b) Data transaksi diskon sampel
DATA_DISKON = [
    {"biaya_spp": 5_000_000, "anak_karyawan": True,  "ipk": 3.90, "tepat_waktu": True},
    {"biaya_spp": 5_000_000, "anak_karyawan": False, "ipk": 3.60, "tepat_waktu": True},
    {"biaya_spp": 4_500_000, "anak_karyawan": False, "ipk": 3.10, "tepat_waktu": False},
    {"biaya_spp": 4_500_000, "anak_karyawan": True,  "ipk": 2.80, "tepat_waktu": True},
    {"biaya_spp": 6_000_000, "anak_karyawan": False, "ipk": 2.50, "tepat_waktu": False},
    {"biaya_spp": 6_000_000, "anak_karyawan": False, "ipk": 1.90, "tepat_waktu": True},
    {"biaya_spp": 5_500_000, "anak_karyawan": True,  "ipk": 3.80, "tepat_waktu": False},
    {"biaya_spp": 5_500_000, "anak_karyawan": False, "ipk": 3.50, "tepat_waktu": True},
]

# (c) Data inventaris sampel
DATA_INVENTARIS = [
    {"kode": "ITM-001", "nama": "Kertas HVS A4",       "stok": 45, "batas_aman": 30, "batas_rendah": 10, "harga_satuan": 55_000},
    {"kode": "ITM-002", "nama": "Tinta Printer Hitam", "stok": 8,  "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 85_000},
    {"kode": "ITM-003", "nama": "Ballpoint Biru",      "stok": 3,  "batas_aman": 10, "batas_rendah": 5,  "harga_satuan": 28_000},
    {"kode": "ITM-004", "nama": "Spidol Whiteboard",   "stok": 0,  "batas_aman": 5,  "batas_rendah": 2,  "harga_satuan": 45_000},
    {"kode": "ITM-005", "nama": "Staples No.10",       "stok": 20, "batas_aman": 10, "batas_rendah": 4,  "harga_satuan": 12_000},
    {"kode": "ITM-006", "nama": "Amplop Coklat",       "stok": 2,  "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 18_000},
    {"kode": "ITM-007", "nama": "Folder Plastik",      "stok": 0,  "batas_aman": 20, "batas_rendah": 8,  "harga_satuan": 7_500},
    {"kode": "ITM-008", "nama": "Buku Tulis A5",       "stok": 12, "batas_aman": 8,  "batas_rendah": 3,  "harga_satuan": 36_000},
    {"kode": "ITM-009", "nama": "Tipe-X Cair",         "stok": 4,  "batas_aman": 10, "batas_rendah": 4,  "harga_satuan": 9_500},
    {"kode": "ITM-010", "nama": "Penggaris 30cm",      "stok": 25, "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 11_000},
]


# ======================================================================
#  FUNGSI PERHITUNGAN
# ======================================================================

def hitung_status_mahasiswa(data):
    """
    (a) Menghitung distribusi status mahasiswa.
    Aturan:
      - Aktif       : IPK >= 2.0 dan SKS >= 18
      - Peringatan  : 1.5 <= IPK < 2.0  ATAU  IPK >= 2.0 dan SKS < 18
      - Tidak Aktif : IPK < 1.5
    """
    hitung = {"Aktif": 0, "Peringatan": 0, "Tidak Aktif": 0}
    for m in data:
        ipk, sks = m["ipk"], m["sks"]
        if ipk < 1.5:
            hitung["Tidak Aktif"] += 1
        elif ipk < 2.0:
            hitung["Peringatan"] += 1
        elif ipk >= 2.0 and sks >= 18:
            hitung["Aktif"] += 1
        else:
            hitung["Peringatan"] += 1
    return hitung, len(data)


def hitung_rata_diskon(data):
    """
    (b) Menghitung rata-rata diskon dari kumpulan data transaksi.
    """
    total_diskon = 0.0
    rincian = []
    for d in data:
        persen = 0.0
        if d["anak_karyawan"]:
            persen += 25.0
        if d["ipk"] >= 3.8:
            persen += 20.0
        elif d["ipk"] >= 3.5:
            persen += 15.0
        elif d["ipk"] >= 3.0:
            persen += 10.0
        if d["tepat_waktu"]:
            persen += 5.0
        persen = min(persen, 100.0)
        potongan = d["biaya_spp"] * persen / 100
        total_diskon += persen
        rincian.append({
            "biaya_spp":  d["biaya_spp"],
            "persen":     persen,
            "potongan":   potongan,
            "biaya_final": d["biaya_spp"] - potongan,
        })
    rata_rata = total_diskon / len(data) if data else 0.0
    return rata_rata, rincian


def hitung_restock_inventaris(data):
    """
    (c) Menghitung persentase item yang perlu restock.
    Restock = HABIS + RENDAH + PERINGATAN.
    """
    hitung = {"AMAN": 0, "PERINGATAN": 0, "RENDAH": 0, "HABIS": 0}
    for item in data:
        s = item["stok"]
        if s == 0:
            hitung["HABIS"] += 1
        elif s < item["batas_rendah"]:
            hitung["RENDAH"] += 1
        elif s < item["batas_aman"]:
            hitung["PERINGATAN"] += 1
        else:
            hitung["AMAN"] += 1
    total = len(data)
    perlu = hitung["HABIS"] + hitung["RENDAH"] + hitung["PERINGATAN"]
    persen = (perlu / total * 100) if total > 0 else 0.0
    return hitung, total, perlu, persen


# ======================================================================
#  FUNGSI TAMPILAN TABEL
# ======================================================================

def garis(lebar=72, karakter="="):
    print(karakter * lebar)


def tampilkan_tabel_a(hitung_mhs, total_mhs):
    """Tabel (a): Distribusi Status Mahasiswa."""
    garis()
    print("  (A) RINGKASAN STATUS MAHASISWA")
    garis()
    print(f"  {'Status':<20} {'Jml':>5}  {'Persentase':>11}  Bar Chart")
    garis(72, "-")

    label_ikon = {
        "Aktif":       "[OK]",
        "Peringatan":  "[!!]",
        "Tidak Aktif": "[XX]",
    }
    for status, jumlah in hitung_mhs.items():
        persen = (jumlah / total_mhs * 100) if total_mhs > 0 else 0
        bar    = "#" * int(persen / 5)
        ikon   = label_ikon[status]
        print(f"  {ikon} {status:<16} {jumlah:>5}  {persen:>10.1f}%  {bar}")

    garis(72, "-")
    aktif     = hitung_mhs["Aktif"]
    peringatan = hitung_mhs["Peringatan"]
    tidak_aktif = hitung_mhs["Tidak Aktif"]
    persen_aktif = (aktif / total_mhs * 100) if total_mhs > 0 else 0
    persen_masalah = 100 - persen_aktif

    print(f"  Total Mahasiswa          : {total_mhs}")
    print(f"  Mahasiswa Aktif          : {aktif} dari {total_mhs} ({persen_aktif:.1f}%)")
    print(f"  Mahasiswa Bermasalah     : {peringatan + tidak_aktif} dari {total_mhs} ({persen_masalah:.1f}%)")
    garis()


def format_rupiah(angka):
    return f"Rp {angka:>13,.0f}".replace(",", ".")


def tampilkan_tabel_b(rata_diskon, rincian_diskon):
    """Tabel (b): Rincian Diskon per Transaksi."""
    garis()
    print("  (B) RINGKASAN DISKON BIAYA KULIAH")
    garis()
    print(f"  {'No':<4} {'SPP Awal':>16}  {'Diskon':>7}  {'Potongan':>16}  {'SPP Final':>16}")
    garis(72, "-")

    for i, d in enumerate(rincian_diskon, 1):
        spp   = format_rupiah(d["biaya_spp"])
        pot   = format_rupiah(d["potongan"])
        final = format_rupiah(d["biaya_final"])
        print(f"  {i:<4} {spp}  {d['persen']:>6.1f}%  {pot}  {final}")

    garis(72, "-")
    diskon_min = min(d["persen"] for d in rincian_diskon)
    diskon_max = max(d["persen"] for d in rincian_diskon)
    tanpa_diskon = sum(1 for d in rincian_diskon if d["persen"] == 0)
    print(f"  Rata-rata Diskon : {rata_diskon:.2f}%")
    print(f"  Diskon Minimum   : {diskon_min:.1f}%   |   Diskon Maksimum : {diskon_max:.1f}%")
    print(f"  Tanpa Diskon     : {tanpa_diskon} transaksi")
    garis()


def tampilkan_tabel_c(hitung_inv, total_inv, perlu_restock, persen_restock):
    """Tabel (c): Status Stok Inventaris."""
    garis()
    print("  (C) RINGKASAN STATUS STOK INVENTARIS")
    garis()
    print(f"  {'Status':<16} {'Jml':>5}  {'Persentase':>11}  Bar Chart")
    garis(72, "-")

    label_ikon = {
        "AMAN":       "[OK]",
        "PERINGATAN": "[~~]",
        "RENDAH":     "[!!]",
        "HABIS":      "[XX]",
    }
    for status in ["AMAN", "PERINGATAN", "RENDAH", "HABIS"]:
        jumlah = hitung_inv[status]
        persen = (jumlah / total_inv * 100) if total_inv > 0 else 0
        bar    = "#" * int(persen / 5)
        ikon   = label_ikon[status]
        print(f"  {ikon} {status:<12} {jumlah:>5}  {persen:>10.1f}%  {bar}")

    garis(72, "-")
    persen_aman = 100 - persen_restock
    print(f"  Total Item        : {total_inv}")
    print(f"  Item Aman         : {hitung_inv['AMAN']} dari {total_inv} ({persen_aman:.1f}%)")
    print(f"  Item Perlu Restock: {perlu_restock} dari {total_inv} ({persen_restock:.1f}%)")
    garis()


def main():
    print()
    garis()
    print("          RINGKASAN ALGORITMA TIGA STUDI KASUS")
    garis()
    print(f"  Data mahasiswa  : {len(DATA_MAHASISWA)} orang")
    print(f"  Data diskon     : {len(DATA_DISKON)} transaksi")
    print(f"  Data inventaris : {len(DATA_INVENTARIS)} item")
    garis()

    # Hitung ketiga studi kasus
    hitung_mhs, total_mhs = hitung_status_mahasiswa(DATA_MAHASISWA)
    rata_diskon, rincian_diskon = hitung_rata_diskon(DATA_DISKON)
    hitung_inv, total_inv, perlu_restock, persen_restock = hitung_restock_inventaris(DATA_INVENTARIS)

    # Tampilkan tabel
    print()
    tampilkan_tabel_a(hitung_mhs, total_mhs)
    print()
    tampilkan_tabel_b(rata_diskon, rincian_diskon)
    print()
    tampilkan_tabel_c(hitung_inv, total_inv, perlu_restock, persen_restock)

    # Kesimpulan akhir
    print()
    garis()
    print("  KESIMPULAN KESELURUHAN")
    garis()
    persen_aktif = (hitung_mhs["Aktif"] / total_mhs * 100) if total_mhs > 0 else 0
    print(f"  (a) {persen_aktif:.1f}% mahasiswa berstatus Aktif.")
    print(f"  (b) Rata-rata diskon biaya kuliah sebesar {rata_diskon:.2f}%.")
    print(f"  (c) {persen_restock:.1f}% item inventaris memerlukan restock.")
    garis()
    print()


if __name__ == "__main__":
    main()
