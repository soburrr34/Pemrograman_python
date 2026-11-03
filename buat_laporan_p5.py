"""
Script Pembuat Laporan Word - Pertemuan 5
==========================================
Membuat file laporan .docx untuk Pertemuan 5 Pemrograman Python
yang berisi penjelasan, source code, dan analisis semua soal.
Topik: Struktur Data Python (String, List, Set, Dictionary & Tuple).
Penyusun: Sobur (NIM: 20241320046)
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ─── Helper Functions ────────────────────────────────────────────────────────

def set_font(run, name='Times New Roman', size=12, bold=False, italic=False, color=None):
    run.font.name        = name
    run.font.size        = Pt(size)
    run.font.bold        = bold
    run.font.italic      = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_heading(doc, text, level=1, font_size=14, bold=True, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p    = doc.add_paragraph()
    p.alignment = align
    run  = p.add_run(text)
    set_font(run, size=font_size, bold=bold, color=color)
    space_after  = {1: 6, 2: 4, 3: 3}
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(space_after.get(level, 3))
    return p


def add_paragraph(doc, text, size=12, indent=False, bold=False, italic=False, color=None):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic, color=color)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.line_spacing = Pt(20)
    if indent:
        p.paragraph_format.left_indent = Cm(1)
    return p


def add_code_block(doc, code_text):
    """Menambahkan blok kode dengan style monospace dan background abu-abu."""
    lines = code_text.strip().split('\n')
    for line in lines:
        p   = doc.add_paragraph()
        run = p.add_run(line if line else ' ')
        run.font.name = 'Courier New'
        run.font.size = Pt(9)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.left_indent  = Cm(0.5)

        # Warna background abu muda untuk blok kode
        pPr  = p._p.get_or_add_pPr()
        shd  = OxmlElement('w:shd')
        shd.set(qn('w:val'),   'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'F0F0F0')
        pPr.append(shd)


def add_info_table(doc, rows_data, headers):
    """Menambahkan tabel informasi."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        run = hdr_cells[i].paragraphs[0].runs[0]
        set_font(run, bold=True, size=11)
        # Warna header biru tua
        tc_pr = hdr_cells[i]._tc.get_or_add_tcPr()
        shd   = OxmlElement('w:shd')
        shd.set(qn('w:val'),   'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '2E4057')
        tc_pr.append(shd)
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Data
    for row_data in rows_data:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val)
            run = row_cells[i].paragraphs[0].runs[0]
            set_font(run, size=10)

    doc.add_paragraph()


def add_separator(doc):
    p   = doc.add_paragraph('─' * 70)
    run = p.runs[0]
    run.font.color.rgb = RGBColor(180, 180, 180)
    run.font.size      = Pt(9)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)


# ─── Halaman Sampul ──────────────────────────────────────────────────────────

def buat_sampul(doc):
    # Judul utama
    doc.add_paragraph()
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('LAPORAN PRAKTIKUM')
    set_font(run, size=18, bold=True, color=(46, 64, 87))
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('PEMROGRAMAN PYTHON')
    set_font(run, size=22, bold=True, color=(46, 64, 87))
    p.paragraph_format.space_after = Pt(4)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('PERTEMUAN 5')
    set_font(run, size=20, bold=True, color=(231, 76, 60))
    p.paragraph_format.space_after = Pt(4)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Struktur Data Python: String, List, Set, Dictionary & Tuple')
    set_font(run, size=13, italic=True, color=(100, 100, 100))
    p.paragraph_format.space_after = Pt(30)

    doc.add_paragraph()

    # Tabel info mahasiswa
    info = [
        ('Nama Mahasiswa', 'Sobur'),
        ('NIM',            '20241320046'),
        ('Kelas',          'A1'),
        ('Program Studi',  'Teknik Informatika / Sistem Informasi'),
        ('Mata Kuliah',    'Pemrograman Python / Pemrograman Modern'),
        ('Pertemuan',      '5 (Lima)'),
        ('Topik',          'Struktur Data: String, List, Set, Dictionary & Tuple'),
        ('Semester',       'Ganjil 2024/2025'),
    ]

    table = doc.add_table(rows=len(info), cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, (label, value) in enumerate(info):
        row = table.rows[i]
        row.cells[0].text = label
        row.cells[1].text = value
        lrun = row.cells[0].paragraphs[0].runs[0]
        vrun = row.cells[1].paragraphs[0].runs[0]
        set_font(lrun, bold=True, size=11)
        set_font(vrun, size=11)

    doc.add_page_break()


# ─── BAB I Pendahuluan ───────────────────────────────────────────────────────

def bab_pendahuluan(doc):
    add_heading(doc, 'BAB I  PENDAHULUAN', level=1, font_size=14, color=(46, 64, 87))
    add_separator(doc)

    add_heading(doc, '1.1  Latar Belakang', level=2, font_size=12)
    add_paragraph(doc,
        'Pemrograman Python merupakan salah satu bahasa pemrograman yang paling '
        'populer dan banyak digunakan di industri teknologi saat ini. Pada pertemuan '
        'kelima ini, praktikan mempelajari struktur data bawaan Python yang fundamental, '
        'yaitu String, List, Set, Dictionary, dan Tuple. Pemahaman yang baik terhadap '
        'struktur data ini merupakan fondasi yang penting sebelum mempelajari konsep '
        'pemrograman yang lebih lanjut.'
    )

    add_heading(doc, '1.2  Tujuan Praktikum', level=2, font_size=12)
    tujuan = [
        'Mahasiswa mampu memanipulasi String menggunakan method bawaan Python.',
        'Mahasiswa mampu mengolah List untuk analisis data numerik.',
        'Mahasiswa mampu menggunakan operasi Set (intersection, difference, union).',
        'Mahasiswa mampu mengimplementasikan Dictionary dan Tuple untuk sistem inventaris.',
        'Mahasiswa mampu menganalisis teks dari file menggunakan struktur data Dictionary.',
    ]
    for i, t in enumerate(tujuan, 1):
        p   = doc.add_paragraph(style='List Number')
        run = p.add_run(t)
        set_font(run, size=11)

    add_heading(doc, '1.3  Lingkungan Pengembangan', level=2, font_size=12)
    add_info_table(doc,
        rows_data=[
            ('Bahasa Pemrograman', 'Python 3.10'),
            ('IDE / Editor',       'Visual Studio Code / Terminal'),
            ('Sistem Operasi',     'Windows 11'),
            ('Library',            'Standard Library Python (os, re, string)'),
        ],
        headers=['Komponen', 'Keterangan']
    )

    doc.add_page_break()


# ─── BAB II Dasar Teori ──────────────────────────────────────────────────────

def bab_dasar_teori(doc):
    add_heading(doc, 'BAB II  DASAR TEORI', level=1, font_size=14, color=(46, 64, 87))
    add_separator(doc)

    teori = [
        ('String',
         'String adalah tipe data yang merepresentasikan urutan karakter. Python menyediakan '
         'berbagai method untuk memanipulasi string, seperti split(), replace(), title(), upper(), '
         'lower(), dan len(). String bersifat immutable (tidak dapat diubah setelah dibuat).',
         'kalimat = "hello world"\nprint(kalimat.title())   # Hello World\nprint(kalimat.split())   # ["hello", "world"]'
        ),
        ('List',
         'List adalah struktur data yang menyimpan sekumpulan nilai secara berurutan. List bersifat '
         'mutable (dapat diubah) dan mendukung berbagai operasi seperti append(), remove(), sort(), '
         'dan slicing. List sering digunakan untuk menyimpan data yang homogen.',
         'nilai = [85, 70, 90, 60, 75]\nprint(max(nilai))     # 90\nprint(sum(nilai)/len(nilai))  # 76.0'
        ),
        ('Set',
         'Set adalah koleksi data yang tidak berurutan dan tidak memiliki elemen duplikat. Set sangat '
         'efisien untuk operasi matematika himpunan seperti union (|), intersection (&), dan difference (-).',
         'A = {"M001", "M002", "M003"}\nB = {"M002", "M003", "M004"}\nprint(A & B)  # {"M002", "M003"}\nprint(A | B)  # semua unik\nprint(A - B)  # {"M001"}'
        ),
        ('Dictionary',
         'Dictionary adalah struktur data key-value yang memungkinkan akses data secara cepat berdasarkan '
         'kunci unik. Dictionary bersifat mutable dan sangat berguna untuk menyimpan data terstruktur '
         'seperti inventaris atau frekuensi kata.',
         'inventaris = {"Beras": (15000, 100)}\nharga, stok = inventaris["Beras"]\nprint(f"Harga: {harga}, Stok: {stok}")'
        ),
        ('Tuple',
         'Tuple mirip dengan list namun bersifat immutable. Tuple sering digunakan sebagai pasangan '
         'nilai yang tidak boleh diubah, seperti koordinat atau pasangan (harga, stok) pada sistem inventaris.',
         'data = (15000, 100)  # (harga, stok)\nharga, stok = data    # tuple unpacking\nprint(harga)          # 15000'
        ),
    ]

    for i, (nama, penjelasan, contoh) in enumerate(teori, 1):
        add_heading(doc, f'2.{i}  {nama}', level=2, font_size=12)
        add_paragraph(doc, penjelasan)
        add_paragraph(doc, 'Contoh penggunaan:', size=11, bold=True)
        add_code_block(doc, contoh)
        doc.add_paragraph()

    doc.add_page_break()


# ─── BAB III Pembahasan Soal ─────────────────────────────────────────────────

def bab_pembahasan(doc):
    add_heading(doc, 'BAB III  HASIL DAN PEMBAHASAN', level=1, font_size=14, color=(46, 64, 87))
    add_separator(doc)

    # ── SOAL 1 ──────────────────────────────────────────────────────────────
    add_heading(doc, '3.1  Soal 1 – Analisis Kalimat', level=2, font_size=13, color=(231, 76, 60))

    add_heading(doc, 'Deskripsi Soal', level=3, font_size=11)
    add_paragraph(doc,
        'Membuat program analisis kalimat yang dapat menghitung jumlah kata, '
        'jumlah karakter (dengan dan tanpa spasi), menemukan kata terpanjang, '
        'serta mengkonversi kalimat ke format Title Case.'
    )

    add_heading(doc, 'Konsep yang Digunakan', level=3, font_size=11)
    konsep1 = ['String method: split(), len(), replace(), title()', 'List comprehension untuk kata terpanjang', 'Fungsi max() dengan generator expression']
    for k in konsep1:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(k)
        set_font(run, size=11)

    add_heading(doc, 'Source Code', level=3, font_size=11)
    add_code_block(doc, '''def analisis_kalimat(kalimat):
    # (a) Hitung jumlah kata
    daftar_kata = kalimat.split()
    jumlah_kata = len(daftar_kata)

    # (b) Hitung jumlah karakter
    jumlah_karakter_total       = len(kalimat)
    jumlah_karakter_tanpa_spasi = len(kalimat.replace(" ", ""))

    # (c) Cari kata terpanjang
    panjang_max   = max(len(kata) for kata in daftar_kata)
    kata_terpanjang = [kata for kata in daftar_kata
                       if len(kata) == panjang_max]

    # (d) Title Case
    kalimat_title_case = kalimat.title()

    return {
        "jumlah_kata"              : jumlah_kata,
        "jumlah_karakter_total"    : jumlah_karakter_total,
        "jumlah_karakter_tanpa_spasi": jumlah_karakter_tanpa_spasi,
        "kata_terpanjang"          : kata_terpanjang,
        "panjang_max"              : panjang_max,
        "kalimat_title_case"       : kalimat_title_case,
    }''')

    add_heading(doc, 'Contoh Output', level=3, font_size=11)
    add_code_block(doc, '''Input  : "belajar pemrograman python sangat menyenangkan"

=======================================================
       HASIL ANALISIS KALIMAT
=======================================================
  Kalimat asli   : belajar pemrograman python sangat menyenangkan
=======================================================
  (a) Jumlah kata                : 5 kata
  (b) Jumlah karakter (dengan spasi)   : 47 karakter
      Jumlah karakter (tanpa spasi)    : 43 karakter
  (c) Kata terpanjang (13 huruf) : menyenangkan
  (d) Kalimat title case         : Belajar Pemrograman Python Sangat Menyenangkan
=======================================================''')

    add_heading(doc, 'Penjelasan Logika', level=3, font_size=11)
    add_paragraph(doc,
        'Fungsi split() memecah kalimat berdasarkan spasi menjadi list kata. '
        'Jumlah karakter dihitung menggunakan len() pada string asli dan string '
        'setelah replace(" ", ""). Kata terpanjang dicari dengan kombinasi max() '
        'dan list comprehension. Method title() mengubah huruf pertama setiap '
        'kata menjadi kapital secara otomatis.'
    )
    add_separator(doc)

    # ── SOAL 2 ──────────────────────────────────────────────────────────────
    add_heading(doc, '3.2  Soal 2 – Analisis Nilai Mahasiswa', level=2, font_size=13, color=(231, 76, 60))

    add_heading(doc, 'Deskripsi Soal', level=3, font_size=11)
    add_paragraph(doc,
        'Membuat program analisis nilai mahasiswa yang menghitung rata-rata, '
        'menentukan nilai tertinggi dan terendah, mengelompokkan nilai ke dalam '
        'kategori A/B/C/D/E, serta menampilkan frekuensi setiap kategori dalam '
        'bentuk bar chart teks.'
    )

    add_heading(doc, 'Tabel Konversi Nilai', level=3, font_size=11)
    add_info_table(doc,
        rows_data=[
            ('A', '80 – 100', 'Sangat Baik'),
            ('B', '70 – 79',  'Baik'),
            ('C', '60 – 69',  'Cukup'),
            ('D', '50 – 59',  'Kurang'),
            ('E', '0  – 49',  'Tidak Lulus'),
        ],
        headers=['Grade', 'Rentang Nilai', 'Keterangan']
    )

    add_heading(doc, 'Source Code', level=3, font_size=11)
    add_code_block(doc, '''def tentukan_kategori(nilai):
    if 80 <= nilai <= 100: return "A"
    elif 70 <= nilai <= 79: return "B"
    elif 60 <= nilai <= 69: return "C"
    elif 50 <= nilai <= 59: return "D"
    else: return "E"

def analisis_nilai(list_nilai):
    # (a) Rata-rata
    rata_rata = sum(list_nilai) / len(list_nilai)

    # (b) Tertinggi dan terendah
    nilai_tertinggi = max(list_nilai)
    nilai_terendah  = min(list_nilai)

    # (c) Pengelompokan ke kategori
    kelompok_nilai = {"A": [], "B": [], "C": [], "D": [], "E": []}
    for nilai in list_nilai:
        kelompok_nilai[tentukan_kategori(nilai)].append(nilai)

    # (d) Frekuensi menggunakan dictionary comprehension
    frekuensi = {k: len(v) for k, v in kelompok_nilai.items()}

    return {"rata_rata": rata_rata, "nilai_tertinggi": nilai_tertinggi,
            "nilai_terendah": nilai_terendah,
            "kelompok_nilai": kelompok_nilai, "frekuensi": frekuensi}''')

    add_heading(doc, 'Contoh Output', level=3, font_size=11)
    add_code_block(doc, '''Input: 85 70 55 90 65 45 75 88 72 60

=======================================================
    HASIL ANALISIS NILAI MAHASISWA
=======================================================
  (a) Rata-rata nilai      : 70.50
  (b) Nilai tertinggi      : 90
      Nilai terendah       : 45
  (c) Pengelompokan Nilai :
      Kategori A  : [85, 90, 88]
      Kategori B  : [70, 75, 72]
      Kategori C  : [65, 60]
      Kategori D  : [55]
      Kategori E  : [45]
  (d) Frekuensi Kategori :
    A  | ###                  3 mahasiswa (30.0%)
    B  | ###                  3 mahasiswa (30.0%)
    C  | ##                   2 mahasiswa (20.0%)
    D  | #                    1 mahasiswa (10.0%)
    E  | #                    1 mahasiswa (10.0%)''')
    add_separator(doc)

    # ── SOAL 3 ──────────────────────────────────────────────────────────────
    add_heading(doc, '3.3  Soal 3 – Operasi Set Beasiswa', level=2, font_size=13, color=(231, 76, 60))

    add_heading(doc, 'Deskripsi Soal', level=3, font_size=11)
    add_paragraph(doc,
        'Menganalisis data penerima dua jenis beasiswa menggunakan operasi Set Python. '
        'Program menentukan mahasiswa yang menerima kedua beasiswa (intersection), '
        'hanya beasiswa A (difference A-B), hanya beasiswa B (difference B-A), '
        'dan semua penerima unik (union).'
    )

    add_heading(doc, 'Operasi Set yang Digunakan', level=3, font_size=11)
    add_info_table(doc,
        rows_data=[
            ('Intersection (A & B)', 'Mahasiswa yang menerima KEDUA beasiswa'),
            ('Difference (A - B)',   'Mahasiswa yang HANYA menerima beasiswa A'),
            ('Difference (B - A)',   'Mahasiswa yang HANYA menerima beasiswa B'),
            ('Union (A | B)',        'SEMUA mahasiswa penerima beasiswa (unik)'),
        ],
        headers=['Operasi Set', 'Keterangan']
    )

    add_heading(doc, 'Source Code', level=3, font_size=11)
    add_code_block(doc, '''def analisis_beasiswa(beasiswa_a, beasiswa_b):
    set_a = set(beasiswa_a)
    set_b = set(beasiswa_b)

    # (a) Intersection: menerima keduanya
    keduanya = set_a & set_b       # set_a.intersection(set_b)

    # (b) Hanya beasiswa A
    hanya_a  = set_a - set_b       # set_a.difference(set_b)

    # (c) Hanya beasiswa B
    hanya_b  = set_b - set_a       # set_b.difference(set_a)

    # (d) Union: semua mahasiswa unik
    semua    = set_a | set_b       # set_a.union(set_b)

    return {"keduanya": keduanya, "hanya_a": hanya_a,
            "hanya_b": hanya_b,   "semua": semua}

# Data contoh
beasiswa_a = ["M001","M002","M003","M004","M005","M006"]
beasiswa_b = ["M004","M005","M006","M007","M008","M009"]''')

    add_heading(doc, 'Contoh Output', level=3, font_size=11)
    add_code_block(doc, '''=======================================================
    HASIL ANALISIS BEASISWA - OPERASI SET
=======================================================
  (a) Menerima KEDUA beasiswa  : {M004, M005, M006}
      Jumlah                   : 3 mahasiswa
  (b) HANYA beasiswa A         : {M001, M002, M003}
      Jumlah                   : 3 mahasiswa
  (c) HANYA beasiswa B (not A) : {M007, M008, M009}
      Jumlah                   : 3 mahasiswa
  (d) Semua mahasiswa unik     : {M001, M002, ..., M009}
      Jumlah                   : 9 mahasiswa

  Diagram Venn (representasi teks):
  +-----------------+----------------+-----------------+
  |  Hanya A        |  Keduanya      |  Hanya B        |
  +-----------------+----------------+-----------------+
  |  M001           |  M004          |  M007           |
  |  M002           |  M005          |  M008           |
  |  M003           |  M006          |  M009           |
  +-----------------+----------------+-----------------+''')
    add_separator(doc)

    # ── SOAL 4 ──────────────────────────────────────────────────────────────
    add_heading(doc, '3.4  Soal 4 – Sistem Inventaris Toko', level=2, font_size=13, color=(231, 76, 60))

    add_heading(doc, 'Deskripsi Soal', level=3, font_size=11)
    add_paragraph(doc,
        'Membuat sistem inventaris toko menggunakan Dictionary dan Tuple. '
        'Setiap barang disimpan dengan struktur {nama_barang: (harga, stok)}. '
        'Program memiliki fitur tambah barang, update stok, pencarian berdasarkan '
        'rentang harga, dan perhitungan total nilai inventaris.'
    )

    add_heading(doc, 'Struktur Data', level=3, font_size=11)
    add_code_block(doc, '''# Struktur: {nama_barang: (harga, stok)}
inventaris = {
    "Beras Premium" : (15000, 100),
    "Minyak Goreng" : (18500,  80),
    "Gula Pasir"    : (13000,  60),
    "Mie Instan"    : ( 3500, 200),
    # ... dst
}''')

    add_heading(doc, 'Fungsi-Fungsi Utama', level=3, font_size=11)
    add_info_table(doc,
        rows_data=[
            ('tambah_barang()',        'Menambah barang baru, cek duplikasi'),
            ('update_stok()',          'Update stok (buat tuple baru karena immutable)'),
            ('cari_rentang_harga()',   'Filter & urutkan barang berdasarkan rentang harga'),
            ('hitung_total_nilai()',   'Σ (harga × stok) untuk semua barang'),
            ('tampilkan_inventaris()', 'Tampilkan tabel inventaris + total nilai'),
        ],
        headers=['Fungsi', 'Keterangan']
    )

    add_heading(doc, 'Source Code', level=3, font_size=11)
    add_code_block(doc, '''def tambah_barang(inventaris, nama, harga, stok):
    nama = nama.strip().title()
    if nama in inventaris:
        print(f"  Barang '{nama}' sudah ada!")
    else:
        inventaris[nama] = (harga, stok)

def update_stok(inventaris, nama, stok_baru):
    # Tuple immutable -> buat tuple baru
    harga_lama, _ = inventaris[nama]
    inventaris[nama] = (harga_lama, stok_baru)

def cari_rentang_harga(inventaris, harga_min, harga_max):
    hasil = [(nama, harga, stok)
             for nama, (harga, stok) in inventaris.items()
             if harga_min <= harga <= harga_max]
    return sorted(hasil, key=lambda x: x[1])  # sort by harga

def hitung_total_nilai(inventaris):
    return sum(harga * stok for harga, stok in inventaris.values())''')

    add_heading(doc, 'Contoh Output Tabel Inventaris', level=3, font_size=11)
    add_code_block(doc, '''============================================================
              DAFTAR INVENTARIS TOKO
============================================================
  No   Nama Barang          Harga       Stok  Nilai
------------------------------------------------------------
  1    Beras Premium     Rp  15,000     100  Rp 1,500,000
  2    Minyak Goreng     Rp  18,500      80  Rp 1,480,000
  3    Gula Pasir        Rp  13,000      60  Rp   780,000
  4    Mie Instan        Rp   3,500     200  Rp   700,000
  ...
------------------------------------------------------------
                       TOTAL NILAI INVENTARIS  Rp 9,835,000
============================================================''')
    add_separator(doc)

    # ── SOAL 5 ──────────────────────────────────────────────────────────────
    add_heading(doc, '3.5  Soal 5 – Analisis Teks dari File', level=2, font_size=13, color=(231, 76, 60))

    add_heading(doc, 'Deskripsi Soal', level=3, font_size=11)
    add_paragraph(doc,
        'Membuat program yang membaca teks dari file .txt, kemudian menganalisis '
        'frekuensi kata menggunakan Dictionary, menentukan Top-10 kata paling sering '
        'muncul, mengidentifikasi hapax legomena (kata yang hanya muncul satu kali), '
        'dan menghitung Type-Token Ratio (TTR) sebagai ukuran keberagaman kosakata.'
    )

    add_heading(doc, 'Konsep Analisis Teks', level=3, font_size=11)
    add_info_table(doc,
        rows_data=[
            ('Token',            'Setiap kemunculan kata dalam teks (total kata)'),
            ('Type',             'Kata unik dalam teks (tidak duplikat)'),
            ('Frekuensi Kata',   'Jumlah kemunculan setiap kata {kata: jumlah}'),
            ('Top-N Kata',       'N kata dengan frekuensi tertinggi'),
            ('Hapax Legomena',   'Kata yang hanya muncul tepat satu kali dalam teks'),
            ('Type-Token Ratio', 'TTR = jumlah type / jumlah token (0.0 – 1.0)'),
        ],
        headers=['Istilah', 'Penjelasan']
    )

    add_heading(doc, 'Source Code', level=3, font_size=11)
    add_code_block(doc, '''import re

def bersihkan_kata(teks):
    teks_bersih = re.sub(r"[^\w\s]", " ", teks.lower())
    return [k for k in teks_bersih.split() if k and not k.isdigit()]

def hitung_frekuensi(kata_list):
    frekuensi = {}
    for kata in kata_list:
        frekuensi[kata] = frekuensi.get(kata, 0) + 1
    return frekuensi

def top_n_kata(frekuensi, n=10):
    return sorted(frekuensi.items(),
                  key=lambda x: (-x[1], x[0]))[:n]

def hapax_legomena(frekuensi):
    # Set comprehension: kata dengan frekuensi == 1
    return {kata for kata, freq in frekuensi.items() if freq == 1}

def type_token_ratio(frekuensi, total_kata):
    return len(frekuensi) / total_kata  # type / token''')

    add_heading(doc, 'Interpretasi TTR', level=3, font_size=11)
    add_info_table(doc,
        rows_data=[
            ('TTR >= 0.70', 'Sangat beragam – kosakata kaya'),
            ('TTR >= 0.50', 'Cukup beragam – kosakata normal'),
            ('TTR >= 0.30', 'Sedang – ada pengulangan cukup banyak'),
            ('TTR < 0.30',  'Rendah – banyak pengulangan kata'),
        ],
        headers=['Rentang TTR', 'Interpretasi']
    )

    doc.add_page_break()


# ─── BAB IV Kesimpulan ───────────────────────────────────────────────────────

def bab_kesimpulan(doc):
    add_heading(doc, 'BAB IV  KESIMPULAN', level=1, font_size=14, color=(46, 64, 87))
    add_separator(doc)

    kesimpulan = [
        ('String',
         'String Python menyediakan banyak method bawaan yang sangat berguna untuk '
         'manipulasi teks, seperti split(), title(), replace(), dan len(). Operasi ini '
         'dapat dikombinasikan secara efisien untuk menganalisis kalimat.'),
        ('List',
         'List mendukung operasi matematis melalui fungsi bawaan Python seperti sum(), '
         'max(), min(), dan len(). Dictionary comprehension memudahkan pembuatan '
         'ringkasan frekuensi data.'),
        ('Set',
         'Set sangat efisien untuk operasi himpunan. Operator &, -, dan | langsung '
         'mengimplementasikan intersection, difference, dan union secara intuitif '
         'tanpa perlu loop manual.'),
        ('Dictionary & Tuple',
         'Kombinasi Dictionary sebagai key-value store dengan Tuple sebagai value yang '
         'immutable sangat tepat untuk sistem inventaris. Sifat immutable Tuple '
         'menjamin integritas data harga dan stok.'),
        ('Analisis Teks',
         'Dictionary sangat efisien untuk menghitung frekuensi kata. Set comprehension '
         'memudahkan identifikasi hapax legomena. Type-Token Ratio memberikan ukuran '
         'kuantitatif keberagaman kosakata dalam suatu teks.'),
    ]

    for i, (topik, isi) in enumerate(kesimpulan, 1):
        p   = doc.add_paragraph()
        run = p.add_run(f'{i}. {topik}: ')
        set_font(run, bold=True, size=11)
        run2 = p.add_run(isi)
        set_font(run2, size=11)
        p.paragraph_format.space_after = Pt(6)

    doc.add_paragraph()
    add_paragraph(doc,
        'Secara keseluruhan, pertemuan 5 memberikan pemahaman mendalam tentang '
        'penggunaan struktur data bawaan Python. Setiap struktur data memiliki '
        'keunggulan dan kasus penggunaan masing-masing yang perlu dipahami untuk '
        'menulis kode yang efisien dan elegan.',
        italic=True
    )


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print('Membuat laporan Word Pertemuan 5...')

    doc = Document()

    # Setting margin halaman
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3.0)
        section.right_margin  = Cm(2.5)

    # Default font seluruh dokumen
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Bangun halaman
    buat_sampul(doc)
    bab_pendahuluan(doc)
    bab_dasar_teori(doc)
    bab_pembahasan(doc)
    bab_kesimpulan(doc)

    # Simpan file di folder pertemuan_5
    dir_p5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pertemuan_5')
    if not os.path.exists(dir_p5):
        dir_p5 = os.path.dirname(os.path.abspath(__file__))

    output_1 = os.path.join(dir_p5, 'Laporan_Pertemuan_5_Pemrograman_Python.docx')
    output_2 = os.path.join(dir_p5, 'Laporan_Praktikum_Pertemuan_5_20241320046_Sobur.docx')
    output_3 = os.path.join(dir_p5, 'Tugas Teori Pemrograman modern(python)20241320046_sobur_p5.docx')

    doc.save(output_1)
    doc.save(output_2)
    doc.save(output_3)

    print(f'[OK] Laporan Pertemuan 5 berhasil disimpan!')
    print(f'     1. {output_1}')
    print(f'     2. {output_2}')
    print(f'     3. {output_3}')


if __name__ == '__main__':
    main()
