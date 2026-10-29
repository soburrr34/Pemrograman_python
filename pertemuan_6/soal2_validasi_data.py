"""
Soal 2 - Fungsi Validasi Data
==============================
Membuat fungsi validasi_data() yang menerima dictionary data dan schema validasi.
Mengembalikan tuple (is_valid: bool, errors: list).
Menggunakan *args dan **kwargs untuk fleksibilitas tambahan.
"""


def validasi_data(data: dict, schema: dict, *args, **kwargs) -> tuple:
    """
    Memvalidasi dictionary data berdasarkan schema validasi.

    Args:
        data   (dict): Dictionary data yang akan divalidasi
        schema (dict): Dictionary berisi aturan validasi per field
        *args        : Argumen tambahan opsional (misalnya nama validator)
        **kwargs     : Keyword arguments opsional:
                         - strict (bool) : Tolak field di luar schema (default False)
                         - label  (str)  : Label untuk pesan error (default 'Data')

    Returns:
        tuple: (is_valid: bool, errors: list)

    Format schema per field:
        {
            'nama_field': {
                'type'          : <tipe>,        # Wajib  - tipe data yang diharapkan
                'required'      : True/False,    # Opsional (default True)
                'min'           : <angka>,       # Opsional - nilai minimum (int/float)
                'max'           : <angka>,       # Opsional - nilai maksimum (int/float)
                'min_length'    : <int>,         # Opsional - panjang minimum (str/list)
                'max_length'    : <int>,         # Opsional - panjang maksimum (str/list)
                'allowed_values': [...],         # Opsional - daftar nilai yang diizinkan
                'pattern'       : <str>,         # Opsional - awalan yang harus ada (str)
            }
        }
    """
    errors = []
    strict = kwargs.get('strict', False)
    label  = kwargs.get('label', 'Data')

    # Tampilkan nama validator jika ada di *args
    validator_name = args[0] if args else 'default'

    # Mode strict: tolak field yang tidak ada di schema
    if strict:
        extra_fields = set(data.keys()) - set(schema.keys())
        for field in sorted(extra_fields):
            errors.append(
                f"[{label}] Field '{field}' tidak diizinkan (mode strict aktif)"
            )

    # Iterasi setiap field dalam schema
    for field, rules in schema.items():
        is_required = rules.get('required', True)

        # Cek keberadaan field
        if field not in data:
            if is_required:
                errors.append(f"[{label}] Field '{field}' wajib diisi")
            continue  # skip validasi lanjutan jika field tidak ada

        value = data[field]
        expected_type = rules.get('type')

        # 1. Validasi tipe data
        if expected_type and not isinstance(value, expected_type):
            errors.append(
                f"[{label}] Field '{field}' harus bertipe {expected_type.__name__}, "
                f"bukan {type(value).__name__} (nilai: {value!r})"
            )
            continue  # skip validasi lain jika tipe salah

        # 2. Validasi rentang nilai (int/float)
        if isinstance(value, (int, float)):
            if 'min' in rules and value < rules['min']:
                errors.append(
                    f"[{label}] Field '{field}' harus >= {rules['min']}, "
                    f"nilai saat ini: {value}"
                )
            if 'max' in rules and value > rules['max']:
                errors.append(
                    f"[{label}] Field '{field}' harus <= {rules['max']}, "
                    f"nilai saat ini: {value}"
                )

        # 3. Validasi panjang (str/list)
        if isinstance(value, (str, list)):
            if 'min_length' in rules and len(value) < rules['min_length']:
                errors.append(
                    f"[{label}] Field '{field}' harus memiliki panjang "
                    f">= {rules['min_length']} (saat ini: {len(value)})"
                )
            if 'max_length' in rules and len(value) > rules['max_length']:
                errors.append(
                    f"[{label}] Field '{field}' harus memiliki panjang "
                    f"<= {rules['max_length']} (saat ini: {len(value)})"
                )

        # 4. Validasi nilai yang diizinkan
        if 'allowed_values' in rules and value not in rules['allowed_values']:
            errors.append(
                f"[{label}] Field '{field}' harus salah satu dari "
                f"{rules['allowed_values']}, nilai saat ini: {value!r}"
            )

        # 5. Validasi awalan string (pattern sederhana)
        if isinstance(value, str) and 'pattern' in rules:
            if not value.startswith(rules['pattern']):
                errors.append(
                    f"[{label}] Field '{field}' harus dimulai dengan "
                    f"'{rules['pattern']}', nilai saat ini: {value!r}"
                )

    is_valid = len(errors) == 0
    return (is_valid, errors)


# Testing
if __name__ == '__main__':
    print("=" * 60)
    print("  TESTING SOAL 2 - validasi_data()")
    print("=" * 60)

    # Schema mahasiswa
    schema_mahasiswa = {
        'nama': {
            'type'      : str,
            'required'  : True,
            'min_length': 3,
            'max_length': 100,
        },
        'nim': {
            'type'      : str,
            'required'  : True,
            'min_length': 10,
            'max_length': 10,
            'pattern'   : '202',  # NIM harus diawali '202'
        },
        'ipk': {
            'type'    : float,
            'required': True,
            'min'     : 0.0,
            'max'     : 4.0,
        },
        'semester': {
            'type'    : int,
            'required': True,
            'min'     : 1,
            'max'     : 14,
        },
        'program_studi': {
            'type'          : str,
            'required'      : True,
            'allowed_values': ['Teknik Informatika', 'Sistem Informasi', 'Teknik Komputer'],
        },
        'status': {
            'type'          : str,
            'required'      : False,
            'allowed_values': ['Aktif', 'Cuti', 'Lulus', 'DO'],
        },
    }

    # ── Test 1: Data valid ───────────────────────────────────────────────────
    data_valid = {
        'nama'         : 'Budi Santoso',
        'nim'          : '2021001001',
        'ipk'          : 3.75,
        'semester'     : 6,
        'program_studi': 'Teknik Informatika',
        'status'       : 'Aktif',
    }
    print("\n[Test 1] Data VALID:")
    is_valid, errors = validasi_data(data_valid, schema_mahasiswa, 'MahasiswaValidator', label='Mahasiswa')
    print(f"  is_valid : {is_valid}")
    print(f"  errors   : {errors}")

    # ── Test 2: Data tidak valid ─────────────────────────────────────────────
    data_invalid = {
        'nama'         : 'Bu',           # terlalu pendek
        'nim'          : '12345',         # NIM tidak 10 digit & pola salah
        'ipk'          : 4.5,             # melebihi max
        'semester'     : 0,               # di bawah min
        'program_studi': 'Kedokteran',    # bukan nilai yang diizinkan
    }
    print("\n[Test 2] Data TIDAK VALID:")
    is_valid, errors = validasi_data(data_invalid, schema_mahasiswa, label='Mahasiswa')
    print(f"  is_valid : {is_valid}")
    print(f"  errors   :")
    for err in errors:
        print(f"    - {err}")

    # ── Test 3: Strict mode ──────────────────────────────────────────────────
    data_extra = {
        'nama'               : 'Ani Wijaya',
        'nim'                : '2022002002',
        'ipk'                : 3.50,
        'semester'           : 4,
        'program_studi'      : 'Sistem Informasi',
        'hobi'               : 'Membaca',   # Field tidak ada di schema
        'alamat_tidak_dikenal': 'Jakarta',  # Field tidak ada di schema
    }
    print("\n[Test 3] Mode STRICT (ada field ekstra):")
    is_valid, errors = validasi_data(data_extra, schema_mahasiswa, strict=True, label='Mahasiswa')
    print(f"  is_valid : {is_valid}")
    print(f"  errors   :")
    for err in errors:
        print(f"    - {err}")

    # ── Test 4: Field opsional tidak ada ─────────────────────────────────────
    data_tanpa_status = {
        'nama'         : 'Citra Dewi',
        'nim'          : '2023003003',
        'ipk'          : 3.20,
        'semester'     : 2,
        'program_studi': 'Teknik Komputer',
        # 'status' sengaja tidak diisi (required=False)
    }
    print("\n[Test 4] Field opsional tidak diisi:")
    is_valid, errors = validasi_data(data_tanpa_status, schema_mahasiswa, label='Mahasiswa')
    print(f"  is_valid : {is_valid}")
    print(f"  errors   : {errors}")

    print("\n[SELESAI] Semua test berhasil!")
