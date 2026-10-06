"""
Program: Menu Interaktif SI Mahasiswa
Deskripsi: Menggabungkan tiga studi kasus dalam satu menu interaktif:
  (1) Cek Status Mahasiswa
  (2) Hitung Diskon Biaya Kuliah
  (3) Cek Peringatan Stok
  (0) Keluar
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ======================================================================
#  MODUL 1 - STATUS MAHASISWA
# ======================================================================

def tentukan_status_mahasiswa(ipk, sks):
    """Menentukan status mahasiswa berdasarkan IPK dan SKS."""
    if ipk < 1.5:
        return "Tidak Aktif"
    elif ipk < 2.0:
        return "Peringatan"
    elif ipk >= 2.0 and sks >= 18:
        return "Aktif"
    else:
        return "Peringatan"


def menu_status_mahasiswa():
    """Submenu cek status mahasiswa."""
    print("\n" + "=" * 60)
    print("        CEK STATUS MAHASISWA")
    print("=" * 60)

    while True:
        try:
            jumlah = int(input("  Jumlah mahasiswa yang akan dicek (1-20): "))
            if 1 <= jumlah <= 20:
                break
            print("  [!] Masukkan angka antara 1 - 20.")
        except ValueError:
            print("  [!] Masukkan bilangan bulat.")

    daftar = []
    for i in range(1, jumlah + 1):
        print(f"\n  --- Mahasiswa ke-{i} ---")

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
                print("  [!] IPK harus 0.0 - 4.0.")
            except ValueError:
                print("  [!] Masukkan angka desimal.")

        while True:
            try:
                sks = int(input("  SKS (0-24)  : "))
                if 0 <= sks <= 24:
                    break
                print("  [!] SKS harus 0 - 24.")
            except ValueError:
                print("  [!] Masukkan bilangan bulat.")

        daftar.append({"nim": nim, "nama": nama, "ipk": ipk, "sks": sks})

    print("\n" + "=" * 70)
    print("                   LAPORAN STATUS MAHASISWA")
    print("=" * 70)
    print(f"{'No':<4} {'NIM':<12} {'Nama':<20} {'IPK':<6} {'SKS':<5} Status")
    print("-" * 70)

    hitung = {"Aktif": 0, "Peringatan": 0, "Tidak Aktif": 0}
    for idx, m in enumerate(daftar, 1):
        st = tentukan_status_mahasiswa(m["ipk"], m["sks"])
        hitung[st] += 1
        ikon = {"Aktif": "[OK]", "Peringatan": "[!!]", "Tidak Aktif": "[XX]"}[st]
        print(f"{idx:<4} {m['nim']:<12} {m['nama']:<20} {m['ipk']:<6.2f} {m['sks']:<5} {ikon} {st}")

    print("-" * 70)
    print(f"  Aktif: {hitung['Aktif']}  |  Peringatan: {hitung['Peringatan']}  |  Tidak Aktif: {hitung['Tidak Aktif']}")
    print("=" * 70)


# ======================================================================
#  MODUL 2 - DISKON BIAYA KULIAH
# ======================================================================

def hitung_diskon(biaya_spp, anak_karyawan, ipk, tepat_waktu):
    """Menghitung diskon biaya kuliah."""
    rincian = []
    total_persen = 0.0

    if anak_karyawan:
        rincian.append({"keterangan": "Anak Karyawan", "persen": 25.0})
        total_persen += 25.0

    if ipk >= 3.8:
        rincian.append({"keterangan": "IPK >= 3.8 (Istimewa)", "persen": 20.0})
        total_persen += 20.0
    elif ipk >= 3.5:
        rincian.append({"keterangan": "IPK >= 3.5 (Sangat Baik)", "persen": 15.0})
        total_persen += 15.0
    elif ipk >= 3.0:
        rincian.append({"keterangan": "IPK >= 3.0 (Baik)", "persen": 10.0})
        total_persen += 10.0

    if tepat_waktu:
        rincian.append({"keterangan": "Pembayaran Tepat Waktu", "persen": 5.0})
        total_persen += 5.0

    total_persen = min(total_persen, 100.0)
    potongan = biaya_spp * (total_persen / 100)
    return {
        "biaya_spp": biaya_spp,
        "rincian_diskon": rincian,
        "total_persen": total_persen,
        "potongan": potongan,
        "biaya_final": biaya_spp - potongan,
    }


def input_ya_tidak(prompt):
    """Input validasi y/n."""
    while True:
        jawaban = input(prompt).strip().lower()
        if jawaban in ("y", "n"):
            return jawaban == "y"
        print("  [!] Masukkan 'y' (Ya) atau 'n' (Tidak).")


def format_rupiah(angka):
    return f"Rp {angka:>14,.0f}".replace(",", ".")


def menu_diskon_biaya():
    """Submenu kalkulator diskon biaya kuliah."""
    print("\n" + "=" * 58)
    print("        KALKULATOR DISKON BIAYA KULIAH")
    print("=" * 58)

    while True:
        try:
            biaya_spp = float(
                input("  Biaya SPP (Rp)            : ").strip().replace(".", "").replace(",", "")
            )
            if biaya_spp > 0:
                break
            print("  [!] Biaya harus lebih dari 0.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    anak_karyawan = input_ya_tidak("  Anak karyawan? (y/n)     : ")

    while True:
        try:
            ipk = float(input("  IPK (0.0 - 4.0)          : "))
            if 0.0 <= ipk <= 4.0:
                break
            print("  [!] IPK harus 0.0 - 4.0.")
        except ValueError:
            print("  [!] Masukkan angka desimal.")

    tepat_waktu = input_ya_tidak("  Bayar tepat waktu? (y/n) : ")

    hasil = hitung_diskon(biaya_spp, anak_karyawan, ipk, tepat_waktu)

    print("\n" + "=" * 58)
    print("          HASIL PERHITUNGAN DISKON")
    print("=" * 58)
    print(f"  Biaya SPP Awal  : {format_rupiah(hasil['biaya_spp'])}")
    print("-" * 58)
    if hasil["rincian_diskon"]:
        for d in hasil["rincian_diskon"]:
            pot = hasil["biaya_spp"] * d["persen"] / 100
            print(f"  [{d['persen']:4.1f}%] {d['keterangan']:<30} -{format_rupiah(pot)}")
    else:
        print("  Tidak ada diskon.")
    print("-" * 58)
    print(f"  Total Diskon    : {hasil['total_persen']:.1f}%  ({format_rupiah(hasil['potongan'])})")
    print("=" * 58)
    print(f"  BIAYA FINAL     : {format_rupiah(hasil['biaya_final'])}")
    print("=" * 58)


# ======================================================================
#  MODUL 3 - PERINGATAN STOK
# ======================================================================

INVENTARIS_DEFAULT = [
    {"kode": "ITM-001", "nama": "Kertas HVS A4",       "satuan": "rim",   "stok": 45, "batas_aman": 30, "batas_rendah": 10, "harga_satuan": 55_000},
    {"kode": "ITM-002", "nama": "Tinta Printer Hitam", "satuan": "botol", "stok": 8,  "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 85_000},
    {"kode": "ITM-003", "nama": "Ballpoint Biru",      "satuan": "lusin", "stok": 3,  "batas_aman": 10, "batas_rendah": 5,  "harga_satuan": 28_000},
    {"kode": "ITM-004", "nama": "Spidol Whiteboard",   "satuan": "set",   "stok": 0,  "batas_aman": 5,  "batas_rendah": 2,  "harga_satuan": 45_000},
    {"kode": "ITM-005", "nama": "Staples No.10",       "satuan": "kotak", "stok": 20, "batas_aman": 10, "batas_rendah": 4,  "harga_satuan": 12_000},
    {"kode": "ITM-006", "nama": "Amplop Coklat",       "satuan": "pack",  "stok": 2,  "batas_aman": 15, "batas_rendah": 5,  "harga_satuan": 18_000},
    {"kode": "ITM-007", "nama": "Folder Plastik",      "satuan": "buah",  "stok": 0,  "batas_aman": 20, "batas_rendah": 8,  "harga_satuan": 7_500},
    {"kode": "ITM-008", "nama": "Buku Tulis A5",       "satuan": "lusin", "stok": 12, "batas_aman": 8,  "batas_rendah": 3,  "harga_satuan": 36_000},
]

PRIO_ORDER = {"HABIS": 1, "RENDAH": 2, "PERINGATAN": 3, "AMAN": 4}


def status_stok(item):
    s = item["stok"]
    if s == 0:
        return "HABIS"
    elif s < item["batas_rendah"]:
        return "RENDAH"
    elif s < item["batas_aman"]:
        return "PERINGATAN"
    return "AMAN"


def menu_peringatan_stok():
    """Submenu cek peringatan stok."""
    print("\n" + "=" * 78)
    print("                 CEK PERINGATAN STOK INVENTARIS")
    print("=" * 78)

    hasil = []
    for item in INVENTARIS_DEFAULT:
        ev = item.copy()
        ev["status"] = status_stok(item)
        ev["nilai_stok"] = item["stok"] * item["harga_satuan"]
        hasil.append(ev)
    hasil.sort(key=lambda x: PRIO_ORDER[x["status"]])

    label_map = {
        "HABIS":      "[XX] HABIS     ",
        "RENDAH":     "[!!] RENDAH    ",
        "PERINGATAN": "[~~] PERINGATAN",
        "AMAN":       "[OK] AMAN      ",
    }

    print(f"{'Pri':<4} {'Kode':<9} {'Nama':<22} {'Stok':>5}  {'Status':<16} {'Nilai Stok':>18}")
    print("-" * 78)

    total_nilai = 0
    hitung = {"AMAN": 0, "PERINGATAN": 0, "RENDAH": 0, "HABIS": 0}
    for item in hasil:
        hitung[item["status"]] += 1
        total_nilai += item["nilai_stok"]
        print(
            f"{PRIO_ORDER[item['status']]:<4} {item['kode']:<9} {item['nama']:<22}"
            f"{item['stok']:>5}  {label_map[item['status']]:<16}"
            f"  {format_rupiah(item['nilai_stok']):>16}"
        )

    print("=" * 78)
    print(f"  Total Nilai Inventaris : {format_rupiah(total_nilai)}")
    total = len(hasil)
    print(f"\n  STATISTIK: Aman={hitung['AMAN']} | Peringatan={hitung['PERINGATAN']} "
          f"| Rendah={hitung['RENDAH']} | Habis={hitung['HABIS']}")
    perlu = hitung["HABIS"] + hitung["RENDAH"] + hitung["PERINGATAN"]
    print(f"  Item perlu restock : {perlu}/{total} ({perlu/total*100:.1f}%)")
    print("=" * 78)


# ======================================================================
#  MENU UTAMA
# ======================================================================

def tampilkan_menu():
    print("\n" + "=" * 48)
    print("          MENU UTAMA SI MAHASISWA")
    print("=" * 48)
    print("  [1] Cek Status Mahasiswa")
    print("  [2] Hitung Diskon Biaya Kuliah")
    print("  [3] Cek Peringatan Stok Inventaris")
    print("  [0] Keluar")
    print("=" * 48)


def main():
    print("\n" + "=" * 48)
    print("   SELAMAT DATANG DI SISTEM SI MAHASISWA")
    print("=" * 48)

    while True:
        tampilkan_menu()
        pilihan = input("  Pilih menu [0-3] : ").strip()

        if pilihan == "1":
            menu_status_mahasiswa()
        elif pilihan == "2":
            menu_diskon_biaya()
        elif pilihan == "3":
            menu_peringatan_stok()
        elif pilihan == "0":
            print("\n  Terima kasih. Program selesai.\n")
            break
        else:
            print("  [!] Pilihan tidak valid. Masukkan angka 0 - 3.")


if __name__ == "__main__":
    main()
