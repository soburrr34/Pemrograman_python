# src/models.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Mahasiswa:
    """Model data mahasiswa untuk Sistem Informasi."""
    nim: str
    nama: str
    program_studi: str
    angkatan: int
    ipk: float = 0.0

    def __post_init__(self):
        """Validasi data setelah inisialisasi."""
        if not self.nim or len(self.nim) < 6:
            raise ValueError(f"NIM tidak valid: {self.nim}")
        if not self.nama:
            raise ValueError("Nama tidak boleh kosong")
        if not (0.0 <= self.ipk <= 4.0):
            raise ValueError(f"IPK harus 0.0-4.0, got {self.ipk}")

    def __str__(self) -> str:
        return (f"{self.nim} | {self.nama:<30} | "
                f"{self.program_studi:<20} | {self.angkatan} | "
                f"IPK: {self.ipk:.2f}")

@dataclass
class DaftarMahasiswa:
    """Koleksi data mahasiswa dengan operasi CRUD."""
    data: List[Mahasiswa] = field(default_factory=list)

    def tambah(self, mhs: Mahasiswa) -> None:
        """Tambah mahasiswa baru (NIM harus unik)."""
        if self.cari(mhs.nim):
            raise ValueError(f"NIM {mhs.nim} sudah terdaftar")
        self.data.append(mhs)

    def cari(self, nim: str) -> Optional[Mahasiswa]:
        """Cari mahasiswa berdasarkan NIM."""
        for mhs in self.data:
            if mhs.nim == nim:
                return mhs
        return None

    def hapus(self, nim: str) -> bool:
        """Hapus mahasiswa berdasarkan NIM."""
        mhs = self.cari(nim)
        if mhs:
            self.data.remove(mhs)
            return True
        return False

    @property
    def jumlah(self) -> int:
        return len(self.data)
