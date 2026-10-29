# ============================================================
# PERTEMUAN 5 - SOAL PRAKTIK 3
# Operasi Set Beasiswa Mahasiswa:
# Intersection, Difference, Union
# ============================================================

def analisis_beasiswa(beasiswa_a, beasiswa_b):
    """
    Menggunakan operasi SET untuk menganalisis penerima beasiswa:
    (a) Mahasiswa yang menerima KEDUA beasiswa (intersection)
    (b) Mahasiswa yang HANYA menerima beasiswa A (difference A-B)
    (c) Mahasiswa yang menerima beasiswa B tapi TIDAK A (difference B-A)
    (d) Semua mahasiswa UNIK yang menerima beasiswa (union)
    """
    set_a = set(beasiswa_a)
    set_b = set(beasiswa_b)

    # (a) Intersection: menerima keduanya
    keduanya = set_a & set_b          # atau set_a.intersection(set_b)

    # (b) Hanya beasiswa A (ada di A tapi tidak di B)
    hanya_a  = set_a - set_b          # atau set_a.difference(set_b)

    # (c) Hanya beasiswa B (ada di B tapi tidak di A)
    hanya_b  = set_b - set_a          # atau set_b.difference(set_a)

    # (d) Union: semua mahasiswa unik
    semua    = set_a | set_b          # atau set_a.union(set_b)

    return {
        "set_a"   : set_a,
        "set_b"   : set_b,
        "keduanya": keduanya,
        "hanya_a" : hanya_a,
        "hanya_b" : hanya_b,
        "semua"   : semua,
    }


def format_set(s):
    """Format set menjadi string terurut yang rapi."""
    return "{" + ", ".join(sorted(s)) + "}" if s else "{ (tidak ada) }"


def tampilkan_diagram_venn(hasil):
    """Menampilkan diagram Venn sederhana di teks."""
    hanya_a   = sorted(hasil["hanya_a"])
    keduanya  = sorted(hasil["keduanya"])
    hanya_b   = sorted(hasil["hanya_b"])

    print("\n  Diagram Venn (representasi teks):")
    print("  +-----------------+----------------+-----------------+")
    print("  |  Hanya A        |  Keduanya      |  Hanya B        |")
    print("  +-----------------+----------------+-----------------+")

    max_baris = max(len(hanya_a), len(keduanya), len(hanya_b), 1)
    for i in range(max_baris):
        col_a = hanya_a[i]   if i < len(hanya_a)  else ""
        col_k = keduanya[i]  if i < len(keduanya) else ""
        col_b = hanya_b[i]   if i < len(hanya_b)  else ""
        print(f"  |  {col_a:<15}|  {col_k:<14}|  {col_b:<15}|")

    print("  +-----------------+----------------+-----------------+")


def tampilkan_hasil(hasil):
    garis = "=" * 55
    print(f"\n{garis}")
    print("    HASIL ANALISIS BEASISWA - OPERASI SET")
    print(garis)
    print(f"  Penerima Beasiswa A : {format_set(hasil['set_a'])}")
    print(f"  Penerima Beasiswa B : {format_set(hasil['set_b'])}")
    print(garis)
    print(f"  (a) Menerima KEDUA beasiswa  : {format_set(hasil['keduanya'])}")
    print(f"      Jumlah                   : {len(hasil['keduanya'])} mahasiswa")
    print(f"\n  (b) HANYA beasiswa A         : {format_set(hasil['hanya_a'])}")
    print(f"      Jumlah                   : {len(hasil['hanya_a'])} mahasiswa")
    print(f"\n  (c) HANYA beasiswa B (not A) : {format_set(hasil['hanya_b'])}")
    print(f"      Jumlah                   : {len(hasil['hanya_b'])} mahasiswa")
    print(f"\n  (d) Semua mahasiswa unik     : {format_set(hasil['semua'])}")
    print(f"      Jumlah                   : {len(hasil['semua'])} mahasiswa")
    tampilkan_diagram_venn(hasil)
    print(garis)


def main():
    print("=" * 55)
    print("  PROGRAM OPERASI SET BEASISWA - PERTEMUAN 5")
    print("=" * 55)

    # Data contoh bawaan
    beasiswa_a = ["M001", "M002", "M003", "M004", "M005", "M006"]
    beasiswa_b = ["M004", "M005", "M006", "M007", "M008", "M009"]

    print("\n[Menggunakan data contoh bawaan]")
    print(f"  Beasiswa A : {beasiswa_a}")
    print(f"  Beasiswa B : {beasiswa_b}")

    pilihan = input("\nGunakan data sendiri? (y/n): ").strip().lower()
    if pilihan == "y":
        print("\nMasukkan ID mahasiswa penerima beasiswa A (pisahkan spasi/koma).")
        print("Contoh: M001 M002 M003")
        raw_a = input("Beasiswa A: ").replace(",", " ").split()
        raw_b_input = input("Beasiswa B: ").replace(",", " ").split()
        if raw_a:
            beasiswa_a = raw_a
        if raw_b_input:
            beasiswa_b = raw_b_input

    hasil = analisis_beasiswa(beasiswa_a, beasiswa_b)
    tampilkan_hasil(hasil)


if __name__ == "__main__":
    main()
