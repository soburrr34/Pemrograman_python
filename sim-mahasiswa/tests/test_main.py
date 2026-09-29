# tests/test_main.py
import sys
import os

# Tambahkan path src agar bisa import models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from models import Mahasiswa, DaftarMahasiswa

class TestMahasiswa:
    def test_buat_mahasiswa_valid(self):
        mhs = Mahasiswa("202451001", "Andi Pratama",
                        "Sistem Informasi", 2024, 3.50)
        assert mhs.nim == "202451001"
        assert mhs.nama == "Andi Pratama"
        assert mhs.ipk == 3.50

    def test_nim_tidak_valid(self):
        with pytest.raises(ValueError):
            Mahasiswa("abc", "Test", "SI", 2024, 3.0)

    def test_ipk_diluar_range(self):
        with pytest.raises(ValueError):
            Mahasiswa("2024SI002", "Test", "SI", 2024, 5.0)

    def test_ipk_negatif(self):
        with pytest.raises(ValueError):
            Mahasiswa("2024SI003", "Test", "SI", 2024, -1.0)

    def test_nama_kosong(self):
        with pytest.raises(ValueError):
            Mahasiswa("2024SI004", "", "SI", 2024, 3.0)

class TestDaftarMahasiswa:
    def test_tambah_dan_cari(self):
        db = DaftarMahasiswa()
        mhs = Mahasiswa("202451001", "Andi", "SI", 2024)
        db.tambah(mhs)
        assert db.cari("202451001") == mhs
        assert db.jumlah == 1

    def test_nim_duplikat(self):
        db = DaftarMahasiswa()
        m1 = Mahasiswa("202451001", "Andi", "SI", 2024)
        m2 = Mahasiswa("202451001", "Budi", "SI", 2024)
        db.tambah(m1)
        with pytest.raises(ValueError):
            db.tambah(m2)

    def test_cari_tidak_ditemukan(self):
        db = DaftarMahasiswa()
        assert db.cari("999999999") is None

    def test_hapus_mahasiswa(self):
        db = DaftarMahasiswa()
        mhs = Mahasiswa("202451001", "Andi", "SI", 2024)
        db.tambah(mhs)
        hasil = db.hapus("202451001")
        assert hasil is True
        assert db.jumlah == 0

    def test_hapus_nim_tidak_ada(self):
        db = DaftarMahasiswa()
        hasil = db.hapus("999999999")
        assert hasil is False
