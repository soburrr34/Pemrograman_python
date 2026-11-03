"""
Soal 1 - Pembacaan Data Mahasiswa dari File CSV
================================================
Program untuk membaca data mahasiswa dari file CSV dengan penanganan
exception komprehensif:
  - FileNotFoundError : File tidak ditemukan pada path yang diberikan
  - csv.Error         : Terjadi kesalahan format/parsing CSV
  - ValueError        : Data nilai/IPK/SKS tidak dapat dikonversi ke tipe numerik
Blok else digunakan untuk menampilkan ringkasan data jika pembacaan sukses.
Blok finally digunakan untuk memastikan file stream ditutup dengan aman.
"""

import csv
import os
from typing import List, Dict, Any, Optional


def baca_data_mahasiswa(filepath: str) -> Optional[List[Dict[str, Any]]]:
    """
    Membaca data mahasiswa dari file CSV dengan penanganan exception lengkap.

    Args:
        filepath (str): Jalur/path ke file CSV.

    Returns:
        Optional[List[Dict[str, Any]]]: Daftar mahasiswa jika berhasil, None jika gagal.

    Raises:
        FileNotFoundError, csv.Error, ValueError ditangani di dalam fungsi.
    """
    file_handle = None
    data_mahasiswa: List[Dict[str, Any]] = []

    print(f"\n{'=' * 65}")
    print(f"Mencoba membaca file: '{filepath}'")
    print(f"{'=' * 65}")

    try:
        # Membuka file secara eksplisit tanpa context manager
        # agar penggunaan blok finally untuk file.close() teruji nyata
        file_handle = open(filepath, mode="r", encoding="utf-8")
        reader = csv.DictReader(file_handle)

        # Validasi header minimal
        field_wajib = {"nim", "nama", "jurusan", "ipk", "sks"}
        if reader.fieldnames is None:
            raise csv.Error("File CSV kosong atau header tidak ditemukan.")

        header_set = {f.strip().lower() for f in reader.fieldnames if f}
        if not field_wajib.issubset(header_set):
            missing = field_wajib - header_set
            raise ValueError(f"Header CSV tidak lengkap, kolom wajib tidak ada: {missing}")

        for nomor_baris, row in enumerate(reader, start=2):
            # Normalisasi kunci header ke huruf kecil
            row_normalized = {k.strip().lower(): v.strip() for k, v in row.items() if k}

            nim = row_normalized.get("nim", "")
            nama = row_normalized.get("nama", "")
            jurusan = row_normalized.get("jurusan", "")
            raw_ipk = row_normalized.get("ipk", "")
            raw_sks = row_normalized.get("sks", "")

            # Validasi string wajib
            if not nim or not nama:
                raise ValueError(
                    f"Baris {nomor_baris}: NIM atau Nama tidak boleh kosong! (NIM: '{nim}', Nama: '{nama}')"
                )

            # Konversi IPK ke float (dapat memicu ValueError)
            try:
                ipk = float(raw_ipk)
            except ValueError as err:
                raise ValueError(
                    f"Baris {nomor_baris}: Nilai IPK '{raw_ipk}' bukan angka valid! ({err})"
                ) from err

            if not (0.0 <= ipk <= 4.0):
                raise ValueError(
                    f"Baris {nomor_baris}: Nilai IPK {ipk} di luar rentang valid (0.00 - 4.00)!"
                )

            # Konversi SKS ke int (dapat memicu ValueError)
            try:
                sks = int(raw_sks)
            except ValueError as err:
                raise ValueError(
                    f"Baris {nomor_baris}: Nilai SKS '{raw_sks}' bukan bilangan bulat valid! ({err})"
                ) from err

            if sks <= 0:
                raise ValueError(
                    f"Baris {nomor_baris}: Nilai SKS {sks} harus lebih besar dari 0!"
                )

            data_mahasiswa.append({
                "nim": nim,
                "nama": nama,
                "jurusan": jurusan,
                "ipk": ipk,
                "sks": sks,
            })

    except FileNotFoundError as e:
        print(f"[EXCEPTION CAUGHT] FileNotFoundError:")
        print(f"  -> File '{filepath}' tidak ditemukan di sistem!")
        print(f"  -> Pesan Sistem: {e}")
        return None

    except csv.Error as e:
        print(f"[EXCEPTION CAUGHT] csv.Error:")
        print(f"  -> Terjadi kesalahan format/parsing CSV pada '{filepath}'!")
        print(f"  -> Detail: {e}")
        return None

    except ValueError as e:
        print(f"[EXCEPTION CAUGHT] ValueError:")
        print(f"  -> Kesalahan validasi nilai/data mahasiswa!")
        print(f"  -> Detail: {e}")
        return None

    except Exception as e:
        print(f"[EXCEPTION CAUGHT] Exception Tak Terduga ({type(e).__name__}):")
        print(f"  -> Detail: {e}")
        return None

    else:
        # Blok ELSE: Dijalankan HANYA jika TIDAK ADA exception pada blok try
        print(f"[SUKSES] Pembacaan file '{filepath}' berhasil tanpa error!")
        tampilkan_ringkasan_data(data_mahasiswa)
        return data_mahasiswa

    finally:
        # Blok FINALLY: Selalu dijalankan dalam kondisi apapun
        if file_handle is not None and not file_handle.closed:
            file_handle.close()
            print(f"[FINALLY] Status File: File '{filepath}' telah berhasil ditutup dengan aman.")
        else:
            print(f"[FINALLY] Status File: Tidak ada resource file yang terbuka atau file belum sempat dibuka.")


def tampilkan_ringkasan_data(data: List[Dict[str, Any]]) -> None:
    """
    Menampilkan ringkasan statistik data mahasiswa.
    Dipanggil di dalam blok else saat pembacaan sukses.
    """
    if not data:
        print("  -> Data kosong, tidak ada statistik yang dapat dihitung.")
        return

    total_mahasiswa = len(data)
    total_ipk = sum(m["ipk"] for m in data)
    rata_ipk = total_ipk / total_mahasiswa
    total_sks = sum(m["sks"] for m in data)

    mhs_tertinggi = max(data, key=lambda m: m["ipk"])
    mhs_terendah = min(data, key=lambda m: m["ipk"])

    print("-" * 65)
    print("                    RINGKASAN DATA MAHASISWA")
    print("-" * 65)
    print(f"  * Total Mahasiswa Terdaftar : {total_mahasiswa} orang")
    print(f"  * Total Beban SKS Keseluruhan : {total_sks} SKS")
    print(f"  * Rata-rata IPK Mahasiswa   : {rata_ipk:.2f}")
    print(f"  * IPK Tertinggi              : {mhs_tertinggi['ipk']:.2f} ({mhs_tertinggi['nama']} - NIM: {mhs_tertinggi['nim']})")
    print(f"  * IPK Terendah               : {mhs_terendah['ipk']:.2f} ({mhs_terendah['nama']} - NIM: {mhs_terendah['nim']})")
    print("-" * 65)
    print(f"  {'No':<4} {'NIM':<12} {'Nama Mahasiswa':<22} {'Jurusan':<20} {'IPK':<6} {'SKS':<5}")
    print("-" * 65)
    for i, m in enumerate(data, start=1):
        print(f"  {i:<4} {m['nim']:<12} {m['nama']:<22} {m['jurusan']:<20} {m['ipk']:<6.2f} {m['sks']:<5}")
    print("-" * 65)


def siapkan_file_uji() -> Dict[str, str]:
    """
    Membuat file-file CSV simulasi untuk menguji semua kemungkinan exception:
    1. Valid
    2. Invalid ValueError (IPK teks non-numerik atau out of bounds)
    3. Invalid csv.Error (format rusak dengan karakter NULL)
    4. Non-existent path (FileNotFoundError)
    """
    direktori = os.path.dirname(os.path.abspath(__file__))

    # 1. File CSV Valid
    path_valid = os.path.join(direktori, "mahasiswa_valid.csv")
    with open(path_valid, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nim", "nama", "jurusan", "ipk", "sks"])
        writer.writerow(["20241320001", "Ahmad Fauzi", "Teknik Informatika", "3.75", "20"])
        writer.writerow(["20241320002", "Budi Santoso", "Sistem Informasi", "3.40", "22"])
        writer.writerow(["20241320046", "Sobur", "Teknik Informatika", "3.90", "24"])
        writer.writerow(["20241320015", "Citra Lestari", "Teknik Informatika", "3.65", "20"])
        writer.writerow(["20241320020", "Dewi Sartika", "Sistem Informasi", "3.20", "18"])

    # 2. File CSV Memicu ValueError (IPK berupa kata 'tiga koma lima')
    path_invalid_val = os.path.join(direktori, "mahasiswa_invalid_value.csv")
    with open(path_invalid_val, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nim", "nama", "jurusan", "ipk", "sks"])
        writer.writerow(["20241320001", "Ahmad Fauzi", "Teknik Informatika", "3.75", "20"])
        writer.writerow(["20241320099", "Eko Prasetyo", "Teknik Informatika", "tiga_koma_lima", "20"])

    # 3. File CSV Memicu csv.Error (menyisipkan byte NULL / \x00 yang dilarang parser csv)
    path_corrupt = os.path.join(direktori, "mahasiswa_corrupt.csv")
    with open(path_corrupt, "wb") as f:
        f.write(b"nim,nama,jurusan,ipk,sks\r\n")
        f.write(b"20241320001,Ahmad\x00Fauzi,Teknik Informatika,3.75,20\r\n")

    # 4. File tidak ada
    path_tidak_ada = os.path.join(direktori, "mahasiswa_tidak_ditemukan.csv")
    if os.path.exists(path_tidak_ada):
        os.remove(path_tidak_ada)

    return {
        "valid": path_valid,
        "invalid_value": path_invalid_val,
        "corrupt_csv": path_corrupt,
        "not_found": path_tidak_ada,
    }


def main():
    print("\n" + "#" * 65)
    print("DEMO SOAL 1: PEMBACAAN CSV & PENANGANAN EXCEPTION LENGKAP")
    print("#" * 65)

    files = siapkan_file_uji()

    # Skenario 1: File Valid -> Blok TRY -> ELSE -> FINALLY
    print("\n--- SKENARIO 1: MEMBACA FILE CSV VALID (SUKSES) ---")
    baca_data_mahasiswa(files["valid"])

    # Skenario 2: File Tidak Ada -> Memicu FileNotFoundError -> FINALLY
    print("\n--- SKENARIO 2: FILE TIDAK DITEMUKAN (FileNotFoundError) ---")
    baca_data_mahasiswa(files["not_found"])

    # Skenario 3: Nilai Tidak Valid -> Memicu ValueError -> FINALLY
    print("\n--- SKENARIO 3: NILAI DATA TIDAK VALID (ValueError) ---")
    baca_data_mahasiswa(files["invalid_value"])

    # Skenario 4: File Rusak -> Memicu csv.Error -> FINALLY
    print("\n--- SKENARIO 4: FORMAT CSV RUSAK/KORUP (csv.Error) ---")
    baca_data_mahasiswa(files["corrupt_csv"])


if __name__ == "__main__":
    main()

