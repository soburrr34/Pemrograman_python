"""
Soal 5 - Identifikasi Code Smell dan Refactoring Sesuai PEP 8
============================================================
Program ini menyajikan:
1. Kode Sebelum Refactoring (Legacy Code) yang mengandung 5 Code Smell:
   - Magic Number  : Angka tanpa nama deskriptif bertebaran langsung di kode.
   - Duplikasi     : Logika perhitungan dan formatting berulang di beberapa tempat.
   - Long Method   : Satu fungsi raksasa yang menangani terlalu banyak tanggung jawab.
   - Deep Nesting  : Sarang percabangan bertingkat (if di dalam if di dalam loop) yang sulit dibaca.
   - Dead Code     : Variabel dan baris kode mati yang tidak pernah digunakan/dieksekusi.
2. Identifikasi & Penjelasan Masalah setiap Code Smell.
3. Kode Sesudah Refactoring yang mematuhi prinsip Clean Code, SRP (Single Responsibility Principle),
   Guard Clauses, PEP 8 type hints, dan docstring lengkap.
4. Verifikasi bahwa hasil eksekusi kode bersih identik dengan kode lama.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# BAGIAN 1: KODE SEBELUM REFACTORING (LEGACY CODE DENGAN 5 CODE SMELL)
# =====================================================================

def proses_mahasiswa_lama(mhs_list):
    # [CODE SMELL 1: LONG METHOD] - Fungsi ini mengerjakan validasi, kelulusan,
    # perhitungan beasiswa, pemformatan string, dan statistik sekaligus (> 60 baris).
    
    hasil = []
    # [CODE SMELL 5: DEAD CODE] - Variabel total_biaya_kampus di bawah ini didefinisikan tapi tidak pernah dipakai
    total_biaya_kampus = 100000000 
    
    for m in mhs_list:
        # [CODE SMELL 4: DEEP NESTING] - Tingkat indentasi bertingkat (level 1-5)
        if m is not None:
            if "nim" in m and "nama" in m:
                if len(m["nim"]) == 10:
                    ipk = m.get("ipk", 0)
                    sks = m.get("sks", 0)
                    penghasilan_ortu = m.get("penghasilan_ortu", 0)
                    
                    status_lulus = "Belum Lulus"
                    # [CODE SMELL 1: MAGIC NUMBER] - Angka 144, 2.0, 3.5, 3.0 tanpa konstanta
                    if sks >= 144:
                        if ipk >= 2.0:
                            if ipk >= 3.5:
                                status_lulus = "Lulus dengan Pujian (Cumlaude)"
                            elif ipk >= 3.0:
                                status_lulus = "Lulus Sangat Memuaskan"
                            else:
                                status_lulus = "Lulus Memuaskan"
                        else:
                            status_lulus = "Tidak Lulus (IPK Tidak Memenuhi)"
                    
                    # [CODE SMELL 1: MAGIC NUMBER & SMELL 2: DUPLIKASI]
                    # Logika perhitungan bantuan beasiswa berulang-ulang dengan magic number
                    beasiswa = 0
                    if ipk >= 3.5:
                        if penghasilan_ortu < 3000000:
                            # [CODE SMELL 2: DUPLIKASI] Rumus beasiswa penuh + subsidi hidup
                            beasiswa = 2500000 + 500000
                        else:
                            beasiswa = 2500000
                    elif ipk >= 3.0:
                        if penghasilan_ortu < 3000000:
                            # [CODE SMELL 2: DUPLIKASI] Rumus beasiswa sebagian + subsidi hidup
                            beasiswa = 1500000 + 500000
                        else:
                            beasiswa = 1500000
                    else:
                        beasiswa = 0
                        
                    hasil.append({
                        "nim": m["nim"],
                        "nama": m["nama"],
                        "status_lulus": status_lulus,
                        "nominal_beasiswa": beasiswa
                    })
                else:
                    hasil.append({"nim": m.get("nim", "-"), "error": "NIM tidak 10 digit"})
            else:
                hasil.append({"error": "Data mahasiswa tidak lengkap"})
                
    # [CODE SMELL 5: DEAD CODE] - Kode setelah return atau kondisi mustahil
    if False:
        print("Ini adalah dead code yang tidak akan pernah dieksekusi!")
        
    return hasil


# =====================================================================
# BAGIAN 2: IDENTIFIKASI DAN PENJELASAN 5 CODE SMELL
# =====================================================================

CATATAN_CODE_SMELL = [
    {
        "nama": "1. Magic Number",
        "baris": "sks >= 144, ipk >= 2.0, 3.5, 3.0, penghasilan_ortu < 3000000, 2500000, 500000",
        "masalah": (
            "Angka-angka harfiah tertulis langsung di badan kode tanpa nama variabel penjelas. "
            "Developer lain tidak memahami makna bisnis dari '144' atau '3000000', dan jika "
            "aturan kampus berubah (misal batas SKS jadi 140), pengembang harus mengubahnya di banyak tempat secara rawan keliru."
        ),
        "solusi": "Definisikan konstanta tingkat modul dengan nama deskriptif huruf kapital (misal: MIN_SKS_KELULUSAN = 144)."
    },
    {
        "nama": "2. Duplikasi Logika (Code Duplication)",
        "baris": "Perhitungan subsidi uang saku (+ 500000) dan percabangan beasiswa",
        "masalah": (
            "Pengecekan 'penghasilan_ortu < 3000000' dan penambahan uang saku 500000 ditulis ulang secara berulang "
            "pada setiap tingkatan IPK. Melanggar prinsip DRY (Don't Repeat Yourself)."
        ),
        "solusi": "Ekstraksi logika penentuan beasiswa dasar dan subsidi ekonomi ke fungsi terpisah yang dapat dikomposisikan."
    },
    {
        "nama": "3. Long Method / Large Function",
        "baris": "Fungsi proses_mahasiswa_lama() secara keseluruhan",
        "masalah": (
            "Satu fungsi memikul terlalu banyak tanggung jawab: iterasi list, validasi NIM, evaluasi kelulusan, "
            "kalkulasi beasiswa, serta perakitan output. Fungsi sulit dibaca, di-debug, dan diuji (unit-test)."
        ),
        "solusi": (
            "Terapkan Single Responsibility Principle (SRP). Pecah menjadi fungsi-fungsi kecil dan kohesif: "
            "validasi_data_mahasiswa(), tentukan_predikat_kelulusan(), hitung_tunjangan_beasiswa()."
        )
    },
    {
        "nama": "4. Deep Nesting (Pyramid of Doom)",
        "baris": "if m is not None -> if 'nim' in m -> if len() -> if sks -> if ipk -> if ...",
        "masalah": (
            "Percabangan bersarang hingga kedalaman 5 level menciptakan bentuk panah ('arrow anti-pattern'). "
            "Meningkatkan kompleksitas siklomatis (cyclomatic complexity) dan menyulitkan pembaca mengikuti alur logika."
        ),
        "solusi": "Gunakan Guard Clauses (Early Return) untuk menolak kasus invalid di awal dan memflatsasikan hierarki kode."
    },
    {
        "nama": "5. Dead Code (Kode Mati)",
        "baris": "total_biaya_kampus = 100000000 dan blok 'if False:'",
        "masalah": (
            "Variabel dialokasikan tetapi tidak pernah dibaca, serta blok kode yang tidak pernah bisa dieksekusi. "
            "Membuang memori, membingungkan pemelihara kode, dan mengaburkan esensi logika bisnis."
        ),
        "solusi": "Hapus seluruh variabel tak terpakai dan blok kode tak terjangkau."
    }
]


# =====================================================================
# BAGIAN 3: KODE HASIL REFACTORING (BERSIH, PEP 8, TYPE HINTS, DOCSTRING)
# =====================================================================

# --- KONSTANTA GLOBAL (MENGGANTIKAN MAGIC NUMBER) ---
MIN_SKS_KELULUSAN: int = 144
IPK_MINIMUM_LULUS: float = 2.00
IPK_CUMLAUDE: float = 3.50
IPK_SANGAT_MEMUASKAN: float = 3.00

AMBANG_BATAS_EKONOMI_LEMAH: int = 3_000_000
NOMINAL_BEASISWA_UTAMA: int = 2_500_000
NOMINAL_BEASISWA_SEBAGIAN: int = 1_500_000
NOMINAL_SUBSIDI_UANG_SAKU: int = 500_000

PANJANG_NIM_VALID: int = 10


@dataclass
class HasilEvaluasiMahasiswa:
    """Representasi data hasil evaluasi akademik dan finansial mahasiswa."""
    nim: str
    nama: str
    status_lulus: str
    nominal_beasiswa: int
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Mengonversi hasil evaluasi ke dictionary."""
        if self.error:
            res: Dict[str, Any] = {"error": self.error}
            if self.nim != "-":
                res = {"nim": self.nim, "error": self.error}
            return res
        return {
            "nim": self.nim,
            "nama": self.nama,
            "status_lulus": self.status_lulus,
            "nominal_beasiswa": self.nominal_beasiswa,
        }


def validasi_format_mahasiswa(data_mhs: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Memvalidasi kelengkapan kamus data mahasiswa dan format NIM.
    Menggunakan Guard Clauses untuk menghindari Deep Nesting.

    Args:
        data_mhs: Dictionary data mahasiswa atau None.

    Returns:
        Tuple[bool, Optional[str]]: (Status kevalidan, Pesan error jika tidak valid).
    """
    if data_mhs is None or not isinstance(data_mhs, dict):
        return False, "Data mahasiswa tidak lengkap"

    if "nim" not in data_mhs or "nama" not in data_mhs:
        return False, "Data mahasiswa tidak lengkap"

    nim = str(data_mhs["nim"]).strip()
    if len(nim) != PANJANG_NIM_VALID:
        return False, "NIM tidak 10 digit"

    return True, None


def tentukan_predikat_kelulusan(sks: int, ipk: float) -> str:
    """
    Mengevaluasi status kelulusan dan predikat mahasiswa berdasarkan SKS dan IPK.

    Args:
        sks: Jumlah satuan kredit semester yang telah diselesaikan.
        ipk: Indeks prestasi kumulatif (0.00 - 4.00).

    Returns:
        str: Keterangan predikat kelulusan mahasiswa.
    """
    if sks < MIN_SKS_KELULUSAN:
        return "Belum Lulus"

    if ipk < IPK_MINIMUM_LULUS:
        return "Tidak Lulus (IPK Tidak Memenuhi)"

    if ipk >= IPK_CUMLAUDE:
        return "Lulus dengan Pujian (Cumlaude)"

    if ipk >= IPK_SANGAT_MEMUASKAN:
        return "Lulus Sangat Memuaskan"

    return "Lulus Memuaskan"


def hitung_tunjangan_beasiswa(ipk: float, penghasilan_ortu: int) -> int:
    """
    Menghitung total nominal beasiswa berdasarkan prestasi IPK dan kondisi ekonomi keluarga.

    Args:
        ipk: Indeks prestasi kumulatif mahasiswa.
        penghasilan_ortu: Nominal pendapatan orang tua per bulan dalam Rupiah.

    Returns:
        int: Total tunjangan beasiswa yang diterima (dalam Rupiah).
    """
    # 1. Tentukan beasiswa prestasi pokok
    if ipk >= IPK_CUMLAUDE:
        beasiswa_pokok = NOMINAL_BEASISWA_UTAMA
    elif ipk >= IPK_SANGAT_MEMUASKAN:
        beasiswa_pokok = NOMINAL_BEASISWA_SEBAGIAN
    else:
        return 0  # Tidak berhak mendapatkan beasiswa

    # 2. Tentukan subsidi afirmatif uang saku (ekstraksi DRY)
    subsidi_ekonomi = NOMINAL_SUBSIDI_UANG_SAKU if penghasilan_ortu < AMBANG_BATAS_EKONOMI_LEMAH else 0

    return beasiswa_pokok + subsidi_ekonomi


def proses_evaluasi_mahasiswa_bersih(mhs_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fungsi orkestrasi bersih untuk memproses daftar mahasiswa.
    Telah di-refactor: Bebas magic number, bebas duplikasi, modular (SRP),
    menggunakan guard clauses (flat, tanpa deep nesting), serta bersih dari dead code.

    Args:
        mhs_list: Daftar data mahasiswa yang akan dievaluasi.

    Returns:
        List[Dict[str, Any]]: Daftar hasil evaluasi kelulusan dan beasiswa.
    """
    hasil_evaluasi: List[Dict[str, Any]] = []

    for item_mhs in mhs_list:
        # Guard clause 1: Validasi keberadaan data & struktur
        is_valid, pesan_error = validasi_format_mahasiswa(item_mhs)
        if not is_valid:
            nim_fallback = str(item_mhs.get("nim", "-")) if isinstance(item_mhs, dict) else "-"
            hasil_evaluasi.append(HasilEvaluasiMahasiswa(
                nim=nim_fallback,
                nama="",
                status_lulus="",
                nominal_beasiswa=0,
                error=pesan_error
            ).to_dict())
            continue

        # Ekstraksi field aman
        nim: str = str(item_mhs["nim"])
        nama: str = str(item_mhs["nama"])
        ipk: float = float(item_mhs.get("ipk", 0.0))
        sks: int = int(item_mhs.get("sks", 0))
        penghasilan_ortu: int = int(item_mhs.get("penghasilan_ortu", 0))

        # Delegasi logika bisnis ke sub-fungsi independen
        status_lulus = tentukan_predikat_kelulusan(sks=sks, ipk=ipk)
        beasiswa = hitung_tunjangan_beasiswa(ipk=ipk, penghasilan_ortu=penghasilan_ortu)

        hasil_evaluasi.append(HasilEvaluasiMahasiswa(
            nim=nim,
            nama=nama,
            status_lulus=status_lulus,
            nominal_beasiswa=beasiswa
        ).to_dict())

    return hasil_evaluasi


# =====================================================================
# BAGIAN 4: VERIFIKASI HASIL & PROGRAM UTAMA
# =====================================================================

def main():
    print("=" * 75)
    print("SOAL 5: REFACTORING CODE SMELL SESUAI PRINSIP CLEAN CODE & PEP 8")
    print("=" * 75)

    print("\n" + "-" * 75)
    print("1. TABEL ANALISIS CODE SMELL DAN SOLUSI REFACTORING")
    print("-" * 75)
    for c in CATATAN_CODE_SMELL:
        print(f"\n[{c['nama']}]")
        print(f"  * Lokasi Kode : {c['baris']}")
        print(f"  * Masalah     : {c['masalah']}")
        print(f"  * Solusi      : {c['solusi']}")

    # Dataset pengujian
    data_uji = [
        {"nim": "2024101001", "nama": "Ahmad Fauzi", "sks": 146, "ipk": 3.80, "penghasilan_ortu": 2_500_000},
        {"nim": "2024101002", "nama": "Budi Santoso", "sks": 144, "ipk": 3.20, "penghasilan_ortu": 5_000_000},
        {"nim": "2024132046", "nama": "Sobur", "sks": 148, "ipk": 3.90, "penghasilan_ortu": 1_800_000},
        {"nim": "2024101004", "nama": "Citra", "sks": 120, "ipk": 3.60, "penghasilan_ortu": 2_000_000},
        {"nim": "2024101005", "nama": "Doni", "sks": 144, "ipk": 1.90, "penghasilan_ortu": 3_500_000},
        {"nim": "202410", "nama": "Eka", "sks": 144, "ipk": 3.50},  # NIM pendek
        {"sks": 100},  # Tidak ada nama & NIM
    ]

    print("\n" + "-" * 75)
    print("2. VERIFIKASI EKUIVALENSI OUTPUT KODE LAMA VS KODE BERSIH")
    print("-" * 75)

    hasil_lama = proses_mahasiswa_lama(data_uji)
    hasil_baru = proses_evaluasi_mahasiswa_bersih(data_uji)

    # Pastikan kedua implementasi menghasilkan output yang sama persis
    is_identik = hasil_lama == hasil_baru
    print(f"Hasil Eksekusi Identik 100% : {'YA (VALID)' if is_identik else 'TIDAK (ADA SELISIH)'}")
    print("-" * 75)
    print(f"{'NIM':<12} {'Nama':<15} {'Status Kelulusan':<32} {'Beasiswa':<12}")
    print("-" * 75)
    for row in hasil_baru:
        if "error" in row:
            print(f"{row.get('nim', '-'):<12} {'[ERROR]':<15} {row['error']:<32} {'-':<12}")
        else:
            print(f"{row['nim']:<12} {row['nama']:<15} {row['status_lulus']:<32} Rp {row['nominal_beasiswa']:,}")
    print("=" * 75)


if __name__ == "__main__":
    main()
