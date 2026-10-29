"""
Soal 3 - Module Utilitas Akademik
===================================
Module ini berisi fungsi-fungsi utilitas untuk keperluan akademik:
  - hitung_ipk()            : Menghitung IPK dari daftar nilai dan SKS
  - konversi_nilai_huruf()  : Mengkonversi nilai angka ke nilai huruf (A/B/C/D/E)
  - generate_transkrip()    : Menghasilkan transkrip akademik lengkap

Dapat diimport ke file lain atau dijalankan langsung untuk testing.
"""


# Tabel konversi nilai angka ke huruf (standar umum perguruan tinggi Indonesia)
TABEL_KONVERSI_NILAI = [
    (85, 100, 'A',  4.00, 'Sangat Baik'),
    (80, 84,  'A-', 3.75, 'Sangat Baik'),
    (75, 79,  'B+', 3.50, 'Baik'),
    (70, 74,  'B',  3.00, 'Baik'),
    (65, 69,  'B-', 2.75, 'Cukup Baik'),
    (60, 64,  'C+', 2.50, 'Cukup'),
    (55, 59,  'C',  2.00, 'Cukup'),
    (40, 54,  'D',  1.00, 'Kurang'),
    (0,  39,  'E',  0.00, 'Tidak Lulus'),
]


def konversi_nilai_huruf(nilai_angka: float) -> dict:
    """
    Mengkonversi nilai angka (0-100) ke nilai huruf beserta bobot dan keterangan.

    Args:
        nilai_angka (float): Nilai dalam skala 0-100

    Returns:
        dict: {
            'nilai_angka' : float,
            'nilai_huruf' : str,   (A, A-, B+, B, B-, C+, C, D, E)
            'bobot'       : float, (0.00 - 4.00)
            'keterangan'  : str
        }

    Raises:
        ValueError: Jika nilai_angka di luar rentang 0-100
    """
    if not (0 <= nilai_angka <= 100):
        raise ValueError(f"Nilai angka harus antara 0-100, bukan {nilai_angka}")

    for batas_bawah, batas_atas, huruf, bobot, keterangan in TABEL_KONVERSI_NILAI:
        if batas_bawah <= nilai_angka <= batas_atas:
            return {
                'nilai_angka': round(nilai_angka, 2),
                'nilai_huruf': huruf,
                'bobot'      : bobot,
                'keterangan' : keterangan,
            }

    # Fallback (seharusnya tidak tercapai)
    return {'nilai_angka': nilai_angka, 'nilai_huruf': 'E', 'bobot': 0.0, 'keterangan': 'Tidak Lulus'}


def hitung_ipk(daftar_matakuliah: list) -> dict:
    """
    Menghitung IPK (Indeks Prestasi Kumulatif) dari daftar mata kuliah.

    Args:
        daftar_matakuliah (list): List of dict, setiap dict berisi:
            - 'nama_mk'    (str)  : Nama mata kuliah
            - 'sks'        (int)  : Jumlah SKS
            - 'nilai_angka'(float): Nilai angka (0-100)

    Returns:
        dict: {
            'ipk'         : float,  IPK dengan 2 desimal
            'total_sks'   : int,    Total SKS yang ditempuh
            'total_mutu'  : float,  Total angka mutu (SKS x bobot)
            'jumlah_mk'   : int,    Jumlah mata kuliah
            'predikat'    : str,    Predikat kelulusan
            'detail'      : list    Detail per mata kuliah
        }

    Raises:
        ValueError: Jika list kosong atau data tidak valid
    """
    if not daftar_matakuliah:
        raise ValueError("Daftar mata kuliah tidak boleh kosong!")

    total_sks   = 0
    total_mutu  = 0.0
    detail      = []

    for mk in daftar_matakuliah:
        nama_mk     = mk.get('nama_mk', 'Tidak Diketahui')
        sks         = mk.get('sks', 0)
        nilai_angka = mk.get('nilai_angka', 0)

        if sks <= 0:
            raise ValueError(f"SKS untuk '{nama_mk}' harus lebih dari 0")

        konversi   = konversi_nilai_huruf(nilai_angka)
        mutu       = sks * konversi['bobot']  # angka mutu = SKS × bobot

        total_sks  += sks
        total_mutu += mutu

        detail.append({
            'nama_mk'    : nama_mk,
            'sks'        : sks,
            'nilai_angka': konversi['nilai_angka'],
            'nilai_huruf': konversi['nilai_huruf'],
            'bobot'      : konversi['bobot'],
            'angka_mutu' : round(mutu, 2),
            'keterangan' : konversi['keterangan'],
        })

    ipk = round(total_mutu / total_sks, 2) if total_sks > 0 else 0.0

    # Tentukan predikat
    if ipk >= 3.51:
        predikat = 'Cumlaude (Dengan Pujian)'
    elif ipk >= 3.01:
        predikat = 'Sangat Memuaskan'
    elif ipk >= 2.76:
        predikat = 'Memuaskan'
    elif ipk >= 2.00:
        predikat = 'Cukup'
    else:
        predikat = 'Kurang Memuaskan'

    return {
        'ipk'        : ipk,
        'total_sks'  : total_sks,
        'total_mutu' : round(total_mutu, 2),
        'jumlah_mk'  : len(daftar_matakuliah),
        'predikat'   : predikat,
        'detail'     : detail,
    }


def generate_transkrip(
    nama: str,
    nim: str,
    program_studi: str,
    semester: int,
    daftar_matakuliah: list,
    **info_tambahan
) -> str:
    """
    Menghasilkan transkrip akademik dalam format teks terformat.

    Args:
        nama              (str) : Nama mahasiswa
        nim               (str) : Nomor Induk Mahasiswa
        program_studi     (str) : Program studi
        semester          (int) : Semester saat ini
        daftar_matakuliah (list): Daftar mata kuliah (lihat hitung_ipk())
        **info_tambahan         : Info opsional (tahun_akademik, wali_dosen, dll.)

    Returns:
        str: Transkrip akademik dalam format teks
    """
    hasil_ipk    = hitung_ipk(daftar_matakuliah)
    lebar        = 65
    garis_tebal  = '=' * lebar
    garis_tipis  = '-' * lebar

    baris = []
    baris.append(garis_tebal)
    baris.append("TRANSKRIP AKADEMIK MAHASISWA".center(lebar))
    baris.append("Sistem Informasi Akademik".center(lebar))
    baris.append(garis_tebal)

    # Info mahasiswa
    baris.append(f"  Nama           : {nama}")
    baris.append(f"  NIM            : {nim}")
    baris.append(f"  Program Studi  : {program_studi}")
    baris.append(f"  Semester       : {semester}")

    # Info tambahan dari **kwargs
    for key, value in info_tambahan.items():
        label = key.replace('_', ' ').title()
        baris.append(f"  {label:<15}: {value}")

    baris.append(garis_tipis)
    baris.append("DAFTAR NILAI MATA KULIAH".center(lebar))
    baris.append(garis_tipis)

    # Header tabel
    header = f"  {'No':<4} {'Mata Kuliah':<28} {'SKS':<5} {'Nilai':<6} {'Huruf':<6} {'Mutu':<6}"
    baris.append(header)
    baris.append(f"  {'-'*4} {'-'*28} {'-'*5} {'-'*6} {'-'*6} {'-'*6}")

    # Baris detail mata kuliah
    for i, mk in enumerate(hasil_ipk['detail'], 1):
        baris.append(
            f"  {i:<4} {mk['nama_mk']:<28} {mk['sks']:<5} "
            f"{mk['nilai_angka']:<6} {mk['nilai_huruf']:<6} {mk['angka_mutu']:<6}"
        )

    baris.append(garis_tipis)
    baris.append(f"  Total SKS        : {hasil_ipk['total_sks']}")
    baris.append(f"  Total Angka Mutu : {hasil_ipk['total_mutu']}")
    baris.append(f"  IPK              : {hasil_ipk['ipk']:.2f}")
    baris.append(f"  Predikat         : {hasil_ipk['predikat']}")
    baris.append(garis_tebal)

    return '\n'.join(baris)


# Testing modul ini secara langsung
if __name__ == '__main__':
    print("=" * 65)
    print("  TESTING MODULE utilitas_akademik.py")
    print("=" * 65)

    # ── Test konversi_nilai_huruf() ──────────────────────────────────────────
    print("\n[1] Test konversi_nilai_huruf():")
    nilai_uji = [95, 82, 76, 71, 67, 62, 57, 45, 30]
    for n in nilai_uji:
        hasil = konversi_nilai_huruf(n)
        print(f"  Nilai {n:3d} -> {hasil['nilai_huruf']:<3} | Bobot: {hasil['bobot']} | {hasil['keterangan']}")

    # ── Test hitung_ipk() ────────────────────────────────────────────────────
    print("\n[2] Test hitung_ipk():")
    mk_list = [
        {'nama_mk': 'Pemrograman Python',    'sks': 3, 'nilai_angka': 88},
        {'nama_mk': 'Basis Data',             'sks': 3, 'nilai_angka': 75},
        {'nama_mk': 'Struktur Data',          'sks': 3, 'nilai_angka': 82},
        {'nama_mk': 'Kalkulus',               'sks': 2, 'nilai_angka': 65},
        {'nama_mk': 'Bahasa Inggris',         'sks': 2, 'nilai_angka': 90},
    ]
    hasil_ipk = hitung_ipk(mk_list)
    print(f"  IPK      : {hasil_ipk['ipk']}")
    print(f"  Total SKS: {hasil_ipk['total_sks']}")
    print(f"  Predikat : {hasil_ipk['predikat']}")

    # ── Test generate_transkrip() ────────────────────────────────────────────
    print("\n[3] Test generate_transkrip():")
    transkrip = generate_transkrip(
        nama              = 'Ahmad Fauzi',
        nim               = '2022001001',
        program_studi     = 'Teknik Informatika',
        semester          = 3,
        daftar_matakuliah = mk_list,
        tahun_akademik    = '2024/2025',
        wali_dosen        = 'Dr. Budi Rahmat, M.Kom',
    )
    print(transkrip)

    print("\n[SELESAI] Module utilitas_akademik siap digunakan!")
