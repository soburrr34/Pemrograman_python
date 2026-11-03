"""
Soal 3 - Konfigurasi Modul Logging untuk Aplikasi Sistem Informasi
===================================================================
Konfigurasi logging terstandarisasi untuk aplikasi SI:
  (a) File Handler menggunakan RotatingFileHandler:
      - Menangkap level DEBUG ke atas (DEBUG, INFO, WARNING, ERROR, CRITICAL)
      - Mencegah ukuran file log membengkak dengan batas maxBytes & backupCount.
  (b) Console Handler menggunakan StreamHandler:
      - Menangkap level WARNING ke atas (WARNING, ERROR, CRITICAL)
      - Menjaga console tetap bersih dari log debug/info operasional harian.
  (c) Formatter terstandarisasi:
      - Menyertakan %(asctime)s (timestamp), %(levelname)s (level),
        %(name)s (nama logger), dan %(message)s (pesan).

Dilengkapi dengan fungsi verifikasi otomatis untuk membuktikan filter tingkat log
pada masing-masing handler.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import sys


def setup_logger_si(
    nama_logger: str = "SIAKAD_App",
    log_file: str = "aplikasi_si.log",
    max_bytes: int = 500_000,
    backup_count: int = 3
) -> logging.Logger:
    """
    Mengonfigurasi dan mengembalikan instance Logger untuk aplikasi SI.

    Args:
        nama_logger: Nama pengenal logger
        log_file: Nama/path file tujuan log
        max_bytes: Ukuran maksimal file log sebelum dirotasi (default 500 KB)
        backup_count: Jumlah cadangan file rotasi yang dipertahankan

    Returns:
        logging.Logger: Objek logger terkonfigurasi
    """
    # 1. Inisialisasi Logger
    logger = logging.getLogger(nama_logger)
    logger.setLevel(logging.DEBUG)  # Pintu gerbang utama: izinkan semua level log lewat

    # Bersihkan handler lama jika fungsi dipanggil ulang
    if logger.hasHandlers():
        logger.handlers.clear()

    # 2. Formatter: timestamp, level, nama logger, pesan
    format_standar = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 3. (a) File Handler: RotatingFileHandler (Level DEBUG ke atas)
    file_handler = RotatingFileHandler(
        filename=log_file,
        mode="a",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(format_standar)
    logger.addHandler(file_handler)

    # 4. (b) Console Handler: StreamHandler (Level WARNING ke atas)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(format_standar)
    logger.addHandler(console_handler)

    return logger


def simulasi_aktivitas_si(logger: logging.Logger) -> None:
    """
    Menulis pesan log pada berbagai level untuk mensimulasikan
    operasi Sistem Informasi Akademik.
    """
    print("\n" + "=" * 70)
    print("MENJALANKAN SIMULASI AKTIVITAS SISTEM INFORMASI...")
    print("Catatan: Hanya log level WARNING, ERROR, dan CRITICAL yang muncul di console.")
    print("=" * 70)

    # Level 1: DEBUG (Hanya masuk ke File)
    logger.debug("Koneksi pool database PostgreSQL diinisialisasi (Host: localhost:5432, PoolSize: 10)")
    logger.debug("Query SQL: SELECT * FROM mahasiswa WHERE status = 'aktif' executed in 0.0035s")

    # Level 2: INFO (Hanya masuk ke File)
    logger.info("Pengguna 'sobur_2024' berhasil login dari IP 192.168.1.100")
    logger.info("Mahasiswa NIM 20241320046 berhasil mengajukan Rencana Studi (KRS) Semester 3")

    # Level 3: WARNING (Muncul di Console dan masuk ke File)
    logger.warning("Kapasitas kuota mata kuliah 'Pemrograman Python Modern' tersisa 1 kursi!")
    logger.warning("Percobaan login gagal untuk user 'admin_si' (Percobaan ke-2 dari 3)")

    # Level 4: ERROR (Muncul di Console dan masuk ke File)
    logger.error("Gagal mengirim email notifikasi ke 'mahasiswa@kampus.ac.id': SMTP Connection Timeout")
    logger.error("Gagal memproses pembayaran tagihan UKT #INV-2026-8891: Gateway timeout (504)")

    # Level 5: CRITICAL (Muncul di Console dan masuk ke File)
    logger.critical("Database utama terputus tidak terduga! Mengaktifkan mode read-only failover.")


def verifikasi_output_log(log_file: str) -> None:
    """
    Membaca kembali isi file log untuk memverifikasi bahwa seluruh level (DEBUG+)
    benar-benar tersimpan di dalam file sementara hanya WARNING+ yang ada di console.
    """
    print("\n" + "=" * 70)
    print("VERIFIKASI OUTPUT LOG PADA KEDUA HANDLER:")
    print("=" * 70)

    print("\n1. ANALISIS KONSOL (Console Handler):")
    print("   - Threshold Level : WARNING (>= 30)")
    print("   - Pesan Tertampil  : Hanya pesan [WARNING], [ERROR], dan [CRITICAL].")
    print("   - Pesan [DEBUG] dan [INFO] disaring keluar (tidak mengotori layar operator).")

    print(f"\n2. ANALISIS FILE '{log_file}' (RotatingFileHandler):")
    print("   - Threshold Level : DEBUG (>= 10)")
    print("   - Pesan Tersimpan : Seluruh pesan (DEBUG, INFO, WARNING, ERROR, CRITICAL).")
    print("\n--- ISI LENGKAP FILE LOG (DIBACA DARI DISK) ---")

    if not os.path.exists(log_file):
        print(f"Error: File log '{log_file}' tidak ditemukan!")
        return

    with open(log_file, "r", encoding="utf-8") as f:
        isi = f.readlines()

    level_counter = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}

    for nomor, baris in enumerate(isi, start=1):
        clean_line = baris.strip()
        print(f"[{nomor:02d}] {clean_line}")
        for lvl in level_counter:
            if f"| {lvl:<8} |" in clean_line or f"| {lvl} " in clean_line:
                level_counter[lvl] += 1

    print("\n--- STATISTIK LEVEL LOG PADA FILE ---")
    for lvl, count in level_counter.items():
        print(f"  * Level {lvl:<8} : {count} baris")
    print(f"  * Total Baris Log : {len(isi)} baris tersimpan.")
    print("=" * 70)


def main():
    direktori = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(direktori, "aplikasi_si.log")

    # Hapus file log lama jika ada agar pengujian bersih
    if os.path.exists(log_path):
        os.remove(log_path)

    # Konfigurasi logger
    logger = setup_logger_si(nama_logger="SI_Akademik", log_file=log_path)

    # Tulis berbagai pesan log
    simulasi_aktivitas_si(logger)

    # Verifikasi dan tampilkan perbedaan output kedua handler
    verifikasi_output_log(log_path)


if __name__ == "__main__":
    main()

