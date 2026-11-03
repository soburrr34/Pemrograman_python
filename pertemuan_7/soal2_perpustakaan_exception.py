"""
Soal 2 - Hierarki Custom Exception Sistem Informasi Perpustakaan
================================================================
Mendefinisikan hierarki custom exception berbasis OOP untuk sistem perpustakaan:
  - PerpustakaanError (Base Exception)
    ├── BukuNotFoundError
    ├── BukuTidakTersediaError
    ├── AnggotaNotFoundError
    └── BatasPeminjamanError (ekstensi opsional)

Mengimplementasikan fungsi pinjam_buku() dan program utama untuk mendemonstrasikan
penanganan setiap jenis exception secara spesifik maupun polimorfik.
"""

from datetime import datetime, timedelta
from typing import Dict, Any


# =====================================================================
# 1. HIERARKI CUSTOM EXCEPTION
# =====================================================================

class PerpustakaanError(Exception):
    """Base class exception untuk seluruh kesalahan Sistem Informasi Perpustakaan."""

    def __init__(self, pesan: str, kode_error: str = "ERR_PERPUS_GENERAL"):
        super().__init__(pesan)
        self.pesan = pesan
        self.kode_error = kode_error
        self.waktu = datetime.now()

    def __str__(self) -> str:
        return f"[{self.kode_error}] {self.pesan}"


class BukuNotFoundError(PerpustakaanError):
    """Exception saat buku dengan ID/ISBN yang dicari tidak ditemukan dalam katalog."""

    def __init__(self, id_buku: str, pesan: str = None):
        pesan = pesan or f"Buku dengan ID '{id_buku}' tidak terdaftar dalam katalog perpustakaan."
        super().__init__(pesan, kode_error="ERR_BUKU_NOT_FOUND")
        self.id_buku = id_buku


class BukuTidakTersediaError(PerpustakaanError):
    """Exception saat buku terdaftar dalam katalog, tetapi stok fisik sedang kosong/habis."""

    def __init__(self, id_buku: str, judul: str, stok: int = 0, pesan: str = None):
        pesan = pesan or f"Buku '{judul}' (ID: {id_buku}) tidak tersedia saat ini (Stok: {stok})."
        super().__init__(pesan, kode_error="ERR_BUKU_UNAVAILABLE")
        self.id_buku = id_buku
        self.judul = judul
        self.stok = stok


class AnggotaNotFoundError(PerpustakaanError):
    """Exception saat anggota tidak ditemukan dalam database perpustakaan."""

    def __init__(self, id_anggota: str, pesan: str = None):
        pesan = pesan or f"Anggota dengan ID '{id_anggota}' tidak terdaftar sebagai member aktif perpustakaan."
        super().__init__(pesan, kode_error="ERR_ANGGOTA_NOT_FOUND")
        self.id_anggota = id_anggota


class BatasPeminjamanError(PerpustakaanError):
    """Exception saat anggota telah mencapai batas kuota maksimal buku yang boleh dipinjam."""

    def __init__(self, id_anggota: str, nama: str, total_pinjam: int, batas_maks: int = 3):
        pesan = (
            f"Anggota '{nama}' (ID: {id_anggota}) telah mencapai batas maksimal peminjaman "
            f"({total_pinjam}/{batas_maks} buku sedang dipinjam)."
        )
        super().__init__(pesan, kode_error="ERR_MAX_BORROW_REACHED")
        self.id_anggota = id_anggota
        self.nama = nama
        self.total_pinjam = total_pinjam
        self.batas_maks = batas_maks


# =====================================================================
# 2. LOGIKA BISNIS: PINJAM BUKU
# =====================================================================

def pinjam_buku(
    id_anggota: str,
    id_buku: str,
    db_anggota: Dict[str, Dict[str, Any]],
    db_buku: Dict[str, Dict[str, Any]],
    db_transaksi: list,
    batas_maks_pinjam: int = 3
) -> Dict[str, Any]:
    """
    Memproses peminjaman buku oleh seorang anggota perpustakaan.

    Args:
        id_anggota: ID unik anggota perpustakaan
        id_buku: ID atau kode unik buku
        db_anggota: Dictionary data anggota perpustakaan
        db_buku: Dictionary katalog buku perpustakaan
        db_transaksi: List riwayat transaksi peminjaman
        batas_maks_pinjam: Kuota maksimal peminjaman per anggota (default 3)

    Returns:
        dict: Detail transaksi peminjaman jika berhasil

    Raises:
        AnggotaNotFoundError: Jika ID anggota tidak ada dalam sistem
        BukuNotFoundError: Jika ID buku tidak ada dalam katalog
        BukuTidakTersediaError: Jika stok buku yang diminta habis (0)
        BatasPeminjamanError: Jika kuota pinjaman anggota sudah penuh
    """
    # 1. Validasi keberadaan Anggota
    if id_anggota not in db_anggota:
        raise AnggotaNotFoundError(id_anggota)

    anggota = db_anggota[id_anggota]

    # 2. Validasi kuota peminjaman anggota
    pinjaman_aktif = anggota.get("buku_dipinjam", [])
    if len(pinjaman_aktif) >= batas_maks_pinjam:
        raise BatasPeminjamanError(
            id_anggota=id_anggota,
            nama=anggota.get("nama", "Anonim"),
            total_pinjam=len(pinjaman_aktif),
            batas_maks=batas_maks_pinjam
        )

    # 3. Validasi keberadaan Buku dalam katalog
    if id_buku not in db_buku:
        raise BukuNotFoundError(id_buku)

    buku = db_buku[id_buku]

    # 4. Validasi ketersediaan stok fisik buku
    if buku.get("stok", 0) <= 0:
        raise BukuTidakTersediaError(
            id_buku=id_buku,
            judul=buku.get("judul", "Tanpa Judul"),
            stok=buku.get("stok", 0)
        )

    # 5. Eksekusi peminjaman (State mutation)
    buku["stok"] -= 1
    pinjaman_aktif.append(id_buku)

    tgl_pinjam = datetime.now()
    tgl_kembali = tgl_pinjam + timedelta(days=7)

    transaksi = {
        "id_transaksi": f"TRX-{len(db_transaksi) + 1:04d}",
        "id_anggota": id_anggota,
        "nama_anggota": anggota["nama"],
        "id_buku": id_buku,
        "judul_buku": buku["judul"],
        "tanggal_pinjam": tgl_pinjam.strftime("%Y-%m-%d %H:%M:%S"),
        "tenggat_kembali": tgl_kembali.strftime("%Y-%m-%d"),
        "sisa_stok_buku": buku["stok"]
    }
    db_transaksi.append(transaksi)
    return transaksi


# =====================================================================
# 3. DEMONSTRASI PENANGANAN EXCEPTION (PROGRAM UTAMA)
# =====================================================================

def jalankan_uji_pinjam(
    label_skenario: str,
    id_anggota: str,
    id_buku: str,
    db_anggota: dict,
    db_buku: dict,
    db_transaksi: list
):
    """Fungsi pembantu untuk menguji dan menangkap exception secara terstruktur."""
    print(f"\n{'-' * 65}")
    print(f"UJI: {label_skenario}")
    print(f"Permintaan: Anggota '{id_anggota}' meminjam Buku '{id_buku}'")
    print(f"{'-' * 65}")

    try:
        hasil = pinjam_buku(id_anggota, id_buku, db_anggota, db_buku, db_transaksi)
        print("[BERHASIL] Peminjaman Sukses!")
        print(f"  * ID Transaksi  : {hasil['id_transaksi']}")
        print(f"  * Peminjam      : {hasil['nama_anggota']} ({hasil['id_anggota']})")
        print(f"  * Buku          : {hasil['judul_buku']} ({hasil['id_buku']})")
        print(f"  * Tenggat Kembali: {hasil['tenggat_kembali']}")
        print(f"  * Sisa Stok Buku: {hasil['sisa_stok_buku']} eksemplar")

    except AnggotaNotFoundError as e:
        print(f"[TERTANGKAP] AnggotaNotFoundError:")
        print(f"  -> Kode Error : {e.kode_error}")
        print(f"  -> ID Anggota : {e.id_anggota}")
        print(f"  -> Pesan      : {e.pesan}")

    except BukuNotFoundError as e:
        print(f"[TERTANGKAP] BukuNotFoundError:")
        print(f"  -> Kode Error : {e.kode_error}")
        print(f"  -> ID Buku    : {e.id_buku}")
        print(f"  -> Pesan      : {e.pesan}")

    except BukuTidakTersediaError as e:
        print(f"[TERTANGKAP] BukuTidakTersediaError:")
        print(f"  -> Kode Error : {e.kode_error}")
        print(f"  -> ID Buku    : {e.id_buku}")
        print(f"  -> Judul Buku : {e.judul}")
        print(f"  -> Sisa Stok  : {e.stok}")
        print(f"  -> Pesan      : {e.pesan}")

    except BatasPeminjamanError as e:
        print(f"[TERTANGKAP] BatasPeminjamanError:")
        print(f"  -> Kode Error : {e.kode_error}")
        print(f"  -> Anggota    : {e.nama} ({e.id_anggota})")
        print(f"  -> Kuota      : {e.total_pinjam}/{e.batas_maks} buku")
        print(f"  -> Pesan      : {e.pesan}")

    except PerpustakaanError as e:
        # Menangkap turunan PerpustakaanError lainnya secara polimorfik
        print(f"[TERTANGKAP via Base Class] PerpustakaanError: {e}")

    except Exception as e:
        print(f"[FATAL] Kesalahan sistem tak terduga: {e}")


def main():
    print("=" * 65)
    print("DEMO SOAL 2: HIERARKI CUSTOM EXCEPTION SISTEM INFORMASI PERPUSTAKAAN")
    print("=" * 65)

    # Inisialisasi Database Simulasi
    db_anggota = {
        "A001": {"nama": "Sobur", "buku_dipinjam": []},
        "A002": {"nama": "Ahmad Fauzi", "buku_dipinjam": ["B-101", "B-102", "B-103"]},  # Penuh (3 buku)
        "A003": {"nama": "Citra Lestari", "buku_dipinjam": ["B-105"]},
    }

    db_buku = {
        "B-101": {"judul": "Pemrograman Python Modern", "stok": 2},
        "B-102": {"judul": "Struktur Data & Algoritma", "stok": 0},  # Stok habis!
        "B-103": {"judul": "Machine Learning Praktis", "stok": 5},
        "B-104": {"judul": "Clean Code & Refactoring", "stok": 1},
    }

    db_transaksi = []

    # Skenario 1: Happy Path (Peminjaman Berhasil)
    jalankan_uji_pinjam(
        "Skenario 1: Peminjaman Berhasil (Happy Path)",
        id_anggota="A001",
        id_buku="B-101",
        db_anggota=db_anggota,
        db_buku=db_buku,
        db_transaksi=db_transaksi
    )

    # Skenario 2: Anggota Tidak Terdaftar (AnggotaNotFoundError)
    jalankan_uji_pinjam(
        "Skenario 2: Anggota Tidak Ditemukan",
        id_anggota="A999",  # Tidak ada di database
        id_buku="B-101",
        db_anggota=db_anggota,
        db_buku=db_buku,
        db_transaksi=db_transaksi
    )

    # Skenario 3: Buku Tidak Terdaftar di Katalog (BukuNotFoundError)
    jalankan_uji_pinjam(
        "Skenario 3: Buku Tidak Ditemukan dalam Katalog",
        id_anggota="A001",
        id_buku="B-999",  # Tidak ada di database
        db_anggota=db_anggota,
        db_buku=db_buku,
        db_transaksi=db_transaksi
    )

    # Skenario 4: Buku Terdaftar tapi Stok Habis (BukuTidakTersediaError)
    jalankan_uji_pinjam(
        "Skenario 4: Stok Buku Habis / Tidak Tersedia",
        id_anggota="A001",
        id_buku="B-102",  # Stok = 0
        db_anggota=db_anggota,
        db_buku=db_buku,
        db_transaksi=db_transaksi
    )

    # Skenario 5: Anggota Melebihi Kuota Pinjam (BatasPeminjamanError)
    jalankan_uji_pinjam(
        "Skenario 5: Anggota Sudah Mencapai Batas Maksimal Pinjam",
        id_anggota="A002",  # Sudah pinjam 3 buku
        id_buku="B-104",
        db_anggota=db_anggota,
        db_buku=db_buku,
        db_transaksi=db_transaksi
    )

    print("\n" + "=" * 65)
    print("VERIFIKASI HIERARKI INHERITANCE KELAS EXCEPTION:")
    print("=" * 65)
    exceptions = [BukuNotFoundError, BukuTidakTersediaError, AnggotaNotFoundError, BatasPeminjamanError]
    for exc in exceptions:
        is_sub = issubclass(exc, PerpustakaanError)
        is_exc = issubclass(exc, Exception)
        print(f"  * {exc.__name__:<25} -> Subclass PerpustakaanError: {is_sub} | Subclass Exception: {is_exc}")
    print("=" * 65)


if __name__ == "__main__":
    main()

