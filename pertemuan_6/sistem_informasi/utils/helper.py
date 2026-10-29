"""
Module: sistem_informasi.utils.helper
=======================================
Fungsi-fungsi pembantu untuk formatting output dan tampilan data mahasiswa.
"""


def cetak_judul(judul: str, lebar: int = 60) -> None:
    """Mencetak judul dengan border yang rapi."""
    print(f"\n{'=' * lebar}")
    print(f"  {judul}".center(lebar))
    print(f"{'=' * lebar}")


def format_tabel(
    data     : list,
    kolom    : list = None,
    lebar_col: list = None,
) -> str:
    """
    Memformat list of dict menjadi tabel teks yang rapi.

    Args:
        data      (list): List of dict yang akan ditampilkan
        kolom     (list): List nama kolom (key dari dict). Default: semua key.
        lebar_col (list): Lebar tiap kolom. Default: otomatis.

    Returns:
        str: String tabel terformat
    """
    if not data:
        return "  (Tidak ada data)"

    # Tentukan kolom
    if kolom is None:
        kolom = list(data[0].keys())

    # Tentukan lebar kolom otomatis jika tidak ditentukan
    if lebar_col is None:
        lebar_col = []
        for col in kolom:
            max_lebar = len(str(col))
            for row in data:
                val = str(row.get(col, ''))
                if len(val) > max_lebar:
                    max_lebar = len(val)
            lebar_col.append(min(max_lebar + 2, 30))  # max 30 char

    baris = []
    garis = '  ' + '+'.join('-' * w for w in lebar_col) + '+'

    # Header
    baris.append(garis)
    header = '  ' + '|'.join(
        f" {str(col)[:w-2]:<{w-1}}" for col, w in zip(kolom, lebar_col)
    ) + '|'
    baris.append(header)
    baris.append(garis)

    # Baris data
    for row in data:
        baris_data = '  ' + '|'.join(
            f" {str(row.get(col, ''))[:w-2]:<{w-1}}" for col, w in zip(kolom, lebar_col)
        ) + '|'
        baris.append(baris_data)

    baris.append(garis)
    return '\n'.join(baris)


def cetak_hasil(label: str, hasil: dict) -> None:
    """Mencetak hasil operasi CRUD secara terformat."""
    status = "BERHASIL" if hasil.get('success') else "GAGAL"
    ikon   = "OK" if hasil.get('success') else "X!"
    print(f"\n  [{ikon}] {label} - {status}")
    print(f"      Pesan: {hasil.get('message', '-')}")
    if hasil.get('data') and isinstance(hasil['data'], dict):
        for key, val in hasil['data'].items():
            print(f"      {key:<15}: {val}")


def cetak_statistik(stat: dict) -> None:
    """Mencetak statistik mahasiswa secara terformat."""
    print(f"\n  Total Mahasiswa    : {stat.get('total', 0)}")
    if stat.get('total', 0) == 0:
        return
    print(f"  IPK Tertinggi      : {stat.get('ipk_tertinggi', 0)}")
    print(f"  IPK Terendah       : {stat.get('ipk_terendah', 0)}")
    print(f"  IPK Rata-rata      : {stat.get('ipk_rata_rata', 0)}")
    print(f"  Per Status:")
    for status, jumlah in stat.get('per_status', {}).items():
        print(f"    - {status:<12}: {jumlah} mahasiswa")
    print(f"  Per Program Studi:")
    for prodi, jumlah in stat.get('per_program_studi', {}).items():
        print(f"    - {prodi:<25}: {jumlah} mahasiswa")


# Testing helper functions
if __name__ == '__main__':
    cetak_judul("Testing Helper Functions")

    sample_data = [
        {'nim': '2023001', 'nama': 'Budi',  'ipk': 3.75, 'status': 'Aktif'},
        {'nim': '2023002', 'nama': 'Ani',   'ipk': 3.50, 'status': 'Aktif'},
        {'nim': '2023003', 'nama': 'Citra', 'ipk': 2.80, 'status': 'Cuti'},
    ]

    print(format_tabel(sample_data))
