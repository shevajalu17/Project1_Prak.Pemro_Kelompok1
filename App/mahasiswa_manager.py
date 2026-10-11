from .entities import Mahasiswa


class MahasiswaManager:
    def __init__(self):
        self.data: dict[str, Mahasiswa] = {}

    def tambah(self, nim: str, nama: str, noHp: str) -> bool:
        nim, nama, noHp = nim.strip(), nama.strip(), noHp.strip()
        if not nim or not nama or not noHp or nim in self.data:
            return False
        self.data[nim] = Mahasiswa(nim, nama, noHp)
        return True

    def edit(self, nim: str, nama: str, noHp: str) -> bool:
        mhs = self.getByNim(nim)
        if not mhs or not nama.strip() or not noHp.strip():
            return False
        mhs.ubahData(nama.strip(), noHp.strip())
        return True

    def hapus(self, nim: str) -> bool:
        mhs = self.getByNim(nim)
        if not mhs or mhs.statusAktifPeminjaman:
            return False
        del self.data[nim]
        return True

    def cari(self, kataKunci: str) -> list[Mahasiswa]:
        kunci = kataKunci.strip().casefold()
        return [m for m in self.data.values()
                if kunci in m.nim.casefold() or kunci in m.nama.casefold()]

    def getByNim(self, nim: str) -> Mahasiswa | None:
        return self.data.get(nim)

    def tampilkanSemua(self) -> list[Mahasiswa]:
        return list(self.data.values())
