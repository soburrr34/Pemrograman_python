"""
Module: sistem_informasi.model.mahasiswa
==========================================
Mendefinisikan entitas Mahasiswa sebagai class dengan validasi data dasar.
Data disimpan sebagai dictionary untuk kompatibilitas in-memory storage.
"""

from datetime import datetime


PROGRAM_STUDI_VALID = [
    'Teknik Informatika',
    'Sistem Informasi',
    'Teknik Komputer',
    'Ilmu Komputer',
]

STATUS_VALID = ['Aktif', 'Cuti', 'Lulus', 'DO']


class Mahasiswa:
    """
    Representasi entitas Mahasiswa dalam sistem informasi akademik.

    Attributes:
        nim           (str)   : Nomor Induk Mahasiswa (primary key, unik)
        nama          (str)   : Nama lengkap mahasiswa
        program_studi (str)   : Program studi
        semester      (int)   : Semester saat ini (1-14)
        ipk           (float) : Indeks Prestasi Kumulatif (0.00-4.00)
        status        (str)   : Status mahasiswa (Aktif/Cuti/Lulus/DO)
        tanggal_daftar(str)   : Tanggal pendaftaran (otomatis)
    """

    def __init__(
        self,
        nim          : str,
        nama         : str,
        program_studi: str,
        semester     : int   = 1,
        ipk          : float = 0.00,
        status       : str   = 'Aktif',
    ):
        self.nim            = nim
        self.nama           = nama
        self.program_studi  = program_studi
        self.semester       = semester
        self.ipk            = ipk
        self.status         = status
        self.tanggal_daftar = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Representasi string saat di-print
    def __repr__(self) -> str:
        return (
            f"Mahasiswa(nim={self.nim!r}, nama={self.nama!r}, "
            f"prodi={self.program_studi!r}, semester={self.semester}, "
            f"ipk={self.ipk}, status={self.status!r})"
        )

    def __str__(self) -> str:
        return f"[{self.nim}] {self.nama} - {self.program_studi} (Sem {self.semester}, IPK: {self.ipk})"

    def to_dict(self) -> dict:
        """Mengkonversi objek Mahasiswa menjadi dictionary."""
        return {
            'nim'           : self.nim,
            'nama'          : self.nama,
            'program_studi' : self.program_studi,
            'semester'      : self.semester,
            'ipk'           : self.ipk,
            'status'        : self.status,
            'tanggal_daftar': self.tanggal_daftar,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Mahasiswa':
        """Membuat objek Mahasiswa dari dictionary."""
        mhs = cls(
            nim           = data['nim'],
            nama          = data['nama'],
            program_studi = data['program_studi'],
            semester      = data.get('semester', 1),
            ipk           = data.get('ipk', 0.00),
            status        = data.get('status', 'Aktif'),
        )
        if 'tanggal_daftar' in data:
            mhs.tanggal_daftar = data['tanggal_daftar']
        return mhs

    def validasi(self) -> tuple:
        """
        Memvalidasi data mahasiswa.

        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []

        if not self.nim or len(self.nim) < 5:
            errors.append("NIM minimal 5 karakter")

        if not self.nama or len(self.nama.strip()) < 3:
            errors.append("Nama minimal 3 karakter")

        if self.program_studi not in PROGRAM_STUDI_VALID:
            errors.append(
                f"Program studi harus salah satu dari {PROGRAM_STUDI_VALID}"
            )

        if not (1 <= self.semester <= 14):
            errors.append("Semester harus antara 1 hingga 14")

        if not (0.00 <= self.ipk <= 4.00):
            errors.append("IPK harus antara 0.00 hingga 4.00")

        if self.status not in STATUS_VALID:
            errors.append(f"Status harus salah satu dari {STATUS_VALID}")

        return (len(errors) == 0, errors)


# Testing entitas Mahasiswa
if __name__ == '__main__':
    print("Testing Entitas Mahasiswa")
    print("=" * 40)

    mhs = Mahasiswa(
        nim           = '2023001001',
        nama          = 'Budi Santoso',
        program_studi = 'Teknik Informatika',
        semester      = 3,
        ipk           = 3.75,
        status        = 'Aktif',
    )

    print(f"str : {mhs}")
    print(f"repr: {mhs!r}")
    print(f"dict: {mhs.to_dict()}")

    is_valid, errors = mhs.validasi()
    print(f"Valid: {is_valid}, Errors: {errors}")
