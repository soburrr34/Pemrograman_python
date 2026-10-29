"""
Package: sistem_informasi
==========================
Package untuk Sistem Informasi Akademik Mahasiswa.
Menyediakan CRUD untuk entitas Mahasiswa menggunakan in-memory dictionary.

Subpackage:
    - model   : Definisi entitas data (Mahasiswa)
    - service : Business logic & operasi CRUD
    - utils   : Fungsi pembantu (formatter, validator)
"""

# Ekspor publik package
from sistem_informasi.model.mahasiswa import Mahasiswa
from sistem_informasi.service.mahasiswa_service import MahasiswaService
from sistem_informasi.utils.helper import (
    format_tabel,
    cetak_judul,
)

__version__ = '1.0.0'
__author__  = 'Tim Pemrograman Python'

__all__ = [
    'Mahasiswa',
    'MahasiswaService',
    'format_tabel',
    'cetak_judul',
]
