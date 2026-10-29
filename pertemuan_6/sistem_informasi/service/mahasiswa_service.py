"""
Module: sistem_informasi.service.mahasiswa_service
====================================================
Implementasi operasi CRUD untuk entitas Mahasiswa.
Menggunakan dictionary sebagai penyimpanan in-memory.

Struktur storage:
    _db = {
        'NIM': Mahasiswa,
        ...
    }
"""

from sistem_informasi.model.mahasiswa import Mahasiswa


class MahasiswaService:
    """
    Service class untuk operasi CRUD entitas Mahasiswa.
    Data disimpan dalam dictionary in-memory (simulasi database).
    """

    def __init__(self):
        """Inisialisasi storage in-memory sebagai dictionary kosong."""
        self._db: dict[str, Mahasiswa] = {}

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────────────────────────────────

    def tambah(self, mahasiswa: Mahasiswa) -> dict:
        """
        Menambahkan mahasiswa baru ke storage.

        Args:
            mahasiswa (Mahasiswa): Objek mahasiswa yang akan ditambahkan

        Returns:
            dict: {'success': bool, 'message': str, 'data': dict|None}
        """
        # Validasi data
        is_valid, errors = mahasiswa.validasi()
        if not is_valid:
            return {
                'success': False,
                'message': f"Validasi gagal: {'; '.join(errors)}",
                'data'   : None,
            }

        # Cek duplikasi NIM
        if mahasiswa.nim in self._db:
            return {
                'success': False,
                'message': f"NIM '{mahasiswa.nim}' sudah terdaftar!",
                'data'   : None,
            }

        self._db[mahasiswa.nim] = mahasiswa
        return {
            'success': True,
            'message': f"Mahasiswa '{mahasiswa.nama}' berhasil ditambahkan",
            'data'   : mahasiswa.to_dict(),
        }

    def tambah_batch(self, daftar_mahasiswa: list) -> dict:
        """
        Menambahkan banyak mahasiswa sekaligus.

        Args:
            daftar_mahasiswa (list): List objek Mahasiswa

        Returns:
            dict: {'success': bool, 'berhasil': int, 'gagal': int, 'errors': list}
        """
        berhasil = 0
        gagal    = 0
        errors   = []

        for mhs in daftar_mahasiswa:
            hasil = self.tambah(mhs)
            if hasil['success']:
                berhasil += 1
            else:
                gagal += 1
                errors.append(f"[{mhs.nim}] {hasil['message']}")

        return {
            'success' : gagal == 0,
            'berhasil': berhasil,
            'gagal'   : gagal,
            'errors'  : errors,
        }

    # ─────────────────────────────────────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────────────────────────────────────

    def cari_nim(self, nim: str) -> dict:
        """
        Mencari mahasiswa berdasarkan NIM.

        Args:
            nim (str): NIM mahasiswa

        Returns:
            dict: {'success': bool, 'message': str, 'data': dict|None}
        """
        if nim in self._db:
            return {
                'success': True,
                'message': 'Mahasiswa ditemukan',
                'data'   : self._db[nim].to_dict(),
            }
        return {
            'success': False,
            'message': f"NIM '{nim}' tidak ditemukan",
            'data'   : None,
        }

    def cari_nama(self, keyword: str) -> dict:
        """
        Mencari mahasiswa berdasarkan kata kunci nama (case-insensitive).

        Args:
            keyword (str): Kata kunci pencarian nama

        Returns:
            dict: {'success': bool, 'message': str, 'data': list, 'total': int}
        """
        keyword_lower = keyword.lower()
        hasil = [
            mhs.to_dict()
            for mhs in self._db.values()
            if keyword_lower in mhs.nama.lower()
        ]
        return {
            'success': len(hasil) > 0,
            'message': f"{len(hasil)} mahasiswa ditemukan untuk keyword '{keyword}'",
            'data'   : hasil,
            'total'  : len(hasil),
        }

    def tampil_semua(self, filter_status: str = None, filter_prodi: str = None) -> dict:
        """
        Menampilkan semua mahasiswa, dengan filter opsional.

        Args:
            filter_status (str): Filter berdasarkan status (opsional)
            filter_prodi  (str): Filter berdasarkan program studi (opsional)

        Returns:
            dict: {'success': bool, 'data': list, 'total': int}
        """
        data = list(self._db.values())

        if filter_status:
            data = [m for m in data if m.status == filter_status]

        if filter_prodi:
            data = [m for m in data if m.program_studi == filter_prodi]

        return {
            'success': True,
            'data'   : [m.to_dict() for m in data],
            'total'  : len(data),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────────────────────────────────────

    def update(self, nim: str, data_baru: dict) -> dict:
        """
        Memperbarui data mahasiswa berdasarkan NIM.

        Args:
            nim      (str) : NIM mahasiswa yang akan diupdate
            data_baru(dict): Field-field yang akan diperbarui

        Returns:
            dict: {'success': bool, 'message': str, 'data': dict|None}
        """
        if nim not in self._db:
            return {
                'success': False,
                'message': f"NIM '{nim}' tidak ditemukan",
                'data'   : None,
            }

        mhs = self._db[nim]

        # Update field yang ada di data_baru
        field_dapat_diupdate = ['nama', 'program_studi', 'semester', 'ipk', 'status']
        field_diupdate = []

        for field in field_dapat_diupdate:
            if field in data_baru:
                setattr(mhs, field, data_baru[field])
                field_diupdate.append(field)

        # Validasi ulang setelah update
        is_valid, errors = mhs.validasi()
        if not is_valid:
            return {
                'success': False,
                'message': f"Validasi gagal setelah update: {'; '.join(errors)}",
                'data'   : None,
            }

        return {
            'success': True,
            'message': f"Data '{mhs.nama}' berhasil diperbarui. Field: {field_diupdate}",
            'data'   : mhs.to_dict(),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────────────────────────────────────

    def hapus(self, nim: str) -> dict:
        """
        Menghapus mahasiswa berdasarkan NIM.

        Args:
            nim (str): NIM mahasiswa yang akan dihapus

        Returns:
            dict: {'success': bool, 'message': str, 'data': dict|None}
        """
        if nim not in self._db:
            return {
                'success': False,
                'message': f"NIM '{nim}' tidak ditemukan",
                'data'   : None,
            }

        mhs = self._db.pop(nim)
        return {
            'success': True,
            'message': f"Mahasiswa '{mhs.nama}' ({nim}) berhasil dihapus",
            'data'   : mhs.to_dict(),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # STATISTIK
    # ─────────────────────────────────────────────────────────────────────────

    def statistik(self) -> dict:
        """Mengembalikan statistik ringkasan data mahasiswa."""
        if not self._db:
            return {'total': 0, 'pesan': 'Database kosong'}

        semua = list(self._db.values())
        ipk_list = [m.ipk for m in semua]

        return {
            'total'              : len(semua),
            'ipk_tertinggi'      : max(ipk_list),
            'ipk_terendah'       : min(ipk_list),
            'ipk_rata_rata'      : round(sum(ipk_list) / len(ipk_list), 2),
            'per_status'         : {
                s: sum(1 for m in semua if m.status == s)
                for s in set(m.status for m in semua)
            },
            'per_program_studi'  : {
                p: sum(1 for m in semua if m.program_studi == p)
                for p in set(m.program_studi for m in semua)
            },
        }

    def __len__(self) -> int:
        return len(self._db)

    def __repr__(self) -> str:
        return f"MahasiswaService(total={len(self._db)} mahasiswa)"


# Testing service CRUD
if __name__ == '__main__':
    print("Testing MahasiswaService (CRUD)")
    print("=" * 45)

    svc = MahasiswaService()

    # CREATE
    mhs1 = Mahasiswa('2023001', 'Budi', 'Teknik Informatika', 3, 3.75, 'Aktif')
    print(svc.tambah(mhs1))

    # READ
    print(svc.cari_nim('2023001'))

    # UPDATE
    print(svc.update('2023001', {'semester': 4, 'ipk': 3.80}))

    # DELETE
    print(svc.hapus('2023001'))
    print(svc.cari_nim('2023001'))
