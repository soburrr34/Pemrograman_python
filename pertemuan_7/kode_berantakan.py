# File simulasi kode tidak patuh standar
import json
import math
import os
import sys
from datetime import datetime


def fungsi_berantakan(a, b, c):
    # Black violation: spasi di dalam kurung dan operator tanpa spasi
    hasil = a + b * c
    variabel_tidak_terpakai = 999  # Flake8 violation: F841 local variable never used

    # Flake8 violation: E501 line too long (> 88 karakter)
    pesan_sangat_panjang_sekali_yang_melebihi_batas_maksimum_kolom_delapan_puluh_delapan_karakter_pep8 = "Ini adalah string yang sengaja dibuat sangat amat panjang agar ditangkap linter flake8"

    if hasil > 10:
        return {"status": "ok", "nilai": hasil}
    else:
        return {"status": "kurang", "nilai": hasil}
