"""
Script Pembuat Dokumen Laporan Praktikum - Pertemuan 7
======================================================
Mata Kuliah : Pemrograman Python
Topik       : Exception Handling, Logging Terstruktur, Unit Testing,
              Refactoring Code Smells, dan Git Pre-Commit Hooks.
Penyusun    : Sobur (NIM: 20241320046)
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# --- HELPER FORMATTING DOCX ---

def set_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_heading(doc, text, level=1, font_size=13, bold=True, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size=font_size, bold=bold, color=color)
    space_after = {1: 8, 2: 5, 3: 3}
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(space_after.get(level, 3))
    return p


def add_paragraph(doc, text, size=11, indent=False, bold=False, italic=False, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic, color=color)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(16)
    if indent:
        p.paragraph_format.left_indent = Cm(0.8)
    return p


def add_code_block(doc, code_text):
    """Menambahkan blok kode dengan font monospace dan background abu-abu terang."""
    lines = code_text.strip().split("\n")
    for line in lines:
        p = doc.add_paragraph()
        run = p.add_run(line if line else " ")
        run.font.name = "Courier New"
        run.font.size = Pt(8.5)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Cm(0.6)

        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "F4F6F7")
        pPr.append(shd)


def add_table_data(doc, rows_data, headers):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        run = hdr_cells[i].paragraphs[0].runs[0]
        set_font(run, bold=True, size=10)
        tc_pr = hdr_cells[i]._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "2E4057")
        tc_pr.append(shd)
        run.font.color.rgb = RGBColor(255, 255, 255)

    for row_data in rows_data:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val)
            run = row_cells[i].paragraphs[0].runs[0]
            set_font(run, size=9.5)

    doc.add_paragraph()


# --- PEMBUATAN STRUKTUR DOKUMEN ---

def buat_sampul(doc):
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("LAPORAN PRAKTIKUM PEMROGRAMAN PYTHON")
    set_font(run, size=16, bold=True, color=(46, 64, 87))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("PERTEMUAN 7")
    set_font(run, size=20, bold=True, color=(231, 76, 60))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Robust Programming: Exception Handling, Logging, Unit Testing, Refactoring & Pre-Commit")
    set_font(run, size=12, italic=True, color=(100, 100, 100))
    p.paragraph_format.space_after = Pt(40)

    table = doc.add_table(rows=6, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    info = [
        ("Nama Mahasiswa", "Sobur"),
        ("NIM", "20241320046"),
        ("Mata Kuliah", "Pemrograman Python / Pemrograman Modern"),
        ("Pertemuan", "7 (Tujuh) - Robust Programming"),
        ("Program Studi", "Teknik Informatika"),
        ("Dosen Pengampu / Instruktur", "Tim Dosen Pemrograman Python"),
    ]

    for i, (label, val) in enumerate(info):
        row = table.rows[i]
        row.cells[0].text = label
        row.cells[1].text = val
        lrun = row.cells[0].paragraphs[0].runs[0]
        vrun = row.cells[1].paragraphs[0].runs[0]
        set_font(lrun, bold=True, size=11)
        set_font(vrun, size=11)

    doc.add_page_break()


def buat_isi_laporan(doc):
    # BAB I
    add_heading(doc, "BAB I  PENDAHULUAN & TUJUAN PRAKTIKUM", level=1, font_size=14, color=(46, 64, 87))
    add_paragraph(doc,
        "Dalam pengembangan perangkat lunak skala produksi, menulis kode yang sekadar 'bisa jalan' "
        "tidaklah cukup. Aplikasi modern menuntut keandalan tinggi (robustness), transparansi saat terjadi insiden "
        "(observability), ketahanan terhadap regresi (maintainability), dan konsistensi gaya kode tim. "
        "Praktikum Pertemuan 7 ini berfokus pada 5 pilar utama rekayasa perangkat lunak dengan Python: "
        "(1) Exception Handling komprehensif, (2) Hierarki Custom Exception berbasis OOP, "
        "(3) Logging bertingkat dengan file rotasi, (4) Unit Testing menggunakan unittest, "
        "(5) Identifikasi dan refactoring Code Smells sesuai PEP 8, serta (6) Otomasi git hooks menggunakan pre-commit."
    )

    # BAB II PEMBAHASAN
    add_heading(doc, "BAB II  PEMBAHASAN SOAL PRAKTIK", level=1, font_size=14, color=(46, 64, 87))

    # SOAL 1
    add_heading(doc, "2.1 Soal 1: Pembacaan Data Mahasiswa CSV dengan Exception Handling Lengkap", level=2, font_size=12, color=(46, 64, 87))
    add_paragraph(doc,
        "Soal 1 menginstruksikan pembuatan program Python untuk membaca data mahasiswa dari file CSV "
        "dengan menangani tiga jenis exception krusial: FileNotFoundError (file tidak ditemukan), "
        "csv.Error (format CSV korup/rusak), dan ValueError (nilai numerik gagal dikonversi). "
        "Program menggunakan blok finally untuk menjamin penutupan file stream dalam segala situasi "
        "dan blok else untuk menampilkan ringkasan data statistik hanya jika pembacaan sukses tanpa kegagalan."
    )
    with open(os.path.join(os.path.dirname(__file__), "soal1_baca_mahasiswa_csv.py"), "r", encoding="utf-8") as f:
        add_code_block(doc, f.read()[:2800] + "\n# ... (lanjutan fungsi simulasi & runner)")

    # SOAL 2
    add_heading(doc, "2.2 Soal 2: Hierarki Custom Exception Sistem Informasi Perpustakaan", level=2, font_size=12, color=(46, 64, 87))
    add_paragraph(doc,
        "Soal 2 menuntut perancangan hierarki custom exception berbasis Object-Oriented Programming (OOP) "
        "untuk modul peminjaman buku perpustakaan. Dibuat kelas dasar PerpustakaanError(Exception), "
        "kemudian diturunkan menjadi BukuNotFoundError, BukuTidakTersediaError, AnggotaNotFoundError, "
        "dan BatasPeminjamanError. Fungsi pinjam_buku() memvalidasi kondisi bisnis dan melempar exception "
        "yang spesifik, sementara program utama mendemonstrasikan penanganan setiap exception secara terisolasi."
    )
    with open(os.path.join(os.path.dirname(__file__), "soal2_perpustakaan_exception.py"), "r", encoding="utf-8") as f:
        add_code_block(doc, f.read()[:2800] + "\n# ... (lanjutan skenario pengujian)")

    # SOAL 3
    add_heading(doc, "2.3 Soal 3: Konfigurasi Logging Terstruktur Aplikasi SI", level=2, font_size=12, color=(46, 64, 87))
    add_paragraph(doc,
        "Soal 3 mengkonfigurasikan logging modular Python untuk sistem informasi: "
        "(a) RotatingFileHandler yang mencatat log level DEBUG ke atas dengan rotasi file otomatis (maxBytes & backupCount), "
        "(b) Console StreamHandler yang memfilter log level WARNING ke atas agar konsol tetap bersih, "
        "(c) Formatter terstandarisasi yang mencakup timestamp (asctime), level, nama logger, dan pesan. "
        "Pengujian memverifikasi bahwa level DEBUG dan INFO tersimpan di file log namun disaring dari konsol."
    )
    with open(os.path.join(os.path.dirname(__file__), "soal3_logging_si.py"), "r", encoding="utf-8") as f:
        add_code_block(doc, f.read()[:2800] + "\n# ... (lanjutan fungsi verifikasi file log)")

    # SOAL 4
    add_heading(doc, "2.4 Soal 4: Pengujian Unit (Unit Test) Lengkap dengan unittest", level=2, font_size=12, color=(46, 64, 87))
    add_paragraph(doc,
        "Soal 4 membangun suite pengujian unit otomatis menggunakan framework bawaan Python (unittest) untuk 3 fungsi akademik: "
        "hitung_ipk(), validasi_nim(), dan konversi_nilai_huruf(). Masing-masing fungsi diuji secara ketat "
        "meliputi Happy Path (kasus normal), Edge Cases (kasus batas/ekstrem), dan Invalid Input (input tidak valid). "
        "Total 26 unit test berhasil dijalankan dengan status 100% lulus (OK)."
    )
    with open(os.path.join(os.path.dirname(__file__), "soal4_unit_test.py"), "r", encoding="utf-8") as f:
        add_code_block(doc, f.read()[:2800] + "\n# ... (lanjutan test suite TestValidasiNIM & TestKonversiNilaiHuruf)")

    # SOAL 5
    add_heading(doc, "2.5 Soal 5: Identifikasi Code Smell dan Refactoring Sesuai PEP 8", level=2, font_size=12, color=(46, 64, 87))
    add_paragraph(doc,
        "Soal 5 menyajikan analisis mendalam terhadap lima code smell utama pada kode legacy: "
        "Magic Number, Duplikasi Logika, Long Method, Deep Nesting, dan Dead Code. "
        "Setelah identifikasi dan penjelasan dampak teknisnya, dilakukan refactoring menyeluruh "
        "menerapkan Single Responsibility Principle (SRP), Guard Clauses, konstanta deskriptif, "
        "serta type hints dan docstring lengkap sesuai konvensi PEP 8."
    )
    headers_smell = ["No", "Code Smell", "Dampak / Masalah", "Solusi Refactoring"]
    rows_smell = [
        ["1", "Magic Number", "Angka tanpa nama (144, 3.5, 3000000) membingungkan dan rawan salah saat aturan diubah.", "Definisikan konstanta modul UPPERCASE."],
        ["2", "Duplikasi Logika", "Perhitungan beasiswa dan subsidi ditulis berulang, melanggar DRY.", "Ekstraksi logika ke fungsi terpisah."],
        ["3", "Long Method", "Satu fungsi memikul terlalu banyak tanggung jawab (>60 baris).", "Pecah jadi subfungsi mandiri sesuai prinsip SRP."],
        ["4", "Deep Nesting", "Sarang if bersarang 5 tingkat membuat arrow anti-pattern.", "Terapkan Guard Clauses (Early Return)."],
        ["5", "Dead Code", "Variabel tak terpakai & blok 'if False' membuang memori & membingungkan.", "Hapus tuntas kode yang tidak terjangkau."]
    ]
    add_table_data(doc, rows_smell, headers_smell)

    # SOAL 6
    add_heading(doc, "2.6 Soal 6: Konfigurasi dan Demonstrasi Pre-Commit Hooks", level=2, font_size=12, color=(46, 64, 87))
    add_paragraph(doc,
        "Soal 6 mendemonstrasikan otomasi integrasi kualitas kode menggunakan pre-commit. "
        "Dikonfigurasikan file .pre-commit-config.yaml yang mengintegrasikan isort (pengurutan import), "
        "black (format kode deterministik), dan flake8 (linter statis PEP 8). "
        "Simulasi membuktikan bahwa ketika kode melanggar standar (seperti adanya unused variable atau baris melebihi 88 karakter), "
        "pre-commit hook mengembalikan status exit code 1 dan secara otomatis membatalkan git commit (commit rejection)."
    )
    with open(os.path.join(os.path.dirname(__file__), ".pre-commit-config.yaml"), "r", encoding="utf-8") as f:
        add_code_block(doc, f.read())

    # BAB III KESIMPULAN
    add_heading(doc, "BAB III  KESIMPULAN", level=1, font_size=14, color=(46, 64, 87))
    add_paragraph(doc,
        "Praktikum Pertemuan 7 membuktikan bahwa penerapan teknik penanganan exception yang terstruktur, "
        "pencatatan log bertingkat dengan rotasi file, pengujian unit yang komprehensif, pembersihan code smell, "
        "dan otomatisasi pre-commit hooks secara signifikan meningkatkan stabilitas, keamanan, dan maintainability "
        "dari perangkat lunak Python kelas industri."
    )


def main():
    direktori = os.path.dirname(os.path.abspath(__file__))
    output_docx = os.path.join(direktori, "Laporan_Praktikum_Pertemuan_7_20241320046_Sobur.docx")

    print(f"Membuat dokumen laporan Word di: {output_docx} ...")
    doc = Document()

    # Setup Margin
    for s in doc.sections:
        s.top_margin = Cm(2.5)
        s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(3.0)
        s.right_margin = Cm(2.5)

    buat_sampul(doc)
    buat_isi_laporan(doc)

    doc.save(output_docx)
    print(f"[SUKSES] File laporan berhasil disimpan: {output_docx}")

    # Buat juga salinan dengan nama Tugas Teori/Praktik
    alt_output = os.path.join(direktori, "Tugas Teori Pemrograman modern(python)20241320046_sobur_p7.docx")
    doc.save(alt_output)
    print(f"[SUKSES] Salinan tugas berhasil disimpan: {alt_output}")


if __name__ == "__main__":
    main()

