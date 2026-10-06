"""
Program: Peringatan Stok Inventaris
Deskripsi: Mengevaluasi status setiap item inventaris, menampilkan
           laporan lengkap dengan prioritas, total nilai, dan statistik.

Status Stok:
  - AMAN      : stok >= batas_aman
  - PERINGATAN: batas_rendah <= stok < batas_aman
  - RENDAH    : 1 <= stok < batas_rendah
  - HABIS     : stok == 0
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Data inventaris (minimal 8 item dengan variasi status)
INVENTARIS = [
    {"kode": "ITM-001", "nama": "Kertas HVS A4",       "satuan": "rim",   "stok": 45, "batas_aman": 30, "batas_rendah": 10, "harga_satuan": 55_000},
    {"kode": "ITM-002", "nama": "Tinta Printer Hitam", "satuan": "botol", "stok": 8,  "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 85_000},
    {"kode": "ITM-003", "nama": "Ballpoint Biru",      "satuan": "lusin", "stok": 3,  "batas_aman": 10, "batas_rendah": 5,  "harga_satuan": 28_000},
    {"kode": "ITM-004", "nama": "Spidol Whiteboard",   "satuan": "set",   "stok": 0,  "batas_aman": 5,  "batas_rendah": 2,  "harga_satuan": 45_000},
    {"kode": "ITM-005", "nama": "Staples No.10",       "satuan": "kotak", "stok": 20, "batas_aman": 10, "batas_rendah": 4,  "harga_satuan": 12_000},
    {"kode": "ITM-006", "nama": "Amplop Coklat",       "satuan": "pack",  "stok": 2,  "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 18_000},
    {"kode": "ITM-007", "nama": "Folder Plastik",      "satuan": "buah",  "stok": 0,  "batas_aman": 20, "batas_rendah": 8,  "harga_satuan": 7_500},
    {"kode": "ITM-008", "nama": "Buku Tulis A5",       "satuan": "lusin", "stok": 12, "batas_aman": 8,  "batas_rendah": 3,  "harga_satuan": 36_000},
    {"kode": "ITM-009", "nama": "Tipe-X Cair",         "satuan": "botol", "stok": 4,  "batas_aman": 10, "batas_rendah": 4,  "harga_satuan": 9_500},
    {"kode": "ITM-010", "nama": "Penggaris 30cm",      "satuan": "buah",  "stok": 25, "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 11_000},
]

# Prioritas: HABIS paling mendesak
PRIORITAS_ORDER = {"HABIS": 1, "RENDAH": 2, "PERINGATAN": 3, "AMAN": 4}


def tentukan_status_stok(item):
    """Mengembalikan string status stok sebuah item."""
    stok = item["stok"]
    if stok == 0:
        return "HABIS"
    elif stok < item["batas_rendah"]:
        return "RENDAH"
    elif stok < item["batas_aman"]:
        return "PERINGATAN"
    else:
        return "AMAN"


def evaluasi_inventaris(inventaris):
    """Menambahkan field 'status' dan 'nilai_stok' ke setiap item."""
    hasil = []
    for item in inventaris:
        item_eval = item.copy()
        item_eval["status"] = tentukan_status_stok(item)
        item_eval["nilai_stok"] = item["stok"] * item["harga_satuan"]
        hasil.append(item_eval)
    hasil.sort(key=lambda x: PRIORITAS_ORDER[x["status"]])
    return hasil


def format_rupiah(angka):
    return f"Rp {angka:>14,.0f}".replace(",", ".")


def label_status(status):
    return {
        "HABIS":      "[XX] HABIS     ",
        "RENDAH":     "[!!] RENDAH    ",
        "PERINGATAN": "[~~] PERINGATAN",
        "AMAN":       "[OK] AMAN      ",
    }[status]


def tampilkan_laporan(inventaris_eval):
    """Menampilkan laporan lengkap inventaris."""
    print("\n" + "=" * 82)
    print("                    LAPORAN PERINGATAN STOK INVENTARIS")
    print("=" * 82)
    print(f"{'Pri':<4} {'Kode':<9} {'Nama Item':<22} {'Satuan':<7} {'Stok':>5}  "
          f"{'Status':<16} {'Nilai Stok':>18}")
    print("-" * 82)

    total_nilai = 0
    for item in inventaris_eval:
        total_nilai += item["nilai_stok"]
        print(
            f"{PRIORITAS_ORDER[item['status']]:<4}"
            f"{item['kode']:<9}"
            f"{item['nama']:<22}"
            f"{item['satuan']:<7}"
            f"{item['stok']:>5}  "
            f"{label_status(item['status']):<16}"
            f"  {format_rupiah(item['nilai_stok']):>16}"
        )

    print("=" * 82)
    print(f"  TOTAL NILAI INVENTARIS  : {format_rupiah(total_nilai)}")
    print("=" * 82)


def tampilkan_statistik(inventaris_eval):
    """Menampilkan ringkasan statistik."""
    total = len(inventaris_eval)
    hitung = {"AMAN": 0, "PERINGATAN": 0, "RENDAH": 0, "HABIS": 0}
    for item in inventaris_eval:
        hitung[item["status"]] += 1

    print("\n" + "=" * 55)
    print("           RINGKASAN STATISTIK STOK")
    print("=" * 55)
    print(f"  Total Item           : {total}")
    print(f"  {'Status':<20} {'Jumlah':>6}  {'Persentase':>10}")
    print("-" * 55)
    for status in ["AMAN", "PERINGATAN", "RENDAH", "HABIS"]:
        jumlah = hitung[status]
        persen = (jumlah / total * 100) if total > 0 else 0
        print(f"  {label_status(status):<20} {jumlah:>6}  {persen:>9.1f}%")
    print("-" * 55)

    perlu_restock = hitung["HABIS"] + hitung["RENDAH"] + hitung["PERINGATAN"]
    print(f"  Perlu Restock        : {perlu_restock} item ({perlu_restock/total*100:.1f}%)")
    print("=" * 55)

    print("\n  REKOMENDASI RESTOCK (Prioritas Tinggi):")
    print("-" * 55)
    ada_restock = False
    for item in inventaris_eval:
        if item["status"] in ("HABIS", "RENDAH"):
            kebutuhan = item["batas_aman"] - item["stok"]
            print(f"  [{item['kode']}] {item['nama']}")
            print(f"       Stok saat ini : {item['stok']} {item['satuan']}")
            print(f"       Perlu tambah  : {kebutuhan} {item['satuan']}")
            ada_restock = True
    if not ada_restock:
        print("  Semua item dalam kondisi baik.")
    print("=" * 55)


def main():
    print("=" * 82)
    print("             SISTEM PERINGATAN STOK INVENTARIS")
    print("=" * 82)

    inventaris_eval = evaluasi_inventaris(INVENTARIS)
    tampilkan_laporan(inventaris_eval)
    tampilkan_statistik(inventaris_eval)


if __name__ == "__main__":
    main()
