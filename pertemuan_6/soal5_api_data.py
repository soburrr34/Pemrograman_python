"""
Soal 5 - REST API + Lambda + Higher-Order Functions
=====================================================
Program yang:
1. Mengambil data dari JSONPlaceholder REST API menggunakan library requests
2. Memproses data menggunakan lambda dan HOF: map(), filter(), sorted()
3. Menganalisis data (posts, users, comments)
4. Menyimpan hasil analisis ke file JSON menggunakan modul json
"""

import json
import os
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] Library 'requests' belum terinstall.")
    print("        Jalankan: pip install requests")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL      = "https://jsonplaceholder.typicode.com"
OUTPUT_FILE   = "soal5_hasil_analisis.json"
TIMEOUT       = 10  # detik


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI PENGAMBILAN DATA (requests)
# ─────────────────────────────────────────────────────────────────────────────

def ambil_data(endpoint: str) -> list:
    """
    Mengambil data dari JSONPlaceholder API.

    Args:
        endpoint (str): Endpoint API (misal: '/posts', '/users', '/comments')

    Returns:
        list: Data dari API dalam bentuk list of dict

    Raises:
        requests.RequestException: Jika terjadi error jaringan
    """
    url = f"{BASE_URL}{endpoint}"
    print(f"  Mengambil data dari: {url}")

    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()  # raise exception jika status code >= 400

    data = response.json()
    print(f"  Berhasil! Total data: {len(data)} item")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# PEMROSESAN DATA DENGAN LAMBDA & HIGHER-ORDER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def proses_posts(posts: list) -> dict:
    """
    Memproses data posts menggunakan map(), filter(), dan sorted().

    Args:
        posts (list): Data posts dari API

    Returns:
        dict: Hasil analisis posts
    """
    print("\n  [1] Memproses data Posts...")

    # ── map() : Ekstrak field penting & tambahkan metadata ───────────────────
    # Lambda untuk menghitung panjang judul dan body
    hitung_panjang = lambda post: {
        **post,
        'panjang_judul' : len(post['title']),
        'panjang_body'  : len(post['body']),
        'ringkasan'     : post['title'][:50] + '...' if len(post['title']) > 50 else post['title'],
    }
    posts_diperkaya = list(map(hitung_panjang, posts))

    # ── filter() : Saring posts dengan judul panjang (> 40 karakter) ────────
    judul_panjang = list(filter(
        lambda p: p['panjang_judul'] > 40,
        posts_diperkaya
    ))

    # ── filter() : Saring posts dari user tertentu (userId 1-3) ─────────────
    posts_user_top = list(filter(
        lambda p: p['userId'] in [1, 2, 3],
        posts_diperkaya
    ))

    # ── sorted() : Urutkan berdasarkan panjang judul (descending) ────────────
    posts_terpanjang = sorted(
        posts_diperkaya,
        key=lambda p: p['panjang_judul'],
        reverse=True
    )[:5]

    # ── sorted() : Urutkan berdasarkan userId ────────────────────────────────
    posts_per_user = sorted(posts_diperkaya, key=lambda p: p['userId'])

    # ── map() : Hitung jumlah post per userId ───────────────────────────────
    user_ids = list(set(map(lambda p: p['userId'], posts)))
    jumlah_post_per_user = list(map(
        lambda uid: {
            'userId'      : uid,
            'jumlah_post' : sum(1 for p in posts if p['userId'] == uid),
        },
        sorted(user_ids)
    ))

    # Rata-rata panjang judul
    rata_panjang_judul = round(
        sum(map(lambda p: p['panjang_judul'], posts_diperkaya)) / len(posts_diperkaya), 2
    )

    return {
        'total_posts'           : len(posts),
        'rata_panjang_judul'    : rata_panjang_judul,
        'judul_panjang_count'   : len(judul_panjang),  # judul > 40 karakter
        'posts_user_1_2_3_count': len(posts_user_top),
        'top5_judul_terpanjang' : [
            {'id': p['id'], 'userId': p['userId'], 'judul': p['title'], 'panjang': p['panjang_judul']}
            for p in posts_terpanjang
        ],
        'jumlah_post_per_user'  : jumlah_post_per_user,
        'contoh_judul_panjang'  : [
            {'id': p['id'], 'judul': p['title']}
            for p in judul_panjang[:3]
        ],
    }


def proses_users(users: list) -> dict:
    """
    Memproses data users menggunakan map(), filter(), dan sorted().

    Args:
        users (list): Data users dari API

    Returns:
        dict: Hasil analisis users
    """
    print("\n  [2] Memproses data Users...")

    # ── map() : Ekstrak informasi kontak ────────────────────────────────────
    ekstrak_kontak = lambda u: {
        'id'      : u['id'],
        'nama'    : u['name'],
        'username': u['username'],
        'email'   : u['email'],
        'kota'    : u['address']['city'],
        'domain_email': u['email'].split('@')[1] if '@' in u['email'] else 'unknown',
    }
    daftar_kontak = list(map(ekstrak_kontak, users))

    # ── sorted() : Urutkan berdasarkan nama ──────────────────────────────────
    users_sorted_nama = sorted(daftar_kontak, key=lambda u: u['nama'])

    # ── filter() : Filter user dengan email domain tertentu ─────────────────
    domain_unik = list(set(map(lambda u: u['domain_email'], daftar_kontak)))
    users_email_biz = list(filter(
        lambda u: u['domain_email'].endswith('.biz'),
        daftar_kontak
    ))

    # ── sorted() : Urutkan berdasarkan kota ──────────────────────────────────
    users_sorted_kota = sorted(daftar_kontak, key=lambda u: u['kota'])

    # ── map() : Hitung panjang username ─────────────────────────────────────
    stats_username = list(map(
        lambda u: {'username': u['username'], 'panjang': len(u['username'])},
        daftar_kontak
    ))
    username_terpanjang = sorted(stats_username, key=lambda x: x['panjang'], reverse=True)[0]

    return {
        'total_users'            : len(users),
        'domain_unik'            : sorted(domain_unik),
        'users_email_biz_count'  : len(users_email_biz),
        'users_email_biz'        : [u['email'] for u in users_email_biz],
        'username_terpanjang'    : username_terpanjang,
        'daftar_user_sorted_nama': users_sorted_nama,
        'kota_unik'              : sorted(list(set(map(lambda u: u['kota'], daftar_kontak)))),
    }


def proses_comments(comments: list, posts: list) -> dict:
    """
    Memproses data comments menggunakan map(), filter(), dan sorted().

    Args:
        comments (list): Data comments dari API
        posts    (list): Data posts (untuk join data)

    Returns:
        dict: Hasil analisis comments
    """
    print("\n  [3] Memproses data Comments...")

    # ── map() : Hitung panjang body komentar ────────────────────────────────
    tambah_panjang = lambda c: {**c, 'panjang_body': len(c['body'])}
    comments_diperkaya = list(map(tambah_panjang, comments))

    # ── filter() : Saring komentar dengan email dari domain '.net' ──────────
    komentar_net = list(filter(
        lambda c: c['email'].endswith('.net'),
        comments_diperkaya
    ))

    # ── filter() : Saring komentar panjang (>120 karakter) ──────────────────
    komentar_panjang = list(filter(
        lambda c: c['panjang_body'] > 120,
        comments_diperkaya
    ))

    # ── sorted() : 5 komentar terpanjang ────────────────────────────────────
    top5_terpanjang = sorted(
        comments_diperkaya,
        key=lambda c: c['panjang_body'],
        reverse=True
    )[:5]

    # ── map() + sorted() : Hitung jumlah komentar per post ──────────────────
    post_ids = sorted(list(set(map(lambda c: c['postId'], comments))))
    komentar_per_post = list(map(
        lambda pid: {
            'postId'         : pid,
            'jumlah_komentar': sum(1 for c in comments if c['postId'] == pid),
        },
        post_ids
    ))
    # Top 5 post paling banyak dikomentar
    top5_post_ramai = sorted(
        komentar_per_post,
        key=lambda x: x['jumlah_komentar'],
        reverse=True
    )[:5]

    # Rata-rata panjang komentar
    rata_panjang = round(
        sum(map(lambda c: c['panjang_body'], comments_diperkaya)) / len(comments_diperkaya), 2
    )

    return {
        'total_comments'        : len(comments),
        'rata_panjang_body'     : rata_panjang,
        'komentar_panjang_count': len(komentar_panjang),
        'komentar_net_count'    : len(komentar_net),
        'top5_komentar_terpanjang': [
            {'id': c['id'], 'postId': c['postId'], 'email': c['email'], 'panjang': c['panjang_body']}
            for c in top5_terpanjang
        ],
        'top5_post_terbanyak_komentar': top5_post_ramai,
    }


def simpan_ke_json(data: dict, nama_file: str) -> str:
    """
    Menyimpan data ke file JSON.

    Args:
        data      (dict): Data yang akan disimpan
        nama_file (str) : Nama file output

    Returns:
        str: Path file yang tersimpan
    """
    path = os.path.join(os.path.dirname(__file__), nama_file)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    ukuran = os.path.getsize(path)
    print(f"\n  File tersimpan: {path}")
    print(f"  Ukuran file   : {ukuran:,} bytes ({ukuran / 1024:.1f} KB)")
    return path


def tampilkan_ringkasan(hasil: dict) -> None:
    """Menampilkan ringkasan hasil analisis di terminal."""
    lebar = 60
    print(f"\n{'=' * lebar}")
    print("  RINGKASAN HASIL ANALISIS".center(lebar))
    print(f"{'=' * lebar}")

    print(f"\n  POSTS:")
    print(f"    Total posts             : {hasil['posts']['total_posts']}")
    print(f"    Rata-rata panjang judul : {hasil['posts']['rata_panjang_judul']} karakter")
    print(f"    Post judul > 40 karakter: {hasil['posts']['judul_panjang_count']}")

    print(f"\n  USERS:")
    print(f"    Total users             : {hasil['users']['total_users']}")
    print(f"    Domain email unik       : {', '.join(hasil['users']['domain_unik'])}")
    print(f"    User email .biz         : {hasil['users']['users_email_biz_count']}")
    print(f"    Username terpanjang     : {hasil['users']['username_terpanjang']['username']}")

    print(f"\n  COMMENTS:")
    print(f"    Total comments          : {hasil['comments']['total_comments']}")
    print(f"    Rata-rata panjang body  : {hasil['comments']['rata_panjang_body']} karakter")
    print(f"    Komentar panjang (>120) : {hasil['comments']['komentar_panjang_count']}")
    print(f"    Komentar email .net     : {hasil['comments']['komentar_net_count']}")

    print(f"\n  TOP 5 POST PALING BANYAK DIKOMENTAR:")
    for item in hasil['comments']['top5_post_terbanyak_komentar']:
        print(f"    Post #{item['postId']:<4}: {item['jumlah_komentar']} komentar")

    print(f"\n{'=' * lebar}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 60)
    print("  SOAL 5 - REST API + Lambda + Higher-Order Functions")
    print("  Data Source: JSONPlaceholder (https://jsonplaceholder.typicode.com)")
    print("=" * 60)

    # 1. Ambil data dari API
    print("\n[STEP 1] Mengambil data dari REST API...")
    try:
        posts    = ambil_data('/posts')
        users    = ambil_data('/users')
        comments = ambil_data('/comments')
    except requests.ConnectionError:
        print("\n[ERROR] Tidak dapat terhubung ke internet!")
        print("        Pastikan koneksi internet tersedia.")
        return
    except requests.Timeout:
        print(f"\n[ERROR] Koneksi timeout setelah {TIMEOUT} detik.")
        return
    except requests.HTTPError as e:
        print(f"\n[ERROR] HTTP Error: {e}")
        return

    # 2. Proses data dengan lambda dan HOF
    print("\n[STEP 2] Memproses data dengan lambda dan HOF...")
    hasil_posts    = proses_posts(posts)
    hasil_users    = proses_users(users)
    hasil_comments = proses_comments(comments, posts)

    # 3. Gabungkan semua hasil
    hasil_akhir = {
        'metadata': {
            'sumber'         : BASE_URL,
            'waktu_analisis' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'teknik_digunakan': ['map()', 'filter()', 'sorted()', 'lambda', 'requests', 'json'],
        },
        'posts'   : hasil_posts,
        'users'   : hasil_users,
        'comments': hasil_comments,
    }

    # 4. Tampilkan ringkasan
    print("\n[STEP 3] Ringkasan hasil analisis:")
    tampilkan_ringkasan(hasil_akhir)

    # 5. Simpan ke file JSON
    print("\n[STEP 4] Menyimpan hasil ke file JSON...")
    simpan_ke_json(hasil_akhir, OUTPUT_FILE)

    print("\n[SELESAI] Program berhasil dijalankan!")


if __name__ == '__main__':
    main()
