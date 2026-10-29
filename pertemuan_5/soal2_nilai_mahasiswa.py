# ============================================================
# PERTEMUAN 5 - SOAL PRAKTIK 2
# Analisis Nilai Mahasiswa: Rata-rata, Tertinggi/Terendah,
# Kategori, dan Frekuensi
# ============================================================

def tentukan_kategori(nilai):
    """
    Menentukan kategori berdasarkan nilai angka:
    A  : 80 - 100
    B  : 70 - 79
    C  : 60 - 69
    D  : 50 - 59
    E  : 0  - 49
    """
    if 80 <= nilai <= 100:
        return "A"
    elif 70 <= nilai <= 79:
        return "B"
    elif 60 <= nilai <= 69:
        return "C"
    elif 50 <= nilai <= 59:
        return "D"
    else:
        return "E"


def analisis_nilai(list_nilai):
    """
    Menganalisis list nilai mahasiswa:
    (a) Rata-rata
    (b) Nilai tertinggi dan terendah
    (c) Kelompokkan ke kategori A/B/C/D/E
    (d) Frekuensi setiap kategori (dictionary)
    """

    # (a) Rata-rata
    rata_rata = sum(list_nilai) / len(list_nilai)

    # (b) Nilai tertinggi dan terendah
    nilai_tertinggi = max(list_nilai)
    nilai_terendah  = min(list_nilai)

    # (c) Kelompokkan nilai ke kategori
    kelompok_nilai = {"A": [], "B": [], "C": [], "D": [], "E": []}
    for nilai in list_nilai:
        kategori = tentukan_kategori(nilai)
        kelompok_nilai[kategori].append(nilai)

    # (d) Frekuensi setiap kategori menggunakan dictionary
    frekuensi = {kategori: len(anggota) for kategori, anggota in kelompok_nilai.items()}

    return {
        "rata_rata"       : rata_rata,
        "nilai_tertinggi" : nilai_tertinggi,
        "nilai_terendah"  : nilai_terendah,
        "kelompok_nilai"  : kelompok_nilai,
        "frekuensi"       : frekuensi,
    }


def tampilkan_bar(frekuensi, total):
    """Menampilkan bar chart sederhana di terminal."""
    for kategori in ["A", "B", "C", "D", "E"]:
        jumlah = frekuensi[kategori]
        bar    = "#" * jumlah
        persen = (jumlah / total * 100) if total > 0 else 0
        print(f"    {kategori}  | {bar:<20} {jumlah} mahasiswa ({persen:.1f}%)")


def tampilkan_hasil(list_nilai, hasil):
    garis = "=" * 55
    print(f"\n{garis}")
    print("    HASIL ANALISIS NILAI MAHASISWA")
    print(garis)
    print(f"  Data nilai : {list_nilai}")
    print(garis)
    print(f"  (a) Rata-rata nilai      : {hasil['rata_rata']:.2f}")
    print(f"  (b) Nilai tertinggi      : {hasil['nilai_tertinggi']}")
    print(f"      Nilai terendah       : {hasil['nilai_terendah']}")
    print(f"\n  (c) Pengelompokan Nilai :")
    for kat, anggota in hasil["kelompok_nilai"].items():
        print(f"      Kategori {kat}  : {anggota if anggota else '-'}")
    print(f"\n  (d) Frekuensi Kategori :")
    tampilkan_bar(hasil["frekuensi"], len(list_nilai))
    print(garis)


def input_nilai():
    """Meminta input nilai dari pengguna."""
    print("\nMasukkan nilai mahasiswa (pisahkan dengan spasi atau koma).")
    print("Contoh: 85 70 55 90 65 45 75")
    raw = input("Nilai: ").replace(",", " ")
    try:
        list_nilai = [float(n) for n in raw.split()]
        # Validasi rentang nilai
        for n in list_nilai:
            if not (0 <= n <= 100):
                raise ValueError(f"Nilai {n} di luar rentang 0-100!")
        if not list_nilai:
            raise ValueError("List nilai tidak boleh kosong!")
        return list_nilai
    except ValueError as e:
        print(f"[!] Input tidak valid: {e}")
        return None


def main():
    print("=" * 55)
    print("   PROGRAM ANALISIS NILAI MAHASISWA - PERTEMUAN 5")
    print("=" * 55)

    list_nilai = input_nilai()
    if list_nilai is None:
        return

    hasil = analisis_nilai(list_nilai)
    tampilkan_hasil(list_nilai, hasil)


if __name__ == "__main__":
    main()
