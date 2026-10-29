"""
Soal 4 - main.py untuk Package sistem_informasi
==================================================
File utama yang mendemonstrasikan penggunaan package sistem_informasi.
Melakukan operasi CRUD lengkap untuk entitas Mahasiswa.
"""

from sistem_informasi import Mahasiswa, MahasiswaService
from sistem_informasi.utils.helper import (
    cetak_judul,
    format_tabel,
    cetak_hasil,
    cetak_statistik,
)


def demo_create(svc: MahasiswaService) -> None:
    """Demo operasi CREATE - menambahkan mahasiswa."""
    cetak_judul("CREATE - Menambahkan Data Mahasiswa")

    mahasiswa_list = [
        Mahasiswa('2023001001', 'Budi Santoso',      'Teknik Informatika', 5, 3.75, 'Aktif'),
        Mahasiswa('2023001002', 'Ani Rahayu',         'Sistem Informasi',   3, 3.50, 'Aktif'),
        Mahasiswa('2023001003', 'Citra Dewi',         'Teknik Komputer',    7, 3.85, 'Aktif'),
        Mahasiswa('2023001004', 'Deni Firmansyah',    'Teknik Informatika', 1, 0.00, 'Aktif'),
        Mahasiswa('2023001005', 'Eka Putri Lestari',  'Sistem Informasi',   9, 3.20, 'Cuti'),
        Mahasiswa('2023001006', 'Fajar Nugroho',      'Ilmu Komputer',      11, 3.90, 'Lulus'),
    ]

    hasil_batch = svc.tambah_batch(mahasiswa_list)
    print(f"\n  Tambah batch: {hasil_batch['berhasil']} berhasil, {hasil_batch['gagal']} gagal")

    # Coba tambah duplikat NIM
    duplikat = Mahasiswa('2023001001', 'Budi Duplikat', 'Teknik Informatika', 1, 0.0, 'Aktif')
    hasil_dup = svc.tambah(duplikat)
    cetak_hasil("Tambah Duplikat NIM", hasil_dup)


def demo_read(svc: MahasiswaService) -> None:
    """Demo operasi READ - membaca data mahasiswa."""
    cetak_judul("READ - Membaca Data Mahasiswa")

    # Tampilkan semua
    print("\n  [1] Semua Mahasiswa:")
    semua = svc.tampil_semua()
    kolom = ['nim', 'nama', 'program_studi', 'semester', 'ipk', 'status']
    print(format_tabel(semua['data'], kolom=kolom))
    print(f"\n  Total: {semua['total']} mahasiswa")

    # Cari berdasarkan NIM
    print("\n  [2] Cari NIM '2023001003':")
    hasil = svc.cari_nim('2023001003')
    cetak_hasil("Cari NIM", hasil)

    # Cari berdasarkan nama
    print("\n  [3] Cari nama keyword 'udi':")
    hasil_nama = svc.cari_nama('udi')
    print(f"      {hasil_nama['message']}")

    # Filter per status
    print("\n  [4] Filter mahasiswa AKTIF saja:")
    aktif = svc.tampil_semua(filter_status='Aktif')
    print(format_tabel(aktif['data'], kolom=['nim', 'nama', 'ipk', 'status']))

    # Cari NIM tidak ada
    print("\n  [5] Cari NIM yang tidak ada:")
    tidak_ada = svc.cari_nim('9999999999')
    cetak_hasil("Cari NIM Tidak Ada", tidak_ada)


def demo_update(svc: MahasiswaService) -> None:
    """Demo operasi UPDATE - memperbarui data mahasiswa."""
    cetak_judul("UPDATE - Memperbarui Data Mahasiswa")

    # Update semester dan IPK
    print("\n  [1] Update semester dan IPK NIM '2023001001':")
    hasil = svc.update('2023001001', {'semester': 6, 'ipk': 3.82})
    cetak_hasil("Update Semester & IPK", hasil)

    # Update status mahasiswa
    print("\n  [2] Update status NIM '2023001004' menjadi 'Cuti':")
    hasil2 = svc.update('2023001004', {'status': 'Cuti'})
    cetak_hasil("Update Status", hasil2)

    # Update NIM tidak ada
    print("\n  [3] Update NIM yang tidak ada:")
    hasil3 = svc.update('9999999', {'ipk': 3.0})
    cetak_hasil("Update NIM Tidak Ada", hasil3)

    # Update dengan nilai invalid
    print("\n  [4] Update IPK dengan nilai tidak valid (>4.0):")
    hasil4 = svc.update('2023001002', {'ipk': 5.0})
    cetak_hasil("Update IPK Invalid", hasil4)


def demo_delete(svc: MahasiswaService) -> None:
    """Demo operasi DELETE - menghapus data mahasiswa."""
    cetak_judul("DELETE - Menghapus Data Mahasiswa")

    print(f"\n  Total sebelum hapus: {len(svc)} mahasiswa")

    # Hapus mahasiswa yang ada
    print("\n  [1] Hapus NIM '2023001006':")
    hasil = svc.hapus('2023001006')
    cetak_hasil("Hapus Mahasiswa", hasil)

    print(f"\n  Total setelah hapus: {len(svc)} mahasiswa")

    # Hapus NIM tidak ada
    print("\n  [2] Hapus NIM yang tidak ada:")
    hasil2 = svc.hapus('9999999999')
    cetak_hasil("Hapus NIM Tidak Ada", hasil2)


def demo_statistik(svc: MahasiswaService) -> None:
    """Demo statistik mahasiswa."""
    cetak_judul("STATISTIK - Ringkasan Data Mahasiswa")
    stat = svc.statistik()
    cetak_statistik(stat)


def main():
    """Fungsi utama - menjalankan semua demo CRUD."""
    print("\n" + "#" * 60)
    print("  SOAL 4 - Package sistem_informasi")
    print("  CRUD Mahasiswa dengan In-Memory Dictionary")
    print("#" * 60)

    # Inisialisasi service
    svc = MahasiswaService()

    demo_create(svc)
    demo_read(svc)
    demo_update(svc)
    demo_statistik(svc)
    demo_delete(svc)

    print("\n" + "#" * 60)
    print("  Program CRUD selesai!")
    print("#" * 60)


if __name__ == '__main__':
    main()
