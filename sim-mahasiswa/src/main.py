# src/main.py
import sys
import os

# Tambahkan path agar bisa import dari src/
sys.path.insert(0, os.path.dirname(__file__))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from models import Mahasiswa, DaftarMahasiswa

console = Console()
db = DaftarMahasiswa()

def tampilkan_menu():
    """Tampilkan menu utama."""
    menu_text = (
        "[bold cyan]Sistem Informasi Mahasiswa[/]\n\n"
        "[bold]1.[/] Tambah Mahasiswa\n"
        "[bold]2.[/] Tampilkan Semua Mahasiswa\n"
        "[bold]3.[/] Cari Mahasiswa (NIM)\n"
        "[bold]4.[/] Hapus Mahasiswa\n"
        "[bold]0.[/] Keluar"
    )
    console.print(Panel(menu_text, title="[bold cyan]Menu Utama[/]", border_style="cyan"))

def tambah_mahasiswa():
    """Form tambah mahasiswa baru."""
    console.print("\n[bold yellow]--- Tambah Mahasiswa Baru ---[/]")
    nim     = console.input("  NIM          : ")
    nama    = console.input("  Nama         : ")
    prodi   = console.input("  Program Studi: ")
    try:
        angkatan = int(console.input("  Angkatan     : "))
        ipk      = float(console.input("  IPK          : "))
        mhs = Mahasiswa(nim, nama, prodi, angkatan, ipk)
        db.tambah(mhs)
        console.print(f"\n[green]✓ Berhasil: {nama} ({nim}) ditambahkan![/]\n")
    except ValueError as e:
        console.print(f"\n[red]✗ Gagal: {e}[/]\n")

def tampilkan_semua():
    """Tampilkan seluruh data dalam tabel."""
    if not db.data:
        console.print("\n[yellow]⚠ Belum ada data mahasiswa.[/]\n")
        return

    table = Table(title=f"[bold]Daftar Mahasiswa ({db.jumlah} data)[/]",
                  border_style="cyan", show_lines=True)
    table.add_column("No",  style="dim", justify="center", width=4)
    table.add_column("NIM", style="cyan", width=12)
    table.add_column("Nama", width=25)
    table.add_column("Program Studi", width=20)
    table.add_column("Angkatan", justify="center", width=10)
    table.add_column("IPK", justify="center", style="green", width=6)

    for i, m in enumerate(db.data, 1):
        table.add_row(str(i), m.nim, m.nama, m.program_studi,
                      str(m.angkatan), f"{m.ipk:.2f}")

    console.print()
    console.print(table)
    console.print()

def cari_mahasiswa():
    """Cari mahasiswa berdasarkan NIM."""
    console.print("\n[bold yellow]--- Cari Mahasiswa ---[/]")
    nim = console.input("  Masukkan NIM: ")
    mhs = db.cari(nim)
    if mhs:
        console.print(f"\n[green]✓ Mahasiswa ditemukan:[/]")
        console.print(Panel(
            f"[cyan]NIM[/]          : {mhs.nim}\n"
            f"[cyan]Nama[/]         : {mhs.nama}\n"
            f"[cyan]Program Studi[/]: {mhs.program_studi}\n"
            f"[cyan]Angkatan[/]     : {mhs.angkatan}\n"
            f"[cyan]IPK[/]          : {mhs.ipk:.2f}",
            title="Detail Mahasiswa", border_style="green"
        ))
    else:
        console.print(f"\n[red]✗ Mahasiswa dengan NIM '{nim}' tidak ditemukan.[/]")
    console.print()

def hapus_mahasiswa():
    """Hapus data mahasiswa berdasarkan NIM."""
    console.print("\n[bold yellow]--- Hapus Mahasiswa ---[/]")
    nim = console.input("  Masukkan NIM: ")
    mhs = db.cari(nim)
    if not mhs:
        console.print(f"\n[red]✗ NIM '{nim}' tidak ditemukan.[/]\n")
        return
    konfirmasi = console.input(f"  Hapus [bold]{mhs.nama}[/]? (y/n): ")
    if konfirmasi.lower() == 'y':
        db.hapus(nim)
        console.print(f"\n[green]✓ Data {mhs.nama} berhasil dihapus.[/]\n")
    else:
        console.print("\n[yellow]Penghapusan dibatalkan.[/]\n")

def main():
    """Loop utama aplikasi."""
    console.print(Panel.fit(
        "[bold cyan]Selamat Datang di SIM Mahasiswa[/]\n"
        "[dim]Sistem Informasi Mahasiswa - Praktikum Python[/]",
        border_style="cyan"
    ))

    while True:
        tampilkan_menu()
        pilihan = console.input("[bold]Pilih [[cyan]0-4[/]]: [/]")

        if pilihan == "1":
            tambah_mahasiswa()
        elif pilihan == "2":
            tampilkan_semua()
        elif pilihan == "3":
            cari_mahasiswa()
        elif pilihan == "4":
            hapus_mahasiswa()
        elif pilihan == "0":
            console.print("\n[bold cyan]Sampai jumpa! 👋[/]\n")
            break
        else:
            console.print("[red]✗ Pilihan tidak valid, masukkan 0-4.[/]\n")

if __name__ == "__main__":
    main()
