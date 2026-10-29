# ============================================================
# PERTEMUAN 5 - SOAL PRAKTIK 4
# Sistem Inventaris Toko menggunakan Dictionary & Tuple
# ============================================================

# ---- Struktur data: {nama_barang: (harga, stok)} ----

def tambah_barang(inventaris, nama, harga, stok):
    """
    (a) Menambah barang baru ke inventaris.
    Jika barang sudah ada, tampilkan pesan peringatan.
    """
    nama = nama.strip().title()
    if nama in inventaris:
        print(f"  [!] Barang '{nama}' sudah ada di inventaris!")
        print(f"      Gunakan fungsi update stok jika ingin mengubah.")
    else:
        inventaris[nama] = (harga, stok)
        print(f"  [✓] Barang '{nama}' berhasil ditambahkan.")
    return inventaris


def update_stok(inventaris, nama, stok_baru):
    """
    (b) Mengupdate stok barang yang sudah ada.
    Tuple bersifat immutable, sehingga kita buat tuple baru.
    """
    nama = nama.strip().title()
    if nama not in inventaris:
        print(f"  [!] Barang '{nama}' tidak ditemukan di inventaris!")
    else:
        harga_lama, stok_lama = inventaris[nama]
        inventaris[nama] = (harga_lama, stok_baru)
        print(f"  [✓] Stok '{nama}': {stok_lama} → {stok_baru}")
    return inventaris


def cari_rentang_harga(inventaris, harga_min, harga_max):
    """
    (c) Mencari barang dengan harga dalam rentang [harga_min, harga_max].
    Mengembalikan list tuple (nama, harga, stok).
    """
    hasil = [
        (nama, harga, stok)
        for nama, (harga, stok) in inventaris.items()
        if harga_min <= harga <= harga_max
    ]
    return sorted(hasil, key=lambda x: x[1])  # Urutkan berdasarkan harga


def hitung_total_nilai(inventaris):
    """
    (d) Menghitung total nilai inventaris.
    Total nilai = Σ (harga × stok) untuk semua barang.
    """
    total = sum(harga * stok for harga, stok in inventaris.values())
    return total


# ---- Fungsi tampilan ----

def tampilkan_inventaris(inventaris):
    """Menampilkan seluruh isi inventaris dalam format tabel."""
    garis = "=" * 60
    print(f"\n{garis}")
    print("              DAFTAR INVENTARIS TOKO")
    print(garis)
    print(f"  {'No':<4} {'Nama Barang':<20} {'Harga':>12} {'Stok':>6} {'Nilai':>12}")
    print("-" * 60)
    for i, (nama, (harga, stok)) in enumerate(inventaris.items(), 1):
        nilai = harga * stok
        print(f"  {i:<4} {nama:<20} Rp{harga:>10,.0f} {stok:>6} Rp{nilai:>10,.0f}")
    print("-" * 60)
    total = hitung_total_nilai(inventaris)
    print(f"  {'TOTAL NILAI INVENTARIS':>41} Rp{total:>10,.0f}")
    print(garis)


def menu_interaktif(inventaris):
    """Menu interaktif untuk mengelola inventaris."""
    while True:
        print("\n" + "=" * 55)
        print("         MENU INVENTARIS TOKO")
        print("=" * 55)
        print("  1. Tampilkan seluruh inventaris")
        print("  2. Tambah barang baru")
        print("  3. Update stok barang")
        print("  4. Cari barang berdasarkan rentang harga")
        print("  5. Hitung total nilai inventaris")
        print("  0. Keluar")
        print("=" * 55)

        pilihan = input("  Pilih menu [0-5]: ").strip()

        if pilihan == "1":
            tampilkan_inventaris(inventaris)

        elif pilihan == "2":
            print("\n  [Tambah Barang Baru]")
            nama  = input("  Nama barang : ").strip()
            try:
                harga = float(input("  Harga (Rp)  : ").replace(",", ""))
                stok  = int(input("  Stok        : "))
                if harga < 0 or stok < 0:
                    print("  [!] Harga dan stok tidak boleh negatif!")
                else:
                    tambah_barang(inventaris, nama, harga, stok)
            except ValueError:
                print("  [!] Input harga/stok tidak valid!")

        elif pilihan == "3":
            print("\n  [Update Stok Barang]")
            nama = input("  Nama barang : ").strip()
            try:
                stok_baru = int(input("  Stok baru   : "))
                if stok_baru < 0:
                    print("  [!] Stok tidak boleh negatif!")
                else:
                    update_stok(inventaris, nama, stok_baru)
            except ValueError:
                print("  [!] Input stok tidak valid!")

        elif pilihan == "4":
            print("\n  [Cari Barang Berdasarkan Rentang Harga]")
            try:
                harga_min = float(input("  Harga minimum (Rp): ").replace(",", ""))
                harga_max = float(input("  Harga maksimum (Rp): ").replace(",", ""))
                hasil = cari_rentang_harga(inventaris, harga_min, harga_max)
                if hasil:
                    print(f"\n  Barang dengan harga Rp{harga_min:,.0f} - Rp{harga_max:,.0f}:")
                    print(f"  {'No':<4} {'Nama Barang':<20} {'Harga':>12} {'Stok':>6}")
                    print("  " + "-" * 46)
                    for i, (nama, harga, stok) in enumerate(hasil, 1):
                        print(f"  {i:<4} {nama:<20} Rp{harga:>10,.0f} {stok:>6}")
                else:
                    print("  [!] Tidak ada barang dalam rentang harga tersebut.")
            except ValueError:
                print("  [!] Input harga tidak valid!")

        elif pilihan == "5":
            total = hitung_total_nilai(inventaris)
            print(f"\n  Total Nilai Inventaris : Rp{total:,.0f}")

        elif pilihan == "0":
            print("\n  Terima kasih! Program selesai.")
            break

        else:
            print("  [!] Menu tidak valid, pilih 0-5.")


def main():
    print("=" * 55)
    print("   PROGRAM INVENTARIS TOKO - PERTEMUAN 5")
    print("=" * 55)

    # Data awal inventaris: {nama: (harga, stok)}
    inventaris = {
        "Beras Premium"   : (15000, 100),
        "Minyak Goreng"   : (18500,  80),
        "Gula Pasir"      : (13000,  60),
        "Tepung Terigu"   : (10000,  75),
        "Susu UHT"        : (16500,  50),
        "Mie Instan"      : (3500,  200),
        "Kecap Manis"     : (12000,  45),
        "Sabun Mandi"     : (7500,   90),
        "Shampoo"         : (22000,  30),
        "Deterjen"        : (19000,  40),
    }

    print("\n  [Data inventaris awal telah dimuat - 10 barang]")
    menu_interaktif(inventaris)


if __name__ == "__main__":
    main()
