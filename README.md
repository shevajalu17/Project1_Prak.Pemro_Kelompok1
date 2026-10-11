# Sistem Peminjaman Peralatan Laboratorium

Program terminal untuk mencatat peminjaman alat di laboratorium.

Data hanya disimpan sementara di memori, jadi akan hilang saat program ditutup. Memang tidak memakai database sesuai ketentuan tugas.

## Kemampuan Program

- Mengelola data mahasiswa (tambah, edit, hapus, cari, tampilkan).
- Mengelola data alat beserta kategorinya.
- Membuat transaksi peminjaman, satu transaksi boleh berisi beberapa alat.
- Memproses pengembalian alat satu per satu, lengkap dengan pencatatan kondisinya.
- Menandai transaksi yang terlambat.
- Mengatur alat yang rusak agar tidak bisa dipinjam sampai selesai diperbaiki.
- Menampilkan riwayat peminjaman dan statistik sederhana.

## Struktur folder

```text
sistem_peminjaman_lab_terstruktur/
├── main.py                    # titik masuk program
└── app/
    ├── entities.py            # class model + enum
    ├── mahasiswa_manager.py   # logika data mahasiswa
    ├── peralatan_manager.py   # logika data alat & kategori
    ├── transaksi_manager.py   # logika peminjaman & pengembalian
    ├── tampilan.py            # helper tampilan (tabel, warna, kotak menu)
    └── menu_app.py            # menu & interaksi dengan pengguna
```

Programnya dibagi menjadi tiga lapisan supaya tiap file punya tugas yang jelas:

1. **Model** (`entities.py`): menyimpan data dan aturan yang menempel pada objek itu sendiri.
2. **Manager** (`*_manager.py`): menjalankan operasi dan aturan bisnis di atas kumpulan objek.
3. **Antarmuka** (`menu_app.py` dan `tampilan.py`): menerima input, memanggil manager, lalu menampilkan hasilnya.

Manager sama sekali tidak memakai `print` atau `input`. Semua interaksi dengan pengguna ada di `menu_app.py`, jadi logikanya bisa dipakai ulang atau dites tanpa menyentuh terminal.

## Penjelasan tiap bagian

### `main.py`
Hanya membuat objek `MenuApp` lalu menjalankannya. Di sini juga ada pengaturan encoding UTF-8 supaya karakter kotak dan simbol (`✔`, `✘`, `═`) tampil benar, serta penanganan `Ctrl+C` agar program berhenti dengan rapi.

### `entities.py`
Isinya class-class data:

| Class | Fungsi |
|---|---|
| `Kategori` | Pengelompokan alat (id dan nama). |
| `Mahasiswa` | NIM, nama, no. HP, dan daftar ID transaksi yang sedang aktif. |
| `Peralatan` | Kode, nama, kategori, kondisi, serta penanda sedang dipinjam atau dalam pemeliharaan. |
| `ItemPinjam` | Satu alat di dalam satu transaksi, lengkap dengan tanggal dan kondisi saat dikembalikan. |
| `Transaksi` | Satu kali peminjaman: peminjam, daftar item, tanggal pinjam, batas kembali, dan status. |

Ada juga dua enum:
(Enum adalah tipe data yang nilainya dibatasi pada pilihan tetap yang sudah didaftarkan. Dengan begitu, status atau kondisi tidak bisa terisi teks sembarangan, dan salah ketik langsung ketahuan sebagai error (misalnya KondisiAlat.BAIKK tidak akan dikenali).)

- `StatusTransaksi`: `DIPINJAM`, `SEBAGIAN_DIKEMBALIKAN`, `SELESAI`
- `KondisiAlat`: `BAIK`, `RUSAK_RINGAN`, `RUSAK_BERAT`

Beberapa method penting:

- `Peralatan.isTersedia()` bernilai true hanya jika kondisi `BAIK`, tidak sedang dipinjam, dan tidak dalam pemeliharaan.
- `Mahasiswa.bisaMeminjam()` bernilai true selama transaksi aktifnya kurang dari 2.
- `ItemPinjam.kembalikan()` mencatat tanggal dan kondisi, lalu memanggil `Peralatan.terimaKembali()`. Kalau item sudah pernah dikembalikan, akan muncul `ValueError`.
- `Transaksi.perbaruiStatus()` menghitung ulang status berdasarkan jumlah item yang sudah dan belum kembali. Kalau semuanya sudah kembali, status menjadi `SELESAI` dan transaksi dilepas dari daftar aktif mahasiswa.

### `mahasiswa_manager.py`
Data disimpan dalam `dict` dengan NIM sebagai kunci, jadi pencarian per NIM langsung tanpa perulangan. Menyediakan `tambah`, `edit`, `hapus`, `cari` (berdasarkan NIM atau nama, tidak peduli huruf besar/kecil), `getByNim`, dan `tampilkanSemua`.

Mahasiswa yang masih punya transaksi aktif tidak bisa dihapus.

### `peralatan_manager.py`
Mengurus `dict` alat dan `dict` kategori. Selain CRUD, ada beberapa fungsi penyaring: `daftarTersedia`, `daftarDipinjam`, `daftarRusak`, dan `selesaikanPemeliharaan`.

Ada satu hal yang agak unik di sini: atribut `adaDalamTransaksiAktif` awalnya hanya lambda yang selalu mengembalikan `False`. `MenuApp` menggantinya dengan method milik `TransaksiManager` saat inisialisasi. Cara ini dipakai supaya `PeralatanManager` bisa mengecek transaksi aktif sebelum menghapus alat tanpa harus saling mengimpor dengan `TransaksiManager`.

### `transaksi_manager.py`
Bagian yang paling banyak aturannya. Method utamanya:

- `buatTransaksi(nim, listKodeAlat, lamaHari)` membuat transaksi baru.
- `prosesPengembalian(idTrx, kodeAlat, kondisi)` mencatat pengembalian satu alat.
- `cariByMahasiswa` dan `riwayatMahasiswa` mengambil transaksi milik satu NIM.
- `adaAlatDalamTransaksiAktif` dipakai untuk mengecek apakah alat boleh dihapus.
- `statistik` menghitung jumlah transaksi aktif/selesai serta frekuensi pemakaian alat dan mahasiswa.

ID transaksi dibuat otomatis dengan format `TRX001`, `TRX002`, dan seterusnya.

### `tampilan.py`
Kumpulan fungsi kecil untuk merapikan tampilan: pesan status berwarna, banner, kotak menu, tabel berbingkai, dan grafik batang dari karakter. Hanya memakai library standar.

### `menu_app.py`
Class `MenuApp` membuat ketiga manager, menyambungkannya, lalu menampilkan menu dalam sebuah perulangan sampai pengguna memilih keluar. Pemilihan menu memakai dictionary yang memetakan nomor ke method, jadi tidak ada rantai `if/elif` yang panjang di menu utama. Input yang menimbulkan `ValueError` atau `KeyError` ditangkap di sini supaya program tidak langsung berhenti.

Saat pertama dijalankan, data yang sudah ada hanya tiga kategori bawaan:

- `K01` Perangkat Komputasi
- `K02` Perangkat Jaringan
- `K03` Perangkat Multimedia

Data mahasiswa dan alat masih kosong dan harus ditambahkan lewat menu.

## Menu utama

| No | Menu |
|---|---|
| 1 | Kelola mahasiswa |
| 2 | Kelola peralatan (termasuk kategori) |
| 3 | Buat transaksi peminjaman |
| 4 | Tampilkan semua transaksi |
| 5 | Proses pengembalian alat |
| 6 | Cari transaksi berdasarkan mahasiswa |
| 7 | Tampilkan alat tersedia |
| 8 | Tampilkan alat sedang dipinjam |
| 9 | Tampilkan alat rusak/pemeliharaan |
| 10 | Riwayat peminjaman mahasiswa |
| 11 | Statistik peminjaman |
| 12 | Selesaikan pemeliharaan alat |
| 0 | Keluar |

## Alur program

### Alur umum

```text
main.py
  └─ MenuApp()
       ├─ buat MahasiswaManager, PeralatanManager, TransaksiManager
       ├─ sambungkan pengecekan transaksi aktif ke PeralatanManager
       └─ isi kategori awal
  └─ jalankan()
       └─ loop: tampilkan menu → baca pilihan → panggil method → ulangi
```

### Alur peminjaman (menu 3)

```text
Input NIM
  └─ mahasiswa ada?                                   tidak → gagal
Tampilkan alat yang tersedia
Input kode alat (pisah koma) dan lama pinjam
  └─ TransaksiManager.buatTransaksi() memeriksa berurutan:
       1. mahasiswa ada
       2. transaksi aktif mahasiswa kurang dari 2
       3. daftar alat tidak kosong
       4. tidak ada kode alat ganda
       5. lama pinjam 1–7 hari
       6. setiap alat ada dan masih tersedia
  └─ semua lolos?
       ├─ ya   → buat TRXxxx, tandai tiap alat "dipinjam",
       │         tambahkan ke transaksi aktif mahasiswa
       └─ tidak → pesan kesalahan, tidak ada data yang berubah
```

Semua validasi dilakukan lebih dulu, baru data diubah di akhir. Jadi kalau salah satu alat ternyata tidak tersedia, tidak ada alat lain yang sempat ikut tercatat dipinjam.

### Alur pengembalian (menu 5)

```text
Tampilkan transaksi aktif
Input ID transaksi
Tampilkan alat yang belum kembali
Input kode alat dan pilih kondisi (1 BAIK / 2 RUSAK_RINGAN / 3 RUSAK_BERAT)
  └─ prosesPengembalian()
       ├─ ItemPinjam.kembalikan()    → catat tanggal & kondisi
       │    └─ Peralatan.terimaKembali()
       │         ├─ BAIK   → alat langsung tersedia lagi
       │         └─ rusak  → alat masuk pemeliharaan
       └─ Transaksi.perbaruiStatus()
            ├─ masih ada alat belum kembali → SEBAGIAN_DIKEMBALIKAN
            └─ semua sudah kembali          → SELESAI
                                              (jatah transaksi mahasiswa berkurang)
```

Pengembalian bisa dilakukan bertahap. Selama masih ada alat yang belum kembali, transaksi tetap dianggap aktif dan tetap menghabiskan satu dari dua jatah transaksi mahasiswa itu.

### Alur alat rusak (menu 9 dan 12)

```text
Alat dikembalikan dengan kondisi RUSAK_RINGAN / RUSAK_BERAT
  └─ dalamPemeliharaan = True  → tidak lolos isTersedia(), tidak bisa dipinjam
Setelah diperbaiki → menu 12 → selesaikanPemeliharaan()
  └─ kondisi kembali BAIK, dalamPemeliharaan = False → alat tersedia lagi
```

## Aturan bisnis

- Satu transaksi boleh berisi lebih dari satu alat, tapi kode alat tidak boleh dobel.
- Satu mahasiswa maksimal punya 2 transaksi aktif sekaligus.
- Lama peminjaman 1 sampai 7 hari.
- Batas kembali dihitung dari tanggal pinjam ditambah lama hari.
- Alat hanya bisa dipinjam jika kondisinya baik, tidak sedang dipinjam, dan tidak dalam pemeliharaan.
- Alat yang dikembalikan dalam keadaan rusak harus lewat menu pemeliharaan dulu sebelum bisa dipinjam lagi.
- Mahasiswa tidak bisa dihapus selama masih punya transaksi aktif.
- Alat tidak bisa dihapus kalau sedang dipinjam atau masih tercatat di transaksi aktif.
- Alat tidak bisa diedit selama sedang dipinjam.
- Transaksi aktif yang melewati batas kembali ditandai `TERLAMBAT` beserta jumlah harinya. Tidak ada denda atau pembatasan otomatis, hanya penanda di tampilan.

## Statistik

Menu 11 menampilkan ringkasan (total, aktif, selesai, jumlah mahasiswa dan alat terdaftar), lalu dua peringkat teratas lengkap dengan grafik batang: 5 alat yang paling sering dipinjam dan 5 mahasiswa yang paling sering meminjam. Kalau datanya sudah dihapus, namanya tampil sebagai `(dihapus)`.

## Keterbatasan

- Data tidak tersimpan setelah program ditutup.
- Pengecekan terlambat memakai tanggal sistem (`date.today()`), jadi hasilnya bergantung pada jam komputer.
- Program berjalan untuk satu pengguna di satu terminal, tidak ada sistem login atau peran.

## Catatan UML

Nama class dan method utama dipertahankan seperti di diagram: `MenuApp`, `MahasiswaManager`, `TransaksiManager`, `PeralatanManager`, `Mahasiswa`, `Transaksi`, `Peralatan`, `Kategori`, `ItemPinjam`, `StatusTransaksi`, dan `KondisiAlat`. Ada beberapa method tambahan yang tidak ada di diagram, seperti `selesaikanPemeliharaan`, `adaAlatDalamTransaksiAktif`, dan `statistik`, untuk keperluan validasi, pemeliharaan, dan statistik.
