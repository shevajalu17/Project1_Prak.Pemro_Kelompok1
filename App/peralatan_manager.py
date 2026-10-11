from .entities import Peralatan, Kategori, KondisiAlat


class PeralatanManager:
    def __init__(self):
        self.data: dict[str, Peralatan] = {}
        self.kategori: dict[str, Kategori] = {}
        self.adaDalamTransaksiAktif = lambda kode: False

    def tambahKategori(self, idKategori: str, namaKategori: str) -> bool:
        idKategori, namaKategori = idKategori.strip(), namaKategori.strip()
        if not idKategori or not namaKategori or idKategori in self.kategori:
            return False
        self.kategori[idKategori] = Kategori(idKategori, namaKategori)
        return True

    def getKategori(self, idKategori: str) -> Kategori | None:
        return self.kategori.get(idKategori)

    def tambahAlat(self, kode: str, nama: str, idKategori: str) -> bool:
        kode, nama = kode.strip(), nama.strip()
        kategori = self.getKategori(idKategori)
        if not kode or not nama or kode in self.data or not kategori:
            return False
        self.data[kode] = Peralatan(kode, nama, kategori)
        return True

    def editAlat(self, kode: str, nama: str, idKategori: str) -> bool:
        alat, kategori = self.data.get(kode), self.getKategori(idKategori)
        if not alat or not kategori or not nama.strip() or alat.dipinjam:
            return False
        alat.ubahData(nama.strip(), kategori)
        return True

    def hapusAlat(self, kode: str) -> bool:
        alat = self.data.get(kode)
        if not alat or alat.dipinjam or self.adaDalamTransaksiAktif(kode):
            return False
        del self.data[kode]
        return True

    def cariAlat(self, kataKunci: str) -> list[Peralatan]:
        kunci = kataKunci.strip().casefold()
        return [a for a in self.data.values()
                if kunci in a.kodeAlat.casefold()
                or kunci in a.namaAlat.casefold()
                or kunci in a.kategori.namaKategori.casefold()]

    def daftarTersedia(self) -> list[Peralatan]:
        return [a for a in self.data.values() if a.isTersedia()]

    def daftarDipinjam(self) -> list[Peralatan]:
        return [a for a in self.data.values() if a.dipinjam]

    def daftarRusak(self) -> list[Peralatan]:
        return [a for a in self.data.values()
                if a.kondisi != KondisiAlat.BAIK or a.dalamPemeliharaan]

    def daftarSemua(self) -> list[Peralatan]:
        return list(self.data.values())

    def selesaikanPemeliharaan(self, kode: str) -> bool:
        alat = self.data.get(kode)
        if not alat or not alat.dalamPemeliharaan or alat.dipinjam:
            return False
        alat.kondisi = KondisiAlat.BAIK
        alat.dalamPemeliharaan = False
        return True
