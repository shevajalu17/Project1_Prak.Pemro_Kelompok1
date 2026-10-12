# Sistem Peminjaman Alat LAB

Aplikasi berbasis terminal (CLI) untuk mengelola peminjaman peralatan laboratorium. Aplikasi dibuat dengan Python menggunakan pendekatan *Object-Oriented Programming* (OOP) dan struktur data bawaan (`dict` dan `list`), tanpa database dan tanpa pustaka eksternal.

---

## 1. Anggota Kelompok

| No | Nama                    | NIM      |
|----|-------------------------|----------|
| 1  | Fathma Daniswara T.P    | K3525060 |
| 2  | Muhammad Ammar Fathin   | K3525065 |
| 3  | Sheva Jalu Atmaja       | K3525073 |
| 4  | Bhakti Rega Riana       | K3525088 |

---

## 2. Deskripsi Sistem

**Sistem Peminjaman Alat LAB** membantu pengelola laboratorium mencatat data mahasiswa, data peralatan, serta proses peminjaman dan pengembalian alat. Seluruh interaksi dilakukan melalui menu bernomor di terminal, dengan tampilan tabel berbingkai, warna status, dan pesan berikon (`✔` berhasil, `✘` gagal, `!` peringatan).

### Kemampuan Sistem

**Kelola Mahasiswa**
- Menambah, mengubah, menghapus, mencari (berdasarkan NIM atau nama), dan menampilkan seluruh mahasiswa.
- NIM bersifat unik dan semua kolom wajib diisi.
- Mahasiswa yang masih memiliki transaksi aktif tidak dapat dihapus.

**Kelola Peralatan dan Kategori**
- Menambah, mengubah, menghapus, mencari (berdasarkan kode, nama, atau kategori), dan menampilkan seluruh alat.
- Menambah dan menampilkan kategori alat beserta jumlah alat pada tiap kategori. Kategori awal: `K01` Perangkat Komputasi, `K02` Perangkat Jaringan, `K03` Perangkat Multimedia.
- Alat yang sedang dipinjam tidak dapat diubah, dan alat yang sedang dipinjam atau tercatat pada transaksi aktif tidak dapat dihapus.

**Transaksi Peminjaman**
- Satu transaksi dapat memuat beberapa alat sekaligus (kode alat dipisahkan koma).
- Lama peminjaman 1–7 hari, batas kembali dihitung otomatis dari tanggal hari ini.
- Setiap mahasiswa maksimal memiliki 2 transaksi aktif.
- Seluruh alat divalidasi terlebih dahulu sebelum transaksi disimpan, sehingga tidak ada perubahan setengah jalan jika terjadi kesalahan.
- ID transaksi dibuat otomatis (`TRX001`, `TRX002`, dst.).

**Pengembalian Alat**
- Alat dikembalikan satu per satu dengan mencatat kondisi: `BAIK`, `RUSAK_RINGAN`, atau `RUSAK_BERAT`.
- Status transaksi berubah otomatis: `DIPINJAM` → `SEBAGIAN_DIKEMBALIKAN` → `SELESAI`.
- Transaksi yang melewati batas kembali ditandai `TERLAMBAT` beserta jumlah hari keterlambatan.

**Pemeliharaan Alat**
- Alat yang dikembalikan dalam kondisi rusak otomatis masuk status pemeliharaan dan tidak tersedia untuk dipinjam.
- Setelah diperbaiki, alat dikembalikan ke status tersedia melalui menu pemeliharaan.

**Pelaporan**
- Daftar alat tersedia, alat sedang dipinjam, dan alat rusak/pemeliharaan.
- Pencarian transaksi dan riwayat peminjaman per mahasiswa.
- Statistik: total transaksi aktif/selesai, jumlah mahasiswa dan alat terdaftar, 5 alat paling sering dipinjam, dan 5 mahasiswa paling sering meminjam (dilengkapi grafik batang).

### Aturan Bisnis

| Aturan | Keterangan |
|--------|------------|
| Batas transaksi aktif | Maksimal 2 transaksi aktif per mahasiswa |
| Durasi pinjam | 1–7 hari |
| Alat tersedia | Kondisi `BAIK`, tidak sedang dipinjam, dan tidak dalam pemeliharaan |
| Kode alat dalam satu transaksi | Tidak boleh duplikat |
| Penyimpanan data | Hanya di memori; data hilang saat program ditutup |

---

## 3. Struktur Program

```text
sistem_peminjaman_lab_terstruktur/
├── main.py                      # titik masuk aplikasi
├── README.md                    # dokumentasi
└── app/
    ├── __init__.py              # penanda paket
    ├── entities.py              # model data dan enum
    ├── mahasiswa_manager.py     # CRUD dan pencarian mahasiswa
    ├── peralatan_manager.py     # CRUD alat/kategori, stok, pemeliharaan
    ├── transaksi_manager.py     # peminjaman, pengembalian, riwayat, statistik
    ├── tampilan.py              # pembantu tampilan terminal
    └── menu_app.py              # MenuApp: antarmuka dan alur menu
```

### Penjelasan Tiap File

| File | Isi dan Tanggung Jawab |
|------|------------------------|
| `main.py` | Menjalankan `MenuApp`, mengatur encoding UTF-8 pada terminal, dan menangani `Ctrl+C`/`EOF` agar program berhenti dengan rapi. |
| `entities.py` | Class model: `Kategori`, `Mahasiswa`, `Peralatan`, `ItemPinjam`, `Transaksi`, serta enum `StatusTransaksi` dan `KondisiAlat`. Berisi logika dasar tiap entitas (misalnya `bisaMeminjam()`, `isTersedia()`, `perbaruiStatus()`). |
| `mahasiswa_manager.py` | `MahasiswaManager`: tambah, edit, hapus, cari, dan tampilkan mahasiswa. Data disimpan dalam `dict` dengan NIM sebagai kunci. |
| `peralatan_manager.py` | `PeralatanManager`: kelola alat dan kategori, daftar alat (tersedia/dipinjam/rusak), serta `selesaikanPemeliharaan()`. |
| `transaksi_manager.py` | `TransaksiManager`: `buatTransaksi()` dengan validasi aturan bisnis, `prosesPengembalian()`, pencarian/riwayat transaksi, dan `statistik()`. |
| `tampilan.py` | Fungsi pembantu tampilan: warna ANSI, banner, kotak menu, tabel berbingkai, grafik batang, dan input. Warna otomatis nonaktif bila output bukan terminal atau variabel `NO_COLOR` diset. |
| `menu_app.py` | `MenuApp`: menghubungkan semua manager, menyiapkan data awal (kategori), dan menampilkan menu serta interaksi pengguna. |

### Hubungan Antar Class

```text
MenuApp
 ├── MahasiswaManager ──► Mahasiswa
 ├── PeralatanManager ──► Peralatan ──► Kategori
 └── TransaksiManager ──► Transaksi ──► ItemPinjam ──► Peralatan
                              └──────► Mahasiswa
```

### Menu Utama

| No | Menu |
|----|------|
| 1  | Kelola mahasiswa |
| 2  | Kelola peralatan |
| 3  | Buat transaksi peminjaman |
| 4  | Tampilkan transaksi |
| 5  | Proses pengembalian alat |
| 6  | Cari transaksi berdasarkan mahasiswa |
| 7  | Tampilkan alat tersedia |
| 8  | Tampilkan alat sedang dipinjam |
| 9  | Tampilkan alat rusak/pemeliharaan |
| 10 | Riwayat peminjaman mahasiswa |
| 11 | Statistik peminjaman |
| 12 | Selesaikan pemeliharaan alat |
| 0  | Keluar |

---

## 4. Cara Menjalankan Aplikasi

### Prasyarat
- **Python 3.10 atau lebih baru** (memakai sintaks seperti `list[str]` dan `Mahasiswa | None`).
- Tidak memerlukan instalasi pustaka tambahan.
- Terminal yang mendukung UTF-8 agar simbol kotak dan ikon tampil dengan benar.

### Langkah-langkah
1. Ekstrak file ZIP `sistem_peminjaman_lab_terstruktur`.
2. Buka terminal/Command Prompt pada folder yang berisi `main.py`:
   ```bash
   cd sistem_peminjaman_lab_terstruktur
   ```
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```
   (atau `python3 main.py` pada Linux/macOS)
4. Pilih menu dengan mengetik nomor, lalu tekan **Enter**. Ketik `0` untuk keluar, atau tekan `Ctrl+C` kapan saja.

### Contoh Alur Penggunaan
1. Menu **1** → tambah mahasiswa (NIM, nama, no. HP).
2. Menu **2** → tambah alat (kode, nama, ID kategori).
3. Menu **3** → buat transaksi: masukkan NIM, kode alat (contoh `A01,A02`), dan lama pinjam (1–7).
4. Menu **5** → proses pengembalian: pilih ID transaksi, kode alat, dan kondisi alat.
5. Menu **12** → selesaikan pemeliharaan jika ada alat yang dikembalikan dalam kondisi rusak.
6. Menu **11** → lihat statistik peminjaman.

> **Catatan:** Data hanya tersimpan di memori. Semua data akan hilang saat program ditutup.

---

## 5. Pembagian Kontribusi Anggota

| Nama | NIM | Kontribusi |
|------|-----|------------|
| Fathma Daniswara T.P | K3525060 | `peralatan_manager.py` |
| Muhammad Ammar Fathin | K3525065 | `menu_app.py`, `tampilan.py`, `main.py` |
| Sheva Jalu Atmaja | K3525073 | `entities.py`, `mahasiswa_manager.py`, `README.md` |
| Bhakti Rega Riana | K3525088 | `transaksi_manager.py` |
